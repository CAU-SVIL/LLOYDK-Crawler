import sys, os
sys.path.append(os.path.dirname(os.path.abspath(os.path.dirname(__file__))))
from modules import crawling
from selenium import webdriver
from selenium.webdriver.chrome.options import Options
from selenium.webdriver.chrome.service import Service


# 크롤러 함수 작성
def ex_crawling():

  # 환경설정
  options = Options()
  options.add_argument("--no-sandbox")
  options.add_argument("--headless")
  options.add_argument("--disable-dev-shm-usage")

  s=Service('/usr/src/chrome/chromedriver')
  driver = webdriver.Chrome(options=options, service=s)
  
  # 크롤링 코드 넣기
  driver.get("https://google.com")
  data = "wow, this is " + driver.title + "!!!"

  # 드라이버 종료 후 리턴
  driver.quit()
  
  return data

if __name__ == "__main__":
  # 입력 시간 주기로 실행
  # crawling.start_crawling_hour("ex_crawling", ex_crawling, 1)
  # 매일 입력 시각에 실행
  crawling.start_crawling_day("ex_crawling", ex_crawling, "14:00")
