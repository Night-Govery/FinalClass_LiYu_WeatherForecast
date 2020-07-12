import  xlwt, os


def mkdir(path):
    folder = os.path.exists(path)

    if not folder:  # 判断是否存在文件夹如果不存在则创建为文件夹
        os.makedirs(path)  # makedirs 创建文件时如果路径不存在会创建这个路径


areas = ['changping','daxing','fangshan','huairou','mentougou','miyun','pinggu','shunyi','tongzhou','yanqing']



for area in areas:
    max_count = 0
    min_count = 0
    # 1.创建workbook对象
    workbook = xlwt.Workbook(encoding="utf-8", style_compression=0)

    # 2.创建一个sheet对象,一个sheet对象对应excel文件中一张表格.
    sheet = workbook.add_sheet("2", cell_overwrite_ok=True)  # Cell_overwirte_ok 是能够覆盖单元表格的意思。

    sheet.write(max_count, 0, 'TMAX')
    sheet.write(min_count, 1, 'TMIN')
    max_count = max_count + 1
    min_count = min_count + 1

    year=2011
    while year<=2020:
        month=1
        while month<=12:
            if month<10:
                str_month='0'+str(month)
            else:
                str_month=str(month)
            path = "process/" + area
            f = open(path+"/process_" + str(year) + str_month + '.txt', 'r')
            count_num = 1
            max = []
            min = []
            for line in f.readlines():
                if '℃' in line:
                    line = line.replace("℃", "")
                    line = line.replace("\r", "")
                    line = line.replace("\n", "")
                    line = line.replace(" ", "")
                    if count_num == 1:
                        max.append(int(line))
                        count_num = count_num + 1
                    elif count_num == 2:
                        min.append(int(line))
                        count_num = 1
            f.close()

            path1 = "result/txt/"+area
            path2 = "result/excel/" + area
            mkdir(path1)
            mkdir(path2)
            foo = open(path1+"/result_" + str(year) + str_month + '.txt', "w+")
            for i in range(len(max)):
                max[i] = max[i] * 9 / 5 + 32
                min[i] = min[i] * 9 / 5 + 32

                sheet.write(max_count, 0, str(int(max[i])))
                sheet.write(min_count, 1, str(int(min[i])))
                max_count=max_count+1
                min_count=min_count+1

                foo.write(str(int(max[i])) + '	' + str(int(min[i])) + '\n')
            foo.close()
            month=month+1
        year=year+1
    # #4.保存.
    workbook.save(path2+"/"+area+".xls")