
def extract_article_from_daum():

    from daum_crawling import init_articles
    from daum_crawling import complete_articles

    article_list = complete_articles(init_articles())

    return article_list
