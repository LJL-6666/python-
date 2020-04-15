# -*- coding: utf-8 -*-
"""
Created on Sun May 12 15:24:31 2019
 
@author: Administrator
"""
 
# -*- coding: utf-8 -*-
"""
Created on Sat Jan 12 10:31:29 2019
 
@author: Administrator
"""
import json
import time
import pandas as pd
import os
from bs4 import BeautifulSoup  
from pyecharts import Bar,Line,Overlap
from selenium import webdriver 
import sys
import requests
import time
import datetime
from scipy.misc import imread  # 这是一个处理图像的函数
from wordcloud import WordCloud, ImageColorGenerator
from collections import Counter
import matplotlib.pyplot as plt
 
os.chdir('D:/爬虫/B站编程')
tag_dict = pd.read_excel('coding_tag.xlsx')
## 获得列表
def get_list(i,j):
    attempts = 0
    success = False
    while attempts < 5 and not success:
        try:
            url = 'https://search.bilibili.com/all?keyword=%E7%BC%96%E7%A8%8B&from_source=banner_search&order={}&duration=4&tids_1=36&page={}'.format(i,j+1) 
            header = {'User-Agent': 'Mozilla/5.0 (Windows NT 10.0; Win32; x32; rv:54.0) Gecko/20100101 Firefox/54.0',
                      'Connection': 'keep-alive'}
            cookies ='v=3; iuuid=1A6E888B4A4B29B16FBA1299108DBE9CDCB327A9713C232B36E4DB4FF222CF03; webp=true; ci=1%2C%E5%8C%97%E4%BA%AC; __guid=26581345.3954606544145667000.1530879049181.8303; _lxsdk_cuid=1646f808301c8-0a4e19f5421593-5d4e211f-100200-1646f808302c8; _lxsdk=1A6E888B4A4B29B16FBA1299108DBE9CDCB327A9713C232B36E4DB4FF222CF03; monitor_count=1; _lxsdk_s=16472ee89ec-de2-f91-ed0%7C%7C5; __mta=189118996.1530879050545.1530936763555.1530937843742.18'
            cookie = {}
            for line in cookies.split(';'):
                name, value = cookies.strip().split('=', 1)
                cookie[name] = value    
            html = requests.get(url,cookies=cookie, headers=header).content
            bsObj = BeautifulSoup(html.decode('utf-8'),"html.parser")
            script = bsObj.find_all('script')[3].text
            info = json.loads(script.replace('window.__INITIAL_STATE__=','').split(';(function()')[0])['allData']['video']
            return info
        except:
            attempts = attempts+1
    return []
 
 
coding_all = []
type = ['click','stow','dm']
for i in type:
    for j in range(50):
        this_coding = get_list(i,j)
        coding_all = coding_all+this_coding
        print(str(j))
 
 ## 数据处理       
coding=pd.DataFrame()
coding['title'] = [k['title'] for k in coding_all]
coding['arcurl'] = [k['arcurl'] for k in coding_all]
coding['pic'] = [k['pic'] for k in coding_all]
coding['author'] = [k.get('author') for k in coding_all]
coding['play'] = [int(k['play']) if k['play'] != '--' else 0 for k in coding_all]
coding['danmu'] = [k['video_review'] for k in coding_all]
coding['favorites'] = [k['favorites'] for k in coding_all]
coding['review'] =  [k['review'] for k in coding_all]
coding['tag'] =  [k['tag'].split(',') for k in coding_all]
 
 
 
## 拓展标签
def dataframe_explode(dataframe, fieldname): 
    temp_fieldname = fieldname + '_made_tuple_'
    dataframe[temp_fieldname] = dataframe[fieldname].apply(tuple)       
    list_of_dataframes = []
    for values in dataframe[temp_fieldname].unique().tolist(): 
        list_of_dataframes.append(pd.DataFrame({
            temp_fieldname: [values] * len(values), 
            fieldname: list(values), 
        }))
    dataframe = dataframe[list(set(dataframe.columns) - set([fieldname]))].merge(pd.concat(list_of_dataframes), how='left', on=temp_fieldname) 
    del dataframe[temp_fieldname]
    return dataframe
 
## 分组统计
coding_tag = dataframe_explode(coding,'tag')
coding_tag['tag'] = coding_tag['tag'].apply(str.lower)
coding_tag['type'] = coding_tag['tag'].map({tag_dict['tag'][k]:tag_dict['type'][k] for k in range(tag_dict.shape[0])})
coding_tag = coding_tag.groupby(['title','pic','author','arcurl','tag','type'],as_index=False).agg({'play':'max','danmu':'max','favorites':'max','review':'max'})
 
 
 
