#-*- coding: utf-8 -*-
import re
import json
import requests
from bs4 import BeautifulSoup
from datetime import datetime
import pandas
import os
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

jishu = 0
    
def neirong(link1):
    global jishu
    #print(jishu)  
    jieguo = {}
    #liebiao = {}
    res = requests.get(link1)
    res.encoding = 'utf=8'
    soup = BeautifulSoup(res.text,'html.parser')
    try:
        jieguo = {}
            #liebiao = {}
        res = requests.get(link1)
        res.encoding = 'utf=8'
        soup = BeautifulSoup(res.text,'html.parser')
        
        duanluo = (soup.select('#content p'))
        
        ceshi = len(soup.select('#content p'))
        #print(ceshi)
        
        if ceshi > 1:
            
            n = 0
            jieguotext = ''
            for pp in duanluo:
                ppp = re.search('(src=")(.+)"',str(pp))
                #print(ppp[1])
                
                if ppp:
                    #print(ppp[2])
                    tplink = 'http://www.sdjtu.edu.cn' + ppp[2]
                    print(tplink)
                    mulu1 = ''
                    mulu1 = ('D:\\workspace\\123\\12\\' + str(jishu))
                    if os.path.exists(mulu1) == False:
                        os.makedirs(mulu1)
                        print('创建文件夹' + str(jishu))
                    #newmulu = os.path.join('D:\\workspace\\123\\12',str(jishu))
                    tpwenjian = open(os.path.join(str(jishu),os.path.basename(ppp[2])),'wb')
                    #print(tplink)
                    tpdata = requests.get(tplink)
                    for data in tpdata.iter_content(100000):
                        tpwenjian.write(data)
                    tpwenjian.close()
                    n = n + 1
                    #jishu = jishu + 1
                    #print(n)
                else:
                    jieguo = {'neirong':''}
                    #jieguo2 = {}
                    
                    duanluo1 = str(soup.select('#content p')[n].text.replace('\xa0',''))
                    #print(duanluo1)
                    if len(duanluo1) > 0:
                        jieguotext = jieguotext + duanluo1
                        #print(jieguotext)
                        n = n + 1
                        #jishu = jishu + 1
                    else:
                        n = n + 1
                        #jishu = jishu + 1
            jieguo['neirong'] = jieguotext            
            jieguo['yuedushu'] = yuedushuhq(link1)#取得阅读数
            shijian = soup.select('div[align="center"]')[2]
            shijian2 = str(shijian)
            m = re.search('    (.+)    ',shijian2)
            jieguo['time'] = m[1]
            jieguo['laiyuan'] = soup.select('a[target="_blank"]' )[-2].text
            jieguo['biaoti'] = liebiaolink()[link1]
    
        if ceshi == 1:
                jieguo['neirong'] = str(soup.select('#content p')[0].text.replace('\xa0',''))            
                jieguo['yuedushu'] = yuedushuhq(link1)#取得阅读数
                shijian = soup.select('div[align="center"]')[2]
                shijian2 = str(shijian)
                m = re.search('    (.+)    ',shijian2)
                jieguo['time'] = m[1]
                jieguo['laiyuan'] = soup.select('a[target="_blank"]' )[-2].text
                jieguo['biaoti'] = liebiaolink()[link1]
                #jishu = jishu + 1
        #jishu = jishu + 1    
    except:
             
            pass
    jishu = jishu + 1
    return jieguo
huizong = []
count = 40
liebiaolink()
for link in liebiao:
    if count > 0:
        huizong.append(neirong(link))
        count = count - 1
    else:
        df = pandas.DataFrame(huizong)
        df.to_excel('news88.xlsx')
        print('已生成Excel文档！')
        break
#print(neirong('http://www.sdjtu.edu.cn/articles/ch01410/201701/553b499f-df45-4cce-a575-468056dcd282.shtml'))


