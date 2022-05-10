
# 키워드로 제외되는 명사

black_list = [
    # 보편성 의존명사
    '이', '것', '데', '바', '따위', '분',
    # 주어성 의존명사
    '지', '수', '리', '나위',
    # 서술성 의존명사
    '때문', '나름', '따름', '뿐', '터',
    # 부사성 의존명사
    '만큼', '대로', '듯', '양', '체', '채', '척', '등', '뻔', '만',
    # 단위성 의존명사
    '개', '마리', '장', '권', '켤레', '줄', '몰', '명', '여명', '씨', '전',
    '미터', '킬로그램', '리터', '달러', '칼로리', '쿼터', '바이트', '파스칼', '헤르츠', '데시벨',
    '년', '월', '일', '시', '분', '초', '개월',
    # 경험적 제외 명사
    '.net', '이다', '.com'
]

# 숫자는 키워드로 제외
for i in range(3000):
    if len(str(i)) == 1:
        black_list.append('0' + str(i))
        black_list.append('00' + str(i))
        black_list.append('000' + str(i))
        black_list.append('0000' + str(i))
    elif len(str(i)) == 2:
        black_list.append('0' + str(i))
        black_list.append('00' + str(i))
        black_list.append('000' + str(i))
    elif len(str(i)) == 3:
        black_list.append('0' + str(i))
        black_list.append('00' + str(i))
    black_list.append(str(i))

