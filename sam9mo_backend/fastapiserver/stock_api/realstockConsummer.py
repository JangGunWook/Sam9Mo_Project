from fastapi import FastAPI, WebSocket, WebSocketDisconnect, Response
import json
import asyncio
from pymongo import MongoClient
import pandas as pd
from fastapi.middleware.cors import CORSMiddleware
from aiokafka import AIOKafkaConsumer
from fastapi import FastAPI
import uvicorn
import time
from datetime import datetime, timedelta
from pydantic import BaseModel, Field
from stock_API_output2 import get_domestic_stock_price


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

def onStartUp():
    print('server start')
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
class Field_info():
    key: str = Field(title="종목번호로 6자리 숫자")
    # initial
    initial: str = Field(title="initial 초기값을 담고있는 key")
    prdy_vrss: str = Field(title="설명:전일 대비|자료형: String|응답:Y|length:10")
    prdy_vrss_sign: str = Field(title="설명:전일 대비 부호| 자료형:String| 응답:Y| length:1")
    prdy_ctrt: str = Field(title="설명:전일 대비율|	자료형:String| 응답:Y| length:11")
    stck_prdy_clpr:str = Field(title="설명:주식 전일 종가| 자료형:String| 응답:Y| length:10")
    acml_vol:str = Field(title="설명:누적 거래량| 자료형:String| 응답:Y| length:18")
    acml_tr_pbmn:str = Field(title="설명:누적 거래 대금| 자료형:String|	응답:Y|	length:18")	
    hts_kor_isnm:str = Field(title="설명:HTS 한글 종목명| 자료형:String| 응답:Y| length:40")	
    stck_prpr:str=Field(title="설명: 주식 현재가| 자료형:String| 응답:Y| length:10")	
    stck_shrn_iscd:str=Field(title="설명:주식 단축 종목코드| 자료형:String| 응답:Y| length:9")
    prdy_vol:str=Field(title="설명:전일 거래량|	자료형:String|	응답:Y|	length:18|")	
    stck_mxpr:str=Field(title="설명:상한가|	자료형:String| 응답:Y| length:10")
    stck_llam:str=Field(title="설명:하한가| 자료형:String| 응답:Y| length:10")	
    stck_oprc:str=Field(title="설명:시가| 자료형:String| 응답:Y| length:10")
    stck_hgpr:str=Field(title="설명: 최고가| 자료형:String| 응답:Y| length:10")
    stck_lwpr:str=Field(title="설명:최저가|	자료형:String| 응답:Y| length:10")	
    stck_prdy_oprc:str=Field(title="설명:주식 전일 시가| 자료형:String|	응답:Y|	length:10")	
    stck_prdy_hgpr:str=Field(title="설명:주식 전일 최고가| 자료형:String| 응답:Y| length:10")	
    stck_prdy_lwpr:str=Field(title="설명:주식 전일 최저가| 자료형:String| 응답:Y| length:10")	
    askp:str=Field(title="설명:매도호가| 자료형:String| 응답:Y| length:10")	
    bidp:str=Field(title="설명:매수호가| 자료형:String| 응답:Y|	length:10")	
    prdy_vrss_vol:str=Field(title="전일 대비 거래량	String	Y	10")	
    vol_tnrt:str=Field(title="설명:거래량 회전율| 자료형:String| 응답:Y| length:11")	
    stck_fcam:str=Field(title="설명:거래량 회전율!	자료형: String| 응답:Y|	length:11")	
    lstn_stcn:str=Field(title="설명:상장 주수| 자료형:String| 응답:Y| length:18")	
    cpfn:str=Field(title="설명: 자본금| 자료형:String| 응답:Y| length22")	
    hts_avls:str=Field(title="설명: 시가총액| 자료형: String| 응답:Y| length:18")	
    per:str=Field(title="설명:PER| 자료형:String| 응답:Y| length:11")	
    eps:str=Field(title="설명:EPS| 자료형:String| 응답:Y| length:14")	
    pbr:str=Field(title="설명:PBR| 자료형:String| 응답:Y| length:11")	
    itewhol_loan_rmnd_ratem_name:str=Field(title="설명:전체 융자 잔고 비율| 자료형:String| 응답:Y| length:13")	
    COMPANY:str=Field(title="설명:회사명| 자료형:String| 응답:Y") 
    # current_trade
    current_trade:str=Field(title="current_trade 실시간 거래되고 있는 거래현황")
    MKSC_SHRN_ISCD:str= Field(title="설명:유가증권 단축 종목코드| 자료형:String| 응답:Y| length:9")		
    STCK_CNTG_HOUR:str=Field(title="설명:주식 체결 시간| 자료형:String| 응답:Y| length:6")	
    STCK_PRPR:str= Field(title="설명:주식 현재가| 자료형:Number| 응답:Y| length:4")		
    PRDY_VRSS_SIGN:str=Field(title="설명:전일 대비 부호| 자료형:String| 응답:Y| length:1|",description="1 : 상한/ 2 : 상승/ 3 : 보합/ 4 : 하한/ 5 : 하락")
    PRDY_VRSS:str=Field(title="설명:전일 대비| 자료형:Number| 응답:Y| length:4")	
    PRDY_CTRT:str=Field(title="설명: 전일 대비율| 자료형:Number| 응답:Y| length:8")	
    WGHN_AVRG_STCK_PRC:int=Field(title="설명:가중 평균 주식 가격/ 자료형:Number| 응답:Y| length:8")	
    STCK_OPRC:str=Field(title="설명: 식 시가| 자료형:Number| 응답:Y| length:4")	
    STCK_HGPR:str=Field(title="설명:주식 최고가| 자료형:Number| 응답:Y| length:	4")	
    STCK_LWPR:str=Field(title="설명:주식 최저가| 자료형: Number| 응답:Y| length:4")	
    ASKP1:str=Field(title="설명: 매도호가1| 자료형:Number| 응답:Y| length:4")
    BIDP1:str=Field(title="설명:매수호가1| 자료형: Number| 응답:Y| length:4	")	
    CNTG_VOL:str=Field(title="설명:체결 거래량| 자료형:Number| 응답:Y| length:8")	
    ACML_VOL:str=Field(title="설명:누적 거래량| 자료형:Number| 응답:Y| length:8")	
    ACML_TR_PBMN:str=Field(title="설명:누적 거래 대금| 자료형:Number| 응답:Y| length:8")	
    SELN_CNTG_CSNU:str=Field(title="설명:매도 체결 건수| 자료형:Number| 응답:Y| length:4")	
    SHNU_CNTG_CSNU:str=Field(title="설명:매수 체결 건수| 자료형:Number| 응답:Y| length:4")	
    NTBY_CNTG_CSNU:str=Field(title="설명:순매수 체결 건수| 자료형:Number| 응답:Y| length:4")	
    CTTR:str=Field(title="설명:체결강도| 자료형:Number| 응답:Y| lenght:8")	
    SELN_CNTG_SMTN:str=Field("설명: 총 매도 수량| 자료형:Number| 응답:Y| length:8")	
    SHNU_CNTG_SMTN:str=Field("설명: 총 매수 수량| 자료형:Number| 응답:Y| length:8")	
    CCLD_DVSN:str=Field(title="설명: 체결구분| 자료형:String|	응답:Y|	lentght:1|", description="1:매수(+) 3:장전 5:매도(-)")	
    SHNU_RATE:str=Field(title="설명:매수비율	Number	Y	8")		
    PRDY_VOL_VRSS_ACML_VOL_RATE:str=Field(title="설명:전일 거래량 대비 등락율| 자료형:Number| 응답:Y| length:8")	
    OPRC_HOUR:str=Field(title="설명:시가 시간| 자료형:String| 응답:Y| length:6")	
    OPRC_VRSS_PRPR_SIGN:str=Field(title="설명:시가대비구분| 자료형:String| 응답:Y| length:1", description="1 : 상한 2 : 상승 3 : 보합 4 : 하한 5 : 하락")	
    OPRC_VRSS_PRPR:int=Field(title="설명: 시가대비/ 자료형:Number| 응답:Y| length:4")	
    HGPR_HOUR:str=Field(title="설명:최고가 시간| 자료형:String| 응답:Y| length:6")	
    HGPR_VRSS_PRPR_SIGN:str=Field(title="설명:고가대비구분| 자료형:String| 응답:Y| length:1", description="1 : 상한 2 : 상승 3 : 보합 4 : 하한 5 : 하락")	
    HGPR_VRSS_PRPR:int=Field(title="설명:고가대비| 자료형:Number| 응답:Y| lenght:4")	
    LWPR_HOUR:str=Field(title="설명:최저가 시간| 자료형:String| 응답:Y| length:6")	
    LWPR_VRSS_PRPR_SIGN:str=Field(title="설명: 저가대비구분| 자료형:String| 응답:Y| length:	1", description="1 : 상한 2 : 상승 3 : 보합 4 : 하한 5 : 하락")	
    LWPR_VRSS_PRPR:int=Field(title="설명:저가대비| 자료형:Number| 응답:Y| length:4")	
    BSOP_DATE:str=Field(title="설명: 영업 일자| 자료형:String| 자료형Y| length:8")	
   
