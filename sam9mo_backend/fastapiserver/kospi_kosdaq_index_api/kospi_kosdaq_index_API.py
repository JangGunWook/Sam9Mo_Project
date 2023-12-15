from fastapi import FastAPI, HTTPException
from fastapi.middleware.cors import CORSMiddleware
import redis
from enum import Enum
from pydantic import BaseModel, Field
import uvicorn
import json

def onStartUp():
    print('server start')
def onShutDown():
    print("server close")

app = FastAPI(on_startup=[onStartUp], on_shutdown=[onShutDown])

class kospi_kosdaq_API(BaseModel):
    timestamp:int = Field(title="유닉스타임스탬프")
    hight:int = Field(title="고가")
    volume:int = Field(title="거래량?")
    low:int=Field(title="저가")
    open:int=Field(title="시가")

class list12(BaseModel):
    list1:list[kospi_kosdaq_API]
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

rd = redis.StrictRedis(host='59.3.28.12', port=6379, db=0, password='sam9mo!!')

# kospi_index----------------------------------------------------------------
#kospi_D1
#kospi_D5
#kospi_M1
#kospi_M6
#kospi_YTD
class Kospi_index(str, Enum):
    kospi_D1 = "kospi_D1"
    kospi_D5 = "kospi_D5"
    kospi_M1 = "kospi_M1"
    kospi_M6 = "kospi_M6"
    kospi_YTD = "kospi_YTD"

@app.get(path="/kospi/{indexType}",
         name="kospi지수의 D1,D5,M1,M6,YTD를 가져옴",
         #response_model=list12
        )
def consummer(indexType:Kospi_index):
    import json
    if indexType in Kospi_index:
        return dict(json.loads(rd.get(indexType)))
    else:
        raise HTTPException(status_code=404, detail="Item not found")

# kospi200_index----------------------------------------------------------------
# kospi200_D5
# kospi200_M1
# kospi200_M6
# kospi200_YTD
class Kospi200_index(str, Enum):
    kospi200_D1 = "kospi200_D1"
    kospi200_D5 ="kospi200_D5"
    kospi200_M1 = "kospi200_M1"
    kospi200_M6 = "kospi200_M6"
    kospi200_YTD = "kospi200_YTD"

@app.get(path="/kospi200/{indexType}",
         name="kospi200지수의 D1,D5,M1,M6,YTD를 가져옴",
         #response_model=kospi_kosdaq_API
         )
def consummer(indexType:Kospi200_index):
    if indexType in Kospi200_index:
        return dict(json.loads(rd.get(indexType)))
    else:
        raise HTTPException(status_code=404, detail="Item not found")
    
# kosdaq_index-----------------------------------------------------------------
# kosdaq_D5
# kosdaq_M1
# kosdaq_M6
# kosdaq_YTD
class Kosdaq(str, Enum):
    kosdaq_D1 = "kosdaq_D1"
    kosdaq_D5 = "kosdaq_D5"
    kosdaq_M1 = "kosdaq_M1"
    kosdaq_M6 = "kosdaq_M6"
    kosdaq_YTD = "kosdaq_YTD"

@app.get(path="/kosdaq/{indexType}",
         name="kosdaq지수의 D1,D5,M1,M6,YTD를 가져옴",
         #response_model=kospi_kosdaq_API
         )
def consummer(indexType:Kosdaq):
    if indexType in Kosdaq:
        #rd.get(indexType)
        return dict(json.loads(rd.get(indexType)))
    else:
        raise HTTPException(status_code=404, detail="Item not found")
    


if __name__ == "__main__":
    uvicorn.run(app, host="0.0.0.0", port=9199)