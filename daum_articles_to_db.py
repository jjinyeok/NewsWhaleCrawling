 
from db_conn import db
from datetime import datetime
from daum_articles import extract_article_from_daum

# 다음 메인뉴스로부터 뉴스 반환
article_list = extract_article_from_daum()
# db_conn에 설정한 설정정보로부터 db 연결
db = db
# cursor 생성
cursor = db.cursor()

# article INSERT
article_insert_sql = """
    INSERT IGNORE INTO article (article_title, article_reporter, article_url, article_media_name, article_media_url, article_media_image_src, article_last_modified_date)
    VALUES (%s, %s, %s, %s, %s, %s, %s)
"""
article_insert_val = []
for article in article_list:
    article_insert_val.append((article['article_title'],
        article['article_reporter'],
        article['article_url'],
        article['article_media_name'],
        article['article_media_url'],
        article['article_media_image_src'],
        article['article_last_modified_date']
    ))
cursor.executemany(article_insert_sql, article_insert_val)

# keyword INSERT
keyword_insert_sql = """
    INSERT IGNORE INTO keyword (keyword_name, politics_count, economy_count, society_count, culture_count, international_count, local_count, sports_count, it_science_count)
    VALUES (%s, 0, 0, 0, 0, 0, 0, 0, 0)
"""
keyword_insert_val = []
for article in article_list:
    keyword_insert_val.append((article['keyword1'])),
    keyword_insert_val.append((article['keyword2'])),
    keyword_insert_val.append((article['keyword3'])),
cursor.executemany(keyword_insert_sql, keyword_insert_val)

# article_keyword INSERT
article_keyword_insert_sql = """
    INSERT INTO article_keyword (article_id, keyword_id)
    VALUES (%s, %s)
"""
article_keyword_insert_val = []
for article in article_list:
    article_select_sql = """
        SELECT article_id
        FROM article
        WHERE article_title=%s
    """
    cursor.execute(article_select_sql, article['article_title'])
    article_id = cursor.fetchall()
    keyword_select_sql = """
        SELECT keyword_id
        FROM keyword
        WHERE keyword_name=%s
    """
    cursor.execute(keyword_select_sql, article['keyword1'])
    keyword_id1 = cursor.fetchall()
    cursor.execute(keyword_select_sql, article['keyword2'])
    keyword_id2 = cursor.fetchall()
    cursor.execute(keyword_select_sql, article['keyword3'])
    keyword_id3 = cursor.fetchall()
    article_keyword_insert_val.append((article_id[0], keyword_id1[0]))
    article_keyword_insert_val.append((article_id[0], keyword_id2[0]))
    article_keyword_insert_val.append((article_id[0], keyword_id3[0]))
cursor.executemany(article_keyword_insert_sql, article_keyword_insert_val)
db.commit()
db.close()

print("Daum articles to DB time :", datetime.now())
