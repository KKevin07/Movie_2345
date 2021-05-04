#  -*- coding = utf-8  -*-
import re       #re库，设定正则表达式，进行文字匹配
import urllib   #制定URL，获取网页数据，获得html文档
import urllib.request  #对服务器发送请求
import sys      #系统库
import xlwt     #进行excel操作，存到Excel表格
from bs4 import BeautifulSoup    #网页解析，对html文档进行parser解析，获取数据
import sqlite3  #进行SQLite数据库操作,存到数据库

def main():
    baseurl="https://dianying.2345.com/list/-------"

    #1.爬取网页
    datalist=getData(baseurl)

    ##创建数据库
    dbpath = "Movie_2345_Final_PRO_Lasttime.db"
    print('开始输入到数据库...')
    ##输入数据
    saveDataToDB(datalist,dbpath)



#全局变量


#_______________________________________________
find_next_urllink= re.compile(r'<a class="aPlayBtn" data-ajax83=".*?" href="(.*?)" target="_blank" title=".*?"><i></i></a>')
#<h1>汪汪队立大功之超能救援</h1>
find_title = re.compile(r'<h1>(.*?)</h1>')
#<em class="emScore">8.9分</em>
find_score = re.compile(r'<em class="emScore">(.*?)分</em>')
#<a data-ajax83="ys_dy_2015_detail_zhuy_1" href="//www.baidu.com/s?word=灰灰&amp;tn=25017023_3_pg" rel="nofollow" target="_blank" title="灰灰">灰灰</a>
#<a data-ajax83="ys_dy_2015_detail_zhuy_\d" href=".*?" target="_blank" title=".*?">(.*?)</a>
find_actor = re.compile(r'<a data-ajax83="ys_dy_2015_detail_zhuy.*?" href=".*?" target="_blank" title=".*?">(.*?)</a>')
#<a data-ajax83="ys_dy_2015_detail_daoy_1" href="//www.baidu.com/s?word=安德鲁·斯特里梅迪斯&amp;tn=25017023_3_pg" rel="nofollow" target="_blank" title="安德鲁·斯特里梅迪斯">安德鲁·斯特里梅迪斯</a>
#<a data-ajax83="ys_dy_2015_detail_daoy_\d" href=".*?" rel="nofollow" target="_blank" title=".*?">(.*?)</a>
find_director = re.compile(r'<a data-ajax83="ys_dy_2015_detail_daoy.*?" href=".*?" rel="nofollow" target="_blank" title=".*?">(.*?)</a>')
#<a data-ajax83="ys_dy_2015_detail_leix_1" href="/list/lizhi------.html" target="_blank" title="励志电影">励志</a>
#<a data-ajax83="ys_dy_2015_detail_leix_\d" href=".*?" target="_blank" title=".*?">(.*?)</a>
find_movietype = re.compile(r'<a data-ajax83="ys_dy_2015_detail_leix_.*?" href=".*?" target="_blank" title=".*?">(.*?)</a>')
#函数1.爬取网页 -> 解析网页 -> 提取数据data（正则表达式校验）
def getData(baseurl):
    datalist=[]
    count = 0
    #调用获取页面信息的函数10次
    for i in range(0,100):  #(0,100)左闭右开的特性，从第0项（第一页）开始获取电影，
                          # 100个页面，共计3500部
        url = baseurl  +str(i*1)+".html"  #一个网页35部电影

        tip='开始爬取第'+str(i+1)+'个页面，累计'+str((i+1)*35)+'部电影'
        print(tip)

        # 步骤1. 保存获取到的网页源码
        html = askURL(url)

        # 步骤2. 逐一解析数据（使用bs） #每一次html获取信息都进行解析数据
        soup = BeautifulSoup(html,"html.parser")   #形成soup树形结构对象,可以进行对文档的提取

        # 步骤3. 提取数据data （用for循环，对每一个item）
        for qy in soup.find_all('div',class_="pic") :     #查找符合要求的字符串(div标签中含有class（属性值）为item，及其子孙信息)，返回列表
            data = []
            qy = str(qy)
            #print(qy)
            #对第一个页面的抓取
            count=count+1
            print('目前处于第'+str(count)+'部电影页面')
            # data 0 : next_link
            findlink = re.findall(find_next_urllink, qy)[0]
            next_link="https:"+findlink
            data.append(next_link)


            #加载第二页
            Nexthtml =ask_Next_URL(next_link)
            #print(Nexthtml)
            Nextsoup = BeautifulSoup(Nexthtml, "html.parser")
            Next_bs_qy = Nextsoup.find_all('div',class_="txtIntroCon")
            Next_qy=str(Next_bs_qy)
            #print(Next_bs_qy)

            #开始抓第二页的信息

            try:
                # data 1 : title
                title = re.findall(find_title,Next_qy)[0]
                #print(title)
                data.append(title)
            except:
                title = '暂无数据'
                # print(title)
                data.append(title)

            try:
                # data 2 : score
                score = re.findall(find_score,Next_qy)[0]
                # print(score)
                data.append(score)
            except:
                score = '0'
                # print(score)
                data.append(score)

            # data 3 : real_actor
            try:
                actor = re.findall(find_actor,Next_qy)
                real_actor=''
                for i in range(len(actor)):
                    real_actor=real_actor+actor[i]
                #print(real_actor)
                data.append(real_actor)
            except:
                real_actor = '暂无数据'
                # print(real_actor)
                data.append(real_actor)

            # data 4 : director
            try:
             director = re.findall(find_director,Next_qy)[0]
             #print(director)
             data.append(director)
            except:
                director = '暂无数据'
                # print(director)
                data.append(director)

            # data 5 : real_type
            try:
                movie_type = re.findall(find_movietype,Next_qy)
                real_type=''
                for i in range(len(movie_type)):
                    real_type=real_type+movie_type[i]
                #print(real_type)
                data.append(real_type)
            except:
                real_type ='暂无数据'
                # print(real_type)
                data.append(real_type)





            datalist.append(data) #顺序：  next_link, title, score, real_actor, director, real_type



    #print(datalist)  #验证数据校验的结果是否成功

    return datalist

