#coding = utf-8
'''
Created on 2017年4月19日

主要功能：输出需要进行统计分析的数据。
'''

from xlutils.copy import copy
import xlrd
import os
from mainCoding.MyException import MyException

class outputStatus:
    
    #mainContent以标题文本为第一项值的一个网页文本数组
    def __init__(self,myContent,i):
        self.myContent = myContent
        self.i = i
        pass
    
    def pickUpStatus(self):

        #返回本数组中最大值和其所在位置下标（若最大值为头或者尾，予以剔除后，再次取最大值）
        if self.myContent != []:
            
            #剔除长度小于一般可能值的myContent数组，初步设定阈值为5
            myContentLength = len(self.myContent)
            
            item = max(self.myContent)
            #获取最大值下标
            index = self.myContent.index(item)
            #判断最大值是否在头或尾位置
            if index==0 or index==len(self.myContent):
                #移除该值
                self.myContent.pop(index)
                pass
            if self.myContent != []:
                #获取最大值在self.myContent数组的相对位置，即比值ratio（self.myContent.index(item)/len(self.myContent)）
                ratio = self.myContent.index(max(self.myContent))/len(self.myContent)
                #返回长度最大值。以及他的下标.最大值下标/数组长度.数组长度
                return len(max(self.myContent)),self.myContent.index(max(self.myContent)),ratio,myContentLength     
                pass
            else:
                return 0,0,0,0
            pass
        else:
            return 0,0,0,0
            pass
    
    #输出主体部分各文本的长度。    
    def statusFormOutput(self):
 
        #变量定义
        #worksheet 默认是从0行、0列开始计数
        row = self.i
        col = 0
        
        #调用本地方法pickUpStatus，判断是否符合输出条件,返回最大值的文本长度、最大值下标，最大值下标/数组长度
        maxItemLenth,maxItemIndex,ratio,myContentLength= self.pickUpStatus()
        #写入文件，将上述数据写入文件
        oldWb1 = xlrd.open_workbook('statusFormOutput1.xlsx')
        newWb1 = copy(oldWb1)

        newWs1 = newWb1.get_sheet(0)
     
        #worksheet.write 方法将数据写入 xlsx 表格中
        #参数依次为：行号、列号、数据、[格式]
        newWs1.write(row, col, maxItemIndex)#写入最大值所在的下标
        col += 1
        newWs1.write(row, col, maxItemLenth)#写入最大值项的长度
        col += 1
        newWs1.write(row, col, ratio)#写入self.myContent.index(item)/len(self.myContent)
        col += 1
        newWs1.write(row, col, myContentLength)#写入
        
        os.remove('statusFormOutput1.xlsx')
        
        newWb1.save('statusFormOutput1.xlsx')
       
        '''
        -------------------------分割线------------------------------
        '''
        
        col = 0
        
        #在同一个xlsx文件中。依次写入每个网页遍历到的关于myContent数组中各文本的长度。
        oldWb2 = xlrd.open_workbook('statusFormOutput2.xlsx')
        newWb2 = copy(oldWb2)

        newWs2 = newWb2.get_sheet(0)
     
        #worksheet.write 方法将数据写入 xlsx 表格中
        #参数依次为：行号、列号、数据、[格式]
        for item in self.myContent:
            newWs2.write(row, col, len(item))
            col += 1
            pass
        
        os.remove('statusFormOutput2.xlsx')
        
        newWb2.save('statusFormOutput2.xlsx')
        
        pass
    pass
    def outputUrlError(self,url,i):
        #变量定义
        #worksheet 默认是从0行、0列开始计数
        row = i
        col = 0
        
        #写入文件，将上述数据写入文件
        oldWb1 = xlrd.open_workbook('ErrorUrl.xlsx')
        newWb1 = copy(oldWb1)

        newWs1 = newWb1.get_sheet(0)
     
        #worksheet.write 方法将数据写入 xlsx 表格中
        #参数依次为：行号、列号、数据、[格式]
        newWs1.write(row, col, url)#写入出错网站网址
        col += 1
        
        os.remove('ErrorUrl.xlsx')
        
        newWb1.save('ErrorUrl.xlsx')
        pass
    pass
        