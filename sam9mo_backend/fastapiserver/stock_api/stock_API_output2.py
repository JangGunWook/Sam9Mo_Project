"""
해당 접근토큰발급관리 파일을 그대로 사용하시면 오류 발생할 수 있습니다.
토큰저장 및 발급 함수 등을 참고하시되 본인 환경에 맞게 코드 수정하셔서 사용하시기 바랍니다.

Created on Wed Feb 15 16:57:19 2023

@author: Administrator
"""
from pymongo.errors import DuplicateKeyError
from pymongo import MongoClient
from datetime import datetime, timedelta
import time, copy
import yaml
import requests
import json

import os

import pandas as pd

from collections import namedtuple
from datetime import datetime

config_root = os.getcwd() + '\\'
# config_root = 'd:\\KIS\\config\\'  # 토큰 파일이 저장될 폴더, 제3자가 찾지 어렵도록 경로 설정하시기 바랍니다.
#token_tmp = config_root + 'KIS000000'  # 토큰 로컬저장시 파일 이름 지정, 파일이름을 토큰값이 유추가능한 파일명은 삼가바랍니다.
#token_tmp = config_root + 'KIS' + datetime.today().strftime("%Y%m%d%H%M%S")  # 토큰 로컬저장시 파일명 년월일시분초
token_tmp = config_root + 'KIS' + datetime.today().strftime("%Y%m%d")  # 토큰 로컬저장시 파일명 년월일

# 접근토큰 관리하는 파일 존재여부 체크, 없으면 생성
if os.path.exists(token_tmp) == False:
    f = open(token_tmp, "w+")

# 앱키, 앱시크리트, 토큰, 계좌번호 등 저장관리, 자신만의 경로와 파일명으로 설정하시기 바랍니다.
# pip install PyYAML (패키지설치)
with open(config_root + 'kis_devlp.yaml', encoding='UTF-8') as f:
    _cfg = yaml.load(f, Loader=yaml.FullLoader)

_TRENV = tuple()
_last_auth_time = datetime.now()
_autoReAuth = False
_DEBUG = False
_isPaper = False

# 기본 헤더값 정의
_base_headers = {
    "Content-Type": "application/json",
    "Accept": "text/plain",
    "charset": "UTF-8",
    'User-Agent': _cfg['my_agent']
}

# 토큰 발급 받아 저장 (토큰값, 토큰 유효시간,1일, 6시간 이내 발급신청시는 기존 토큰값과 동일, 발급시 알림톡 발송)
def save_token(my_token, my_expired):
    valid_date = datetime.strptime(my_expired, '%Y-%m-%d %H:%M:%S')
    print('Save token date: ', valid_date)
    with open(token_tmp, 'w', encoding='utf-8') as f:
        f.write(f'token: {my_token}\n')
        f.write(f'valid-date: {valid_date}\n')


# 토큰 확인 (토큰값, 토큰 유효시간_1일, 6시간 이내 발급신청시는 기존 토큰값과 동일, 발급시 알림톡 발송)
def read_token():
    try:
        # 토큰이 저장된 파일 읽기
        with open(token_tmp, encoding='UTF-8') as f:
            tkg_tmp = yaml.load(f, Loader=yaml.FullLoader)

        # 토큰 만료 일,시간
        exp_dt = datetime.strftime(tkg_tmp['valid-date'], '%Y-%m-%d %H:%M:%S')
        # 현재일자,시간
        now_dt = datetime.today().strftime("%Y-%m-%d %H:%M:%S")

        print('expire dt: ', exp_dt, ' vs now dt:', now_dt)
        # 저장된 토큰 만료일자 체크 (만료일시 > 현재일시 인경우 보관 토큰 리턴)
        if exp_dt > now_dt:
            return tkg_tmp['token']
        else:
            # print('Need new token: ', tkg_tmp['valid-date'])
            return None
    except Exception as e:
        # print('read token error: ', e)
        return None

# 토큰 유효시간 체크해서 만료된 토큰이면 재발급처리
def _getBaseHeader():
    if _autoReAuth: reAuth()
    return copy.deepcopy(_base_headers)


