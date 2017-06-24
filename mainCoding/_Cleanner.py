#coding=utf-8
'''
Created on 2017年4月16日
主要数据预处理程序。将获得的网页进行噪音消除及其他清理操作。得到一个较为“整洁”的DOM树状结构内容

'''


from bs4 import BeautifulSoup,Comment
import re
import time


def getDom(pageurl,charset):
    
    if charset is None:
        charset = 'utf-8'
    
    soup = BeautifulSoup(pageurl,'html.parser',from_encoding=charset)
    
    #去除特定的head、script、style、img、input标签
    [body.extract() for body in soup(['head','img','script','style','input'])]#
     
    #去除注释
    for element in soup(text=lambda text: isinstance(text, Comment)):
        element.extract()
        pass
    
    #将soup中的文本提取出来，并存储到body数组中
    soup = soup.text.strip().lstrip().rstrip().split()

    #获取当前日期和具体时间，以便提出soup数组中出现的无效数据（当前系统时间）  
    currentDate = time.strftime('%Y-%m-%d',time.localtime(time.time()))
    #处理日期格式，例：2017-04-20---->2017-4-20
    currentDate1 = currentDate[0:5]+currentDate[6:]
    #获取当前具体时间，以便提出soup数组中出现的无效数据（当前系统时间） 
    currentTime = time.strftime('%H:%M',time.localtime(time.time()))
    #处理日期格式，例：23:58---->23:5,防止因为程序运行而导致的时间误差
    currentTime1 = currentTime[0:4]

    #剔除soup数组中无效字符串，减少干扰
    #剔除soup数组中'copyright'后半部分的版权内容
    #剔除soup数组中无效的年月。如"1999",剔除“2001-2007”格式的时间字符串
    #剔除soup数组中类似于”最后登录：2017-04-20 23：:55“的无效时间
    #剔除soup数组中出现的当前系统时间字符串
    re0 = re.compile(r'.*Copyright.*')
    re1 = re.compile(r'.*((19\d{2}\D)|(\d{4}-\d{4}\D)).*')
    re2 = re.compile(r'(^|.*)注册.*(\d{2,4}(-|/))?\d{1,2}(-|/)\d{1,2}$')
    re3 = re.compile(r'.*('+currentDate1+'|'+currentDate+').*')
    re4 = re.compile(r'.*'+currentTime1+'\d.*')
    re5 = re.compile(r'^最后.*(\d{2,4}(-|/))?\d{1,2}(-|/)\d{1,2}.*')
    for item in soup:

        #剔除soup数组中以":"、“：”结尾的文本字符串
        if item.endswith("："):
            soup.pop(soup.index(item))
            pass
        if item.endswith(":"):
            soup.pop(soup.index(item))
            pass
        #剔除soup数组中"|"和“»”和“›”文本字符串
        if '|' in soup:
            soup.pop(soup.index('|'))
            pass
        if '>' in soup:
            soup.pop(soup.index('>'))
            pass
        if '»' in soup:
            soup.pop(soup.index('»'))
            pass
        if '›' in soup:
            soup.pop(soup.index('›'))
            pass
        if re0.match(item):
            CopyrightIndex = soup.index(item)-5
            while CopyrightIndex <= len(soup)-1:
                popItem = soup.pop(CopyrightIndex)
                pass
            pass
        #剔除不规则时间
        if re1.match(item):
            #获得主体内容中re1指定格式匹配到的文本所在的下标timeIndex
            timeIndex = soup.index(item)
            #,剔除不规则不正常时间数据，防止被重复遍历
            soup.pop(timeIndex)
            pass
        
        if re2.match(item):
            #获得主体内容中re2指定格式匹配到的文本所在的下标timeIndex
            timeIndex = soup.index(item)
            #,剔除不规则不正常时间数据，并让该下标下的值置为'|'，防止被重复遍历
            soup.pop(timeIndex)
        pass
        #剔除当前系统时间
        if re3.match(item):
            if item in soup:
                if re4.match(soup[soup.index(item)+1]):
                    #剔除当前系统时间
                    soup.pop(soup.index(item)+1)
                    #去除当前系统日期
                    soup.pop(soup.index(item))
                    pass
                pass
            pass
        if re5.match(item):
            if item in soup:
                #获得主体内容中re2指定格式匹配到的文本所在的下标timeIndex
                timeIndex = soup.index(item)
                #,剔除不规则不正常时间数据，并让该下标下的值置为'|'，防止被重复遍历
                soup.pop(timeIndex)
                pass
            pass
        pass
    #返回经过数据预处理的soup数组
    return soup
    pass