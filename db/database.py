#-*- coding=utf-8 -*-
#from .redis import AppRedisClient
from utils import Singleton,MessageException
from uuid import uuid4
from datetime import datetime,timedelta
from config import config
import redis
import logging
import json
import traceback

logger = logging.getLogger(__name__)

#Redis在使用的时候不要持久化，防止出现数据不一致的场景
@Singleton
class Database:
    def __init__(self, host='127.0.0.1', port=6379 , db=0):
        self.host = host
        self.port = port
        self.db = db

        #定义各种列队的别名
        self.unsolved_problem_list_prefix = "unsolved_list"  # 用户上传但未处理的题目，存放编号
        self.solving_problem_list_prefix  = "solving_list"   # 用户上传正在处理的，存放编号
        #self.solved_problem_list_prefix   = "solved_list:"    # 用户上传后已经解决的题目，存放编号

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
    def _put_problem_id_into_unsolved_list(self,problem_id):
        self.connection.lpush(self.unsolved_problem_list_prefix,problem_id)

    #从队列中取出一个题目编号，并将之从队列中删除，这个操作发生在判题机开始判题的时候
    def _get_problem_id_from_unsolved_list(self):
        self.connection.rpop(self.unsolved_problem_list_prefix)

    #将一个题目编号加入到等待列队中，这个操作发生在判题机开始判题的时候
    def _put_problem_id_into_solving_list(self,problem_id):
        self.connection.lpush(self.solving_problem_list_prefix, problem_id)

    #将一个题目从等待队列中移除，这个操作实在判题任务结束的时候发生
    def _remove_problem_id_from_solving_list(self,problem_id):
        self.connection.lrem(self.solving_problem_list_prefix, 0, problem_id)

    #添加一个问题
    def add_problem(self, problem_json):
        problem_id = self.connection.incr(self.problem_count_key)



