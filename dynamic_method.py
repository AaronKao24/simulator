from math import hypot , floor  , ceil
import parameter
import dynamic_select_resource as select

vec_per = []
vec_all = []

####parammeter####

global total_resource 
total_resource = 400

####parammeter####

def main(vec , time , vec_local , error_data):
    vec_local_data = vec_local
    vec_all = vec
    vec_per = add_vec_info(vec_all , vec_local_data)
    for x in vec_per :          #取得範圍內的車輛資訊
        inrange_information = vec_in_range(x , vec_per)
        x["in_range"] = inrange_information[0]
        x["inrange_dis"] = inrange_information[1]
    if time % 100 == 0:
        print(time , ": ")
    for x in vec_per:
        for y in x["in_range"]:
            if x["direction"] == vec_per[y]["direction"]:
                if vec_per[y]["status"] == "normal":
                    high_boo=""
                    low_boo=""
                    get_method_parameter(x,vec_per)
                    high_pool = [ 0 , floor(re_pool_allocation(x)[0])]
                    low_pool = [ total_resource - floor(re_pool_allocation(x)[1]) + 1, total_resource-1]
                    normal_pool = [(floor(re_pool_allocation(x)[0])+ 1) ,total_resource-floor(re_pool_allocation(x)[1])]
                    # print(high_pool ," / ",normal_pool , " / " , low_pool )
                    if x["speed"] > x["ave_speed"]:
                        high_boo = get_high_status(x , vec_per)
                    else :
                        low_boo = get_low_status(x , vec_per)
                    if high_boo == "yes":
                        x["status"] = "high"
                        x["resource_pool"] = high_pool
                    elif low_boo == "yes":
                        x["status"] = "low"
                        x["resource_pool"] = low_pool
                    else:
                        x["status"] = "normal"
                        x["resource_pool"] = normal_pool
    result = select.main(vec_per , time , error_data)
    error_list = result[0]
    vec_return = result[1]

    for x in vec_return:
        vec_local_data[0][x["id"]] = x["history_ave_speed"]
        vec_local_data[1][x["id"]] = x["speed_counter"] +1 
        vec_local_data[2][x["id"]] = x["resource"]
        vec_local_data[3][x["id"]] = x["reselected_counter"]
        vec_local_data[4][x["id"]] = x["sensing_resource"]
        vec_local_data[5][x["id"]] = x["status"]
        vec_local_data[6][x["id"]] = x["resource_pool"]
        vec_local_data[7][x["id"]] = x["sensing_special"]

    # if time % 100 ==0:
    #     print(time , " : ")
    #     for x in vec_per:
    #         print(x["position"] ," / " , x["ave_speed"] , " / ", x["history_ave_speed"] ," / ", x["higher_ave"]," / " , x["higher_sum"])
            
    vec_per = []
    return vec_local_data , error_list

def add_vec_info(vec_all , vec_local_data):
    vec_per = []
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
                                 "status" : vec_local_data[5][int(x)],
                                 "in_range" : [],
                                 "inrange_dis" : {},
                                 "position" : -1,
                                 "ave_speed" : 0,
                                 "history_ave_speed" : vec_local_data[0][int(x)],
                                 "speed_counter" : vec_local_data[1][int(x)],
                                 "higher_ave" : 0,
                                 "higher_sum" : 0,
                                 "lower_sum" : 0,
                                 "number_same_direction" : 0,
                                 "resource_pool" : vec_local_data[6][int(x)],
                                 "resource_dis" : [ 0 for i in range(total_resource)],
                                 "sensing_resource" :vec_local_data[4][int(x)],
                                 "packet_resource" : [],
                                 "resource" : vec_local_data[2][int(x)],
                                 "tran_boo" : 0,
                                 "reselected_counter" : vec_local_data[3][int(x)],    
                                 "sensing_special" : vec_local_data[7][int(x)],                             
                                }
                                )

    return vec_per
def get_infront_vec_number(vec , vec_per):

    length = 0
    for x in vec["in_range"]:
        if vec["ypos"] > 2000:
            if vec["direction"] == vec_per[x]["direction"]:
                if vec["direction"] == "forward":
                    if vec["xpos"] < vec_per[x]["xpos"]:
                        length += 1
                
                elif vec["direction"] == "reserve":
                    if vec["xpos"] > vec_per[x]["xpos"]:
                        length += 1

        if vec["ypos"] < 2000:
            if vec["direction"] == vec_per[x]["direction"]:
                if vec["direction"] == "reserve":
                    if vec["xpos"] < vec_per[x]["xpos"]:
                        length += 1
                
                elif vec["direction"] == "forward":
                    if vec["xpos"] > vec_per[x]["xpos"]:
                        length += 1

    return length

