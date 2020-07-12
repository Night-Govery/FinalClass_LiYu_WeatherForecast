from mod_timeseries.test import Arima
from mod_timeseries.test2 import Arima2


class Begin:
    def __init__(self, str):
        self.s = str

    def begin(self):

        u1,u2,u3= self.s.split('#',2)

        if u1=="北京":
            u1="00054511.csv"
            u2=int(u2)
            u3=int(u3)
            k=Arima(u2,u3,u1)
            k.arima()
        if u1=="昌平":
            u1="changping.csv"
            u2=int(u2)
            u3=int(u3)
            k=Arima2(u2,u3,u1)
            k.arima2()
        if u1=="大兴":
            u1="daxing.csv"
            u2=int(u2)
            u3=int(u3)
            k=Arima2(u2,u3,u1)
            k.arima2()
        if u1=="房山":
            u1="fangshan.csv"
            u2=int(u2)
            u3=int(u3)
            k=Arima2(u2,u3,u1)
            k.arima2()
        if u1=="怀柔":
            u1="huairou.csv"
            u2=int(u2)
            u3=int(u3)
            k=Arima2(u2,u3,u1)
            k.arima2()
        if u1=="门头沟":
            u1="mentougou.csv"
            u2=int(u2)
            u3=int(u3)
            k=Arima2(u2,u3,u1)
            k.arima2()
        if u1=="密云":
            u1="miyun.csv"
            u2=int(u2)
            u3=int(u3)
            k=Arima2(u2,u3,u1)
            k.arima2()
        if u1=="平谷":
            u1="pinggu.csv"
            u2=int(u2)
            u3=int(u3)
            k=Arima2(u2,u3,u1)
            k.arima2()
        if u1=="顺义":
            u1="shunyi.csv"
            u2=int(u2)
            u3=int(u3)
            k=Arima2(u2,u3,u1)
            k.arima2()
        if u1=="通州":
            u1="tongzhou.csv"
            u2=int(u2)
            u3=int(u3)
            k=Arima2(u2,u3,u1)
            k.arima2()
        if u1=="延庆":
            u1="yanqing.csv"
            u2=int(u2)
            u3=int(u3)
            k=Arima2(u2,u3,u1)
            k.arima2()