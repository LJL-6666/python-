import requests
from bs4 import BeautifulSoup
import numpy as np
import pandas as pd 
import time
from selenium import webdriver
from selenium.webdriver.common.by import By
from selenium.webdriver.common.keys import Keys
from selenium.webdriver.chrome.options import Options
# 定义登录函数
def login_douban():
    '''功能：自动登录豆瓣网站'''
    global browser  # 设置为全局变量
    browser = webdriver.Chrome('C:\Program Files (x86)\Google\Chrome\Application\chromedriver.exe')

    # 进入登录页面
    login_url = 'https://accounts.douban.com/passport/login?source=movie'
    browser.get(login_url)

    # 点击密码登录
    browser.find_element_by_class_name('account-tab-account').click()

    # 输入账号和密码
    username = browser.find_element_by_id('username')
    username.send_keys('13649204620')
    password = browser.find_element_by_id('password')
    password.send_keys('ljlljwlx258')

    # 点击登录
    browser.find_element_by_class_name('btn-account').click()

    # 定义函数获取单页数据
    def get_one_page(url):
        '''功能：传入url，豆瓣电影一页的短评信息'''
        # 进入短评页
        browser.get(url)

        # 使用bs解析网页数据
        bs = BeautifulSoup(browser.page_source, 'lxml')

        # 获取用户名
        username = [i.find('a').text for i in bs.findAll('span', class_='comment-info')]
        # 获取用户url
        user_url = [i.find('a')['href'] for i in bs.findAll('span', class_='comment-info')]

        # 获取推荐星级
        rating = []
        for i in bs.findAll('span', class_='comment-info'):
            try:
                one_rating = i.find('span', class_='rating')['title']
                rating.append(one_rating)
            except:
                rating.append('力荐')

                # 评论时间
        time = [i.find('span', class_='comment-time')['title'] for i in bs.findAll('span', class_='comment-info')]
        # 短评信息
        short = [i.text for i in bs.findAll('span', class_='short')]
        # 投票次数
        votes = [i.text for i in bs.findAll('span', class_='votes')]

        # 创建一个空的DataFrame
        df_one = pd.DataFrame()
        # 存储信息
        df_one['用户名'] = username
        df_one['用户主页'] = user_url
        df_one['推荐星级'] = rating
        df_one['评论时间'] = time
        df_one['短评信息'] = short
        df_one['投票次数'] = votes

        return df_one
# 定义函数获取25页数据（目前所能获取的最大页数）
def get_25_page(movie_id):
    '''功能：传入电影ID，获取豆瓣电影25页的短评信息'''
    # 创建空的DataFrame
    df_all = pd.DataFrame()

    # 循环追加
    for i in range(25):
        url = "https://movie.douban.com/subject/{}/comments?start={}&limit=20&sort=new_score&status=P".format(movie_id,i*20)
        print('我正在抓取第{}页'.format(i+1), end='\r')
        # 调用函数
        df_one = get_one_page(url)
        df_all = df_all.append(df_one, ignore_index=True)
        # 程序休眠一秒
        time.sleep(1.5)
    return df_all

if __name__ == '__main__':
    # 先运行登录函数
    login_douban()
    # 程序休眠两秒
    time.sleep(2)
    # 再运行循环翻页函数
    movie_id = 30306570  # 囧妈
    df_all = get_25_page(movie_id)
    df_all.to_csv('囧妈数据.csv')
    print("爬取完成！！！")
    
