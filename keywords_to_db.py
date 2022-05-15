from time import sleep
from selenium import webdriver
from selenium.webdriver.chrome.service import Service
from webdriver_manager.chrome import ChromeDriverManager

from selenium.webdriver.common.by import By
from selenium.webdriver.common.keys import Keys
chrome_options = webdriver.ChromeOptions()
chrome_options.headless = True
driver = webdriver.Chrome(service=Service(ChromeDriverManager().install()), options=chrome_options)

from db_conn import db

# db_conn에 설정한 설정정보로부터 db 연결
db = db
# cursor 생성
cursor = db.cursor()

def get_keywords():

    driver.get('https://www.bigkinds.or.kr/')
    sleep(3)
    
    request_body = {}

    # 정치(politics) 분야 키워드
    driver.find_element(by=By.XPATH, value='//*[@id="contents"]/div/section[2]/div[1]/div[2]/div[1]/div[1]/div/div[2]/a').send_keys(Keys.ENTER)
    sleep(1)
    a2 = driver.find_element(by=By.ID, value='keyword2')
    politics = list(a2.text.split())
    politics.remove('인물')
    politics.remove('장소')
    politics.remove('기관')
    politics.remove('다운로드')
    request_body['politics'] = politics

    # 경제(economy) 분야 키워드
    driver.find_element(by=By.XPATH, value='//*[@id="contents"]/div/section[2]/div[1]/div[2]/div[1]/div[1]/div/div[3]/a').send_keys(Keys.ENTER)
    sleep(1)
    a3 = driver.find_element(by=By.ID, value='keyword3')
    economy = list(a3.text.split())
    economy.remove('인물')
    economy.remove('장소')
    economy.remove('기관')
    economy.remove('다운로드')
    request_body['economy'] = economy

    # 사회(society) 분야 키워드
    driver.find_element(by=By.XPATH, value='//*[@id="contents"]/div/section[2]/div[1]/div[2]/div[1]/div[1]/div/div[4]/a').send_keys(Keys.ENTER)
    sleep(1)
    a4 = driver.find_element(by=By.ID, value='keyword4')
    society = list(a4.text.split())
    society.remove('인물')
    society.remove('장소')
    society.remove('기관')
    society.remove('다운로드')
    request_body['society'] = society

    # 문화(culture) 분야 키워드
    driver.find_element(by=By.XPATH, value='//*[@id="contents"]/div/section[2]/div[1]/div[2]/div[1]/div[1]/div/div[5]/a').send_keys(Keys.ENTER)
    sleep(1)
    a5 = driver.find_element(by=By.ID, value='keyword5')
    culture = list(a5.text.split())
    culture.remove('인물')
    culture.remove('장소')
    culture.remove('기관')
    culture.remove('다운로드')
    request_body['culture'] = culture

    # 국제(international) 분야 키워드
    driver.find_element(by=By.XPATH, value='//*[@id="contents"]/div/section[2]/div[1]/div[2]/div[1]/div[1]/div/div[6]/a').send_keys(Keys.ENTER)
    sleep(1)
    a6 = driver.find_element(by=By.ID, value='keyword6')
    international = list(a6.text.split())
    international.remove('인물')
    international.remove('장소')
    international.remove('기관')
    international.remove('다운로드')
    request_body['international'] = international

    # 지역(local) 분야 키워드
    driver.find_element(by=By.XPATH, value='//*[@id="contents"]/div/section[2]/div[1]/div[2]/div[1]/div[1]/div/div[7]/a').send_keys(Keys.ENTER)
    sleep(1)
    a7 = driver.find_element(by=By.ID, value='keyword7')
    local = list(a7.text.split())
    local.remove('인물')
    local.remove('장소')
    local.remove('기관')
    local.remove('다운로드')
    request_body['local'] = local

    # 스포츠(sports) 분야 키워드
    driver.find_element(by=By.XPATH, value='//*[@id="contents"]/div/section[2]/div[1]/div[2]/div[1]/div[1]/div/div[8]/a').send_keys(Keys.ENTER)
    sleep(1)
    a8 = driver.find_element(by=By.ID, value='keyword8')
    sports = list(a8.text.split())
    sports.remove('인물')
    sports.remove('장소')
    sports.remove('기관')
    sports.remove('다운로드')
    request_body['sports'] = sports

    # IT/과학(it_science) 분야 키워드
    driver.find_element(by=By.XPATH, value='//*[@id="contents"]/div/section[2]/div[1]/div[2]/div[1]/div[1]/div/div[9]/a').send_keys(Keys.ENTER)
    sleep(1)
    a9 = driver.find_element(by=By.ID, value='keyword9')
    it_science = list(a9.text.split())
    it_science.remove('인물')
    it_science.remove('장소')
    it_science.remove('기관')
    it_science.remove('다운로드')
    request_body['it_science'] = it_science

    driver.close()

    return request_body

request_body = get_keywords()

keyword_select_sql = """
    SELECT *
    FROM keyword
    WHERE keyword_name=%s
"""

# politics_count UPDATE문
keyword_politics_count_update_sql =  """
    UPDATE keyword
    SET politics_count=%s
    WHERE keyword_name=%s
"""

# economy_count UPDATE문
keyword_economy_count_update_sql =  """
    UPDATE keyword
    SET economy_count=%s
    WHERE keyword_name=%s
"""

# society_count UPDATE문
keyword_society_count_update_sql =  """
    UPDATE keyword
    SET society_count=%s
    WHERE keyword_name=%s
"""

