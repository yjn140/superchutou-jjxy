# -*- coding:utf-8 -*-
# @Time : 2023/5/30 23:57
# @Author : yjn140
# @File : chutou.py

"""
出头科技九江学院刷课脚本

注意！此脚本仅用于技术交流，不得欺骗刷课，不得构造攻击！
更不得卖钱！我看不起你！

使用方法
1.安装python环境 (winget install python或scoop install python )
2.使用pip命令安装requests urllib3库 pip install requests urllib3
3.运行这个脚本  python chutou.py 或者是 python3 chutou.py
4.输入用户名 回车 输入密码 回车

写这个代码的初心是为了帮朋友，在网上找了个用户脚本发现用不了，追到他qq群发现软件要收费。然后别的渠道是50一学期的课，就好奇这么点玩意怎么好意思收费！
于是就花了一个晚上，大概是九点钟抓包，九点半摆烂进群求软件，发现收费开始认真研究。凌晨一点代码就写完了。
不得不说，chatGPT极大地帮助了我。根据我的描述出框架，根据每一个环节的请求和返回的响应完善每个函数代码。
大概逻辑就是登录拿到key，获取课程列表拿到课程code，获得课程视频的code，然后发送保存视频播放进度的请求。循环！循环！
代码简陋，能用就行。没有tryexcept，没有加速，没有多线程，就图一个省事和安全
"""

import secrets
import time

import requests
requests.packages.urllib3.disable_warnings()


# # 登录请求
# def login(username, password):
#     login_data = {
#         "card": username,
#         "password": password,
#         "IsOauth": 0,
#         "IsEncryptPasword": 1,  # 这里开发人员还拼错了
#         "Specialty_ID": 0,
#         "notVerifyPhone": True,
#         "CardNumber": username,
#         "Password": password
#     }
#     headers = {
#         "Content-Type": "application/json; charset=utf-8",
#         "Accept": "*/*",
#         "Referer": "https://jjxy.web2.superchutou.com/",
#         "Origin": "https://jjxy.web2.superchutou.com"
#     }
#     cookies={"Cookie": "sessionId=" + session_id}
#     login_response = requests.post(
#         "https://jjxy.web2.superchutou.com/service/eduSuper/Student/BindStudentLoginByCardNumber", json=login_data ,proxies=proxies,
#         headers=headers,cookies=cookies)
#     response_data = login_response.json()
#     if response_data["ResponseCode"] == 0:
#         stu_id = response_data["Data"]["StuID"]
#         return stu_id
#     else:
#         return None


# 获取学生详细信息
def get_student_details(stu_id):
    cookies = {
        "Cookie": f"UserKey={stu_id}; sessionId=" + session_id
    }
    student_details_response = requests.get(
        "https://jjxy.web2.superchutou.com:443/service/eduSuper/StudentinfoDetail/GetStudentDetailRegisterSet",
        cookies=cookies)
    student_details_data = student_details_response.json()
    if student_details_data["ResponseCode"] == 0:
        student_info = student_details_data["Data"][0]
        print(f"Name: {student_info['Name']}")
        print(f"School_Name: {student_info['School_Name']}")
        print(f"Specialty_Name: {student_info['Specialty_Name']}")
        print()
        return student_info['StuDetail_ID']
    else:
        print("无法获取学生详细信息")


# 获取所有课程
def get_courses(cookie, StuDetail_ID):
    cookies = {
        "Cookie": f"UserKey={cookie}; sessionId=" + session_id
    }
    courses_response = requests.get(
        "https://jjxy.web2.superchutou.com/service/eduSuper/Specialty/GetStuSpecialtyCurriculumList?StuDetail_ID=" + StuDetail_ID + "&IsStudyYear=1&StuID=" + stu_id + "",
        cookies=cookies)
    courses_data = courses_response.json()
    if not courses_data.get("SuccessResponse"):
        raise Exception("操作失败")

    course_list = courses_data["Data"]["list"]
    courses = []
    for course in course_list:
        course_id = course["Course_ID"]
        curriculum_id = course["Curriculum_ID"]
        description = course["Description"]
        print(repr(description))
        courses.append({"Course_ID": course_id, "Curriculum_ID": curriculum_id, "Description": description})
    return courses


