from fastapi import FastAPI, WebSocket, WebSocketDisconnect
from fastapi.middleware.cors import CORSMiddleware
import json
import asyncio
from aiokafka import AIOKafkaConsumer
from fastapi import FastAPI, Request
from kafka import TopicPartition
import uvicorn
import logging
from typing import Set, Any
from sse_starlette.sse import EventSourceResponse

BROKERS = ['59.3.28.12:9092', '59.3.28.12:9093', '59.3.28.12:9094']
KRW_TICKERS_VALUE = ['KRW-BTC', 'KRW-ETH', 'KRW-NEO', 'KRW-MTL', 'KRW-XRP', 'KRW-ETC', 'KRW-SNT', 'KRW-WAVES', 'KRW-XEM', 'KRW-QTUM', 'KRW-LSK', 'KRW-STEEM', 'KRW-XLM', 'KRW-ARDR', 'KRW-ARK', 'KRW-STORJ', 'KRW-GRS', 'KRW-ADA', 'KRW-SBD', 'KRW-POWR', 'KRW-BTG', 'KRW-ICX', 'KRW-EOS', 'KRW-TRX', 'KRW-SC', 'KRW-ONT', 'KRW-ZIL', 'KRW-POLYX', 'KRW-ZRX', 'KRW-LOOM', 'KRW-BCH', 'KRW-BAT', 'KRW-IOST', 'KRW-CVC', 'KRW-IQ', 'KRW-IOTA', 'KRW-HIFI', 'KRW-ONG', 'KRW-GAS', 'KRW-UPP', 'KRW-ELF', 'KRW-KNC', 'KRW-BSV', 'KRW-THETA', 'KRW-QKC', 'KRW-BTT', 'KRW-MOC', 'KRW-TFUEL', 'KRW-MANA', 'KRW-ANKR', 'KRW-AERGO', 'KRW-ATOM', 'KRW-TT', 'KRW-CRE', 'KRW-MBL', 'KRW-WAXP', 'KRW-HBAR', 'KRW-MED', 'KRW-MLK', 'KRW-STPT', 'KRW-ORBS', 'KRW-VET', 'KRW-CHZ', 'KRW-STMX', 'KRW-DKA', 'KRW-HIVE', 'KRW-KAVA', 'KRW-AHT', 'KRW-LINK', 'KRW-XTZ', 'KRW-BORA', 'KRW-JST', 'KRW-CRO', 'KRW-TON', 'KRW-SXP', 'KRW-HUNT', 'KRW-PLA', 'KRW-DOT', 'KRW-MVL', 'KRW-STRAX', 'KRW-AQT', 'KRW-GLM', 'KRW-SSX', 'KRW-META', 'KRW-FCT2', 'KRW-CBK', 'KRW-SAND', 'KRW-HPO', 'KRW-DOGE', 'KRW-STRK', 'KRW-PUNDIX', 'KRW-FLOW', 'KRW-AXS', 'KRW-STX', 'KRW-XEC', 'KRW-SOL', 'KRW-MATIC', 'KRW-AAVE', 'KRW-1INCH', 'KRW-ALGO', 'KRW-NEAR', 'KRW-AVAX', 'KRW-T', 'KRW-CELO', 'KRW-GMT', 'KRW-APT', 'KRW-SHIB', 'KRW-MASK', 'KRW-ARB', 'KRW-EGLD', 'KRW-SUI', 'KRW-GRT', 'KRW-BLUR', 'KRW-IMX', 'KRW-SEI', 'KRW-MINA']
STOCK_CODE = ["005930", "373220", "000660", "207940", "005935", "005380", "005490", "051910", "000270", "035420","006400", "068270", "003670", "105560", "028260","012330", "035720", "055550", "066570", "032830",]
I_STOCK = ["005930", "373220", "000660", "207940", "005935","005380", "005490", "051910", "000270", "035420","006400", "068270", "003670", "105560", "028260","012330", "035720", "055550", "066570", "032830",]

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

manager = ConnectionManager()
# global variables
upbit_consumer_task = None
korea_stock_consumer_task = None
sendUpbitPriceByWebSocket_task = None
upbit_consumer = None
korea_stock_consumer = None

_state = 0
MESSAGE_STREAM_DELAY = 2  # second
MESSAGE_STREAM_RETRY_TIMEOUT = 15000  # milisecond

async def onStartUp():
    log.info('Initializing API ...')
    await initializeKoreaStock()
    await initializeUpbit()
    await consume()
    
