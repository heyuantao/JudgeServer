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

def add_problem(client,token):
    source_code_file_path = "./data/code1.c"
    source_code_file = open(source_code_file_path);
    source_code_file_content = source_code_file.read();
    problem_dict = {}
    problem_dict['code'] = source_code_file_content
    problem_dict['lang'] = 'c'
    problem_dict['notify'] = ''
    test_cases = []
    test_cases.append({'input': '1', 'output': '2'})
    problem_dict['test_cases'] = test_cases
    headers = {'Content-Type': 'application/json', 'Authorization': 'Token ' + token}
    response = client.post('/api/v1/webclient/solution/',json=problem_dict,headers=headers)
    response_content = response.get_json()
    new_add_problem_id_str =  response_content['problem_id']
    return new_add_problem_id_str


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
    add_problem(client, TOKEN_VALUE)
    add_problem(client, TOKEN_VALUE)
    add_problem(client, TOKEN_VALUE)

    form_dict = {}
    form_dict['getpending'] = '1'
    form_dict['oj_lang_set'] = '0,1,2,3'
    form_dict['max_running'] = '3'
    headers = {'Content-Type': 'application/json', 'Authorization': 'Token ' + TOKEN_VALUE}
    response = client.post('/api/v1/judgeclient/problem_judge/', data =form_dict, headers=headers, mimetype = "application/x-www-form-urlencoded")  #multipart/form-data also work
    response_content = response.data.decode()
    print(type(response_content))
    print(response_content)
    lines = response_content.split()
    assert len(lines)==3


def test_get_solution_information_sub_view(client):
    new_add_problem_id_str = add_problem(client, TOKEN_VALUE)

    #错误题目号码的测试
    form_dict = {}
    form_dict['getsolutioninfo'] = '1'
    form_dict['sid'] = '999'
    headers = {'Content-Type': 'application/json', 'Authorization': 'Token ' + TOKEN_VALUE}
    response = client.post('/api/v1/judgeclient/problem_judge/', data =form_dict, headers=headers, mimetype = "application/x-www-form-urlencoded")  #multipart/form-data also work
    assert response.status_code==400

    #正确题目号码的测试
    form_dict = {}
    form_dict['getsolutioninfo'] = '1'
    form_dict['sid'] = new_add_problem_id_str
    headers = {'Content-Type': 'application/json', 'Authorization': 'Token ' + TOKEN_VALUE}
    response = client.post('/api/v1/judgeclient/problem_judge/', data =form_dict, headers=headers, mimetype = "application/x-www-form-urlencoded")  #multipart/form-data also work
    response_content = response.data.decode()
    response_content_list = response_content.split()
    print(response_content_list)
    assert response_content_list[0] == new_add_problem_id_str
    assert response_content_list[1] == "judgeserver"
    assert response_content_list[2] == "0"


def test_get_problem_information_sub_view(client):
    new_add_problem_id_str = add_problem(client, TOKEN_VALUE)

    form_dict = {}
    form_dict['getprobleminfo'] = '1'
    form_dict['pid'] = new_add_problem_id_str
    headers = {'Content-Type': 'application/json', 'Authorization': 'Token ' + TOKEN_VALUE}
    response = client.post('/api/v1/judgeclient/problem_judge/', data =form_dict, headers=headers, mimetype = "application/x-www-form-urlencoded")  #multipart/form-data also work
    response_content = response.data.decode()
    response_content_list = response_content.split()
    print(response_content_list)
    response_content_list = response_content.split()
    assert len(response_content_list)==3


def test_add_runing_error_information_sub_view(client):
    new_add_problem_id_str = add_problem(client, TOKEN_VALUE)

    form_dict = {}
    form_dict['addreinfo'] = '1'
    form_dict['sid'] = new_add_problem_id_str
    form_dict['reinfo'] = 'The memory run out !'
    headers = {'Content-Type': 'application/json', 'Authorization': 'Token ' + TOKEN_VALUE}
    response = client.post('/api/v1/judgeclient/problem_judge/', data =form_dict, headers=headers, mimetype = "application/x-www-form-urlencoded")  #multipart/form-data also work
    response_content = response.data.decode()
    assert response_content==""


def test_add_compile_error_information_sub_view(client):
    new_add_problem_id_str = add_problem(client, TOKEN_VALUE)

    form_dict = {}
    form_dict['addceinfo'] = '1'
    form_dict['sid'] = new_add_problem_id_str
    form_dict['ceinfo'] = 'int define error'
    headers = {'Content-Type': 'application/json', 'Authorization': 'Token ' + TOKEN_VALUE}
    response = client.post('/api/v1/judgeclient/problem_judge/', data =form_dict, headers=headers, mimetype = "application/x-www-form-urlencoded")  #multipart/form-data also work
    response_content = response.data.decode()
    assert response_content==""