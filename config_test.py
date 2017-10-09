#-*- encoding: utf-8 -*-
from my_yaml import MyYAML


class TestYAML(object):
    def __init__(self):
        self.my_ini = MyYAML('my.yaml')
        self.flag_ini = MyYAML('flag.yaml')
        
    def get_ini(self):
        #print(self.my_ini.get_ini())
        #print(dict(self.my_ini.get_ini()['kakou']))
        print(self.my_ini.get_ini()['kkdd'])

    def get_ini2(self):
        print(self.flag_ini.get_ini())

    def set_ini(self):
        data = self.flag_ini.get_ini()
        data['id'] = 123
        print(self.flag_ini.set_ini(data))

if __name__ == "__main__":
    ty = TestYAML()
    ty.get_ini()
    #ty.get_ini2()
    #ty.set_ini()
    #ty.set_ini()
