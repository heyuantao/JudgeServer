#-*- coding=utf-8 -*-
from utils import Singleton
from utils.app_exceptions import QueueFullException, MessageException
from uuid import uuid4
from datetime import datetime,timedelta
from config import config
from enum import Enum
import redis
import logging
import json
import traceback

logger = logging.getLogger(__name__)


class ProblemJudgeStatus(Enum):
    waiting=0; judging=1; judged=2;


class ProblemJudgeResultStatus(Enum):
    WT0=0; WT1=1; CI=2; RI=3; AC=4; PE=5; WA=6; TL=7; ML=8; OL=9; RE=10; CE=11; CO=12; TR= 13;


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
  'result' :{'status':'','message':''}
}
The 'judge' field store the information for 'judge client' and the 'web client'. The 'status' is the field for 'judge client'.
The 'result' field is use by 'judge client'for store judge result and judge information when error happen.
'''

class ProblemRecored:
    problem_judge_status_list = [key for key in ProblemJudgeStatus.__members__]  #the judger status for problem
    problem_judge_result_status_list = [key for key in ProblemJudgeResultStatus.__members__]  # Please reference with "OJCLIENT/Core/Judge.h" in OJCLIENT repo for judge_result_status_list

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
        if judge_dict.get('status') not in self.problem_judge_status_list:
            raise MessageException('The status :{} is not in self.problem_judge_status_list'.format(judge_dict.get('status')))

        self.data['judge']['problem_id'] = judge_dict.get('problem_id', '')
        self.data['judge']['secret'] = judge_dict.get('secret', '')
        self.data['judge']['status'] = judge_dict.get('status', '')

    def updateResult(self, result_dict):
        assert type(result_dict) == dict
        self.data['result']['status'] = result_dict.get('status', '')
        self.data['result']['message'] = result_dict.get('message', '')

    def getProblemJudgeResult(self):
        return self.data['result']

    def getProblemJudge(self):
        return self.data['judge']



