from use_func import use_func


#=============================================================
#检测数字函数
def detector(kinds,string,sex): #查询是否为整数，且长度是否正确
    flag = int_func(string)#先进行整数检测
    type = 'OK'
    msg = 'OK'
    if flag == 1:#检测不通过
        type="输入的参数必须为整数"
    #进行分别的长度或范围检测
    if kinds =="number":
        if len(string)!=4: #检测长度
            msg = "学号的长度为4位"
    if kinds =="age":
        if type=="OK": #说明是整数
            if int(string)>100 or int(string)<10: #检测岁数
                msg = "年龄必须大于10岁低于100岁"
    if kinds =="dormitory":
        if type=="OK":
            if sex == "男":
                if int(string)<100 or int(string)>199:
                    msg = "男生寝室的范围是100~199"
            else:
                if int(string)<200 or int(string)>299:
                    msg = "女生寝室的范围是200~299"
    if type =="OK" and msg=="OK":
        return {"flag":"OK"}
    else:#返回错误信息
        return {"flag":"NO","type":type,"msg":msg}
#=============================================================
#判断是否为整数
def int_func(string):
    detection_arr = [0]  # 初始化一个检测数组
    k = 0
    init_num = 0
    # 创建一个数字的检测数组
    for i in range(10):
        detection_arr.insert(k, str(i))
        k += 1
    for value in string:
        if value not in detection_arr:
            init_num = 1
            return init_num
#=============================================================
# 查询函数
def find_data(kinds,num): #查询number 和 dormitory 返回值为OK 和 NO
    # 初始化状态值
    dormitory_flag=0
    number_msg = "OK"
    dormitory_msg = "OK"
    data_list = [0]
    key = 0
    #得到全局变量
    for line in use_func.all_data:
        if kinds=="number":#查询学号
            if line["number"]==num:
                number_msg = "NO"
                break
        if kinds=="dormitory":#查询寝室
            if line["dormitory"]==num:
                dormitory_flag+=1
                if dormitory_flag>=4: #满员
                    dormitory_msg = "NO"
        if kinds=="specific_print":#返回一个数据列表
            if line["dormitory"]==num:#如果寝室号相同
                data_list.insert(key,line)#将这行数据加入到列表中
                key+=1
        if kinds=="all_print":
            data_list.insert(key, line)  # 将这行数据加入到列表中
            key += 1
        # print(line.rstrip())
    if kinds!="specific_print" and kinds!="all_print":
        return {"number":number_msg,"dormitory":dormitory_msg}
    else:#返回查询到的消息
        return data_list
#=============================================================
#打印信息
def console(ele_son):
    print(
        "            | ",
        ele_son["number"],
        " |   ",
        ele_son["name"],
        "   |  ",
        ele_son["sex"],
        "  |  ",
        ele_son["age"],
        "  |  ",
        ele_son["dormitory"],
        "   |   ",
    )
    print(" ")
#=============================================================
#遍历输出
def map_list(value):
    print(value[0])#打印出第一项的信息
    value = value[1:]#截取掉第一项的信息
    _index = 1
    for index in value:
        _index += 1
        print(index,end=" ")
        if  len(value)>10 and _index > 10:
            print("\n")
            _index=1 #初始化
    print("\n")
#=============================================================
#清空文件
def clear():
    # 先将文件进行清空
    with open('data/data.txt', "r+") as f:
        f.seek(0)
        f.truncate()  # 清空文件