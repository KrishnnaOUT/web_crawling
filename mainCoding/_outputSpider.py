#coding=utf-8
'''
Created on 2017年4月17日

主要输出爬取内容程序
'''

class output:
    
    #url:网址
    #title:帖子标题
    #mainContent:以标题开头的主体文本数组
    #timeList:时间
    #myContent：主贴正文
    #BeginTimeIndex:在timeList中属于主贴的时间下标
    #replayContentList：回帖正文
    def __init__(self,url,i,title,mainContent,timeList,myContent,BeginTimeIndex,replysContentList):
        self.url = url
        self.i = i
        self.title = title
        self.mainContent = mainContent
        self.timeList = timeList
        self.myContent = myContent
        self.BeginTimeIndex = BeginTimeIndex
        self.replysContentList = replysContentList
        pass
    
    #输出爬取内容
    def output(self):
        
        #创建一个字典变量
        output = {}
        #创建一个回帖信息输出数组
        replysOutputList = []
        
        #遍历回帖集合
        i = self.BeginTimeIndex+1#定义i,用于遍历时间集合。
        if self.replysContentList is not None:
            for item in self.replysContentList:
                #定义一个中转字典。用于在数组中逐个取出回帖并格式化
                replyDict = {"content":item,
                             "title":self.title,
                             "publish_date":self.timeList[i]
                            }
                #将该中转字典加入到总回帖输出数组中。
                replysOutputList.append(replyDict)
                i = i+1
                pass
    
        #判断时间集合是否为空
        if self.timeList is None or self.timeList == []:
            publish_date = ' '
        else:
            publish_date = self.timeList[self.BeginTimeIndex]
    
        #定义输出内容变量
        output = {"post":
                    {"content":"".join(self.myContent),
                     "title":self.title,
                     "publish_date":publish_date
                    },
                  "replys":replysOutputList
                 }
        
        #创建一个新的txt文件(如果原有同名文件会被覆盖)
        fname = self.url
        fname = self.url.split('/')[-1]
        fname = fname.split('\\')[-1]
        fname = fname.split('/')[-1]
        fname = fname.split('?')[-1]
        fname = fname.split('|')[-1]
        fname = fname.split('.')[-1]
            
          
        #生成随机码
        random = int(self.i*20170423/100)
        
        fname = str(self.i)+'-'+fname+str(random)+'.txt' 
        four = open(fname,'w',encoding='utf-8')
        
        
        #写入文件
        four.write(self.url+'\n')
        four.write(str(output))
        
        #关闭文件
        four.close()
        
        pass
    