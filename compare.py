# coding=utf-8

import bag_db
import bag_json
import os

def  compare(data1,data2,errInfo):
            '''
            校验函数
            data1为数据库对应字典
            data2为json文件对应字典
            info为比较字段注释信息
            '''
            try:
                if str(data1) != str(data2):
                    error_list.append(errInfo)
                    error_list.append('{} != {}'.format(data1, data2))
                    error_list.append('\n')
                    return errInfo
                else:
                    return 1111
            except Exception, e:
                return e
               # print Exception, ":", "grtytryhyghghgf"+errInfo


# a = json_read(r'D:\MyConfiguration\hd48552\Desktop\S1-searchdetail (2).txt')
#     print(a['engineType'])
#     r=proProcess(a)
#     print(r)
def checking(dict1,dict2):  ###dict1为数据库，dict2为文件
        #校验函数
        for key in dict2:
            # error_list.append(str(id))
            # error_list.append('\n')
            #对比sub_tag和bags
            if dict2["sub_tag"]==1 and dict1["sub_tag"]==1:
                a=0
                b=dict1["id"]
                subbaggae = bag_db.get_subbag('10.100.157.78', 3500, 'TCFlyIntFare', 'MDiNkMR85fKgyRXI3iR', 'TCFlyIntFare',
                               'SELECT * FROM TCFlyIntFare.fifc_fsd_sub_baggage where relation_id=%s', dict1["id"])
                #c=1111
                # dd=subbaggae[0]
                subbaggae=dict1.setdefault("subbaggae",subbaggae[0])
                # ff=subbaggae["bags"]
                # gg=dict2["bags"]
                compare(subbaggae["bags"], dict2["bags"], "8:bags错误")
            else:
                if dict2[id]["sub_tag"]==0 and dict1[id]["sub_tag"]==0:
                    compare(dict1["bags"], dict2["bags"], "8:bags错误")
                else:
                    compare(dict1["sub_tag"], dict2["sub_tag"], "9:sub_tag错误")
            #对比其他字段
            # d=dict1["routing"]
            # e=dict2["routing"]
            F=compare(dict1["routing"],dict2["routing"],"2:routing错误")
            compare(dict1["connections"],dict2["connections"],"3:connections错误")
            compare(dict1["fillingairline"], dict2["fillingairline"], "4:fillingairline错误")
            compare(dict1["aircodes"], dict2["aircodes"], "5:aircodes错误")
            compare(dict1["cabinclass"],dict2["cabinclass"],"6:cabinclass错误")
            compare(dict1["pax_type"], dict2["pax_type"],"7:pax_Type错误")
            compare(dict1["create_time"], dict2["create_time"],"10:createTime错误")
            compare(dict1["source"],dict2["source"],"11:source错误")
            rr=compare(dict1["tracerid"], dict2["tracerid"],"12:tracerId错误")
            G=compare(dict1["dep_city"], dict2["dep_city"], "13:dep_city错误")
            h=compare(dict1["arr_city"], dict2["arr_city"], "14:arr_city错误")
            compare(dict1["detail_link"], dict2["detail_link"],"detail_link错误")

            # self.cmp(dict1[id]["bags"], dict2[id]["bags"], "bags错误")
            # self.cmp(dict1[id]["sub_tag"],dict2[id]["sub_tag"], "sub_tag错误")


if __name__ == '__main__':
    error_list = []
    # connect to db
    db = bag_db.get_baggage('10.100.157.78', 3500, 'TCFlyIntFare', 'MDiNkMR85fKgyRXI3iR', 'TCFlyIntFare','SELECT * FROM TCFlyIntFare.fifc_fsd_baggage')
    db_dict = bag_db.db2dict(db)

    # 读入文件
    json = bag_json.json_read(r'D:\MyConfiguration\hd48552\Desktop\sss1.txt')
    json_dict = bag_json.proProcess(json)

    dict2 = json_dict #文件
    # a=json_dict["routing"] + "|" + json_dict["connections"] + "|" + json_dict["fillingairline"] + "|" + json_dict["cabinclass"]
    try:
     a=json_dict["routing"] + "|" + json_dict["connections"] + "|" + json_dict["fillingairline"] + "|" + json_dict[
            "cabinclass"]
     dict1 = db_dict[json_dict["routing"] +"|"+ json_dict["connections"] + "|"+json_dict["fillingairline"] + "|"+json_dict["cabinclass"]] #数据库
     result=checking(dict1, dict2)
     print ("ERROR LIST :---------------------")
     # for iin range(0,len(error_list)):
     print (error_list) ####？？？？？？？？？？？为什么一条错误信息存入多次？？？？？？？？？？？？？？？？
    except Exception,E:  #异常信息有时是因为key与数据库中的字段值不匹配
         print Exception, ":", E#"111111111116666666666666666"













