# 出头科技九江学院刷课脚本

<u>**注意！此脚本仅用于技术交流，不得欺骗刷课，不得构造攻击！**</u>
<u>**更不得卖钱！我看不起你！</u>**

官网给用户名密码登录界面加了个验证框，暂时不知道咋写代码解决，但是可以稍微改动一下代码就能用

1. 浏览器登录界面，登录之前打开开发者工具的网络记录

2. 成功登陆后，在网络记录中搜索`BindStudentLoginByCardNumber`，查看响应，注意

    `"Data"`: {`
           "StuID": "2969A81B8F??????????98680B5919E",`

3. 把原来代码中的`stu_id = login(username, password)`改成`stu_id = "2969A8??????????680B5919E"`

4. 把原来代码中的`session_id = secrets.token_hex(16)`改成`BindStudentLoginByCardNumber`请求标头位置的cookies里的`sessionId=c4f74727152aba2343g24h3508d2319` 即`session_id = "c4f74727152a234bjh335a358e08d2319"`

5. 运行代码，用户名随便输，密码随便输，其他正常

~~打包好的可执行程序下载：[下载界面](https://github.com/yjn140/superchutou-jjxy/releases)~~

使用方法

1. 安装python环境

2. 使用pip命令安装requests库  `pip install requests`

3. 运行这个脚本  `python chutou.py` 或者是 `python3 chutou.py`

4. 输入用户名 回车 输入密码 回车

   ------

   ![](https://yjn140.site/post-images/1685548987305.jpg)
   ![](https://yjn140.site/post-images/1685549382354.png)

   写这个代码的初心是为了帮朋友，在网上找了个用户脚本发现用不了，追到他qq群发现软件要收费。然后别的渠道是50一学期的课，就好奇这么点玩意怎么好意思收费！
   于是就花了一个晚上，大概是九点钟抓包，九点半摆烂进群求软件，发现收费开始认真研究。凌晨一点代码就写完了。
   不得不说，chatGPT极大地帮助了我。根据我的描述出框架，根据每一个环节的请求和返回的响应完善每个函数代码。
   大概逻辑就是登录拿到key，获取课程列表拿到课程code，获得课程视频的code，然后发送保存视频播放进度的请求。循环！循环！
   代码简陋，能用就行。没有trycatch，没有加速，没有多线程，就图一个省事和安全
