# coding=utf-8


def  compare(data1 ,data2 ,errInfo):
    error_list=[]

    try:
        if str(data1) != str(data2):
            error_list.append(errInfo)
            error_list.append('{} != {}'.format(data1, data2))
            error_list.append('\n')
            return error_list
        else:
            return 1111111111111
    except Exception, e:
        print Exception, ":", e


if __name__ == '__main__':
    print (compare(1,2,"3333333握手覅"))