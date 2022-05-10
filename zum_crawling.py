
# article_list안에 있는 article_json을 초기화하는 function
def init_articles():

    import requests
    from bs4 import BeautifulSoup

    zum_news = 'https://news.zum.com'

    article_list = []
    res = requests.get('https://news.zum.com/?cm=front_gnb')
    res = BeautifulSoup(res.text, 'html.parser')

    articles_a_tag_in_main_page = res.find_all('a', 'item')
    for article in articles_a_tag_in_main_page:
        if article.find('p') != None:
            article_title = article.find('p').text
        elif article.find('h2') != None:
            article_title = article.find('h2').text
        elif article.find('h3') != None:
            article_title = article.find('h3').text

        article_url = article['href']
        article_list.append({'article_title': article_title, 'article_url': zum_news + article_url})
    
    return article_list


# 모든 article_json을 완성하여 article_list를 완성하는 function
def complete_articles(article_list):

    import requests
    from bs4 import BeautifulSoup

    from zum_extract_keywords import extract_keywords

    # 초기화 된 article_json으로부터 article_url을 통해 남은 속성들을 하나씩 완성함
    for i in range(len(article_list)):
        
        # article_json의 article_url을 통해 내용을 response 받음
        res = requests.get(article_list[i]['article_url'])
        res = BeautifulSoup(res.text, 'html.parser')

        head_view = res.find('header', 'article_header')
        try:
            article_reporter = head_view.find('span', 'author').find.text
        except:
            article_reporter = ''
        article_media_name = head_view.find('ul', 'article_info').find('a', 'media').text
        article_media_url = head_view.find('ul', 'article_info').find('a', 'media')['href']
        article_media_image_src = head_view.find('p', 'media_logo').find('img')['src']
        article_last_modified_date = head_view.find('dl', 'time').find_all('dd')[-1].text

        article_list[i]['article_reporter'] = article_reporter
        article_list[i]['article_media_name'] = article_media_name
        article_list[i]['article_media_url'] = article_media_url
        article_list[i]['article_media_image_src'] = article_media_image_src
        article_list[i]['article_last_modified_date'] = article_last_modified_date.split()[0]

        keyword1, keyword2, keyword3 = extract_keywords(res, article_list[i]['article_title'])
        article_list[i]['keyword1'] = keyword1
        article_list[i]['keyword2'] = keyword2
        article_list[i]['keyword3'] = keyword3

    return article_list
