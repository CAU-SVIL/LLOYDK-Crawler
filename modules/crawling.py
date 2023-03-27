from pymongo import MongoClient
import schedule
import time


def save_data(name, data):
  print("saving data...", time.strftime('%Y-%m-%d %H:%M:%S'))
  
  client = MongoClient("172.19.0.3", 27017)
  db = client.dbsparta
  
  db.users.insert_one({
    "name": name,
    "time": time.strftime('%Y-%m-%d %H:%M:%S'),
    "data": data
  })


def start_crawling_day(name, func, s_time):
  schedule.every().day.at(s_time).do(lambda : save_data(name, func()))
  while True:
    schedule.run_pending()
    time.sleep(1)


def start_crawling_hour(name, func, hour):
  schedule.every(hour).hour.do(lambda : save_data(name, func()))
  while True:
    schedule.run_pending()
    time.sleep(1)
