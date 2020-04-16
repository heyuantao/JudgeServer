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
from db import Database
import logging

from utils import MessageException

logger = logging.getLogger(__name__)

db = Database()

def api_test_judgeclient():
    try:
        pending = request.form.get('getpending')
        lang_set = request.form.get('oj_lang_set')
        max_running = request.form.get('max_running')

        #print("This is post value !")
        #print(pending)
        #print(lang_set)
        #print(max_running)
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
            #raise Exception(str(len(request.args)))
            logger.critical('Unsupport method in judgeclient_views.api_problem_judge_common_view() !')
            return jsonify({'status': 'error', 'message': 'Unknow method !'}), status.HTTP_400_BAD_REQUEST
    except ValueError as e:
        logger.critical('Unknow method in judgeclient_views.api_problem_judge_common_view() !')
        logger.critical(traceback.format_exc())
        return jsonify({'status': 'error', 'message': 'Method error !'}), status.HTTP_400_BAD_REQUEST
    except Exception as e:
        logger.critical('Unknow error happend in judgeclient_views.api_problem_judge_common_view() !')
        logger.critical(traceback.format_exc())
        return jsonify({'status': 'error', 'message': 'Unknow error happend !'}), status.HTTP_400_BAD_REQUEST


def _get_jobs_sub_view(request):
    lang_set_str = request.form.get('oj_lang_set', '')
    max_running_str = request.form.get('max_running', '')
    if lang_set_str=='' or max_running_str=='':
        logger.error('lang_set or max_runing is empty in  judgeclient_views._get_jobs_sub_view() !')
        return jsonify({'status': 'error', 'message': 'lang_set or max_runing is empty'}), status.HTTP_400_BAD_REQUEST
    # now all the lang is support in judge client
    lang_set_int_list = [int(lang) for lang in lang_set_str.split(',')]
    max_runing_int = int(max_running_str)
    problem_id_str_list = db.get_problem_id_str_list_to_slove_by_count(count=max_runing_int)

    db.put_problem_id_str_list_into_sloving_queue(problem_id_str_list)
    #return problem id split by nextline
    return_content = ''
    for problem_id_str in problem_id_str_list:
        return_content = return_content + problem_id_str + '\n'
    return return_content,status.HTTP_200_OK


def _update_solution_sub_view(request):
    pass

def _add_compile_error_information_sub_view(request):
    pass

def _get_solution_sub_view(request):
    pass

#get problem_id,user_id,lang_id by solubion_id
def _get_solution_information_sub_view(request):
    try:
        solution_id_str = request.form.get('sid', '')
        if solution_id_str == '':
            logger.error('Solution id is empty in  judgeclient_views._get_solution_information_sub_view() !')
            return jsonify({'status': 'error', 'message': 'Solution id is empty !'}), status.HTTP_400_BAD_REQUEST

        return_content = ''
        return_content = return_content + '{problem_id_str}\n'.format(problem_id_str=solution_id_str)
        #lang_extension_str = db.get_lang_extension_by_problem_id(solution_id_str)
        return_content = return_content + '{user_id}\n'.format(user_id='judgeserver')
        return_content = return_content + '{lang_id}\n'.format(lang_id=db.get_lang_id_by_by_problem_id(solution_id_str))
        return return_content,status.HTTP_200_OK
    except MessageException as e:
        return "", status.HTTP_400_BAD_REQUEST

#get time_limit,mem_limit,isspj information by problem
def _get_problem_information_sub_view(request):
    try:
        problem_id_str = request.form.get('pid', '')
        if problem_id_str == '':
            logger.error('Problem id is empty in  judgeclient_views._get_problem_information_sub_view() !')
            return jsonify({'status': 'error', 'message': 'Problem id is empty !'}), status.HTTP_400_BAD_REQUEST

        problem_dict = db.get_problem_dict_by_problem_id(problem_id_str)
        isspj_str="0"
        return_content = '{time_limit}\n{mem_limit}\n{isspj}\n'.format(problem_dict['time_limit'],problem_dict['mem_limit'],isspj_str)
        return return_content
        return problem_dict,status.HTTP_200_OK
    except MessageException as e:
        return "", status.HTTP_400_BAD_REQUEST

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




