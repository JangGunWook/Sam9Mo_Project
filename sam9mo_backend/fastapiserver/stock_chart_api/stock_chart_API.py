# main.py
from enum import Enum
from fastapi import FastAPI,HTTPException  # FastAPI import
from pymongo import MongoClient
import uvicorn
from fastapi.middleware.cors import CORSMiddleware
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

def check_message(content1:str, content2:str):
    check_message ={    #현황체크
                    "consummer" : "stock_chart_API",
                    "check_situation" : content1,
                    "ERROR_content" : content2
            }
    pr.send_message(check_message,False)# kafka전달turn document

#-------------------------------------------------------------------------------------
# from bson.objectid import ObjectId

client = MongoClient('mongodb://sam9:sam9mo!!@59.3.28.12:27017')
db = client['sam9mo']


app = FastAPI()

# origins에는 protocal, domain, port만 등록한다.
origins = [
    # "http://192.168.0.13:3000", # url을 등록해도 되고
    "*" # private 영역에서 사용한다면 *로 모든 접근을 허용할 수 있다.
]

app.add_middleware(
    CORSMiddleware,
    allow_origins=origins,
    allow_credentials=True, # cookie 포함 여부를 설정한다. 기본은 False
    allow_methods=["GET","POST"],    # 허용할 method를 설정할 수 있으며, 기본값은 'GET'이다.
    allow_headers=["*"],	# 허용할 http header 목록을 설정할 수 있으며 Content-Type, Accept, Accept-Language, Content-Language은 항상 허용된다.
)


class Kospi_kosdaq(str, Enum):
	kospi_daily_stock ="kospi_daily_stock"
	kosdaq_daily_stock="kosdaq_daily_stock"
	kospi_week_stock="kospi_week_stock"
	kosdaq_week_stock="kosdaq_week_stock"
	kospi_month_stock="kospi_month_stock"
	kosdaq_month_stock="kosdaq_month_stock"
# kospi 일봉API
@app.post(path="/{stock}/{num}")
def stock_chart_API(stock:Kospi_kosdaq, num):
    try:
        if stock in Kospi_kosdaq:
            # Kospi_kosdaq 안에 주식이 있다면 해당 회사 번호(num)로 데이터를 찾아서 반환
            document = db[stock].find_one({"_id": num})
            check_message("ok","")
            return document
        else:
            # 주식이 없는 경우 404 오류 반환
            check_message("ok")
            return HTTPException(status_code=404, detail="Item not found")
    except Exception as e:
        # 예외 발생 시 에러 메시지 출력
        print(e)
        check_message("ERROR",e)

# @app.get("/json")
# def printJson():
# 	return {
# 		"Number" : 12345
# 	}
    
# # class Post(BaseModel):
# # 	title: str
# # 	content: str

# @app.post("/posts")
# def createContents(post : Post):
# 	title = post.title
# 	content = post.content

if __name__ == "__main__":
    uvicorn.run(app, host="0.0.0.0", port=8081)