
from vnstockdata.client.login import Client
from vnstockdata.config.config import base_url
import requests 
import pandas as pd 
from datetime import datetime


def get_price(ticker:str,fromDate:str,toDate):
    client = Client()
    try:
        fromDate_dt=datetime.strptime(fromDate,'%Y-%m-%d')
        toDate_dt=datetime.strptime(toDate,'%Y-%m-%d')
    except Exception as e:
        print(e)
        raise ValueError(f'''Lỗi định dạng: fromDate | toDate cần là: "yyyy-mm-dd"
Dữ liệu input của bạn:
fromDate: {fromDate}
toDate: {toDate}
Hãy kiểm tra lại''')
  
    headers = client._get_headers()
    url=f"{base_url}/api/historical"
    params={
        'ticker':ticker,
        'fromDate':fromDate,
        'toDate':toDate
    }
    response=requests.get(
        url=url, 
        headers=headers,
        params=params
    )
    if response.status_code==200:
        data=pd.DataFrame(response.json())
        return data 
    else:
        raise ValueError(f'''Có lỗi xảy ra
Chi tiết: 
status:{response.status_code}
content: {response.detail}''')
    