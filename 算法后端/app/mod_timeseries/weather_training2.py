import pandas as pd
import numpy as np
from pmdarima import auto_arima
from scipy import  stats
import matplotlib.pyplot as plt
import statsmodels.api as sm
from statsmodels.graphics.api import qqplot


from process_json import format_json
from datetime import datetime


class Training2:
    def training2(self):
        data = pd.read_csv('maxmin.csv', parse_dates=['date'])
        dta = data['tmax']
        dta_year = data['date']
        # 得到开始年份和结束年份
        begin_year = dta_year[0:1].dt.year # index   value
        end_year = dta_year[-1:].dt.year
        predict_month = dta_year[0:1].dt.month
        predict_day = dta_year[0:1].dt.day

        #设置数据类型
        dta=np.array(dta,dtype=np.float)
        #转换为Series类型的一维数组
        dta=pd.Series(dta)
        dta.index=pd.Index(sm.tsa.datetools.dates_from_range(str(begin_year.values[0]), str(end_year.values[0])))
        #dta.plot(figsize=(10,6))
        #plt.show()

        #fig = plt.figure(figsize=(12,8))
        #ax1= fig.add_subplot(111)
        #diff1 = dta.diff(1)
        #diff1.plot(ax=ax1)
        #plt.show()


        #diff1= dta.diff(1)
        #fig = plt.figure(figsize=(12,8))
        #ax1=fig.add_subplot(211)
        #fig = sm.graphics.tsa.plot_acf(dta,lags=30,ax=ax1)
        #ax2 = fig.add_subplot(212)
        #fig = sm.graphics.tsa.plot_pacf(dta,lags=30,ax=ax2)
        #plt.show()

        #arma_mod76 = sm.tsa.ARMA(dta,(7,6)).fit()

        #print(arma_mod76.aic,arma_mod76.bic,arma_mod76.hqic)

        '''
        使用ARMA(7,6)模型
        '''
        #resid = arma_mod76.resid
        #fig = plt.figure(figsize=(12,8))
        #ax1 = fig.add_subplot(211) #2行,第1列,第1个起始位置
        #fig = sm.graphics.tsa.plot_acf(resid.values.squeeze(), lags=30, ax=ax1)
        #ax2 = fig.add_subplot(212)#2行,第1列,第2个起始位置
        #fig = sm.graphics.tsa.plot_pacf(resid, lags=30, ax=ax2)
        #plt.show()

        #fig = plt.figure(figsize=(12,8))
        #ax = fig.add_subplot(111)
        #fig = qqplot(resid, line='q', ax=ax, fit=True)
        # plt.show()

        #predict_year = 8
        #predict_end_year = end_year.values[0]+predict_year
        #predict_dta = arma_mod76.predict(str(end_year.values[0]), str(predict_end_year),dynamic=True)
        #print(dta)

        train = dta.loc['1980-12-31':'2018-12-31']
        test = dta.loc['2018-12-31':'2020-12-31']
        stepwise_model = auto_arima(train, start_p=0, start_q=0,
                                    max_p=10, max_q=10, m=12,
                                    start_P=0, seasonal=True,
                                    d=None, D=1, trace=True,
                                    error_action='ignore',
                                    suppress_warnings=True,
                                    stepwise=True)
        print(stepwise_model.aic())
        stepwise_model.fit(train)

        future_forecast = stepwise_model.predict(n_periods=len(test))
        future_forecast = pd.DataFrame(future_forecast, index=test.index, columns=['Prediction'])


        import json
        with open('predict.json', 'a', encoding='utf-8') as f:
            # format_json(f, predict_month, predict_day)
            # print(str(future_forecast.to_json()).replace('\\', ''))
            # print(type(future_forecast.to_json()))
            # print(future_forecast.to_json())
            new = eval(future_forecast.to_json())
            for k, v in new['Prediction'].items():
                timestamp = int(k) / 1000
                date = datetime.fromtimestamp(timestamp).strftime('%Y/%m/%d')

                if '2020' in str(date):
                    print('--test--')
                    v = str(v)
                    dd = '"'+'2020/' + str(predict_month[0]) + '/' + str(predict_day[0])+'"' + ':'+v+','
                    print(dd)
                    #json.dump({dd: v}, f)
        return (dd)
        # print(future_forecast)
        print('--test--')






            #print('--test--')
        #p = ProcessData2(data,8,'max')
        #p.process_minmax2()

