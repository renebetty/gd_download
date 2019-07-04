import json
import math
import os
import time
from amap import Map


class MapZoning:
    def __init__(self, city, distance=None, map_service=None):
        self.city = city
        self.distance = distance if distance else 1  # 单位km，默认0.5km
        self.earth_radius = 40075.04 / (2 * math.pi)   #地球平均周长约4万千米,地球赤道半径
        self.lat_unit = self.get_lat_unit(self.distance)   #分块单元纬度
        self.map_service = map_service if map_service else Map('a0388c101f02224cea904687ee273906')
        self.location_validated = {}  # key：[经度,维度] value: 1验证成功，2超出范围

    # 获取一定距离的纬度单位
    def get_lat_unit(self, distance):
        # 1纬度 = 2*pi*r / 360
        return distance * 360 / (2 * math.pi) / self.earth_radius

    # 获取一定距离的经度单位
    def get_lng_unit(self, lat, distance):
        return distance * 360 / (2 * math.pi) / math.cos(math.radians(lat)) / self.earth_radius

    # 根据一个位置点，获取制定大小的矩形区域的四个点
    def _get_area_points(self, quadrant, location):
        # quadrant:象限，四分之一
        # location:传入的位置点，location[0]经度 location[1]纬度
        # :return list : 矩形四个点，顺序：左上、右上、右下、左下

        if quadrant == 1:
            left_lng = float(location[0])  # 经度
            bottom_lat = float(location[1])  # 纬度
            top_lat = round(bottom_lat + self.lat_unit, 6)
            right_lng = round(left_lng + self.get_lng_unit(float(top_lat), self.distance), 6)
        elif quadrant == 2:
            right_lng = float(location[0])
            bottom_lat = float(location[1])
            top_lat = round(bottom_lat + self.get_lat_unit(self.distance), 6)
            left_lng = round(right_lng - self.get_lng_unit(top_lat, self.distance), 6)
        elif quadrant == 3:
            right_lng = float(location[0])
            top_lat = float(location[1])
            left_lng = round(right_lng - self.get_lng_unit(top_lat, self.distance), 6)
            bottom_lat = round(top_lat - self.get_lat_unit(self.distance), 6)
        elif quadrant == 4:
            left_lng = float(location[0])
            top_lat = float(location[1])
            right_lng = round(left_lng + self.get_lng_unit(float(top_lat), self.distance), 6)
            bottom_lat = round(top_lat - self.lat_unit, 6)
        else:
            return None
        return [[left_lng, top_lat], [right_lng, top_lat], [right_lng, bottom_lat], [left_lng, bottom_lat]]

    def get_area_points_x(self, quadrant, res_points, points, i_temp):
        # if i_temp > 60:
        if i_temp > 45:
            return
        if quadrant == 1:
            location = points[2]
        elif quadrant == 2:
            location = points[3]
        elif quadrant == 3:
            location = points[0]
        elif quadrant == 4:
            location = points[1]
        else:
            return
        tmp_pos = self._get_area_points(quadrant, location)
        if self.validate_points(tmp_pos):
            res_points.append(tmp_pos)
        i_temp += 1
        self.get_area_points_x(quadrant, res_points, tmp_pos, i_temp)

    def get_area_points_y(self, quadrant, res_points, points, i_temp):
        # if i_temp > 60:
        if i_temp > 30:   # 65  and  30
            return
        if quadrant == 1:
            location = points[0]
        elif quadrant == 2:
            location = points[1]
        elif quadrant == 3:
            location = points[2]
        elif quadrant == 4:
            location = points[3]
        else:
            return
        tmp_pos = self._get_area_points(quadrant, location)
        if self.validate_points(tmp_pos):
            res_points.append(tmp_pos)
        print("y的i_temp = " + str(i_temp) + "y的tmp_pos = " + str(tmp_pos))
        i_temp += 1
        time.sleep(3)
        self.get_area_points_x(quadrant, res_points, tmp_pos, 1)
        self.get_area_points_y(quadrant, res_points, tmp_pos, i_temp)

    def get_all_area_points(self, quadrant, res_points, location):
        tmp_pos = self._get_area_points(quadrant, location)
        tmp_pos = [[118.796877, 31.47636], [118.80741, 31.47636], [118.80741, 31.467377], [118.796877, 31.467377]]
        res_points.append(tmp_pos)
        self.get_area_points_x(quadrant, res_points, tmp_pos, 1)
        self.get_area_points_y(quadrant, res_points, tmp_pos, 1)

    # 验证列表中的点是不是在所属城市中
    # location_validated   key：[经度,维度] value: 1验证成功，2超出范围
    def validate_points(self, points):
        b_result = False
        # 对矩形的四个点做判断，其中只要有一个点验证通过，即将结果设置为真，判断该区域区块在所属城市；
        for location in points:
            location[0] = float(location[0])
            location[1] = float(location[1])
            # 南京的大矩形范围，超过这个范围即跳过这个点的判断
            if location[0] < 118.332459 or location[1] < 31.2116 or location[1] > 32.62432 or location[0] > 119.2516:
                print("out of NJ")
                continue
            v_key = ','.join([str(x) for x in location])
            v_value = self.location_validated.get(v_key)
            # 如果该点对应的结果值是空，说明以前未判断过，做判断是否属于该城市
            if not v_value:
                res = self.map_service.get_geo_address(location)
                address_component = res.get('regeocode').get('addressComponent') if res and res.get('regeocode') else {}
                if not address_component or address_component.get('citycode') != '025':
                    self.location_validated[v_key] = 2
                else:
                    b_result = True
                    self.location_validated[v_key] = 1
            elif v_value == 1:
                b_result = True
        # print(b_result)
        return b_result

    def zoning(self):
        print(time.time())
        print(self.distance)
        print(self.get_lat_unit(self.distance))
        res_points = []
        location = self.map_service.get_geo_code(self.city).split(',')
        # self.get_all_area_points(1, res_points, location)
        # self.get_all_area_points(2, res_points, location)
        # self.get_all_area_points(3, res_points, location)
        self.get_all_area_points(4, res_points, location)
        # Python引入了with语句来自动帮我们调用close()方法
        with open('../mapslip_data/points--test.json', 'w', encoding='utf-8') as _file:
            # json.dumps将一个Python数据结构转换为JSON
            _file.write('var points = ' + json.dumps(res_points) + ';')
        print(time.time())
        # points = [['113.980092', '22.475719'], ['113.984953', '22.475719'], ['113.984953', '22.471227'],
        #            ['113.980092', '22.471227']]
        # if location[0] < 113.74181 or location[1] < 22.438768 or location[1] > 22.887492 or location[0] > 114.649706:

        # print(self.validate_points(points))
        # print(self.map_service.get_geo_address(['113.980092', '22.475719']))

        print(location)
        print(res_points)
        print(len(res_points))
        print(self.location_validated)
        print(self.location_validated.values())
        print(len(self.location_validated))
        return res_points

MapZoning('南京').zoning()


# 最后设置