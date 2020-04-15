#-*- coding=utf-8 -*-
#判题机对应的接口测试
import os
import sys
import json
import pytest

sys.path.append('..')
from App_JudgeServer import application

TOKEN_VALUE = 'UseMyAPIService'

@pytest.fixture
def client():
    application.config['TESTING'] = True
    with application.test_client() as client:
        yield client


def test_get_jobs_sub_view(client):
    form_dict = {}
    form_dict['getpending'] = '1'
    form_dict['oj_lang_set'] = '0,1,2,3'
    form_dict['max_running'] = '3'

    headers = {'Content-Type': 'application/json', 'Authorization': 'Token ' + TOKEN_VALUE}
    response = client.post('/api/v1/judgeclient/test/', data =form_dict, headers=headers, mimetype = "application/x-www-form-urlencoded")  #multipart/form-data also work

    response_content = json.loads(response.data.decode())
    print(type(response_content))
    print(response_content)
    assert response_content['status'] == 'success'


def test_get_jobs_sub_view(client):
    form_dict = {}
    form_dict['getpending'] = '1'
    form_dict['oj_lang_set'] = '0,1,2,3'
    form_dict['max_running'] = '3'

    headers = {'Content-Type': 'application/json', 'Authorization': 'Token ' + TOKEN_VALUE}
    response = client.post('/api/v1/judgeclient/problem_judge/', data =form_dict, headers=headers, mimetype = "application/x-www-form-urlencoded")  #multipart/form-data also work

    #response_content = json.loads(response.data.decode())
    response_content = response.data.decode()
    print(type(response_content))
    print(response_content)
    lines = response_content.split()
    assert len(lines)==3