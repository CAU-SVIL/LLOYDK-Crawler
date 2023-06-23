import sys, os
sys.path.append(os.path.dirname(os.path.abspath(os.path.dirname(os.path.abspath(os.path.dirname(__file__))))))
from modules import crawling
from selenium import webdriver
from selenium.webdriver.chrome.options import Options
from selenium.webdriver.chrome.service import Service
from selenium.webdriver.common.by import By
import re
import time


# 크롤러 함수 작성
def postype_view():
  # 환경설정
  options = Options()
  options.add_argument("--no-sandbox")
  options.add_argument("--headless")
  options.add_argument("--disable-dev-shm-usage")

  s=Service('/usr/src/chrome/chromedriver')
  driver = webdriver.Chrome(options=options, service=s)
  answer = []
  # 크롤링 코드 넣기
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
                 "마마무",
                 "드림캐쳐",
                 "Weeekly",
                 "Billlie",
                 "VIVIZ",
                 "오마이걸",
                 "브레이브걸스",
                 "퍼플키스",
                 "woo!ah!",
                 "CLASS:y",
                 "로켓펀치",
                 "보이즈플래닛",
                 "백현",
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
                 "SF9",
                 "위아이",
                 "WINNER",
                 "SUPER JUNIOR",
                 "VERIVERY",
                 "P1Harmony",
                 "TEMPEST",
                 "CRAVITY",
                 "비투비",
                 "OMEGA X",
                 "DKZ"
  ]

  for artist in artist_list:
      print(artist)
      query = 'https://www.postype.com/search?keyword='+artist
      driver.get(query)
      time.sleep(5)
      try:
        view = driver.find_element(By.XPATH,'//*[@id="main-content"]/div/div[2]/div[1]/header/div/div').text
        view = re.sub(r'[^0-9]', '', view)
      except:
        view = -1
      print(view)
      answer.append({'artist':artist,'view':view})
      time.sleep(5)

  # 드라이버 종료 후 리턴
  driver.quit()
  
  return answer

if __name__ == "__main__":
  # 입력 시간 주기로 실행
  # crawling.start_crawling_hour("example", example, 1)
  # 매일 입력 시각에 실행
  # crawling.start_crawling_day("example", example, "14:00")
  # 바로 테스트
  crawling.start_crawling_test("postype_view", postype_view)
  crawling.print_recent_data("postype_view")