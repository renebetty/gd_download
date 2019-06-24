import logging
import requests


class Map:
    def  __init__(self, key):
        if not key:
            raise Exception('初始map服务错误，无效key')
        self.key = key

    def get_geo_code(self, address):
        #获取地理位置编码
        api_geocode = 'http://restapi.amap.com/v3/geocode/geo'
        try:
            response = requests.get(api_geocode, {'key':self.key,
                                                  'address':address,
                                                  'city':'南京',
                                                  'output':'JSON'})
            if response.status_code != 200:
                return None
            res = response.json()
            if not res:
                return None
            geocodes = res.get('geocodes')
            if not geocodes:
                return None
            location = geocodes[0].get('location')
            if not location:
                return None
            return location
        except Exception as ex:
            logging.error('获取地址位置编码错误：' + str(ex))
            return None


    def get_geo_address(self, location):
        api = 'http://restapi.amap.com/v3/geocode/regeo'
        try:
            response = requests.get(api, {'key':self.key,
                                          'location':','.join([str(x) for x in location]),
                                          'output':'JSON'})
            if response.status_code != 200:
                return None
            res = response.json()
            if not res:
                return None
            return res
        except Exception as ex:
            logging.error('获取地址位置错误：' + str(ex))
            return None

