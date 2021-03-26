

vec_per = []
vec_all = []
status_list = []            #車輛本身狀態

for x in range(parameter.vec_num*2):    #初始化list
    status_list.insert(x , "normal")        #初始的狀態都設定成常態
def main(vec , time):
    
    vec_all = vec
    add_vec_info()
    

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
                                 "status" : status_list[int(x)],
                                #  "in_range" : [],
                                #  "inrange_dis" : {},
                                #  "sensing_resource" :sen_all_re[int(x)],
                                #  "packet_resource" : [],
                                #  "resource" : resource_list[int(x)],
                                #  "tran_boo" : 0,
                                #  "reselected_counter" : rc_list[int(x)],                                 
                                })

def infront_vec():
    for x in vec_per:
        for y in vec_per:
            if y["id"] in x["in_range"]:
                if x["ypos"] > 2000:    #車輛y座標大於y軸高度
                    if y["direction"] == x["direction"]:    #判斷同方向
                        if x["direction"] == "forward":     #若正向 則 小於比較對象為先行車
                            if x["xpos"] < y ["xpos"]:
                                vec_back_list[x["id"]].append( {
                                    "id" : y["id"],
                                    "dis" : hypot(x["xpos"] - y["xpos"] , x["ypos"] - y["ypos"]),
                                    "resource" : y["resource"]
                                })
                        else:
                            if x["xpos"] > y["xpos"]:
                                vec_back_list[x["id"]].append( {
                                    "id" : y["id"],
                                    "dis" : hypot(x["xpos"] - y["xpos"] , x["ypos"] - y["ypos"]),
                                    "resource" : y["resource"]
                                })
                elif x["ypos"] < 2000:  #車輛y座標小於y軸高度
                    if x["direction"] == "reserve":
                        if y["direction"] == x["direction"]:    #判斷同方向
                            if x["xpos"] < y ["xpos"]:
                                vec_back_list[x["id"]].append({
                                        "id" : y["id"],
                                        "dis" : hypot(x["xpos"] - y["xpos"] , x["ypos"] - y["ypos"]),
                                        "resource" : y["resource"]
                                    })
                            else:
                                if x["xpos"] > y["xpos"]:
                                    vec_back_list[x["id"]].append({
                                        "id" : y["id"],
                                        "dis" : hypot(x["xpos"] - y["xpos"] , x["ypos"] - y["ypos"]),
                                        "resource" : y["resource"]
                                    })

def status_judge():
    print("這邊放公式")