# 가져오기 : 앱키, 앱시크리트, 종합계좌번호(계좌번호 중 숫자8자리), 계좌상품코드(계좌번호 중 숫자2자리), 토큰, 도메인
def _setTRENV(cfg):
    nt1 = namedtuple('KISEnv', ['my_app', 'my_sec', 'my_acct', 'my_prod', 'my_token', 'my_url'])
    d = {
        'my_app': cfg['my_app'],  # 앱키
        'my_sec': cfg['my_sec'],  # 앱시크리트
        'my_acct': cfg['my_acct'],  # 종합계좌번호(8자리)
        'my_prod': cfg['my_prod'],  # 계좌상품코드(2자리)
        'my_token': cfg['my_token'],  # 토큰
        'my_url': cfg['my_url']  # 실전 도메인 (https://openapi.koreainvestment.com:9443)
    }  # 모의 도메인 (https://openapivts.koreainvestment.com:29443)

    global _TRENV
    _TRENV = nt1(**d)


def isPaperTrading():  # 모의투자 매매
    return _isPaper


# 실전투자면 'prod', 모의투자면 'vps'를 셋팅 하시기 바랍니다.
def changeTREnv(token_key, svr='prod', product='01'):
    cfg = dict()

    global _isPaper
    if svr == 'prod':  # 실전투자
        ak1 = 'my_app'  # 실전투자용 앱키
        ak2 = 'my_sec'  # 실전투자용 앱시크리트
        _isPaper = False
    elif svr == 'vps':  # 모의투자
        ak1 = 'paper_app'  # 모의투자용 앱키
        ak2 = 'paper_sec'  # 모의투자용 앱시크리트
        _isPaper = True

    cfg['my_app'] = _cfg[ak1]
    cfg['my_sec'] = _cfg[ak2]

    if svr == 'prod' and product == '01':  # 실전투자 주식투자, 위탁계좌, 투자계좌
        cfg['my_acct'] = _cfg['my_acct_stock']
    elif svr == 'prod' and product == '03':  # 실전투자 선물옵션(파생)
        cfg['my_acct'] = _cfg['my_acct_future']
    elif svr == 'vps' and product == '01':  # 모의투자 주식투자, 위탁계좌, 투자계좌
        cfg['my_acct'] = _cfg['my_paper_stock']
    elif svr == 'vps' and product == '03':  # 모의투자 선물옵션(파생)
        cfg['my_acct'] = _cfg['my_paper_future']

    cfg['my_prod'] = product
    cfg['my_token'] = token_key
    cfg['my_url'] = _cfg[svr]

    _setTRENV(cfg)


def _getResultObject(json_data):
    _tc_ = namedtuple('res', json_data.keys())

    return _tc_(**json_data)


# Token 발급, 유효기간 1일, 6시간 이내 발급시 기존 token값 유지, 발급시 알림톡 무조건 발송
def auth(svr='prod', product='01', url=None):
    p = {
        "grant_type": "client_credentials",
    }
    # 개인 환경파일 "kis_devlp.yaml" 파일을 참조하여 앱키, 앱시크리트 정보 가져오기
    # 개인 환경파일명과 위치는 고객님만 아는 위치로 설정 바랍니다.
    if svr == 'prod':  # 실전투자
        ak1 = 'my_app'  # 앱키 (실전투자용)
        ak2 = 'my_sec'  # 앱시크리트 (실전투자용)
    elif svr == 'vps':  # 모의투자
        ak1 = 'paper_app'  # 앱키 (모의투자용)
        ak2 = 'paper_sec'  # 앱시크리트 (모의투자용)

    # 앱키, 앱시크리트 가져오기
    p["appkey"] = _cfg[ak1]
    p["appsecret"] = _cfg[ak2]

    # 기존 발급된 토큰이 있는지 확인
    saved_token = read_token()  # 기존 발급 토큰 확인
    print("saved_token: ", saved_token)
    if saved_token is None:  # 기존 발급 토큰 확인이 안되면 발급처리
        url = f'{_cfg[svr]}/oauth2/tokenP'
        res = requests.post(url, data=json.dumps(p), headers=_getBaseHeader())  # 토큰 발급
        rescode = res.status_code
        if rescode == 200:  # 토큰 정상 발급
            my_token = _getResultObject(res.json()).access_token  # 토큰값 가져오기
            my_expired= _getResultObject(res.json()).access_token_token_expired  # 토큰값 만료일시 가져오기
            save_token(my_token, my_expired)  # 새로 발급 받은 토큰 저장
        else:
            print('Get Authentification token fail!\nYou have to restart your app!!!')
            return
    else:
        my_token = saved_token  # 기존 발급 토큰 확인되어 기존 토큰 사용

    # 발급토큰 정보 포함해서 헤더값 저장 관리, API 호출시 필요
    changeTREnv(f"Bearer {my_token}", svr, product)

    _base_headers["authorization"] = _TRENV.my_token
    _base_headers["appkey"] = _TRENV.my_app
    _base_headers["appsecret"] = _TRENV.my_sec

    global _last_auth_time
    _last_auth_time = datetime.now()

    if (_DEBUG):
        print(f'[{_last_auth_time}] => get AUTH Key completed!')


