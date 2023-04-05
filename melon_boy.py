
import time
from selenium import webdriver
from selenium.webdriver.common.keys import Keys
from selenium.webdriver.common.by import By
import re



#모든 페이지의 song id 긁어서 임시 저장
def new_song_id(driver):
    addresslist=[]
    id_list_tmp= []
    keyword_list = ["뉴진스","르세라핌","스트레이키즈","투모로우바이투게더"]
    for keyword in keyword_list:
        for page in range(1,10):
            driver.get("https://www.melon.com/search/song/index.htm?q="+keyword+"&section=artist&searchGnbYn=Y&kkoSpl=Y&kkoDpType=#params%5Bq%5D="+keyword+"&params%5Bsort%5D=hit&params%5Bsection%5D=artist&params%5BsectionId%5D=&params%5BgenreDir%5D=GN2501&&po=pageObj&startIndex="
+str((50 * (page - 1) + 1))) #수정사항: text_emphs 있으면 없애버리기 or while True 때리고 없을 때 까지 찾는것 
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
    driver.close()
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
    
        
def execute():
    id_list = new_song_id()
    id_dict = id_query(id_list)
    
if __name__ == "__main__":
    execute()