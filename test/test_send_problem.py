#-*- coding=utf-8 -*-
import os
import requests
import json

POST_URL = 'http://127.0.0.1:5000/api/v1/webclient/solution/'
TOKEN_VALUE = 'UseMyAPIService'

def test_case1():
    print("Run test case1 ！")
    problem = {}
    source_code_file_path = "./data/code1.c"
    source_code_file = open(source_code_file_path);
    source_code_file_content = source_code_file.read();
    #print(source_code_file_content)
    problem['code']=source_code_file_content
    problem['lang']='c'
    problem['notify']=''

    test_cases=[]
    test_cases.append({'input':'1', 'output':'2'})
    test_cases.append({'input':'2', 'output':'3'})
    problem['test_cases'] = test_cases

    #print(problem)
    print("Sending ...")
    print(json.dumps(problem))
    #requests.post(POST_URL,data=json.dumps(problem))
    headers = {'Content-Type': 'application/json','Authorization':'Token '+TOKEN_VALUE}
    res = requests.post(POST_URL,  headers=headers, data=json.dumps(problem))
    print("")
    print("Received ...")
    print(res.text)
    print(res.status_code)

if __name__=="__main__":
    test_case1()