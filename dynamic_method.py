from math import hypot
import parameter

vec_per = []
vec_all = []
status_list = []            #車輛本身狀態
vec_infront_list = []   #前方車的list
his_ave_speed = []      #算術平均車速
his_times = []


for x in range(parameter.vec_num*2):    #初始化list
    status_list.insert(x , "normal")        #初始的狀態都設定成常態
    vec_infront_list.insert(x , [])
    his_ave_speed.insert(x , 0)
    his_times.insert(x,0)

def main(vec , time):
    
    vec_all = vec
    vec_per = add_vec_info(vec_all)
    
    for x in vec_per :
        print(len(vec_per))
        inrange_information = vec_in_range(x , vec_per)

        x["in_range"] = inrange_information[0]
        x["inrange_dis"] = inrange_information[1]
        # print(x["id"])
        # print(x["in_range"])
        # print(x["inrange_dis"])
    
    vec_per = []
    print(len(vec_per))

def add_vec_info(vec_all):

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
                                 "in_range" : [],
                                 "inrange_dis" : {},
                                 "position" : -1,
                                 "ave_speed" : -1,
                                 "history_ave_speed" : his_ave_speed[int(x)],
                                #  "sensing_resource" :sen_all_re[int(x)],
                                #  "packet_resource" : [],
                                #  "resource" : resource_list[int(x)],
                                #  "tran_boo" : 0,
                                #  "reselected_counter" : rc_list[int(x)],                                 
                                }
                                )

    return vec_per
def infront_vec():
    global vec_per

    for x in vec_per:
            for y in x["in_range"]:
                if x["ypos"] > 2000:    #車輛y座標大於x軸高度
                    if x["direction"] == vec_per[y]["direction"]:
                        if x["direction"] == "forward":
                            if x["xpos"] > vec_per[y]["xpos"]:
                                vec_infront_list[x["id"]].append( {
                                        "id" : y,
                                        "dis" : hypot(x["xpos"] - vec_per[y]["xpos"] , x["ypos"] - vec_per[y]["ypos"]),
                                        "resource" : vec_per[y]["resource"]
                                    })
                        elif x["direction"] == "reserve":
                            if x["xpos"] < vec_per[y]["xpos"]:
                                vec_infront_list[x["id"]].append( {
                                        "id" : y,
                                        "dis" : hypot(x["xpos"] - vec_per[y]["xpos"] , x["ypos"] - vec_per[y]["ypos"]),
                                        "resource" : vec_per[y]["resource"]
                                    }) 
                elif x["ypos"] < 2000:
                    if x["direction"] == vec_per[y]["direction"]:
                        if x["direction"] == "reserve":
                            if x["xpos"] > vec_per[y]["xpos"]:
                                vec_infront_list[x["id"]].append( {
                                        "id" : y,
                                        "dis" : hypot(x["xpos"] - vec_per[y]["xpos"] , x["ypos"] - vec_per[y]["ypos"]),
                                        "resource" : vec_per[y]["resource"]
                                    })
                        elif x["direction"] == "forward":
                            if x["xpos"] < vec_per[y]["xpos"]:
                                vec_infront_list[x["id"]].append( {
                                        "id" : y,
                                        "dis" : hypot(x["xpos"] - vec_per[y]["xpos"] , x["ypos"] - vec_per[y]["ypos"]),
                                        "resource" : vec_per[y]["resource"]
                                    }) 
            get_method_parameter(x["id"])

def get_method_parameter(id):
    global his_ave_speed


    his_times[id] = his_times[id] + 1
    vec_per[id]["position"] = len(vec_infront_list[id])             #取得位置
    temp_speed = vec_per[id]["speed"]
    for i in vec_per[id]["in_range"]:                                                   #計算平均速度
        temp_speed = temp_speed + vec_per[i]["speed"]
    vec_per[id]["ave_speed"] = temp_speed / len(vec_per[id]["in_range"]) + 1
    his_ave_speed[id] = (his_ave_speed[id] + vec_per[id]["ave_speed"]) / his_times[id]              #計算算術平均速度

def vec_in_range(vec_cur , vec_per):     #計算範圍內的車輛

    inragne_list = []
    inrange_dis = {}
    for y in range(0 , len(vec_per)):
        dis = hypot(vec_per[y]["xpos"] - vec_cur["xpos"] , vec_per[y]["ypos"] - vec_cur["ypos"])
        if 0< dis < 300 :
            inragne_list.append(y)
            inrange_dis[y]= dis

    return inragne_list , inrange_dis

def status_judge():
    print("這邊放公式")