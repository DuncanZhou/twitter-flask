#!/usr/bin/python
#-*-coding:utf-8-*-
'''@author:duncan'''

from pymongo import MongoClient
import config

# 连接文档数据库
def Conn():
    # connect to mongodb localhost
    client = MongoClient(config.mongo_host,config.mongo_port)
    # define the name of database
    db = client.twitterForTestInflu
    return db

# 根据用户id查找推文,userid是字符串格式
def getTweets(userid):
    db = Conn()
    results = db.PreStandardUsers.find({'user_id':long(userid)})
    return results