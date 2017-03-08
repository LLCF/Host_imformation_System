#!/usr/bin/env python

import re
import os
import socket
import requests
import pickle
import uuid
from time import sleep, ctime
class host():
    def __init__(self,num_cards=None,name_cards=None,driver=None,osenv=None,alive="False",host_name=None,ip=None,mac=None ):
        self.num_cards=num_cards
        self.cards_name=name_cards
        self.driver=driver
        self.osenv=osenv
        self.alive=alive
        self.host_name=host_name
        self.ip=ip
        self.mac=mac
        self.ipmi=""
    def __get_os(self):
        res = os.popen("lsb_release -a | grep -E ' ([0-9.]+) '").read()
        self.osenv = re.search(".*?(\d{2})(\.\d{2}.\d)",res).group(1)
        self.host_name=socket.gethostname()

    def __get_ip(self):
        ips = os.popen("ifconfig | grep -E '10.19\.[0-9]{0,3}\.[0-9]{0,3}'").read()
        self.ip = re.search("10.19.[\d]{1,3}.[\d]{1,3}",ips).group()
        ipmi = os.popen("sudo ipmitool lan print 1 | grep 'IP Address  '")
        self.ipmi=re.search("10.19.[\d]{1,3}.[\d]{1,3}",ipmi).group()
    
    def __get_cardsinfo(self):
        info_card = os.popen(" nvidia-smi -q ").read().strip()
        self.driver = re.search("Driver Version[ :]*([\d]{3}\.[\d]{2})", info_card).group(1)
        self.num_cards = re.search("Attached GPUs[ :]*([\d])",info_card).group(1)
        self.cards_name = list(set(re.findall("Product Name[ :]*([\d\w\. ]*)",info_card)))
        if len(self.cards_name)>1:
            name=''
            for cname in self.cards_name[:-1]:
                name += cname+','
            self.cards_name=name + self.cards_name[-1]
    def __get_mac(self):  
        mac=uuid.UUID(int = uuid.getnode()).hex[-12:].upper()  
        self.mac = '%s:%s:%s:%s:%s:%s' % (mac[0:2],mac[2:4],mac[4:6],mac[6:8],mac[8:10],mac[10:]) 
    def __is_alive(self):
        n = len(os.popen('w').read().strip().split('\n')[2:])
        for i in os.popen('w').read().strip().split('\n')[2:]:
            if "tty" in i:
                n -= 1
        if n >= 1:
            self.alive = "True"
        else:
            self.alive = "False"
    def __call__(self):
        self.__get_os()
        self.__get_ip()
        try:
            self.__get_cardsinfo()
        except:
            self.driver="No driver"
        self.__is_alive()
        self.__get_mac()
    def convert_to_dict(self):
        dict = {}
        dict.update(self.__dict__)
        return dict
    def __str__(self):
        return "host: %s\nip: %s \nGPU: %s\nGPU nums: %s\nUsed : %s\nTime: %s"\
                %(self.host_name, self.ip, self.cards_name[0:], self.num_cards, self.alive, ctime())
        
if __name__ == '__main__':
    h = host()
    server = 'http://127.0.0.1:5000/request'
    while True:
        h()
        try:
            pinfo = pickle.dumps(h)
            requests.post("http://10.19.224.185:8000/requests", data={'info':pinfo})
        except:
            info = h.convert_to_dict()
            print info
            pass
        break

