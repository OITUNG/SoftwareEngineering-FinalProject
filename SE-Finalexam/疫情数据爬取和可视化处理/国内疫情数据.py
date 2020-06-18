import pandas as pd
import requests
import json
from pyecharts.charts import Map
from pyecharts.charts import Bar,Line
from pyecharts import options as opts
import pandas as np
from pymysql import connect

def getData():
    url = 'https://view.inews.qq.com/g2/getOnsInfo?name=disease_h5'
    headers = {
        'user-agent': 'Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/81.0.4044.122 Safari/537.36'
    }
    r = requests.get(url, headers)
    if r.status_code == 200:
        return json.loads(json.loads(r.text)['data'])
data_dict = getData()
print(data_dict.keys())


#每一个省的疫情数据
province_list = list()
for province in data_dict.get('areaTree')[0]['children']:
    province_info = province['total']
    province_info['name'] = province['name']
    province_list.append(province_info)
province_df = pd.DataFrame(province_list)
province_df = province_df.select_dtypes(exclude=['bool'])
province_df.drop([], axis=1, inplace=True)
province_df.drop(['deadRate'], axis=1, inplace=True)
province_df.drop(['healRate'], axis=1, inplace=True)
province_df.to_excel("g:/sp/国家每个省份疫情数据.xlsx")
name = province_df.name.tolist()
confirm = province_df.confirm.tolist()
nowConfirm =province_df.nowConfirm.tolist()
bar = Bar()                                                               #国家每个省份疫情数据
x = name
y1 = confirm
y2 = nowConfirm
bar.add_xaxis(x)
bar.add_yaxis("累计确诊",y1)
bar.add_yaxis("现有确诊",y2)
bar.render('g:/sp/国家每个省份疫情数据.html')
#保存国家疫情数据总数
total = data_dict['chinaTotal']
total['date'] = data_dict['lastUpdateTime'].split()[0]
total_df = pd.DataFrame(pd.Series(total)).T
total_df.to_csv("g:/sp/国家疫情总数.csv")

for i in total_df.iloc[:,:-1].columns:
    total_df.loc[:,i] = total_df.loc[:,i].astype('int32')
total_df.loc[:,'date'] = pd.to_datetime(total_df.loc[:,'date'])

#国家总数
country_list = list()
for country in data_dict['areaTree']:
#     print(data_dict['lastUpdateTime'],country['name'],country['today'],country['total'])
    country_dict = country['total']
    country_dict['add_confirm'] = country['today']['confirm']
    country_dict['name'] = country['name']
    country_dict['date'] = data_dict['lastUpdateTime']
    country_list.append(country_dict)
country_df = pd.DataFrame(country_list)
country_df= country_df.select_dtypes(exclude=['bool'])

#国家地区总数
city_list = list()
for pro in data_dict['areaTree'][0]['children']:
    for city in pro['children']:
        city_dict = city['total']
        city_dict['add_confirm'] = city['today']['confirm']
        city_dict['city_name'] = city['name']
        city_dict['province_name'] = pro['name']
        city_dict['date'] = data_dict['lastUpdateTime']
        city_list.append(city_dict)
city_df = pd.DataFrame(city_list)
city_df= city_df.select_dtypes(exclude=['bool'])
city_df.date = pd.to_datetime(city_df.date)
city_df.to_csv('g:/sp/国内地区数据.csv')
#city_name = city_df.confirm.tolist()
#print(city_name)
province_name = province_df.name.tolist()
province_confirm = province_df.confirm.tolist()
pieces = [                    #颜色配置
    {'min': 1, 'max': 9, 'color': '#FFE0E0'},
    {'min': 10, 'max': 99, 'color': '#FFC0C0'},
    {'min': 100, 'max': 499, 'color': '#FF9090'},
    {'min': 500, 'max': 999, 'color': '#FF6060'},
    {'min': 1000, 'max': 9999, 'color': '#FF3030'},
    {'min': 10000, 'color': '#DD0000'},
]
china_map = Map()                                                     #中国疫情地图
#定义地图,填充数据
china_map.add('地区累计确诊',[tup for tup in zip(province_name,province_confirm)],'china')
#颜色配置
china_map.set_global_opts(title_opts=opts.TitleOpts(title=''),\
                         visualmap_opts=opts.VisualMapOpts(is_piecewise=True,pieces=pieces))
#打印地图
china_map.render('g:/sp/中国疫情地图.html')