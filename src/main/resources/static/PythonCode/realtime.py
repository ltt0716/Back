import czml3
import numpy as np
from czml3 import Document,Packet
import datetime
import random
from sgp4.io import twoline2rv
from sgp4.earth_gravity import wgs72
from datetime import datetime, timedelta
import sys
import math
import re

# 定义地面站类
class Station:
    def __init__(self, id, name, description, position_x, position_y, position_z):
        # 地面站属性
        self.id = id    #id
        self.name = name    #name
        self.description = description  #description
        self.position_x = position_x    #笛卡尔坐标（X）
        self.position_y = position_y    #笛卡尔坐标（Y）
        self.position_z = position_z    #笛卡尔坐标（Z）

#定义卫星类
class Satelite:
    #初始化
    def __init__(self,name,number,category,launch_time,e,Perigee_angle,
                 Perihelion_angle,circuits_day,line1,line2):

        self.name = name    # 名
        self.number = number    # 编号
        self.category = category    # 卫星类别
        self.launch_time = launch_time  # 发射年份
        self.e = e  # 轨道偏心率
        self.Perigee_angle = Perigee_angle  # 近地幅角
        self.Perihelion_angle = Perihelion_angle    # 平近地角
        self.circuits_day = circuits_day    # 每天绕地球圈数
        self.line1=line1
        self.line2=line2

    #html化卫星description
    def to_Description(self):
        head=f"<div><h1 >卫星属性一览</h1></div>"
        table=f"<table>" \
              f"<tr><td>卫星名：</td><td>{self.name}</td></tr>" \
              f"<tr><td>卫星编号：</td><td>{self.number}</td></tr>" \
              f"<tr><td>卫星类别：</td><td>{self.category}</td></tr>" \
              f"<tr><td>发射年份：</td><td>{self.launch_time}</td></tr>" \
              f"<tr><td>轨道偏心率：</td><td>{self.e}</td></tr>" \
              f"<tr><td>近地幅角：</td><td>{self.Perigee_angle}</td></tr>" \
              f"<tr><td>平近地角：</td><td>{self.Perihelion_angle}</td></tr>" \
              f"<tr><td>绕地球圈数/天：</td><td>{self.circuits_day}</td></tr>" \
              "</table>"

        tle=f"<div><p>{self.line1}</p><p>{self.line2}</p></div>"

        description=head+table+tle
        return description

