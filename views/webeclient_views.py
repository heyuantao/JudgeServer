#-*- coding=utf-8 -*-
#该文件处理第三方客户端的接口函数,即从第三方客户端提交过来的题目和相应的测试数据，
from flask import request, jsonify, current_app, stream_with_context, Response
from flask_api import status
from utils import MessageException
import time
from werkzeug.urls import url_quote
import urllib.parse
import base64
import re
from datetime import datetime,timedelta
import traceback
from config import config
from db import Database
import logging

logger = logging.getLogger(__name__)

db = Database()


#return software information
def api_version_info_view():
    return jsonify({'software':'JudgeServer','version':'0.1'})


def api_solution_create_view():
    try:
        code = request.json.get('code')
        lang = request.json.get('lang')
        test_cases = request.json.get('test_cases')
        #notify = request.json.get('notify')
        if code=="":
            raise MessageException('Code is empty !')
        if lang=="":
            raise MessageException('Lang is empty !')
        if test_cases=="":
            raise MessageException('Test_cases is empty !')
        for one_case in test_cases:
            input = one_case['input']
            output = one_case['output']
            if input=="":
                raise MessageException('One input of testcase is empty !')
            if output=="":
                raise MessageException('One input of testcase is empty !')

        #main logic
        return_dict = db.add_problem(request.json)
        return jsonify(return_dict), status.HTTP_201_CREATED
    except MessageException as e:
        return jsonify({'status':'error','message':str(e)}), status.HTTP_400_BAD_REQUEST
    except Exception as e:
        logger.critical('Unknow error happend in webclient_views.api_solution_create_view() !')
        logger.critical(traceback.format_exc())
        return jsonify({'status': 'error', 'message': 'Unknow error happend !'}), status.HTTP_400_BAD_REQUEST


    #return jsonify({'solution': 1000, 'task':'32423xdsfwer'}), status.HTTP_201_CREATED

def api_solution_info_view():
    pass