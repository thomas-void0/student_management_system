from use_func import use_func

information =  '''
｜ ----学生寝室管理系统---- ｜    '''
print(information)
while True:
    #调用函数显示主界面
    use_func.show_view()
    #用户输入一个选项进行选择
    num = input("输入对应的选项值:")
    if num=="1":
        print("|----欢迎进入录入页面,请按照提示进行操作----|")
        use_func.add_infomation() # 调用添加函数
    elif num=="2":
        print("|----欢迎进入打印页面,请按照提示进行操作----|")
        use_func.display_members()# 调用打印函数
    elif num == "3":
        print("|----欢迎进入调整寝室页面,请按照提示进行操作----|")
        # 调用调整学生信息函数
        use_func.change_dormitory()
    elif num == "4":
        print("|----欢迎进入查询页面,请按照提示进行操作----|")
        use_func.examine_dormitory_information()
    elif num == "5":
        #退出的时候必须要保存数据
        use_func.save_data()
        print("|----退出系统----|")
        break
    else:
        print("|----输入错误----|")
        # 调用主界面函数


