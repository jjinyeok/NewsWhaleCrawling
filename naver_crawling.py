import requests
from selenium import webdriver
from selenium.webdriver.chrome.service import Service
from selenium.webdriver.common.by import By
from webdriver_manager.chrome import ChromeDriverManager
from bs4 import BeautifulSoup

# 네이버 랭킹 뉴스
# 언론사별 많이 본 뉴스
# 언론사별 많이 본 뉴스 집계 방식
# 오전 7시 ~ 익일 1시: 한시간 기준으로 집계한 랭킹 노출
# 오전 1시 ~ 오전 6시: 해당 시간동안 별도 집계 X -> 오전 1시 랭킹 노출
# 오전 6시 ~ 오전 7시: 오전 1시 ~ 6시까지의 조회수를 합쳐서 집계한 랭킹 노출
# 업데이트 + 매시 + 약 5분(집계 처리 시간)

# 하루 20번 크롤링 진행
# -> 0시 10분, 1시 10분, 6시 10분, 7시 10분, 8시 10분
# -> 9시 10분, 10시 10분, 11시 10분, 12시 10분, 13시 10분
# -> 14시 10분, 15시 10분, 16시 10분, 17시 10분, 18시 10분
# -> 19시 10분, 20시 10분, 21시 10분, 22시 10분, 23시 10분

# 뉴스 리스트: 뉴스 딕셔너리 들어갈 예정
# 뉴스 딕셔너리:
# {
#     ---DB의 news Table로 이동---
#     "news_title", (뉴스제목) O
#     "news_media", (언론사) O
#     "news_reporter", (기자) △
#     "news_url", (뉴스 URL) O
#     "media_url", (언론사 URL)O
#     "timestamp", (최종수정일자) O
#     ---DB의 news_keyword Table로 이동---
#     "keyword1", (연관키워드)
#     "keyword2", (연관키워드)
#     "keyword3", (연관키워드)
# }
#news_list = []

# chrome 드라이버 로드
def set_chrome_driver():
    chrome_options = webdriver.ChromeOptions()
    driver = webdriver.Chrome(service=Service(ChromeDriverManager().install()), options=chrome_options)
    return driver

# 맨 마지막까지 뉴스를 수집하기 위해 최대한으로 뉴스를 뽑아내는 과정
def find_all_articles (driver):
    while True:
        try:
            # 다른 언론사 랭킹 더보기 <button> 클릭
            driver.find_element(by=By.XPATH, value='//*[@id="wrap"]/div[4]/button').click()
        except:
            break

# 뉴스 제목 <a> find -> news_title, news_url
def init_articles(driver):
    news_list = []
    lis = driver.find_elements(by=By.CSS_SELECTOR, value="a.list_title")
    # 각 뉴스 제목 <a>로부터 news_titel(뉴스 제목), news_url(뉴스 url) 받아옴
    for i in range(len(lis)):    
        ############## ############
        # news_title # # news_url #
        ############## ############
        news_list.append({'news_title': lis[i].text, 'news_url': lis[i].get_attribute('href')})
    return news_list

# 브라우저(chrome) 닫음
def close_browser(driver):
    driver.close()

# news_list 완성
def complete_articles(news_list):
    for i in range(len(news_list)):
        
        res = requests.get(news_list[i]['news_url']).text
        res = BeautifulSoup(res, 'html.parser')
        
        # To-do: 기자를 어디서 찾을 것아며 어떻게 기자가 없는 상황을 방지할 수 있을까?
        #################
        # news_reporter #
        #################
        try:
            news_reporter = res.find('span', 'byline_s').text
        except:
            news_reporter = '기자 없음'

        ############## ############# ###################
        # news_media # # media_url # # media_image_src #
        ############## ############# ###################
        news_media =  res.find('img', 'media_end_head_top_logo_img light_type')['title']
        media_url = res.find('a', 'media_end_head_top_logo')['href']
        media_image_src = res.find('img', 'media_end_head_top_logo_img light_type')['src']

        #############
        # timestamp #
        #############
        # if) 수정시간 find할 수 없다면, timestamp는 작성시간
        try:
            timestamp = res.find('span', 'media_end_head_info_datestamp_time _ARTICLE_DATE_TIME').text
            timestamp = res.find('span', 'media_end_head_info_datestamp_time _ARTICLE_MODIFY_DATE_TIME').text
        except:
            pass

        # news 완성
        news_list[i]['news_reporter'] = news_reporter
        news_list[i]['news_media'] = news_media
        news_list[i]['media_url'] = media_url
        news_list[i]['media_image_src'] = media_image_src
        news_list[i]['timestamp'] = timestamp

        # To-do: 어떤식으로 기사 본문에서 키워드를 추출할 것인가?

        # To-do: 어떤식으로 DB에 전달할 수 있을 것이며 중복을 어떻게 처리할 것인가?

    return news_list
