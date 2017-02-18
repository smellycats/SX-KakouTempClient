# -*- coding: utf-8 -*-
import time
import datetime
import json

import arrow
import requests
from requests.auth import HTTPBasicAuth, HTTPDigestAuth

from kakou import Kakou
from temp_kakou import TempKakou

class TempKakouTest(object):
    def __init__(self):
        self.ini = {
            'host': '10.47.223.151',
            'port': 5000,
	    'city': 'lm'
        }
        self.uk = TempKakou(**self.ini)
    
    def test_kakou_post(self):
        """上传卡口数据"""
        data = [
            {
		'id': 123,
		'cltx_id': 3,
                'jgsj': arrow.now().format('YYYY-MM-DD HH:mm:ss'),
                'hphm': u'粤L70939',
		'hpys': u'蓝牌',
		'hpys_id': 1,
		'hpys_code': 'BU',
		'kkdd': u'交警支队卡口',
                'kkdd_id': '441302004',
                'fxbh': u'进城',
                'fxbh_code': 'IN',
                'cdbh':4,
		'clsd': 45,
		'hpzl': '7',
		'kkbh': '1234',
		'clbj': 'F',
                'imgurl': u'http:///img/123.jpg'
            },
            {
		'id': 124,
		'cltx_id': 4,
                'jgsj': arrow.now().format('YYYY-MM-DD HH:mm:ss'),
                'hphm': u'粤L12345',
		'hpys': u'蓝牌',
		'hpys_id': 1,
		'hpys_code': 'BU',
		'kkdd': u'交警支队卡口',
                'kkdd_id': '441302004',
                'fxbh': u'进城',
                'fxbh_code': 'IN',
                'cdbh':4,
		'clsd': 45,
		'hpzl': '7',
		'kkbh': '1234',
		'clbj': 'F',
                'imgurl': u'http:///img/124.jpg'
            }
        ]

        r = self.uk.post_kakou(data)
        print r
        #assert isinstance(r, dict) == True
        #assert r['headers'] == 201


class KakouTest(object):
    def __init__(self):
        self.ini = {
            'host': '10.47.223.147',
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
        print r
        #assert 'total_count' in r
        
    def test_get_maxid(self):
        """获取最大ID"""
        r = self.kk.get_maxid()
        print r
        #assert 'maxid' in r

if __name__ == '__main__':  # pragma nocover
    #ut = TempKakouTest()
    #ut.test_kakou_post()
    kt = KakouTest()
    kt.test_get_maxid()
    kt.test_get_kakou()

