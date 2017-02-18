# -*- coding: utf-8 -*-
import time
import json

import arrow

#from kakou import Kakou
from helper_kakou2 import Kakou
from temp_kakou import TempKakou

from ini_conf import MyIni


class UploadData(object):
    def __init__(self):
        # 配置文件
        self.my_ini = MyIni()
        self.kk_ini = self.my_ini.get_kakou()

        # request方法类
        self.kk = Kakou(**self.kk_ini)
	tk_ini1 = {
	    'host': '10.47.223.147',
	    'port': 8086,
	    'city': 'hcq1'
	}
	tk_ini2 = {
	    'host': '10.47.223.147',
	    'port': 8086,
	    'city': 'hcq2'
	}
	tk_ini3 = {
	    'host': '10.47.223.147',
	    'port': 8086,
	    'city': 'hcq3'
	}
        self.tk1 = TempKakou(**tk_ini1)
	self.tk2 = TempKakou(**tk_ini2)
	self.tk3 = TempKakou(**tk_ini3)
	
	self.kk.status = True
        self.tk1.status = True

        # ID上传标记
        self.id_flag = self.kk_ini['id_flag']
        self.step = 1000

        self.hpys_id = {
            'WT': 0,
            'YL': 1,
            'BU': 2,
            'BK': 3,
	    'GN': 4,
            'QT': 9
        }

    def set_id(self, _id):
        """设置ID"""
        self.id_flag = _id
        self.my_ini.set_id(_id)

    def post_info(self):
        """上传数据"""
	# 最大ID值
        maxid = self.kk.get_maxid()
        # 没有新数据则返回
        if maxid <= self.id_flag:
	    time.sleep(0.5)
            return

        if maxid > (self.id_flag + self.step):
            last_id = self.id_flag + self.step
        else:
            last_id = maxid
        car_info = self.kk.get_kakou(self.id_flag+1, last_id)
        # 如果查询数据为0
        if car_info['total_count'] == 0:
            # 设置最新ID
            self.set_id(last_id)
	    time.sleep(0.5)
            return

        data1 = []
	data2 = []
	data3 = []
        for i in car_info['items']:
            if i['kkdd_id'] is None or i['kkdd_id'] == '':
		i['kkdd_id'] = '441302000'
            if i['kkdd'] is None or i['kkdd'] == '':
		i['kkdd'] = ''
	    if i['hphm'] is None:
		i['hphm'] = '-'
	    if i['id']%3 == 1:
                data1.append({'id': i['id'],
			      'jgsj': i['jgsj'],           # 经过时间
                              'hphm': i['hphm'],           # 号牌号码
                              'hpys': i['hpys'],
                              'hpys_id': self.hpys_id.get(i['hpys_code'], 9),
			      'hpys_code': i['hpys_code'],
                              'kkdd': i['kkdd'],
                              'kkdd_id': i['kkdd_id'],
			      'fxbh': i['fxbh'],
                              'fxbh_code': i['fxbh_code'], # 方向编号
                              'cdbh': i['cdbh'],           # 车道
			      'clsd': i['clsd'],
			      'hpzl': i['hpzl'],
			      'kkbh': i['kkbh'],
			      'clbj': i['clbj'],
                              'imgurl': i['imgurl']})      # 图片url地址
	    elif i['id']%3 == 2:
                data2.append({'id': i['id'],
			      'jgsj': i['jgsj'],           # 经过时间
                              'hphm': i['hphm'],           # 号牌号码
                              'hpys': i['hpys'],
                              'hpys_id': self.hpys_id.get(i['hpys_code'], 9),
			      'hpys_code': i['hpys_code'],
                              'kkdd': i['kkdd'],
                              'kkdd_id': i['kkdd_id'],
			      'fxbh': i['fxbh'],
                              'fxbh_code': i['fxbh_code'], # 方向编号
                              'cdbh': i['cdbh'],           # 车道
			      'clsd': i['clsd'],
			      'hpzl': i['hpzl'],
			      'kkbh': i['kkbh'],
			      'clbj': i['clbj'],
                              'imgurl': i['imgurl']})      # 图片url地址
	    else:
                data3.append({'id': i['id'],
			      'jgsj': i['jgsj'],           # 经过时间
                              'hphm': i['hphm'],           # 号牌号码
                              'hpys': i['hpys'],
                              'hpys_id': self.hpys_id.get(i['hpys_code'], 9),
			      'hpys_code': i['hpys_code'],
                              'kkdd': i['kkdd'],
                              'kkdd_id': i['kkdd_id'],
			      'fxbh': i['fxbh'],
                              'fxbh_code': i['fxbh_code'], # 方向编号
                              'cdbh': i['cdbh'],           # 车道
			      'clsd': i['clsd'],
			      'hpzl': i['hpzl'],
			      'kkbh': i['kkbh'],
			      'clbj': i['clbj'],
                              'imgurl': i['imgurl']})      # 图片url地址
        r = self.tk1.post_kakou(data1)  #上传数据
	r = self.tk2.post_kakou(data2)  #上传数据
	r = self.tk3.post_kakou(data3)  #上传数据

        # 设置最新ID
        self.set_id(last_id)


    def main_loop(self):
        while 1:
            if self.kk.status and self.tk1.status:
		#print 'test'
                try:
                    self.post_info()
                    time.sleep(0.5)
                except Exception as e:
		    print e
                    time.sleep(1)
            else:
                try:
                    if not self.kk.status:
                        self.kk.get_maxid()
                        self.kk.status = True
                    if not self.tk1.status:
                        self.tk1.connect_test()
                        self.tk1.status = True
                except Exception as e:
                    time.sleep(1)
        
