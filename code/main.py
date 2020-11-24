import requests
from lxml import etree
import csv
import re
import datetime
import time
from wordcloud import WordCloud
import pandas as pd
import jieba


headers={
'cookie': '_zap=1f1da671-08e7-48d8-9b89-5692fb1e7bf8; d_c0="AJDRR4XqXBGPTiKohL_9rTGJ6W59jSy46GY=|1591073269"; _ga=GA1.2.760471543.1591073269; _xsrf=gB1XPkIUr5lBxWkVw2iTYKHiKWWgE5H5; z_c0=Mi4xRXY2dUJnQUFBQUFBa05GSGhlcGNFUmNBQUFCaEFsVk5JazdQWHdEN0JxSHpCTXBORk9qRE90eVlOQS14VUZ2cHZn|1591869474|3e49d2809571dcec39d1b82b596e0a1962340120; q_c1=8289972241ed41d290160f779149ab47|1604841864000|1591869480000; Hm_lvt_98beee57fd2ef70ccdd5ca52b9740c49=1606197115,1606197116,1606198192,1606200762; tst=h; tshl=; Hm_lpvt_98beee57fd2ef70ccdd5ca52b9740c49=1606208455',
# 'referer': 'https://www.zhihu.com/question/406493288',
# 'sec-fetch-mode': 'cors',
# 'sec-fetch-site': 'same-origin',
'user-agent': 'Mozilla/5.0 (X11; Linux x86_64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/86.0.4240.111 Safari/537.36'
}

headers1={
'cookie': '_zap=1f1da671-08e7-48d8-9b89-5692fb1e7bf8; d_c0="AJDRR4XqXBGPTiKohL_9rTGJ6W59jSy46GY=|1591073269"; _ga=GA1.2.760471543.1591073269; _xsrf=gB1XPkIUr5lBxWkVw2iTYKHiKWWgE5H5; z_c0=Mi4xRXY2dUJnQUFBQUFBa05GSGhlcGNFUmNBQUFCaEFsVk5JazdQWHdEN0JxSHpCTXBORk9qRE90eVlOQS14VUZ2cHZn|1591869474|3e49d2809571dcec39d1b82b596e0a1962340120; q_c1=8289972241ed41d290160f779149ab47|1604841864000|1591869480000; Hm_lvt_98beee57fd2ef70ccdd5ca52b9740c49=1606197115,1606197116,1606198192,1606200762; tst=h; tshl=; Hm_lpvt_98beee57fd2ef70ccdd5ca52b9740c49=1606208455',
'referer': 'https://www.zhihu.com/question/406493288',
'sec-fetch-mode': 'cors',
'sec-fetch-site': 'same-origin',
'user-agent': 'Mozilla/5.0 (X11; Linux x86_64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/86.0.4240.111 Safari/537.36'
}

now = datetime.datetime.now()
dt_string = now.strftime("%d-%m-%Y-%H")



def get_parse(response):
    html=etree.HTML(response)
    # 获取知乎热榜排名标题热度
    ret = html.xpath("//section[@class='HotItem']")
    D=[]
    TD=[]
    for item in ret:
        try:
            rank=item.xpath(".//div[@class='HotItem-index']/div/text()")[0]
            title=item.xpath(".//div[@class='HotItem-content']/a/@title")[0]
            rot=item.xpath(".//div[@class='HotItem-metrics HotItem-metrics--bottom']/text()")[0]
            href=item.xpath(".//div[@class='HotItem-content']/a/@href")[0]
            time=datetime.datetime.now().strftime('%Y-%m-%d')
            message=get_content(href)
            answer=str(message['answer'])
            guanzhu=str(message['guanzhu'])
            liulan=str(message['liulan'])
            data=[rank,title,rot,href,answer,guanzhu,liulan,time]
            print(data)
            D.append(data)
        except:
            pass
    save(D)


def get_content(href):
    try:
        response = requests.get(href, headers=headers1).text
        data={}
        html=etree.HTML(response)
        answer=html.xpath('//*[@id="QuestionAnswers-answers"]/div/div/div/div[1]/h4/span/text()')[0]
        data['answer']=answer
        guanzhu=re.findall('</div><strong class="NumberBoard-itemValue" title="(.*?)">(.*?)</strong></div>',response)[0][0]
        data['guanzhu']=guanzhu
        liulan = re.findall('</div><strong class="NumberBoard-itemValue" title="(.*?)">(.*?)</strong></div>', response)[1][0]
        data['liulan'] = liulan
        return data
    except:
        pass


def save(name):
    with open('./csv/{}.csv'.format(dt_string), 'a', newline='', encoding='utf-8') as csvfile:
        writer = csv.writer(csvfile, dialect='excel')
        writer.writerows(name)

def crawl():
    list2=['排名','标题','热度','回答链接','回答数','关注数','浏览数','时间']
    with open('./csv/{}.csv'.format(dt_string), 'a', newline='', encoding='utf-8') as csvfile:
        writer = csv.writer(csvfile, dialect='excel')
        writer.writerow(list2)
    list1=['','?list=zvideo','?list=science','?list=digital','?list=sport','?list=fashion','?list=car','?list=film','?list=school','?list=depth','?list=focus']
    list1=['']
    # 全站,视频，科学，数码，体育，时尚，汽车，校园，影视，汽车，国际
    for i in list1:
        url='https://www.zhihu.com/hot'+i
        print(url)
        response=requests.get(url,headers=headers).text
        get_parse(response)
        time.sleep(10)

def loadStopWords(file_path = '中文停用词词表.txt'):
    stopwords = []
    with open(file_path,'r',encoding='utf-8') as f:
        text = f.readlines()
        for line in text:
            stopwords.append(line[:-1])#去换行符
    return stopwords

def deleteStopWords(g_list,stop_words):
    outcome = []
    for term in g_list:
        if term not in stop_words:
            outcome.append(term)
    return outcome

def generateImage(string, save_file):
    wc = WordCloud(font_path = "./wqy-microhei.ttc", background_color = 'white',
                      collocations = False, width = 800, height = 400, max_words = 150)
    wc.generate(string)
    wc.to_file(save_file)

def generateWordCloud():
    stop_words = loadStopWords()
    df = pd.read_csv('./csv/{}.csv'.format(dt_string))
    df.dropna(inplace = True)
    string = ''
    for title in df['标题']:
        seg_list = jieba.cut(title)
        title = " ".join(deleteStopWords(seg_list, stop_words))
        string += title + ' '
    generateImage(string, './image/{}.png'.format(dt_string))
    

        
if __name__=='__main__':
    crawl()
    generateWordCloud();
