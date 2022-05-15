
black_list_in_daum = [
    '뉴스홈',
    '사회',
    '정치',
    '경제',
    '국제',
    '문화',
    'IT',
    '포토',
    '언론사별 뉴스',
    '배열이력',
    '전체뉴스',
    '연재',
    '팩트체크'
]

def init_articles():

    import requests
    from bs4 import BeautifulSoup

    article_list = []
    res = requests.get('https://news.daum.net/', headers={'User-Agent':'Mozilla/5.0'})
    res = BeautifulSoup(res.text, 'html.parser')

    articles_a_tag_in_main_page = res.find_all('a', 'link_txt')
    for article in articles_a_tag_in_main_page:
        #print(article['href'].split('/')[3])
        if article.text not in black_list_in_daum and article['href'].split('/')[3] == 'v':
            article_list.append({'article_title': article.text.strip(), 'article_url': article['href']})
    
    return article_list


def complete_articles(article_list):

    import requests
    from bs4 import BeautifulSoup

    from daum_extract_keywords import extract_keywords

    # 초기화 된 article_json으로부터 article_url을 통해 남은 속성들을 하나씩 완성함
    for i in range(len(article_list)):
        
        # article_json의 article_url을 통해 내용을 response 받음
        res = requests.get(article_list[i]['article_url'], headers={'User-Agent':'Mozilla/5.0'})
        res = BeautifulSoup(res.text, 'html.parser')
        head_view = res.find('div', 'head_view')
        article_reporter = head_view.find('span', 'txt_info').text
        article_media_name = head_view.find('img', 'thumb_g')['alt']
        try:
            article_media_url = head_view.find('a', 'link_cp')['href']
        except:
            # media_url이 존재하지 않는 경우
            article_media_url = ''
        article_media_image_src = head_view.find('img', 'thumb_g')['src']
        article_last_modified_date = ''.join(head_view.find('span', 'num_date').text.split()[0:3])
        
        article_list[i]['article_reporter'] = article_reporter
        article_list[i]['article_media_name'] = article_media_name
        article_list[i]['article_media_url'] = article_media_url
        article_list[i]['article_media_image_src'] = article_media_image_src
        article_list[i]['article_last_modified_date'] = article_last_modified_date

        keyword1, keyword2, keyword3 = extract_keywords(res, article_list[i]['article_title'])
        article_list[i]['keyword1'] = keyword1
        article_list[i]['keyword2'] = keyword2
        article_list[i]['keyword3'] = keyword3

    return article_list
