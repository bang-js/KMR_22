from selenium import webdriver
from selenium.webdriver.common.keys import Keys
from selenium.webdriver.common.by import By
from selenium.webdriver.support.ui import WebDriverWait
from selenium.webdriver.support import expected_conditions as EC
from selenium.webdriver.common.alert import Alert
import time
import pandas as pd
import os

######
# 종목 읽어오기
######
df = pd.read_csv('KOSPI.csv',  encoding='cp949')
stocks = df['종목명'].to_list()

######
# 부정단어 사전 읽기
######
# 1차 부정 단어
df_n_word = pd.read_csv('최종_2_부정단어사전.csv')
n_words_lst = df_n_word['단어'].to_list()
print("n_words 수", len(n_words_lst))

# ESG 논란 관련 단어
Ewords = '환경법, 환경보전법, 환경부, 배출, 미세먼지, 오염, 대기오염, 수질오염, 토지오염, 매립, 폐기물, 폐수'.split(', ')
Swords = '폭발, 누출, 화재, 개인정보, 보안, 우롱, 사기, 제품, 품질, 리콜, 장애, 안정성, 독성, 유해, 허위광고, 착취, 아동착취, 성폭력, 성차별, 독점, 담합, 골목, 상권, 불공정, 반경쟁, 일감, 협력사, 하도급, 계열사, 내부거래, 과로, 근로환경, 와해, 사찰, 도청, 파견, 산재, 산업안전, 파업, 구조조정, 해고, 퇴직, 임금, 작업환경, 성과급'.split(', ')
Gwords = '불공정거래, 시세조종, 주가조작, 미공개정보, 내부거래, 내부자거래, 부정거래, 보고의무, 공시의무, 리베이트, 물적분할, 분식회계, 낙하산, 부실경영, 성과급, 보수, 부정채용, 채용비리, 로비, 리베이트, 뇌물, 횡령, 배임, 포탈, 탈세, 추징, 접대, 청탁, 정치자금, 정치 자금, 금품, 뒷돈, 비자금, 비리, 투약, 갑질, 국정농단, 경영권, 경영진, 이사진, 임원, 지배구조'.split(', ')
n_words_lst.extend(Ewords)
n_words_lst.extend(Swords)
n_words_lst.extend(Gwords)

# 중복제거 후 하나의 문자열로 결합
n_words_lst = list(set(n_words_lst))
print(len(n_words_lst))
n_words = ", ".join(n_words_lst)


######
# 자동 검색 및 다운로드
######
options = webdriver.ChromeOptions()
options.add_experimental_option("excludeSwitches", ["enable-logging"])
browser = webdriver.Chrome(options=options)
browser.get("https://www.bigkinds.or.kr/v2/news/index.do")

# 로그인
browser.find_element_by_xpath('//*[@id="header"]/div[1]/div/div[2]/button[1]').click()
browser.find_element_by_xpath('//*[@id="login-user-id"]').send_keys("ID")
time.sleep(1) 
browser.find_element_by_xpath('//*[@id="login-user-password"]').send_keys("PASSWORD") 
time.sleep(1)
browser.find_element_by_xpath('//*[@id="login-btn"]').click()

# # 뉴스검색분석 클릭
# browser.find_element_by_xpath('//*[@id="header"]/div[2]/div[2]/div[1]/div/div[1]/div/ul/li[1]').click()
# browser.find_element_by_xpath('//*[@id="header"]/div[2]/div[2]/div[1]/div/div[2]/div/div[1]/ul/li[1]').click()

