import sys, os
sys.path.append(os.path.dirname(os.path.abspath(os.path.dirname(os.path.abspath(os.path.dirname(__file__))))))
from modules import crawling
from selenium import webdriver
from selenium.webdriver.chrome.options import Options
from selenium.webdriver.chrome.service import Service
from selenium.webdriver.common.by import By
import time

# 크롤러 함수 작성
def twitter_trend():
   # 환경설정
    options = Options()
    options.add_argument("--no-sandbox")
    options.add_argument("--headless")
    options.add_argument('lang=ko_KR')
    options.add_argument("--disable-dev-shm-usage")
    
    s=Service('chromedriver.exe')
    #s=Service('/usr/src/chrome/chromedriver')
    driver = webdriver.Chrome(options=options, service=s)
    answer = []
    
    query = 'https://twitter.com/i/trends'
    driver.get(query)
    time.sleep(3)
    for i in range(2,22):
        try:
            trend = driver.find_element(By.XPATH,'//*[@id="react-root"]/div/div/div[2]/main/div/div/div/div/div/div[3]/section/div/div/div['+str(i)+']/div/div/div/div/div[2]/span').text
        except:
            trend = -1
        answer.append({'trend':trend})
        time.sleep(0.5)
    print(answer)
  # 드라이버 종료 후 리턴
    driver.quit()
    return answer

if __name__ == "__main__":
    crawling.start_crawling_test("twitter_trend", twitter_trend)
    crawling.print_recent_data(twitter_trend)
    #crawling.start_crawling_hour("twitter_trend",twitter_trend,1)
   