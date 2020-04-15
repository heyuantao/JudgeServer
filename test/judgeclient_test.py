#-*- coding=utf-8 -*-
#判题机对应的接口测试
import pytest

def des(x):
    return x-1

def test_ans():
    assert des(5)==4
