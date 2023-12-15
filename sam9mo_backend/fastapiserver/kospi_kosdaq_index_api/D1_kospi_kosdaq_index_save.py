import requests
import redis
import json
import time
from datetime import datetime
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
brokers = ['59.3.28.12:9092', '59.3.28.12:9093', '59.3.28.12:9094']
topic = "fastapi_check"
pr = MessageProducer(brokers, topic)

def check_message(content:str):
    check_message ={    #현황체크
                    "consummer" : "D1_kospi_kosdaq_index_save",
                    "check_situation" : content
            }
    pr.send_message(check_message,False)# kafka전달turn document

#-------------------------------------------------------------------------------------


kospi_D1_api_url = "https://query1.finance.yahoo.com/v8/finance/chart/%5EKS11?region=US&lang=en-US&includePrePost=false&interval=2m&range=1d&corsDomain=search.yahoo.com"
kospi200_D1_api_url = "https://query1.finance.yahoo.com/v8/finance/chart/%5EKS200?region=US&lang=en-US&includePrePost=false&interval=2m&useYfid=true&range=1d&corsDomain=finance.yahoo.com&.tsrc=finance"
kosdaq_D1_api_url = "https://query1.finance.yahoo.com/v8/finance/chart/%5EKQ11?region=US&lang=en-US&includePrePost=false&interval=2m&useYfid=true&range=1d&corsDomain=finance.yahoo.com&.tsrc=finance"

custom_user_agent = 'Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/119.0.0.0 Safari/537.36'  # Replace with your desired User-Agent string


def kos_index(url, custom_user_agent):
    # Adding headers with a custom User-Agent
    headers = {
        'User-Agent': custom_user_agent
    }

    index = {}

    # Sending a GET request to the API with custom headers
    try:
        response = requests.get(url, headers=headers)
    except Exception as e :
        print(e)
    if response.status_code == 200:
        #print(response.status_code)
        data = response.json()
        index = data
        
    else:
        print(f"Failed to retrieve data. Status code: {response.status_code}")

    data_sum = []

    result_data = index['chart']['result']

    for result_item in result_data:
        #print("result_item->",result_item)
        try:
            timestamps = result_item['timestamp']
            quotes = result_item['indicators']['quote']
        except Exception as e:
            print("Exception=>", e)
            continue
            
    for ind, timestamp in enumerate(timestamps):
        print("timestamp-->", timestamp)
        data_item = {
            "timestamp": timestamp,
                "close": quotes[0]['close'][ind],
                "high": quotes[0]['high'][ind],
                "volume": quotes[0]['volume'][ind],
                "low": quotes[0]['low'][ind],
                "open": quotes[0]['open'][ind]
        }
        data_sum.append(data_item)
    
    today= datetime.today() 
    today = today.strftime("%Y%m%d")


 
    data_transform={}
    
    data_transform["date"]= today
    data_transform["data"] = data_sum
    

    return json.dumps(data_transform)

print("start--------")

# 레디스 연결
rd = redis.StrictRedis(host='59.3.28.12', port=6379, db=0, password='sam9mo!!')
    
while True:
    time.sleep(15)
    try:
        check_message("ok")
        # kospi
        kospi_d1=kos_index(kospi_D1_api_url,custom_user_agent)
        # kospi200
        kospi200_d1=kos_index(kospi200_D1_api_url,custom_user_agent)
        #kosdaq
        kosdaq_d1=kos_index(kosdaq_D1_api_url,custom_user_agent)
    
        # 레디스 전송
        # str형변환 꼭해야함!!
        #kospi
        rd.set("kospi_D1",str(kospi_d1))
        #kospi200
        rd.set("kospi200_D1",str(kospi200_d1))
        #kosdaq
        rd.set("kosdaq_D1",str(kosdaq_d1))
        print("ok")
    except Exception as e:
        check_message(e)