ID_color1=[184, 7, 43, 155]
Vis_color2=[131, 79, 186, 155]
# 宽度
sate_width1 = 1
Vis_width2 = 1
# tle or 六参数
tleORsix = 1
#卫星实体
satellite_entity=[]
#各大导航卫星的tle
Iridium=r'''IRIDIUM 7
1 24793U 97020B   24145.94221896  .00000739  00000+0  25167-3 0  9992
2 24793  86.3953 339.5728 0002013  81.6332 278.5092 14.35226750416196
IRIDIUM 5
1 24795U 97020D   24145.81019409  .00008917  00000+0  84483-3 0  9997
2 24795  86.3924 261.7073 0124090  85.6550 275.8842 14.87728208427592
IRIDIUM 4
1 24796U 97020E   24145.89436387  .00000770  00000+0  25773-3 0  9990
2 24796  86.3946 336.7281 0002228  85.1214 275.0237 14.36151671416722
IRIDIUM 914
1 24836U 97030A   24145.91789761  .00000861  00000+0  26713-3 0  9992
2 24836  86.3936 346.4625 0003862  76.2175 283.9453 14.40009183551237'''
GlobalStar=r'''GLOBALSTAR M001
1 25162U 98008A   24150.58388358 -.00000103  00000+0 -46940-4 0  9993
2 25162  52.0058   9.7091 0001922 134.5945 242.2614 12.38184615196195
GLOBALSTAR M004
1 25163U 98008B   24150.38923962 -.00000086  00000+0  10077-3 0  9998
2 25163  51.9970 144.9966 0002863 156.0774 351.5748 12.63360857213176
GLOBALSTAR M002
1 25164U 98008C   24150.34813425 -.00000082  00000+0 -11459-3 0  9999
2 25164  51.9988 122.6087 0000989 159.9837 200.1022 11.61503093139463
GLOBALSTAR M003
1 25165U 98008D   24150.42188789  .00000039  00000+0  13701-2 0  9998
2 25165  51.9840 151.4042 0007972 241.1618 266.9966 12.12006037186688
GLOBALSTAR M014
1 25306U 98023A   24150.58897912 -.00000059  00000+0  35071-3 0  9992
2 25306  51.9864  53.2932 0001453  29.8781  46.1004 11.65468138146440
GLOBALSTAR M006
1 25307U 98023B   24150.26241361 -.00000042  00000+0  68862-3 0  9995
2 25307  51.9935  92.2428 0003556 127.7977  21.2832 11.58164292172341
GLOBALSTAR M015
1 25308U 98023C   24150.36344236 -.00000074  00000+0 -11635-4 0  9995
2 25308  51.9781 172.8729 0012448 114.8455 345.0738 11.48852680149966
GLOBALSTAR M008
1 25309U 98023D   24150.54279966 -.00000096  00000+0  89266-6 0  9993
2 25309  51.9962 230.3134 0002762  96.1995   7.1210 12.36043700190406
GLOBALSTAR M023
1 25621U 99004A   24150.39890876 -.00000071  00000+0  18316-3 0  9990
2 25621  52.0081 142.0468 0010350   0.2924 146.8203 12.62455049167258
GLOBALSTAR M040
1 25622U 99004B   24150.38351778 -.00000083  00000+0  11715-3 0  9992
2 25622  51.9889 145.6809 0000679 289.6265 217.9088 12.61975336166799
GLOBALSTAR M036
1 25623U 99004C   24150.34893649 -.00000074  00000+0  13509-3 0  9990
2 25623  51.9932 172.0077 0011174  34.0093  69.9909 11.86566598133415
GLOBALSTAR M038
1 25624U 99004D   24150.28444267 -.00000070  00000+0  20768-3 0  9993
2 25624  51.9968  97.1400 0002116 345.1170 162.4047 12.32500548155039
GLOBALSTAR M022
1 25649U 99012A   24150.46711032 -.00000080  00000+0  81926-4 0  9991
2 25649  52.0043 254.0125 0003077 131.0821 309.0482 12.02483201130210
GLOBALSTAR M041
1 25650U 99012B   24150.32471424 -.00000068  00000+0  21788-3 0  9991
2 25650  51.9997 124.1448 0002658 290.1607  69.8943 11.96660516132321
GLOBALSTAR M046
1 25651U 99012C   24150.37108972 -.00000134  00000+0 -50482-3 0  9990
2 25651  52.0040 218.4183 0002625 200.3901 252.6687 12.09392227137227
GLOBALSTAR M037
1 25652U 99012D   24150.50360429 -.00000081  00000+0  12680-3 0  9991
2 25652  52.0012 272.4906 0002208  76.3420   1.2275 12.62406776162812
GLOBALSTAR M045
1 25676U 99019A   24150.42462605 -.00000045  00000+0  42708-3 0  9998
2 25676  51.9984 319.0521 0001007 132.7160 242.9338 12.27038435146280
GLOBALSTAR M019
1 25677U 99019B   24150.15448559 -.00000087  00000+0  30037-4 0  9990
2 25677  51.9896  63.1672 0000545 304.4337 203.8183 12.13858288138508
GLOBALSTAR M044
1 25678U 99019C   24150.00568044 -.00000076  00000+0  10933-3 0  9997
2 25678  51.9986 326.8808 0006417  25.9076 151.8239 11.90233262125578
GLOBALSTAR M042
1 25679U 99019D   24150.55039826 -.00000043  00000+0  46215-3 0  9995
2 25679  52.0037  53.9495 0002279 224.8504 199.2963 12.22062452138353
GLOBALSTAR M025
1 25770U 99031A   24150.51382562 -.00000068  00000+0 -25509-4 0  9997
2 25770  51.9838 328.0739 0001283 193.0586 202.6926 11.22550695438621
GLOBALSTAR M049
1 25771U 99031B   24150.55258653 -.00000078  00000+0 -43546-3 0  9996
2 25771  51.9899 343.4684 0003483  90.8962 269.2233 11.12109453 74745
GLOBALSTAR M047
1 25772U 99031C   24150.09829210 -.00000055  00000+0  39700-3 0  9990
2 25772  51.9866  18.1614 0016148 325.8992  34.0776 11.31921011427616
GLOBALSTAR M052
1 25773U 99031D   24150.30712959 -.00000075  00000+0 -32255-3 0  9997
2 25773  51.9859  98.0951 0002599 265.1343 265.1809 11.15051493435681
GLOBALSTAR M035
1 25851U 99037A   24150.41619500 -.00000057  00000+0  24778-3 0  9990
2 25851  51.9919 190.8040 0013099  81.1858  19.2914 11.04530893 53853
GLOBALSTAR M032
1 25852U 99037B   24150.06129002 -.00000021  00000+0  14740-2 0  9993
2 25852  51.9981  43.2956 0009341 239.6792 120.3084 11.19053308 91785
GLOBALSTAR M051
1 25853U 99037C   24150.57307623 -.00000045  00000+0  65877-3 0  9991
2 25853  51.9793 246.3077 0001425 228.6918 131.3770 11.42197835 88555
GLOBALSTAR M030
1 25854U 99037D   24150.21472850 -.00000108  00000+0 -69626-3 0  9995
2 25854  51.9886  77.6906 0004198  76.7713 283.3572 11.55095607105679
GLOBALSTAR M048
1 25872U 99041A   24150.37703159 -.00000078  00000+0 -20864-3 0  9993
2 25872  51.9330 166.9733 0013754 241.1779 223.9156 11.33846685 81443
GLOBALSTAR M026
1 25873U 99041B   24150.60228756 -.00000123  00000+0 -21605-2 0  9999
2 25873  52.0029 312.3849 0001037 358.1818  80.0514 11.06835421106017
GLOBALSTAR M043
1 25874U 99041C   24150.58281003 -.00000111  00000+0 -12700-2 0  9994
2 25874  51.9404 258.8403 0012106  19.7438  77.9373 11.25680558 79679
GLOBALSTAR M028
1 25875U 99041D   24150.59310647 -.00000068  00000+0  21057-3 0  9999
2 25875  51.9628 256.8513 0062820 318.4787  41.1312 12.50556411142184
GLOBALSTAR M024
1 25883U 99043A   24150.47334712 -.00000135  00000+0 -25013-2 0  9997
2 25883  51.9973 166.4078 0001614 207.6117 323.6962 11.10157740 72243
GLOBALSTAR M027
1 25884U 99043B   24150.54185406 -.00000094  00000+0 -11344-2 0  9996
2 25884  52.0205 233.3677 0021508  93.1363 267.1891 11.04368473 98856
GLOBALSTAR M054
1 25885U 99043C   24150.18517260 -.00000063  00000+0  20068-3 0  9993
2 25885  52.0155  65.8993 0004259 244.4208 264.9611 11.39203421 75289
GLOBALSTAR M053
1 25886U 99043D   24150.01345562 -.00000053  00000+0  44231-3 0  9997
2 25886  52.0010 352.0951 0003924 139.2887  30.5944 11.27655438 76101
GLOBALSTAR M058
1 25907U 99049A   24150.13455076 -.00000033  00000+0  69152-3 0  9999
2 25907  51.9961  54.6773 0001867 269.0299  91.0321 11.93179980495694
GLOBALSTAR M050
1 25908U 99049B   24150.02979014 -.00000157  00000+0 -77662-3 0  9994
2 25908  51.9991  91.3324 0009504 348.2097  93.0575 12.07434805101783
GLOBALSTAR M033
1 25909U 99049C   24149.94680124 -.00000093  00000+0 -17884-4 0  9995
2 25909  51.9935 349.9366 0011857 193.9010 166.1512 12.20273706488837
GLOBALSTAR M055
1 25910U 99049D   24150.02696888 -.00000070  00000+0  21077-3 0  9994
2 25910  52.0044  19.1525 0007813  56.3702 303.7895 12.29402052121038
GLOBALSTAR M057
1 25943U 99058A   24150.55859495 -.00000104  00000+0 -10267-3 0  9991
2 25943  52.0010 356.9025 0001531 318.4729  41.6004 12.24787737119999
GLOBALSTAR M059
1 25944U 99058B   24150.34879142 -.00000077  00000+0  11256-3 0  9997
2 25944  51.9986 165.5636 0000620 272.7231 188.5375 11.99962490527964
GLOBALSTAR M056
1 25945U 99058C   24150.48663556 -.00000044  00000+0  50451-3 0  9997
2 25945  51.9929 177.0034 0000867 146.7734  25.2600 12.04775795116377
GLOBALSTAR M031
1 25946U 99058D   24150.24131632 -.00000034  00000+0  57072-3 0  9992
2 25946  51.9961  92.9786 0001547  99.7888  48.5128 12.16009709117839
GLOBALSTAR M039
1 25961U 99062A   24150.53205331 -.00000048  00000+0  31013-3 0  9996
2 25961  51.9867 357.2222 0002290 199.2020 160.8761 12.62292941131765
GLOBALSTAR M034
1 25962U 99062B   24150.55104781 -.00000102  00000+0 -33298-3 0  9995
2 25962  51.9885 288.6031 0013948  40.0576  39.1445 11.79429001 93122
GLOBALSTAR M029
1 25963U 99062C   24149.91026733 -.00000067  00000+0  24326-3 0  9995
2 25963  51.9824  55.1142 0003169  77.1260   2.4100 11.99878552122991
GLOBALSTAR M061
1 25964U 99062D   24150.30059920 -.00000070  00000+0  17302-3 0  9995
2 25964  51.9783 108.1992 0006371 325.9532 202.5912 11.76762782 75984
GLOBALSTAR M063
1 26081U 00008A   24150.08679446 -.00000133  00000+0 -74043-3 0  9990
2 26081  51.9978  43.1399 0004274 305.9841 201.7146 11.86155004111997
GLOBALSTAR M062
1 26082U 00008B   24150.39422053 -.00000072  00000+0  18650-3 0  9998
2 26082  51.9818 144.3746 0007192  12.5189 135.5236 12.43436984448876
GLOBALSTAR M060
1 26083U 00008C   24150.55304288 -.00000122  00000+0 -30530-3 0  9994
2 26083  52.0041  49.6406 0003973  62.3492   8.9457 12.17632534105632
GLOBALSTAR M064
1 26084U 00008D   24150.39502911 -.00000068  00000+0  21786-3 0  9991
2 26084  51.9999 145.6828 0001488  29.3499 330.7417 11.88519820121467
GLOBALSTAR M065
1 31571U 07020A   24150.48832684 -.00000081  00000+0  12880-3 0  9992
2 31571  51.9905 314.0866 0010310 174.5770 220.4216 12.61971438784965
GLOBALSTAR M069
1 31573U 07020C   24150.50668494 -.00000069  00000+0  19161-3 0  9998
2 31573  51.9958 269.8809 0000879 145.7000 338.2764 12.62274083786099
GLOBALSTAR M072
1 31574U 07020D   24150.55808714 -.00000076  00000+0  15726-3 0  9996
2 31574  52.0105   5.6450 0001044  85.1524 292.2975 12.62263835784372
GLOBALSTAR M071
1 31576U 07020F   24150.52323794 -.00000064  00000+0  22136-3 0  9995
2 31576  52.0074 274.9824 0000614 105.6974 333.0019 12.62266966447281
GLOBALSTAR M067
1 32263U 07048A   24150.22417262 -.00000058  00000+0  29167-3 0  9994
2 32263  51.9738  79.4137 0000409 275.2305 232.5458 12.40645992761824
GLOBALSTAR M070
1 32264U 07048B   24150.51068616 -.00000078  00000+0  14150-3 0  9990
2 32264  51.9738 217.3146 0000129  83.1798  21.9400 12.62293542765217
GLOBALSTAR M066
1 32265U 07048C   24149.99085490 -.00000074  00000+0  16844-3 0  9998
2 32265  51.9683  80.8707 0000531  41.5831  37.7381 12.62262774767416
GLOBALSTAR M068
1 32266U 07048D   24149.88218594 -.00000052  00000+0  28924-3 0  9998
2 32266  51.9907  33.7133 0001496  39.2395  42.6930 12.62790448769002
GLOBALSTAR M079
1 37188U 10054A   24150.53990407 -.00000088  00000+0  90418-4 0  9998
2 37188  52.0032 227.6704 0000606 154.5183 309.9914 12.62270622628009
GLOBALSTAR M074
1 37189U 10054B   24150.40264914 -.00000084  00000+0  10982-3 0  9995
2 37189  52.0008 227.4709 0000384 141.0111 298.6799 12.62269255628590
GLOBALSTAR M076
1 37190U 10054C   24150.51293722 -.00000080  00000+0  13254-3 0  9999
2 37190  52.0019 227.2688 0000564 190.9925 271.8750 12.62261734628329
GLOBALSTAR M077
1 37191U 10054D   24150.59420132 -.00000104  00000+0  59656-6 0  9991
2 37191  52.0048 183.7691 0000003 105.8557  65.1685 12.62273726628703
GLOBALSTAR M075
1 37192U 10054E   24150.52401900 -.00000076  00000+0  15321-3 0  9993
2 37192  51.9954 269.7060 0000762 129.2728 323.3198 12.62274866627551
GLOBALSTAR M073
1 37193U 10054F   24150.28392990 -.00000096  00000+0  41320-4 0  9996
2 37193  52.0036 183.9653 0000173 191.4765 248.2705 12.62265943629353
GLOBALSTAR M083
1 37739U 11033A   24150.13832802 -.00000111  00000+0 -39562-4 0  9999
2 37739  51.9836 133.6613 0000414  67.5013  11.7893 12.62270163598356
GLOBALSTAR M088
1 37740U 11033B   24150.13044905 -.00000103  00000+0  29349-5 0  9993
2 37740  51.9757  39.4994 0000903  77.6005  86.2446 12.62268283593896
GLOBALSTAR M091
1 37741U 11033C   24150.58698873 -.00000084  00000+0  11063-3 0  9992
2 37741  52.0018   0.9806 0001143  94.3607 283.8981 12.62263173594742
GLOBALSTAR M085
1 37742U 11033D   24150.49806550 -.00000082  00000+0  11936-3 0  9993
2 37742  51.9878 312.6276 0001074 109.7440 285.3146 12.62271421595249
GLOBALSTAR M081
1 37743U 11033E   24150.61303885 -.00000082  00000+0  12137-3 0  9995
2 37743  51.9971 314.8288 0001017 119.2641 317.7349 12.62265410595401
GLOBALSTAR M089
1 37744U 11033F   24150.49472337 -.00000087  00000+0  96174-4 0  9990
2 37744  51.9937 269.4911 0000455 158.4528 279.3249 12.62264197596231
GLOBALSTAR M084
1 38040U 11080A   24150.36462543 -.00000097  00000+0  36267-4 0  9994
2 38040  51.9987 136.9676 0000291 339.5532 168.4654 12.62262970574193
GLOBALSTAR M080
1 38041U 11080B   24150.42117854 -.00000101  00000+0  16024-4 0  9999
2 38041  52.0037 138.2677 0000345 284.3650 240.5081 12.62273231574329
GLOBALSTAR M082
1 38042U 11080C   24150.27211984 -.00000096  00000+0  41532-4 0  9997
2 38042  52.0075  94.1273 0001069  57.5026  89.0253 12.62269736575014
GLOBALSTAR M092
1 38043U 11080D   24150.56604671 -.00000108  00000+0 -23955-4 0  9993
2 38043  52.0059 183.5884 0000071  55.9385 108.4116 12.62262908573500
GLOBALSTAR M090
1 38044U 11080E   24150.21934817 -.00000092  00000+0  63641-4 0  9991
2 38044  51.9886  88.5902 0000759  62.5594  84.5081 12.62263471575122
GLOBALSTAR M086
1 38045U 11080F   24150.24573970 -.00000095  00000+0  51262-4 0  9993
2 38045  51.9900  89.0303 0000630 157.0119 350.7006 12.62271258575073
GLOBALSTAR M097
1 39072U 13005A   24149.76508953 -.00000089  00000+0  81441-4 0  9992
2 39072  52.0069   4.6557 0001003  97.2324 262.8657 12.62263305522266
GLOBALSTAR M093
1 39073U 13005B   24150.53029021 -.00000086  00000+0  10107-3 0  9991
2 39073  51.9832 356.2419 0001119 100.9046 259.1946 12.62259657522318
GLOBALSTAR M094
1 39074U 13005C   24150.60943454 -.00000084  00000+0  10850-3 0  9998
2 39074  51.9965 269.9983 0000900 131.2328 228.8617 12.62266370523936
GLOBALSTAR M096
1 39075U 13005D   24150.46419666 -.00000085  00000+0  10343-3 0  9994
2 39075  52.0087 318.6551 0001163 111.8406 248.2584 12.62266126522836
GLOBALSTAR M078
1 39076U 13005E   24149.88391485 -.00000028  00000+0  42251-3 0  9997
2 39076  51.9894  45.4557 0001623  58.0924 302.0101 12.62276881521382
GLOBALSTAR M095
1 39077U 13005F   24150.06797785 -.00000083  00000+0  11339-3 0  9997
2 39077  51.9822  42.2776 0001391  78.4153 281.6870 12.62266615521260
GLOBALSTAR M087
1 52888U 22064A   24150.50282188 -.00000082  00000+0  88028-4 0  9991
2 52888  51.9762 273.5328 0008784 318.9814  41.0425 13.37575217 95027'''
Telesat=r'''AMSC 1   
1 23553C 95019A   24150.75000000  .00000016  00000+0  00000+0 0  1500
2 23553  12.6147  21.4840 0004442  43.2818 345.5169  1.00270394    10
ANIK F1  
1 26624C 00076A   24150.00000000  .00000028  00000+0  00000+0 0  1502
2 26624   3.2553  83.9627 0009391 359.4873  54.4556  1.00268792    11
NIMIQ 2  
1 27632C 02062A   24150.75000000  .00000028  00000+0  00000+0 0  1501
2 27632   7.6892  64.4059 0005499   8.5733 335.5831  1.00272050    11
ANIK F2  
1 28378C 04027A   24150.62500000  .00000040  00000+0  00000+0 0  1507
2 28378   1.3494  88.7535 0002796 350.7496 282.0373  1.00270132    17
XTAR-EUR 
1 28542C 05005A   24150.79166667  .00000241  00000+0  00000+0 0  1505
2 28542   2.4025  86.0429 0003066 346.3244 129.4426  1.00271945    14
ANIK F1R 
1 28868C 05036A   24150.75000000  .00000016  00000+0  00000+0 0  1504
2 28868   2.3852  85.8571 0003828 353.3550 331.2564  1.00271028    19
ANIK F3  
1 31102C 07009A   24150.75000000  .00000089  00000+0  00000+0 0  1501
2 31102   0.0166 286.9355 0002217 148.3254 323.7916  1.00273033    10
NIMIQ 4  
1 33373C 08044A   24150.75000000 -.00000131  00000+0  00000+0 0  1502
2 33373   0.0161 286.1819 0002199 148.3701   1.2208  1.00268762    15
TELSTAR 11N
1 34111C 09009A   24150.79166667 -.00003814  00000+0  00000+0 0  1502
2 34111   0.0128  49.2295 0002525  12.9663  73.0550  1.00271304    14
TERRESTAR-1
1 35496C 09035A   24150.75000000  .00000040  00000+0  00000+0 0  1509
2 35496   4.3950  47.4155 0002950  24.9952 334.3443  1.00271388    18
NIMIQ 5  
1 35873C 09050A   24150.75000000 -.00000167  00000+0  00000+0 0  1506
2 35873   0.0347 112.4552 0002950 318.6214  13.9833  1.00269462    11
SKYTERRA 1 
1 37218C 10061A   24150.75000000 -.00000023  00000+0  00000+0 0  1506
2 37218   3.5827  48.1019 0002976 357.8681  10.4844  1.00270330    11
TELSTAR 14R
1 37602C 11021A   24150.75000000 -.00000171  00000+0  00000+0 0  1504
2 37602   0.0303 104.2199 0003242 312.0639  38.4819  1.00271734    16
NIMIQ 6  
1 38342C 12026A   24150.75000000 -.00000083  00000+0  00000+0 0  1504
2 38342   0.0062 341.5971 0002838  79.9870   5.0666  1.00272268    13
ANIK G1  
1 39127C 13014A   24150.75000000  .00000016  00000+0  00000+0 0  1509
2 39127   0.0205 283.9055 0001488 136.6842 349.8659  1.00271531    19
TELSTAR 12V
1 41036C 15068A   24150.75000000 -.00000029  00000+0  00000+0 0  1507
2 41036   0.0127 291.4146 0002443 141.4927  69.8647  1.00269529    19
VIASAT-2 
1 42740C 17029A   24150.04166667 -.00000178  00000+0  00000+0 0  1508
2 42740   0.0264  89.9292 0000405 341.4412 120.7949  1.00270207    10
TELSTAR 19V
1 43562C 18059A   24150.75000000 -.00000188  00000+0  00000+0 0  1502
2 43562   0.0337 159.2900 0002695 306.1820 349.2967  1.00270033    10
TELSTAR 18V
1 43611C 18069A   24150.79166667 -.00000696  00000+0  00000+0 0  1508
2 43611   0.0333 136.1881 0002325 298.3720 236.2449  1.00269777    17
AMOS-17
1 44479C 19050A   24150.75000000  .00000193  00000+0  00000+0 0  1507
2 44479   0.0325  97.4113 0001720   2.1224  75.2129  1.00269871    17'''

