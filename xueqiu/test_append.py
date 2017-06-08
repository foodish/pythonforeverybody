#!/usr/bin/env python3
# -*- coding: utf-8 -*-
# @Date    : 2017/6/8
# @Author  : foodish
# @File    : test_append.py
import time


def app1(count):
    a=[]
    for i in range(count):
        for j in range(10000):
            a.append((i,j))
    return a

def app2(count):
    a=[]
    fun_app = a.append
    for i in range(count):
        for j in range(10000):
            fun_app((i,j))
    return a

def run(count):
    time1 = time.clock()
    app1(count)
    time2 = time.clock()
    print("time app1:",time2-time1)
    time3 = time.clock()
    app2(count)
    time4 = time.clock()
    print("time app2:",time4-time3)


if __name__ == '__main__':
    for i in [10,100, 1000, 10000]:
        print(i)
        run(i)

