#-*- coding: utf-8 -*-
'''
改成多线程的了，每个页面使用一个线程，速度快了很多，不过爬的图片不能分类存放了，都在一个文件夹里
'''
import re
import json
import requests
from bs4 import BeautifulSoup
import pandas
import os
import threading

def yuedushuhq(newsurl):#获取新闻阅读数
    
    res3 = requests.get(newsurl)
    res3.encoding = 'utf=8'
    soup3 = BeautifulSoup(res3.text,'html.parser')
    fangwenshulink = soup3.select('script')[-5].text#取得含有阅读数id的链接
    urlmuban = 'http://www.sdjtu.edu.cn/InterFront/embedservice/count.shtml?method=count&articleId={}&channelId=b395b5bd-91b3-42fc-b8ce-19e06703e915&siteId=12590635-85fe-408e-ad99-c812962f0fa2'
    m = re.search('articleId=(.+)&channelId',fangwenshulink)#取得新闻阅读数id
    plurl = urlmuban.format(m[1])#组成获取阅读数的链接
    json2 = requests.get(plurl)

    yuedu = json.loads(json2.text)
    yuedushu= str(yuedu['result']).lstrip('[').rstrip(']')#取得阅读数
    return yuedushu

def liebiaolink():#取得新闻链接
    print("正在初始化爬虫参数！")
    res2 = requests.get('http://www.sdjtu.edu.cn/channels/ch01410/')
    res2.encoding = 'utf=8'
    soup2 = BeautifulSoup(res2.text,'html.parser')
    for new in soup2.select('.pagedContent'):
        xwlianjie = new.select('a')[0]['href']
        liebiao.append(xwlianjie)
        #liebiao['lianjie'] = 
    print('\n初始化完成！\n')    
    return liebiao

jishu = 0
    
def neirong(args):#获取新闻内容
    global jishu
    global huizong
    try:
        jieguo = {}
            #liebiao = {}
        res = requests.get(args)
        res.encoding = 'utf=8'
        soup = BeautifulSoup(res.text,'html.parser')
        duanluo = (soup.select('#content p'))
        ceshi = len(soup.select('#content p'))
        
        if ceshi > 1:
           
            n = 0
            jieguotext = ''
            for pp in duanluo:
                ppp = re.search('(src=")(.+)"',str(pp))
                if ppp:
                    #print(ppp[2])
                    tplink = 'http://www.sdjtu.edu.cn' + ppp[2]
                    print("获取新闻图片！" + tplink)
                    mulu1 = 'D:\\12\\pachong2\\'
                    
                    tpwenjian = open(os.path.join(mulu1,os.path.basename(ppp[2])),'wb')
                    #print(tplink)
                    tpdata = requests.get(tplink)
                    for data in tpdata.iter_content(100000):#保存图片
                        tpwenjian.write(data)
                    tpwenjian.close()
                    n = n + 1

                else:
                    jieguo = {'neirong':''}
                    #jieguo2 = {}
                    
                    duanluo1 = str(soup.select('#content p')[n].text.replace('\xa0',''))
                    #print(duanluo1)
                    if len(duanluo1) > 0:
                        jieguotext = jieguotext + duanluo1

                        n = n + 1

                    else:
                        n = n + 1

            jieguo['neirong'] = jieguotext       
            try:
                     
                jieguo['yuedushu'] = yuedushuhq(args)
            except:
                pass
            shijian = soup.select('div[align="center"]')[2]
            shijian2 = str(shijian)
            m = re.search('    (.+)    ',shijian2)
            jieguo['time'] = m[1]
            jieguo['laiyuan'] = soup.select('a[target="_blank"]' )[-2].text
            jieguo['biaoti'] = soup.select('td[align="center"] p')[0].text
    
        if ceshi == 1:
                jieguo['neirong'] = str(soup.select('#content p')[0].text.replace('\xa0',''))
                try:
                                
                    jieguo['yuedushu'] = yuedushuhq(args)
                except:
                    pass
                shijian = soup.select('div[align="center"]')[2]
                shijian2 = str(shijian)
                m = re.search('    (.+)    ',shijian2)
                jieguo['time'] = m[1]
                jieguo['laiyuan'] = soup.select('a[target="_blank"]' )[-2].text
                jieguo['biaoti'] = soup.select('td[align="center"] p')[0].text
    
    except: 
            pass

    huizong.append(jieguo)
    

def shuru():
    global xzxc 
    
    global name
    name = ""
    t = 1
    global x
    global y
    try:
        x = int(input("请输入新闻起始位置（整数，大于等于1）：\n"))
        y = int(input("请输入要新闻结束位置（整数，大于等于起始条数）：\n"))
        
        #print(x,y)
        if x >= 1:
            #z = y - x
            if ((y >= x) and (y < 600)):
                x -= 1
                #y += 1
                #print(x,y)
            else:
                print("输入错误，请重新输入！")
                return shuru()
        else:
            print("输入错误，请重新输入！")
            return shuru()
    except:
        print("输入错误，请重新输入！")
        return shuru()
    
    else:
        name = input("请输入保存新闻的excel文件名称：\n")
        #print(x,y)
        for i in range(x,y):
            xz1 = threading.Thread(target=neirong,args=(lianjie[i],))
            xzxc.append(xz1)
        for i in range(x,y):
            xzxc[i].start()
            print("我启动了第%s线程获取新闻！" %(t))
            t += 1
        for xz1 in xzxc:
            xz1.join()
        
def yunxing():
    print("-------------山东交通学院官网新闻抓取程序--------------\n----------------请以管理员身份运行！-----------------")
    global lianjie
    global xzxc
    global huizong
    global liebiao
    xzxc = []
    huizong = []
    liebiao = []
    lianjie = liebiaolink()
    mulu1 = 'D:\\12\\pachong2\\'
    if os.path.exists(mulu1) == False:#判断存放图片的文件夹是否存在
        os.makedirs(mulu1)
        print('创建文件夹')            
    shuru()
    df = pandas.DataFrame(huizong)
    df.to_excel('%s.xlsx' %(name))
    print('\n已生成%s.xlsx！存放在本程序所在目录\n新闻图片存放在D:\\12\\pachong2\\目录中\n' %(name))
    jieshu = input("输入r重新运行本程序，输入其他字符结束程序！\n")
    if jieshu == "r":
        return yunxing()
    

yunxing()
