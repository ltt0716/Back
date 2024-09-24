import time
import czml3
from czml3 import Document,Packet
import datetime
import random
from sgp4.io import twoline2rv
from sgp4.earth_gravity import wgs72
from datetime import datetime, timedelta
from pyproj import Transformer
import math
# 创建czml文档
StartTime="2012-03-15T10:00:00Z"    #ISO 8601 标准的时间格式
StopTime="2012-03-16T10:00:00Z"
#卫星实体
satellite_entity=[]

#创建第一个包preamble
def Create_Preamble(name="simple",start=StartTime,stop=StopTime,multiplier=60):
    clock={
        "interval": f"{start}/{stop}",
        "currentTime": f"{start}",
        "multiplier": multiplier,
        "range": "LOOP_STOP",
        "step": "SYSTEM_CLOCK_MULTIPLIER"
    }
    #初始化Preamable包
    data = czml3.Preamble(version="1.0", name=name, clock=clock)
    #返回
    return data

#计算卫星位置
def Satellite_Position(line1,line2,startime,stoptime,step):
    #解析
    satellite = twoline2rv(line1, line2, wgs72)
    #计算卫星位置
    time_step = timedelta(seconds=step)
    current_time = startime
    stoptime = stoptime
    #相对秒数
    ATime = 0
    positions = []
    Aviliable=[]
    #地面站位置
    F_position=[1152255.80150063, -4694317.951340558, 4147335.9067563135]
    while True:
        utc_time = datetime.strptime(current_time, "%Y-%m-%dT%H:%M:%SZ")
        position, velocity = satellite.propagate(
            utc_time.year, utc_time.month, utc_time.day,
            utc_time.hour, utc_time.minute, utc_time.second
        )
        #添加包的信息
        positions.append(ATime)
        positions.append(position[0]*1000)
        positions.append(position[1]*1000)
        positions.append(position[2]*1000)

        #计算可见性
        If_Visiable=Determine_Visible(F_position, position)
        # if(If_Visiable==True):
        Aviliable.append((current_time,If_Visiable))

        #更新当前时间
        current_time = (utc_time + time_step).strftime("%Y-%m-%dT%H:%M:%SZ")
        ATime += step

        #循环跳出条件
        if (current_time > stoptime):
            break

    #返回位置
    return positions,Aviliable

#计算可见性ulti
def Calculate_Visiable(start,stop,origin):

    aviliable=[]

    tem1,tem2=[],[]
    # print(origin)
    for i in range(0,len(origin)):
        if(len(tem1)==0 and origin[i][1]==True):
            tem1.append(origin[i][0])
            continue

        if(origin[i][1]==True and len(tem1)!=0):
            if(len(tem1)==len(tem2)):
                tem1.append(origin[i][0])
                continue

        if(origin[i][1]==False):
            if(len(tem1)>len(tem2)):
                tem2.append(origin[i][0])
                continue
    # print(tem1)
    # print(tem2)
    if(len(tem1)==len(tem2)):
        for i in range(0, len(tem1)):
            aviliable.append(f"{tem1[i]}/{tem2[i]}")

    else:
        for i in range(0, len(tem1)-1):
            aviliable.append(f"{tem1[i]}/{tem2[i]}")

        aviliable.append(f"{tem1[len(tem1)-1]}/{stop}")


    show=[]

    if(len(tem1)==len(tem2)):
        tem = [
            {
                "interval": f"0000-01-01T00:00:00Z/{tem1[0]}",
                "boolean": False
            }
        ]
        show.append(tem)
        for i in range(0, len(tem1)):
            tmp = [
                {
                    "interval": f"{tem1[i]}/{tem2[i]}",
                    "boolean": True
                }
            ]
            show.append(tmp)
            if(i==len(tem1)-1):
                tmp = [
                    {
                        "interval": f"{tem2[i]}/{stop}",
                        "boolean": False
                    }
                ]
                show.append(tmp)
            else:
                tmp = [
                    {
                        "interval": f"{tem2[i]}/{tem1[i+1]}",
                        "boolean": False
                    }
                ]
                show.append(tmp)
    else:
        tem = [
            {
                "interval": f"0000-01-01T00:00:00Z/{tem1[0]}",
                "boolean": False
            }
        ]
        show.append(tem)
        for i in range(0, len(tem1)-1):
            tmp = [
                {
                    "interval": f"{tem1[i]}/{tem2[i]}",
                    "boolean": True
                }
            ]
            show.append(tmp)
            if(i==len(tem1)-1):
                tmp = [
                    {
                        "interval": f"{tem1[i]}/{stop}",
                        "boolean": True
                    }
                ]
                show.append(tmp)
            else:
                tmp = [
                    {
                        "interval": f"{tem2[i]}/{tem1[i+1]}",
                        "boolean": False
                    }
                ]
                show.append(tmp)

    #返回
    return aviliable,show

