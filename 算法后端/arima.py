from test import Arima

class Begin:
    def __init__(self, str):
        self.s = str

    def begin(self):

        u1,u2= self.s.split('#',1)

        u1=int(u1)
        u2=int(u2)
        k=Arima(u1,u2)
        k.arima()