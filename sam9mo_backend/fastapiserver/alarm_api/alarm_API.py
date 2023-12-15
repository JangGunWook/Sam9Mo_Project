
from fastapi.middleware.cors import CORSMiddleware
from fastapi import FastAPI, WebSocket, WebSocketDisconnect, Response
import json
import asyncio
import pandas as pd
from datetime import datetime
import time
import uvicorn
from aiokafka import AIOKafkaConsumer
import threading
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
                    "consummer" : "alarm",
                    "check_situation" : content
            }
    pr.send_message(check_message,False)# kafka전달turn document

#-------------------------------------------------------------------------------------


STOCK_CODE = {
    '005930': '삼성전자',    '373220': 'LG에너지솔루션',    '000660': 'SK하이닉스',    '207940': '삼성바이오로직스',    '005935': '삼성전자우',
    '005490': 'POSCO홀딩스',    '005380': '현대차',    '051910': 'LG화학',    '035420': 'NAVER',    '000270': '기아',
    '006400': '삼성SDI',    '068270': '셀트리온',    '003670': '포스코퓨처엠',    '035720': '카카오',    '105560': 'KB금융',
    '028260': '삼성물산',    '012330': '현대모비스',    '055550': '신한지주',    '066570': 'LG전자',    '096770': 'SK이노베이션',
    '032830': '삼성생명',    '003550': 'LG',    '323410': '카카오뱅크',    '033780': 'KT&G',    '086790': '하나금융지주',
    '000810': '삼성화재',    '034730': 'SK',    '015760': '한국전력',    '138040': '메리츠금융지주',    '017670': 'SK텔레콤',
    '018260': '삼성에스디에스',    '011200': 'HMM',    '329180': 'HD현대중공업',    '010130': '고려아연',    '009150': '삼성전기',
    '047050': '포스코인터내셔널',    '259960': '크래프톤',    '316140': '우리금융지주',    '034020': '두산에너빌리티',    '024110': '기업은행',
    '247540': '에코프로비엠',    '086520': '에코프로',    '091990': '셀트리온헬스케어',    '022100': '포스코DX',    '066970': '엘앤에프',
    '028300': 'HLB',    '196170': '알테오젠',    '068760': '셀트리온제약',    '035900': 'JYP Ent.',    '277810': '레인보우로보틱스',    '403870': 'HPSP',
    '058470': '리노공업',    '263750': '펄어비스',    '214150': '클래시스',    '293490': '카카오게임즈',    '357780': '솔브레인',    '041510': '에스엠',
    '039030': '이오테크닉스',    '145020': '휴젤',    '005290': '동진쎄미켐',    '095340': 'ISC',    '112040': '위메이드',
    '240810': '원익IPS',    '036930': '주성엔지니어링',    '253450': '스튜디오드래곤',    '035760': 'CJ ENM',    '000250': '삼천당제약',
    '086900': '메디톡스',    '121600': '나노신소재',    '214370': '케어젠',    '067310': '하나마이크론',    '393890': '더블유씨피',
    '025900': '동화기업',    '034230': '파라다이스',    '237690': '에스티팜',    '078600': '대주전자재료',    '048410': '현대바이오',
    '141080': '레고켐바이오',    '365340': '성일하이텍',    '195940': 'HK이노엔'}

STOCK_CODE_TICKERS = {}


class ConnectionManager:
    def __init__(self):
        self.active_connections: list[WebSocket] = []

    async def connect(self, websocket: WebSocket):
        await websocket.accept()
        self.active_connections.append(websocket)

    def disconnect(self, websocket: WebSocket):
        self.active_connections.remove(websocket)

    async def send_personal_message(self, message: str, websocket: WebSocket):
        await websocket.send_text(message)

    async def broadcast(self, message: str):
        for connection in self.active_connections:
            try:
                await connection.send_text(message)
            except WebSocketDisconnect as e: # 웹소켓이 닫힌 경우 예외 처리
                print(f"WebSocket disconnected : {e}")
                self.disconnect(connection) # 웹소켓을 목록에서 제거
            except Exception as e: # 웹소켓이 닫힌 경우 예외 처리
                print(f"Error : {e}")
                self.disconnect(connection) # 웹소켓을 목록에서 제거

manager = ConnectionManager()

async def onStartUp():
    print('server start')
    startServer()

async def onShutDown():
    await manager.disconnect()

app = FastAPI(on_startup=[onStartUp], on_shutdown=[onShutDown])


