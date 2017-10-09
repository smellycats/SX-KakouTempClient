# -*- coding: utf-8 -*-
import time
import datetime
import json

import arrow
import requests
from requests.auth import HTTPBasicAuth, HTTPDigestAuth

from helper_consul import ConsulAPI


class KakouTest(object):
    def __init__(self):
        self.ini = {
            'host': '127.0.0.1',
            'port': 8081,
	    'username': 'zkkakou',
	    'password': 'kakoutest'
        }
        self.kk = Kakou(**self.ini)

    def __del__(self):
        pass

    def test_get_kakou(self):
        """根据ID范围获取卡口信息"""
        r = self.kk.get_kakou(54059471, 54059473)
        print(r)
        #assert 'total_count' in r
        
    def test_get_maxid(self):
        """获取最大ID"""
        r = self.kk.get_maxid()
        print(r)
        #assert 'maxid' in r


class ConsulTest(object):
    def __init__(self):
        self.ini = {
            'host': '127.0.0.1',
            'port': 8500
        }
        self.con = ConsulAPI(**self.ini)

    def __del__(self):
        pass

    def test_get_id(self):
        print(self.con.get_id())

    def test_get_service(self):
        print(self.con.get_service('kakouHcq'))
        print(self.con.get_service('proxy'))

    def test_get_health(self):
        print(self.con.get_health('kakouHcq'))
        
#    def test_set_id(self):
#        r = self.con.get_id()
#        cas = r[0]['ModifyIndex']
#        print(self.con.put_id(23, cas))


if __name__ == '__main__':  # pragma nocover
    ct = ConsulTest()
    ct.test_get_id()
    #ct.test_set_id()
    #ct.test_get_service()
    ct.test_get_health()
