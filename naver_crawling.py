
# 네이버 크롤링과 관련된 함수 모듈

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

# article_list (기사 리스트): article_json (기사 딕셔너리) 들어갈 예정
# article_json:
# {
#     ---DB의 article Table로 이동---
#     "article_title", (기사 제목) O
#     "article_reporter", (기자) △
#     "article_url", (기사 URL) O
#     "article_media_name", (언론사 이름) O
#     "article_media_url", (언론사 URL)O
#     "article_media_image_src", (언론사 이미지 소스) O
#     "article_last_modified_date" (최종수정일자) O
#     ---DB의 article_keyword Table로 이동---
#     "keyword1", (연관키워드 1)
#     "keyword2", (연관키워드 2)
#     "keyword3", (연관키워드 3)
# }

# chrome driver 로드하는 function
# param: null
# return: 로드 된 chrome driver
def set_chrome_driver():

    from selenium import webdriver
    from selenium.webdriver.chrome.service import Service
    from webdriver_manager.chrome import ChromeDriverManager

    chrome_options = webdriver.ChromeOptions()
    driver = webdriver.Chrome(service=Service(ChromeDriverManager().install()), options=chrome_options)
    return driver


# 브라우저(chrome) 닫는 function
# param: set_chrome_driver에서 return 받은 driver
# return: null
def close_browser(driver):
    
    driver.close()


# 맨 마지막까지 기사를 수집하기 위해 최대한으로 기사를 찾아내는 function
# chrome driver를 통해 마지막 기사까지 '다른 언론사 랭킹 더보기'를 click
# param: set_chrome_driver에서 return 받은 driver
# return: null
def find_all_articles (driver):
    
    from selenium.webdriver.common.by import By
    
    while True:
        try:
            # 다른 언론사 랭킹 더보기 <button> 클릭
            driver.find_element(by=By.XPATH, value='//*[@id="wrap"]/div[4]/button').click()
        except:
            break


# article_list안에 있는 article_json을 초기화하는 function
# 기사 제목에서 article_title, article_url 추출해서 article_list (기사 리스트)에 저장 후 반환
# param: set_chrome_driver에서 return 받은 driver
# return: article_list
def init_articles(driver):
    
    from selenium.webdriver.common.by import By

    article_list = []
    # 네이버 랭킹 뉴스 메인 페이지에서 각 뉴스 제목이 들어 있는 <a>로부터 article_title(기사 제목), article_url(기사 url) 받아옴
    # 여기서 받은 article_url을 기반으로 나머지 article_json을 완성함
    articles_a_tag_in_ranking_page = driver.find_elements(by=By.CSS_SELECTOR, value="a.list_title")
    for i in range(len(articles_a_tag_in_ranking_page)):    
        article_list.append({'article_title': articles_a_tag_in_ranking_page[i].text, 'article_url': articles_a_tag_in_ranking_page[i].get_attribute('href')})
    return article_list


# 모든 article_json을 완성하여 article_list를 완성하는 function
# param: init_articles에서 초기화하여 article_title과 article_url만 들어 있는 article_list
# return: 모든 정보가 들어 있는 article_list
def complete_articles(article_list):
    
    import requests
    from bs4 import BeautifulSoup
    from naver_extract_keywords import extract_keywords

    # 초기화 된 article_json으로부터 article_url을 통해 남은 속성들을 하나씩 완성함
    for i in range(len(article_list)):
        # article_json의 article_url을 통해 내용을 response 받음
        res = requests.get(article_list[i]['article_url']).text
        res = BeautifulSoup(res, 'html.parser')
        
        # exception이 없는 경우
        # article_media_list, article_media_url, article_media_image_src
        article_media_name =  res.find('img', 'media_end_head_top_logo_img light_type')['title']
        article_media_url = res.find('a', 'media_end_head_top_logo')['href']
        article_media_image_src = res.find('img', 'media_end_head_top_logo_img light_type')['src']

        # exception이 있는 경우
        # article_reporter
        # 간혹 속보 같은 경우, article_reporter가 없는 상태로 기사 나옴
        try:
            article_reporter = res.find('span', 'byline_s').text
        except:
            article_reporter = '기자 없음'

        # exception이 있는 경우
        # article_last_modified_date
        # media_end_head_info_datestamp_date _ARTICLE_MODIFY_DATE_TIME가 없다면 (= 수정된 적이 없다면) 
        # media_end_head_info_datestamp_date _ARTICLE_DATE_TIME가 article_last_modified_date가 됨
        try:
            article_last_modified_date = res.find('span', 'media_end_head_info_datestamp_time _ARTICLE_DATE_TIME').text
            article_last_modified_date = res.find('span', 'media_end_head_info_datestamp_time _ARTICLE_MODIFY_DATE_TIME').text
        except:
            pass

        # extract_keyword 함수 호출
        # res = 기사 내용, article_list[i]['article_title'] = 기사 제목, article_media_name = 언론사
        keyword1, keyword2, keyword3 = extract_keywords(res, article_list[i]['article_title'], article_media_name)

        # 하나의 article_json 완성
        article_list[i]['article_reporter'] = article_reporter
        article_list[i]['article_media_name'] = article_media_name
        article_list[i]['article_media_url'] = article_media_url
        article_list[i]['article_media_image_src'] = article_media_image_src
        article_list[i]['article_last_modified_date'] = article_last_modified_date.split()[0]
        article_list[i]['keyword1'] = keyword1
        article_list[i]['keyword2'] = keyword2
        article_list[i]['keyword3'] = keyword3

        print(article_list[i])

    return article_list

