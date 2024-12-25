import requests
import hashlib
from prettytable import PrettyTable as pt
from datetime import datetime
import os


#pyinstaller -i D:\下载\OIP-C256x256.ico --onefile 飞跃家长.py
def isint(num):
    try:
        num=int(num)
        return num
    except:
        return -1
def show(json_data):
    print(f"总分：{json_data['student_score']} 校排：{json_data['grade_rank']} 班排：{json_data['class_rank']}")
    scoresdata=json_data['subject_rank']
    tb = pt()
    tb.field_names = ["学科", "成绩", "赋分后", "班级排名","班级平均分(未赋分)","年级排名","年级平均分(未赋分)"]
    for i in range(len(scoresdata)):
        for b in scoresdata:
            if b['subject_id']==i+1:
                tb.add_row([b['subject_name'],b['score'],b["degree_score"] if 'degree_score' in b else "-",
                            b['class_rank'],b['class_mean'],b['grade_rank'],b['grade_mean']])
    tb.align = "c"
    print(tb)
def zhuangbi():
    print("""_________          ____.  _____.___.
\_   ___ \        |    |  \__  |   |
/    \  \/        |    |   /   |   |
\     \____   /\__|    |   \____   |
 \______  /   \________|   / ______|
        \/                 \/       """)
def begin():
    try:
        global head1,head,stuid,studentdata
        os.system('cls')
        zhuangbi()
        print("\n飞阅学生成绩查询工具\n")
        head1={"User-Agent":"Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/126.0.0.0 Safari/537.36 Edg/126.0.0.0"}
        username=input("请输入账号：")
        password=input("请输入密码：")
        #username = 13859852523
        #password = "Aa123456"
        os.system('cls')
        x = hashlib.md5()
        x.update(password.encode('utf-8'))
        data={"username":username,"password":x.hexdigest(),
              "captcha_token":"610824a5-1d90-479c-853c-0ecbd6b25a49",
              "verification_code":""}
        url="https://api2.xiaoxianai.cn/authorizations/parent/auth?"
        response = requests.post(url, data=data,headers=head1,allow_redirects=True)
        #print(response.text)
        json_data = response.json()
        #stuid=json_data['id']
        atoken=json_data['access_token']
        #print(atoken)
        head = {
            "Accept": "*/*",
            "Accept-Encoding":"gzip, deflate, br, zstd",
            "Accept-Language": "zh-CN,zh;q=0.9,en-US;q=0.8,en;q=0.7",
            "Authorization": "Bearer "+atoken,
            "Connection": "keep-alive",
            "Host": "api2.xiaoxianai.cn",
            "Origin": "https://mjz.xiaoxianai.cn",
            #"Priority": "u=1, i",
            "Referer": "https://mjz.xiaoxianai.cn/",
            "Sec-Ch-Ua": '"Not/A)Brand";v="8", "Chromium";v="126", "Google Chrome";v="126"',
            "Sec-Ch-Ua-Mobile": "?0",
            "Sec-Ch-Ua-Platform": '"Windows"',
            "Sec-Fetch-Dest": "empty",
            "Sec-Fetch-Mode": "cors",
            "Sec-Fetch-Site": "same-site",
            "User-Agent": "Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/126.0.0.0 Safari/537.36"
        }
        response = requests.get("https://api2.xiaoxianai.cn/students/list/parent?", headers=head,allow_redirects=True)
        #print(response.text)
        json_data = response.json()
        studentdata=json_data['student_data'][0]
        stuid=studentdata['uid']
        response = requests.get(f"https://api2.xiaoxianai.cn/parentmobile/schoolyears?&student_uuid={stuid}", headers=head, allow_redirects=True)
        json_data = response.json()
        global years
        years=[]
        for year_data in json_data["all_years"]:
            # 将每个学年的年份添加到列表中
            years.append(year_data["year"])
        #print(f"信息：{studentdata['school_name']}{studentdata['grade_name']}{studentdata['class_name']}班 {studentdata['name']}")
        #print(stuid)
    except Exception as e:
        # 捕获所有异常，并打印异常信息
        print(f"\nError：{e} \n按下Enter键重试...")
        input()
        os.system('cls')
        begin()
def showexam():
    os.system('cls')
    global years
    global stuid,studentdata
    print(f"信息：{studentdata['school_name']}{studentdata['grade_name']}{studentdata['class_name']}班 {studentdata['name']}")

    print(f"\n     {years[0]}-{years[-1]}考试列表")
    reports=[]
    for year in years:
        response = requests.get(f"https://api2.xiaoxianai.cn/parentmobile/totalscore/list?student_uuid={stuid}&year={year}", headers=head,allow_redirects=True)
        json_data = response.json()
        reports = reports+json_data['reports']
    #print(json_data)
    if len(reports)==0:
        print("没有考试！\n按Enter键返回...")
        input()
        caidan()
    for i in range(len(reports)):
        print(f"【{i+1}】 {reports[i]['name'].replace("\n","")}")

    num=input("请输入查询考试序号（按Enter键返回）：")
    num=isint(num)
    while((num>len(reports))or(num<0)):
        num=isint(num)
        if num==-1:
            caidan()
        print("输入无效，请重新输入。")
        num = input("请输入查询考试序号：")
        num = isint(num)
    #获取单次考试内容
    response = requests.get(f"https://api2.xiaoxianai.cn/parentmobile/totalscore/detail?student_uuid={stuid}&report_uuid={reports[num-1]['uuid']}", headers=head,allow_redirects=True)
    json_data = response.json()
    print(f"\n\n总分：{json_data['student_score']} 校排：{json_data['grade_rank']} 班排：{json_data['class_rank']}")
    scoresdata = json_data['subject_rank']
    tb = pt()
    tb.field_names = ["学科", "成绩", "赋分后", "班级排名", "班级平均分(未赋分)", "年级排名", "年级平均分(未赋分)"]
    for i in range(len(scoresdata)):
        for b in scoresdata:
            if b['subject_id'] == i + 1:
                tb.add_row([b['subject_name'], b['score'], b["degree_score"] if 'degree_score' in b else "-",
                            b['class_rank'], b['class_mean'], b['grade_rank'], b['grade_mean']])
    tb.align = "c"
    print(tb)
    print("按下Enter键返回...")
    input()
    os.system('cls')
    caidan()


