# coding=utf-8

import bag_db
import bag_json
import os

class BagDataOptimization:
    def reading(self):
         #connect to db
        db=bag_db.get_baggage('10.100.157.78', 3500, 'TCFlyIntFare', 'MDiNkMR85fKgyRXI3iR', 'TCFlyIntFare',
                                'SELECT * FROM TCFlyIntFare.fifc_fsd_bag')
        db_dict=bag_db.db2dict(db)
        json=bag_json.json_read(r'D:\MyConfiguration\hd48552\Desktop\S1-searchdetail (2).txt')
        json_dict=bag_json.proProcess(json)



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
                    return 0
                else:
                    return 1
            except Exception, e:
                print Exception, ":", e


# a = json_read(r'D:\MyConfiguration\hd48552\Desktop\S1-searchdetail (2).txt')
#     print(a['engineType'])
#     r=proProcess(a)
#     print(r)
    def check(dict1,dict2):
        #校验函数
        for id in cabin_bak_map:
            error_list.append(str(id))
            error_list.append('\n')
            if dict2[id]["sub_tag"]==1 and dict1[id]["sub_tag"]==1
                fsd_bag_data = bag_db.get_subbag('10.100.157.78', 3500, 'TCFlyIntFare', 'MDiNkMR85fKgyRXI3iR', 'TCFlyIntFare',
                                          'SELECT * FROM TCFlyIntFare.fifc_fsd_bag where "id"=%s ', 3619184, "")
                subbag=fsd_bag_data[bags]
                self.cmp(subbag, dict2[id]["bags"], "bags错误")
            else:
                if dict2[id]["sub_tag"]==0 and dict1[id]["sub_tag"]==0
                    self.cmp(dict1[id]["bags"], dict2[id]["bags"], "bags错误")
                else:
                    self.cmp(dict1[id]["sub_tag"], dict2[id]["sub_tag"], "sub_tag错误")
            self.cmp(dict1[id]["routing"],dict2[id]["routing"],"routing错误")
            self.cmp(dict1[id]["connections"],dict2[id]["connections"],"connections错误")
            self.cmp(dict1[id]["cabinclass"],dict2[id]["cabinclass"],"cabinclass错误")
            self.cmp(dict1[id]["fillingairline"],dict2[id]["fillingairline"],"fillingairline错误")
            self.cmp(dict1[id]["pax_Type"], dict2[id]["pax_Type"],"pax_Type错误")
            self.cmp(dict1[id]["createTime"], dict2[id]["createTime"],"createTime错误")
            self.cmp(dict1[id]["source"],dict2[id]["source"],"source错误")
            self.cmp(dict1[id]["tracerId"], dict2[id]["tracerId"],"tracerId错误")
            self.cmp(dict1[id]["aircodes"], dict2[id]["aircodes"],"aircodes错误")
            self.cmp(dict1[id]["detail_link"], dict2[id]["detail_link"],"detail_link错误")

            # self.cmp(dict1[id]["bags"], dict2[id]["bags"], "bags错误")
            # self.cmp(dict1[id]["sub_tag"],dict2[id]["sub_tag"], "sub_tag错误")













