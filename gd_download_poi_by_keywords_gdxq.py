from urllib.parse import quote
from urllib import request
import json
import xlwt


amap_web_key = '11a751404c14fc917ff1ad27529d3cca'
poi_search_url_by_city_and_type= "http://restapi.amap.com/v3/place/text"


# 根据城市名称和分类关键字获取poi数据
def getpois(cityname, keywords, types):
    # print('开始下载')
    poilist = []
    result = getpoi_page(cityname, keywords, types, 1)
    result = json.loads(result)  # 将字符串转换为json
    print(keywords)
    print(result['status'])
    if result['status'] == '1':
        return result['pois']



# 数据写入excel
def write_to_excel(poilist, cityname, types, keywords):
    print('正在写入表格')
    # 一个Workbook对象，这就相当于创建了一个Excel文件
    book = xlwt.Workbook(encoding='utf-8', style_compression=0)
    sheet = book.add_sheet(types, cell_overwrite_ok=True)
    # 第一行(列标题)
    sheet.write(0, 0, 'id')
    sheet.write(0, 1, 'name')
    sheet.write(0, 2, 'address')
    sheet.write(0, 3, 'type')
    sheet.write(0, 4, 'location')
    sheet.write(0, 5, 'pname')
    sheet.write(0, 6, 'pcode')
    sheet.write(0, 7, 'cityname')
    sheet.write(0, 8, 'citycode')
    sheet.write(0, 9, 'adname')
    sheet.write(0, 10, 'adcode')
    sheet.write(0, 11, 'keyword')
    i = 0
    for poi in poilist.keys():
        # 每一行写入
        if poilist[poi]:
            sheet.write(i + 1, 0, poilist[poi][0]['id'])
            sheet.write(i + 1, 1, poilist[poi][0]['name'])
            sheet.write(i + 1, 2, poilist[poi][0]['address'])
            sheet.write(i + 1, 3, poilist[poi][0]['type'])
            sheet.write(i + 1, 4, poilist[poi][0]['location'])
            sheet.write(i + 1, 5, poilist[poi][0]['pname'])
            sheet.write(i + 1, 6, poilist[poi][0]['pcode'])
            sheet.write(i + 1, 7, poilist[poi][0]['cityname'])
            sheet.write(i + 1, 8, poilist[poi][0]['citycode'])
            sheet.write(i + 1, 9, poilist[poi][0]['adname'])
            sheet.write(i + 1, 10, poilist[poi][0]['adcode'])
            sheet.write(i + 1, 11, poi)
        else:
            sheet.write(i + 1, 11, poi)
        i+=1
    # 最后，将以上操作保存到指定的Excel文件中
    print('存储在当前目录下的' + cityname + '.xls文件中')
    book.save(cityname + '.xls')

# 单页获取pois
def getpoi_page(cityname, keywords, types, page):
    req_url = poi_search_url_by_city_and_type + "?key=" + amap_web_key + '&extensions=all&keywords=' + quote(keywords) + '&types=' + quote(
        types) + '&city=' + quote(cityname) + '&citylimit=true' + '&offset=1' + '&page=' + str(
        page) + '&output=json'
    data = ''
    with request.urlopen(req_url) as f:
        data = f.read()
        data = data.decode('utf-8')
    return data

def loop_getpois(cityname, keywords, types):
    pois = {}
    for keyword in keywords:
        # 开始下载具体poi信息
        # 开始下载具体poi信息
        poi = getpois(cityname, keyword, types)
        pois[keyword] = poi
    # 将数据写入excel
    write_to_excel(pois, cityname, types, keywords)
    print(pois)
    print('写入成功')



# 获取城市分类数据
cityname = "六合区"
city = 320116   # 六合区
types = " "
keywords = ['军王', '马营', '柳张']
keywords = []
# 读取要搜索的广电宽带小区关键字
f = open(r"E:\Mypython\gd_download\data\test.txt",encoding='UTF-8-sig')
line = f.readline()
while line:
    keywords = list(map(str, line.split()))
    line = f.readline()
f.close()
loop_getpois(cityname, keywords, types)
# keywords = input('输入楼宇或园区关键字：')
# # 开始下载具体poi信息
# pois = getpois(cityname, keywords, types)
# # 将数据写入excel
# write_to_excel(pois, cityname, types, keywords)
# print('写入成功')