async def onShutDown():
    log.info('Shutting down API')
    upbit_consumer_task.cancel()
    korea_stock_consumer_task.cancel()
    sendUpbitPriceByWebSocket_task.cancel()

app = FastAPI(on_startup=[onStartUp], on_shutdown=[onShutDown])
app.add_middleware(
    CORSMiddleware,
    allow_origins=["*"],
    allow_credentials=True,
    allow_methods=["*"],
    allow_headers=["*"],
)
# initialize logger
logging.basicConfig(format='%(asctime)s - %(levelname)s - %(message)s',
                    level=logging.INFO)
log = logging.getLogger(__name__)

@app.get('/api/coin/tradeprice')
async def krwCoinTradePrice():
    return json.dumps(KRW_COIN_TICKERS_TRADE_PRICE_API)

@app.get('/api/coin/all')
async def krwCoinAll():
    return json.dumps(KRW_COIN_TICKERS_ALL_API)

@app.get('/api/stock/all')
async def koreaStockAll():
    return json.dumps(STOCK_CODE_TICKERS)

@app.websocket("/ws/{client_id}")
async def websocket_endpoint(websocket: WebSocket, client_id: int):
    await manager.connect(websocket)
    try:
        while True:
            # 웹소켓으로부터 텍스트 데이터를 수신합니다.
            await websocket.receive_text()
            # 웹소켓으로 텍스트 데이터를 전송합니다.
    except WebSocketDisconnect as e:
        manager.disconnect(websocket)
    except Exception as e:
        print(f'websocket_endpoint {e}')

@app.get("/krwcoinallstream")
async def message_stream(request: Request):
    async def event_generator():
        while True:
            if await request.is_disconnected():
                log.debug("Request disconnected")
                break

            yield json.dumps(KRW_COIN_TICKERS_ALL_API)
            await asyncio.sleep(MESSAGE_STREAM_DELAY)

    return EventSourceResponse(event_generator())

@app.get("/krwcoinstream")
async def message_stream(request: Request):
    async def event_generator():
        while True:
            if await request.is_disconnected():
                log.debug("Request disconnected")
                break

            yield json.dumps(KRW_COIN_TICKERS_TRADE_PRICE_API)
            await asyncio.sleep(MESSAGE_STREAM_DELAY)

    return EventSourceResponse(event_generator())

@app.get("/koreastockstream")
async def message_stream(request: Request):
    async def event_generator():
        while True:
            if await request.is_disconnected():
                log.debug("Request disconnected")
                break

            yield json.dumps(STOCK_CODE_TICKERS)
            await asyncio.sleep(MESSAGE_STREAM_DELAY)

    return EventSourceResponse(event_generator())

KRW_COIN_TICKERS_ALL_API = {}
KRW_COIN_TICKERS_TRADE_PRICE_API = {}
for i in KRW_TICKERS_VALUE:
    KRW_COIN_TICKERS_ALL_API[i] = 0
    KRW_COIN_TICKERS_TRADE_PRICE_API[i] = 0

STOCK_CODE_TICKERS = {}
for i in STOCK_CODE:
    STOCK_CODE_TICKERS[i] = 0

def _update_state(message: Any) -> None:
    value = json.loads(message.value)
    global _state
    _state = value

async def initializeKoreaStock():
    # loop = asyncio.get_event_loop()
    global korea_stock_consumer
    KAFKA_TOPIC = 'korea_stock'
    korea_stock_consumer = AIOKafkaConsumer(KAFKA_TOPIC,
                                         bootstrap_servers=BROKERS)
    # get cluster layout and join group
    await korea_stock_consumer.start()

    partitions: Set[TopicPartition] = korea_stock_consumer.assignment()
    nr_partitions = len(partitions)
    if nr_partitions != 1:
        log.warning(f'Found {nr_partitions} partitions for topic {KAFKA_TOPIC}. Expecting '
                    f'only one, remaining partitions will be ignored!')
    for tp in partitions:

        # get the log_end_offset
        end_offset_dict = await korea_stock_consumer.end_offsets([tp])
        end_offset = end_offset_dict[tp]

        if end_offset == 0:
            log.warning(f'Topic ({KAFKA_TOPIC}) has no messages (log_end_offset: '
                        f'{end_offset}), skipping initialization ...')
            return

        log.debug(f'Found log_end_offset: {end_offset} seeking to {end_offset-1}')
        korea_stock_consumer.seek(tp, end_offset-1)
        msg = await korea_stock_consumer.getone()
        log.info(f'Initializing API with data from msg: {msg}')

        # update the API state
        _update_state(msg)
        return