# 종목별 검색
for i in stocks :
    # 기간클릭
    browser.find_element_by_xpath('//*[@id="collapse-step-1-body"]/div[3]/div/div[1]/div[1]').click()
    time.sleep(0.5)

    # 시작날짜 입력
    elem = browser.find_element_by_xpath('//*[@id="search-begin-date"]')
    elem.click()
    elem.send_keys(Keys.CONTROL, 'a')
    elem.send_keys("2012-01-01") 	

    # 종료날짜 입력
    elem = browser.find_element_by_xpath('//*[@id="search-end-date"]')
    elem.click()
    elem.send_keys(Keys.CONTROL, 'a')
    elem.send_keys("2021-12-31") 	
    time.sleep(0.5)

    # 통합분류 : "경제/사회"만 설정, 금융_재테크, 증권_증시 제외
    browser.find_element_by_xpath('//*[@id="collapse-step-1-body"]/div[3]/div/div[2]/div[1]/a').click() # 통합분류
    time.sleep(0.5) 
    browser.find_element_by_xpath('//*[@id="srch-tab3"]/ul/li[2]/div/span[3]/label').click() # 경제 체크
    time.sleep(0.5)
    browser.find_element_by_xpath('//*[@id="srch-tab3"]/ul/li[2]/div/span[2]').click() # 경제 열기
    time.sleep(0.5)
    browser.find_element_by_xpath('//*[@id="srch-tab3"]/ul/li[2]/ul/li[3]/div/span[3]/label').click() # 금융_재테크 해제
    time.sleep(0.5)
    browser.find_element_by_xpath('//*[@id="srch-tab3"]/ul/li[2]/ul/li[10]/div/span[3]/label').click() # 증권_증시 해제
    time.sleep(0.5)
    browser.find_element_by_xpath('//*[@id="srch-tab3"]/ul/li[3]/div/span[3]/label').click() # 사회 체크
    time.sleep(0.5)

    # 상세검색 클릭
    browser.find_element_by_xpath('//*[@id="collapse-step-1-body"]/div[3]/div/div[3]/div[1]').click()
    time.sleep(0.5)

    # 검색어 처리 클릭 후 "형태소"에서 "바이그램"으로 변경
    search_pr = browser.find_element_by_xpath('//*[@id="search-filter-type"]')
    search_pr.click()
    search_pr.send_keys(Keys.DOWN)

    # 검색어범위 클릭 후 "제목+본문"에서 "제목"으로 설정
    search_range = browser.find_element_by_xpath('//*[@id="search-scope-type"]')
    search_range.click() # 검색어 범위 클릭 (제목+본문, 제목, 본문)
    search_range.send_keys(Keys.DOWN) # 아래(=제목)

    # 찾고자하는 단어 입력
    search_1 = browser.find_element_by_xpath('//*[@id="orKeyword1"]')  #단어중한개이상포함 
    search_1.send_keys(n_words) # 부정단어 및 ESG논란단어 list
    time.sleep(5)
    search_3 = browser.find_element_by_xpath('//*[@id="exactKeyword1"]') #정확히일치하는단어 
    search_3.click()
    search_3.send_keys(i)

    # 검색 클릭
    browser.find_element_by_xpath('//*[@id="detailSrch1"]/div[7]/div/button[2]').click()

    # 로딩 대기
    element = WebDriverWait(browser, 10).until(EC.presence_of_all_elements_located( \
    (By.XPATH, '//*[@id="dataResult-news"]/a') ))

    # 분석 결과 클릭
    browser.find_element_by_xpath('//*[@id="collapse-step-3"]').click()
    time.sleep(5)
  
    # 엑셀 다운로드 클릭
    browser.find_element_by_xpath('//*[@id="analytics-data-download"]/div[3]/button').click()

    # 2만건 이상 다운로드 시 팝업창 뜸
    try :
        WebDriverWait(browser,3).until(EC.alert_is_present())
        da = Alert(browser)
        da.accept()
        time.sleep(20)
    except :
        pass  
    
    time.sleep(45) # 다운로드대기

    # 파일명 변경
    df = pd.read_excel('Downloads/NewsResult_20120101-20211231.xlsx', engine='openpyxl')
    if i in df.iloc[0]['제목'] :
        file_oldname = os.path.join("Downloads", "NewsResult_20120101-20211231.xlsx")
        file_newname_newfile = os.path.join("Downloads", "{}.xlsx".format(i))
        os.rename(file_oldname, file_newname_newfile)

    #새로고침
    browser.refresh()

######
# 파일명 변경
######
for k in range(len(stocks)):
    file_oldname = os.path.join("파일명", "NewsResult_20120101-20211231 ({}).xlsx".format(k)) 
    file_newname_newfile = os.path.join("파일명", "{}.xlsx".format(stocks[k]))
    os.rename(file_oldname, file_newname_newfile)