# 获取课程视频列表
def get_course_videos(cookie, course_id, curriculum_id):
    import requests

    cookies = {
        "Cookie": f"UserKey={cookie}; sessionId=" + session_id
    }

    course_videos_response = requests.get(
        f"https://jjxy.web2.superchutou.com/service/eduSuper/Question/GetCourse_ChaptersNodeList?Valid=1&Course_ID={course_id}&Curriculum_ID={curriculum_id}",
        cookies=cookies)

    course_videos_data = course_videos_response.json()

    if course_videos_data["ResponseCode"] == 200:
        videos = course_videos_data["Data"]
        video_list = []

        def extract_videos(videos):
            for video in videos:
                child_videos = video.get("ChildNodeList")
                if child_videos == "null":
                    duration = video["Duration"]
                    total_second = video["TotalSecond"]
                    video_id = video["ID"]
                    name = video["Name"]
                    video_list.append({"Duration": duration, "TotalSecond": total_second, "ID": video_id, "Name": name})
                else:
                    for child_video in child_videos:
                        duration = child_video["Duration"]
                        total_second = child_video["TotalSecond"]
                        video_id = child_video["ID"]
                        name = child_video["Name"]
                        video_list.append(
                            {"Duration": duration, "TotalSecond": total_second, "ID": video_id, "Name": name})

        extract_videos(videos)
        return video_list
    else:
        print("无法获取课程视频列表")
        return []


# 学习视频
def learn_video(cookie, course_chapters_id, look_time):

    url = "https://jjxy.web2.superchutou.com/service/datastore/WebCourse/SaveCourse_Look"
    headers = {
        "Accept": "*/*",
        "Accept-Language": "zh-CN,zh;q=0.9",
        "Access-Control-Allow-Origin": "*",
        "Cache-Control": "no-cache",
        "Connection": "keep-alive",
        "Content-Type": "application/json; charset=utf-8",
        "DNT": "1",
        "Origin": "https://jjxy.web2.superchutou.com",
        "Pragma": "no-cache",
        "Referer": "https://jjxy.web2.superchutou.com/",
        "User-Agent": "Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/92.0.4515.131 Safari/537.36 Edg/92.0.902.73",
        "sec-gpc": "1"
    }
    cookies={"Cookie": f"UserKey={cookie}; sessionId=" + session_id}
    payload = {
        "CourseChapters_ID": course_chapters_id,
        "LookType": 0,
        "LookTime": look_time,
        "IP": "IP无法获取"
    }
    response = requests.post(url, headers=headers, json=payload, verify=False, cookies=cookies)
    return response





# 输入用户名和密码
# username = input("请输入用户名：")
# password = input("请输入密码：")
print("页面登录成功后，可以直接去cookies里面找sessionId和UserKey两个参数")
session_id = str(input("请输入sessionId："))
stu_id=(input("请输入UserKey："))

proxies = {'http': 'http://127.0.0.1:8081', 'https': 'http://127.0.0.1:8081'}

# 每隔几秒保存一次60s的观看速度
# 这个地方越小，速度越快，但是不建议改
timetime = float(input("请输入刷课速度（比如输入 5 表示 每五秒保存一次60s的视频观看进度）  最好是60s，其他时间会失效："))


if stu_id:
    print("登录成功！")
    # 打印学生信息
    StuDetail_ID = get_student_details(stu_id)
    # 获取所有课程
    courses = get_courses(stu_id, StuDetail_ID)
    # 遍历课程并学习视频
    for course in courses:
        description = course["Description"]
        course_id = course["Course_ID"]
        curriculum_id = course["Curriculum_ID"]
        print(f"现在刷 {description} {course_id} {curriculum_id}")
        # 获取课程视频列表
        course_videos = get_course_videos(stu_id, course_id, curriculum_id)
        for video in course_videos:
            video_code = video["ID"]
            total_duration = int(video["TotalSecond"])
            duration = int(video["Duration"])
            name = video["Name"]
            while total_duration < duration + 100:
                # 学习视频
                try:
                    learn_response = learn_video(stu_id, video_code, 60)  # 学习60秒钟，最好别改动这个
                    print(
                        f"{description}  视频 {name} {video_code} 还剩 {duration + 100 - total_duration} s ，请耐心等待,慢点好！")
                    time.sleep(timetime)
                    total_duration += 60  # 假设每次学习60秒钟
                except:
                    time.sleep(61)
                    learn_response = learn_video(stu_id, video_code, 60)  # 学习60秒钟，最好别改动这个
                    print(
                        f"{description}  视频 {name} {video_code} 还剩 {duration + 100 - total_duration} s ，请耐心等待,慢点好！")
                    time.sleep(timetime)
                    total_duration += 60  # 假设每次学习60秒钟
            print(f"{description}  视频 {name} {video_code} 完成学习\n")
        print(f"课程 {description} {course_id} 的所有视频已完成学习")
else:
    print("登录失败！请检查用户名和密码。")
