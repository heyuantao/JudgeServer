#-*- coding=utf-8 -*-
#该文件处理第三方客户端的接口函数
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

#save the solution informatin into db(redis)
#the post data is :
# {'code':'xxx','lang':'x',test_case:[{'input':'xxx','output':'xxxx'},{'input':'xxx','output':'xxxx'},'notify':'url to notify']}
#the return data is:
#{'solution_id':234234234,'task':'xdfsfsdfdsf'}
def api_create_solution_view():
    pass

#