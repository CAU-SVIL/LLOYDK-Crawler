import sys, os
sys.path.append(os.path.dirname(os.path.abspath(os.path.dirname(__file__))))
#from modules import crawling
from selenium import webdriver
from selenium.webdriver.chrome.options import Options
from selenium.webdriver.chrome.service import Service
from selenium.webdriver.common.by import By
from selenium.common.exceptions import NoSuchElementException
import re
import time

 # 크롤링 코드 넣기
def new_song_id(driver):
    addresslist=[]
    id_list_tmp= []
    keyword_list = ["피프티피프티"]
    for keyword in keyword_list:
        for page in range(1,6):
            driver.get("https://www.melon.com/search/song/index.htm?q="+keyword+"&section=artist&searchGnbYn=Y&kkoSpl=Y&kkoDpType=#params%5Bq%5D="+keyword+"&params%5Bsort%5D=hit&params%5Bsection%5D=artist&params%5BsectionId%5D=&params%5BgenreDir%5D=GN2501&&po=pageObj&startIndex="+str((50 * (page - 1) + 1))) #수정사항: text_emphs 있으면 없애버리기 or while True 때리고 없을 때 까지 찾는것 
            try: 
                time.sleep(3)
                elems = driver.find_elements(By.XPATH,'//*[@id="frm_defaultList"]/div/table/tbody/tr/td[3]/div/div/a[1]')
                if (elems == []):
                    pass
            except:
                pass
            for i in elems: 
                addresslist.append(i.get_attribute("href"))
            try:
                none= driver.find_element(By.CSS_SELECTOR,'#pageList > div > div > p')
                break
            except NoSuchElementException:
                continue
        print(keyword)
    for i in addresslist:
        new = re.sub(r"[^(""\d"")$]","",i)
        n = re.findall(r'\(([^)]+)',i)[1]
        id_list_tmp.append(n.strip("''"))
    return id_list_tmp 
#긁어온 id를 query 안에 넣어서 곡, 아티스트, 앨범, 발매일, 장르, 마음수, 어제의 차트 긁기(숫자만)
def id_query(driver, id_list):
        tmp_list = []
        for sngid in id_list:
            id = sngid
            query = 'https://www.melon.com/song/detail.htm?songId='+id
            driver.get(query)
            try:
                song = driver.find_element(By.CSS_SELECTOR, "#downloadfrm > div > div > div.entry > div.info > div.song_name").text
            except:
                song = -1
            try:
                artist = driver.find_element(By.CSS_SELECTOR,"#downloadfrm > div > div > div.entry > div.info > div.artist > a").text
            except:
                artist = -1
            try:
                album = driver.find_element(By.CSS_SELECTOR,"#downloadfrm > div > div > div.entry > div.meta > dl > dd:nth-child(2) > a").text
            except:
                album = -1
            try:
                release = driver.find_element(By.CSS_SELECTOR,"#downloadfrm > div > div > div.entry > div.meta > dl > dd:nth-child(4)").text
            except:
                release = -1
            try:
                genre = driver.find_element(By.CSS_SELECTOR,"#downloadfrm > div > div > div.entry > div.meta > dl > dd:nth-child(6)").text
            except:
                genre = -1
            try:
                heart = driver.find_element(By.CLASS_NAME,"cnt").text 
            except:
                heart = -1
            try:
                chart = driver.find_element(By.CLASS_NAME,"chart").text
                chart_num = re.sub(r'[^0-9]', '', chart)
            except:
                chart_num = -1
            tmp_list.append({'song':song,'artist':artist,'album':album,'release':release, 'genre':genre,'heart':heart,'chart_num':chart_num} )
        return tmp_list
    
    
# 크롤러 함수 작성
def ex_crawling():

  # 환경설정
    options = Options()
    options.add_argument("--no-sandbox")
    options.add_argument("--headless")
    options.add_argument('lang=ko_KR')
    options.add_argument("--disable-dev-shm-usage")

    s=Service('C:/Users/82104/Desktop/crawling/chromedriver_win32/chromedriver.exe')
    driver = webdriver.Chrome(options=options, service=s)
    id_list = new_song_id(driver)
    db_list = id_query(driver, id_list)
  # 드라이버 종료 후 리턴
    driver.quit()
    
    return db_list

if __name__ == "__main__":
  # 입력 시간 주기로 실행
  print(ex_crawling())
#crawling.start_crawling_hour("ex_crawling", ex_crawling, 24)
  # 매일 입력 시각에 실행
#crawling.start_crawling_day("ex_crawling", ex_crawling, "14:00")