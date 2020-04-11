#-*- coding=utf-8 -*-
from utils import Singleton
from utils.app_exceptions import QueueFullException, MessageException
from uuid import uuid4
from datetime import datetime,timedelta
from config import config
import redis
import logging
import json
import traceback


logger = logging.getLogger(__name__)

'''
The web client will post data and this will be save in redis，then the problem is waiting tobe judged
POST data is in flowing format
{'code':'xxx','lang':'x',test_cases:[{'input':'xxx','output':'xxxx'},{'input':'xxx','output':'xxxx'},'notify':'url to notify']}
Fields description
'code' is the field for store source code . Required !
'lang' is languare type such as c  java .Required !
'test_cases' is test cases which store many test case, every test case contain input and output. Required !
'notify' is call back url if the 'judge client' need notify if judge finished ! If this filed value is empty ,the Judge Server will not notify.

POST response in flowing format
{'problem_id':'234234234','secret':'xdfsfsdfdsf'}
'problem_id' is problem id assign for this problem .
'secret' is secret assign for this problem. this field is use for query result .

The software store more informat in redis.
{
  'problem':{'code':'xxx','lang':'x','test_cases':[{'input':'xxx','output':'xxxx'},{'input':'xxx','output':'xxxx'}],'notify':'url to notify'},
  'judge'  :{'problem_id':'234234234','secret':'xdfsfsdfdsf','status':'waiting'},
  'result' :{'status':'OL','message':''}
}
'''


class ProblemRecored:
    def __init__(self):
        self.data = {}
        self.data['problem'] = {'code': '', 'lang': '', 'test_cases': [{'input': '', 'output': ''}, ], 'notify': ''}
        self.data['judge'] = {'problem_id': '', 'secret': '', 'status': ''}
        self.data['result'] = {'status': '', 'message': ''}

    def toString(self):
        return json.dumps(self.data)

    def fromString(self,data_str):
        self.data = json.loads(data_str)

    def updateProblem(self, problem_dict):
        assert type(problem_dict) == dict
        self.data['problem']['code'] = problem_dict.get('code','')
        self.data['problem']['lang'] = problem_dict.get('lang', '')
        self.data['problem']['notify'] = problem_dict.get('notify', '')
        new_test_cases=[]
        for item in problem_dict.get('test_cases',[]):
            new_test_cases.append({'input':item.get('input',''),'output':item.get('output','')})
        self.data['problem']['test_cases'] = new_test_cases

    def updateJudge(self, judge_dict):
        assert type(judge_dict) == dict
        self.data['judge']['problem_id'] = judge_dict.get('problem_id', '')
        self.data['judge']['secret'] = judge_dict.get('secret', '')
        self.data['judge']['status'] = judge_dict.get('status', '')

    def updateResult(self, result_dict):
        assert type(result_dict) == dict
        self.data['result']['status'] = result_dict.get('status', '')
        self.data['result']['message'] = result_dict.get('message', '')


