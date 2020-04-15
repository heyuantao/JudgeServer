#-*- coding=utf-8 -*-
#判题机对应的接口测试
import os
import sys
import json
import pytest

sys.path.append('..')
from App_JudgeServer import application

POST_URL = '/api/v1/judgeclient/test/?getpending=2'
TOKEN_VALUE = 'UseMyAPIService'


@pytest.fixture
def client():
    application.config['TESTING'] = True
    with application.test_client() as client:
        yield client


def test_get_jobs_sub_view(client):
    form_dict = {}
    form_dict['getpending'] = '1'
    form_dict['oj_lang_set'] = '0,1,2'
    form_dict['max_running'] = '2'

    headers = {'Content-Type': 'application/json', 'Authorization': 'Token ' + TOKEN_VALUE}
    response = client.post(POST_URL, data =form_dict, headers=headers)

    response_content = response.data.decode()
    print(response_content)
    assert True==False
    #assert response_content['status'] == ''