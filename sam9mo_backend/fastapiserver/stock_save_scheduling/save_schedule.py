# 사용방법

import sys
import os
sys.path.append(os.path.dirname(os.path.abspath(os.path.dirname(__file__))))
import schedule
import time
import datetime
from Daily_save_stock import daily_save
from Week_save_stock import week_save
from Month_save_stock import month_save
from kospi_kosdaq_index_api.DWMY_kospi_kosdaq_index_save import DWMY_kospi_kosdaq_index
from kafka import KafkaProducer
import json
import time
#-------------------------------------------------------------------------------------
class MessageProducer:
    def __init__(self, broker, topic):
        self.broker = broker
        self.topic = topic
        self.producer = KafkaProducer(
            bootstrap_servers=self.broker,
            value_serializer=lambda x: json.dumps(x).encode("utf-8"),
            acks=0,
            api_version=(2, 5, 0),
            retries=3,
        )

    def send_message(self, msg, auto_close=False):
        try:
            future = self.producer.send(self.topic, msg)
            self.producer.flush()  # 비우는 작업
            if auto_close:
                self.producer.close()
            future.get(timeout=2)
            return {"status_code": 200, "error": None}
        except Exception as exc:
            raise exc

# 브로커와 토픽명을 지정한다.


def check_message(content:str):
    brokers = ['59.3.28.12:9092', '59.3.28.12:9093', '59.3.28.12:9094']
    topic = "fastapi_check"
    pr = MessageProducer(brokers, topic)

    check_message ={    #현황체크
                    "consummer" : "schedculing",
                    "check_situation" : content
            }
    pr.send_message(check_message,False)# kafka전달turn document

#-------------------------------------------------------------------------------------
#-------------------------------------------------------------------------------------------------------
# daily_save_stock 화수목금토 저장
schedule.every().tuesday.at("07:05").do(daily_save)
schedule.every().wednesday.at("07:10").do(daily_save)
schedule.every().thursday.at("07:15").do(daily_save)
schedule.every().friday.at("07:20").do(daily_save)
schedule.every().saturday.at("07:25").do(daily_save)

# week_save_Stock 매주월요일 저장
schedule.every().monday.at("07:30").monday.do(week_save)



# 매월 1일에 month_save_stock  함수 실행
if datetime.datetime.now().day == 1:
    schedule.every().day.at('07:35').do(month_save)



# ------------------------------------------------------------------------------------------------------------------
# 코스피/코스닥 5일, 일주일, 1달, 6개월, 1년 indexAPI 매일 7시 Redis에 저장 
schedule.every().day.at("07:00").do(DWMY_kospi_kosdaq_index)
try:
    while True:
        schedule.run_pending()
        check_message("ok")
        time.sleep(1)
except Exception as e:
    check_message("ERROR")
    print(e)