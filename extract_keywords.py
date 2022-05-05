
# 키워드 추출과 관련된 함수 모듈

# 기사 내용, 기사 제목을 바탕으로 키워드 3개를 추출하는 function
# param: 
# res = 기사 본문이 들어 있는 html 형식의 response
# news_title = 기사 제목
# news_media = 언론사 (영어 기사 같은 경우, 키워드를 추출할 수 없어 키워드 '영어 기사'로 통일)
# return: keyword1, keyword2, keyword3
def extract_keywords (res, article_title, article_media_name):

    # Komoran Model: 테스트 상 가장 키워드를 잘 추출하였음
    from konlpy.tag import Komoran
    from collections import Counter

    from black_list import black_list

    article_content = str(res.find('div', id='dic_area'))
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

    # 영어 기사인 경우, Komoran으로는 키워드를 추출할 수 없고, 사용자들이 원할 가능성이 적기 때문에 '영어 기사'라는 키워드로 대체
    if article_media_name == '코리아헤럴드' or article_media_name == '코리아중앙데일리':
        return '영어 기사', '영어 기사', '영어 기사'

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

    return keywords[0], keywords[1], keywords[2]

