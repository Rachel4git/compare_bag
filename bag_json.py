# -*- coding:utf-8 -*-

import os
import time
import json

#读取 txt文件,返回list
def txt_read(path):
    try:
        txt_obj = open(path,'r')
        txt_data =  txt_obj.readlines()
        return txt_data
    except Exception,E:
        print  Exception,":",E
    finally:
        txt_obj.close()

#读取txt文件，返回json
def json_read(path):
    try:
        json_obj = open(path,'r')
        json_data = json.loads(json_obj.read().decode("GB2312"))
        return json_data
    except Exception,E:
        print  Exception,":",E
    finally:
        json_obj.close()

#字段值转换
def proProcess(json_data):
    #获取flightSegments
    flightSegments = json_data['flightSegments'] # flightSegments为列表形式
    l=len(flightSegments)
    #初始化
    orgiDestSeqID=[None]*l
    segmentSeqID=[None]*l
    aircode=[None]*l
    departure=[None]*l
    arrival=[None]*l
    departureCityCode = [None] * l
    arrivalCityCode = [None] * l
    cabinclass=[None]*l
    isMainSegment=[None]*l
    operatingFlightNumber=[None]*l
    bag=[None]*l
    #遍历&取值&转换
    for i in range(0, l):
         orgiDestSeqID[i]= flightSegments[i]['orgiDestSeqID']
         segmentSeqID[i] = flightSegments[i]["segmentSeqID"]
         aircode[i] = flightSegments[i]["aircode"]
         departure[i] = flightSegments[i]["departure"]
         arrival[i] = flightSegments[i]["arrival"]
         departureCityCode[i] = flightSegments[i]["departureCityCode"]
         arrivalCityCode[i]=flightSegments[i]["arrivalCityCode"]
         cabinclass[i] = flightSegments[i]["cabinClass"]
         isMainSegment[i]=flightSegments[i]["isMainSegment"]
         operatingFlightNumber[i]=flightSegments[i]["operatingFlightNumber"]
         bag[i] = flightSegments[i]["bag"]
    #
    routing=rout(l,departure,aircode,arrival)
    aircodes=air_codes(l,aircode)
    cabinclasses=cabin_class(l,isMainSegment,cabinclass)
    connections, depCtiy,arrCity= connect(l,orgiDestSeqID,segmentSeqID,departure,arrival)
    subtag=sub_tag(l,aircode,operatingFlightNumber)
    operating=operate(l, operatingFlightNumber)
    bags=""
    for i in range(0,l):
        if isMainSegment[i] == "1":
            if str(bags) != "":
                bags = bags+"|"
            bags = bags+bags_(bag[i])

    #写入字典
    idb_S1_dict = {}
    #与数据源格式有关
    idb_S1_dict.setdefault('fillingairline', json_data['ticketCarrier'])
    idb_S1_dict.setdefault('pax_Type', "ADT")
    idb_S1_dict.setdefault('createTime', json_data['createDate'])
    idb_S1_dict.setdefault('source', json_data['engineType'])
    idb_S1_dict.setdefault('tracerId', json_data['traceId'])

    idb_S1_dict.setdefault('aircodes', aircodes)
    idb_S1_dict.setdefault('arrCity',arrCity )
    idb_S1_dict.setdefault('depCity',depCtiy )
    idb_S1_dict.setdefault('detail_link', )
    idb_S1_dict.setdefault('routing', routing)  # depairport-marktingairlin-ariport
    idb_S1_dict.setdefault('connections', connections)
    idb_S1_dict.setdefault('cabinclass',cabinclass )
    idb_S1_dict.setdefault('bags', bags)
    idb_S1_dict.setdefault('sub_tag', sub_tag)  #？？？？？？？？？？？？？、、
    return idb_S1_dict

#routing,
def rout(L,departure,aircode,arrival):
    rou=[None]*L
    routing=""
    for i1 in range(0, L):
        #routing
        rou[i1]=departure[i1]+"-"+aircode[i1]+"-"+arrival[i1]
        if i1==0:
            routing = routing +  rou[i1]
        else:
            routing = routing + "/" + rou[i1]

    return  routing

#aircodes,
def air_codes(L,aircode):
    aircodes=""
    for i in range(0, L):
        # aircodes
        if i == 0:
            aircodes = aircodes + aircode[i]
        else:
            aircodes = aircodes + "|" + aircode[i]
    return  aircodes

#cabinclass,
def cabin_class(L,isMainSegment,cabinclass):
    cabinclasses=""
    for i in range(0, L):
        # cabinclass
        if isMainSegment[i] == "1":
            a=cabinclass[i]
            cabinclasses = cabinclasses + cabinclass[i]
    return cabinclasses

# operating
def operate(L,operatingFlightNumber):
    operating=""
    for i in range(0, L):
        if i == 0:
            operating = operating + operatingFlightNumber[i][0:2]
        else:
            operating = operating + "|" + operatingFlightNumber[i][0:2]
    return  operating

#sub_tag 是否有附表
def sub_tag(L,aircode,operatingFlightNumber):
    subtag="0"
    for i in range(0, L):
        if aircode[i] != operatingFlightNumber[i][0:1]:
            subtag ="1"
    return subtag

#bags
def bags_(bag):
    bags=""
    a=len(bag)
    if len(bag)==1:
        b=bag.keys()[0]
        if str(bag.keys()[0]) =='allowedPieces':
            bags=bags+bag[bag.keys()[0]]+"/"+"PC"
        if str(bag.keys()[0]) =="allowedWeight":
            bags = bags+bag[bag.keys()[0]]+ "/" + "KG"
    else:
        if len(bag)==2:
            if str(bag.keys()[0])=="allowedPieces"  and  str(bag.keys()[1])=="allowedWeight":
                bags = bags + bag[bag.keys()[0]]+"/"+"PC"+","+bag[bag.keys()[1]]+ "/" + "KG"
            if str(bag.keys()[0])=="allowedWeight"  and  str(bag.keys()[1])=="allowedPieces":
                bags = bags + bag[bag.keys()[0]]+"/"+"KG"+","+bag[bag.keys()[1]]+ "/" + "PC"
    return  bags

#connections,dep_city, arr_city
def connect(L,orgiDestSeqID,segmentSeqID,departureCityCode,arrivalCityCode):
    connections=""
    if L==1:
        connections="S"
        depCtiy= departureCityCode[0]
        arrCity= arrivalCityCode[0]
    else:
        if L ==4:
            connections = "X-S-X-S"
            depCtiy = departureCityCode[0]
            arrCity = arrivalCityCode[1]
        else:
            if L==2:
                if segmentSeqID[1]-orgiDestSeqID ==0:
                    connections = "S-S"
                    depCtiy = departureCityCode[0]
                    arrCity = arrivalCityCode[0]
                else:
                    connections = "X-S"
                    depCtiy = departureCityCode[0]
                    arrCity = arrivalCityCode[1]
            else:
                if L ==3 :
                    if segmentSeqID[1]-orgiDestSeqID ==0:
                        connections="S-X-S"
                        depCtiy = departureCityCode[0]
                        arrCity = arrivalCityCode[0]
                    else:
                        connections ="X-S-S"
                        depCtiy = departureCityCode[0]
                        arrCity = arrivalCityCode[1]
    return connections,depCtiy,arrCity

if __name__ == '__main__':
    a = json_read(r'D:\MyConfiguration\hd48552\Desktop\S1-searchdetail (2).txt')
    print(a['engineType'])
    r=proProcess(a)
    print(r)