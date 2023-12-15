import requests
import redis
import json
from datetime import datetime

kospi_D5_api_url = "https://query1.finance.yahoo.com/v8/finance/chart/%5EKS11?region=US&lang=en-US&includePrePost=false&interval=15m&range=5d&corsDomain=search.yahoo.com"
kospi_M1_api_url = "https://query1.finance.yahoo.com/v8/finance/chart/%5EKS11?region=US&lang=en-US&includePrePost=false&interval=30m&range=1mo&corsDomain=search.yahoo.com"
kospi_M6_api_url = "https://query1.finance.yahoo.com/v8/finance/chart/%5EKS11?region=US&lang=en-US&includePrePost=false&interval=1d&range=6mo&corsDomain=search.yahoo.com"
kospi_YTD_api_url = "https://query1.finance.yahoo.com/v8/finance/chart/%5EKS11?region=US&lang=en-US&includePrePost=false&interval=1d&range=ytd&corsDomain=search.yahoo.com"

kospi200_D5_api_url = "https://query1.finance.yahoo.com/v8/finance/chart/%5EKS200?region=US&lang=en-US&includePrePost=false&interval=15m&useYfid=true&range=5d&corsDomain=finance.yahoo.com&.tsrc=finance"
kospi200_M1_api_url = "https://query1.finance.yahoo.com/v8/finance/chart/%5EKS200?region=US&lang=en-US&includePrePost=false&interval=30m&useYfid=true&range=1mo&corsDomain=finance.yahoo.com&.tsrc=finance"
kospi200_M6_api_url = "https://query1.finance.yahoo.com/v8/finance/chart/%5EKS200?region=US&lang=en-US&includePrePost=false&interval=1d&useYfid=true&range=6mo&corsDomain=finance.yahoo.com&.tsrc=finance"
kospi200_YTD_api_url = "https://query1.finance.yahoo.com/v8/finance/chart/%5EKS200?region=US&lang=en-US&includePrePost=false&interval=1d&useYfid=true&range=ytd&corsDomain=finance.yahoo.com&.tsrc=finance"

kosdaq_D5_api_url = "https://query1.finance.yahoo.com/v8/finance/chart/%5EKQ11?region=US&lang=en-US&includePrePost=false&interval=15m&useYfid=true&range=5d&corsDomain=finance.yahoo.com&.tsrc=finance"
kosdaq_M1_api_url = "https://query1.finance.yahoo.com/v8/finance/chart/%5EKQ11?region=US&lang=en-US&includePrePost=false&interval=30m&useYfid=true&range=1mo&corsDomain=finance.yahoo.com&.tsrc=finance"
kosdaq_M6_api_url = "https://query1.finance.yahoo.com/v8/finance/chart/%5EKQ11?region=US&lang=en-US&includePrePost=false&interval=1d&useYfid=true&range=6mo&corsDomain=finance.yahoo.com&.tsrc=finance"
kosdaq_YTD_api_url ="https://query1.finance.yahoo.com/v8/finance/chart/%5EKQ11?region=US&lang=en-US&includePrePost=false&interval=1d&useYfid=true&range=ytd&corsDomain=finance.yahoo.com&.tsrc=finance"

custom_user_agent = 'Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/119.0.0.0 Safari/537.36'  # Replace with your desired User-Agent string


def kos_index(url, custom_user_agent):
    # Adding headers with a custom User-Agent
    headers = {
        'User-Agent': custom_user_agent
    }

    index = {}

    # Sending a GET request to the API with custom headers
    response = requests.get(url, headers=headers)
    print(response.status_code, "OK")
    if response.status_code == 200:
        data = response.json()
        index = data
    else:
        print(f"Failed to retrieve data. Status code: {response.status_code}")

    data_sum = []

    result_data = index['chart']['result']

    for result_item in result_data:
        timestamps = result_item['timestamp']
        quotes = result_item['indicators']['quote']

    for ind, timestamp in enumerate(timestamps):
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


def DWMY_kospi_kosdaq_index():
    print("start")
    # kospi
    kospi_d5=kos_index(kospi_D5_api_url,custom_user_agent)
    kospi_m1=kos_index(kospi_M1_api_url,custom_user_agent)
    kospi_m6=kos_index(kospi_M6_api_url,custom_user_agent)
    kospi_ytd=kos_index(kospi_YTD_api_url,custom_user_agent)
    # kospi200
    kospi200_d5=kos_index(kospi200_D5_api_url,custom_user_agent)
    kospi200_m1=kos_index(kospi200_M1_api_url,custom_user_agent)
    kospi200_m6=kos_index(kospi200_M6_api_url,custom_user_agent)
    kospi200_ytd=kos_index(kospi200_YTD_api_url,custom_user_agent)
    #kosdaq
    kosdaq_d5=kos_index(kosdaq_D5_api_url,custom_user_agent)
    kosdaq_m1=kos_index(kosdaq_M1_api_url,custom_user_agent)
    kosdaq_m6=kos_index(kosdaq_M6_api_url,custom_user_agent)
    kosdaq_ytd=kos_index(kosdaq_YTD_api_url,custom_user_agent)


    # 레디스 연결
    rd = redis.StrictRedis(host='59.3.28.12', port=6379, db=0, password='sam9mo!!')
    # 레디스 전송
    # str형변환 꼭해야함!!
    #kospi
    print("save")
    rd.set("kospi_D5",str(kospi_d5))
    rd.set("kospi_M1",str(kospi_m1))
    rd.set("kospi_M6",str(kospi_m6))
    rd.set("kospi_YTD",str(kospi_ytd))
    #kospi200
    rd.set("kospi200_D5",str(kospi200_d5))
    rd.set("kospi200_M1",str(kospi200_m1))
    rd.set("kospi200_M6",str(kospi200_m6))
    rd.set("kospi200_YTD",str(kospi200_ytd))
    #kosdaq
    rd.set("kosdaq_D5",str(kosdaq_d5))
    rd.set("kosdaq_M1",str(kosdaq_m1))
    rd.set("kosdaq_M6",str(kosdaq_m6))
    rd.set("kosdaq_YTD",str(kosdaq_ytd))

    print("kospi, kosdaq, kospi200의 지표가 Redis로 올라갔습니다")