def get_method_parameter(vec , vec_per):
    
    higher_counter = 1
    higher_sum = 0
    lower_sum =0
    num = 1

    vec["position"] = get_infront_vec_number(vec , vec_per)

    temp_speed = vec["speed"]
    for x in vec["in_range"]:
        if vec["direction"] == vec_per[x]["direction"]:
            num = num + 1
            temp_speed = temp_speed + vec_per[x]["speed"]
    vec["ave_speed"] = temp_speed / num
    vec["history_ave_speed"] = ((vec["history_ave_speed"] * (vec["speed_counter"]-1))+vec["ave_speed"]) / vec["speed_counter"]
    higher_sum = vec["speed"] - vec["ave_speed"]
    for x in vec["in_range"]:
        if vec["direction"] == vec_per[x]["direction"]:
            if vec_per[x]["speed"] > vec["ave_speed"]:
                higher_counter += 1
                higher_sum = higher_sum + (vec_per[x]["speed"] - vec["ave_speed"])
            else :
                lower_sum = lower_sum + abs(vec_per[x]["speed"] - vec["ave_speed"])
    if vec["speed"] < vec["ave_speed"]:
        higher_counter = higher_counter -1
    vec["higher_ave"] = higher_counter
    vec["higher_sum"] = higher_sum
    vec["loewwr_sum"] = lower_sum
    vec["number_same_direction"] = num
def vec_in_range(vec_cur , vec_per):     #計算範圍內的車輛

    # print(vec_per)
    inragne_list = []
    inrange_dis = {}
    for y in range(0 , len(vec_per)):
        dis = hypot(vec_per[y]["xpos"] - vec_cur["xpos"] , vec_per[y]["ypos"] - vec_cur["ypos"])
        if dis > vec_cur["resource_dis"][vec_per[y]["resource"]]:
            vec_cur["resource_dis"][vec_per[y]["resource"]] = dis
        if 0< dis < 300 :
            inragne_list.append(y)
            inrange_dis[y]= dis

    return inragne_list , inrange_dis
def re_pool_allocation(vec):
    if vec["number_same_direction"] > 0:
        high_pool = total_resource * (vec["higher_ave"] / vec["number_same_direction"])*(vec["history_ave_speed"]/(vec["ave_speed"] + (2.5 * vec["history_ave_speed"])))
        low_pool = total_resource * ((vec["number_same_direction"] - vec["higher_ave"] ) / vec["number_same_direction"])*(vec["history_ave_speed"]/(vec["ave_speed"] + (2.5 * vec["history_ave_speed"])))
        normal_pool = total_resource -(high_pool + low_pool)

        return high_pool ,low_pool


def get_high_status(vec , vec_per):
    judge_counter = 0
    num = 1
    judge_speed = (1+ (vec["higher_ave"] / vec["number_same_direction"])) * (vec["higher_sum"] / vec["higher_ave"])
    judge_number = ceil((vec["higher_ave"]+vec["position"]) / vec["number_same_direction"] * vec["higher_ave"])
    for x in vec["in_range"]:
        if vec["direction"] == vec_per[x]["direction"]:
            num += 1
            if vec["speed"] > vec_per[x]["speed"] + judge_speed:
                judge_counter += 1
    # print("Hn : " , vec["higher_ave"] , " Ph : " , vec["position"] , "N : " , vec["number_same_direction"] , "vecspeeda : " , vec["higher_sum"] )
    # print("total : " , num , "超過數量： " , judge_counter , "須超過數量： " , judge_number , "須超過速度： " , judge_speed)
    if judge_counter > judge_number:
        return "yes"
    else :
        return "no"

    print(judge_speed ," / " , judge_number)
def get_low_status(vec , vec_per):
    judge_counter = 0
    N = vec["number_same_direction"]
    Ln = N - vec["higher_ave"] +1
    Pl = N - vec["position"]

    # print( N , " / " , Ln )
    judge_speed = (1+(Ln / N)) * (vec["lower_sum"] / Ln)
    judge_number = ceil((Ln + Pl) / N * Ln)
    # print(judge_number , " / " , judge_speed)

    for x in vec["in_range"]:
        if vec["direction"] == vec_per[x]["direction"]:
            if vec["speed"] < vec_per[x]["speed"] - judge_speed:
                judge_counter += 1

    if judge_counter > judge_number:
        return "yes"
    else:
        return "no"