tag_count = coding_tag.groupby(['tag','type'],as_index=False).agg({'title':['count'],'play':['sum'],'danmu':['sum'],'favorites':['sum']})   
tag_count.columns = ['tag','type','num','play','danmu','favorites']
## 词云
tag_stat = Counter(dataframe_explode(coding,'tag')['tag'])
back_color = imread('D:/爬虫/西红柿/西红柿.jpg')  # 解析该图片
 
wc = WordCloud(background_color='white',  # 背景颜色
               max_words=100,  # 最大词数
               mask=back_color,  # 以该参数值作图绘制词云，这个参数不为空时，width和height会被忽略
               max_font_size=200,  # 显示字体的最大值
               font_path="C:/Windows/Fonts/STFANGSO.ttf",  # 解决显示口字型乱码问题，可进入C:/Windows/Fonts/目录更换字体
               random_state=42,  # 为每个词返回一个PIL颜色
               # width=1000,  # 图片的宽
               # height=860  #图片的长
               )
# WordCloud各含义参数请点击 wordcloud参数
image_colors = ImageColorGenerator(back_color)
wc.generate_from_frequencies(tag_stat)
 
plt.figure(figsize=(8,8),dpi=80)
plt.imshow(wc.recolor(color_func=image_colors))
plt.axis('off')
 
 
tag_stat = {tag_count['tag'][k]:tag_count['play'][k] for k in range(tag_count.shape[0])}
back_color = imread('D:/爬虫/西红柿/西红柿.jpg')  # 解析该图片
 
wc = WordCloud(background_color='white',  # 背景颜色
               max_words=100,  # 最大词数
               mask=back_color,  # 以该参数值作图绘制词云，这个参数不为空时，width和height会被忽略
               max_font_size=200,  # 显示字体的最大值
               font_path="C:/Windows/Fonts/STFANGSO.ttf",  # 解决显示口字型乱码问题，可进入C:/Windows/Fonts/目录更换字体
               random_state=42,  # 为每个词返回一个PIL颜色
               # width=1000,  # 图片的宽
               # height=860  #图片的长
               )
# WordCloud各含义参数请点击 wordcloud参数
image_colors = ImageColorGenerator(back_color)
wc.generate_from_frequencies(tag_stat)
 
plt.figure(figsize=(8,8),dpi=80)
plt.imshow(wc.recolor(color_func=image_colors))
plt.axis('off')
 
## 绘制图片
coding_stat = tag_count[tag_count['type']=='语言']
coding_stat.sort_values('play',ascending=False,inplace=True)
attr = coding_stat['tag'][0:10]
v1 = coding_stat['play'][0:10]
bar = Bar("语言类播放量TOP10")
bar.add("播放数量", attr, v1, is_stack=True, xaxis_rotate=30,xaxis_label_textsize=18,
         xaxis_interval =0,is_splitline_show=False,label_text_size=12,is_label_show=True)
bar.render('语言类播放量TOP10.html')
 
coding_stat = tag_count[tag_count['type']=='技术']
coding_stat.sort_values('play',ascending=False,inplace=True)
attr = coding_stat['tag'][0:10]
v1 = coding_stat['play'][0:10]
bar = Bar("技术类播放量TOP10")
bar.add("播放数量", attr, v1, is_stack=True, xaxis_rotate=30,xaxis_label_textsize=18,
         xaxis_interval =0,is_splitline_show=False,label_text_size=12,is_label_show=True)
bar.render('技术类播放量TOP10.html')
 
coding_stat = tag_count[tag_count['type']=='语言']
coding_stat.sort_values('danmu',ascending=False,inplace=True)
attr = coding_stat['tag'][0:10]
v1 = coding_stat['danmu'][0:10]
bar = Bar("语言类弹幕量TOP10")
bar.add("弹幕数量", attr, v1, is_stack=True, xaxis_rotate=30,xaxis_label_textsize=18,
         xaxis_interval =0,is_splitline_show=False,label_text_size=12,is_label_show=True)
bar.render('语言类弹幕量TOP10.html')
 
coding_stat = tag_count[tag_count['type']=='技术']
coding_stat.sort_values('danmu',ascending=False,inplace=True)
attr = coding_stat['tag'][0:10]
v1 = coding_stat['danmu'][0:10]
bar = Bar("技术类弹幕量TOP10")
bar.add("弹幕数量", attr, v1, is_stack=True, xaxis_rotate=30,xaxis_label_textsize=18,
         xaxis_interval =0,is_splitline_show=False,label_text_size=12,is_label_show=True)
bar.render('技术类弹幕量TOP10.html')
