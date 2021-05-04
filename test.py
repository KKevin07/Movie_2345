file = open("./First_html_Final.html", "rb")  # read(bytes)方式打开html文件
html = file.read().decode("utf-8")
print(html)