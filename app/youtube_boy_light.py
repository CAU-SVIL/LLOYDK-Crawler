#!/usr/bin/env python
# coding: utf-8

# In[ ]:


#!/usr/bin/env python
# coding: utf-8

#전체 코드
import sys, os
sys.path.append(os.path.dirname(os.path.abspath(os.path.dirname(__file__))))
from modules import crawling
from selenium import webdriver
from selenium.webdriver.chrome.options import Options
from selenium.webdriver.chrome.service import Service
from selenium.webdriver.common.by import By
import re
import time
#추가라이브러리
from selenium.webdriver.common.keys import Keys
from selenium.webdriver import ActionChains
from bs4 import BeautifulSoup
import requests
import json

def ytb_channel_data_func(driver, channel_name_list):
    
    def scroll():
        try:        
            # 페이지 내 스크롤 높이 받아오기
            last_page_height = driver.execute_script("return document.documentElement.scrollHeight")
            while True:
                # 페이지 최하단까지 스크롤
                driver.execute_script("window.scrollTo(0, document.documentElement.scrollHeight);")
                # 페이지 로딩 대기
                time.sleep(0.05)
                # 무한 스크롤 동작을 위해 살짝 위로 스크롤(i.e., 페이지를 위로 올렸다가 내리는 제스쳐)
                driver.execute_script("window.scrollTo(0, document.documentElement.scrollHeight-50)")
                time.sleep(0.05)
                # 페이지 내 스크롤 높이 새롭게 받아오기
                new_page_height = driver.execute_script("return document.documentElement.scrollHeight")
                # 스크롤을 완료한 경우(더이상 페이지 높이 변화가 없는 경우)
                if new_page_height == last_page_height:
                    print("스크롤 완료")
                    break

                # 스크롤 완료하지 않은 경우, 최하단까지 스크롤
                else:
                    last_page_height = new_page_height

        except Exception as e:
            print("에러 발생: ", e)

    api_key = "AIzaSyAbWnmuhCBOG5JQwUmfj8vUXrcgL6hoxH0" #api key     
    
    ytb_channel_data=[]
    
    try:
        for channel_name in channel_name_list:

            channel_data = {'name': '', 'channel_url': '','date': '', 'total_views':'', 'subscriber': '', 'video_counts': '', 'video_url': []}
           
            #api이용 channel_id 추출해 채널 url 뽑아내기
            url = f"https://www.googleapis.com/youtube/v3/search?key={api_key}&part=id&type=channel&q={channel_name}"
            response = requests.get(url)

            json_data = json.loads(response.text) #json data 로 고유 코드 받아오는 기능

            channel_id=json_data["items"][0]["id"]["channelId"]

            channel_url = "https://www.youtube.com/channel/" + channel_id
            driver.get(channel_url+ "/about")
            driver.implicitly_wait(1.5)
            # 스크롤 다운

            driver.find_element(By.TAG_NAME, 'body').send_keys(Keys.END)

            channel_name = driver.find_element(By.XPATH, '//*[@id="text-container"]').text
            channel_name = re.sub('[=+,#/\?:^$.@*\"※~&%ㆍ!』\\‘|\(\)\[\]\<\>`\'…《\》]', '', channel_name)
            subscribe = driver.find_element(By.CSS_SELECTOR, '#subscriber-count').text
            total_views = driver.find_element(By.XPATH, '//*[@id="right-column"]/yt-formatted-string[3]').text
            channel_date=driver.find_element(By.XPATH, '//*[@id="right-column"]/yt-formatted-string[2]/span[2]').text

            driver.get(channel_url+"/videos")
            driver.implicitly_wait(1.5)
            scroll()

            # bs4 실행    
            html = driver.page_source
            soup = BeautifulSoup(html, 'lxml')

            video_list = soup.find('div', {'id': 'contents'})
            video_list = video_list.find_all('ytd-rich-grid-row', {'class':'style-scope ytd-rich-grid-renderer'})

            base_url = 'http://www.youtube.com'
            video_url = []

            # 반복문을 실행시켜 비디오의 주소를 video_url에 넣는다.
            for i in range(len(video_list)):
                for j in range(len(video_list[i].find_all('a',{'id':'thumbnail'}))):
                    url = base_url+video_list[i].find_all('a',{'id':'thumbnail'})[j]['href']
                    video_url.append(url)
            video_url=list(sorted(set(video_url), key= lambda x: video_url.index(x)))

            #driver.quit()    
            channel_data['name']=channel_name
            channel_data['channel_url']=channel_url
            channel_data['date']=channel_date
            channel_data['subscriber']=subscribe
            channel_data['total_views']=total_views
            channel_data['video_counts']=str(len(video_url))
            channel_data['video_url']=video_url    
            ytb_channel_data.append(channel_data)

    except:
        print("channel_inform_fail")
        
    driver.quit()
