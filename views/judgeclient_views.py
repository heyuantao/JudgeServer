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

def api_get_jobs_view():
    try:
        pending = request.form.get('getpending')
        lang_set = request.form.get('oj_lang_set')
        max_running = request.form.get('max_running')

        #more work need tobe finished !
    except Exception as e:
        logger.critical('Unknow error happend in judgeclient_views.api_get_jobs_view() !')
        logger.critical(traceback.format_exc())
        return jsonify({'status': 'error', 'message': 'Unknow error happend !'}), status.HTTP_400_BAD_REQUEST


def api_test_judgeclient():
    try:
        print("run at this")
        print(request.form)
        raise Exception("no")
        return jsonify({'status': 'success'})
    except Exception as e:
        logger.critical('Unknow error happend in judgeclient_views.api_get_jobs_view() !')
        logger.critical(traceback.format_exc())
        return jsonify({'status': 'error', 'message': 'Unknow error happend !'}), status.HTTP_400_BAD_REQUEST
