# -*- coding: utf-8 -*-
import time
import json
import base64

import arrow

import helper
from helper_kakou_v2 import Kakou
from helper_temp_kakou import TempKakou
from helper_consul import ConsulAPI
from my_yaml import MyYAML
from my_logger import *


debug_logging(u'/home/logs/error.log')
logger = logging.getLogger('root')


class UploadData(object):
    def __init__(self):
        # 配置文件
        self.my_ini = MyYAML('/home/my.yaml').get_ini()
        self.kakou_ini = dict(self.my_ini['kakou'])
        # request方法类
        self.kk = None
        self.tk = None
        self.con = ConsulAPI(**dict(self.my_ini['consul']))
	
        #self.kk.status = False
        #self.tk.status = False
	
        # ID上传标记
        self.id_flag = 0
        self.step = self.my_ini['step']
        self.kkdd = self.my_ini['kkdd']

        self.uuid = None                    # session id
        self.session_time = time.time()     # session生成时间戳
        self.proxy_list = []                # 代理服务ip列表
        self.proxy_time = time.time() - 60  # 代理服务刷新

    def set_id(self, _id):
        """设置ID"""
        r = self.con.get_id()
        if self.con.put_id(_id, r[0]['ModifyIndex']):
            self.id_flag = _id

    def post_data(self, start_id, end_id):
        """上传卡口数据"""
        info = self.kk.get_kakou(start_id, end_id, 1, self.step+1)
        # 如果查询数据为0则退出
        if info['total_count'] == 0:
            return

        data = []
        for i in info['items']:
            if i['kkdd_id'] is None:
                i['kkdd_id'] = self.kkdd
            if i['hphm'] is None or i['hphm'] == '':
                i['hphm'] = '-'
            if i['id'] > 0:
                i['imgpath'] = ''
                data.append(i)
            i['imgurl'] = helper.created_url(i['imgurl'], self.proxy_list)
        if len(data) > 0:
            #print(len(data))
            #print(data[1]['imgurl'])
            self.tk.post_final(data)  #上传数据

    def post_info(self):
        print('id_flag: {0}'.format(self.id_flag))
        """上传实时数据"""
        maxid = self.kk.get_maxid()
        # id间隔
        interval = maxid - self.id_flag
        # 没有新数据则返回
        if interval <= 0:
            return 1
        # id间隔小于步长则使用maxid
        if interval < self.step:
            self.post_data(self.id_flag+1, maxid)
            self.set_id(maxid)   # 设置最新ID
            return 1
        
        self.post_data(self.id_flag+1, self.id_flag+self.step)
        self.set_id(self.id_flag+self.step)
        return 1

    def get_lock(self):
        """获取锁"""
        if self.uuid is None:
            self.uuid = self.con.put_session(30, 'hcq-temp-kakou-lock')['ID']
            self.session_time = time.time()
            # 获取上传id
            val = self.con.get_id()[0]['Value']
            self.id_flag = json.loads(base64.b64decode(val).decode())
        # 大于一定时间间隔则更新session
        t = time.time() - self.session_time
        if t > 20:
            self.con.renew_session(self.uuid)
            self.session_time = time.time()
        l = self.con.get_lock(self.uuid)
        #print(self.uuid, l)
        # session过期
        if l == None:
            self.uuid = None
            return False
        return l

    def get_proxy(self):
        """获取代理服务"""
        if time.time() - self.proxy_time < 60:
            return
        s = self.con.get_service('proxy')
        h = self.con.get_health('proxy')
        proxy_list = []
        service_status = {}
        for i in h:
            service_status[i['ServiceID']] = i['Status']
        for i in s:
            if service_status[i['ServiceID']] == 'passing':
                proxy_list.append('{0}:{1}'.format(i['ServiceAddress'], i['ServicePort']))
        self.proxy_list = proxy_list
        self.proxy_time = time.time()

    def get_service(self, service='kakouHcq'):
        s = self.con.get_service(service)
        if len(s) == 0:
            return None
        h = self.con.get_health(service)
        if len(h) == 0:
            return None
        service_status = {}
        for i in h:
            service_status[i['ServiceID']] = i['Status']
        for i in s:
            if service_status[i['ServiceID']] == 'passing':
                return {'host': i['ServiceAddress'], 'port': i['ServicePort']}
        return None

    def main_loop(self):
        while 1:
            self.get_proxy()
            if len(self.proxy_list) == 0:
                time.sleep(5)
                continue
            if not self.get_lock():
                time.sleep(2)
                continue
            if self.kk is not None and self.tk is not None and self.kk.status and self.tk.status:
                try:
                    self.post_info()
                    time.sleep(1)
                except Exception as e:
                    logger.error(e)
                    time.sleep(15)
            else:
                try:
                    if self.kk is None or not self.kk.status:
                        s = self.get_service('kakouHcq')
                        if s is None:
                            time.sleep(5)
                            continue
                        self.kk = Kakou(**{'host':s['host'], 'port':s['port'],
                                           'username':self.kakou_ini['username'],
                                           'password':self.kakou_ini['password']})
                        self.kk.status = True
                    if self.tk is None or not self.tk.status:
                        s = self.get_service('kakouTemp')
                        if s is None:
                            time.sleep(5)
                            continue
                        self.tk = TempKakou(**{'host':s['host'], 'port':s['port'],
                                               'city':self.kakou_ini['city']})
                        self.tk.status = True
                except Exception as e:
                    logger.error(e)
                    time.sleep(1)
        