#创建卫星与地面站相联系的packet
def Create_FacilityToSatellite(id,name,parent,description,available,show,S_id):
    #属性

    polyline={
        "show":show,
        "width":1,
        "material": {
             "solidColor": {
                 "color": {
                     "rgba": [
                         0, 255, 255, 255
                ]
            }
        }
    },
        "arcType": "NONE",
        "positions": {
            "references": [
                "Facility/AGI#position", f"{S_id}#position"
            ]
        }

    }

    data=Packet(id=id,name=name,description=description,parent=parent,polyline=polyline,availability=available)
    #返回
    return data



#创建卫星packet
def Create_SatellitePacket(id,name,line1,line2,description,image,text,period,start,stop,width=1,step=60):
    availability=f"{start}/{stop}"
    billboard={
            "eyeOffset": {
                "cartesian": [
                    0,
                    0,
                    -90
                ]
            },
            "horizontalOrigin": "CENTER",
            "image": f"{image}",
            "pixelOffset": {
                "cartesian2": [
                    0,
                    0
                ]
            },
            "scale": 1.5,
            "show": True,
            "verticalOrigin": "CENTER"
    }
    #产生随机数
    random_numbers = []
    for _ in range(4):
        random_number = random.randint(0, 255)
        random_numbers.append(random_number)

    label={
        "fillColor": {
            "rgba": [
                random_numbers[0], random_numbers[1], random_numbers[2], random_numbers[3]
            ]
        },
        "font": "11pt Lucida Console",
        "horizontalOrigin": "LEFT",
        "outlineColor": {
            "rgba": [
                random_numbers[3], random_numbers[2], random_numbers[1], random_numbers[0]
            ]
        },
        "outlineWidth": 2,
        "pixelOffset": {
            "cartesian2": [
                12,
                0
            ]
        },
        "show": True,
        "style": "FILL_AND_OUTLINE",
        "text": text,
        "verticalOrigin": "CENTER"
    }

    lead_times=[]
    trail_times=[]
    # 卫星周期，转换成timedelta对象
    period_time = timedelta(seconds=period)

    # 当前时间，给定的时间字符串
    current_time = start

    while True:
        lead_time = {}
        trail_time = {}
        # leadtime、trialtime属性
        property_interval = "interval"
        property_epoch = "epoch"
        property_number = "number"
        # 将时间字符串转换为 datetime 对象（注意这里的时间是 UTC 时间）
        utc_time = datetime.strptime(current_time, "%Y-%m-%dT%H:%M:%SZ")
        end_time=(utc_time + period_time).strftime("%Y-%m-%dT%H:%M:%SZ")

        # 设置leadtime属性
        lead_time[property_interval] = f"{current_time}/{end_time}"
        lead_time[property_epoch] = f"{current_time}"
        lead_time[property_number] = [
            0, period,
            period, 0
        ]
        # 设置trailtime属性
        trail_time[property_interval] = f"{current_time}/{end_time}"
        trail_time[property_epoch] = f"{current_time}"
        trail_time[property_number] = [
            0, 0,
            period, period
        ]
        # 属性列表添加到字典中
        lead_times.append(lead_time)
        trail_times.append(trail_time)
        # 更新当前时间
        current_time = (utc_time + period_time).strftime("%Y-%m-%dT%H:%M:%SZ")

        # 终止循环
        if current_time > stop:
            break;
    path={
        "show": [
            {
                "interval": f"{start}/{stop}",
                "boolean": True
            }
        ],
        "width": width,
        "material": {
            "solidColor": {
                "color": {
                    "rgba": [
                        random_numbers[3], random_numbers[1], random_numbers[0], random_numbers[2]
                    ]
                }
            }
        },
        "resolution": 120,
        "leadTime":lead_times,
        "trailTime":trail_times
    }

    cartesian,Aviliable=Satellite_Position(line1=line1,line2=line2,startime=start,stoptime=stop,step=step)
    position={
        "interpolationAlgorithm": "LAGRANGE",
        "interpolationDegree": 5,
        "referenceFrame": "INERTIAL",
        "epoch": start,
        "cartesian": cartesian
    }

    aviliable,show=Calculate_Visiable(start, stop, Aviliable)

    print(aviliable)
    #地面站与卫星的可见性包
    data2=Create_FacilityToSatellite(id="Facility/AGI-to-Satellite"+id, name="Facility/AGI-to-Satellite"+id,
                                     parent="9927edc4-e87a-4e1f-9b8b-0bfb3b05b227",
                                     description="<h2>Access times</h2><table class='sky-infoBox-access-table'><tr><th>Start</th><th>End</th><th>Duration</th></tr><tr><td> 2012-03-15 10:52:19.394Z </td><td>2012-03-15 11:02:24.557Z </td><td> 605.163s </td></tr><tr><td> 2012-03-15 12:28:24.034Z </td><td>2012-03-15 12:38:34.640Z </td><td> 610.606s </td></tr><tr><td> 2012-03-15 14:06:02.098Z </td><td>2012-03-15 14:14:48.531Z </td><td> 526.433s </td></tr><tr><td> 2012-03-15 15:43:15.235Z </td><td>2012-03-15 15:52:06.565Z </td><td> 531.330s </td></tr><tr><td> 2012-03-15 17:19:26.319Z </td><td>2012-03-15 17:29:36.024Z </td><td> 609.705s </td></tr><tr><td> 2012-03-15 18:55:44.708Z </td><td>2012-03-15 19:05:17.734Z </td><td> 573.026s </td></tr><tr><td> 2012-03-16 09:56:05.906Z </td><td>2012-03-16 10:00:00.000Z </td><td> 234.094s </td></tr></table>",
                                     available=aviliable, show=show, S_id=id)
    data=Packet(id=id,name=name,availability=availability,description=description,label=label,
                billboard=billboard,path=path,position=position)



    #返回对象
    return data,data2