# pyinstaller -i D:\BaiduNetdiskDownload\121920362533_0OIP-C.ico --onefile 飞跃家长.py
def showsubject():
    os.system("cls")
    global years
    global stuid,studentdata
    print(f"信息：{studentdata['school_name']}{studentdata['grade_name']}{studentdata['class_name']}班 {studentdata['name']}")
    current_datetime = datetime.now()
    # 提取年份
    current_year = current_datetime.year
    print(f"\n    科目")
    response = requests.get(f"https://api2.xiaoxianai.cn/subjects?student_id={stuid}", headers=head,allow_redirects=True)
    json_data = response.json()
    subjects = {}  # 初始化一个空字典来存储科目信息
    for b in json_data:
        subjects[b['id']] = b['name']  # 将id和name存储到字典中

    # 对字典的键进行排序，并打印排序后的id和name
    for i, j in sorted(subjects.items(), key=lambda item: item[0]):
        print(f"【{i}】 {j}")
    num1=input("\n请输入要查询的科目（按Enter键返回）：")
    num1=isint(num1)
    while(num1 not in subjects):
        num1=isint(num1)
        if num1==-1:
            caidan()
        print("输入无效，请重新输入。")
        num1 = input("请输入查询考试序号：")
        num1 = isint(num1)

    subjectname=subjects[num1]
    papers=[]
    for year in years:
        response = requests.get(f"https://api2.xiaoxianai.cn/parentmobile/singlestatus?student_uuid={stuid}&subject_id={num1}&year={year}", headers=head,
                                allow_redirects=True)
        json_data = response.json()
        papers=papers+json_data['papers']
    if len(papers)==0:
        print("没有考试！")
        input("按Enter键返回...")
        showsubject()
    print(f"\n     {years[0]}-{years[-1]}考试列表")
    for i in range(len(papers)):
        print(f"【{i+1}】 {papers[i]['paper_name'].replace("\n","")}")

    num = input("请输入查询考试序号（按Enter键返回）：")

    num=isint(num)
    while (int(num) > len(papers) or (int(num) < 1)):
        num = isint(num)
        if num == -1:
            showsubject()
        print("输入无效，请重新输入。")
        num = input("请输入查询考试序号：")
        num = isint(num)
    print(f'\n\n{subjectname} {papers[num-1]['paper_name'].replace("\n","")}')
    response = requests.get(
        f"https://api2.xiaoxianai.cn/parentmobile/teststatus?&answer_uid={papers[num-1]['answer_uid']}&subject_id={num1}&student_uuid=006158a2-4769-4324-8231-c228a47fa7f9&year={current_year}",
        headers=head,
        allow_redirects=True)
    score_data1 = response.json()

    response = requests.get(
        f"https://api2.xiaoxianai.cn/parentmobile/gradedis?&answer_uid={papers[num-1]['answer_uid']}&subject_id={num1}",
        headers=head,
        allow_redirects=True)
    score_data2 = response.json()

    tb = pt()
    tb.field_names = [ "成绩",  "班级排名", "班级平均分(未赋分)","班级最高分", "年级排名", "年级平均分(未赋分)","年级最高分","错题数"]
    tb.add_row([score_data1['test_info']['student_score'],score_data1['test_info']['class_rank'],score_data1['test_info']['class_mean'],score_data2['class']['highest_score'],
                score_data1['test_info']['grade_rank'],score_data1['test_info']['grade_mean'],score_data2['grade']['highest_score'],score_data1['wrong_count']])
    tb.align = "c"
    print(tb)
    print("按下Enter键返回...")
    input()
    os.system('cls')
    showsubject()
def caidan():
    os.system('cls')
    zhuangbi()

    print(f"信息：{studentdata['school_name']}{studentdata['grade_name']}{studentdata['class_name']}班 {studentdata['name']}")
    print("【1】查看考试（若在考试中没有可以尝试2）")
    print("【2】查看单科目")
    print("【3】退出登录")

    num=input("请输入序号：")
    try:
        while ((int(num)>3)or (int(num)<1)):
            print("无效数字，请重新输入：",end="")
            num=input()
        if int(num)==1:
            showexam()
        if int(num)==2:
            showsubject()
        if int(num)==3:
            begin()
    except Exception as e:
        caidan()

begin()
caidan()
