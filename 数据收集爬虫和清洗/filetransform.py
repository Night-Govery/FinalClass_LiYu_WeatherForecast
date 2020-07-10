import  xlwt

#1.创建workbook对象
workbook =xlwt.Workbook(encoding ="utf-8",style_compression=0)


#2.创建一个sheet对象,一个sheet对象对应excel文件中一张表格.
sheet =workbook.add_sheet("2",cell_overwrite_ok=True)  #Cell_overwirte_ok 是能够覆盖单元表格的意思。

max_count=0
min_count=0

year=2012
while year<=2020:
    month=1
    while month<=12:
        if month<10:
            str_month='0'+str(month)
        else:
            str_month=str(month)
        f = open("process/process_" + str(year) + str_month + '.txt', 'r')
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

        foo = open("result/result_" + str(year) + str_month + '.txt', "w+")
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
workbook.save("2.xls")