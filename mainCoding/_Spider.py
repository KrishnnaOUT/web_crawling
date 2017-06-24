#coding=utf-8
'''
Created on 2017年4月15日

主要抓取程序，内含抓取的规则及算法

'''
from bs4 import BeautifulSoup
import re
import time
from mainCoding.MyException import MyException


class _description:

    #初始化函数
    def __init__(self,html,charset,body):
        
        if charset is None:
            charset = 'utf-8'
        
        self.soup = BeautifulSoup(html,'html.parser',from_encoding=charset)
        
        self.weightList = []#定义权重集合
        #定义时间戳集合
        self.timeList = []
        #定义日期戳下标集合
        self.timeIndexList = []
        self.body = body

        pass
    
    def getMainContent(self):

        #确定最大值的唯一性。假设最大值大于2个，解决标题在正文标题中和版块导航中重复所导致的误差
        if self.weightList != []:
            if self.weightList.count(max(self.weightList))>2:

                #将第一个值下标存于变量firstMaxIndex中，并设置self.weightList中第一个最大值为零，
                self.weightList.index(max(self.weightList))
                self.weightList[self.weightList.index(max(self.weightList))] = 0
                pass
            #若最大值个数为两个
            elif self.weightList.count(max(self.weightList))>1:

                #若不唯一且第二个最大值下标比上数组长度距离小于0.5，即第二个最大值位于前半部分中，则去掉第一个，取第二个值。
                #若比值大于0.5，即在后半部分中，那么取第一个值。
                #将第一个值下标存于变量firstMaxIndex中，并设置self.weightList中第一个最大值为零，
                firstMaxIndex = self.weightList.index(max(self.weightList))
                self.weightList[self.weightList.index(max(self.weightList))] = 0
                
                #第二个最大值下标和数组长度的比值<0.5,则取第二个最大值。否则。取回第一个最大值
                if self.weightList.index(max(self.weightList))/len(self.weightList)>0.5:
                    self.weightList[firstMaxIndex] = max(self.weightList)
                    pass
                else:
                    #若第二个值其上下部分被文本包围，即设定一个阈值，其上个个文本长度大于该最大值。则取回第一个最大值
                    secondMaxIndex = self.weightList.index(max(self.weightList))
                    if len(self.body[secondMaxIndex-1])>=len(self.body[secondMaxIndex]):
                        self.weightList[firstMaxIndex] = max(self.weightList)
                        pass
                    pass
                pass
            #获得正文帖子标题下标
            self.titleIndex = self.weightList.index(max(self.weightList))
            #获得涵盖主要内容的部分(即从主贴标题开始的后续部分)并存储在mainContent数组中
            self.mainContent = self.body[self.titleIndex:]
            pass
        else:
            self.mainContent = []
            pass
        return self.mainContent
        pass
        
    #获取帖子标题
    def getTitle(self):

        #先获取指定网页的标题，即<title></title>中的值，通过该值匹配对应帖子的主题
        pagetitle = self.soup.find('title')
        
        #剔除异常标题如带有“——”的标题
        if "——" in pagetitle:
            pagetitle.replace('——','')
            
        
        #剔除关于论坛信息等噪音
        if pagetitle is not None:
            page_title = re.split('-|_|—|\|',pagetitle.text)[0]
            
            #对比title和body数组中的字符串，得到计算body数组中各字符串所占的权重，
            #权重越高，说明匹配度越高。那么是正文标题的几率越大
            #i为title循环变量
            #weight为权重变量
            #continuity为连续变量数组,,若连续匹配次数高。则额外增加权重
            #得到网页标题page_title与body中遍历值的长度差值lenDiff1，权重减少(1/len(self.body[i]))*lenDiff1
            #i为body集合的下标循环变量。j为title的字符下标循环变量,k为连续下标循环变量
            i = 0
            
            while i<len(self.body):
                
                continuity = [] 
                weight = 0
                j = 0
                k = 0
                
                continuity.append(1)
                
                while j<len(page_title):
                    
                    #若为空格则跳过
                    if page_title[j] is not ' ':
                        
                        if page_title[j] in self.body[i]:
                            
                            #每匹配对一个字，就增加1/len(self.body[i])的权重量
                            weight = weight + 1/len(self.body[i])
                            
                            #每匹配对一个字，连续变量continuity就增加1
                            continuity[k] = continuity[k]+1
                            
                            pass
                        else:
                            
                            k = k+1
                            continuity.append(1)
                            
                            pass
                        pass
                    j = j+1
                    pass
                
                #若出现标题被分割成两个文本存在的情况。在此做个判断,并拼接成完整的标题字符串
                if weight == 1 and max(continuity) == len(self.body[i])+1:
                    
                    #构造条件weight1，即当前遍历项的下一项的权重值。
                    #若为空格则跳过
                    l = 0
                    weight1 = 0
                    
                    while l<len(page_title):
                        
                        if page_title[l] is not ' ':
                         
                            if page_title[l] in self.body[i+1]:
                            
                                #每匹配对一个字，就增加1/len(self.body[i])的权重量
                                weight1 = weight1 + 1/len(self.body[i+1])
                                pass
                            pass
                        
                        l = l + 1
                        pass
                    
                    #若满足条件。即当前遍历项和下一项可以构成标题。那么就将当前遍历项拼接成标题
                    if len(page_title)-len(self.body[i] + self.body[i+1]) <= 2 and weight1 == 1:
                        
                        #拼接字符串，得到完整标题存于这个正在被遍历的值中
                        self.body[i] = self.body[i]+self.body[i+1]
                        
                        #并让他成为最大权重的项
                        weight = weight + 1000
                        pass
                    pass 
                
                #得到两者文本的长度差值lenDiff，权重减少(1/(len(self.body[i])*2))*lenDiff1
                lenDiff1 = abs(len(page_title)-len(self.body[i]))
                
                #若长度差值为0，那么增加权重1
                if lenDiff1 == 0:
                    
                    weight = weight + 1
                    
                    pass
                else:
                    
                    weight = weight - (1/(len(self.body[i])*2))*lenDiff1
                    pass
                
                weight = weight * max(continuity)
                
                #将权重变量weight添加到权重集合中
                self.weightList.append(weight)
                
                i = i+1
                pass
    
            return page_title.strip()
            pass
        
        return 'this is no title'
        pass
    
    #获取帖子发表时间
    def getTime(self):
        
        #判断self.mainContent.index(timeItem)>distance成立，则添加当前系统时间置于开头项之后#，并转入下一个循环
        re1 = re.compile(r'[^登录]*(\d{2,4}(-|/))?([0-9]{1,2})(-|/)[0-9]{1,2}.*')
        re2 = re.compile(r'^\d{1,2}:\d{2}(:\d{2})?$')
        re3 = re.compile(r'^((.{1,2}天前$)|(\d{0,2}.{1,2}分钟前$)|(\d{1,2}.{1,2}小时前$))')
        re4_1 = re.compile(r'^(发表于|发布于).*')
        re4_2_1 = re.compile(r'^(\d|\D)$')
        re4_2_2 = re.compile(r'^.天$')
        re4_3 = re.compile(r'((天前)|(小时前)|(分钟前))$')
        
        for timeItem in self.mainContent:
         
            #网站时间格式为“2016-04-15 23:55”类型的。即出现年月日的
            if re1.match(timeItem):#判断是否匹配re1规则（匹配日期）            
                
                self.judgeDistanceNextTitle2FirstTime(timeItem)
 
                break
                pass
            
            #网站时间格式为“23:55:33"类型的。即出现具体时间的
            elif re2.match(timeItem):
    
                self.judgeDistanceNextTitle2FirstTime(timeItem)
 
                break
                pass
            
            #网站时间格式为“三天前”“9小时前”或者“10分钟前”类型的。即出现年月日的
            elif re3.match(timeItem):
            
                self.judgeDistanceNextTitle2FirstTime(timeItem)
 
                break
                pass
            
            #若网站时间为块状分布，如分成三个文本，【例："发表于","3","天前"】【例："发表于","前天","05：45"】
            elif re4_1.match(timeItem):#匹配第一个字符串。
                
                if re4_2_1.match(self.mainContent[self.mainContent.index(timeItem)+1]):#匹配第二个字符串。
                    
                    if re4_3.match(self.mainContent[self.mainContent.index(timeItem)+2]):#匹配第三个字符串。
                    
                        self.judgeDistanceNextTitle2FirstTime(timeItem)
 
                        break
                        pass
                    pass
                
                elif re4_2_2.match(self.mainContent[self.mainContent.index(timeItem)+1]):#匹配第二个字符串。:
                
                    if re2.match(self.mainContent[self.mainContent.index(timeItem)+2]):#匹配第三个字符串。
                    
                        self.judgeDistanceNextTitle2FirstTime(timeItem)
 
                        break
                        pass
                    pass
                pass
            pass

        #循环遍历。匹配出现的时间项
        for timeItem in self.mainContent:
            
            #网站时间格式为“2016-04-15 23:55”类型的。即出现年月日的
            if re1.match(timeItem):#判断是否匹配re1规则（匹配日期) 
                
                #获得主体内容中日期戳所在的下标timeIndex
                timeIndex = self.mainContent.index(timeItem)
                
                #日期的下一个为具体时间。一并抓取
                if timeIndex != len(self.mainContent)-1:#判断所匹配得到的字符串文本是否为数组中最后一项
                    
                    #并让日期下标下的值置为“日期：time”，防止被重复遍历
                    self.mainContent[timeIndex] = '日期：'+ self.mainContent[timeIndex]
                    timeItem = '日期：'+timeItem
    
                    if re2.match(self.mainContent[timeIndex+1]):#判断timeItem下一项是否为re2规则（匹配具体时间)
                                                        
                        #并让具体时间下标下的值置为“时间：time”，防止被重复遍历
                        self.mainContent[timeIndex+1] = '时间：'+ self.mainContent[timeIndex+1]
                        timeItem = timeItem+' '+self.mainContent[timeIndex+1]
                        pass
                            
                    #将获得的下标放入日期戳下标集合中
                    self.timeIndexList.append(timeIndex)
                    #将日期戳放入时间数组中
                    self.timeList.append(timeItem)
                    pass
                pass
                
            #网站时间格式为“23:55:33"类型的。即出现具体时间的
            elif re2.match(timeItem):
                #获得主体内容中具体时间戳所在的下标timeIndex
                timeIndex = self.mainContent.index(timeItem)
                #并让具体时间下标下的值置为“时间：time”，防止被重复遍历
                self.mainContent[timeIndex] = '时间：'+ self.mainContent[timeIndex]
                timeItem = '时间：'+timeItem
                            
                #将获得的下标放入具体时间戳下标集合中
                self.timeIndexList.append(timeIndex)
                #将日期戳放入时间数组中
                self.timeList.append(timeItem)
                pass
                
            #网站时间格式为“三天前”“9小时前”或者“10分钟前”类型的。即出现年月日的
            elif re3.match(timeItem):
                #获得主体内容中具体时间戳所在的下标timeIndex
                timeIndex = self.mainContent.index(timeItem)
                #并让具体时间下标下的值置为“时间：time”，防止被重复遍历
                self.mainContent[timeIndex] = '时间：'+ self.mainContent[timeIndex]
                timeItem = '时间：'+timeItem
                             
                #将获得的下标放入具体时间戳下标集合中
                self.timeIndexList.append(timeIndex)
                #将日期戳放入时间数组中
                self.timeList.append(timeItem)
                pass
                
            #若网站时间为块状分布，如分成三个文本，【例："发表于","3","天前"】
            elif re4_1.match(timeItem):#匹配第一个字符串
                if re4_2_1.match(self.mainContent[self.mainContent.index(timeItem)+1]):#匹配第二个字符串
                    if re4_3.match(self.mainContent[self.mainContent.index(timeItem)+2]):#匹配第三个字符串
                        #获得主体内容中具体时间戳所在的下标timeIndex
                        timeIndex = self.mainContent.index(timeItem)
                        #并让具体时间下标下的值置为“时间：time”，防止被重复遍历
                        self.mainContent[timeIndex] = '时间：'+ self.mainContent[timeIndex]
                        timeItem = '时间：'+timeItem+self.mainContent[timeIndex+1]+self.mainContent[timeIndex+2]
                                     
                        #将获得的下标放入具体时间戳下标集合中
                        self.timeIndexList.append(timeIndex)
                        #将日期戳放入时间数组中
                        self.timeList.append(timeItem)
                        pass
                    else:
                        #改变格式（在原有值之前增加“.”）防止被重复遍历
                        self.mainContent[self.mainContent.index(timeItem)] = '.'+self.mainContent[self.mainContent.index(timeItem)]
                        pass
                        pass
                elif re4_2_2.match(self.mainContent[self.mainContent.index(timeItem)+1]):#匹配第二个字符串。:
                    if re2.match(self.mainContent[self.mainContent.index(timeItem)+2]):#匹配第三个字符串。
                        #获得主体内容中具体时间戳所在的下标timeIndex
                        timeIndex = self.mainContent.index(timeItem)
                        #并让具体时间下标下的值置为“时间：time”，防止被重复遍历
                        self.mainContent[timeIndex] = '时间：'+ self.mainContent[timeIndex]
                        timeItem = '时间：'+timeItem+self.mainContent[timeIndex+1]+self.mainContent[timeIndex+2]
                                     
                        #将获得的下标放入具体时间戳下标集合中
                        self.timeIndexList.append(timeIndex)
                        #将日期戳放入时间数组中
                        self.timeList.append(timeItem)
                        pass
                    else:
                        #改变格式（在原有值之前增加“.”）防止被重复遍历
                        self.mainContent[self.mainContent.index(timeItem)] = '.'+self.mainContent[self.mainContent.index(timeItem)]
                        pass
                        pass
                else:
                    #改变格式（在原有值之前增加“.”）防止被重复遍历
                    self.mainContent[self.mainContent.index(timeItem)] = '.'+self.mainContent[self.mainContent.index(timeItem)]
                    pass
                pass
            pass
        return self.timeList
        pass
    
    # 判断第一个时间与标题的距离是否超过阈值
    def judgeDistanceNextTitle2FirstTime(self,timeItem):
        #设定标题与时间戳距离的阈值
        distance = 45
        
        #获取当前日期
        currentDate = time.strftime('%Y-%m-%d',time.localtime(time.time()))
        #获取当前具体时间
        currentTime = time.strftime('%H:%M',time.localtime(time.time()))
       
        #若是标题与第一个时间戳距离超过阈值distance
        if self.mainContent.index(timeItem) > distance:
                    
            # 增加一个时间戳于标题后                            
            self.mainContent.insert(1, currentDate)
            self.mainContent.insert(2, currentTime)

            pass
        pass
    
    
    #获取回复
    def getReplayList(self):
        #回帖正文：replayContent(存储于replayContent数组中）
        replysContentList = []#定义回帖正文数组
        
        #定义记录回帖正文开始的下标变量
        k = self.BeginTimeIndex
        
        #定义正文在两个时间戳之间的变量，定义为headIndex,tailIndex,由大量数据进行统计学探索分析得出
        headPercentage = 0.1569
        tailPercentage = 0.5965
       
        if len(self.timeIndexList)>=2:  
            #若k=len(self.timeIndexList)-2时
            while k<len(self.timeIndexList)-1:
                k = k+1
                if k == len(self.timeIndexList)-1:
                    lengthSection = len(self.mainContent[self.timeIndexList[k]:])
                    #得出正文在self.mainContent中的头尾坐标
                    headIndex = int(lengthSection*headPercentage)+self.timeIndexList[self.BeginTimeIndex]
                    tailIndex = int(lengthSection*tailPercentage)+self.timeIndexList[self.BeginTimeIndex]
                    
                    #实时判断误差值#
                    headIndexAdjust,tailIndexAdjust = self.myContentAdjustment(headIndex,tailIndex,self.timeIndexList[self.BeginTimeIndex],self.timeIndexList[self.BeginTimeIndex]+lengthSection)
                    
                    replyContent = self.mainContent[headIndexAdjust:tailIndexAdjust]
                    pass
                else:
                    lengthSection = len(self.mainContent[self.timeIndexList[k]:self.timeIndexList[k+1]])
                    #得出正文在self.mainContent中的头尾坐标
                    headIndex = int(lengthSection*headPercentage)+self.timeIndexList[self.BeginTimeIndex]
                    tailIndex = int(lengthSection*tailPercentage)+self.timeIndexList[self.BeginTimeIndex]
                    
                    #实时判断误差值#
                    headIndexAdjust,tailIndexAdjust = self.myContentAdjustment(headIndex,tailIndex,self.timeIndexList[self.BeginTimeIndex],self.timeIndexList[self.BeginTimeIndex]+lengthSection)
                    
                    replyContent = self.mainContent[headIndexAdjust:tailIndexAdjust]
                    pass
                
                #将回帖内容加入到回帖数组中
                replysContentList.append("".join(replyContent))
                pass 
            return replysContentList
            pass
        pass
    
    #获取主贴正文
    def getMyContent(self): 

        #获取正文：
        #主贴正文：myContent
        
        #定义正文变量
        
        
        #定义正文开始的下标值,默认为0
        self.BeginTimeIndex = 0
        
        #定义一个长度阈值（前两个时间戳的在self.mainContent中的位置距离），记为length2time,设定为6
        length2time = 6
        #定义正文在两个时间戳之间的变量，定义为headIndex,tailIndex,由大量数据进行统计学探索分析得出
        headPercentage = 0.1569
        tailPercentage = 0.5965
        #定义区间长度变量
        lengthSection = 0
        #清除在时间提取阶段自己增加的格式
        i = 0
        for timeItem in self.timeList:
            newtimeItem = timeItem[3:]
            self.timeList[i] = newtimeItem
            i = i + 1
            pass
        
        # 判断：timeIndexList的长度至少为2
        if len(self.timeIndexList) >= 2:
            # 判断：若timeIndexList中相邻两项的长度小于或等于length2time，跳入else
            if self.timeIndexList[1]-self.timeIndexList[0] <= length2time:
                
                #取正文开头所取时间戳为timeIndexList集合中的下标
                self.BeginTimeIndex = 1
                
                #得出包含正文的区间长度
                if len(self.timeIndexList) == 2:
                    lengthSection = len(self.mainContent)-self.timeIndexList[self.BeginTimeIndex]
                else:
                    lengthSection = self.timeIndexList[2]-self.timeIndexList[self.BeginTimeIndex]
                
            # timeIndexList中相邻两项的长度大于length2time
            else:
                
                #得出包含正文的区间长度
                lengthSection = self.timeIndexList[1]-self.timeIndexList[self.BeginTimeIndex]
                pass
        elif len(self.timeIndexList) > 0:
            
            #得出包含正文的区间长度
            lengthSection = len(self.mainContent)-self.timeIndexList[0]
            pass
