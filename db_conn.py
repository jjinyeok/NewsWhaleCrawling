import pymysql

# DB와 연결
db = pymysql.connect(host='localhost',
                        user='root',
                        password='12345678',
                        db='news_whale',
                        charset='utf8',
                        port=3306
                    )
