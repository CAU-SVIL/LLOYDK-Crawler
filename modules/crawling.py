from pymongo import MongoClient
import schedule
import time

BASE_URL = "mongodb://crawling_db"
PORT = 27000
# DB와 통신 - 데이터이름, 저장 시간, 데이터
def save_data(name, data):
  print("saving data...", time.strftime('%Y-%m-%d %H:%M:%S'))
  
  client = MongoClient(BASE_URL, PORT)
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

# DB의 collection의 최신 데이터 조회
def print_recent_data(name):
  client = MongoClient(BASE_URL, PORT)
  db = client.crawling
  collection = db[name]
  data = collection.find()[0]["data"]
  print(data)

# test용 즉각 크롤링
def start_crawling_test(name, func):
  time.sleep(3)
  save_data(name, func())
  print_recent_data(name)
