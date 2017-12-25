# -*- coding:utf-8 -*-

import MySQLdb
import MySQLdb.cursors


# connecting to MySQLdb
def get_baggage(host,port,user,passwd,db,sql):
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
            passwd = passwd,
            db = db,
            cursorclass = MySQLdb.cursors.DictCursor
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


def get_subbag(host,port,user,passwd,db,sql,relation_id): #,conditon
    #连接附表，通过ID获取相关数据
    try:
        #建立数据库连接
        conn=MySQLdb.Connect(
            host = host,
            port = port,
            user = user,
            passwd = passwd,
            db = db,
            cursorclass = MySQLdb.cursors.DictCursor #设置SQL语句的返回形式为字典

        )
        #获取cursor对象，用于SQL查询并返回结果
        cur = conn.cursor()
        #执行单条SQL语句，返回数据量
        datas = cur.execute( sql, [relation_id])
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
        l = len(info)
        for i in range(0, l):
            k=info[i]['master_routing']+"-"+info[i]['cabinclass'] #唯一索引
            v=info[i]
            dict.setdefault(k, v)
        return dict
    except Exception,E:
        print Exception,":",E




if __name__ == '__main__':
    #  fsd_bag_data = get_baggage('10.100.157.78', 3500, 'TCFlyIntFare', 'MDiNkMR85fKgyRXI3iR', 'TCFlyIntFare',
    #                                   'SELECT * FROM TCFlyIntFare.fifc_fsd_baggage')
    #  print(fsd_bag_data[0])
    # # a=fsd_bag_data[0]
    # # fsd_bag_dic=db2dict(fsd_bag_data)
    # # print(fsd_bag_dic)


    fsd_subbag_data = get_subbag('10.100.157.78', 3500, 'TCFlyIntFare', 'MDiNkMR85fKgyRXI3iR', 'TCFlyIntFare',
                               'SELECT * FROM TCFlyIntFare.fifc_fsd_baggage where id =%s ', 463)

    print(fsd_subbag_data[0])