# 函数2. 得到指定的一个URL的网页内容，返回html
#对豆瓣电影的爬取工作运用在250部电影，需要10个页面，每一页含有25部电影，
def askURL(url):
    headers = {
        "User-Agent":"Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/89.0.4389.114 Safari/537.36 Edg/89.0.774.68"
    }                     #head内信息多则用列表方式
                           #head["User-Agent"] #head内信息不多时使用键值对方式
                           #User-Agent表示本机的类型和浏览器信息（本质上是告知目标网页服务器，本机可以接受什么类别的文件内容）

    request=urllib.request.Request(url,headers=headers)
    #urllib.request进行访问，向服务器发送请求，括号内为封装的信息（网址、头部），用request对象接收
    html = ""  #用于存储服务器返回的信息
    try:       #尝试接收服务器返回信息
        response = urllib.request.urlopen(request)  #服务器返回的信息
        html = response.read().decode("gbk")
        #print(html)
    except urllib.error.URLError as e:  # 如果请求发生错误，则返回code码和reason原因
        if hasattr(e, "code"):
            print(e.code)
        if hasattr(e, "reason"):
            print(e.reason)



    return html
def ask_Next_URL(url):
    headers = {
        "User-Agent":"Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/89.0.4389.114 Safari/537.36 Edg/89.0.774.68"
    }                     #head内信息多则用列表方式
                           #head["User-Agent"] #head内信息不多时使用键值对方式
                           #User-Agent表示本机的类型和浏览器信息（本质上是告知目标网页服务器，本机可以接受什么类别的文件内容）

    request=urllib.request.Request(url,headers=headers)
    #urllib.request进行访问，向服务器发送请求，括号内为封装的信息（网址、头部），用request对象接收
    html = ""  #用于存储服务器返回的信息
    try:       #尝试接收服务器返回信息
        response = urllib.request.urlopen(request)  #服务器返回的信息
        html = response.read().decode("gbk")
        #print(html)
    except :  # 如果请求发生错误，则返回code码和reason原因
        file = open("./Next_html_Final.html", "rb")  # read(bytes)方式打开html文件
        html = file.read().decode("utf-8")



    return html
#(sqlite数据库方式)
def saveDataToDB(datalist,dbpath):
    init_db(dbpath)
    conn = sqlite3.connect(dbpath)
    cur = conn.cursor()     #获取游标(可操作的对象)

    for data in datalist:
        for index in range(len(data)):
             if index == 2:
                continue

             data[index] = '"'+str(data[index])+'"'
        sql = '''
                insert into Movie_2345(
                next_link,title,score,real_actor,director,real_type)
                values(%s)            
            '''%','.join(data)          #‘%’填补sql语句
        #print(sql)
        cur.execute(sql)
        conn.commit()


    cur.close()
    conn.close()




def init_db(dbpath):

    #创建数据表  #顺序：next_link,title,score,real_actor,director,real_type
    sql = '''
        create table if not exists Movie_2345
        (
        id integer primary key autoincrement,
        next_link text,
        title text,
        score numeric,
        real_actor text,
        director text,
        real_type text
                 
        )
    
    
    '''
    conn = sqlite3.connect(dbpath)
    cursor = conn.cursor()
    cursor.execute(sql)
    conn.commit()
    conn.close()








#主程序，执行main()
if __name__ == "__main__":   #当程序执行时
#调用函数
    main()
    #init_db("test_movie.db")  #测试用
    print("电影数据爬取工作已完毕")