def angle_between_vectors(vec1, vec2):
    # # 归一化两个向量
    vec1 = vec1 / np.linalg.norm(vec1)
    vec2 = vec2 / np.linalg.norm(vec2)

    # 计算点积和叉积
    dot_product = np.dot(vec1,vec2)
    cross_product = np.cross(vec1,vec2)

    # 计算夹角的正弦值和余弦值
    sine = np.linalg.norm(cross_product)
    cosine = dot_product

    # 计算夹角（弧度）
    angle_rad = np.arctan2(sine, cosine)

    # 转换为角度
    angle_deg = np.degrees(angle_rad)

    return angle_deg
#创建第一个包preamble
def Create_Preamble(start,stop,current,name="simple",multiplier=60):
    clock={
        "interval": f"{start}/{stop}",
        "currentTime": f"{current}",
        "multiplier": multiplier,
        "range": "LOOP_STOP",
        "step": "SYSTEM_CLOCK_MULTIPLIER"
    }
    #初始化Preamable包
    data = czml3.Preamble(version="1.0", name=name, clock=clock)
    #返回
    return data

#接收地面站参数，返回地面站列表
def ReturnStations(Station_str):
    #定义地面站列表
    StationList=[];
    # 字符串处理
    stations_str = Station_str[1:-1].split("),")

    #循环处理
    for i in range(0, len(stations_str)):
        if(i!=len(stations_str)-1):
            stations_str[i] += ")"
        # 输入的字符串示例
        # station_str = "Station(id=11, name=22, description=33, position_x=444.0, position_y=55.0, position_z=66.0)"
        # 使用正则表达式提取键值对
        matches = re.findall(r'(\w+)=([\w.-]+)', stations_str[i])
        # 构建参数字典
        params = dict(matches)
        # 创建 Station 对象
        station = Station(**params)
        #添加入列表
        StationList.append(station)
    #返回地面站列表
    return StationList

