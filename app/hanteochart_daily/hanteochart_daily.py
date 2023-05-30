import sys, os
sys.path.append(os.path.dirname(os.path.abspath(os.path.dirname(os.path.abspath(os.path.dirname(__file__))))))
from modules import crawling
from selenium import webdriver
from selenium.webdriver.chrome.options import Options
from selenium.webdriver.chrome.service import Service
from selenium.webdriver.common.by import By
from selenium.common.exceptions import NoSuchElementException

def get_cards(dv, cards_info):
	cards = dv.find_elements(By.CSS_SELECTOR, ".chart-item.rank-data.single-col.double-stat.long")
	for c in cards:
		artist = c.find_element(By.CSS_SELECTOR, ".center > div > .bottom > .left").text
		album = c.find_element(By.CSS_SELECTOR, ".center > div > .top").text
		sales = c.find_element(By.CSS_SELECTOR, ".right > div > .left").text
		album_index = c.find_element(By.CSS_SELECTOR, ".right > div > .right").text
		cards_info.append({
			"artist": artist,
			"album": album,
			"sales": sales,
			"album_index": album_index
		})


def see_more(dv):
	try:
		btn = dv.find_element(By.CLASS_NAME, "see-more-btn")
		btn.click()
		return True
	except NoSuchElementException:
		return False


# 크롤러 함수 작성
def hanteochart_daily():

  # 환경설정
  options = Options()
  options.add_argument("--no-sandbox")
  options.add_argument("--headless")
  options.add_argument("--disable-dev-shm-usage")

  s=Service('/usr/src/chrome/chromedriver')
  driver = webdriver.Chrome(options=options, service=s)
  
  # 크롤링 코드 넣기
  driver.get("https://www.hanteochart.com/chart/album/daily")

  cards_info = list()
  has_more = True
  while has_more:
    has_more = see_more(driver)

  get_cards(driver, cards_info)

  for card in cards_info:
    print(card)
	
  # 드라이버 종료 후 리턴
  driver.quit()
  
  return cards_info

if __name__ == "__main__":
  crawling.start_crawling_day("hanteochart_daily", hanteochart_daily, "00:30")
