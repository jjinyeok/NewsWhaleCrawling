# cd demo
# source bin/activate
# cd ..
# 크롤링 외부 라이브러리
import naver_crawling

# 네이버 랭킹뉴스 - 언론사별 많이 본 뉴스
naver_ranking_news = 'https://news.naver.com/main/ranking/popularDay.naver'

# chrome 드라이버 로드
driver = naver_crawling.set_chrome_driver()

# 해당 URL을 브라우저(chrome)에서 띄움
driver.get(naver_ranking_news)

# 모든 랭킹기사 보기
naver_crawling.find_all_articles(driver)

# 기사 리스트 초기화
# {기사제목, 기사URL}
articles = naver_crawling.init_articles(driver)

# 브라우저 닫기
naver_crawling.close_browser(driver)

# 기사 리스트 전체 가지고 옴
articles = naver_crawling.complete_articles(articles)