#计算卫星位置
def Satellite_Position(line1,line2,startime,stoptime,step,StationList):
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
    #存储卫星相对于每个地面站的可见性
    for i in range(0,len(StationList)):
        Aviliable.append([])

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
        #循环计算卫星与地面站的可见性
        for i in range(0,len(StationList)):
            # 地面站位置(每个)
            position_x=float(StationList[i].position_x)
            position_y = float(StationList[i].position_y)
            position_z = float(StationList[i].position_z)
            F_position = [position_x, position_y,position_z]
            If_Visiable = Determine_Visible(F_position, position)
            # if(If_Visiable==True):
            Aviliable[i].append((current_time, If_Visiable))
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
    if(len(tem1)!=0):
        if (len(tem1) == len(tem2)):
            for i in range(0, len(tem1)):
                aviliable.append(f"{tem1[i]}/{tem2[i]}")
        elif(len(tem1) ==1):
            aviliable.append(f"{tem1[0]}/{stop}")
        else:
            for i in range(0, len(tem1) - 1):
                aviliable.append(f"{tem1[i]}/{tem2[i]}")
            aviliable.append(f"{tem1[len(tem1) - 1]}/{stop}")
    # print(aviliable)
    show=[]
    if(len(tem1)!=0):
        if (len(tem1) == len(tem2)):
            tem ={
                "interval": f"0000-01-01T00:00:00Z/{tem1[0]}",
                "boolean": False
            }
            show.append(tem)
            for i in range(0, len(tem1)):
                tmp = {
                    "interval": f"{tem1[i]}/{tem2[i]}",
                    "boolean": True
                }
                show.append(tmp)
                if (i == len(tem1) - 1):
                    tmp = {
                        "interval": f"{tem2[i]}/{stop}",
                        "boolean": False
                    }
                    show.append(tmp)
                else:
                    tmp = {
                        "interval": f"{tem2[i]}/{tem1[i + 1]}",
                        "boolean": False
                    }
                    show.append(tmp)
        elif(len(tem1) ==1):
            tem01 ={
                "interval": f"0000-01-01T00:00:00Z/{tem1[0]}",
                "boolean": False
            }
            tem02 ={
                "interval": f"{tem1[0]}/{stop}",
                "boolean": True
            }
            show.append(tem01)
            show.append(tem02)
        else:
            tem ={
                "interval": f"0000-01-01T00:00:00Z/{tem1[0]}",
                "boolean": False
            }
            show.append(tem)
            for i in range(0, len(tem1) - 1):
                tmp = {
                    "interval": f"{tem1[i]}/{tem2[i]}",
                    "boolean": True
                }
                show.append(tmp)
                if (i == len(tem1) - 1):
                    tmp = {
                        "interval": f"{tem1[i]}/{stop}",
                        "boolean": True
                    }
                    show.append(tmp)
                else:
                    tmp = {
                        "interval": f"{tem2[i]}/{tem1[i + 1]}",
                        "boolean": False
                    }
                    show.append(tmp)
    else:
        tmp = {
            "interval": f"0000-01-01T00:00:00Z/9999-01-01T00:00:00Z",
            "boolean": False
        }
        show.append(tmp)


    # print(aviliable)
    # print(show)
    #返回
    return aviliable,show

