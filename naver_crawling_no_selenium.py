
def init_articles():

    import requests
    from bs4 import BeautifulSoup
    res = requests.get('https://news.naver.com/main/ranking/popularDay.naver',  headers={'User-Agent':'Mozilla/5.0'})
    res = BeautifulSoup(res.text, 'html.parser')

    article_list = []
    articles_a_tag_in_main_page = res.find_all('a', 'list_title')
    
    for article in articles_a_tag_in_main_page:
        article_list.append({'article_title': article.text.strip(), 'article_url': article['href']})
    
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
            article_reporter = ''

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

        # print(article_list[i])

    return article_list