#创建地面站packet
def Create_FacilityPacket(id,name,start,stop,description,image,text,position):
    availability = f"{start}/{stop}"
    billboard = {
        "eyeOffset": {
            "cartesian": [
                0,
                0,
                0
            ]
        },
        "horizontalOrigin": "CENTER",
        "image": f"{image}",
        "pixelOffset": {
            "cartesian2": [
                0,
                0
            ]
        },
        "scale": 1.5,
        "show": True,
        "verticalOrigin": "CENTER"
    }
    # 产生随机数
    random_numbers = []
    for _ in range(4):
        random_number = random.randint(0, 255)
        random_numbers.append(random_number)

    label = {
        "fillColor": {
            "rgba": [
                random_numbers[0], random_numbers[1], random_numbers[2], random_numbers[3]
            ]
        },
        "font": "11pt Lucida Console",
        "horizontalOrigin": "LEFT",
        "outlineColor": {
            "rgba": [
                random_numbers[3], random_numbers[2], random_numbers[1], random_numbers[0]
            ]
        },
        "outlineWidth": 2,
        "pixelOffset": {
            "cartesian2": [
                12,
                0
            ]
        },
        "show": True,
        "style": "FILL_AND_OUTLINE",
        "text": text,
        "verticalOrigin": "CENTER"
    }
    cartesian=position
    A_position = {
        "cartesian": cartesian
    }

    data = Packet(id=id, name=name, availability=availability, description=description, label=label,
                  billboard=billboard, position=A_position)

    # 返回对象
    return data

