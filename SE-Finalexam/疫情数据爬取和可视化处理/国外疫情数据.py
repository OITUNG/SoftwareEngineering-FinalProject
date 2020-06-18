import pandas as pd
import requests
import json
from pyecharts import options as opts
from pyecharts.charts import Bar,Line




def getData():
    url = 'https://view.inews.qq.com/g2/getOnsInfo?name=disease_foreign'
    headers = {
        'user-agent': 'Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/81.0.4044.122 Safari/537.36'
    }
    r = requests.get(url, headers)
    if r.status_code == 200:
        return json.loads(json.loads(r.text)['data'])


data_dict = getData()
print(data_dict.keys())

# 获取国外疫情数据日期（做趋势图用）
dateAll_list = list()
for dateAll in data_dict.get('globalDailyHistory'):
    dateAll_info = dateAll['all']
    dateAll_info['date'] = dateAll['date']
    dateAll_list.append(dateAll_info)
dateAll_df = pd.DataFrame(dateAll_list)
dateAll_df = dateAll_df.select_dtypes(exclude=['bool'])
dateAll_df.to_csv("g:/sp/国外历史数据.csv")
dateAll_confirm = dateAll_df.confirm.tolist()
dateAll_heal = dateAll_df.heal.tolist()
dateAll_date = dateAll_df.date.tolist()
line = Line()  # 海外疫情历史趋势
x = dateAll_date
y1 = dateAll_confirm
y2 = dateAll_heal
line.add_xaxis(x)
line.add_yaxis('累计确诊',y1)
line.add_yaxis('累计治愈',y2)
line.render("g:/sp/海外疫情历史趋势.html")
# 获取国家名称和数据
print(data_dict['globalStatis'])

areaAll_list = list()
for areaAll in data_dict.get('foreignList'):
    areaAll_info = areaAll
    areaAll_list.append(areaAll_info)
areaAll_df = pd.DataFrame(areaAll_list)
areaAll_df.drop(['children'], axis=1, inplace=True)
areaAll_df.to_csv("g:/sp/国外地区疫情数据.csv")
areaAll_name = areaAll_df.name.tolist()
areaAll_confirm = areaAll_df.confirm.tolist()
areaAll_dead = areaAll_df.dead.tolist()
areaAll_heal = areaAll_df.heal.tolist()

# 几大国家数据
nation_list = list()
for nation in data_dict.get('countryAddConfirmRankList'):
    nation_info = nation
    nation_list.append(nation_info)
nation_df = pd.DataFrame(nation_list)
nation_df.to_csv("g:/sp/国外几大国家.csv")
nation = nation_df.nation.tolist()
nation_Addconfirm = nation_df.addConfirm.tolist()
bar = Bar()# 海外几大国家新增疫情
x = nation
y = nation_Addconfirm
bar.add_xaxis(x)
bar.add_yaxis('累计确诊',y)
bar.render('g:/sp/海外几大国家新增疫情.html')
