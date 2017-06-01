#!/usr/bin/python
#-*-coding:utf-8-*-

import re
import math
import TwitterWithMysql as mydb
import TweetsWithMongo as mongo

def getUsersInfo(table):
    # db = Conn(hostname,username,password,databasename)
    # cursor = db.cursor()
    user = mydb.getUsersInfo(table)
    return user

def getUserInfo(id,table):
    twitter_user = mydb.getUserInfo(id,table)
    return twitter_user

def getUserTweets(userid,Search):
    tweets = []
    result = Search.find({"user_id":long(userid)})
    for res in result:
        tweets.append(res["text"])
    return tweets

# 获取某一类别的用户
def getUsersByCategory(table,category):
    users = mydb.getUsersByCategory(table,category)
    return users

# # 形成最后的标准人物样本库
# def GenerateStandardUsers(cursor,userid):
#     '''
#
#     :param cursor:
#     :param userid:存储娱乐领域的用户的id
#     :return:
#     '''
#     for id in userid:
#         cursor.execute("insert into StandardUsers(name,screen_name,category,userid,location,created_at,description,statuses_count,followers_count,friends_count,favourites_count,lang,protected,time_zone,verified,geo_enabled) select name,screen_name,category,userid,location,created_at,description,statuses_count,followers_count,friends_count,favourites_count,lang,protected,time_zone,verified,geo_enabled from PreStandardUsers where userid = %s" % id)
#     print "标准人物样本库生成完成!"

# split Origin and RT
def CalucateParameters(tweets):
    OTN = RTN = RTrtN = ORTN = OFavN = RTFavN = 0
    if tweets.count() == None:
        return OTN,RTN,ORTN,RTrtN,OFavN,RTFavN
    for tweet in tweets:
        # 转推
        if re.match(r"^RT @[\w|\d|_]+",tweet["text"]) != None:
            RTN += 1
            RTrtN += tweet["retweet_count"]
            RTFavN += tweet["favorite_count"]
        # 非转推
        else:
            OTN += 1
            ORTN += tweet["retweet_count"]
            OFavN += tweet["favorite_count"]
    # OriginNumber RTNumber
    return OTN,RTN,ORTN,RTrtN,OFavN,RTFavN

# active
def CalucateActive(user,OriginN,RTN):
    d_active = 0.5 * math.log(OriginN + 1,math.e) + 0.3 * math.log(RTN + 1,math.e) + 0.2 * math.log(user.followers_count + 1,math.e)
    return d_active

# Influence
def CalucateInfluence(ORTN,OFavN,RTN,RTFavN):
    return 0.4 * math.log(ORTN + 1,math.e) + 0.2 * math.log(OFavN + 1,math.e) + 0.2 * math.log(RTN + 1,math.e) + 0.2 * math.log(RTFavN + 1,math.e)

# twitter Influence
def CalucateTwitterInfluence(d_active,d_twitter):
    return 0.2 * d_active + 0.8 * d_twitter

# 对外接口计算用户影响力分数
def CalucateUserInfluence(userid):
    # connect to mongodb localhost
    result = mongo.getTweets(userid)
    user = getUserInfo(userid,table="StandardUsers")
    OTN,RTN,ORTN,RTrtN,OFavN,RTFavN = CalucateParameters(result)
    score = CalucateTwitterInfluence(CalucateActive(user,OTN,RTN),CalucateInfluence(ORTN,OFavN,RTrtN,RTFavN))

    # 返回用户影响力分数
    return score

def test():
    score = CalucateUserInfluence('29479000')
    print  score
# if __name__ == "__main__":
#     conn = MySQLdb.connect(
#         host='localhost',
#         port = 3306,
#         user='root',
#         passwd='123',
#         db ='TwitterUserInfo',
#     )
#     cursor = conn.cursor()
#
#     # connect to mongodb localhost
#     client = MongoClient('127.0.0.1',27017)
#     # 获取所有用户
#     # users = getUsersInfo(cursor)
#
#     # 获取娱乐领域的用户
#     users = getUsersByCategory("Entertainment",cursor)
#     userid = []
#     for user in users:
#         userid.append(user.id)
#     print "用户id获取完成"
#
#     # define the name of database
#     db = client.twitterForTestInflu
#     # tweets1 = db.tweets_10
#     # tweets2 = db.tweets_11
#     # tweets3 = db.tweets_12
#     # tweets = [tweets1,tweets2,tweets3]
#     tweet = db.PreStandardUsers
#     user_influ = {}
#
#     # for user in users:
#     #     if user.id[:2] == "11":
#     #         tweet = tweets2
#     #     elif user.id[:2] == "12":
#     #         tweet = tweets3
#     #     else:
#     #         tweet = tweets1
#     #     if tweet.find({"user_id":long(user.id)}).count() > 0:
#     #         userid.append(user.id)
#     count = 0
#     print "开始计算用户影响力"
#     for id in userid:
#         # if id[:2] == "11":
#         #     result = tweets2.find({"user_id":long(id)})
#         # elif id[:2] == "12":
#         #     result = tweets3.find({"user_id":long(id)})
#         # else:
#         #     result = tweets1.find({"user_id":long(id)})
#         result = tweet.find({'user_id':long(id)})
#         user = getUserInfo(id,cursor)
#         OTN,RTN,ORTN,RTrtN,OFavN,RTFavN = CalucateParameters(result)
#         print OTN,RTN,ORTN,RTrtN,OFavN,RTFavN
#         user_influ[id] = CalucateTwitterInfluence(CalucateActive(user,OTN,RTN),CalucateInfluence(ORTN,OFavN,RTrtN,RTFavN))
#         count += 1
#         print "已计算%d个" % count
#     user_influ = sorted(user_influ.items(),key=lambda dic:dic[1],reverse=True)
#     # 针对某一类用户(针对娱乐界用户,选取前880个)
#     en_users = user_influ[:880]
#     en_users_id = []
#     for user in en_users:
#         en_users_id.append(user[0])
#     GenerateStandardUsers(cursor,en_users_id)
#
#     # 针对所有用户
#     # 将前三千人的name/userid以及screen_name写入文本文件中
#     # print "开始将3000人id写入文本文件"
#     # with open("/home/duncan/3000Famous","w") as f:
#     #     for dic in user_influ[:3000]:
#     #         f.write(dic[0])
#     #         f.write("\n")
#     cursor.close()
#     conn.commit()
#     conn.close()