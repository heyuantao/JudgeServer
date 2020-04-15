#-*- coding=utf-8 -*-
#该文件处理第三方客户端的接口函数,即从第三方客户端提交过来的题目和相应的测试数据，
from flask import request, jsonify, current_app, stream_with_context, Response
from flask_api import status
from utils import MessageException, QueueFullException
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
        notify = request.json.get('notify')
        if code == None:
            raise MessageException('Code is empty !')
        if lang == None:
            raise MessageException('Lang is empty !')
        if test_cases == None:
            raise MessageException('Test_cases is empty !')
        for one_case in test_cases:
            try:
                input = one_case['input']
                output = one_case['output']
                if input == None:
                    raise MessageException('One input of testcase is empty !')
                if output == None:
                    raise MessageException('One input of testcase is empty !')
            except KeyError:
                raise MessageException('Test case key is incorrect !')


        #main logic
        return_dict = db.add_problem(request.json)
        return jsonify(return_dict), status.HTTP_201_CREATED
    except MessageException as e:
        return jsonify({'status':'error','message':str(e)}), status.HTTP_400_BAD_REQUEST
    except QueueFullException as e:
        return jsonify({'status': 'error', 'message': str(e)}), status.HTTP_400_BAD_REQUEST
    except Exception as e:
        logger.critical('Unknow error happend in webclient_views.api_solution_create_view() !')
        logger.critical(traceback.format_exc())
        return jsonify({'status': 'error', 'message': 'Unknow error happend !'}), status.HTTP_400_BAD_REQUEST


def api_solution_info_view():
    try:
        problem_id = request.json.get('problem_id')
        secret = request.json.get('secret')
        if problem_id == "":
            raise MessageException('One input of testcase is empty !')
        if secret == "":
            raise MessageException('One input of testcase is empty !')
        judged_result_dict = db.get_problem_status(problem_id, secret)
        return jsonify(judged_result_dict), status.HTTP_200_OK
    except MessageException as e:
        return jsonify({'status':'error','message':str(e)}), status.HTTP_400_BAD_REQUEST
    except Exception as e:
        logger.critical('Unknow error happend in webclient_views.api_solution_info_view() !')
        logger.critical(traceback.format_exc())
        return jsonify({'status': 'error', 'message': 'Unknow error happend !'}), status.HTTP_400_BAD_REQUEST