# end of initialize, 토큰 재발급, 토큰 발급시 유효시간 1일
# 프로그램 실행시 _last_auth_time에 저장하여 유효시간 체크, 유효시간 만료시 토큰 발급 처리
def reAuth(svr='prod', product='01'):
    n2 = datetime.now()
    if (n2 - _last_auth_time).seconds >= 86400:  # 유효시간 1일
        auth(svr, product)

# 접근토큰발급 저장
auth()
# 접근토큰 조회
gettoken = read_token()
print(gettoken)

# 국내주식기간별시세(일/주/월/년)
def get_domestic_stock_price(stock_no:str,start_day:str,end_day:str):
    PATH = "uapi/domestic-stock/v1/quotations/inquire-daily-itemchartprice"
    URL = f"{_cfg['prod']}/{PATH}"

    # 헤더 설정
    headers = {"Content-Type":"application/json", 
            "authorization": f"Bearer {gettoken}",
            "appKey": _cfg['my_app'],
            "appSecret":_cfg['my_sec'],
            "tr_id":"FHKST03010100",
            "custtype":"P"
            }
    # Query Parameter
    params = {
        "fid_cond_mrkt_div_code":"J",
        "fid_input_iscd": stock_no,
        "fid_input_date_1" : start_day,    #시작일자
        "fid_input_date_2" : end_day,    #종료일자
        "fid_period_div_code" : "D",
        "fid_org_adj_prc" : "0"
    }

    # 호출
    res = requests.get(URL, headers=headers, params=params)

    if res.status_code == 200 and res.json()["rt_cd"] == "0" :
        #print(res.json())    
        return(res.json())
    
    # 토큰 만료 시
    elif res.status_code == 200 and res.json()["msg_cd"] == "EGW00123" :
        auth()
        get_domestic_stock_price(stock_no)
    else:
        print("Error Code : " + str(res.status_code) + " | " + res.text)
        return None
#----------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------
# kospi_stock = kospi_stock_number()
KOSPI_STOCK_CODE = ['005930', '373220', '000660', '207940', '005935',
               '005490', '005380', '051910', '035420', '000270', 
               '006400', '068270', '003670', '035720', '105560',
               '028260', '012330', '055550', '066570', '096770', 
               '032830', '003550', '323410', '033780', '086790', 
               '000810', '034730', '015760', '138040', '017670', 
               '018260', '011200', '329180', '010130', '009150', 
               '047050', '259960', '316140', '034020', '024110'] 
               
# kosdaq_stock = kosdaq_stock_number()
KOSDAQ_STOCK_CODE = ['247540', '086520', '091990', '022100', '066970', 
                '028300', '196170', '068760', '035900', '277810', 
                '403870', '058470', '263750', '214150', '293490', 
                '357780', '041510', '039030', '145020', '005290', 
                '095340', '112040', '240810', '036930', '253450', 
                '035760', '000250', '086900', '121600', '214370', 
                '067310', '393890', '025900', '034230', '237690', 
                '078600', '048410', '141080', '365340', '195940']


# for code in KOSPI_STOCK_CODE: 
#     try:
#         get_domestic_stock_price(code,20231127,20231127)
#     except Exception as e :
#         print(e)

# for code in KOSDAQ_STOCK_CODE: 
#     try:
#         get_domestic_stock_price(code,20231127,20231127)
#     except Exception as e :
#         print(e)

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


# # 오늘 날짜 가져오기
# today = datetime.today().strftime("%Y%m%d")


# STOCK_CODE_TICKERS = {}
# # 초기값을 몽고DB의 
# for key, value in STOCK_CODE.items():
#     result = get_domestic_stock_price(key,today,today)
#     if result:
#         stock_data = result["output1"]
#         if stock_data:
#             stock_data["COMPANY"] = value
#             STOCK_CODE_TICKERS[key] = {
#                 "initial":stock_data,    # API로 가져온 값
#                 "current_trade": ""         # 변화되는 거래값 
#                 }
            

# print(STOCK_CODE_TICKERS)