# origins에는 protocal, domain, port만 등록한다.
origins = [
    # "http://192.168.0.13:3000", # url을 등록해도 되고
    "*" # private 영역에서 사용한다면 *로 모든 접근을 허용할 수 있다.
]

app.add_middleware(
    CORSMiddleware,
    allow_origins=origins,
    allow_credentials=True, # cookie 포함 여부를 설정한다. 기본은 False
    allow_methods=["*"],    # 허용할 method를 설정할 수 있으며, 기본값은 'GET'이다.
    allow_headers=["*"],	# 허용할 http header 목록을 설정할 수 있으며 Content-Type, Accept, Accept-Language, Content-Language은 항상 허용된다.
)


@app.get("/json")
def consummer():
    return STOCK_CODE_TICKERS

@app.get("/alarm")
def alarm():
    return js12



# 정가되면 비교가격
static_price = {}

js12 = []

# for key, value in STOCK_CODE_TICKERS.items():
#        static_price = {
#            key : {
#                "STCK_PRPR" : ""
#            }
#        }
def initStaticPrice():
    global static_price
    for key, value in STOCK_CODE_TICKERS.items():
        #print(value)
        static_price[key] = {
                "STCK_PRPR" : "0"
        }
    print("initStaticPrice_초기화 : =>",static_price)    
       
# 정각이면 비교가격 받기
def static_price_methond():
    #  static_price 초기화
    current_hour = int(datetime.now().strftime("%H%M")) 
    print("current_hour :", current_hour) 
    #시간이 정각이면
    if current_hour % 5  == 0:
          
        try:
                for key, value in STOCK_CODE_TICKERS.items():
                    if value != 0: 
                        static_price[key] =  { # 회사번호
                            "STCK_PRPR" : value["STCK_PRPR"] # 거래가
                            }
                
        except Exception as e:
            print(f'static_price_methond error => {e}')  

    threading.Timer(5, static_price_methond).start()            


js12=[]
for key in STOCK_CODE.keys():
    js = {
        "stock_num" : key,
        "percent_change" : None
    }
    js12.append(js)

# 시간대별 가격 변동 비교 함수
def compare_price_changes():
    # 초기 시간 설정 (9시부터 시작)
    current_hour = int(datetime.now().strftime("%H%M")) 
    
    if current_hour != 0: #현재시 간 이 0 이 아 니 면 
        try:
            check_message("ok")
            for key,value in STOCK_CODE_TICKERS.items():
                current_opening_price = None
                try:
                    current_opening_price = value["STCK_PRPR"]
                    percent_change = ((int(current_opening_price) - int(static_price[key]["STCK_PRPR"])) / int(static_price[key]["STCK_PRPR"])) * 100
                except Exception as e:
                    continue
                print(f"{key}는{datetime.now().strftime('%H%M')}시 이전 가격 대비 가격 변동률: {percent_change:.2f}%")
                if percent_change:
                    for Index, value in enumerate(js12):
                        if js12[Index]['stock_num'] == key:
                           js12[Index]["percent_change"] = percent_change
                    
            print("compare_price_changes")
        except Exception as e:
            print(f'compare_price_changes error => {e}')
            check_message(e) 
    threading.Timer(5, compare_price_changes).start()  

for key, value in STOCK_CODE.items():
        STOCK_CODE_TICKERS[key] = 0

async def receive_korea_stock_message():
    print(f'receive_korea_stock_message => start')   
    PAYMENT_TOPIC = 'stock_api'
    brokers = ['59.3.28.12:9092', '59.3.28.12:9093', '59.3.28.12:9094']
    consumer = AIOKafkaConsumer(
        PAYMENT_TOPIC,
        bootstrap_servers=brokers,
        value_deserializer=lambda m:json.loads(m.decode('utf-8'))
    )

    try:
        await consumer.start()
    except Exception as e:
        print(e)
        return

    try:
        async for message in consumer:
            #print(message.value)           
            STOCK_CODE_TICKERS[message.value["MKSC_SHRN_ISCD"]] = message.value
            #print("Message : \n",STOCK_CODE_TICKERS)
            #for key, value in STOCK_CODE_TICKERS:
            #    if key == STOCK_CODE[key]:
            #        STOCK_CODE_TICKERS[key][]   
            await manager.broadcast(json.dumps(STOCK_CODE_TICKERS))
    finally:
        await consumer.stop()
        print(f'receive_korea_stock_message => end')   

def startServer():
    initStaticPrice()
    static_price_methond()
    compare_price_changes()
    asyncio.create_task(    
        receive_korea_stock_message()
    )

if __name__ == "__main__":
    uvicorn.run(app, host="0.0.0.0", port=9101)