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
    #db_fd, flaskr.app.config['DATABASE'] = tempfile.mkstemp()

    application.config['TESTING'] = True

    with application.test_client() as client:
        #with application.app.app_context():
        #    application.init_db()
        yield client



def test_webclient_version(client):
    rv = client.get('/version')
    response_content = str(rv.data)
    print(response_content)
    assert '{"software":"JudgeServer","version":"0.1"}' in str(response_content)

def test_add_problem(client):
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

    response = client.post('/api/v1/webclient/solution/',data=problem_dict,headers=headers)

    print(response.data)
    assert True==False
