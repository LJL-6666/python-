import os
os.getcwd()
os.chdir("G://CDO//杂玩")
import requests
from pyquery import PyQuery as pq
import re
import pandas as pd
import time
import random  
from fake_useragent import UserAgent
ua = UserAgent()
headers = {'User-Agent':ua.random}

def restaurant(url):
    try:
        response = requests.get(url,headers=headers)
        if response.status_code == 200:
            return response.text
    except Exception:
        print('此页有问题！')
        return None


def filter_str(desstr,restr=''):
    res = re.compile("[^\uAC00-\uD7A3^a-z^A-Z^0-9^ ^]")
    return res.sub(restr, desstr)


def main():
    data = []
    for i in range(1,20):
        url = 'https://movie.naver.com/movie/bi/mi/pointWriteFormList.nhn?code=161967&type=after&onlyActualPointYn=N&onlySpoilerPointYn=N&order=newest&page='+str(i)
        print('准备采集第{}页数据'.format(i))
        html = restaurant(url)
        doc = pq(html)
        #print(i)
        for i in range(0,10):
            dic = {}
            dic['star'] = doc('li:nth-child(' + str(i+1) +') > div.star_score > em').text()
            dic['text'] = doc('#_filtered_ment_' + str(i)).text()
            dic['datetime'] = doc('li:nth-child(' + str(i+1) +') > div.score_reple > dl > dt > em:nth-child(2)').text()
            dic['name'] = doc('li:nth-child(' + str(i+1) +') > div.score_reple > dl > dt > em:nth-child(1) > a').text()
            dic['zan'] = doc('li:nth-child(' + str(i+1) +') > div.btn_area > a._sympathyButton > strong').text()
            dic['cai'] = doc('li:nth-child(' + str(i+1) +') > div.btn_area > a._notSympathyButton > strong').text()
            data.append(dic)
        time.sleep(random.random())
        pd.DataFrame(data).to_csv('电影评论.csv',encoding="utf_8",index = False)
    return data  


if __name__ == '__main__':
    data = main()
    final_result = pd.DataFrame(data)
    #final_result.to_csv('电影评论.csv',encoding="utf_8",index = False)
