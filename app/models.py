# -*- coding:utf-8 -*-
from sqlalchemy import Column, Integer, String, DateTime
from app.database import db

class Admin(db.Model):
    __tablename__ = 'admin'
    userid = Column(String(20), primary_key = True)
    username = Column(String(20))
    password = Column(String(40))

    def __init__(self, userid = None, username = None, password = None):
        self.userid = userid
        self.username = username
        self.password = password


class Task(db.Model):
    __tablename__ = 'task'
    id = Column(Integer, primary_key = True)
    task_name = Column(String(100))
    userid = Column(String(30))
    created_at = Column(DateTime)
    finished_at = Column(DateTime)
    search_name = Column(String(30))
    search_type = Column(Integer)
    remark = Column(String(300))

    thread_num = Column(Integer)
    deepth = Column(Integer)
    style = Column(Integer)
    extension = Column(Integer)
    tweet_num = Column(Integer)
    friends_num = Column(Integer)
    followers_num = Column(Integer)
    basicinfo_num = Column(Integer)

    # def __init__(self, task_name = None, userid = None, search_name = None,  remark = None, created_at = None, finished_at = None, search_type = '1'):
    #     self.task_name = task_name
    #     self.userid = userid
    #     self.created_at = created_at
    #     self.finished_at = finished_at
    #     self.search_type = search_type
    #     self.search_name = search_name
    #     self.remark = remark

class StandardUsers(db.Model):
    """docstring for StandardUsers"""
    __tablename__ = "StandardUsers"
    name = Column(String(50))
    screen_name = Column(String(50),primary_key=True)
    category = Column(String(255))
    userid = Column(String(30))
    location = Column(String(100))
    created_at = Column(String(50))
    description = Column(String(255))
    statuses_count = Column(Integer)
    followers_count = Column(Integer)
    friends_count = Column(Integer)
    favourites_count = Column(Integer)
    lang = Column(String(20))
    protected = Column(Integer)
    time_zone = Column(String(50))
    verified = Column(Integer)
    geo_enabled = Column(Integer)
        