#创建卫星与地面站相联系的packet
def Create_FacilityToSatellite(id,name,parent,description,available,show,F_id,S_id):
    #属性
    polyline={
        "show":show,
        "width":Vis_width2,
        "material": {
            "solidColor": {
                "color": {
                    "rgba":Vis_color2
                }
            }
        },
        "arcType": "NONE",
        "positions": {
            "references": [
                f"{F_id}#position", f"{S_id}#position"
            ]
        }

    }

    data=Packet(id=id,name=name,description=description,parent=parent,polyline=polyline,availability=available)
    #返回
    return data

#计算卫星与地面站可见时间段
def Acess_Times(aviliable):
    head=f"<div style=' display=flex;justify-content=center;'><h2 >可见时间段一览</h2></div>"
    table=f"<table style='border-collapse: separate;'><tr><th>开始时间</th><th>结束时间</th><th>持续时间</th></tr>"

    for time_str in aviliable:
        times=time_str.split('/')
        start=datetime.strptime(times[0], "%Y-%m-%dT%H:%M:%SZ")
        end = datetime.strptime(times[1], "%Y-%m-%dT%H:%M:%SZ")
        seconds=(end-start).total_seconds()
        #每行显示
        tr=f"<tr><td>{start}</td><td>{end}</td><td>{seconds}s</td></tr>"
        table+=tr

    table+=f"</table>"

    return head+table
