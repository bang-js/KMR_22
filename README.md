# KMR_22
[Korean Management Review, 2022] ESG controversises and stock market returns: using a natural language processing

## bigkinds_scrap
1. 1차 부정 단어와 ESG 논란 관련 단어 통합
2. selenium을 사용하여 BIGKINDS에서 각 주식 종목에 대하여 해당 단어 모음을 자동으로 검색하고 결과를 엑셀 파일로 다운로드
3. 다운로드된 엑셀 파일명을 일괄적으로 변경

## preprocess
1. 부정 단어 모음, 긍정 및 무의미 단어 모음 정리
2. 지주사(홀딩스) 및 보편적 단어가 기업명에 포함되는 경우 제외
3. 종목들의 기사 제목들을 병합한 데이터프레임에서 기사 제목 중복 시 삭제하고, 제목에 부정단어가 2번 있는지, 제목에 긍정 및 무의미 단어가 있는지 확인
4. 기사 제목 데이터를 엑셀 파일로 저장

analysis_news
anounce
count
news_stock
news_stock_vol (py)
news_stock_vol_t_test (py)
newspaper_url
overlap_week

regression
ror_zero
stock_database
t_test
test
ticker_overlap
vol_temp

##
news_stock_vol (ipynb)
news_stock_vol_no_refine (ipynb)
news_stock_vol_t_test (ipynb)
