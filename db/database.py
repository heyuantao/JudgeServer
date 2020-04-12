#-*- coding=utf-8 -*-
#from .redis import AppRedisClient
from utils import Singleton
from utils.app_exceptions import QueueFullException, MessageException
from db.models import ProblemRecored,ProblemJudgeStatusEnum,ProblemJudgeResultStatusEnum
from uuid import uuid4
from datetime import datetime,timedelta
from config import config
import redis
import logging
import json
import traceback


logger = logging.getLogger(__name__)

#Please not presistent data
@Singleton
class Database:
    def __init__(self, host='127.0.0.1', port=6379 , db=0):
        self.host = host
        self.port = port
        self.db = db

        #定义各种列队的别名
        self.unsolved_problem_queue_key = "unsolved_queue"  # 用户上传但未处理的题目，存放编号
        self.solving_problem_queue_key  = "solving_queue"   # 用户上传正在处理的，存放编号
        #self.solved_problem_queue_prefix   = "solved_list:"    # 用户上传后已经解决的题目，存放编号

        #定义问题编号，使用自增的方式,在一开始初始化为1000
        self.problem_count_key = "count"

        #定义题目存入的
        try:
            logger.debug("Connect to redis ... in Database.__init__()")
            self.connection_pool = redis.ConnectionPool(host=self.host, port=self.port, db=self.db, decode_responses=True) #password
            self.connection = redis.StrictRedis(connection_pool=self.connection_pool)
        except Exception as e:
            msg_str = "Error in conncetion redis ! in Database.__init__()"
            logger.error(msg_str)
            raise MessageException(msg_str)

    #flask 初始化调用该函数
    def init_app(self,app=None):
        logger.debug("Init database in Database.__init__()")
        logger.debug("Set the begin problem is to 100 !")
        self.connection.set(self.problem_count_key, 1000)

    #将一个题目编号加入到等待列队中，这个操作发生在用户提交判题代码的时候
    def _put_problem_id_into_unsolved_queue(self,problem_id_str):
        self.connection.sadd(self.unsolved_problem_queue_key,problem_id_str)

    #从队列中取出一个题目编号，并将之从队列中删除，这个操作发生在判题机开始判题的时候
    def _get_problem_id_from_unsolved_queue(self):
        self.connection.srem(self.unsolved_problem_queue_key)

    #将一个题目编号加入到等待列队中，这个操作发生在判题机开始判题的时候
    def _put_problem_id_into_solving_queue(self,problem_id_str):
        self.connection.sadd(self.solving_problem_queue_key, problem_id_str)

    #将一个题目从等待队列中移除，这个操作实在判题任务结束的时候发生
    def _remove_problem_id_from_solving_queue(self,problem_id_str):
        self.connection.srem(self.solving_problem_queue_key, problem_id_str)

    #检查两个判题的队列是否是满的，如果是满的说明有大量任务待完成，可能是判题机出了问题，应拒绝提交
    def _check_queue_is_full(self):
        if self.connection.smembers(self.unsolved_problem_queue_key) == 1000:
            return True
        elif self.connection.smembers(self.solving_problem_queue_key) == 1000:
            return True
        else:
            return False

    #添加一个问题
    #流程为获得新的题目编号，然后将题目内容放在会过期的key:value中，将题目加入到等待队列中
    #返回一个对象，内容为题目的编号和task的编号
    def add_problem(self, problem_dict):
        assert type(problem_dict) == dict

        if self._check_queue_is_full():
            raise QueueFullException("One of queue is full !")

        problem_id_str = str(self.connection.incr(self.problem_count_key))
        secret = str(uuid4().hex)

        problem_record = ProblemRecored()
        problem_record.updateProblem(problem_dict)
        problem_record.updateJudge({'problem_id':problem_id_str,'secret':secret,'status':str(ProblemJudgeStatusEnum.waiting)})

        self.connection.set(problem_id_str,problem_record.toString())
        self.connection.expire(problem_id_str,timedelta(hours=1))       #record will expire at 1 hour later
        self._put_problem_id_into_unsolved_queue(problem_id_str)

        return {"problem_id":problem_id_str, "secret":secret}

    #客户端主动获得代码的执行状态
    def get_problem_status(self, problem_id_str, secret):
        if self.connection.exists(problem_id_str):
            record_string_in_redis = self.get(problem_id_str)

            problem_record = ProblemRecored()
            problem_record.fromString(record_string_in_redis)
            problem_judge = problem_record.getProblemJudge()

            #problem_id_str = problem_judge["problem_id"]
            problem_secret = problem_judge["secret"]
            if secret != problem_secret:
                raise MessageException('Secret not match with is problem !')
            else:
                return problem_judge
        else:
            raise MessageException('The problem is not exist !')
            #if self.connection.l





