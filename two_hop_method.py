import parameter
from operator import itemgetter
import math
import random
from math import hypot , ceil
import collision_judge as cj

####list zoon####
vec_per = []
vec_all = {}
vec_back_list = []
vec_twohop_list = []    #2hop方法最終結果
sen_all_re = []     #偵測的資源分組
rc_list = []    #reselected counter 的list
resource_list = []      #資源list
error_count = []      #錯誤的數量統計
total_count = []        #傳輸數量總數
sec_error_count = []    #一次性的錯誤統計
sec_total_count = []    #一次性總數統計    
two_hop_list = []
twohop_exclude_list = []    #2hop所排除之資源
last_xpos = []          #上次的xpos
last_ypos = []          #上次的ypos
next_xpos = []          #預測的xpos
next_ypos = []          #預測的ypos
last_speed = []         #上次的速度


for x in range(parameter.vec_num*2):    #初始化list
    vec_back_list.insert(x , [])        #初始化後方車輛list
    rc_list.insert(x , 0) 
    error_count.insert(x , 0)
    total_count.insert(x , 0)
    sec_error_count.insert(x , 0)
    sec_total_count.insert(x , 0)
    two_hop_list.insert(x , [])
    sen_all_re.insert(x , [])
    resource_list.insert(x , -1)
    vec_twohop_list.insert(x , [])
    twohop_exclude_list.insert(x ,[])
    last_xpos.insert(x,[])
    last_ypos.insert(x,[])
    next_xpos.insert(x,0)
    next_ypos.insert(x,0)
    last_speed.insert(x , [])
    for i in range (0,15):
        last_xpos[x].insert(i,0)
        last_ypos[x].insert(i,0)
        last_speed[x].insert(i,0)
for x in range(parameter.vec_num*2):
    for y in range(0,10):
        sen_all_re[x].insert(y , [])

