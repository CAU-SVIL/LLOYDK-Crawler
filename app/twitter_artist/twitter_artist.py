import sys, os
sys.path.append(os.path.dirname(os.path.abspath(os.path.dirname(os.path.abspath(os.path.dirname(__file__))))))
from modules import crawling
from selenium import webdriver
from selenium.webdriver.chrome.options import Options
from selenium.webdriver.chrome.service import Service
from selenium.webdriver.common.by import By
#import re
import time

# 크롤러 함수 작성
def twitter_artist():
   # 환경설정
    options = Options()
    options.add_argument("--no-sandbox")
    options.add_argument("--headless")
    options.add_argument('lang=ko_KR')
    options.add_argument("--disable-dev-shm-usage")
    
    #s=Service('chromedriver.exe')
    s=Service('/usr/src/chrome/chromedriver')
    driver = webdriver.Chrome(options=options, service=s)
    answer = []
    artist_list = ["뉴진스",
                   "르세라핌", 
                   "엔믹스",
                   "아이브",
                   "있지",
                   "에스파",
                   "블랙핑크",
                   "트와이스",
                   "아이들",
                   "레드벨벳",
                   "케플러",
                   "스테이씨",
                   "프로미스나인",
                   "이달의소녀",
                   "우주소녀",
                   "보이즈플래닛",
                   "방탄소년단",
                   "스트레이키즈",
                   "세븐틴",
                   "투모로우바이투게더",
                   "NCT127",
                   "NCTDREAM",
                   "엔하이픈",
                   "에이티즈",
                   "트레저",
                   "더보이즈",
                   "갓세븐",
                   "몬스타엑스",
                   "아스트로",
                   "원어스",
                   "SF9"]
    id_list = ['le_sserafim',
                   'NewJeans_ADOR',
                   'NMIXX_official',
                   'IVEstarship',
                   'ITZYOfficial',
                   'aespa_official',
                   'blackpink',
                   'JYPETWICE',
                   'G_I_DLE',
                   'RVsmtown',
                   'official_kep1er',
                   'STAYC_official',
                   'realfromis_9',
                   'loonatheworld',
                   'WJSN_Cosmic',
                   'ZB1_official',
                   'Stray_Kids',
                   'pledis_17',
                   'TXT_bighit',
                   'NCTsmtown_127',
                   'NCTsmtown_DREAM',
                   'ENHYPEN',
                   'ATEEZofficial',
                   'ygtreasuremaker',
                   'IST_THEBOYZ',
                   'GOT7',
                   'OfficialMonstaX',
                   'offclASTRO',
                   'official_ONEUS',
                   'SF9official']
    for artist, id in zip(artist_list, id_list):
      query = 'https://twitter.com/'+id
      driver.get(query)
      time.sleep(5)
      try:
        fllwrs = driver.find_element(By.XPATH,'//*[@id="react-root"]/div/div/div[2]/main/div/div/div/div/div/div[3]/div/div/div/div/div[5]/div[2]/a/span[1]/span').text
      except:
        fllwrs = -1
      answer.append({'artist':artist,'fllwrs':fllwrs})
      time.sleep(5)
      print(artist, fllwrs)

  # 드라이버 종료 후 리턴
    driver.quit()
    return answer

if __name__ == "__main__":
   crawling.start_crawling_test("twitter_artist", twitter_artist)
   crawling.print_recent_data("twitter_artist")