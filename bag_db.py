# -*- coding:utf-8 -*-

import MySQLdb
import MySQLdb.cursors

# connecting to MySQLdb
def get_baggage(host,port,user,password,db,sql):
    #连接主表
    '''
    :param host: 
    :param port: 
    :param user: 
    :param password: 
    :param db: 
    :param sql: 
    :return: 
    '''
    try:
        #建立数据库连接
        conn=MySQLdb.Connect(
            host = host,
            port = port,
            user = user,
            password = password,
            db = db,
            cursorclass = MySQLdb.cursors.Dictcursor #设置SQL语句的返回形式为字典

        )
        #获取cursor对象，用于SQL查询并返回结果
        cur = conn.cursor()
        #执行单条SQL语句，返回数据量
        datas = cur.execute(sql)
        #print(datas)
        #抓取数据
        info = cur.fetchmany(datas)
        #print(info)
        #关闭资源
        cur.close()
        conn.commit()
        conn.close()
        return info

    except MySQLdb.Error,e:
        print "Mysqldb error %d,%s" % ( e.args[0],e.args[1])


def get_subbag(host,port,user,password,db,sql,relation_id,condition):
    #连接附表，通过ID获取相关数据
    try:
        #建立数据库连接
        conn=MySQLdb.Connect(
            host = host,
            port = port,
            user = user,
            password = password,
            db = db,
            cursorclass = MySQLdb.cursors.Dictcursor #设置SQL语句的返回形式为字典

        )
        #获取cursor对象，用于SQL查询并返回结果
        cur = conn.cursor()
        #执行单条SQL语句，返回数据量
        datas = cur.execute( 'SELECT * FROM TCFlyIntFare.fifc_fsd_subbag where /"relation_id /"= relation_id and condition = condition')
        #print(datas)
        #抓取数据
        info = cur.fetchmany(datas)
        #print(info)
        #关闭资源
        cur.close()
        conn.commit()
        conn.close()
        return info

    except MySQLdb.Error,e:
        print "Mysqldb error %d,%s" % ( e.args[0],e.args[1])


def db2dict(info):
    # 将数据库中数据写入字典
    try:
        dict = {}
        for data in info:
            dict.setdefault(data['id'], data)
            return dict
    except Exception,E:
        print Exception,":",E

