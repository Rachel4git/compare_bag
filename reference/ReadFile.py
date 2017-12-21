# -*- coding:utf-8 -*-
import json
import chardet
import time
import os
import sys

reload(sys)
sys.setdefaultencoding('utf-8')
error_list = []

class Compare:
    #对比函数
    def cmp(self,old_data,new_data,info=None):
        '''
        校验函数
        old_data为旧表对应字段数据
        new_data为新表对应字段数据
        info为比较字段注释信息
        '''
        try:
            if str(old_data) != str(new_data):
                error_list.append(info)
                error_list.append('{} != {}'.format(old_data,new_data))
                error_list.append('\n')
        except Exception, e:
            print Exception, ":", e

    #解析文件编码格式
    def code(self,path):
        f = open(path, 'rb')
        f_read = f.read()
        f_charInfo = chardet.detect(f_read)
        return f_charInfo

    #读取文件转换为json
    def read(self,path):
        #读取txt文件
        try:
            file_object = open(path,'r')
            alljson = json.loads(file_object.read().decode("GB2312"))
            return alljson
        except Exception, e:
            print Exception, ":", e
        finally:
            file_object.close()

    #数据存为字典格式
    def setDict(self,alljson):
        flight_map = {}
        flight_list = []
        for eachflight in alljson['flights']:
            flight_map.setdefault(eachflight['flightNo'], eachflight)
            flight_list.append(flight_map)
        return flight_list

    def handleRoute(self,data):
        datalist = []
        for data_new in data["<add name>"]["flightCombinationList"]:
            for datain_new in data_new["origDestOptionList"]:
                datalist.append(datain_new["origDestOptionPath"])
        return datalist

    def compareRoute(self,data1,data2):
        comparelist = []
        data_old = self.handleRoute(data1)
        data_new = self.handleRoute(data2)
        comparelist = [val for val in data_old if val not in data_new]
        return comparelist

    def compare(self,old_map,new_map):
        for old_flightNo in old_map[0].keys():
            for new_flightNo in new_map[0].keys():
                if old_flightNo == new_flightNo:
                    try:
                        # error_list = []
                        self.cmp(old_map[0][old_flightNo]["id"], new_map[0][new_flightNo]["id"], "航班号为%sid不一致" % old_flightNo)
                        self.cmp(old_map[0][old_flightNo]["airline"],new_map[0][new_flightNo]["airline"],"航班号为%s航司不一致"% old_flightNo)
                        self.cmp(old_map[0][old_flightNo]["airlineCnName"], new_map[0][new_flightNo]["airlineCnName"], "航班号为%s航司中文不一致" % old_flightNo)
                        self.cmp(old_map[0][old_flightNo]["operationAirline"], new_map[0][new_flightNo]["operationAirline"], "航班号为%s承运航司不一致" % old_flightNo)
                        self.cmp(old_map[0][old_flightNo]["operationAirlineCnName"], new_map[0][new_flightNo]["operationAirlineCnName"],
                                 "航班号为%s承运航司中文不一致" % old_flightNo)
                    except Exception, e:
                        print Exception, ":", e
                    if len(error_list) >= 1:
                        # 对比结果错误写入txt
                        error_info = ';'.join(error_list)
                        try:
                            output1 = open("%s\\result_RoutingMapJson.txt" % dir, 'w')
                            output1.write(error_info)
                            output1.write('\n')
                        except Exception, e:
                            print Exception, ":", e
                        finally:
                            output1.close()


if __name__ == '__main__':
    path_old = "D:\\MyConfiguration\\TCLDUSER\\Desktop\\shopping.txt"
    path_new = "D:\\MyConfiguration\\TCLDUSER\\Desktop\\shopping1.txt"
    path_old_route = "C:\\Users\Administrator\\Documents\\QQEIM Files\\2355905601\\FileRecv\\HKG-CI-TPE-OZ-SEL.json"
    path_new_route = "C:\\Users\Administrator\\Documents\\QQEIM Files\\2355905601\\FileRecv\\HKG-CI-TPE-OZ-SEL1.json"
    # error_list = []  # 错误信息列表
    t_now = time.strftime('%Y%m%d_%H%M%S', time.localtime(time.time()))
    dir = 'D:\\test_result\\' + t_now + '\\'  # 错误信息存储路径
    os.mkdir(dir)
    test = Compare()
    all_old_flight_datas = test.read(path_old)
    all_new_flight_datas = test.read(path_new)
    all_old_json_datas = test.read(path_old_route)
    all_new_json_datas = test.read(path_new_route)
    list_1 = test.compareRoute(all_old_json_datas, all_new_json_datas)
    list_2 = test.compareRoute(all_new_json_datas, all_old_json_datas)
    print "新接口存在但老接口不存在的route有：",list_1
    print "老接口存在但老接口不存在的route有：",list_2
    old_map = test.setDict(all_old_flight_datas)
    new_map = test.setDict(all_new_flight_datas)
    test.compare(old_map,new_map)
    print test.code(path_new)

