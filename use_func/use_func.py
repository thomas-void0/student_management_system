import random
from tools import tools
import ast
import json
#定义一个全局变量作为状态值进行返回
CHANGE_FLAG = 0
#定义一个全局变量接收文件数据
all_data = [0]
#进入系统后在这里读取信息，
with open("data/data.txt", encoding='GBK') as file_obj:
    lines = file_obj.readlines()  # 将数据读取为一个列表
for line in lines:
    line = line[0:-1] #将每一行的换行符去掉
    line = ast.literal_eval(line)  # 将序列化的字符串数据转换为字典
    all_data.append(line)
#清除掉全局列表中的默认值0
all_data.remove(0)   #all_data是所有的数据
#==========================================主界面的显示信息=============================================
def show_view():
    info = '''
  |----------主菜单---------|
    ｜ 1 添加学生信息  ｜
    ｜ 2 打印学生信息  ｜
    ｜ 3 调整学生寝室  ｜
    ｜ 4 查看寝室信息  ｜ 
    ｜ 5 退出系统      ｜ 
    < "注意:数据将在退出系统操作时进行保存，请务必使用输入索引值的方式进行退出!">
    '''
    print(info)
#==========================================录入成员信息=============================================
def add_infomation():
    while True:
        #学号
        while True:
            student_number = input("请输入学号:")
            #进行学号的检测，学号必须为纯数字,长度不超过4个，并且必须唯一,
            number_state = tools.detector("number", student_number, "null") #检测类型和长度
            if number_state["flag"]=="OK":
                student_number = int(student_number)
                number_flag = tools.find_data("number", student_number)["number"]  #检测是否唯一
                if number_flag == 'OK':
                    break
                else:
                    print("该学号已经存在了,请重新输入!")
            else:
                if number_state["type"]=="OK":
                    print(number_state["msg"])
                else:
                    print(number_state["type"])
        #姓名
        student_name = input("请输入姓名:")
        #性别
        while True:
            student_sex = input("请输入性别:")
            if student_sex == "男" or student_sex == "女":
                break
            else:
                print("暂不接受其他性别")
        #年龄
        while True:
            student_age = input("请输入年龄:")
            age_state = tools.detector("age", student_age, "null") #检测类型和长度
            if age_state["flag"]=="OK":
                student_age = int(student_age)
                break
            else:
                if age_state["type"]=="OK":
                    print(age_state["msg"])
                else:
                    print(age_state["type"])
        #寝室
        info_dormitory = '''
            | 请选择寝室的分配 |
        |男生为100开始，女生为200开始|
               | 1 手动分配 |
               | 2 自动分配 |
        '''
        print(info_dormitory)
        num = input("请输入对应的索引值:")
        if num == '1':#手动分配
            while True:
                student_dormitory = input("请分配寝室:")
                #1,先检测寝室的输入是否为整数
                dormitory_state = tools.detector("dormitory", student_dormitory, student_sex)  # 检测类型和长度
                if dormitory_state["flag"] == "OK":
                    student_dormitory = int(student_dormitory)
                    # 判断寝室是否满员
                    dormitory_flag = tools.find_data("dormitory", student_dormitory)["dormitory"]
                    if dormitory_flag == 'NO':
                        tip_dormitory = '''
                            | 该寝室已经满员了，系统将进行随机分配：|
                            | 确认请输入 1                          |
                            | 重新分配请输入 2                      |
                        '''
                        print(tip_dormitory)
                        restart_num = input("*请输入对应的索引值:")
                        if restart_num=="1":
                            student_dormitory = auto_allot(student_sex)  # 调用自动分配函数
                            break
                    else:
                        print("分配成功")
                        break  # 退出循环
                else:
                    if dormitory_state["type"] == "OK":
                        print(dormitory_state["msg"])
                    else:
                        print(dormitory_state["type"])
        else:#自动分配
            student_dormitory = auto_allot(student_sex) #调用自动分配函数
        doc_information = {
            "number":student_number,
            "name":student_name,
            "sex":student_sex,
            "age":student_age,
            "dormitory":student_dormitory
        }
        #将新添加的数据放入到全局数据中
        all_data.append(doc_information)
        # 询问是否还要继续录入信息
        text = '''
            | 是否还要继续录入信息？ |
            | 1,是                   |
            | 2,返回主菜单           |
        '''
        print(text)
        text_num = input("请输入对应索引值:")
        if text_num != "1":
            break
