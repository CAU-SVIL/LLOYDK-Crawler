from pymongo import MongoClient
import schedule
import time

# DB와 통신 - 데이터이름, 저장 시간, 데이터
def save_data(name, data):
  print("saving data...", time.strftime('%Y-%m-%d %H:%M:%S'))
  
  client = MongoClient("172.19.0.3", 27017)
  db = client.crawling
  collection = db[name]

  collection.insert_one({
    "time": time.strftime('%Y-%m-%d %H:%M:%S'),
    "data": data
  })

# 하루 특정한 시간에 크롤링
def start_crawling_day(name, func, s_time):
  schedule.every().day.at(s_time).do(lambda : save_data(name, func()))
  while True:
    schedule.run_pending()
    time.sleep(1)

# 매 시간 마다 크롤링
def start_crawling_hour(name, func, hour):
  schedule.every(hour).hour.do(lambda : save_data(name, func()))
  while True:
    schedule.run_pending()
    time.sleep(1)

# test용 즉각 크롤링
def start_crawling_test(name, func):
  time.sleep(5)
  save_data(name, func())