####list zoon####
def main(vec , time):

    global vec_all
    global vec_per
    global rc_list
    global sen_all_re
    global error_count
    global total_count
    global sec_error_count
    global sec_total_count
    global two_hop_list
    global vec_twohop_list
    global twohop_exclude_list
    global last_xpos
    global last_ypos
    
    for x in range(parameter.vec_num*2):
        twohop_exclude_list.insert(x ,[])

    if time % 1000 == 0:
        print(time , " : " )
    vec_all = vec
    add_vec_info()
    get_back_vec(time)
    vec_in_range()

    if time % 100 == 0:
        get_next_position()
        two_hop_function()
        exclude_resource()

    for x in vec_per:
        if time % 100 == 0:                         #每100ms判斷要不要重選資源
            if x["reselected_counter"] == 0:
                get_resource(x["id"])
        if (x["resource"]//4) == (time%100):        #確認該車輛的資源會不會在這個ms傳輸
            x["tran_boo"] = 1
            rc_list[x["id"]] = rc_list[x["id"]] -1

    for x in vec_per:
        get_packet_resource(x["id"])

    for x in vec_per:
        error_boo = 0
        error_boo_tra = 0                           #給計算單台傳輸的boolean
        if x["tran_boo"] == 1:
            for y in x["in_range"]:
                ###傳輸有錯率###
                error_boo = cj.error_main(vec_per[y]["packet_resource"] , vec_per[x["id"]]["resource"])
                if error_boo == 1:
                    sec_error_count[x["id"]] += 1
                    if error_boo_tra ==0:
                        error_boo_tra = 1
                    
            if error_boo_tra == 1:
                error_count[x["id"]] += 1

            total_count[x["id"]] += 1
            sec_total_count[x["id"]] += len(x["in_range"])

        get_sensing_resource(x["id"])
    vec_per = [] 
    return error_count , total_count , sec_error_count , sec_total_count

def add_vec_info():
    global vec_per
    global vec_all
    for x in vec_all:
        if int(x) % 2 == 0:
            temp_dir = "forward"
        else :
            temp_dir = "reserve"
        vec_per.insert(int(x) , {

                                 "id" : int(x) ,
                                 "time" : int(float(vec_all[x][3])),
                                 "speed" : float(vec_all[x][0]),
                                 "xpos"  : float(vec_all[x][1]),
                                 "ypos"  : float(vec_all[x][2]),
                                 "direction" : temp_dir,
                                 "in_range" : [],
                                 "inrange_dis" : {},
                                 "sensing_resource" :sen_all_re[int(x)],
                                 "packet_resource" : [],
                                 "resource" : resource_list[int(x)],
                                 "tran_boo" : 0,
                                 "reselected_counter" : rc_list[int(x)],
                                 
                                #  "select_time" : select_time_list[int(x)],
                                 
                                })

def get_back_vec(time):
    global vec_back_list
    global vec_twohop_list
    
    for x in range(parameter.vec_num*2):    #初始化list
        vec_back_list.insert(x , [])        #初始化後方車輛list
    
    for x in vec_per:
        for y in vec_per:
            if x["ypos"] > 2000:    #車輛y座標大於y軸高度
                if y["direction"] == x["direction"]:    #判斷同方向
                    if x["direction"] == "forward":     #若正向 則 小於比較對象為先行車
                        if x["xpos"] < y ["xpos"]:
                            vec_back_list[x["id"]].insert(y["id"] , {
                                "id" : y["id"],
                                "dis" : hypot(x["xpos"] - y["xpos"] , x["ypos"] - y["ypos"]),
                                "resource" : y["resource"]
                            })
                    else:
                        if x["xpos"] > y["xpos"]:
                            vec_back_list[x["id"]].insert(y["id"] , {
                                "id" : y["id"],
                                "dis" : hypot(x["xpos"] - y["xpos"] , x["ypos"] - y["ypos"]),
                                "resource" : y["resource"]
                            })
            elif x["ypos"] < 2000:  #車輛y座標小於y軸高度
                if x["direction"] == "reserve":
                    if y["direction"] == x["direction"]:    #判斷同方向
                        if x["xpos"] < y ["xpos"]:
                            vec_back_list[x["id"]].insert(y["id"] , {
                                    "id" : y["id"],
                                    "dis" : hypot(x["xpos"] - y["xpos"] , x["ypos"] - y["ypos"]),
                                    "resource" : y["resource"]
                                })
                        else:
                            if x["xpos"] > y["xpos"]:
                                vec_back_list[x["id"]].insert(y["id"] , {
                                    "id" : y["id"],
                                    "dis" : hypot(x["xpos"] - y["xpos"] , x["ypos"] - y["ypos"]),
                                    "resource" : y["resource"]
                                })
        vec_twohop_list = vec_back_list


def vec_in_range():     #計算範圍內的車輛
    for x in range(0 , len(vec_per)) :
        for y in range(0 , len(vec_per)):
            dis = hypot(vec_per[y]["xpos"] - vec_per[x]["xpos"] , vec_per[y]["ypos"] - vec_per[x]["ypos"])
            if 0< dis < 300 :
                vec_per[x]["in_range"].append(y)
                vec_per[x]["inrange_dis"][y] = dis

def get_resource(id):     #取得資源且重置RC
    if vec_per[id]["reselected_counter"] == 0 :     #當RC=0後重新選擇
        select_resource(id)
        rc_list[id] = random.randint(5,15)      #選完資源後設定RC

def select_resource(id):    #選擇資源
    re_pool = []
    resource_list[id] = -1

    for x in range(0,400):      #將所有資源做判斷能否進入待選list
        add_boo = 1
        for y in range(0,9):    #假設資源在1000感應內
            if x in vec_per[id]["sensing_resource"][y]:
                add_boo = 0
        if add_boo == 1:
            re_pool.append(x)
    if len(re_pool) < 400 * 0.2:    #資源少於全部20%  增加到20%
        for x in range(ceil(400*0.2) - len(re_pool)):
            sort_temp = 0
            id_temp = -1
            for y in vec_per[id]["inrange_dis"].keys():
                if vec_per[y]["resource"] not in re_pool: 
                    if vec_per[id]["inrange_dis"][y] > sort_temp:
                        sort_temp = vec_per[id]["inrange_dis"][y]
                        id_temp = y
            if id_temp != -1:
                re_pool.append(vec_per[id_temp]["resource"])
                del vec_per[id]["inrange_dis"][id_temp]

    else:
        # print(re_pool)
        for i in twohop_exclude_list :
            if i in re_pool:
                re_pool.remove(i)
        resource_list[id] = random.choice(re_pool)  #選擇資源

def get_packet_resource(id):        #新增車輛的資源偵測
    for x in vec_per[id]["in_range"]:
        if vec_per[x]["tran_boo"] == 1:
            vec_per[id]["packet_resource"].insert(x , vec_per[x]["resource"])


def get_sensing_resource(vec_id):       #將偵測的資源做分組
    global sen_all_re

    for x in vec_per[vec_id]["packet_resource"]:
        if (vec_per[vec_id]["time"])>1000 and (vec_per[vec_id]["time"]%100) ==0:
            sen_all_re[vec_id][(vec_per[vec_id]["time"]//100) % 10] = []

        if x not in sen_all_re[vec_id][(vec_per[vec_id]["time"]//100) % 10]:
            sen_all_re[vec_id][(vec_per[vec_id]["time"]//100) % 10].append(x)
        
def two_hop_function():     #取的2hop的資源
    global two_hop_list
    global vec_back_list
    global last_xpos , last_ypos , next_xpos , next_ypos

    for x in vec_per:
        for y in x["in_range"]:
            if len(vec_twohop_list[y]) >0:
                for i in vec_back_list[y]:
                    if i["resource"] not in two_hop_list[x["id"]]:
                        if hypot(next_xpos[x["id"]] - next_xpos[y] , next_ypos[x["id"]] - next_ypos[y]) < 300 :
                            two_hop_list[x["id"]].append(i["resource"])
        # print(x["id"] , " : " , two_hop_list[x["id"]])
 
def exclude_resource():
    global vec_per
    global last_xpos , last_ypos , next_xpos , next_ypos

    for x in vec_per:
        for y in vec_per:
            for z in vec_back_list[x["id"]]:
                if y["id"] == z["id"]:
                    if x["resource"] in two_hop_list[y["id"]]:
                        vec_per[x["id"]]["reselected_counter"] = 0
                    
                    for i in two_hop_list[y["id"]]:
                        if i not in twohop_exclude_list[x["id"]]:
                            twohop_exclude_list[x["id"]].append(i)

def get_next_position():
    global last_xpos , last_ypos , next_xpos , next_ypos , last_speed

    for x in vec_per:
        # print(x["id"]," : " , " x:" , last_xpos[x["id"]] , "y: " , last_ypos[x["id"]])
        nextx = ((x["speed"] * 1.5) + ((x["speed"]-last_speed[x["id"]][0])*0.75)) * ((x["xpos"] - last_xpos[x["id"]][0])**2 / (hypot(x["xpos"] - last_xpos[x["id"]][0], x["ypos"] - last_ypos[x["id"]][0]))**2)
        nexty = ((x["speed"] * 1.5) + ((x["speed"]-last_speed[x["id"]][0])*0.75)) * ((x["ypos"] - last_ypos[x["id"]][0])**2 / (hypot(x["xpos"] - last_xpos[x["id"]][0], x["ypos"] - last_ypos[x["id"]][0]))**2)
        next_xpos[x["id"]] = nextx
        next_ypos[x["id"]] = nexty

        for i in range(14):
            last_xpos[x["id"]][i] = last_xpos[x["id"]][i+1]
            last_ypos[x["id"]][i] = last_ypos[x["id"]][i+1]
            last_speed[x["id"]][i] = last_speed[x["id"]][i+1]

        last_xpos[x["id"]][14] = x["xpos"]
        last_ypos[x["id"]][14] = x["ypos"]       
        last_speed[x["id"]][14] = x["speed"]