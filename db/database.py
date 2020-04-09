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

@Singleton
class Database:
    def __init__(self, host='127.0.0.1', port=6379 , db=0):
        self.host = host
        self.port = port
        self.db = db

        #定义各种列队的别名
        self.unsloved_problem_list_prefix = "unsloved_list:"  # 用户上传但未处理的题目，存放编号
        self.sloving_problem_list_prefix  = "sloving_list:"   # 用户上传正在处理的，存放编号
        self.sloved_problem_list_prefix   = "sloved_list:"    # 用户上传后已经解决的题目，存放编号

        
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

    #