# cd demo
# source bin/activate
# cd ..
# DB 관련 외부 라이브러리
import pymysql

# DB와 연결
db = pymysql.connect(host='demo.csfp9hcywqnb.ap-northeast-2.rds.amazonaws.com',
                        user='fun2314',
                        password='12345678',
                        db='demo',
                        charset='utf8',
                        port=3306
                    )
cursor = db.cursor()

# 데이터 입력. list 형 데이터 
insert_data = [['raul', 10], ['zidane', 7], ['ronaldo', 9]] 
insert_sql = "INSERT INTO `people` VALUES (%s, %s);" 
cursor.executemany(insert_sql, insert_data) 
db.commit()


cursor.execute("SELECT * FROM news;")
result = cursor.fetchall()
for article in result:
    print(article)
db.commit()