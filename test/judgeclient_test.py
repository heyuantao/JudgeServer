#-*- coding=utf-8 -*-
#判题机对应的接口测试
import os
import sys
import pytest

sys.path.append('..')
from App_JudgeServer import application

POST_URL = 'http://127.0.0.1:5000/api/v1/webclient/solution/'
TOKEN_VALUE = 'UseMyAPIService'

@pytest.fixture
def client():
    application.config['TESTING'] = True
    with application.test_client() as client:
        yield client


def test_api_version_info_view(client):
    rv = client.get('/version')
    response_content = str(rv.data)
    print(response_content)
    assert '{"software":"JudgeServer","version":"0.1"}' in str(response_content)

def test_api_solution_create_view(client):
    source_code_file_path = "./data/code1.c"
    source_code_file = open(source_code_file_path);
    source_code_file_content = source_code_file.read();
    problem_dict = {}
    problem_dict['code'] = source_code_file_content
    problem_dict['lang'] = 'c'
    problem_dict['notify'] = ''

    test_cases = []
    test_cases.append({'input': '1', 'output': '2'})
    test_cases.append({'input': '2', 'output': '3'})
    problem_dict['test_cases'] = test_cases

    headers = {'Content-Type': 'application/json', 'Authorization': 'Token ' + TOKEN_VALUE}

    response = client.post('/api/v1/webclient/solution/',json=problem_dict,headers=headers)

    response_content = response.get_json()
    print(response_content)
    assert response_content['problem_id'] != ''
    assert response_content['secret'] != ''
    #assert True==False

def test_api_solution_info_view(client):
    source_code_file_path = "./data/code1.c"
    source_code_file = open(source_code_file_path);
    source_code_file_content = source_code_file.read();
    problem_dict = {}
    problem_dict['code'] = source_code_file_content
    problem_dict['lang'] = 'c'
    problem_dict['notify'] = ''

    test_cases = []
    test_cases.append({'input': '1', 'output': '2'})
    test_cases.append({'input': '2', 'output': '3'})
    problem_dict['test_cases'] = test_cases

    headers = {'Content-Type': 'application/json', 'Authorization': 'Token ' + TOKEN_VALUE}
    response = client.post('/api/v1/webclient/solution/',json=problem_dict,headers=headers)

    response_content = response.get_json()
    problem_id_str = response_content['problem_id']
    secret = response_content['secret']


    headers = {'Content-Type': 'application/json', 'Authorization': 'Token ' + TOKEN_VALUE}
    response = client.post('/api/v1/webclient/solution/info', json={'problem_id':problem_id_str,'secret':secret}, headers=headers)
    response_content = response.get_json()
    print(response_content)

    problem_id_str = response_content['problem_id']
    status = response_content['status']
    assert status=='waiting'

