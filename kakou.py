# -*- coding: utf-8 -*-
import json

import requests
from requests.auth import HTTPBasicAuth, HTTPDigestAuth


class Kakou(object):

    def __init__(self, **kwargs):
        self.host = kwargs['host']
        self.port = kwargs['port']
	self.username = kwargs['username']
	self.password = kwargs['password']
	self.headers = {'content-type': 'application/json'}
        self.status = False
        
    def get_kakou(self, first_id, last_id):
        url = 'http://{0}:{1}/kakou/{2}/{3}'.format(
            self.host, self.port, first_id, last_id)
        try:
            r = requests.get(url, headers=self.headers,
			     auth=HTTPBasicAuth(self.username, self.password))
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
        """获取cltx表最大id值"""
        url = 'http://{0}:{1}/maxid'.format(self.host, self.port)
        try:
            r = requests.get(url, headers=self.headers,
			     auth=HTTPBasicAuth(self.username, self.password))
            if r.status_code == 200:
                return json.loads(r.text)
            else:
                self.status = False
                raise Exception('url: {url}, status: {code}, {text}'.format(
                    url=url, code=r.status_code, text=r.text))
        except Exception as e:
            self.status = False
            raise

