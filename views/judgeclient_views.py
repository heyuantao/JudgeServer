#-*- coding=utf-8 -*-
#该文件处理对应的判题机的接口函数
from flask import request, jsonify, current_app, stream_with_context, Response
from flask_api import status
import time
from werkzeug.urls import url_quote
import urllib.parse
import base64
import re
from datetime import datetime,timedelta
import traceback
from config import config
#from db import Database
import logging

logger = logging.getLogger(__name__)


def api_test_judgeclient():
    try:
        pending = request.form.get('getpending')
        lang_set = request.form.get('oj_lang_set')
        max_running = request.form.get('max_running')

        print("This is post value !")
        print(pending)
        print(lang_set)
        print(max_running)
        return jsonify({'status': 'success'})
    except Exception as e:
        logger.critical('Unknow error happend in judgeclient_views.api_get_jobs_view() !')
        logger.critical(traceback.format_exc())
        return jsonify({'status': 'error', 'message': 'Unknow error happend !'}), status.HTTP_400_BAD_REQUEST

#the judge client share one api use different post params
def api_problem_judge_common_view():
    try:
        if request.form.get('getpending', '') == '1':
            return _get_jobs_sub_view(request)
        elif request.form.get('update_solution', '') == '1':
            return _update_solution_sub_view(request)
        elif request.form.get('addceinfo', '') == '1':
            return _add_compile_error_information_sub_view(request)
        elif request.form.get('getsolution', '') == '1':
            return _get_solution_sub_view(request)
        elif request.form.get('getsolutioninfo', '') == '1':
            return _get_solution_information_sub_view(request)
        elif request.form.get('getprobleminfo', '') == '1':
            return _get_problem_information_sub_view(request)
        elif request.form.get('addreinfo', '') == '1':
            return _add_runing_error_information_sub_view(request)
        elif request.form.get('gettestdatalist', '') == '1':
            return _get_test_data_list_sub_view(request)
        elif request.form.get('gettestdata', '') == '1':
            return _get_test_data_sub_view(request)
        elif request.form.get('gettestdatadate', '') == '1':
            return _get_test_data_date_sub_view(request)
        elif request.form.get('updateproblem', '') == '1':
            return _update_problem_sub_view(request)
        elif request.form.get('updateuser', '') == '1':
            return _update_user_sub_view(request)
        elif request.form.get('checklogin', '') == '1':
            return _check_login_sub_view(request)
        else:
            logger.critical('Unsupport method in judgeclient_views.api_problem_judge_common_view() !')
            return jsonify({'status': 'error', 'message': 'Unknow method !'}), status.HTTP_400_BAD_REQUEST
    except ValueError as e:
        logger.critical('Unknow method in judgeclient_views.api_problem_judge_common_view() !')
        logger.critical(traceback.format_exc())
        return jsonify({'status': 'error', 'message': 'Unknow method !'}), status.HTTP_400_BAD_REQUEST
    except Exception as e:
        logger.critical('Unknow error happend in judgeclient_views.api_problem_judge_common_view() !')
        logger.critical(traceback.format_exc())
        return jsonify({'status': 'error', 'message': 'Unknow error happend !'}), status.HTTP_400_BAD_REQUEST


def _get_jobs_sub_view(request):
    pass

def _update_solution_sub_view(request):
    pass

def _add_compile_error_information_sub_view(request):
    pass

def _get_solution_sub_view(request):
    pass

def _get_solution_information_sub_view(request):
    pass

def _get_problem_information_sub_view(request):
    pass

def _add_runing_error_information_sub_view(request):
    pass

def _get_test_data_list_sub_view(request):
    pass

def _get_test_data_sub_view(request):
    pass

def _get_test_data_date_sub_view(request):
    pass

def _update_problem_sub_view(request):
    return jsonify({'status': 'success', 'message': 'nothing to do with update_problem !'}), status.HTTP_200_OK

def _update_user_sub_view(request):
    return jsonify({'status': 'success', 'message': 'nothing to do with update_user !'}), status.HTTP_200_OK

def _check_login_sub_view(request):
    return jsonify({'status': 'success', 'message': 'Login check passed !'}), status.HTTP_200_OK




