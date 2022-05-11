
# 키워드 추출과 관련된 함수 모듈

# 기사 내용, 기사 제목을 바탕으로 키워드 3개를 추출하는 function
# param: 
# res = 기사 본문이 들어 있는 html 형식의 response
# news_title = 기사 제목
# return: keyword1, keyword2, keyword3
def extract_keywords (res, article_title):

    # Komoran Model: 테스트 상 가장 키워드를 잘 추출하였음
    from konlpy.tag import Komoran
    from collections import Counter

    from black_list import black_list

    article_content = str(res.find('div', 'news_view'))
    komoran = Komoran()

    # article_title로부터 명사 추출
    keyword_from_title = komoran.nouns(article_title)
    # article_content로부터 명사 추출
    keyword_from_content = komoran.nouns(article_content)

    # 제목으로부터 나온 키워드는 2의 가중치를 둠
    # 내용으로부터 나온 키워드는 1의 가중치를 둠
    # 명사가 사용된 빈도수를 계산
    keyword_from_article = keyword_from_title * 2 + keyword_from_content
    keyword_dic = Counter(keyword_from_article)

    sorted_keyword_dic = sorted(keyword_dic.items(), key = lambda item: -item[1])

    # 가장 많이 인용된 명사 중 블랙리스트에 없고 명사의 1글자가 아니라면 기사에 대한 키워드
    # 기사에 대한 키워드 총 3개를 뽑아냄
    limit = 0
    keywords = []
    for keyword, count in sorted_keyword_dic:
        if len(keyword) != 1 and keyword not in black_list:
            keywords.append(keyword)
            count += 1
        if limit == 3:
            break

    try:
        return keywords[0], keywords[1], keywords[2]
    except:
        return '', '', ''

