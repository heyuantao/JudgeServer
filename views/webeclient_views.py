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

#第三方系统POST的数据会被保存在数据库中，并等待判题机处理
#POST的数据格式如下，
# {'code':'xxx','lang':'x',test_case:[{'input':'xxx','output':'xxxx'},{'input':'xxx','output':'xxxx'},'notify':'url to notify']}
#各字段的说明：
#code为用户的代码，该字段必须存在。
#lang为语言类型，该字段必须存在。
#test_case为测试用例,该字段必须存在。字段内容以数组的方式进行存储；每一个测试用例包含了input和output选项，input是要输入的数据，output为期望输出的数据
#notify为回调函数的网址，该字段不强制存在。如果存在，服务器将会向该网址发送GET请求，标识判题已经完成，第三方客户端即可进行查询
#the return data is，
#{'solution_id':234234234,'task':'xdfsfsdfdsf'}
def api_solutions_view():

    pass

#