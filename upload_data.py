# -*- coding: utf-8 -*-
import time
import json

import arrow

#from kakou import Kakou
from helper_kakou2 import Kakou
#from temp_kakou import TempKakou
from helper_temp_kakou2 import TempKakou

#from ini_conf import MyIni
from my_yaml import MyYAML


class UploadData(object):
    def __init__(self):
        # 配置文件
        self.my_ini = MyYAML('my.yaml').get_ini()
        self.flag_ini = MyYAML('flag.yaml')

        # request方法类
        self.kk = Kakou(**dict(self.my_ini['kakou']))
        self.tk = TempKakou(**dict(self.my_ini['temp']))
	
        self.kk.status = True
        self.tk.status = True

        # ID上传标记
        self.id_flag = self.flag_ini.get_ini()['id']
        self.step = self.my_ini['step']

    def set_id(self, _id):
        """设置ID"""
        self.id_flag = _id
        self.flag_ini.set_ini({"id": _id})
        print(_id)

    def post_info(self):
        """上传数据"""
        car_info = self.kk.get_kakou(self.id_flag+1, self.id_flag+self.step)
        # 如果查询数据为0
        if car_info['total_count'] == 0:
            time.sleep(1)
            return

        data = []
        for i in car_info['items']:
            if i['kkdd_id'] is None or i['kkdd_id'] == '':
                i['kkdd_id'] = '441322000'
            if i['hphm'] is None or i['hphm'] == '':
                i['hphm'] = '-'
            if i['id'] > 0:
                i['imgpath'] = ''
                data.append(i)
            i['imgurl'] = i['imgurl'].replace("10.44.245.247:8083", "10.47.223.151:8099/blkk")
        r = self.tk.post_final(data)  #上传数据
        # 设置最新ID
        self.set_id(car_info['items'][-1]['id'])


    def main_loop(self):
        while 1:
            if self.kk.status and self.tk.status:
                #print('test')
                try:
                    self.post_info()
                    time.sleep(0.5)
                except Exception as e:
                    print(e)
                    time.sleep(1)
            else:
                try:
                    if not self.kk.status:
                        self.kk.get_kakou(214542651, 214542653)
                        self.kk.status = True
                    if not self.tk.status:
                        self.tk.connect_test()
                        self.tk.status = True
                except Exception as e:
                    time.sleep(1)
        
