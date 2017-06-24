#coding=utf-8
'''
Created on 2017年4月14日
主要调度程序，

'''
from mainCoding._Cleanner import getDom
from urllib import request
from urllib.request import urlopen
from mainCoding._Spider import _description
from mainCoding._outputSpider import output
from mainCoding._outputStatistics import outputStatus
import chardet


class main:
    def __init__(self,pageurl,i):
        self.pageurl =pageurl
        self.i = i
        req = request.Request(self.pageurl)
        req.add_header('User-Agent','Mozilla/5.0 (Windows NT 6.3; WOW64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/39.0.2171.95 Safari/537.36')
         
        self.resp = urlopen(req).read()
        #用chardet进行内容分析
        chardit1 = chardet.detect(self.resp)
        #得到网页编码格式
        self.charset = chardit1['encoding']
        print(self.charset)
        
        if self.charset == 'GB2312':
            self.resp = urlopen(req).read().decode('gbk')
        elif self.charset == 'Windows-1254':
            self.resp = urlopen(req).read().decode('utf-8')
        else:
            self.resp = urlopen(req).read().decode(self.charset)
        #定义回帖正文数组
        self.replayContentList = []
        #定义主体内容文本数组
        self.mainContent = []
        
        pass
    
    #清除噪音。得到Dom树结构
    def _cleaner(self):
        #调用方法getDom，为了获得网页内容
        self.body = getDom(self.resp,self.charset)

        pass
    
    #爬取内容
    def _response(self):
        print("执行")
        Object_title = _description(self.resp,self.charset,self.body)
        
        #获取帖子标题
        title = Object_title.getTitle()
        print("【标题】："+str(title))
        
        #获取主体部分
        self.mainContent = Object_title.getMainContent()
        print("【主体】："+str(self.mainContent))
        
        #获取帖子发表时间
        self.timeList = Object_title.getTime()
        print("【时间集合】："+str(self.timeList))
        
        #获取主贴正文
        self.myContent,BeginTimeIndex = Object_title.getMyContent()
        print("【正文】："+str(self.myContent))
        
        #获取回复贴正文
        self.replayContentList = Object_title.getReplayList()
        print("【回帖集合】："+str(self.replayContentList))
        
        #调用_output中的output函数，将爬取的内容存储到文件中
        Object_output = output(self.pageurl,self.i,title,self.mainContent,self.timeList,self.myContent,BeginTimeIndex,self.replayContentList)
        Object_output.output()
# 
#         #调用——outputStatus中的outputStatus函数，将需要分析统计的数据传入函数，进行文件输出。
#         #传入参数。主体部分mainContent，时间在主体部分的下标集合timeList
#         Object_outputStatus = outputStatus(self.myContent,self.i)
#         Object_outputStatus.statusFormOutput()
        
        pass