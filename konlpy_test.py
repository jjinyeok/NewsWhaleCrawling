# Test code 
import requests
from selenium import webdriver
from selenium.webdriver.chrome.service import Service
from selenium.webdriver.common.by import By
from webdriver_manager.chrome import ChromeDriverManager
from bs4 import BeautifulSoup

res = requests.get('https://n.news.naver.com/article/020/0003426282?ntype=RANKING').text
res = BeautifulSoup(res, 'html.parser')
content = str(res.find('div', id='dic_area'))
print(content)

from konlpy.tag import Komoran
from collections import Counter
komoran = Komoran()
list_article = komoran.nouns(content)

count_list_article = Counter(list_article)
count = 0
keywords = []
print(count_list_article.most_common(50))
