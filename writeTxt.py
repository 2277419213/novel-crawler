import requests
import re
import time


# 请求内容地址
def req(id):
    url = "https://www.24kwx.com/book/4/4020/"+id+".html"
    strHtml = requests.get(url)
    return strHtml.text

def getList():
    f = open("xsList.txt",'r', encoding='utf-8')
    # 这里按行读取
    line = f.readlines()
    f.close()
    return line

contextRule = r'<div class="content">(.+?)<script>downByJs();</script>'
titleRule = r'<h1>(.+?)</h1>'
def getcontext(objstr):
    xsobj = re.split(",",objstr)
    id = re.split("id:",xsobj[0])[1]
    name = re.split("name:",xsobj[1])[1]
    html = req(id)
    lstitle = re.findall(titleRule,html)
    title = lstitle[0] if len(lstitle) > 0 else name
    context = re.split('<div id="content" class="showtxt">',html)[1]
    context = re.split('</div>',context)[0]
    context = re.sub('&nbsp;|\r|\n','',context)
    textList = re.split('<br />',context)
    textList.insert(0,title)
    for item in textList :
        writeTxt(item)
    print('%s--写入成功'%(title))

def writeTxt(txt):
    if txt :
        f = open("nr.txt",'a',encoding="utf-8")
        f.write(txt+'\n')

def getTxt():
    # 默认参数配置
    startNum = 1261 # 起始章节
    endNum = 1300 # 结束章节
    # 开始主程序
    f = open("nr.txt",'w',encoding='utf-8')
    f.write("")
    if endNum < startNum:
        print('结束条数必须大于开始条数')
        return
    allList = getList()
    needList = allList[startNum-1:endNum]
    for item in needList:
        getcontext(item)
        time.sleep(0.2)
    print("全部爬取完成")

    
def main():
    getTxt()

if __name__ == "__main__":
    main()