#         else:
#             myContent = "该贴已被删除或正在被审核"
#             raise MyException(str(myContent))
#             pass
                
        #得出正文在self.mainContent中的头尾坐标
        if self.timeIndexList != []:
            
            headIndex = int(lengthSection*headPercentage)+self.timeIndexList[self.BeginTimeIndex]
            tailIndex = int(lengthSection*tailPercentage)+self.timeIndexList[self.BeginTimeIndex]
                        
            #实时判断误差值#
            headIndexAdjust,tailIndexAdjust = self.myContentAdjustment(headIndex,tailIndex,self.timeIndexList[self.BeginTimeIndex],self.timeIndexList[self.BeginTimeIndex]+lengthSection)
                         
            #得出正文
            myContent = self.mainContent[headIndexAdjust:tailIndexAdjust]
        else:
            myContent = ''
            self.BeginTimeIndex = 0
            
        
        # 返回正文和正文在时间戳集合上的开始下标    
        return myContent,self.BeginTimeIndex
        pass
    
    
    # 正文区间调整方法 #
    # 参数：headIndex：预处理正文区间的开头下标值
    #      tailIndex：预处理正文区间的结尾下标值
    #      i:初始正文区间的开头下标值
    #      j:初始正文区间的结尾下标值
    def myContentAdjustment(self,headIndex,tailIndex,i,j):

        #    average为给定正文区间中各文本长度的平均值
        #    abnormalBeforeItemList,abnormalInnerItemList为存储预处理正文区间中满足一定条件的文本下标值
        average = 0
        abnormalBeforeItemList = []
        abnormalInnerItemList = []
        abnormalAfterItemList = []
        abnormalAfterItemLengthList = []
        
        #判断取得的headIndex坐标之前和之后的文本是否大于区间中文本平均值，若是也一并抓取#
        
        #1.计算文本平均值
        #1.1 计算所有文本长度和
        for item in self.mainContent[headIndex:tailIndex]:
            average = average + len(item)
            
            pass
        
        #1.2 计算预处理正文区间中的文本平均长度
        average = average/len(self.mainContent[headIndex:tailIndex])

        #取出headIndex坐标之前到时间戳这段文本的集合
        beforeAdjustList = self.mainContent[i:headIndex]
        #2.1 判断headIndex坐标之前的文本是否有连续大于headIndex‘和tailIndex区间文本的平均值的文本，连续阈值continute设为3
        continuite = 0
        for item in beforeAdjustList:

            if len(item)>=average:

                #连续阈值加1
                continuite = continuite + 1
                #获得该异常值所在下标并存于集合中
                abnormalBeforeItemList.append(beforeAdjustList.index(item))
            pass

        #3.1 获取abnormalBeforeItemList中第一个值，即坐标最小值，并根据该值再次更新headIndex值
        if abnormalBeforeItemList != []:
            
            #判断集合中最小值是否为0，即是否为首项
            if abnormalBeforeItemList[0] == 0:
                #若为首项，则移除它。
                abnormalBeforeItemList.pop(abnormalBeforeItemList[0])
                pass
            
            #判断集合是否为空，不为空则执行更新headIndex操作
            if len(abnormalBeforeItemList)>0:
                minResult = abnormalBeforeItemList[0]
                headIndex = headIndex - len(beforeAdjustList)+ minResult
                pass
            pass
        
        #取出headIndex坐标到tailIndex坐标这段文本的集合
        innerAdjustList = self.mainContent[headIndex:tailIndex]
        #2.2 判断innerAdjustList之间的文本是否有连续小于该区间文本长度平均值的文本，连续阈值continute设为3
        continute = 0
        for item in innerAdjustList:
            
            if len(item)<average:
                continute = continute + 1
                abnormalInnerItemList.append(innerAdjustList.index(item))
                pass
            else:
                if continute < 3:
                    continute = 0
                    abnormalAfterItemList = []
                    pass
                else:
                    break
                pass
            pass
        
        #3.2 获取abnormalInnerItemList中第一项值，即坐标最小值，并根据该值再次更新headIndex值
        if abnormalInnerItemList != []:
            
            #获取该集合中第一项的值
            BeginIndex = abnormalInnerItemList[0]

            if BeginIndex == 0:
                headIndex = headIndex + 3
            else:
                tailIndex = headIndex + BeginIndex
                pass
            pass
        
        #取出headIndex坐标到tailIndex坐标这段文本的集合
        afterAdjustList = self.mainContent[tailIndex:j]
        #2.3 判断innerAdjustList之间的文本是否有小于该区间文本长度平均值的文本，
        continute= 0
        for item in afterAdjustList:
            
            if len(item)>average:

                continute = continute + 1
                abnormalAfterItemList.append(afterAdjustList.index(item))
                abnormalAfterItemLengthList.append(len(item))
                pass
            pass
        
        #3.3 获取abnormalAfterItemList中最后一项值，即坐标最小值，并根据该值再次更新headIndex值

        if abnormalAfterItemList != []:
            
            #获取该集合中第一项的值
            firstIndex = abnormalAfterItemList[0]

            #若首项为0，则添加首项
            if firstIndex == 0:
                i = 0
                for index in abnormalAfterItemList:
                    if index == i:
                        i = i + 1
                        pass
                    else:
                        break
                    pass
                
                tailIndex = tailIndex + i
            else:
                bigIndexList = []
                i = 0
                for length in abnormalAfterItemLengthList:
                    if length > 3*average:
                        bigIndexList.append(i)
                        pass 
                    i = i + 1
                    pass
                if len(bigIndexList) > 1:
                    headIndex = tailIndex + abnormalAfterItemList[bigIndexList[0]]
                    tailIndex = tailIndex + abnormalAfterItemList[bigIndexList[-1]]
                    pass
                elif len(bigIndexList) == 1:
                    headIndex = tailIndex + abnormalAfterItemList[bigIndexList[0]]
                    tailIndex = tailIndex + abnormalAfterItemList[bigIndexList[-1]]+1
                    pass  
                pass
            pass
        
        #返回headIndex 和tailIndex
        return headIndex,tailIndex
        pass
