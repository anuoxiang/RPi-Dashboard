# -*- coding: utf-8 -*-
import requests
import re
import json
import time
import getpass

class Bar(object):
    def __init__(self, d = None):
        if d != None:
            self.__dict__ = d


class Item(object):
    name = ''
    file = ''
    regexp = ''
    def __init__(self):
        pass

# data = json.loads(s, object_hook=Bar)
conf = Bar()

# 载入配置文件
# 服务器地址
conf.server_url = 'http://localhost:5000/foo'
# 刷新提交时间（毫秒）
conf.interval = 2000

# 硬件信息文件名，[{硬件信息对象名，硬件信息读取规则}...]
a1 = Item()
a1.name = "cpuinfo"
a1.file = "/proc/cpuinfo"
a1.regexp = "model\s+name\s{0,}\:+\s{0,}(.+)[\r\n]+"

conf.items = []
conf.items.append(a1)

def readinfo(filename):
    file_obj = open(filename)
    try:
        file_context = file_obj.read()
    finally:
        file_obj.close()
    return file_context

def getvalue(reg, con):
    value = re.findall(reg, con)
    return value

def makeobj(kn, vl):
    node = Bar()
    node.name = kn
    node.value = vl
    return node

def post(url,jsondata):
    r = requests.post(url, json=jsondata)
    print (r.text)

'''
主对象结构
{   Hostname: Rpi1,
    User:
    Data:[{}...]}
'''
root = Bar()
root.Hostname = readinfo("/etc/hostname")
root.User = getpass.getuser()

while True:
    root.Nodes = []
    print json.dumps(root.__dict__)
    for i in conf.items:
        node = makeobj(i.name, getvalue(i.regexp, readinfo(i.file)))
        root.Nodes.append(node.__dict__)

    # print json.dumps(root.__dict__)
    res = post(conf.server_url, json.dumps(root.__dict__))
    print res
    time.sleep(conf.interval / 1000)