# param에 담기는 데이터 형식을 정형화
# company: str
# initial: list
# current_trade: list
class Item(BaseModel):  #BaseModel은 정형화하기 위함
    company: str    # 회사는 단일(str)
    initial: list   # initial에 해당하는 컬럼은 list
    current_trade: list # current_trade에 해당하는 컬럼은 list

#
def makeData(company: str, initial: list, current_trade: list):
    stockData = {}  # 최종 데이터를 담을 dict
    stockData[company] = {} # 일단 회사num을 key지정해놓는다
    try:
        responseJsonCompanyInfo = STOCK_CODE_TICKERS[company]
        responseInitial = responseJsonCompanyInfo['initial']
        responseCurrentTrade = responseJsonCompanyInfo['current_trade']
        # responseJsonCompanyInfo에 담겨있는 데이터 형태
        # stockData ={
        #       company : {
        #                     initial : {},
        #                     current_trade : {}
        #                   }
        #            }

        initialData = {}
        if (len(responseInitial) > 0):  # responseInitial은 리스트 형태이다! 배열의 길이를 체크
            for key, value in responseInitial.items():
                if key in initial:  # initial은 자료형이 리스트임                           
                    initialData.update({key : value }) 

        stockData[company]['initial'] = initialData

        currentTradeData = {}
        if (len(responseCurrentTrade) > 0):  # responseCurrentTrade은 리스트 형태이다! 배열의 길이를 체크
            for key, value in responseCurrentTrade.items():
                if key in current_trade:  # # responseInitial은 자료형이 리스트임    
                    currentTradeData.update({key : value })

        stockData[company]['current_trade'] = currentTradeData
    except Exception as e:
        stockData = { "status" : "error" }
        print(f'::::::: makeData Error => {e}')        
    finally:
        return stockData


