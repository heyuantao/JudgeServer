#-*- coding=utf-8 -*-
#该文件处理第三方客户端的接口函数,即从第三方客户端提交过来的题目和相应的测试数据，
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

#return software information
def api_version_info_view():
    return jsonify({'software':'JudgeServer','version':'0.1'})


def api_solutions_view():
    code = request.json.get('code')
    lang = request.json.get('lang')
    test_cases = request.json.get('test_cases')
    notify = request.json.get('notify')
    print(type(request.json))
    print(request.json)
    return jsonify({'solution': 1000, 'task':'32423xdsfwer'}), status.HTTP_201_CREATED

#