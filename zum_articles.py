
def extract_article_from_zum():

    import zum_crawling

    article_list = zum_crawling.init_articles()

    article_list = zum_crawling.complete_articles(article_list)

    return article_list
