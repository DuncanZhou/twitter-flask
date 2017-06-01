#!/usr/bin/python
#-*-coding:utf-8-*-
'''@author:duncan'''

# 与Msql交互层
import MySQLdb
import config
import TwitterUsers

# 数据库连接
def Connection():
    conn = MySQLdb.connect(
        host=config.host,
        port = config.port,
        user=config.user,
        passwd=config.passwd,
        db =config.db,
    )
    # 全局变量cursor
    cursor = conn.cursor()
    return conn,cursor

# 数据库关闭
def Close(conn,cursor):
    cursor.close()
    conn.commit()
    conn.close()

# 根据用户id查询用户信息
def getUserInfo(id,table):
    '''
    :param id: 用户id
    :param table: 表名
    :param cursor: cursor
    :return:
    '''
    conn,cursor = Connection()
    cursor.execute("SELECT * FROM %s where userid = '%s'" % (table,id))
    d = cursor.fetchall()
    twitter_user = TwitterUsers.User(d[0][3],d[0][1],d[0][0],d[0][4],d[0][7],d[0][9],d[0][8],d[0][10],d[0][14],d[0][2])
    Close(conn,cursor)
    return twitter_user

# 获取表内所有用户的信息
def getUsersInfo(table):
    # db = Conn(hostname,username,password,databasename)
    # cursor = db.cursor()
    conn,cursor = Connection()
    cursor.execute("SELECT * FROM %s" % table)
    data = cursor.fetchall()
    user = []
    for d in data:
        twitter_user = TwitterUsers.User(d[3],d[1],d[0],d[4],d[7],d[9],d[8],d[10],d[14],d[2])
        user.append(twitter_user)
    Close(conn,cursor)
    return user

# 获取某一类别的用户
def getUsersByCategory(table,category):
    conn,cursor = Connection()
    users = []
    cursor.execute("select * from '%s' where category = '%s'" % (table,category))
    data = cursor.fetchall()
    for d in data:
        twitter_user = TwitterUsers.User(d[3],d[1],d[0],d[4],d[7],d[9],d[8],d[10],d[14],d[2])
        users.append(twitter_user)
    Close(conn,cursor)
    return users