#创建卫星packet
def Create_SatellitePacket(id,name,line1,line2,description,image,text,period,timeslot,start,stop,StationList,width=1,step=60):
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

    # period=1200 #test
    #时间段的2倍
    timeslot=timeslot*2

    lead_time = {}
    trail_time = {}
    # leadtime、trialtime属性
    property_interval = "interval"
    property_epoch = "epoch"
    property_number = "number"

    # 设置leadtime属性
    lead_time[property_interval] = f"{StartTime}/{StopTime}"
    lead_time[property_epoch] = f"{StartTime}"
    lead_time[property_number] = [
        0, timeslot,
        timeslot, 0
    ]
    # 设置trailtime属性
    trail_time[property_interval] = f"{StartTime}/{StopTime}"
    trail_time[property_epoch] = f"{StartTime}"
    trail_time[property_number] = [
        0, 0,
        timeslot, timeslot
    ]
    # 属性列表添加到字典中
    lead_times.append(lead_time)
    trail_times.append(trail_time)

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
                     "rgba":[
        random_numbers[0], random_numbers[1], random_numbers[2], random_numbers[3]
    ]
                }
            }
        },
        "resolution": 120,
        "leadTime":lead_times,
        "trailTime":trail_times
    }
    #某个卫星的坐标以及与每个地面站的可见性
    cartesian,Aviliable=Satellite_Position(line1=line1,line2=line2,startime=start,stoptime=stop,step=step,StationList=StationList)
    # print(Aviliable)
    position={
        "interpolationAlgorithm": "LAGRANGE",
        "interpolationDegree": 5,
        "referenceFrame": "INERTIAL",
        "epoch": start,
        "cartesian": cartesian
    }

    Station_datas = []
    # 卫星包
    data = Packet(id=id, name=name, availability=availability, description=description, label=label,
                  billboard=billboard, path=path, position=position)

    for i in range(0,len(StationList)):
        aviliable, show = Calculate_Visiable(start, stop, Aviliable[i])
        # print(aviliable)
        description = Acess_Times(aviliable)
        # 地面站与卫星的可见性包
        data2 = Create_FacilityToSatellite(id=f"{StationList[i].id}/" + id, name=f"{StationList[i].name}/" + id,
                                           parent="9927edc4-e87a-4e1f-9b8b-0bfb3b05b227",F_id=StationList[i].id,
                                           description=description,available=aviliable, show=show, S_id=id)
        #返回列表
        Station_datas.append(data2)

    #返回对象
    return data,Station_datas

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
            "rgba":ID_color1
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

    F_S=[F_x-S_x,F_y-S_y,F_z-S_z]
    angle=angle_between_vectors(F_S,F_position)
    # print(D,F_position,F_S,angle)
    if(angle>=90):
        return True
    else:
        return False

