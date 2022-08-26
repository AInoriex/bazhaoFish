from operator import mod
import string
import pymysql
import os
# @Function     Bazhao Fish DataBase picInfo Operations
# @Author       AInoriex
# @Date         22.08.18

# 初始化数据库和表
def initDB():
    try:
        db = pymysql.connect(host="localhost",user="root",password="1234qwer",database="test")
    except Exception as e:
        print("[Warn] Failed to connect to the Database. Error:%s"%e)
        os.system("exit")

    cursor = db.cursor()
    sql_createDB = """
        CREATE DATABASE IF NOT EXISTS bazhaoyu
        DEFAULT CHARACTER SET utf8
        DEFAULT COLLATE utf8_general_ci;
    """
    sql_useDB = "USE bazhaoyu"
    sql_createTable = """
        create table PicInfo(
            fatherUrl   char(100),
            childLink1  char(100),
            childDown1  char(100),
            childLink2  char(100),
            childDown2  char(100),
            childLink3  char(100),
            childDown3  char(100),
            childLink4  char(100),
            childDown4  char(100),
            childLink5  char(100),
            childDown5  char(100),
            childLink6  char(100),
            childDown6  char(100),
            childLink7  char(100),
            childDown7  char(100),
            childLink8  char(100),
            childDown8  char(100),
            childLink9  char(100),
            childDown9  char(100),
            childLink10 char(100),
            childDown10 char(100),
            childLink11 char(100),
            childDown11 char(100),
            childLink12 char(100),
            childDown12 char(100),
            childLink13 char(100),
            childDown13 char(100),
            childLink14 char(100),
            childDown14 char(100),
            childLink15 char(100),
            childDown15 char(100),
            childLink16 char(100),
            childDown16 char(100),
            childLink17 char(100),
            childDown17 char(100),
            childLink18 char(100),
            childDown18 char(100),
            childLink19 char(100),
            childDown19 char(100),
            childLink20 char(100),
            childDown20 char(100),
            createdTime TIMESTAMP(6) not NULL DEFAULT CURRENT_TIMESTAMP(6),
            updatedTime TIMESTAMP(6) not NULL DEFAULT CURRENT_TIMESTAMP(6) ON UPDATE CURRENT_TIMESTAMP(6)
        ) ENGINE=MyISAM DEFAULT CHARSET=utf8;
    """
    try:
        cursor.execute(sql_createDB)
        cursor.execute(sql_useDB)

        cursor.execute(sql_createTable)
        print("[Info] Initialize succeed.")
        # print("[Info]Create the table 'DOUBANTOPMOVIE' succeed.")
    except Exception as e:
        print("[Warn] Something Failed. Error:%s"%e)
    finally:
        cursor.close()
        db.close()

# v0.1 根据输入父亲url筛选子url_4个
# v0.2 以上+自选n个数select出来(1<n<=20)
def mySelect(searchUrl:string,select_num:int,mode=0):
    res_list = []
    if mode == 0:
        keyword = "childLink"
    elif mode == 1:
        keyword = "childDown"
    else:
        return
    try:
        db = pymysql.connect(host="localhost",user="root",password="1234qwer",database="test")
    except Exception as e:
        print("[Warn] Failed to connect to the Database. Error:%s"%e)
        os.system("exit")
    cursor = db.cursor()
    sql_useDB = "USE bazhaoyu"
    # 根据select_num参数生成select字段
    str_select = ""
    for i in range(select_num):
        if i > 0:
            str_select += ","
        each_str = keyword+str(i+1)
        str_select += each_str

    sql_createDB = """
        SELECT  %s
        FROM    picInfo
        WHERE   fatherUrl = "%s"
    """%(str_select,searchUrl)
    print(sql_createDB)
    try:
        cursor.execute(sql_useDB)
        cursor.execute(sql_createDB)
        res_list = cursor.fetchone()
        print("[Info] Get the child urls succeed.")
        print("[Info] 查询结果如下")
        print(list(res_list))
        res_list = list(res_list)
    except Exception as e:
        print("[ERR]",e)
    finally:
        cursor.close()
        db.close()
        return res_list


# 重建数据表
def rebuildTable():
    ans = input("[Warn] 即将重置数据库，是否继续(yes/no)")
    if ans in ["no","No","n","No"]:
        print("[Info] 已取消操作")
        return
    try:
        db = pymysql.connect(host="localhost",user="root",password="1234qwer",database="test")
    except Exception as e:
        print("[Warn] Failed to connect to the Database. Error:%s"%e)
        os.system("exit")
    cursor = db.cursor()
    sql_useDB = "USE bazhaoyu"
    sql_dropTable = """
        DROP table picInfo;
    """
    try:
        cursor.execute(sql_useDB)
        cursor.execute(sql_dropTable)
        print("[Info] Succeed to drop the picInfo")
    except Exception as e:
        print("[ERR]%s"%e)
        cursor.close()
        db.close()
        return
    print("[Info] Start to rebuild table picInfo")
    initDB()
    print("[Info] Rebuild DONE")