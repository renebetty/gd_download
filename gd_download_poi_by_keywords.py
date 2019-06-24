from urllib.parse import quote
from urllib import request
import json
import xlwt


amap_web_key = 'a0388c101f02224cea904687ee273906'
poi_search_url_by_city_and_type= "http://restapi.amap.com/v3/place/text"


# 根据城市名称和分类关键字获取poi数据
def getpois(cityname, keywords, types):
    print('开始下载')
    i = 1
    poilist = []
    while True:  # 使用while循环不断分页获取数据
        result = getpoi_page(cityname, keywords, types, i)
        result = json.loads(result)  # 将字符串转换为json
        if result['count'] == '0':
            break
        poilist.extend(result['pois'])
        i = i + 1
    return poilist


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

    for i in range(len(poilist)):
        # 每一行写入
        sheet.write(i + 1, 0, poilist[i]['id'])
        sheet.write(i + 1, 1, poilist[i]['name'])
        sheet.write(i + 1, 2, poilist[i]['address'])
        sheet.write(i + 1, 3, poilist[i]['type'])
        sheet.write(i + 1, 4, poilist[i]['location'])
        sheet.write(i + 1, 5, poilist[i]['pname'])
        sheet.write(i + 1, 6, poilist[i]['pcode'])
        sheet.write(i + 1, 7, poilist[i]['cityname'])
        sheet.write(i + 1, 8, poilist[i]['citycode'])
        sheet.write(i + 1, 9, poilist[i]['adname'])
        sheet.write(i + 1, 10, poilist[i]['adcode'])
    # 最后，将以上操作保存到指定的Excel文件中
    print('搜索到' + str(i + 1) + '条信息,存储在当前目录下的' + cityname + keywords + '.xls文件中')
    print('单次搜索量达到850时大概率未下载完全，请考虑具体化关键词缩小范围再次查询')
    book.save(cityname + keywords + '.xls')

# 单页获取pois
def getpoi_page(cityname, keywords, types, page):
    req_url = poi_search_url_by_city_and_type + "?key=" + amap_web_key + '&extensions=all&keywords=' + quote(keywords) + '&types=' + quote(
        types) + '&city=' + quote(cityname) + '&citylimit=true' + '&offset=25' + '&page=' + str(
        page) + '&output=json'
    data = ''
    with request.urlopen(req_url) as f:
        data = f.read()
        data = data.decode('utf-8')
    return data

def loop_getpois(cityname, keywords, types):
    keywords = input('输入楼宇或园区关键字进行搜索(q退出）：')
    while keywords != 'q':
        # 开始下载具体poi信息
        pois = getpois(cityname, keywords, types)
        # 将数据写入excel
        write_to_excel(pois, cityname, types, keywords)
        print('写入成功')
        keywords = input('输入楼宇或园区关键字进行搜索(q退出）：')



# 获取城市分类数据
cityname = "南京"
types = " "
keywords = "start"
loop_getpois(cityname, keywords, types)
# keywords = input('输入楼宇或园区关键字：')
# # 开始下载具体poi信息
# pois = getpois(cityname, keywords, types)
# # 将数据写入excel
# write_to_excel(pois, cityname, types, keywords)
# print('写入成功')


input(u'按回车键退出')