# culture_count UPDATE문
keyword_culture_count_update_sql =  """
    UPDATE keyword
    SET culture_count=%s
    WHERE keyword_name=%s
"""

# international_count UPDATE문
keyword_international_count_update_sql =  """
    UPDATE keyword
    SET international_count=%s
    WHERE keyword_name=%s
"""

# local_count UPDATE문
keyword_local_count_update_sql =  """
    UPDATE keyword
    SET local_count=%s
    WHERE keyword_name=%s
"""

# sports_count UPDATE문
keyword_sports_count_update_sql =  """
    UPDATE keyword
    SET sports_count=%s
    WHERE keyword_name=%s
"""

# it_science_count UPDATE문
keyword_it_science_count_update_sql =  """
    UPDATE keyword
    SET it_science_count=%s
    WHERE keyword_name=%s
"""

# politics_count INSERT문
keyword_politics_count_insert_sql = """
    INSERT INTO keyword (keyword_name, politics_count, economy_count, society_count, culture_count, international_count, local_count, sports_count, it_science_count)
    VALUES (%s, 1, 0, 0, 0, 0, 0, 0, 0)
"""

# economy_count INSERT문
keyword_economy_count_insert_sql = """
    INSERT INTO keyword (keyword_name, politics_count, economy_count, society_count, culture_count, international_count, local_count, sports_count, it_science_count)
    VALUES (%s, 0, 1, 0, 0, 0, 0, 0, 0)
"""

# society_count INSERT문
keyword_society_count_insert_sql = """
    INSERT INTO keyword (keyword_name, politics_count, economy_count, society_count, culture_count, international_count, local_count, sports_count, it_science_count)
    VALUES (%s, 0, 0, 1, 0, 0, 0, 0, 0)
"""

# culture_count INSERT문
keyword_culture_count_insert_sql = """
    INSERT INTO keyword (keyword_name, politics_count, economy_count, society_count, culture_count, international_count, local_count, sports_count, it_science_count)
    VALUES (%s, 0, 0, 0, 1, 0, 0, 0, 0)
"""

# international_count INSERT문
keyword_international_count_insert_sql = """
    INSERT INTO keyword (keyword_name, politics_count, economy_count, society_count, culture_count, international_count, local_count, sports_count, it_science_count)
    VALUES (%s, 0, 0, 0, 0, 1, 0, 0, 0)
"""

# local_count INSERT문
keyword_local_count_insert_sql = """
    INSERT INTO keyword (keyword_name, politics_count, economy_count, society_count, culture_count, international_count, local_count, sports_count, it_science_count)
    VALUES (%s, 0, 0, 0, 0, 0, 1, 0, 0)
"""

# sports_count INSERT문
keyword_sports_count_insert_sql = """
    INSERT INTO keyword (keyword_name, politics_count, economy_count, society_count, culture_count, international_count, local_count, sports_count, it_science_count)
    VALUES (%s, 0, 0, 0, 0, 0, 0, 1, 0)
"""

# it_science_count INSERT문
keyword_it_science_count_insert_sql = """
    INSERT INTO keyword (keyword_name, politics_count, economy_count, society_count, culture_count, international_count, local_count, sports_count, it_science_count)
    VALUES (%s, 0, 0, 0, 0, 0, 0, 0, 1)
"""

for key, keywords in request_body.items():
    for keyword in keywords:
        cursor.execute(keyword_select_sql, keyword)
        sql_result = cursor.fetchone()
        if sql_result != None:
            # keyword가 등록되어 있는 경우 -> update
            if key == 'politics':
                cursor.execute(keyword_politics_count_update_sql, (sql_result[7] + 1, sql_result[5]))
            elif key == 'economy':
                cursor.execute(keyword_economy_count_update_sql, (sql_result[2] + 1, sql_result[5]))
            elif key == 'society':
                cursor.execute(keyword_society_count_update_sql, (sql_result[8] + 1, sql_result[5]))
            elif key == 'culture':
                cursor.execute(keyword_culture_count_update_sql, (sql_result[1] + 1, sql_result[5]))
            elif key == 'international':
                cursor.execute(keyword_international_count_update_sql, (sql_result[3] + 1, sql_result[5]))
            elif key == 'local':
                cursor.execute(keyword_local_count_update_sql, (sql_result[6] + 1, sql_result[5]))
            elif key == 'sports':
                cursor.execute(keyword_sports_count_update_sql, (sql_result[9] + 1, sql_result[5]))
            elif key == 'it_science':
                cursor.execute(keyword_it_science_count_update_sql, (sql_result[4] + 1, sql_result[5]))
        else:
            # keyword가 등록되어 있지 않는 경우 -> insert
            if key == 'politics':
                cursor.execute(keyword_politics_count_insert_sql, keyword)
            elif key == 'economy':
                cursor.execute(keyword_economy_count_insert_sql, keyword)
            elif key == 'society':
                cursor.execute(keyword_society_count_insert_sql, keyword)
            elif key == 'culture':
                cursor.execute(keyword_culture_count_insert_sql, keyword)
            elif key == 'international':
                cursor.execute(keyword_international_count_insert_sql, keyword)
            elif key == 'local':
                cursor.execute(keyword_local_count_insert_sql, keyword)
            elif key == 'sports':
                cursor.execute(keyword_sports_count_insert_sql, keyword)
            elif key == 'it_science':
                cursor.execute(keyword_it_science_count_insert_sql, keyword)

db.commit()
db.close()
