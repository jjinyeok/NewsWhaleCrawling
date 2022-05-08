
def delete(db):

    from datetime import datetime
    from datetime import timedelta

    db = db
    cursor = db.cursor()

    now_date = datetime.now().date()

    seven_date = timedelta(days=7)
    before_seven_days = now_date - seven_date

    # 종속성 관계를 해결하기 위함
    # 1. 날짜가 지난 기사의 article_id를 구함
    article_select_before_seven_days_sql = """
        SELECT article_id
        FROM article
        WHERE article_last_modified_date<=%s
    """
    cursor.execute(article_select_before_seven_days_sql, before_seven_days)
    article_id_list = cursor.fetchall()
    # print(lis)

    delete_sql_val = []
    for article_id in article_id_list:
        delete_sql_val.append(article_id[0])


    if len(delete_sql_val) >= 1:
        # 2. article_id를 기반으로 article_keyword 테이블에서 연관관계 삭제
        article_keyword_delete_sql = """
            DELETE
            FROM article_keyword
            WHERE article_id=%s
        """
        cursor.executemany(article_keyword_delete_sql, delete_sql_val)
        cursor.fetchall()

        # 3. aritlce_id를 기반으로 aritlce 테이블에서 기사 삭제
        article_delete_sql = """
            DELETE
            FROM article
            WHERE article_id=%s
        """
        cursor.executemany(article_delete_sql, delete_sql_val)
        cursor.fetchall()

    db.commit()
