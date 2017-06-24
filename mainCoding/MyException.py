#coding=utf-8
'''
Created on 2017年4月20日
异常类
'''

class MyException(Exception):
    
    def __init__(self,value):
        self.value = value
        pass
    
    def __str__(self):
        return self.value