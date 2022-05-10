import pymysql

# DB와 연결
db = pymysql.connect(host='demo.csfp9hcywqnb.ap-northeast-2.rds.amazonaws.com',
                        user='fun2314',
                        password='12345678',
                        db='demo',
                        charset='utf8',
                        port=3306
                    )
