import requests
import re

# 请求书签地址
def req():
    url = "https://www.24kwx.com/book/4/4020/"
    strHtml = requests.get(url)
    return strHtml.text

# 定义一个章节对象
class Xs(object):
    def __init__(self,id,key,name):
        self._id = id
        self._key = key
        self._name = name

    @property
    def id(self):
        self._id
    @property
    def key(self):
        self._key
    @property
    def name(self):
        self._name

    def getString(self):
        return 'id:%s,name:%s,key:%s' %(self._id,self._name,self._key)

# 转换成书列表
def tranceList():
    key = 0
    name = ""
    xsList = []
    idrule = r'/4020/(.+?).html'
    keyrule = r'第(.+?)章'
    html = req()
    html = re.split("</dt>",html)[2]
    html = re.split("</dl>",html)[0]
    htmlList = re.split("</dd>",html)
    for i in htmlList:
        i = i.strip()
        if(i):
            # 获取id
            id = re.findall(idrule,i)[0]
            lsKeyList = re.findall(keyrule,i)
            # 如果有章节
            if len(lsKeyList) > 0 :
                key = int(lsKeyList[0])
                lsname = re.findall(r'章(.+?)</a>',i)
            else :
                key = key + 1
            # 获取名字
            # lsname = re.findall(r'.html">(.+?)</a>',i)[0]
            # name = re.sub('，',' ', lsname, flags=re.IGNORECASE)
            name = re.findall(r'.html">(.+?)</a>',i)[0]
            xsobj = Xs(id,key,name)
            xsList.append(xsobj.getString())
    writeList(xsList)

# 写入到文本
def writeList(list):
    f = open("xsList.txt",'w',encoding='utf-8')
    # 这里不能写list，要先转字符串 TypeError: write() argument must be str, not list
    f.write('\n'.join(list))
    print('写入成功')


def main():
    tranceList()

if __name__ == '__main__':
    main() 