import time
start = time.time()

from extract_article_from_naver import extract_article_from_naver

# 네이버 랭킹뉴스로부터 뉴스 반환
article_list = extract_article_from_naver()

print("time :", time.time() - start)  # 현재시각 - 시작시간 = 실행 시간