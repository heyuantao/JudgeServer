#-*- coding=utf-8 -*-
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

def api_software_info_view():
    return jsonify({'software':'JudgeServer','version':'0.1'})