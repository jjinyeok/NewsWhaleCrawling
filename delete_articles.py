
# 7일 전의 기사와 기사_키워드를 삭제
def delete_articles():

    from datetime import datetime
    from datetime import timedelta

    from db_conn import db

    db = db
    cursor = db.cursor()

    # 현재 시각을 기준으로
    now_date = datetime.now().date()
    # 7일 전의 기사를 삭제하기 위해 7일 전 날짜 구함
    seven_date = timedelta(days=7)
    before_seven_days = now_date - seven_date

    # 종속성 관계를 해결하기 위해 (article과 article_keyword 테이블은 Foreign Key로 Mapping되어 있음)
    # 1. 날짜가 지난 기사의 article_id를 구함
    article_select_before_seven_days_sql = """
        SELECT article_id
        FROM article
        WHERE article_last_modified_date<=%s
    """
    cursor.execute(article_select_before_seven_days_sql, before_seven_days)
    article_id_list = cursor.fetchall()

    delete_sql_val = []
    for article_id in article_id_list:
        delete_sql_val.append(article_id[0])


    if len(delete_sql_val) >= 1:
        # 2. article_id를 기반으로 article_keyword 테이블에서 연관관계(aritcle_keyword) 삭제
        article_keyword_delete_sql = """
            DELETE
            FROM article_keyword
            WHERE article_id=%s
        """
        cursor.executemany(article_keyword_delete_sql, delete_sql_val)
        cursor.fetchall()

        # 3. aritlce_id를 기반으로 aritlce 테이블에서 기사(article) 삭제
        article_delete_sql = """
            DELETE
            FROM article
            WHERE article_id=%s
        """
        cursor.executemany(article_delete_sql, delete_sql_val)
        cursor.fetchall()

    db.commit()