#自动分配函数
def auto_allot(student_sex):
    while True:
        # 利用random生成随机数，实现随机分配寝室
        # 检测是男是女
        if student_sex == "男":
            student_dormitory = int(random.uniform(100, 199))
        else:
            student_dormitory = int(random.uniform(200, 299))
        # 进行查询--j文件中随机分配一个寝室---调用查询函数
        dormitory_flag = tools.find_data("dormitory", student_dormitory)["dormitory"]
        if dormitory_flag == "OK":
            print("*自动分配成功!*")
            print(" *寝室号是:", student_dormitory)
            return student_dormitory
#==========================================打印寝室成员列表=============================================
def display_members():
    while True:
        #输入需要打印的寝室
        info = '''
            | 1，根据寝室号打印 |
            | 2，全部打印       | 
            | 3，根据学号打印   |
            | 4, 根据姓名打印   |
        '''
        print(info)
        num = input("*请输入对应的索引值:")
        if num=="1":
            number = input("*请输入需要查询的寝室号:")
            #做一个检测，输入的是否是整数以继是否符合寝室标准要求
            flag = 0
            if number!='':
                flag = tools.detector("NULL", number, "NULL")  # 只检测是否为整数即可
            if flag["flag"]=="OK":
                number = int(number)
                #检测输入的寝室号是否正确
                if 100<=number and number<300:
                    members_list = tools.find_data("specific_print", number)
                    members_list.remove(0)
                    length = len(members_list)
                    if length>0:
                        text = '''
                        该寝室所有入住人员的信息：
                        '''
                        print(text)
                        table_head = '''
            |  学号  |    姓名    |  性别  |  年龄  |  寝室号  |
                        '''
                        print(table_head)
                        for content in members_list:
                            tools.console(content)
                    else:
                        print("输入的寝室中暂没有人入住")
                else:
                    print("请输入正确的寝室号，男生为100~199，女生为200~299")
            else:
                print(flag["type"])
        elif num=="2":#全部打印
            print("所有入住人员的信息:")
            #对列表进行排序
            center_list = [0]
            key = 0
            #取出所有元素寝室的索引值
            for content in all_data:
                center_list.insert(key,content["dormitory"])
                key+=1
            #列表去重
            center_list.remove(0)
            center_list = list(set(center_list))
            #初始化一个最终的数组---最终生成一个2维数组
            end_arr=[0]
            #初始化一个存储数组
            storage_arr = [0]
            # 初始化索引值
            arr_index = 0
            end_arr_index = 0
            for index in center_list:
                for find_index in all_data:
                    if find_index["dormitory"] == index:#判断列表中的寝室号是否与指定的相同
                        storage_arr.insert(arr_index,find_index)
                        arr_index+=1
                storage_arr.remove(0) #删除定义数组时的元素0
                end_arr.insert(end_arr_index,storage_arr)#将每一个寝室的数组存储到最终数组中
                end_arr_index+=1
                arr_index = 0  #对应寝室号查询完毕后 初始化索引值
                storage_arr=[0] #初始化存储数组
            #处理二维数组，打印出每一个寝室的结果
            end_arr.remove(0)
            for ele in end_arr: #ele是每一个寝室对应所有成员信息
                print("====================",ele[0]["dormitory"],"寝室中所有成员信息如下====================\n")
                table_head = '''
            |  学号  |    姓名    |  性别  |  年龄  |  寝室号  |
                '''
                print(table_head)
                for ele_son in ele: #eke_son是寝室中每一个人的详细信息
                    tools.console(ele_son)
        elif num=="3":#根据学号查询
            while True:
                init_num=0
                number = input("*请输入一个学号")
                #对输入的学号进行检测
                flag = tools.detector("number", number, "NULL")
                if flag["flag"]=="OK":
                    number=int(number)
                    for item in all_data:
                        if item["number"]==number:#如果找到相同的学号
                            init_num=1
                            #打印出来这个学生的信息
                            table_head = '''
            |  学号  |    姓名    |  性别  |  年龄  |  寝室号  |
                                '''
                            print(table_head)
                            tools.console(item)
                            break #终止循环
                    if init_num==1:
                        init_num = 0 #初始化
                        break
                    else:
                        print("没有这个学号的学生信息")
                else:
                    if flag["type"]=="OK":
                        print(flag["msg"])
                    else:
                        print(flag["type"])
        else: #根据姓名查询
            while True:
                name = input("*请输入一个名字:")
                key=0
                name_flag=0
                #初始化一个存储数组
                storage_arr=[0]
                #获取查询的数组 all_data
                for item in all_data:
                    if item["name"] == name:
                        #加入到存储数组中
                        storage_arr.insert(key,item)
                        name_flag=1
                storage_arr.remove(0)
                if name_flag==0:#没有找到这个学生
                    print("没有这个姓名的学生")
                else:
                    table_head = '''
            |  学号  |    姓名    |  性别  |  年龄  |  寝室号  |
                                        '''
                    print(table_head)
                    for i in storage_arr:
                        # 打印出来这个学生的信息(可能会有重名的)
                        tools.console(i)
                    break
        #询问是否还要继续打印
        text='''
            | 是否还要继续打印？ |
            | 1,是               |
            | 2,返回主菜单       | 
        '''
        print(text)
        text_num = input("请输入对应索引值:")
        if text_num!="1":
            break