@app.post(path="/stock_api",
         name="실시간 종목별 데이터API",
         description="코스피, 코스닥 각40종목씩 실시간 거래 및 자본,재무정보 확인가능",
         )
def consummer(item: Item):
    if STOCK_CODE_TICKERS is not None:
        company = item.company
        initial = item.initial
        current_trade = item.current_trade
        returnData = {}
        if company != '0':
            # STOCK_CODE_TICKERS에 들어오는 dict의 key값이 일치하는 지 확인
            if company in STOCK_CODE_TICKERS:
                # 일치하는 key값이 있을 경우 그에 해당하는 데이터 추출
                returnData.update(makeData(company, initial, current_trade))  
            else:
                # STOCK_CODE_TICKERS에에 들어있는 key값이 없을시 실행
                returnData = { "status" : "company is not found"}
        else:
            # 0을 입력시 모든 데이터를 추출함            
            for companyCode in STOCK_CODE_TICKERS:
                returnData.update(makeData(companyCode, initial, current_trade))
                
        return returnData
    else:
        return { "status" : "none" }  


@app.get(path="/stock_api_all")
def stock_appi_all():
    return STOCK_CODE_TICKERS

@app.websocket(path="/ws/{client_id}",
               name="실시간 종목별 데이터websocket")
async def websocket_endpoint(websocket: WebSocket, client_id: int):
    await manager.connect(websocket)
    while True:
        # 웹소켓으로부터 텍스트 데이터를 수신합니다.
        data = await websocket.receive_text()
        # 웹소켓으로 텍스트 데이터를 전송합니다.
        await websocket.send_text(f"Message text was: {data}")



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


# 오늘 날짜 가져오기
today = datetime.today().strftime("%Y%m%d")

STOCK_CODE_TICKERS = {}
# 초기값을 몽고DB의 
for key, value in STOCK_CODE.items():
    result = get_domestic_stock_price(key,today,today)
    if result:
        stock_data = result["output1"]
        if stock_data:
            stock_data["COMPANY"] = value
            STOCK_CODE_TICKERS[key] = {
                "initial":stock_data,    # API로 가져온 값
                "current_trade": ""         # websocket의 변화되는 거래값 
                }

finalConsumerTime = None
async def receive_korea_stock_message(): 
    global finalConsumerTime  
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
            STOCK_CODE_TICKERS[message.value["MKSC_SHRN_ISCD"]]["current_trade"] = message.value
            await manager.broadcast(json.dumps(STOCK_CODE_TICKERS))
            finalConsumerTime = time.time()
    finally:
        await consumer.stop()

@app.get('/finalConsumerTime')
def finalConsumerTime():
    return finalConsumerTime

asyncio.create_task(
    receive_korea_stock_message()
)        

# if __name__ == "__main__":
#     asyncio.run(receive_korea_stock_message())
#     # uvicorn.run(app, host="0.0.0.0", port=8881)