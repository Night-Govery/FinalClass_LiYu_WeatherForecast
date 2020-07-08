import pandas as pd#为了方便实用pandas 采用pd简写

from mod_timeseries.weather_training2 import Training2
from mod_timeseries.weather_traning import Training
from pyspark import SparkContext

from datetime import datetime, date
from dateutil import parser


class Arima:
    def __init__(self, month, day):
        self.m = month
        self.d = day

    def arima(self):
        with open('predict.json', 'w', encoding='utf-8') as f:
            f.truncate()

        for i in range(self.d, self.d + 7):
            data_raw = pd.read_csv('00054511.csv',encoding='utf-8')
            data_raw['date'] = data_raw['DATE'].apply(parser.parse)
            data_raw['tmax'] = data_raw['TMAX'].astype(float)
            data_raw['tmin'] = data_raw['TMIN'].astype(float)
            data = data_raw.loc[:, ['date','tmax','tmin']]
            data = data[(pd.Series.notnull(data['tmax'])) & (pd.Series.notnull(data['tmin']))]
            data = data[(data['date'] >= datetime(1980, 1, 1)) & (data['date'] <= datetime(2013, 1, 1))]

            data.query(f"date.dt.day =={i} & date.dt.month =={self.m}", inplace=True)
            data.to_csv('maxmin.csv', index=None)


            m=Training2()
            m.training2()
            n=Training()
            n.training()

