import parameter
from operator import itemgetter
from math import hypot , ceil

vec_per = []
vec_all = {}
vec_back_list = []
for x in range(parameter.vec_num*2):    #初始化list
    vec_back_list.insert(x , [])        #初始化後方車輛list
    


def main(vec , time):
    
    global vec_all
    global vec_per
    vec_all = vec
    add_vec_info()
    get_back_vec(time)
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
                                 "direction" : temp_dir
                                #  "in_range" : [],
                                #  "sensing_resource" :sen_all_re[int(x)],
                                #  "packet_resource" : [],
                                #  "resource" : resource_list[int(x)],
                                #  "tran_boo" : 0,
                                #  "reselected_counter" : rc_ilst[int(x)],
                                #  "inrange_dis" : {},
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
            if time %1000 ==0:
                print(x["id"]," : ",vec_back_list[x["id"]])
