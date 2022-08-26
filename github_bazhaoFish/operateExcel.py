import string
from xlrd import open_workbook     # xlrd<= 1.2.0 which supports .xls and .xlsx
from xlrd import book
from xlutils.copy import copy
from os import system

def editUrl(url:string)->int:
    # 写入cmd.txt
    # cols = sheet1.ncols #获取列数
    file = r'.\waterRPA\cmd.xls'
    tempBook = open_workbook(file)
    WriteBook = copy(tempBook)
    sheet1 = WriteBook.get_sheet(0)
    sheet1.write(5,1,url)
    print("[Info] 新url写入完成")
    try:
        WriteBook.save(file)
        return 0
    except Exception as e:
        print("[ERR]",e)
        return -1