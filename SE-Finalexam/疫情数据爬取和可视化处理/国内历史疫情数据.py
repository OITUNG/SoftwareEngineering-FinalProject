import pandas as pd
import pymysql
import requests
import json
import pandas as np
from pymysql import connect
from pyecharts.charts import Line

def getData():
    url = 'https://view.inews.qq.com/g2/getOnsInfo?name=disease_other'
    headers = {
        'user-agent': 'Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/81.0.4044.122 Safari/537.36'
    }
    r = requests.get(url, headers)
    if r.status_code == 200:
        return json.loads(json.loads(r.text)['data'])
data_dict = getData()
print(data_dict.keys())
#print(data_dict['chinaDayList'])

#国家历史疫情数据
history_list = list()
for history in data_dict.get('chinaDayList'):
    history_info = history
    history_list.append(history_info)
history_df = pd.DataFrame(history_list)
history_df = history_df.select_dtypes(exclude=['bool'])
history_df.to_csv("g:/sp/国家历史疫情数据.csv")
history_confirm = history_df.confirm.tolist()
history_date = history_df.date.tolist()
bar = Line()
x = history_date
y = history_confirm
bar.add_xaxis(x)
bar.add_yaxis("",y)
bar.render("g:/sp/国家历史疫情数据.html")




