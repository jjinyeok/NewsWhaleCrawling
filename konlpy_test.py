# Test code 
import requests
from konlpy.tag import Komoran
from collections import Counter

# 의존명사 제외
black_list = [
    # 보편성 의존명사
    '이', '것', '데', '바', '따위', '분',
    # 주어성 의존명사
    '지', '수', '리', '나위',
    # 서술성 의존명사
    '때문', '나름', '따름', '뿐', '터',
    # 부사성 의존명사
    '만큼', '대로', '듯', '양', '체', '채', '척', '등', '뻔', '만',
    # 단위성 의존명사
    '개', '마리', '장', '권', '켤레', '줄', '몰', '명', '여명', '씨', '전',
    '미터', '킬로그램', '리터', '달러', '칼로리', '쿼터', '바이트', '파스칼', '헤르츠', '데시벨',
    '년', '월', '일', '시', '분', '초', '개월'

    
]

for i in range(3000):
    if len(str(i)) == 1:
        black_list.append('0' + str(i))
        black_list.append('00' + str(i))
        black_list.append('000' + str(i))
        black_list.append('0000' + str(i))
    elif len(str(i)) == 2:
        black_list.append('0' + str(i))
        black_list.append('00' + str(i))
        black_list.append('000' + str(i))
    elif len(str(i)) == 3:
        black_list.append('0' + str(i))
        black_list.append('00' + str(i))
    black_list.append(str(i))

def get_keywords (res, news_title, news_media):
    content = str(res.find('div', id='dic_area'))
    komoran = Komoran()

    list_title = komoran.nouns(news_title)
    count_list_title = Counter(list_title * 2)

    list_article = komoran.nouns(content)

    count_list_article = Counter(list_article)

    count_list = count_list_title + count_list_article
    sorted_count_list = sorted(count_list.items(), key = lambda item: -item[1])

    if news_media == '코리아헤럴드' or news_media == '코리아중앙데일리':
        return '영어기사', '영어기사', '영어기사'

    count = 0
    keywords = []
    for i, c in sorted_count_list:
        if len(i) != 1 and i not in black_list:
            keywords.append(i)
            count += 1
        if count == 3:
            break

    #print(keywords)
    return keywords[0], keywords[1], keywords[2]

#res = requests.get(url).text
#res = BeautifulSoup(res, 'html.parser')
#get_keywords('https://n.news.naver.com/article/016/0001986402')