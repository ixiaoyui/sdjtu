#-*- coding: utf-8 -*-
import re
import json
import requests
from bs4 import BeautifulSoup
from datetime import datetime
import pandas
liebiao = {}

def hqlianjie():
    res2 = requests.get('http://www.sdjtu.edu.cn/channels/ch01410/')
    res2.encoding = 'utf=8'
    soup2 = BeautifulSoup(res2.text,'html.parser')
    lianjie = []
    for new in soup2.select('.pagedContent'):
        lianjie.append(new.select('a')[0]['href'])
    return lianjie

def yuedushuhq(newsurl):
    
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

def liebiaolink():
    res2 = requests.get('http://www.sdjtu.edu.cn/channels/ch01410/')
    res2.encoding = 'utf=8'
    soup2 = BeautifulSoup(res2.text,'html.parser')
    #for news in soup.select
    
    #news = soup2.select('.pagedContent')
    for new in soup2.select('.pagedContent'):
        liebiao[new.select('a')[0]['href']] = new.select('a')[0]['title']
        #liebiao['lianjie'] = 
    return liebiao
    
def neirong(link1):
       
    jieguo = {}
    #liebiao = {}
    res = requests.get(link1)
    res.encoding = 'utf=8'
    soup = BeautifulSoup(res.text,'html.parser')
    try:
        ceshi = soup.select('#content p')
        changdu = len(ceshi)
        if changdu > 1:
            
            jieguo['neirong'] = soup.select('#content p')[(changdu-1)].text.replace('\xa0','')
            jieguo['yuedushu'] = yuedushuhq(link1)#取得阅读数
            shijian = soup.select('div[align="center"]')[2]
            shijian2 = str(shijian)
            m = re.search('    (.+)    ',shijian2)
            jieguo['time'] = m[1]
            jieguo['laiyuan'] = soup.select('a[target="_blank"]' )[-2].text
            jieguo['biaoti'] = liebiaolink()[link1]
        else:
            jieguo['neirong'] = soup.select('#content p')[0].text.replace('\xa0','')
            jieguo['yuedushu'] = yuedushuhq(link1)#取得阅读数
            shijian = soup.select('div[align="center"]')[2]
            shijian2 = str(shijian)
            m = re.search('    (.+)    ',shijian2)
            jieguo['time'] = m[1]
            jieguo['laiyuan'] = soup.select('a[target="_blank"]' )[-2].text
            jieguo['biaoti'] = liebiaolink()[link1]
        
    except:
        pass
    print(changdu)
    return jieguo
huizong = []
count = 20
liebiaolink()
for link in liebiao:
    if count > 0:
        huizong.append(neirong(link))
        count = count - 1
    else:
        df = pandas.DataFrame(huizong)
        df.to_excel('news10.xlsx')
        print('已生成Excel文档！')
        break
#print(neirong('http://www.sdjtu.edu.cn/articles/ch01410/201701/553b499f-df45-4cce-a575-468056dcd282.shtml'))


