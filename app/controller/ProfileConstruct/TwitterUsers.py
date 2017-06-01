#!/usr/bin/python
#-*-coding:utf-8-*-
'''@author:duncan'''

class User:
    def __init__(self,id,screen_name,name,location,statuses_count,friends_count,followers_count,favourites_count,verified,category):
        self.id = id
        self.screen_name = screen_name
        self.name = name
        self.followers_count = followers_count
        self.friends_count = friends_count
        self.statuses_count = statuses_count
        self.favourites_count = favourites_count
        self.location = location
        self.verified = verified
        self.category = category

    def getProportion(self):
        if self.friends_count != 0:
            return (self.followers_count) * 1.0 / self.friends_count
        else:
            return (self.followers_count) * 1.0 / 0.1

    # 获取该类所有属性
    def list_all_members(self):
        attributes = []
        for name,value in vars(self).items():
            attributes.append(name)
        return attributes

    def __str__(self):
        if self.verified == 1:
            verify = "yes"
        else:
            verify = "no"
        if self.location == "":
            location = "no file"
        else:
            location = self.location

        return "user id:%s  screen_name:%s  name:%s  verified:%s  location:%s  followers:%d  followings:%d  tweets:%d  favourites:%d" % (self.id,self.screen_name,self.name,verify,location,self.followers_count,self.friends_count,self.statuses_count,self.favourites_count)