from concurrent.futures import ThreadPoolExecutor

import requests, time      #导入requests包
from bs4 import BeautifulSoup


def main(year):
    month=12
    while month<=12:
    # if month<10:
    #    str_month='0'+str(month)
        str_month=str(month)
        url='http://www.tianqihoubao.com/lishi/beijing/month/'+str(year)+str_month+'.html'
        strhtml=requests.get(url)
        soup=BeautifulSoup(strhtml.text,'lxml')
        data = soup.select('#content > table')

        for item in data:
            result={
                "title":item.get_text(),
            }

        fo = open("process/process_"+str(year)+str_month+'.txt', "w+")
        for i in result:
            if result[i]:
                res = result[i].replace(" ","")
                res = res.replace("\n", "")
                res = res.replace("/", "")
                fo.write(res)
        fo.close()
        month=month+1

if __name__ == "__main__":
    start = time.time()
    year = [2012,2013,2014,2015,2016,2017,2018,2019,2020]
    month = [1,2,3,4,5,6,7,8,9,10,11,12]
    with ThreadPoolExecutor() as pool:
        pool.map(main, year)

    end = time.time()
    takeTime = end - start
    print(f"【总共耗时】{takeTime}")