#    ytb_channel_data=json.dumps(ytb_channel_data)
    
    return(ytb_channel_data)

def ytb_video_data_func(options, service, video_info, ytb_video_data):
    
    ytb_video_data=[]
    ytb_video_data.append({'title': video_info['name'],'url': video_info['channel_url'], 'date': video_info['date'],
                  'view': video_info['total_views'], 'comment': video_info['subscriber'], 'tag': video_info['video_counts']})
    driver=webdriver.Chrome(options=options, service=service)


    print(video_info['name']+'크롤링 시작')
    start = time.time()

    for video_url in video_info['video_url']: 
        video_data={'title': '','url': video_url, 'date': '', 'view': '', 'comment': '', 'tag': '0'}
        video_error={'title': '-1','url': '-1', 'date': '-1', 'view': '-1', 'comment': '-1', 'tag': '-1'}

        try:
            action=ActionChains(driver)
            driver.get(video_url)
            driver.implicitly_wait(1.5)

            try:
                time.sleep(0.9)
                driver.implicitly_wait(1.5)
                body = driver.find_element(By.TAG_NAME, 'body')
                num_of_pagedowns = 5

                while num_of_pagedowns:
                    driver.implicitly_wait(1.5)
                    body.send_keys(Keys.PAGE_DOWN)
                    driver.implicitly_wait(1.5)
                    num_of_pagedowns -= 1

                try:
                    #제목 추출
                    title=driver.find_element(By.XPATH, '//*[@id="title"]/h1/yt-formatted-string').text
                except:
                    print("제목추출 실패")
                    title="-1"

                try:
                    #댓글 수 추출
                    driver.implicitly_wait(1.5)
                    comment = driver.find_element(By.XPATH, '//*[@id="count"]/yt-formatted-string/span[2]').text.replace(',','')
                    #action.move_to_element(sub0).perform()
                    #sub2 = sub0.text

                except:
                    #print("댓글추출 실패")
                    comment="-1"

                try:
                    #더보기로 이동, 선택
                    action.move_to_element(driver.find_element(By.XPATH, '//*[@id="expand"]')).perform()
                    driver.find_element(By.XPATH, '//*[@id="expand"]').click()

                    try:
                        #날짜 추출
                        day=driver.find_element(By.XPATH, '//*[@id="info"]/span[3]').text

                    except:
                        print("날짜 추출 실패")
                        day="-1"

                    try:
                        #조회수 추출
                        view=re.sub(r'[^0-9]', '', driver.find_element(By.XPATH, '//*[@id="info"]/span[1]').text)

                    except:
                        print("조회수 추출 실패")
                        view="-1"

                except:
                    print("더보기 선택 실패")
                    day="-1"
                    view="-1"
                    
                video_data['date']=day
                video_data['title']=title
                video_data['view']=view
                video_data['comment']=comment
                
                ##### 추후에 제거할 거
                ytb_video_data.append(video_data)

            except Exception as e:
                print("동영상 추출 관련 에러 발생: ", e)
                ytb_video_data.append(video_error)
        
        except Exception as e:
            print("드라이버 연결 관련 에러 발생: ", e)

    driver.quit()
    
    ##############################################
    end = time.time()
    print(str(round((end-start), 3)) + '소요시간')
    print(video_info['name']+'크롤링 종료')
    
#    return(ytb_video_data)

def youtube_boy_light():

  # 환경설정
    options = Options()
    options.add_argument("--no-sandbox")
    options.add_argument("--headless")
    options.add_argument('lang=ko_KR')
    options.add_argument("--disable-dev-shm-usage")
    options.add_argument('--kiosk')

    service = Service("/usr/src/chrome/chromedriver")
    driver = webdriver.Chrome(options=options, service=service)
    
    #test
    #channel_name_list = ['겂도 없꾸라', 'FIFTY FIFTY Official']

    #youtube_boy_light
    channel_name_list =['ZEROBASEONE', '백현 Baekhyun', 'NCT 127', 'NCT DREAM', 'TREASURE (트레저)', 'THE BOYZ', 'GOT7', 'MONSTA X', 'ASTRO 아스트로', 'ONEUS', 'SF9']

    videos_data=[]
    #data=ytb_channel_data_func(driver)
    channel_data=ytb_channel_data_func(driver, channel_name_list)
    for i in range(len(channel_data)):
        ytb_video_data_func(options, service ,channel_data[i], videos_data)

    return videos_data
  # 드라이버 종료 후 리턴


if __name__ == "__main__":
    # crawling.start_crawling_hour("youtube", youtube, 1)
    #crawling.start_crawling_test("youtube", youtube)
    crawling.start_crawling_day("youtube_boy_light", youtube_boy_light, "01:00")

