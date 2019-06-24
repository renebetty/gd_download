from urllib.parse import quote
from urllib import request
import json
import xlwt


amap_web_key = 'a0388c101f02224cea904687ee273906'
poi_search_url_by_city_and_type= "http://restapi.amap.com/v3/place/text"
poi_search_url_by_rec= "http://restapi.amap.com/v3/place/text"


# 根据城市名称和分类关键字获取poi数据
def getpois(cityname, keywords):
    i = 1
    poilist = []
    while True:  # 使用while循环不断分页获取数据
        result = getpoi_page_by_city_and_type(cityname, keywords, i)
        result = json.loads(result)  # 将字符串转换为json
        if result['count'] == '0':
            break
        poilist.extend(result['pois'])
        i = i + 1
    return poilist


# 数据写入excel
def write_to_excel(poilist, cityname, types):
    # 一个Workbook对象，这就相当于创建了一个Excel文件
    book = xlwt.Workbook(encoding='utf-8', style_compression=0)
    sheet = book.add_sheet(types, cell_overwrite_ok=True)
    # 第一行(列标题)
    sheet.write(0, 0, 'id')
    sheet.write(0, 1, 'name')
    sheet.write(0, 2, 'location')
    sheet.write(0, 3, 'pname')
    sheet.write(0, 4, 'pcode')
    sheet.write(0, 5, 'cityname')
    sheet.write(0, 6, 'citycode')
    sheet.write(0, 7, 'adname')
    sheet.write(0, 8, 'adcode')
    sheet.write(0, 9, 'address')
    sheet.write(0, 10, 'type')
    for i in range(len(poilist)):
        # 每一行写入
        sheet.write(i + 1, 0, poilist[i]['id'])
        sheet.write(i + 1, 1, poilist[i]['name'])
        sheet.write(i + 1, 2, poilist[i]['location'])
        sheet.write(i + 1, 3, poilist[i]['pname'])
        sheet.write(i + 1, 4, poilist[i]['pcode'])
        sheet.write(i + 1, 5, poilist[i]['cityname'])
        sheet.write(i + 1, 6, poilist[i]['citycode'])
        sheet.write(i + 1, 7, poilist[i]['adname'])
        sheet.write(i + 1, 8, poilist[i]['adcode'])
        sheet.write(i + 1, 9, poilist[i]['address'])
        sheet.write(i + 1, 10, poilist[i]['type'])
    # 最后，将以上操作保存到指定的Excel文件中
    book.save(r'd:\\' + cityname + '.xls')

#多边形搜索
#restapi.amap.com/v3/place/polygon?key=您的key&polygon=118.777000,32.042000|118.782000,32.052000&keywords=&types=170000&offset=20&page=1&extensions=all

#关键字搜索
#restapi.amap.com/v3/place/text?key=您的key&keywords=&types=010000|170000&city=320102&children=1&offset=20&page=1&extensions=all
# 单页获取pois
def getpoi_page_by_city_and_type(cityname, types, page):
    req_url = poi_search_url_by_city_and_type + "?key=" + amap_web_key + '&extensions=all&keywords=&types=' + quote(
        types) + '&city=' + quote(cityname) + '&citylimit=true' + '&offset=25' + '&page=' + str(
        page) + '&output=json'
    data = ''
    with request.urlopen(req_url) as f:
        data = f.read()
        data = data.decode('utf-8')
    return data




# 获取城市分类数据
cityname = "南京"
types = "010000|170000"
pois = getpois(cityname, types)

# 将数据写入excel
write_to_excel(pois, cityname, types)
print('写入成功')