
# 네이버, 다음, 줌으로부터 매 시각 15분부터 기사를 받아 옴
from naver_articles_to_db import naver_articles_to_db
from daum_articles_to_db import daum_articles_to_db
from zum_articles_to_db import zum_articles_to_db
from delete_articles import delete_articles

# article을 INSERT하기 전에 7일이 지난(오래된) article 삭제
delete_articles()

# NAVER, Daum, Zum으로부터
# article을 Crawling
# article 내용으로부터 keyword 추출
# DB article, article_keyword 테이블에 data 저장
naver_articles_to_db()
daum_articles_to_db()
zum_articles_to_db()