async def initializeUpbit():
    # loop = asyncio.get_event_loop()
    global upbit_consumer
    KAFKA_TOPIC = 'upbit'
    upbit_consumer = AIOKafkaConsumer(KAFKA_TOPIC,
                                         bootstrap_servers=BROKERS)
    # get cluster layout and join group
    await upbit_consumer.start()

    partitions: Set[TopicPartition] = upbit_consumer.assignment()
    nr_partitions = len(partitions)
    if nr_partitions != 1:
        log.warning(f'Found {nr_partitions} partitions for topic {KAFKA_TOPIC}. Expecting '
                    f'only one, remaining partitions will be ignored!')
    for tp in partitions:

        # get the log_end_offset
        end_offset_dict = await upbit_consumer.end_offsets([tp])
        end_offset = end_offset_dict[tp]

        if end_offset == 0:
            log.warning(f'Topic ({KAFKA_TOPIC}) has no messages (log_end_offset: '
                        f'{end_offset}), skipping initialization ...')
            return

        log.debug(f'Found log_end_offset: {end_offset} seeking to {end_offset-1}')
        upbit_consumer.seek(tp, end_offset-1)
        msg = await upbit_consumer.getone()
        log.info(f'Initializing API with data from msg: {msg}')

        # update the API state
        _update_state(msg)
        return
    
async def receive_upbit_message(upbitconsumer):       
    global KRW_COIN_TICKERS_ALL_API
    global KRW_COIN_TICKERS_TRADE_PRICE_API

    try:
        # consume messages
        async for message in upbitconsumer:
            messageValueStr = json.loads(message.value.decode('utf-8'))
            KRW_COIN_TICKERS_ALL_API[messageValueStr['code']] = messageValueStr
            KRW_COIN_TICKERS_TRADE_PRICE_API[messageValueStr['code']] = messageValueStr['trade_price']
            # print(message.value['code'])
            # await manager.broadcast(json.dumps(KRW_COIN_TICKERS_ALL_API))
    except Exception as e:
        print(f'receive_upbit_message {e}')
    finally:
        # will leave consumer group; perform autocommit if enabled
        log.warning('receive_upbit_message Stopping upbitconsumer')
        await upbitconsumer.stop()

async def receive_korea_stock_message(consumer):
    global STOCK_CODE_TICKERS 
    try:
        async for message in consumer:
            messageValueStr = json.loads(message.value.decode('utf-8'))
            # print(f'||| receive_korea_stock_message ||| {messageValueStr}')
            STOCK_CODE_TICKERS[messageValueStr['MKSC_SHRN_ISCD']] = messageValueStr
            # print(message.value['code'])
            # await manager.broadcast(json.dumps(STOCK_CODE_TICKERS))
    except Exception as e:
        print(f'||| receive_korea_stock_message ||| {e}')
    finally:
        # will leave consumer group; perform autocommit if enabled
        log.warning('receive_korea_stock_message Stopping korea_stock_consumer')
        await korea_stock_consumer.stop()

async def sendUpbitPriceByWebSocket():
    while True:
        try:
            await manager.broadcast(json.dumps(KRW_COIN_TICKERS_ALL_API))
            await asyncio.sleep(0.5)
        except Exception as e:
            continue

# async def send_consumer_message(consumer):
#     try:
#         # consume messages
#         async for msg in consumer:
#             # x = json.loads(msg.value)
#             #log.info(f"Consumed msg: {msg}")
#             _update_state(msg)
#             # await manager.broadcast(str(msg.value))
#             # update the API state
#     except Exception as e:
#         print(e)
#     finally:
#         # will leave consumer group; perform autocommit if enabled
#         log.warning('send_consumer_message Stopping consumer')
#         await consumer.stop()
  
async def consume():
    global upbit_consumer_task
    upbit_consumer_task = asyncio.create_task(receive_upbit_message(upbit_consumer))
    global korea_stock_consumer_task
    korea_stock_consumer_task = asyncio.create_task(receive_korea_stock_message(korea_stock_consumer))
    global sendUpbitPriceByWebSocket_task
    sendUpbitPriceByWebSocket_task = asyncio.create_task(sendUpbitPriceByWebSocket())
    
if __name__ == "__main__":
    # TODO 로컬 배포
    #uvicorn.run(app, host="127.0.0.1", port=8000, reload=True)
    # TODO 실서버 배포
    uvicorn.run(app, host="0.0.0.0", port=9100)
    