#==========================================调整学生寝室=============================================
def change_dormitory():
    while True:
        text='''
        |  1, 调整学生寝室  |
        |  2, 删除学生信息  |
        |  3, 返回主菜单    |
        '''
        print(text)
        number = input("*请输入对应的索引值:")
        if number=="1":#调整学生寝室
            while True:
                one_info='''
                        |---1, 根据学号调整---|
                        |---2, 根据姓名调整---|
                        |---3, 返回上一级  ---|
                '''
                print(one_info)
                one_num = input("*请输入对应的索引值:")
                if one_num=="1":
                    while True:
                        print(":")
                        text = """
                            |------根据学号进行调整------|
                            |------1, 继续调整     ------|
                            |------2, 返回上一级   ------|
                        """
                        print(text)
                        flag_num = input("*请输入对应的索引值:")
                        if flag_num=="1":
                            stu_num = input("*请输入一个学号:")
                            stu_num = int(stu_num)
                            #将学号在全局中进行查找，然后将信息呈现出来进行确认
                            key = 0
                            sex = 0
                            for index in all_data:
                                if index["number"] == stu_num:
                                    sex = index["sex"]
                                    key=1
                                    table_head = '''
            |  学号  |    姓名    |  性别  |  年龄  |  寝室号  |
                     '''
                                    print(table_head)
                                    tools.console(index) #打印出学生信息
                            if key!=1:
                                print("没有查找到该学号的信息.")
                                key = 0 #初始化
                            else:
                                while True:
                                    #查询到了信息后，询问是否调整该学生的信息
                                    content='''
                                    |----是否调整该学生的寝室？----|
                                    |----1, 是                 ----|
                                    |----2, 返回上一级         ----|
                                    '''
                                    print(content)
                                    num = input("*请输入对应的索引值：")
                                    if num=="1":#进入调整
                                        flag = "OK" #用于检测寝室是否满员
                                        global CHANGE_FLAG
                                        while True:#CHANGE_FLAG改变后，结束这个循环到上一级的循环中去
                                            if CHANGE_FLAG==0:#如果全局为0
                                                dormitory_number = input("*请输入一个需要调整的寝室号:")
                                                dormitory_number = int(dormitory_number)
                                                if sex == "男":
                                                    if dormitory_number < 100 or dormitory_number >= 200:
                                                        print("输入的寝室号不合理，男生为100~199")
                                                        flag = "NO"
                                                else:
                                                    if dormitory_number < 200 or dormitory_number >= 300:
                                                        print("输入的寝室号不合理，女生为200~299")
                                                        flag = "NO"
                                                if flag == "OK":
                                                    # 检测对应的寝室号是否满员
                                                    key = 0
                                                    for index in all_data:
                                                        if index["dormitory"] == dormitory_number:
                                                            key += 1
                                                        if key >= 4:
                                                            break
                                                    if key >= 4:
                                                        print("该寝室已经满员了,请重新调整")
                                                        # 这里提供重新输入寝室号的方案
                                                        key = 0
                                                    else:  # 寝室可以分配
                                                        # 根据学号查找到更改寝室
                                                        for i in all_data:
                                                            if i["number"] == stu_num:
                                                                i["dormitory"] = dormitory_number
                                                                print("调整成功,返回上一级")
                                                                CHANGE_FLAG = 1
                                                                break
                                                else:
                                                    flag = "OK"  # 初始化，以便下一次的使用
                                            else:
                                                CHANGE_FLAG = 0 #重置全局变量
                                                break #退出循环
                                    else: #返回上一级
                                        break
                        else:
                            print("成功返回上一级")
                            break
                elif one_num=="2":#根据姓名进行调整
                    name_flag_inint=0
                    while True:
                        text='''
                            |---1，两人互换寝室 ---|
                            |---2，单人换寝室   ---|
                            |---3，返回上一级   ---|
                        '''
                        print(text)
                        input_num=input("*请输入对应的索引值：")
                        if input_num=="1":
                            if name_flag_inint==0:
                                print("执行2个人互换寝室")
                                while True:
                                    name_one = input("*请输入第一个名字：")
                                    name_two = input("*请输入第二个名字:")
                                    # 初始化两个存储名字的数组
                                    one_list = [0]
                                    two_list = [0]
                                    # 查询姓名是否均存在
                                    for name in all_data:
                                        if name["name"] == name_one:
                                            one_list.append(name)
                                        elif name["name"] == name_two:
                                            two_list.append(name)
                                    if len(one_list) > 1 and len(two_list) > 1:
                                        one_list.remove(0)
                                        two_list.remove(0)
                                        # 打印出分别的学生信息
                                        print("第一个：")
                                        table_head = '''
            |  学号  |    姓名    |  性别  |  年龄  |  寝室号  |
                                                                            '''
                                        print(table_head)
                                        for one in one_list:
                                            tools.console(one)
                                        print("\n")
                                        table_head = '''
            |  学号  |    姓名    |  性别  |  年龄  |  寝室号  |
                                                                            '''
                                        print(table_head)
                                        for two in two_list:
                                            tools.console(two)
                                        # 如果学生有多个提示输入学号进行检索
                                        print("如表所示:\n名叫", name_one, "的学生有", len(one_list), "个")
                                        print("名叫", name_two, "的学生有", len(two_list), "个")
                                        one_number = input("*请输入指定的第一个学生的学号：")
                                        two_number = input("*请输入指定的第二个学生的学号：")
                                        # 查找这两个学生：
                                        one_student = 0
                                        two_student = 1
                                        k = 0  # 初始化一个索引值
                                        one_index = 0
                                        two_index = 0
                                        temp = 0
                                        for student in all_data:
                                            if student["number"] == int(one_number):
                                                one_student = student
                                                one_index = k
                                            elif student["number"] == int(two_number):
                                                two_student = student
                                                two_index = k
                                            k += 1
                                        # 判断他们的性别
                                        if one_student["sex"] != two_student["sex"]:
                                            print("男女生不能进行寝室交换")
                                        else:
                                            temp = all_data[one_index]["dormitory"]  # 第一个名字的寝室号
                                            all_data[one_index]["dormitory"] = all_data[two_index]["dormitory"]
                                            all_data[two_index]["dormitory"] = temp
                                            print("互换寝室成功,返回上一级")
                                            break  # 终止循环，返回上一级
                                    elif len(one_list) > 1:
                                        print("查找不到", name_two, "这个学生的信息")
                                    else:
                                        print("查找不到", name_one, "这个学生的信息")
                            else:
                                name_flag_inint=0#初始化
                                break
                        elif input_num=="2":
                            if name_flag_inint==0:
                                #1,输入学生的姓名
                                name=input("*请输入学生的姓名:")
                                #2,查找是否有这个学生
                                name_flag = 0 #记录一个状态值
                                name_lsit = [0]
                                for stu_name in all_data:
                                    if stu_name["name"]==name:
                                        name_flag = 1
                                        name_lsit.append(stu_name) #将学生信息加入到数组中
                                if name_flag=="0":
                                    print("没有这个名字的学生,请重新输入")
                                else:
                                    name_flag = 0#初始化状态值
                                    name_lsit.remove(0) #清楚列表的默认值
                                    table_head='''
            |  学号  |    姓名    |  性别  |  年龄  |  寝室号  |
                                    '''
                                    print(table_head)
                                    for student_info in name_lsit:#遍历打印出学生信息
                                        tools.console(student_info)
                                    if len(name_lsit)>1:
                                        print("名叫",name,"的学生有",len(name_lsit),"个")
                                        print("请根据表格输入对应的学号")
                                        number = input("*请输入对应的学号:")
                                    sex = 0 #初始化一个性别变量
                                    for stu_num in all_data:
                                        if stu_num["number"] == int(number):#查询到这个学生的信息
                                            sex = stu_num["sex"]
                                            table_head = '''
            |  学号  |    姓名    |  性别  |  年龄  |  寝室号  |
                                        '''
                                            print(table_head)
                                            tools.console(stu_num) #打印出这个学生的信息
                                            break #结束for循环
                                    while True:
                                        doc_num = input("*请输入需要调换到的寝室：")
                                        doc_num = int(doc_num)
                                        #检查doc_num是否合理
                                        doc_num_flag = 0
                                        if sex=="男":
                                            if doc_num<100 or doc_num>=200:
                                                doc_num_flag = 1
                                                print("输入的寝室不合理，男生寝室的范围是100~199")
                                        else:
                                            if doc_num<200 or doc_num>=300:
                                                doc_num_flag = 1
                                                print("输入的寝室不合理，女生寝室的范围是200~300")
                                        if doc_num_flag==0: #寝室合法
                                            #检测目标寝室是否满员：
                                            aim_num=0 #初始化一个计数器
                                            for doc in all_data:
                                                if doc["dormitory"]==doc_num:
                                                    aim_num+=1
                                                if aim_num >= 4:
                                                    break #跳出for循环
                                            if aim_num>=4:#说明寝室已经满员了
                                                print("这个寝室已经满员了")
                                            else: #修改全局对象中的寝室号
                                                for doc in all_data:
                                                    if doc["number"]==int(number):
                                                        doc["dormitory"]=doc_num
                                                        break #终止for循环
                                                print("寝室修改成功,返回上一级")
                                                name_flag_inint=1
                                                break
                                        else:#寝室不合法
                                            doc_num_flag=0 #初始化状态值
                            else:
                                name_flag_inint=0 #初始化全局变量
                                break #终止循环，返回到上一级
                        else:
                            break #终止循环 返回上一级
                else:
                    print("返回上一级成功")
                    break
        elif number=="2": #删除学生信息
            while True:
                text='''
                | 1, 根据学号删除     |
                | 2, 根据姓名删除     |
                | 3, 根据寝室号删除     |
                | 4, 清空管理系统信息 |
                | 5, 返回上一级       |
                '''
                print(text)
                del_flag=input("*请输入对应的索引值：")
                if del_flag=="1": #根据学号删除
                    while True:
                        stu_num=input("*请输入学号:")
                        stu_num = int(stu_num)
                        k=0
                        for number in all_data:
                            if number["number"] == stu_num:
                                break #终止循环
                            k+=1
                        if k == (len(all_data)):
                            print("无此学号的学生")
                        else:
                            del all_data[k]
                            print("删除成功，返回上一级")
                            break
                elif del_flag=="2": #根据姓名删除
                    name=input("*请输入需要删除的学生姓名:")
                    #查找姓名
                    k = 0
                    for stu_name in all_data:
                        if stu_name["name"] == name:
                            break
                        k+=1
                    if k == len(all_data):
                        print("没有叫这个名字的学生")
                    else:
                        table_head = '''
            |  学号  |    姓名    |  性别  |  年龄  |  寝室号  |
                                                    '''
                        print(table_head)
                        i=0
                        for stu_name in all_data:
                            if stu_name["name"] == name:
                                tools.console(stu_name)
                                i+=1
                        print("名叫",name,"的学生有",i,"个")
                        del_number=input("*请输入你要删除的学生学号：")
                        _flag = 0
                        for del_n in all_data:
                            if int(del_number)==del_n["number"]:
                                all_data.remove(del_n)
                                _flag = 1
                                break
                        if _flag == 1:
                            print("删除成功,返回上一级")
                            _flag = 0
                            break
                elif del_flag=="3": #根据寝室删除
                    while True:
                        doc_num = input("*请输入需要删除的寝室号:")
                        doc_num = int(doc_num)
                        #查找是否存在寝室号
                        doc_flag = 0
                        for i in all_data:
                            if i["dormitory"] == doc_num:
                                doc_flag =1.
                        if doc_flag==1:#说明这个寝室是存在的
                            #遍历，删除寝室的所有成员
                            k = 0
                            n = 0
                            husa = 0
                            for item in all_data:
                                if item["dormitory"] == doc_num:
                                    n+=1
                                    all_data[k] = 0 #将其变为0
                                k+=1
                                #数组去重 ---子元素为字典
                            while husa<n:
                                all_data.remove(0)
                                husa+=1
                            print("删除成功,返回上一级")
                            break
                        else:
                            print("该寝室不存在")
                elif del_flag=="4":#清空信息
                    tools.clear()
                    print("所有信息删除成功,返回上一级")
                    break
                else:
                    break
        else:#返回主菜单
            print("返回主菜单成功")
            break