#创建Area Packet
def Create_AreaPacket(id,name,start,stop,description,text,position,positions=[]):
    #可见性
    availability = f"{start}/{stop}"
    # 产生随机数
    random_numbers = []
    for _ in range(4):
        random_number = random.randint(0, 255)
        random_numbers.append(random_number)
    #label属性
    label = {
        "fillColor": {
            "rgba": [
                random_numbers[0], random_numbers[1], random_numbers[2], random_numbers[3]
            ]
        },
        "font": "11pt Lucida Console",
        "horizontalOrigin": "LEFT",
        "outlineColor": {
            "rgba": [
                random_numbers[3], random_numbers[2], random_numbers[1], random_numbers[0]
            ]
        },
        "outlineWidth": 2,
        "pixelOffset": {
            "cartesian2": [
                12,
                0
            ]
        },
        "show": True,
        "style": "FILL_AND_OUTLINE",
        "text": text,
        "verticalOrigin": "CENTER"
    }
    #point属性
    point= {
        "color": {
            "rgba": [
                random_numbers[3], random_numbers[2], random_numbers[0], random_numbers[1]
            ]
        },
        "outlineWidth": 0,
        "pixelSize": 5,
        "show": True
    }
    #多边形属性
    polygon={
        "positions": {
            "cartographicRadians": [
                -1.3522077240237877,
                0.6932383436059149,
                0,
                -1.3630314740519183,
                0.6933402355423893,
                0,
                -1.3671958658568963,
                0.6933164116349497,
                0,
                -1.3680725973741055,
                0.6933103378544294,
                0,
                -1.3756294390644388,
                0.693299289626768,
                0,
                -1.37759145155452,
                0.693285710886166,
                0,
                -1.3857323154905137,
                0.6932329317993553,
                0,
                -1.387204693159873,
                0.6932497043584019,
                0,
                -1.3921642397583167,
                0.6932764600632868,
                0,
                -1.3948369679907713,
                0.6932740164944832,
                0,
                -1.403752356914346,
                0.6932421638673993,
                0,
                -1.4054136839844849,
                0.6932660224548367,
                0,
                -1.4054203339781848,
                0.6974061187809533,
                0,
                -1.40542577948586,
                0.6985302157572724,
                0,
                -1.4054446815793686,
                0.7009683713811051,
                0,
                -1.4054013802466303,
                0.7051660984836011,
                0,
                -1.4054152208071435,
                0.7064882030988564,
                0,
                -1.405374066131245,
                0.7092531367782914,
                0,
                -1.405344517975858,
                0.7130398911135833,
                0,
                -1.4053553041696831,
                0.7137921630703696,
                0,
                -1.4053903506948033,
                0.717847558527404,
                0,
                -1.4053391082894005,
                0.7241248283511975,
                0,
                -1.4054076823049872,
                0.724226301809922,
                0,
                -1.4053853251132624,
                0.7304339504245932,
                0,
                -1.4053495111334156,
                0.732809309071272,
                0,
                -1.3921311340866651,
                0.7377041737073639,
                0,
                -1.3921036273290417,
                0.7330926289989202,
                0,
                -1.3894979895551738,
                0.7330486468055195,
                0,
                -1.3798484450375388,
                0.7330586305001696,
                0,
                -1.3773883852209647,
                0.7330357493325297,
                0,
                -1.3666816595180005,
                0.7330283146713379,
                0,
                -1.3649219132838528,
                0.7330070217223114,
                0,
                -1.3569064163205986,
                0.7329918900387238,
                0,
                -1.354599770992057,
                0.7330180002614316,
                0,
                -1.3433550648083268,
                0.7330904667885002,
                0,
                -1.342653826195758,
                0.7330826651925256,
                0,
                -1.3362924480939438,
                0.7330909906599572,
                0,
                -1.328981348766283,
                0.7330498535192947,
                0,
                -1.3282799705255588,
                0.7330296775356948,
                0,
                -1.317369878937513,
                0.7329750316713255,
                0,
                -1.3156783227347815,
                0.7330097463386135,
                0,
                -1.3150298279817356,
                0.7329135612488367,
                0,
                -1.314652993784966,
                0.7323625607125478,
                0,
                -1.3139482994025766,
                0.7321239392772451,
                0,
                -1.313439099339346,
                0.7307498413128194,
                0,
                -1.3119864438784967,
                0.730731794657347,
                0,
                -1.3115849481938966,
                0.7305214824566543,
                0,
                -1.3111742895338896,
                0.7304061685456499,
                0,
                -1.3110525702187852,
                0.7301933081536464,
                0,
                -1.3103904967805342,
                0.7297947098063845,
                0,
                -1.3106869061243591,
                0.7294990335104291,
                0,
                -1.3106926482391603,
                0.7291819769374323,
                0,
                -1.31006717438301,
                0.7290287195687776,
                0,
                -1.3099912873941209,
                0.7282685936295457,
                0,
                -1.3101384361377446,
                0.7280613880956304,
                0,
                -1.3098927634269164,
                0.7267083737010938,
                0,
                -1.3102614817770415,
                0.7262854105154587,
                0,
                -1.3102163475385047,
                0.7261352772658493,
                0,
                -1.3094348237109952,
                0.7254602361685523,
                0,
                -1.3092568000409661,
                0.7250021744241752,
                0,
                -1.308504580282513,
                0.7240255927322389,
                0,
                -1.3078199921164888,
                0.72403864782177,
                0,
                -1.3072264926882589,
                0.7236467166299556,
                0,
                -1.307169245851595,
                0.7233461185166344,
                0,
                -1.3066244760589671,
                0.7233894550695429,
                0,
                -1.3053806318405998,
                0.7230886126517037,
                0,
                -1.304717877749918,
                0.7230926094796837,
                0,
                -1.3044598132746381,
                0.7229514646847072,
                0,
                -1.304466742212013,
                0.7225949985688139,
                0,
                -1.3038530144070728,
                0.7221311597980974,
                0,
                -1.3037620652441313,
                0.7217037983975161,
                0,
                -1.3053608047669052,
                0.7210299440396993,
                0,
                -1.3054040889283545,
                0.7207376013315654,
                0,
                -1.3059460661823945,
                0.7205192954872712,
                0,
                -1.3066654038056376,
                0.7195438482063814,
                0,
                -1.3066038809082192,
                0.7191939794384397,
                0,
                -1.307509392852277,
                0.7180478912764205,
                0,
                -1.3081242027013054,
                0.7175373648956472,
                0,
                -1.308728104256843,
                0.717319652461049,
                0,
                -1.3088029439804343,
                0.7170121428373868,
                0,
                -1.3084086390699141,
                0.7170281126169686,
                0,
                -1.3090170610213867,
                0.7166757130974598,
                0,
                -1.3096123057176687,
                0.7160773791853247,
                0,
                -1.3102183365700435,
                0.7157721733780154,
                0,
                -1.3110323583836496,
                0.7155894722475611,
                0,
                -1.3114282515208273,
                0.715192915896617,
                0,
                -1.3113623303982265,
                0.7149382548578634,
                0,
                -1.3103886282856712,
                0.7138982478932651,
                0,
                -1.3102830183588716,
                0.7135714872902171,
                0,
                -1.3099828739776964,
                0.7133519073843598,
                0,
                -1.3099502537461944,
                0.7130661620241878,
                0,
                -1.3107343082404708,
                0.71278013738274,
                0,
                -1.3105539981986583,
                0.7124678106579555,
                0,
                -1.3107517440349952,
                0.7119489067090039,
                0,
                -1.31127146832641,
                0.711618131825877,
                0,
                -1.311969495533574,
                0.7116548186295764,
                0,
                -1.3123766984036227,
                0.7111869655638845,
                0,
                -1.312273898452243,
                0.7107655382832366,
                0,
                -1.3125810939125313,
                0.7101058734983065,
                0,
                -1.3122094259121033,
                0.7098219258392405,
                0,
                -1.3126432625232558,
                0.7094893707227551,
                0,
                -1.312451642745932,
                0.7092008153872138,
                0,
                -1.3124943858525955,
                0.7088611393395713,
                0,
                -1.3123744118489564,
                0.7083205235010411,
                0,
                -1.3124452547722973,
                0.708092164574061,
                0,
                -1.3121783938297178,
                0.7078498255687451,
                0,
                -1.311170361152473,
                0.7079894345182887,
                0,
                -1.3103895005747963,
                0.707650107564989,
                0,
                -1.3101083802768658,
                0.7072250674577409,
                0,
                -1.3102207619963784,
                0.7060949839922579,
                0,
                -1.309999715938635,
                0.7054652167207774,
                0,
                -1.3093681334206897,
                0.7051362570197143,
                0,
                -1.3090052619072645,
                0.705263631186341,
                0,
                -1.3085229574630952,
                0.7051907985987479,
                0,
                -1.3081275878407266,
                0.704161490481042,
                0,
                -1.3078189262517947,
                0.7039573043817338,
                0,
                -1.3076207789382897,
                0.7036127588721909,
                0,
                -1.3069140774300372,
                0.7033606983954779,
                0,
                -1.3062526671932404,
                0.7024681543136311,
                0,
                -1.3044385887704104,
                0.701233735108179,
                0,
                -1.3042056919320535,
                0.7007377298965646,
                0,
                -1.304568964853792,
                0.7003023050552322,
                0,
                -1.3060128412908008,
                0.7001592403389345,
                0,
                -1.3067616226475691,
                0.699494182468726,
                0,
                -1.3082325342309757,
                0.6991443834599382,
                0,
                -1.3087087299920748,
                0.6987265340836812,
                0,
                -1.3097941505737305,
                0.698265086353168,
                0,
                -1.310184580829599,
                0.6978768726763835,
                0,
                -1.3104732932768435,
                0.6977082912802286,
                0,
                -1.3109336414681285,
                0.6977250115221181,
                0,
                -1.3114380592151826,
                0.6973624890931379,
                0,
                -1.3115653635501037,
                0.6969928457322186,
                0,
                -1.3113672162189656,
                0.6963321861243438,
                0,
                -1.311491064806832,
                0.6960654124902647,
                0,
                -1.3122363904438565,
                0.6959921609813949,
                0,
                -1.313307848385792,
                0.6955209219518895,
                0,
                -1.3134255708764333,
                0.69543595930277,
                0,
                -1.3150346253356304,
                0.6954879526165308,
                0,
                -1.316335524310828,
                0.6946234384593984,
                0,
                -1.3171997767525299,
                0.6951045210815227,
                0,
                -1.319179975605344,
                0.6953413971468251,
                0,
                -1.3202367902547627,
                0.695309754284478,
                0,
                -1.3211230163524166,
                0.694998230372876,
                0,
                -1.3220100103668133,
                0.6942036166803666,
                0,
                -1.322522002814063,
                0.6933243719682792,
                0,
                -1.3228041702830704,
                0.6933123989973828,
                0,
                -1.3288801694793237,
                0.6932838277389112,
                0,
                -1.330519016712254,
                0.693277265241703,
                0,
                -1.3363957516005893,
                0.6932495491982945,
                0,
                -1.3402469439857425,
                0.6932668452760358,
                0,
                -1.3438479258876066,
                0.6932604746923505,
                0,
                -1.347761635982283,
                0.6932567744504896,
                0,
                -1.3520094545588786,
                0.6932461975964622,
                0,
                -1.3522077240237877,
                0.6932383436059149,
                0
            ]
        },
        "material": {
            "solidColor": {
                "color": {
                    "rgba": [
                        255,
                        0,
                        0,
                        77
                    ]
                }
            }
        },
        "fill": False,
        "outline": True,
        "outlineColor": {
            "rgba": [
                random_numbers[2], random_numbers[0], random_numbers[1], random_numbers[3]
            ]
        }
    }
    #地面站的位置
    cartesian = position
    A_position = {
        "cartesian": cartesian
    }
    #定义packet
    data = Packet(id=id, name=name, availability=availability, description=description, label=label,
                  point=point,polygon=polygon,position=A_position)

    # 返回对象
    return data

