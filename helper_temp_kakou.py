# -*- coding: utf-8 -*-
import json

import requests
from requests.auth import HTTPBasicAuth


class TempKakou(object):
    def __init__(self, **kwargs):
        self.host = kwargs['host']
        self.port = kwargs['port']
        self.city = kwargs['city']
        self.headers = {'content-type': 'application/json'}

        self.status = False

    def get_kakou_info(self, start_id, end_id):
        """根据id范围获取车辆信息"""
        url = 'http://%s:%s/final/%s?q={"startid":%s,"endid":%s}' % (
            self.host, self.port, self.city, start_id, end_id)
        try:
            r = requests.get(url, headers=self.headers)
            if r.status_code == 200:
                return json.loads(r.text)
            else:
                self.status = False
                raise Exception('url: {url}, status: {code}, {text}'.format(
                    url=url, code=r.status_code, text=r.text))
        except Exception as e:
            self.status = False
            raise

    def get_maxid(self):
        """根据id范围获取车辆信息"""
        url = 'http://{0}:{1}/maxid/{2}'.format(
            self.host, self.port, self.city)
        try:
            r = requests.get(url, headers=self.headers)
            if r.status_code == 200:
                return json.loads(r.text)
            else:
                self.status = False
                raise Exception('url: {url}, status: {code}, {text}'.format(
                    url=url, code=r.status_code, text=r.text))
        except Exception as e:
            self.status = False
            raise

    def post_final(self, data):
        url = 'http://{0}:{1}/final/{2}'.format(self.host, self.port, self.city)
        try:
            r = requests.post(url, headers=self.headers, data=json.dumps(data))
            if r.status_code == 201:
                return json.loads(r.text)
            else:
                self.status = False
                raise Exception('url: {url}, status: {code}, {text}'.format(
                    url=url, code=r.status_code, text=r.text))
        except Exception as e:
            self.status = False
            raise

    def post_temp(self, data):
        url = 'http://{0}:{1}/temp/{2}'.format(self.host, self.port, self.city)
        try:
            r = requests.post(url, headers=self.headers, data=json.dumps(data))
            if r.status_code == 201:
                return json.loads(r.text)
            else:
                self.status = False
                raise Exception('url: {url}, status: {code}, {text}'.format(
                    url=url, code=r.status_code, text=r.text))
        except Exception as e:
            self.status = False
            raise


