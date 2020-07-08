import pandas as pd
import numpy as np


from datetime import datetime, date
from dateutil import parser


meta_data = pd.read_csv('00054511.csv', encoding='utf-8')

data = pd.DataFrame()
# data['date'] = meta_data['DATE']
# data['max'] = meta_data['TMAX']
# data['min'] = meta_data['TMIN']


data['date'] = meta_data['DATE'].apply(parser.parse)
data['tmax'] = meta_data['TMAX'].astype(float)
data['tmin'] = meta_data['TMIN'].astype(float)


# 删除有空值的数据
data = data.dropna()
data = data.loc[:, ['date','tmax','tmin']]
data = data[(pd.Series.notnull(data['tmax'])) & (pd.Series.notnull(data['tmin']))]
data = data[(data['date'] >= datetime(1980,6,1)) & (data['date'] <= datetime(2020,6,26))]
print(data.query("date.dt.day == 7 & date.dt.month == 7", inplace=True))



# import json
# with open('data.json', 'a') as f:
#     record = {}
#     for index, row in data.iterrows():
#         record[row[0]] = [row[1], row[2]]
#         print(index)
#
#     json.dump(record, f)
#     print('Writer Success!')

