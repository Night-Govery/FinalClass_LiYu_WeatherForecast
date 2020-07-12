from concurrent.futures import ThreadPoolExecutor
import requests, time  ,os  ,sys ,io#导入requests包
from bs4 import BeautifulSoup
from retrying import retry

areas = ['changping','daxing','fangshan','huairou','mentougou','miyun','pinggu','shunyi','tongzhou','yanqing','beijing']
year = [2011, 2012, 2013, 2014, 2015, 2016, 2017, 2018, 2019, 2020]
month = [1, 2, 3, 4, 5, 6, 7, 8, 9, 10, 11, 12]


def mkdir(path):
    folder = os.path.exists(path)

    if not folder:  # 判断是否存在文件夹如果不存在则创建为文件夹
        os.makedirs(path)  # makedirs 创建文件时如果路径不存在会创建这个路径

@retry(stop_max_attempt_number=1)
def main():
    month = 12
    year = 2012
    area='changping'
    while month<=12:
        if month<10:
            str_month='0'+str(month)
        else:
            str_month=str(month)
        url='http://www.tianqihoubao.com/lishi/'+area+'/month/'+str(year)+str_month+'.html'
        strhtml=requests.get(url,timeout=5)
        soup=BeautifulSoup(strhtml.text,'lxml')
        data1 = soup.select('#main > div.dayDetails.center > div.dayExtras > div.highLowTemp.swip')
        for item in data1:
            result1={
                "title":item.get_text(),
            }
        path="process/"+area
        mkdir(path)
        fo = open(path+"/process_"+str(year)+str_month+'.txt', "w+", encoding="utf-8")
        for i in result1:
            if result1[i]:
                res = result1[i].replace("\n"," ")
                print(res)
                fo.write(str(res))
        fo.close()
        month=month+1


if __name__ == "__main__":
    start = time.time()
    '''
        for i in areas:
        area=i
        with ThreadPoolExecutor() as pool:
            pool.map(main, year)
    '''
    main()
    end = time.time()
    takeTime = end - start
    print(f"【总共耗时】{takeTime}")