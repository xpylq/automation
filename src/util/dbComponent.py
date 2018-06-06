#!/usr/bin/python3
import configparser
import json
import time
import pymysql
import src.bean as bean

global db


def init():
    # 初始化db
    conf = configparser.ConfigParser()
    conf.read("properties.ini")
    host = conf.get("db", "host")
    username = conf.get("db", "username")
    password = conf.get("db", "password")
    database = conf.get("db", "database")
    global db
    db = pymysql.connect(host, username, password, database)


def add_user(name, password, user_type):
    """
    创建账号
    user_type 1:豆瓣,2:知乎
    """
    cursor = db.cursor()
    sql = "INSERT INTO automation_user(name,password,type) VALUES ('%s', '%s', '%d')" % \
          (name, password, user_type)
    try:
        cursor.execute(sql)
        db.commit()
    except Exception as e:
        db.rollback()
        print(e)


def add_user_and_cookies(name, password, user_type, cookies):
    """
    创建账号
    user_type 1:豆瓣,2:知乎
    """
    for cookie in cookies:
        cookie['expiry'] = time.time() + 60 * 60 * 24 * 365 * 10
    cookies = json.dumps(cookies)
    cookies = cookies.replace("\\", "\\\\\\")
    cursor = db.cursor()
    sql = "INSERT INTO automation_user(name,password,type,cookies) VALUES ('%s', '%s', '%d','%s')" % \
          (name, password, user_type, cookies)
    try:
        cursor.execute(sql)
        db.commit()
    except Exception as e:
        db.rollback()
        print(e)


def get_un_login_user(user_type):
    """
    获取所有没有登录的账号
    user_type 1:豆瓣,2:知乎
    """
    cursor = db.cursor()
    sql = "SELECT id,name,password,type,loginFlag,cookies from automation_user WHERE type = '%d' and loginFlag = 0" % \
          user_type
    try:
        cursor.execute(sql)
        results = cursor.fetchall()
        user_list = []
        for row in results:
            cookies = row[5]
            if cookies:
                cookies = json.loads(row[5])
            user = bean.user(row[0], row[1], row[2], row[3], row[4], cookies)
            user_list.append(user)
        return user_list
    except Exception as e:
        db.rollback()
        print(e)


def get_new_user(user_type):
    """
    获取所有没有登录的账号
    user_type 1:豆瓣,2:知乎
    """
    cursor = db.cursor()
    sql = "SELECT id,name,password,type,loginFlag,cookies from automation_user WHERE type = '%d' and isNew = 1" % \
          user_type
    try:
        cursor.execute(sql)
        results = cursor.fetchall()
        user_list = []
        for row in results:
            cookies = row[5]
            if cookies:
                cookies = json.loads(row[5])
            user = bean.user(row[0], row[1], row[2], row[3], row[4], cookies)
            user_list.append(user)
        return user_list
    except Exception as e:
        db.rollback()
        print(e)


def get_login_user(user_type, limit):
    """
    获取所有没有登录的账号
    user_type 1:豆瓣,2:知乎
    """
    cursor = db.cursor()
    sql = "SELECT id,name,password,type,loginFlag,cookies from automation_user WHERE type = '%d' and loginFlag = 1 order by id limit %d" % \
          (user_type, limit)
    try:
        cursor.execute(sql)
        results = cursor.fetchall()
        user_list = []
        for row in results:
            cookies = row[5]
            if cookies:
                cookies = json.loads(row[5])
            user = bean.user(row[0], row[1], row[2], row[3], row[4], cookies)
            user_list.append(user)
        return user_list
    except Exception as e:
        db.rollback()
        print(e)


def get_login_user_by_id(user_id):
    """
    获取所有没有登录的账号
    user_type 1:豆瓣,2:知乎
    """
    cursor = db.cursor()
    sql = "SELECT id,name,password,type,loginFlag,cookies from automation_user WHERE id = '%d' " % user_id
    try:
        cursor.execute(sql)
        results = cursor.fetchall()
        row = results[0]
        cookies = row[5]
        if cookies:
            cookies = json.loads(row[5])
        user = bean.user(row[0], row[1], row[2], row[3], row[4], cookies)
        return user
    except Exception as e:
        print(e)


def save_cookies(user_id, cookies):
    """
    保存cookie
    """
    for cookie in cookies:
        cookie['expiry'] = time.time() + 60 * 60 * 24 * 365 * 10
    cookies = json.dumps(cookies)
    cookies = cookies.replace("\\", "\\\\\\")
    cursor = db.cursor()
    sql = "UPDATE automation_user set cookies ='%s',loginFlag=1 where id ='%d' " % \
          (cookies, user_id)
    try:
        cursor.execute(sql)
        db.commit()
    except Exception as e:
        db.rollback()
        print(e)


def update_isNew(user_id):
    """
    保存cookie
    """
    cursor = db.cursor()
    sql = "UPDATE automation_user set isNew=0 where id ='%d' " % user_id
    try:
        cursor.execute(sql)
        db.commit()
    except Exception as e:
        db.rollback()
        print(e)


def delete_cookies(user_id):
    """
    保存cookie
    """
    cursor = db.cursor()
    sql = "UPDATE automation_user set cookies =null,loginFlag=0 where id ='%d' " % user_id
    try:
        cursor.execute(sql)
        db.commit()
    except Exception as e:
        db.rollback()
        print(e)


# 初始化db
init()
