import pandas as pd#为了方便实用pandas 采用pd简写

from pyspark import SparkContext

from datetime import datetime
from dateutil import parser


data_raw = pd.read_csv('00054511.csv',encoding='utf-8')

data_raw['date'] = data_raw['DATE'].apply(parser.parse)
data_raw['tmax'] = data_raw['TMAX'].astype(float)
data_raw['tmin'] = data_raw['TMIN'].astype(float)
data = data_raw.loc[:,['date','tmax','tmin']]
data = data[(pd.Series.notnull(data['tmax'])) & (pd.Series.notnull(data['tmin']))]
data = data[(data['date'] >= datetime(1980,1,1)) & (data['date'] <= datetime(2016,1,1))]
data.query("date.dt.day == 28 & date.dt.month == 6", inplace=True)
data.to_csv('maxmin.csv', index=None)
