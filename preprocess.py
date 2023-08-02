import pandas as pd
import numpy as np

# 부정 단어 모음
df_n_word = pd.read_csv('최종_2_부정단어사전.csv')
n_words = df_n_word['단어'].to_list()
Ewords = '환경법, 환경보전법, 환경부, 배출, 미세먼지, 오염, 대기오염, 수질오염, 토지오염, 매립, 폐기물, 폐수'.split(', ')
Swords = '폭발, 누출, 화재, 개인정보, 보안, 우롱, 사기, 제품, 품질, 리콜, 장애, 안정성, 독성, 유해, 허위광고, 착취, 아동착취, 성폭력, 성차별, 독점, 담합, 골목, 상권, 불공정, 반경쟁, 일감, 협력사, 하도급, 계열사, 내부거래, 과로, 근로환경, 와해, 사찰, 도청, 파견, 산재, 산업안전, 파업, 구조조정, 해고, 퇴직, 임금, 작업환경, 성과급'.split(', ')
Gwords = '불공정거래, 시세조종, 주가조작, 미공개정보, 내부거래, 내부자거래, 부정거래, 보고의무, 공시의무, 리베이트, 물적분할, 분식회계, 낙하산, 부실경영, 성과급, 보수, 부정채용, 채용비리, 로비, 리베이트, 뇌물, 횡령, 배임, 포탈, 탈세, 추징, 접대, 청탁, 정치자금, 정치 자금, 금품, 뒷돈, 비자금, 비리, 투약, 갑질, 국정농단, 경영권, 경영진, 이사진, 임원, 지배구조'.split(', ')
n_words.extend(Ewords)
n_words.extend(Swords)
n_words.extend(Gwords)
print(len(n_words))

# 긍정 및 무의미 단어 모음
p_words = "석방, 영장 기각, 무죄, 무혐의, 불기소, 기부, 협약, 구축, 무공해, 친환경, 출범, 초청, 지원, 개최, 어린이, 행사, 무료, 본격화, 최우수, 1위, 선정, 종목, 급상승, 급락, 반등, 목표가, 증시, 투자뉴스, Hot, 특징주, 신저가, 약세, 로봇뉴스, 마켓, 급락, 코스피, 실적, 사진, 포토, 사설, 부고, 공시, 컨콜".split(', ')

# KOSPI 종목 가져오기
df = pd.read_csv('KOSPI.csv',  encoding='cp949')
stocks = df['종목명'].to_list() 

# 지주사(홀딩스) 및 보편적 단어가 기업명에 포함되는 경우 제외
except_list = ['GS', 'LG', 'SK', '롯데지주', '두산', '한화', 'CJ', '두산', 'DB', '대웅', '효성', 'LS', 'DL', '동서', '신세계', '대덕',\
    '코오롱', '현대건설기계', '동양', 'HDC', 'KCC', '넥센', '세아제강지주', '아세아', '케이씨', '웅진', '한라', 'STX', '서연', '디와이',\
        '샘표', '디아이', '유니온', 'KTis', '대창', '동방', '한창', '한진', '한국화장품제조', '대동', '우진', '남성', '신흥', '전방',\
            '선진','진도','보령','신원','우성','만도','국보','한라','대덕','서원','국동','조비','덕성','성안','한창','무학','화신','대현',\
                '경농','세방','혜인','서연','대창','금비','한독','후성','경방', '대교', 'E1', '백산', 'LF', '대상', '세하']
for stock in stocks:
    if '홀딩스' in stock:
        except_list.append(stock)

# 각 종목의 기사 제목을 크롤링한 excel 파일 불러오기 (except_list에 있는 종목 제외) -> 해당 종목에 대해 기사 제목 데이터를 병합
for i in range(len(stocks)) :
    if i == 0 :
        df = pd.read_excel('{}.xlsx'.format(stocks[i]), engine='openpyxl')
        df['기업'] = stocks[i]
    elif stocks[i] in except_list :
        continue
    else:  
        df_temp = pd.read_excel('{}.xlsx'.format(stocks[i]), engine='openpyxl')
        if df_temp.shape[0] > 0 :
            df_temp['기업'] = stocks[i]
            df = pd.concat([df, df_temp], ignore_index=True)
        else :
            continue
        print(stocks[i])
print(df.shape)

# 기사 제목 중복 시 삭제
df.drop_duplicates(subset=['제목'],inplace=True)

# row index 초기화
df.reset_index(drop=True, inplace=True) 

# 제목에 부정단어가 2번 있는지
lst = []
for i in range(df.shape[0]):
    words_lst = []
    title = df.iloc[i]['제목']
    for n_word in n_words :
        if n_word in title :
            words_lst.append(n_word)
    if len(words_lst) > 0:
        lst.append(len(list(set(words_lst) & set(n_words))))
    else :
        lst.append(0)    
df['n_word'] = lst
df = df[df['n_word'] > 1]
print(df.shape)

# 제목에 긍정 및 무의미 단어가 있는지
lst = []
for i in range(df.shape[0]):
    words_lst = []
    title = df.iloc[i]['제목']
    for p_word in p_words :
        if p_word in title :
            words_lst.append(p_word)
    if len(words_lst) > 0:
        lst.append(len(list(set(words_lst) & set(p_words))))
    else :
        lst.append(0)    
df['p_word'] = lst
df = df[df['p_word'] == 0]

print(df.shape)
df.to_excel('DF_최종_4.xlsx', index=None)
