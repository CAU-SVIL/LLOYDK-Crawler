import sys, os
sys.path.append(os.path.dirname(os.path.abspath(os.path.dirname(__file__))))
from modules import crawling
from selenium import webdriver
from selenium.webdriver.chrome.options import Options
from selenium.webdriver.chrome.service import Service
from selenium.webdriver.common.by import By
import re
import time

 # 크롤링 코드 넣기
def new_song_id(driver):
    addresslist=[]
    id_list_tmp= []
    keyword_list = ["뉴진스","르세라핌", "엔믹스","아이브","잇지","에스파","블랙핑크","트와이스","아이들","레드벨벳","케플러","스테이시","프로미스나인","이달의소녀","우주소녀",
                    "방탄소년단","스트레이키즈","세븐틴","투모로우바이투게더","NCT127","NCTDREAM","엔하이픈","에이티즈","트레저","더보이즈","갓세븐","몬스타엑스","아스트로","원어스","SF9"]
    for keyword in keyword_list:
        for page in range(1,10):
            driver.get("https://www.melon.com/search/song/index.htm?q="+keyword+"&section=artist&searchGnbYn=Y&kkoSpl=Y&kkoDpType=#params%5Bq%5D="+keyword+"&params%5Bsort%5D=hit&params%5Bsection%5D=artist&params%5BsectionId%5D=&params%5BgenreDir%5D=GN2501&&po=pageObj&startIndex="+str((50 * (page - 1) + 1))) #수정사항: text_emphs 있으면 없애버리기 or while True 때리고 없을 때 까지 찾는것 
            time.sleep(1)
            elems = ""
            elems = driver.find_elements(By.XPATH,'//*[@id="frm_defaultList"]/div/table/tbody/tr/td[3]/div/div/a[1]')
            for i in elems: 
                addresslist.append(i.get_attribute("href"))
            try:
                none= driver.find_element(By.CSS_SELECTOR,'#pageList > div > div > p')
                break
            except:
                continue
        for i in addresslist:
            new = re.sub(r"[^(""\d"")$]","",i)
            n = re.findall(r'\(([^)]+)',i)[1]
            id_list_tmp.append(n.strip("''"))
    return id_list_tmp
#긁어온 id를 query 안에 넣어서 곡, 아티스트, 앨범, 발매일, 장르, 마음수, 어제의 차트 긁기(숫자만)
def id_query(driver, id_list):
        tmp_list = []
        tmp_dict = {}
        index = 0
        for sngid in id_list:
            id = sngid
            query = 'https://www.melon.com/song/detail.htm?songId='+id
            driver.get(query)
            index +=1
            song = driver.find_element(By.CSS_SELECTOR, "#downloadfrm > div > div > div.entry > div.info > div.song_name").text
            artist = driver.find_element(By.CSS_SELECTOR,"#downloadfrm > div > div > div.entry > div.info > div.artist > a").text
            album = driver.find_element(By.CSS_SELECTOR,"#downloadfrm > div > div > div.entry > div.meta > dl > dd:nth-child(2) > a").text
            release = driver.find_element(By.CSS_SELECTOR,"#downloadfrm > div > div > div.entry > div.meta > dl > dd:nth-child(4)").text
            genre = driver.find_element(By.CSS_SELECTOR,"#downloadfrm > div > div > div.entry > div.meta > dl > dd:nth-child(6)").text
            heart = driver.find_element(By.CLASS_NAME,"cnt").text 
            try:
                chart = driver.find_element(By.CLASS_NAME,"chart").text
                chart_num = re.sub(r'[^0-9]', '', chart)
            except:
                chart_num = ""
            tmp_list.append([song,artist,album, release, genre, heart,chart_num])
            tmp_dict[str(index)] = {'song':song,'artist':artist,'album':album,'release':release, 'genre':genre,'heart':heart,'chart_num':chart_num}   
        return tmp_dict
    
    
# 크롤러 함수 작성
def ex_crawling():

  # 환경설정
    options = Options()
    options.add_argument("--no-sandbox")
    options.add_argument("--headless")
    options.add_argument("--disable-dev-shm-usage")

    s=Service('C:/Users/82104/Desktop/crawling/chromedriver_win32/chromedriver.exe')
    driver = webdriver.Chrome(options=options, service=s)
  
  # 크롤링 코드 넣기
    id_list = new_song_id(driver)
    id_dict = id_query(driver, id_list)
  # 드라이버 종료 후 리턴
    driver.quit()
    
    return id_dict

if __name__ == "__main__":
  # 입력 시간 주기로 실행
  crawling.start_crawling_hour("ex_crawling", ex_crawling, 1)
  # 매일 입력 시각에 실행
#crawling.start_crawling_day("ex_crawling", ex_crawling, "14:00")