#计算地面站与卫星可见性
def Determine_Visible(F_position,S_position):

    # 地面站笛卡尔坐标
    F_x = F_position[0]
    F_y = F_position[1]
    F_z = F_position[2]
    # 卫星笛卡尔坐标
    S_x = S_position[0]*1000
    S_y = S_position[1]*1000
    S_z = S_position[2]*1000

    # 计算卫星到地面站的向量
    vec_sat = [F_x - S_x, F_y - S_y , F_z - S_z ]

    # 计算卫星到地面站的距离
    distance = math.sqrt(vec_sat[0] ** 2 + vec_sat[1] ** 2 + vec_sat[2] ** 2)
    # 计算仰角
    angle = math.degrees(math.asin(vec_sat[2] / distance))

    # print("卫星和地面站的仰角为: ", angle, "度")
    if(angle>10):
        return True
    else:
        return False


#创建czml文件
def Generate_czml(start=StartTime,stop=StopTime):
    #tle数据
    tle_data = """GPS BIIR-2  (PRN 13)
1 24876U 97035A   24038.65105561 -.00000004  00000+0  00000+0 0  9990
2 24876  55.6292 132.2355 0075986  52.9268 307.7795  2.00565220194695
GPS BIIR-4  (PRN 20)
1 26360U 00025A   24038.76125965 -.00000015  00000+0  00000+0 0  9997
2 26360  54.5625  54.2002 0040179 211.4690 318.1645  2.00558870174019
GPS BIIR-5  (PRN 22)
1 26407U 00040A   24038.99662889  .00000086  00000+0  00000+0 0  9999
2 26407  55.1248 249.3646 0147719 294.1808 246.0304  2.00558238172698
GPS BIIR-8  (PRN 16)
1 27663U 03005A   24038.33882119  .00000092  00000+0  00000+0 0  9993
2 27663  55.1654 249.2017 0138116  46.5081 155.8365  2.00557061154044
GPS BIIR-9  (PRN 21)
1 27704U 03010A   24038.35239510 -.00000073  00000+0  00000+0 0  9998
2 27704  55.1141 359.0715 0253781 323.2789 106.1030  2.00557837152847
GPS BIIR-11 (PRN 19)
1 28190U 04009A   24038.57667391 -.00000032  00000+0  00000+0 0  9998
2 28190  55.5633 310.2510 0093165 143.0349  28.7712  2.00562434145710
GPS BIIR-13 (PRN 02)
1 28474U 04045A   24038.52339744 -.00000073  00000+0  00000+0 0  9991
2 28474  55.4420 359.4393 0164759 288.3577 251.0152  2.00538261141161
GPS BIIRM-1 (PRN 17)
1 28874U 05038A   24038.56561527 -.00000026  00000+0  00000+0 0  9996
2 28874  55.6114 307.7081 0138382 283.0415 265.2558  2.00564534134568
GPS BIIRM-2 (PRN 31)
1 29486U 06042A   24038.45059140  .00000046  00000+0  00000+0 0  9994
2 29486  54.6811 185.4661 0104580  36.6902 328.7457  2.00562560127137
GPS BIIRM-3 (PRN 12)
1 29601U 06052A   24036.87695940  .00000098  00000+0  00000+0 0  9999
2 29601  55.1919 248.2293 0087292  80.6543 280.3945  2.00558891126114
GPS BIIRM-4 (PRN 15)
1 32260U 07047A   24039.17645875 -.00000002  00000+0  00000+0 0  9993
2 32260  53.5382 115.6377 0152181  73.7134 288.0011  2.00571169119589
GPS BIIRM-5 (PRN 29)
1 32384U 07062A   24038.26154765 -.00000029  00000+0  00000+0 0  9998
2 32384  55.7478 308.5643 0024522 147.9918  39.2162  2.00566813118241
GPS BIIRM-6 (PRN 07)
1 32711U 08012A   24038.59582485  .00000043  00000+0  00000+0 0  9993
2 32711  54.4514 184.2550 0181213 237.0636 121.1443  2.00563338116494
GPS BIIRM-8 (PRN 05)
1 35752U 09043A   24039.09044498 -.00000006  00000+0  00000+0 0  9999
2 35752  55.5654  61.4599 0054389  69.7640 300.7451  2.00577358106092
GPS BIIF-1  (PRN 25)
1 36585U 10022A   24038.14401428  .00000096  00000+0  00000+0 0  9996
2 36585  54.4967 243.2916 0115972  60.9651 109.1078  2.00569975100328
GPS BIIF-3  (PRN 24)
1 38833U 12053A   24037.77090176  .00000040  00000+0  00000+0 0  9991
2 38833  53.5145 178.8385 0149186  54.8952 306.4551  2.00556411 82167
GPS BIIF-4  (PRN 27)
1 39166U 13023A   24038.13498831 -.00000019  00000+0  00000+0 0  9997
2 39166  55.2249 303.8591 0121748  42.6107 318.3796  2.00563337 78614
GPS BIIF-5  (PRN 30)
1 39533U 14008A   24038.13797489  .00000046  00000+0  00000+0 0  9999
2 39533  53.5995 184.4029 0069090 216.2607 143.2337  2.00560503 72415
GPS BIIF-6  (PRN 06)
1 39741U 14026A   24038.41821555 -.00000067  00000+0  00000+0 0  9997
2 39741  56.7113   4.9359 0033069 312.4505  47.2685  2.00577465 71275
GPS BIIF-7  (PRN 09)
1 40105U 14045A   24038.50585965 -.00000005  00000+0  00000+0 0  9998
2 40105  54.8733 122.8309 0025981 117.6639 242.6315  2.00556940 68812
GPS BIIF-8  (PRN 03)
1 40294U 14068A   24037.87448797 -.00000004  00000+0  00000+0 0  9991
2 40294  56.3094  64.3668 0048696  59.9052 300.6456  2.00551115 67933
GPS BIIF-9  (PRN 26)
1 40534U 15013A   24038.01676420  .00000096  00000+0  00000+0 0  9992
2 40534  53.3951 239.8343 0086950  28.9279 331.6007  2.00573547 64554
GPS BIIF-10 (PRN 08)
1 40730U 15033A   24038.17822704 -.00000017  00000+0  00000+0 0  9991
2 40730  54.7104 302.3955 0092324  16.6989 343.6585  2.00573761 62725
GPS BIIF-11 (PRN 10)
1 41019U 15062A   24038.23103406 -.00000003  00000+0  00000+0 0  9997
2 41019  56.2919  64.2052 0094675 224.5690 134.7321  2.00562240 60566
GPS BIIF-12 (PRN 32)
1 41328U 16007A   24038.31435847 -.00000006  00000+0  00000+0 0  9999
2 41328  55.0728 123.6519 0076977 235.9202 123.3769  2.00568148 58573
GPS BIII-1  (PRN 04)
1 43873U 18109A   24038.58133934 -.00000004  00000+0  00000+0 0  9990
2 43873  55.2460 126.1903 0028814 193.5027 254.1002  2.00573551 37812
GPS BIII-2  (PRN 18)
1 44506U 19056A   24038.35952383 -.00000068  00000+0  00000+0 0  9998
2 44506  55.8396   5.2617 0038745 190.3465 353.6376  2.00569150 32807
GPS BIII-3  (PRN 23)
1 45854U 20041A   24038.44988073 -.00000004  00000+0  00000+0 0  9996
2 45854  56.0134  62.5667 0040332 193.2423 356.4021  2.00560020 26773
GPS BIII-4  (PRN 14)
1 46826U 20078A   24036.66815719  .00000098  00000+0  00000+0 0  9996
2 46826  54.2370 245.7928 0039738 193.2954 126.8470  2.00561669 24200
GPS BIII-5  (PRN 11)
1 48859U 21054A   24038.63247436 -.00000068  00000+0  00000+0 0  9991
2 48859  55.3611   6.9627 0014038 225.7263 257.9008  2.00565173 19493
GPS BIII-6  (PRN 28)
1 55268U 23009A   24037.41443029  .00000052  00000+0  00000+0 0  9998
2 55268  55.0884 182.3326 0004568 103.5844 259.0756  2.00573456  7969"""

    # 将字符串按换行符分割成列表
    tle_lines = tle_data.split('\n')
    #创建第一个包docment
    entity_0 = Create_Preamble(name="first", start=StartTime, stop=StopTime, multiplier=120)
    #添加文件包
    satellite_entity.append(entity_0)
    #循环添加卫星实体
    for i in range(0, len(tle_lines), 3):
        name=tle_lines[i].split('(')[0].strip()
        # 获取卫星每天绕地球的圈数
        circuits_day = float(tle_lines[i + 2][53:63])  # 每天绕地球圈数
        periodx = 24 * 60 * 60 / circuits_day  # 周期/s
        #卫星实体
        x1,x2 = Create_SatellitePacket(id=name, name=name,line1=tle_lines[i + 1],line2=tle_lines[i + 2],description= tle_lines[i],
                           image="data:image/png;base64,iVBORw0KGgoAAAANSUhEUgAAABAAAAAQCAYAAAAf8/9hAAAAAXNSR0IArs4c6QAAAARnQU1BAACxjwv8YQUAAAAJcEhZcwAADsMAAA7DAcdvqGQAAADJSURBVDhPnZHRDcMgEEMZjVEYpaNklIzSEfLfD4qNnXAJSFWfhO7w2Zc0Tf9QG2rXrEzSUeZLOGm47WoH95x3Hl3jEgilvDgsOQUTqsNl68ezEwn1vae6lceSEEYvvWNT/Rxc4CXQNGadho1NXoJ+9iaqc2xi2xbt23PJCDIB6TQjOC6Bho/sDy3fBQT8PrVhibU7yBFcEPaRxOoeTwbwByCOYf9VGp1BYI1BA+EeHhmfzKbBoJEQwn1yzUZtyspIQUha85MpkNIXB7GizqDEECsAAAAASUVORK5CYII=",
                           text="NO:"+str(i/3+1), period=periodx,start=StartTime,stop=StopTime,width=1,step=60)
        #添加卫星实体
        satellite_entity.append(x1)
        #添加地面炸与卫星可见实体
        satellite_entity.append(x2)

    #创建地面站实体
    Facility_Entity=Create_FacilityPacket(id="Facility/AGI",name="AGI",start=StartTime,stop=StopTime,text="AGI",
                                          image="data:image/png;base64,iVBORw0KGgoAAAANSUhEUgAAABAAAAAQCAYAAAAf8/9hAAAAAXNSR0IArs4c6QAAAARnQU1BAACxjwv8YQUAAAAJcEhZcwAADsMAAA7DAcdvqGQAAADJSURBVDhPnZHRDcMgEEMZjVEYpaNklIzSEfLfD4qNnXAJSFWfhO7w2Zc0Tf9QG2rXrEzSUeZLOGm47WoH95x3Hl3jEgilvDgsOQUTqsNl68ezEwn1vae6lceSEEYvvWNT/Rxc4CXQNGadho1NXoJ+9iaqc2xi2xbt23PJCDIB6TQjOC6Bho/sDy3fBQT8PrVhibU7yBFcEPaRxOoeTwbwByCOYf9VGp1BYI1BA+EeHhmfzKbBoJEQwn1yzUZtyspIQUha85MpkNIXB7GizqDEECsAAAAASUVORK5CYII=",
                                          position=[1216469.9357990976,-4736121.71856379,4081386.8856866374],description="<!--HTML-->\r\n<p>Pennsylvania, officially</p>"
    )
    #添加地面站实体
    satellite_entity.append(Facility_Entity)

    #创建Area实体
    Area_Entity=Create_AreaPacket(id="AreaTarget",name="Pennsylvania",start=StartTime,stop=StopTime, description="<!--HTML-->\r\n<p>Pennsylvania, off</p>",
                                  text="Pennsylvania",position=[ 1152255.80150063,-4694317.951340558,4147335.9067563135]
                                  )
    #添加Area实体
    satellite_entity.append(Area_Entity)

    #创建父packet
    parent_packet=Packet(id="9927edc4-e87a-4e1f-9b8b-0bfb3b05b227",name="Accesses",description="List of Accesses")
    satellite_entity.append(parent_packet)

    #创建czml文件，并添加所有实体
    doc = Document(satellite_entity)
    #保存
    # with open("example.czml", 'w', encoding="utf-8") as file:
    #     file.write(doc.dumps())
    print(doc.dumps())

# 记录程序开始时间
start_time = time.time()
#调用创建czml文件函数
Generate_czml()
# 记录程序结束时间
end_time = time.time()

# 计算程序运行时间
run_time = end_time - start_time
# print("程序运行时间为: ", run_time, "秒")


