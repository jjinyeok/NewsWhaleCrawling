from collections import Counter
from konlpy.tag import Komoran
komoran = Komoran()
list_title = komoran.nouns('[속보]공수처 ''고발사주 의혹'' 윤석열 한동훈 무혐의')
count_list_title = Counter(list_title * 2)

print(count_list_title)