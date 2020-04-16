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

        #the two queue use in judge
        self.unsolved_problem_queue_key = "unsolved_queue"  # this queue store the problem id which is waiting for judge
        self.solving_problem_queue_key  = "solving_queue"   # this queue store the problem is which is judging

        #this is the problem id,when user submit a task , add one to it
        self.problem_count_key = "count"

        try:
            logger.debug("Connect to redis ... in Database.__init__()")
            self.connection_pool = redis.ConnectionPool(host=self.host, port=self.port, db=self.db, decode_responses=True) #password
            self.connection = redis.StrictRedis(connection_pool=self.connection_pool)
        except Exception as e:
            msg_str = "Error in conncetion redis ! in Database.__init__()"
            logger.error(msg_str)
            raise MessageException(msg_str)

    #flask init this modules
    def init_app(self,app=None):
        logger.debug("Init database in Database.__init__()")
        logger.debug("Set the begin problem is to 100 !")
        self._init_problem_id_count(begin_value=1000)

    #--------------------------Handle the queue -----------------------------#
    #put a problem_id into unsolved_problem_queue,this function is called when a webclient submit a solution
    def _put_problem_id_into_unsolved_queue(self,problem_id_str):
        if (problem_id_str != None) and (problem_id_str != ""):
            self.connection.sadd(self.unsolved_problem_queue_key,problem_id_str)

    #get a problem_id from queue and remove it from queue. This function is call when a problem_id going to be judged
    def _get_problem_id_from_unsolved_queue(self):
        return self.connection.spop(self.unsolved_problem_queue_key)

    #add a problem_id into sloving queue. this function is called when a problem_id is judging
    def _put_problem_id_into_solving_queue(self,problem_id_str):
        if (problem_id_str != None) and (problem_id_str !=""):
            self.connection.sadd(self.solving_problem_queue_key, problem_id_str)

    #remove a problem_id from sloving queue .this function is called when judge is finished
    def _remove_problem_id_from_solving_queue(self,problem_id_str):
        return self.connection.srem(self.solving_problem_queue_key, problem_id_str)

    #Check if two queue is full,this problem my happen when judge client is not work or to many problem submit
    def _check_queue_is_full(self):
        if self.connection.scard(self.unsolved_problem_queue_key) >= 1000:
            logger.critical('Something went wrong, because unsolved_problem_queue is full !')
            return True
        elif self.connection.scard(self.solving_problem_queue_key) >= 1000:
            logger.critical('Something went wrong, because solving_problem_queue is full !')
            return True
        else:
            return False

    #problem will expire ,but problem is my store in two queue ,so delete is .This my happen when judge client is not inline
    def _remove_problem_from_queue_by_problem_id(self, problem_id_str):
        self._get_problem_id_from_unsolved_queue(problem_id_str)
        self._remove_problem_id_from_solving_queue(problem_id_str)

    # --------------------------Handle the queue end---------------------------#



    # --------------------------Handle the problem count--------------------------#
    def _get_unused_problem_id_str(self):
        problem_id_str = str(self.connection.incr(self.problem_count_key))
        return problem_id_str

    def _init_problem_id_count(self,begin_value=1000):
        if not self.connection.exists(self.problem_count_key):  #keep the value if this server restart
            self.connection.set(self.problem_count_key, 1000)
    # ---------------------Handle the problem count  end--------------------------#



    # ---------------------Handle the operation for problem------------------------#
    #Add a problem into redis and return the dict for problem : {"problem_id":problem_id_str, "secret":secret}
    def add_problem(self, problem_dict):
        assert type(problem_dict) == dict

        if self._check_queue_is_full():
            raise QueueFullException("One of queue is full !")

        problem_id_str = self._get_unused_problem_id_str()
        secret = str(uuid4().hex)
        judge_dict = {'problem_id':problem_id_str,'secret':secret,'status':str(ProblemJudgeStatusEnum.waiting)}

        problem_record = ProblemRecored()
        problem_record.updateProblem(problem_dict)
        problem_record.updateJudge(judge_dict)

        self.connection.set(problem_id_str,problem_record.toString())
        self.connection.expire(problem_id_str,timedelta(minutes=30))       #record will expire at 1 hour later
        self._put_problem_id_into_unsolved_queue(problem_id_str)

        return {"problem_id":problem_id_str, "secret":secret}



    def get_problem_judge_and_result_status(self, problem_id_str, secret):  #web client use this to get the judge status of a given problem
        if self.connection.exists(problem_id_str):
            record_string_in_redis = self.connection.get(problem_id_str)

            problem_record = ProblemRecored()
            problem_record.fromString(record_string_in_redis)
            problem_judge = problem_record.getJudge()

            problem_secret = problem_judge["secret"]
            if secret != problem_secret:
                raise MessageException('Secret not match with is problem !')
            else:
                problem_record.data.pop('problem')  #return the ProblemRecord without problem field
                return problem_record.data
        else:
            self._remove_problem_from_queue_by_problem_id(problem_id_str)
            logger.error('Problem \"{}\" not exist , delete from waiting and judging queue !'.format(problem_id_str))
            raise MessageException('The problem is not exist !')

    #-------------------Return ProblemRecord information by problem_id -----------------#

    def get_problem_dict_by_problem_id(self, problem_id_str):  #This function is call by judge client
        if self.connection.exists(problem_id_str):
            record_string_in_redis = self.connection.get(problem_id_str)

            problem_record = ProblemRecored()
            problem_record.fromString(record_string_in_redis)
            problem_dict = problem_record.getProblem()
            return problem_dict
        else:
            logger.error('Problem \"{}\" not exist when call judgeclient_view.get_problem_dict_by_problem_id() !'.format(problem_id_str))
            raise MessageException('The problem is not exist !')


    def get_judge_dict_by_problem_id(self, problem_id_str): #This function is call by judge client
        if self.connection.exists(problem_id_str):
            record_string_in_redis = self.connection.get(problem_id_str)

            problem_record = ProblemRecored()
            problem_record.fromString(record_string_in_redis)
            judge_dict = problem_record.getJudge()
            return judge_dict
        else:
            logger.error('Problem \"{}\" not exist when call judgeclient_view.get_judge_dict_by_problem_id() !'.format(problem_id_str))
            raise MessageException('The problem is not exist !')


    def get_result_dict_by_problem_id(self, problem_id_str):  #This function is call by judge client
        if self.connection.exists(problem_id_str):
            record_string_in_redis = self.connection.get(problem_id_str)

            problem_record = ProblemRecored()
            problem_record.fromString(record_string_in_redis)
            result_dict = problem_record.getJudgeResult()
            return result_dict
        else:
            logger.error('Problem \"{}\" not exist when call judgeclient_view.get_result_dict_by_problem_id() !'.format(problem_id_str))
            raise MessageException('The problem is not exist !')

    # -------------------Return ProblemRecord information by problem_id end-------------#

    def get_problem_id_str_list_to_slove_by_count(self, count=2, lang_set_extension_list=None):  #fetch a problem for judger, lang_set_extension_list is not use
        problem_list = []
        for i in range(count):
            one_problem = self._get_problem_id_from_unsolved_queue()
            #print(one_problem)
            if one_problem == None:
                break
            else:
                problem_list.append(str(one_problem))
        print(problem_list)
        return problem_list


    def put_problem_id_str_list_into_sloving_queue(self,problem_id_str_list):  # add problem list into sloving queue
        assert type(problem_id_str_list) == list
        for problem_id_str in problem_id_str_list:
            self._put_problem_id_into_solving_queue(problem_id_str)


    def get_lang_extension_by_problem_id(self,problem_id_str): ##to be continue
        #print("problem id:{}".format(problem_id_str))
        if self.connection.exists(problem_id_str):
            record_string_in_redis = self.connection.get(problem_id_str)

            problem_record = ProblemRecored()
            problem_record.fromString(record_string_in_redis)
            lang_extension_str = problem_record.getProblem()['lang']
            return lang_extension_str
            #return ProblemRecored.getLangExtensionNameById(int(problem_id))
        else:
            logger.critical('Problem \"{}\" not exist ! Error happen in Database.get_lang_extension_by_problem_id()'.format(problem_id_str))
            raise MessageException('Problem not exist when get its extension !')
            #clear_the_problem_in_queue()


    def get_lang_id_by_by_problem_id(self,problem_id_str):     ##to be continue
        #print("problem id:{}".format(problem_id_str))
        lang_extension_str = self.get_lang_extension_by_problem_id(problem_id_str)
        return ProblemRecored.getLangIdByExtensionName(lang_extension_str)