#解析卫星属性信息
def Analysi_Satellite(name,line1,line2):

    name=name   #名
    number=line1[2:7]   #编号
    category=line1[7]   #卫星类别
    launch=line1[9:11]   #发射年份
    launch_time="19"+launch+"年" if int(launch)>24 else "20"+launch+"年"
    e="0."+line2[26:33] #轨道偏心率
    Perigee_angle=line2[34:42]+"°"  #近地幅角
    Perihelion_angle=line2[43:51]+"°"   #平近地角
    circuits_day = float(line2[52:63])  #每天绕地球圈数
    #卫星类
    sate=Satelite(name,number,category,launch_time,e,Perigee_angle,
                  Perihelion_angle,circuits_day,line1,line2)

    return sate

#创建czml文件
def Generate_czml(start,stop,current,tle_data,StationList):
    #开始、结束时间
    StartTime=start
    StopTime=stop
    #tle数据
    tle_data1 =tle_data
    # 将字符串按换行符分割成列表
    tle_lines = tle_data1.split('\n')
    #创建第一个包docment
    entity_0 = Create_Preamble(name="first", start=StartTime, stop=StopTime,current=current,multiplier=1)
    #添加文件包
    satellite_entity.append(entity_0)
    #循环添加卫星实体
    for i in range(0, len(tle_lines), 3):
        # name=tle_lines[i].split('(')[0].strip()
        # 获取卫星每天绕地球的圈数
        sate = Analysi_Satellite(tle_lines[i], tle_lines[i + 1], tle_lines[i + 2])
        name=sate.name
        circuits_day = sate.circuits_day # 每天绕地球圈数
        periodx = 24 * 60 * 60 / circuits_day  # 周期/s
        description = sate.to_Description()
        #卫星实体
        x1,x2 = Create_SatellitePacket(id=name, name=name,line1=tle_lines[i + 1],line2=tle_lines[i + 2],description= description,timeslot=600,
                                       image="data:image/png;base64,iVBORw0KGgoAAAANSUhEUgAAABAAAAAQCAYAAAAf8/9hAAAAAXNSR0IArs4c6QAAAARnQU1BAACxjwv8YQUAAAAJcEhZcwAADsMAAA7DAcdvqGQAAADJSURBVDhPnZHRDcMgEEMZjVEYpaNklIzSEfLfD4qNnXAJSFWfhO7w2Zc0Tf9QG2rXrEzSUeZLOGm47WoH95x3Hl3jEgilvDgsOQUTqsNl68ezEwn1vae6lceSEEYvvWNT/Rxc4CXQNGadho1NXoJ+9iaqc2xi2xbt23PJCDIB6TQjOC6Bho/sDy3fBQT8PrVhibU7yBFcEPaRxOoeTwbwByCOYf9VGp1BYI1BA+EeHhmfzKbBoJEQwn1yzUZtyspIQUha85MpkNIXB7GizqDEECsAAAAASUVORK5CYII=",
                                       text=name, period=periodx,start=StartTime,stop=StopTime,width=1,step=3,StationList=StationList)

        # 添加卫星实体
        satellite_entity.append(x1)
        # 循环添加卫星实体及地面站可见实体
        for i in range(0,len(x2)):
            # 添加地面炸与卫星可见实体
            satellite_entity.append(x2[i])


    for i in range(0,len(StationList)):
        F_position = [float(StationList[i].position_x), float(StationList[i].position_y), float(StationList[i].position_z)]
        # 创建地面站实体
        Facility_Entity = Create_FacilityPacket(id=StationList[i].id, name=StationList[i].name, start=StartTime, stop=StopTime,
                                                text="text:"+StationList[i].id,
                                                image="data:image/png;base64,iVBORw0KGgoAAAANSUhEUgAAABAAAAAQCAYAAAAf8/9hAAAAAXNSR0IArs4c6QAAAARnQU1BAACxjwv8YQUAAAAJcEhZcwAADsMAAA7DAcdvqGQAAACvSURBVDhPrZDRDcMgDAU9GqN0lIzijw6SUbJJygUeNQgSqepJTyHG91LVVpwDdfxM3T9TSl1EXZvDwii471fivK73cBFFQNTT/d2KoGpfGOpSIkhUpgUMxq9DFEsWv4IXhlyCnhBFnZcFEEuYqbiUlNwWgMTdrZ3JbQFoEVG53rd8ztG9aPJMnBUQf/VFraBJeWnLS0RfjbKyLJA8FkT5seDYS1Qwyv8t0B/5C2ZmH2/eTGNNBgMmAAAAAElFTkSuQmCC",
                                                position=F_position,description="description"+StationList[i].id)
        # 添加地面站实体
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

