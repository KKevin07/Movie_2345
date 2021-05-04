import urllib.request

#获取一个get请求

# response=urllib.request.urlopen("http://www.baidu.com")
# print(response.read().decode('utf-8'))  #对获取到的网页源码进行utf-8解码

#获取一个post请求(httpbin.org网站,测试用途的服务器，可用于测试http\cookie等等)
#post请求用于模拟用户真实登录时使用

# import  urllib.parse #解析器
# #用post形式进行封装，以data传递参数，data用字节文件形式封装进去
# data=bytes(urllib.parse.urlencode({"hello":"world"}),encoding="utf-8")
# response=urllib.request.urlopen("http://httpbin.org/post",data=data)
# print(response.read().decode("utf-8"))
# #utf-8解码，理清格式,适用于获取的信息不适合中文格式阅读或者格式混乱

#httpbin服务器下的get请求

# try:  #超时处理，网速不好而超时，或者服务器拒绝爬虫访问而超时
#     response=urllib.request.urlopen("http://httpbin.org/get",timeout=5)
#     print(response.read().decode("utf-8"))
# except urllib.error.URLError as e:
#     print("time out!")


# response=urllib.request.urlopen("http://www.baidu.com",timeout=5)
# #print(response.status)
# #print(response.getheaders())
# print(response.getheader("Server")) #说明response可以帮助我们获取请求过程中的所有的相关信息



#将爬虫伪装为正常的浏览器。即对请求对象进行封装,模拟正常浏览器请求时发送的Headers,包括模拟cookie,然后发送给目标网站
#url="https://www.douban.com"
# url="http://httpbin.org/post"
# headers={
# "User-Agent":"Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/89.0.4389.114 Safari/537.36 Edg/89.0.774.68"
# }
# data=bytes(urllib.parse.urlencode({'name':'eric'}),encoding="utf-8")
# req=urllib.request.Request(url=url,data=data,headers=headers,method="POST")   #request.Request()封装
# response=urllib.request.urlopen(req)
# print(response.read().decode("utf-8"))

#伪装完成之后，对豆瓣进行伪装后的访问请求

# url="https://dianying.2345.com/detail/210414.html"
url="https://dianying.2345.com/list/-------"+str(69*1)+".html" #  i:0-100   共3500部
headers={
"User-Agent":"Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/89.0.4389.114 Safari/537.36 Edg/89.0.774.68"
 }
req=urllib.request.Request(url=url,headers=headers)
response=urllib.request.urlopen(req)
print(response.read().decode("gbk"))


