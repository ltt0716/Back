import re
import sys

# 定义 Station 类
class Station:
    def __init__(self, id, name, description, position_x, position_y, position_z):
        self.id = id
        self.name = name
        self.description = description
        self.position_x = position_x
        self.position_y = position_y
        self.position_z = position_z


Station_str=sys.argv[1]
# Station_str="[Station(id=11, name=22, description=33, position_x=444.0, position_y=55.0, position_z=66.0), Station(id=12, name=22, description=33, position_x=44.0, position_y=44.0, position_z=44.0), Station(id=13, name=22, description=33, position_x=44.0, position_y=44.0, position_z=44.0), Station(id=14, name=22, description=22, position_x=22.0, position_y=22.0, position_z=22.0), Station(id=18, name=22, description=33, position_x=44.0, position_y=55.0, position_z=66.0)]"
stations_str= Station_str[1:-1].split("),")    #数据处理

for i in range(0,len(stations_str)):
    # 输入的字符串
    # station_str = "Station(id=11, name=22, description=33, position_x=444.0, position_y=55.0, position_z=66.0)"
    stations_str[i]+="),"
    # 使用正则表达式提取键值对
    matches = re.findall(r'(\w+)=(\w+\.?\w*)', stations_str[i])

    # 构建参数字典
    params = dict(matches)

    # 创建 Station 对象
    station = Station(**params)

    # 打印属性值
    print(station.id,station.name,station.description,station.position_x,station.position_y,station.position_z)



