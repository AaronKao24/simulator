import parameter
from operator import itemgetter
from math import hypot , ceil
import random

vec_per = []
vec_all = {}
vec_back_list = []
rc_list = []    #reselected counter 的list
resource_list = []      #資源list

for x in range(parameter.vec_num*2):    #初始化list
    vec_back_list.insert(x , [])        #初始化後方車輛list
    rc_list.insert(x , 0) 


def main(vec , time):
    
    global vec_all
    global vec_per
    global rc_list

    vec_all = vec
    add_vec_info()
    get_back_vec(time)
    vec_in_range()

    for x in vec_per:
        if time % 100 == 0:                         #每100ms判斷要不要重選資源
            if x["reselected_counter"] == 0:
                get_resource(x["id"])
        if (x["resource"]//4) == (time%100):        #確認該車輛的資源會不會在這個ms傳輸
            x["tran_boo"] = 1
            rc_list[x["id"]] = rc_list[x["id"]] -1
    vec_per = [] 
    return 0

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
                                #  "sensing_resource" :sen_all_re[int(x)],
                                #  "packet_resource" : [],
                                #  "resource" : resource_list[int(x)],
                                 "tran_boo" : 0,
                                 "reselected_counter" : rc_list[int(x)],
                                 
                                #  "select_time" : select_time_list[int(x)],
                                 
                                })

def get_back_vec(time):
    for x in range(parameter.vec_num*2):    #初始化list
        vec_back_list.insert(x , [])        #初始化後方車輛list
    global get_back_vec

    for x in vec_per:
        for y in vec_per:
            if x["ypos"] > 2000:    #車輛y座標大於y軸高度
                if y["direction"] == x["direction"]:    #判斷同方向
                    if x["direction"] == "forward":     #若正向 則 小於比較對象為先行車
                        if x["xpos"] < y ["xpos"]:
                            vec_back_list[x["id"]].insert(y["id"] , {
                                "id" : y["id"],
                                "dis" : hypot(x["xpos"] - y["xpos"] , x["ypos"] - y["ypos"])
                            })
                    else:
                        if x["xpos"] > y["xpos"]:
                            vec_back_list[x["id"]].insert(y["id"] , {
                                "id" : y["id"],
                                "dis" : hypot(x["xpos"] - y["xpos"] , x["ypos"] - y["ypos"])
                            })
            elif x["ypos"] < 2000:  #車輛y座標小於y軸高度
                if x["direction"] == "reserve":
                    if y["direction"] == x["direction"]:    #判斷同方向
                        if x["xpos"] < y ["xpos"]:
                            vec_back_list[x["id"]].insert(y["id"] , {
                                    "id" : y["id"],
                                    "dis" : hypot(x["xpos"] - y["xpos"] , x["ypos"] - y["ypos"])
                                })
                        else:
                            if x["xpos"] > y["xpos"]:
                                vec_back_list[x["id"]].insert(y["id"] , {
                                    "id" : y["id"],
                                    "dis" : hypot(x["xpos"] - y["xpos"] , x["ypos"] - y["ypos"])
                                })
                                
        if len(vec_back_list[x["id"]]) > 5: 
            vec_back_list[x["id"]] = sorted(vec_back_list[x["id"]] , key=itemgetter("dis"))


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
        resource_list[id] = random.choice(re_pool)  #選擇資源
