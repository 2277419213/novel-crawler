# 国内网站小说爬虫

### 原理先行

作为一个资深的小说爱好者，国内很多小说网站如出一辙，什么 🖊\*阁啊等等，大都是 get 请求返回 html 内容，而且会有标志性的`<dl><dd>`等标签。  
所以大概的原理，就是先 get 请求这个网站，然后对获取的内容进行清洗，写进文本里面，变成一个 txt，导入手机，方便看小说。

### 实践篇

之前踩过一个坑，一开始我看了几页小说，大概小说的内容网站是`https://www.xxx.com/小说编号/章节编号.html`，一开始看前几章，我发现章节编号是连续的，
于是我一开始想的就是记住起始章节编号，然后在循环的时候章节编号自增就行，后面发现`草率了`，可能看个 100 章之后，章节列表会出现断层现象，这个具体为啥
还真不知道，按理说小说编号固定，可以算是一个数据表，那里面的章节编号不就是一个自增 id 就完了嘛？有懂王可以科普一下！  
所以这里要先获取小说的目录列表，并把目录列表洗成一个数组方便我们后期查找！`getList.py`文件：

#### 定义一个请求书签的方法

```
# 请求书签地址
def req():
    url = "https://www.24kwx.com/book/4/4020/"
    strHtml = requests.get(url)
    return strHtml.text
```

#### 将获取到的内容提取出（id:唯一值/或第 X 章小说）(name:小说的章节名称)（key:小说的章节 id）

```
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
```

`注意一下我：`如果你从别的语言转 py，第一次写`object`对象可能会比较`懵`，没错因为他的`object`是一个`class`，这里我创建的对象就是`{id,key,name}`但是你写入 txt 的时候还是要`getString`，所以后面想想我直接写个`{id:xxx,name:xxx,key:xxx}`的字符串不就完了，还弄啥`class`,后面还是想想给兄弟盟留点看点，就留着了

#### 最后写入 txt 文件

```
# 写入到文本
def writeList(list):
    f = open("xsList.txt",'w',encoding='utf-8')
    # 这里不能写list，要先转字符串 TypeError: write() argument must be str, not list
    f.write('\n'.join(list))
    print('写入成功')

# 大概写完的txt是这样的
id:3798160,name:第1章 孙子，我是你爷爷,key:1
id:3798161,name:第2章 孙子，等等我！,key:2
id:3798162,name:第3章 天上掉下个亲爷爷,key:3
id:3798163,name:第4章 超级大客户,key:4
id:3798164,name:第5章 一张退婚证明,key:5
```

`ok ! Last one `  
这里已经写好了小说的目录，那我们就要读取小说的内容，同理

#### 先写个请求

```
# 请求内容地址
def req(id):
    url = "https://www.24kwx.com/book/4/4020/"+id+".html"
    strHtml = requests.get(url)
    return strHtml.text
```

#### 读取我们刚刚保存的目录

```
def getList():
    f = open("xsList.txt",'r', encoding='utf-8')
    # 这里按行读取,读取完后line是个数组
    line = f.readlines()
    f.close()
    return line
```

#### 定义好一个清洗数据的规则

```
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
```

#### 再写入文件

```
def writeTxt(txt):
    if txt :
        f = open("nr.txt",'a',encoding="utf-8")
        f.write(txt+'\n')
```

#### 最后当然是串联起来啦

```
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
```

### 写在最后

本 github 只是作为技术交流以及学术探讨，文中所涉及到的网站均为`某度搜索`出来的网站，不代表本人任何立场，如有侵权，请提`Issues`告诉我！
