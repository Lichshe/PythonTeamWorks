# -*- coding:utf-8 -*-
#coding=utf-8
import urllib
import urllib2
import re
import time
import os
import string
class ScanQiusbk:
        x=1
        Index = 1
        user_agent = 'Mozilla/4.0 (compatible; MSIE 5.5; Windows NT)'
        headers = { 'User-Agent' : user_agent }
        news =[]
        FunMax=[]
        FunMaxID=1
        FunMaxCount=1
        enable = False
        Dir = os.path.abspath('')
        nowtime = time.strftime("%H-%M-%S")
        style='o'
        os.makedirs(Dir+'/'+str(nowtime)+'/')
        Dir1=Dir+'/'+str(nowtime)+'/'
        fout1=open(Dir1+'result.txt','w')
        def getHtml(self,Index):
            try:
                url = 'http://www.qiushibaike.com/8hr/page/' + str(self.Index)+'/?s=4844584'
                request = urllib2.Request(url,headers = self.headers)
                response = urllib2.urlopen(request)
                pageContent = response.read().decode('utf-8')
                return pageContent
            except(urllib2.URLError, e):
                if hasattr(e,"reason"):
                    print(u"连接糗事百科失败,错误原因",e.reason)
                elif hasattr(e,"code"):
                    print(u"连接糗事百科失败,错误代码",e.code)
        def getPageinfo(self,Indexs,style):
            pageinfo = self.getHtml(Indexs)
            if not pageinfo:
                print("页面加载失败....")
                return None
            #第一个是发布者 第二个是内容 第三个是可能会出现的图片 第四个是好笑数 第五个是评论数 第六个是赞的个数
            #re.S 标志代表在匹配时为点任意匹配模式，点 . 也可以代表换行符
            pattern = re.compile('<div.*?author.*?<h2>(.*?)</h2>.*?content">(.*?)<!--.*?</div>(.*?)<div class="stats".*?number">(.*?)</i>.*?number">(.*?)</i>.*?hidden">(.*?)</span>',re.S)
            infos = re.findall(pattern,pageinfo)
            pagenews= []
            if (style=='O'):
                for info in infos:
                    haveImg = re.search("img",info[3])
                    if not haveImg:
                        replace = re.compile('<br/>')
                        realtext = re.sub(replace,"\n",info[1])
                        #info[0]是发布者,realtext(要去掉空格符)是内容,info[3]是好笑数,info[4]是评论数，info[5]是赞的个数
                        pagenews.append([info[0].strip(),realtext.strip(),info[3].strip(),info[4].strip(),info[5].strip()])                            
                return pagenews
            else:
                for info in infos:
                    #info[2]中可能有图片也可能没有，如果没有的话 因为包含换行符 所以还是得搜索img是否存在
                    replace = re.compile('<br/>')
                    realtext = re.sub(replace,"\n",info[1])
                    #info[0]是发布者,realtext(要去掉空格符)是内容,info[3]是好笑数,info[4]是评论数，info[5]是赞的个数
                    if(string.atoi(info[3].strip(),base=10)>self.FunMaxCount):
                            self.FunMaxID=self.x
                            FunMax=[]
                            FunMax.append([info[0].strip(),realtext.strip(),info[3].strip(),info[4].strip(),info[5].strip()])
                    a=info[0].encode("gbk")
                    b=info[3].encode("gbk")
                    c=info[4].encode("gbk")
                    d=info[5].encode("gbk")
                    e=realtext.encode('gbk','ignore')
                    self.fout1.write('NO.'+str(self.x).encode("gbk")+'\t'+'\t'+'Name:'+a+'\t'+'Laugh:'+b+'\t'+'commend:'+c+'\t'+'Praise:'+d+'\n'+e+'\n')
                    haveImg = re.search("img",info[2])
                    #如果不存在图片减免
                    if haveImg:
                        head=info[2].find('src')
                        tail=info[2].find('.jpg')
                        name=str(self.x)+'.jpg'
                        imgsource=info[2][head+5:tail+4]
                        urllib.urlretrieve(imgsource,self.Dir1+str(self.x)+'.jpg')
                    self.x+=1
                print(u"第%d页，当前页最好笑的糗事百科是：No:%s\t发布人:%s\t好笑:%s\t评论:%s\t赞:%s\n%s" %(self.Index,self.FunMaxID,FunMax[0][0],FunMax[0][2],FunMax[0][3],FunMax[0][4],FunMax[0][1]))
                    
        def loadPage(self):
            if (self.enable == True):
                if (len(self.news)==0):
                    pagenews = self.getPageinfo(self.Index,self.style)
                    if pagenews:
                        self.news = pagenews
                        self.Index += 1
        def saveWhole(self):
            if (self.enable==True):
                self.getPageinfo(self.Index,self.style) 
        def getOneNews(self,pagenews,page):
            for info in pagenews:
                input = raw_input()
                self.loadPage()
                del self.news[0]
                if (input == "Q"):
                    self.enable = False
                    return
                print(u"第%d页\t发布人:%s\t好笑:%s\t评论:%s\t赞:%s\n%s" %(page,info[0],info[2],info[3],info[4],info[1]))
        
        def start(self,raw_style):
            self.enable = True
            self.style=raw_style
            if (self.style=='O'):
                print(u"正在读取糗事百科,按回车查看新段子，Q退出")
                self.loadPage()
                while self.enable:
                    if len(self.news)>0:
                        pagenews = self.news
                        self.getOneNews(pagenews,self.Index-1)
                    else:
                        self.loadPage()
                exit()
            else:
                while self.enable:
                    print(u"正在保存糗事百科,按回车保存下一页，Q退出")
                    input = raw_input()
                    if (input == "Q"):
                        self.enable = False
                    else:
                        self.saveWhole()
                        self.Index+=1
                exit()
spider = ScanQiusbk()
print(u"请选择输出方式：单步输出请按O,一次性保存请按T")
style=raw_input()
if(style=='O' or style=='T'):
    spider.start(style)
else:
    exit()
