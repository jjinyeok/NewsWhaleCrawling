import requests
from selenium import webdriver
from selenium.webdriver.chrome.service import Service
from selenium.webdriver.common.by import By
from webdriver_manager.chrome import ChromeDriverManager
from bs4 import BeautifulSoup

res = requests.get('https://n.news.naver.com/article/020/0003426282?ntype=RANKING').text
res = BeautifulSoup(res, 'html.parser')
print(res.find('div', id='dic_area'))