#==========================================查看寝室信息=============================================
def examine_dormitory_information():
    while True:
        text='''
            | 1, 统计男女生数量 |
            | 2, 统计空闲寝室   |
        '''
        boy=0
        girl=0
        print(text)
        number = input("*请输入对应的索引值:")
        #生成一个100~299的数组
        dormitory_list = range(299)
        dormitory_list=dormitory_list[100:]#所有的寝室编号
        if number=="1":
            for index in all_data:
                # 统计男女数目
                if index["sex"] == "男":
                    boy += 1
                else:
                    girl += 1
            print("男生的数目是：|----->", boy)
            print("女生的数目是：|----->", girl)
        else:
            init_number=0
            no_body=["|----以下寝室没有人住：----|"]#没有人住
            one_body=["|----以下寝室还可以住3人：----|"]#可以住3人
            two_body=["|----以下寝室还可以住2人：----|"]#可以住2人
            three_body=["|----以下寝室还可以住一人：----|"]#可以住1人
            four_body=["|----以下寝室已满：----|"]#不能住人了
            #统计空余的寝室 和 分别可以容纳的人数==进行数据分类
            for n in dormitory_list:  # n是所有的寝室编号
                for index in all_data:
                    _n = index["dormitory"]  # 文件中的寝室编号
                    if _n == n:  # 将所有的文件中已经存在的寝室进行对比
                        init_number += 1
                # 记录下这个寝室的信息
                if init_number==0:#寝室没有住人
                    no_body.append(n)
                elif init_number==1:#寝室还剩3个空位
                    one_body.append(n)
                elif init_number == 2:#寝室还剩2个空位
                    two_body.append(n)
                elif init_number==3:#寝室还剩一个空位
                    three_body.append(n)
                else: #寝室已满
                    four_body.append(n)
                init_number = 0 #初始化
            #分类统计输出
            all_list = [no_body,one_body,two_body,three_body,four_body]
            for value in all_list:
                if len(value)>1:
                    tools.map_list(value)
        text_info='''
            | 是否还要查看信息？ |
            | 1,是               |
            | 2,返回主菜单       | 
        '''
        print(text_info)
        text_info_num=input("*请输入对应的索引值:")
        if text_info_num!="1":
            break
#==========================================存储数据，生成json=============================================
def save_data():
    #将数据存储到txt文件中===存储之前必须要清空txt文件
    tools.clear()
    #重新将全局变量中的数据写入文件
    file_name = open(r"data/data.txt","a+",encoding="GBK") #打开文件
    for content_dict in all_data:
        file_name.writelines(str(content_dict)+"\n")
    file_name.close() #关闭文件
    # 打开json文件
    with open("data/data.json","w") as f:
        json.dump(all_data,f,sort_keys=True,indent=4,separators=(',',':'),ensure_ascii=False)
    print("json文件写入完成......")