# StartTime="2012-03-15T10:00:00Z"    #ISO 8601 标准的时间格式
# StopTime="2012-03-16T10:00:00Z"

# 开始时间 ISO 8601
StartTime = sys.argv[1]
# StartTime="2012-03-15T10:00:00Z"
# 结束时间 ISO 8601
StopTime = sys.argv[2]
# StopTime="2012-03-15T10:20:00Z"
# 当前时间ISO 8601
CurrentTime = sys.argv[3]
# CurrentTime ="2012-03-15T10:10:00Z"
#接收前端所传的导航系统
NS_Name = sys.argv[4]
# NS_Name="[GPSS]"
NS_Names = NS_Name[1:-1].split(',')    #数据处理
tle_datas = ""
for i in range(0,len(NS_Names)):
    if(i!=0):
        tle_datas+='\n'+eval(NS_Names[i])
    else:
        tle_datas += eval(NS_Names[i])

#颜色
ID_color1= sys.argv[6]
ID_color1= [int(x) for x in ID_color1[5:-1].split(',')]
Vis_color2 = sys.argv[7]
Vis_color2 = [int(x) for x in Vis_color2[5:-1].split(',')]
#宽度
sate_width1 = int(sys.argv[8])
Vis_width2 = int(sys.argv[9])
# #tle or 六参数
tleORsix=int(sys.argv[10])

# 获取地面站信息（列表）
Station_str = sys.argv[5]
StationList=ReturnStations(Station_str)
# Station_str="[Station(id=AGI, name=AGI, description=AGI, position_x=1216469.9357990976, position_y=-4736121.71856379, position_z=4081386.8856866374)," \
#             "Station(id=BUPT, name=BUPT, description=BUPT, position_x=-2173482.480052372, position_y=4386503.05048138, position_z=4074714.5434855656)]"



Generate_czml(start=StartTime,stop=StopTime,current=CurrentTime,tle_data=tle_datas,StationList=StationList)







