#!/usr/bin/python
#-*-coding:utf-8-*-
'''@author:duncan'''
# 配置文件
# 目录配置
import os
project_path = os.path.abspath("..") + "/flask-twitter"
static_path = project_path + "/app/static/"
classify_pickles_path = static_path + "classify_pickles/"
senti_pickles_path = static_path + "senti_pickle_algos/"
resource_path = static_path + "resource/"
stop_words_path = resource_path + "/stopwords.txt"
xml_path = static_path + "xml/"

# mysql配置
host = "localhost"
port = 3306
user = "root"
passwd = "123"
db = "Web"

# mongodb配置
mongo_host = "127.0.0.1"
mongo_port = 27017

# neo4j配置
neo_host = "bolt://localhost:7687"
neo_user = "neo4j"
neo_passwd = "123"

# 参数配置
months = {'Jan':'1','Feb':'2','Mar':'3','Apr':'4','May':'5','Jun':'6','Jul':'7','Aug':'8','Sep':'9','Oct':'10','Nov':'11','Dec':'12'}

#多项式贝叶斯分类器
mnb = "MultinomialNB"

# 资源配置
# 读取停用词
def getStopWords(path):
    stopwords = set()
    with open(path,"r") as f:
        lines = f.readlines()
    for line in lines:
        stopwords.add(line.replace("\r\n","").rstrip())
    return stopwords

stopwords = getStopWords(stop_words_path)
