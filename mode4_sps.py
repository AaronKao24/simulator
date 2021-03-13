
from math import hypot , ceil
import random
import parameter 
import collision_judge as cj
import rc_method as rm
import copy

#global variable

vec_all = {}
vec_per = []
sen_all_re = []
rc_ilst = []
select_time_list = []
rc_method_list = []
resource_list = []
error_count = []
total_count = []
rc_resouce = []
del_rc_list = []
sec_error_count = []
sec_total_count = []
rm_sensing_list = {}
counter_great = 0
counter_total = 0
counter_same_time = 0
counter_same_total = 0
total_test = 0
rc_counter = 0
mode4_counter = 0
len_rc_counter = 0
out_len_counter = 0
rc_error_c = 0             #測試RC方法會不會有相同RC問題

parameter.para()
for x in range(parameter.vec_num*2):
        sen_all_re.insert(x , [] )              #將sensing resource第一層設定
        rc_ilst.insert(x , 0)                   #將rc list設定出來
        resource_list.insert(x , -1)            #將資源列表先建出來
        select_time_list.insert(x , 0)
        error_count.insert(x , 0)
        total_count.insert(x , 0)
        sec_error_count.insert(x , 0)
        sec_total_count.insert(x , 0)        
for x in range(parameter.vec_num*2):
    for y in range(0,10):
        sen_all_re[x].insert(y , [])            #將sensing resource第二設定

#global variable

def mode_main(vec , time):
    global vec_all 
    global vec_per
    global sen_all_re
    global error_count
    global re_error
    global total_count
    global sec_error_count
    global sec_total_count
    global rc_method_list
    global counter_great
    global rm_sensing_list
    global counter_total
    global select_time_list
    global counter_same_time
    global counter_same_total
    global total_test
    global rc_counter
    global mode4_counter
    global len_rc_counter
    global out_len_counter
    global rc_error_c
    global rc_resouce

    re_error = 0    
    vec_all = vec

    add_vec_info()
    vec_in_range()

    ###RC method zoon###
    """
    rc_method_list = []
    del_rc_list = []
    rm_sensing_list = {}
    for x in vec_per:
        if time % 100 == 0:
            # print(x["reselected_counter"] , parameter.rc_small)
            # print(type(parameter.rc_small))
            if x["reselected_counter"] == parameter.rc_small - 1:
                rc_method_list.insert(x["id"] , {
                                                    "id" : x["id"],
                                                    "resource" : x["resource"],
                                                    "in_range" : x["in_range"],
                                                    "xpos" : x["xpos"],
                                                    "ypos" : x["ypos"],
                                                })
    # print(rc_method_list)
    if len(rc_method_list) > 1 :
        temp_rm_list = []
        for x in rc_method_list:
            boo_rc_same = 0
            for y in rc_method_list:
                if x["id"] != y["id"]:
                    if x["resource"] == y["resource"]:
                        boo_rc_same = 1
                        break
            if boo_rc_same == 0:
                temp_rm_list.append(x)
        rc_method_list = copy.deepcopy(temp_rm_list)


        # print(rc_method_list)
        temp_rc = rm.rc_method(rc_method_list)
        for x in temp_rc[0]:
            rc_resouce.append(x)
            counter_great += temp_rc[1]
        # print("------------------------------------------")
        # print(rc_resouce)
        
    
    for x in vec_per:
        temp_list = []
        for y in rc_resouce:
            if y["id"] in x["in_range"] :
                temp_list.append(y["resource"])

        rm_sensing_list[x["id"]] = temp_list
    # if time %100 ==0:
        # print(rm_sensing_list)
    if time % 100 == 0:
        temp_same_list = []
        for x in rc_resouce:
            boo_rc_same = 0
            for y in rc_resouce:
                if x["id"] != y["id"]:
                    if x["resource"] == y["resource"]:
                        boo_rc_same = 1
            if boo_rc_same == 0:
                temp_same_list.append(x)
        rc_resouce = copy.deepcopy(temp_same_list)
    
    if time % 100 == 0:
        for x in rc_resouce:
            for y in rc_resouce:
                if x["id"] != y["id"]:
                    if x["resource"] == y["resource"]:
                        rc_error_c += 1

    for x in vec_per:
        boo_inlen = 0
        temp_remo_list = []
        if time % 100 ==0:
            if x["reselected_counter"] == 0:
                total_test += 1
                if len(rc_resouce) > 0:
                    len_rc_counter += 1
                    for y in rc_resouce:
                        if x["id"] == y["id"]:
                            rc_counter += 1
                            # print(type(y["resource"]))
                            resource_list[x["id"]] = y["resource"]
                            rc_ilst[x["id"]] = random.randint(5,15)
                            del_rc_list.append(x["id"])
                            temp_remo_list.append(y)
                            boo_inlen = 1
                    for y in temp_remo_list:
                        rc_resouce.remove(y)

                    if x["id"] not in del_rc_list:
                        # print("x[id] = " , x["id"] , " list : " , del_rc_list)
                        mode4_counter += 1
                        get_resource(x["id"])
                        boo_inlen = 1
                if boo_inlen == 0:
                    out_len_counter += 1
                    print(out_len_counter)
                    get_resource(x["id"])
                select_time_list[x["id"]] = time
        # print(type(x["resource"]))
        if (x["resource"]*2//1) == (time%100):
            x["tran_boo"] = 1
            rc_ilst[x["id"]] = rc_ilst[x["id"]] -1

    # if time % 100 ==0:
    #     print("end" , rc_resouce , del_rc_list)
    ###End RC method####
    
    """
    for x in vec_per:
        if time % 100 == 0:                         #每100ms判斷要不要重選資源
            if x["reselected_counter"] == 0:
                get_resource(x["id"])
                select_time_list[x["id"]] = time
        if (x["resource"]//4) == (time%100):        #確認該車輛的資源會不會在這個ms傳輸
            x["tran_boo"] = 1
            rc_ilst[x["id"]] = rc_ilst[x["id"]] -1
    
    
    for x in vec_per:
        get_packet_resource(x["id"])
    
    
    for x in vec_per:
        error_boo = 0
        error_boo_tra = 0                           #給計算單台傳輸的boolean
        if x["tran_boo"] == 1:
            for y in x["in_range"]:
                ###傳輸有錯率###
                error_boo = cj.error_main(vec_per[y]["packet_resource"] , vec_per[x["id"]]["resource"])
                if vec_per[y]["select_time"] == vec_per[x["id"]]["select_time"]:
                    counter_same_total += 1
                if error_boo == 1:
                    if vec_per[y]["select_time"] == vec_per[x["id"]]["select_time"]:
                        counter_same_time += 1
                    sec_error_count[x["id"]] += 1
                    if error_boo_tra ==0:
                        error_boo_tra = 1
                    
            if error_boo_tra == 1:
                error_count[x["id"]] += 1

            total_count[x["id"]] += 1
            sec_total_count[x["id"]] += len(x["in_range"])

        get_sensing_resource(x["id"])
    


    # if time % 100 == 0:
    #     for x in vec_per:
    #         # print(x["id"] , ":" , x["select_time"] , "   " , end="")
    #     # print()
    
    vec_per = []                                     #釋放車輛資訊                  
    return error_count , total_count , re_error , sec_error_count , sec_total_count , counter_great , counter_total , counter_same_time ,counter_same_total , rc_counter , mode4_counter , len_rc_counter , out_len_counter , total_test , rc_error_c
    

def add_vec_info():
    global vec_per
    global sen_all_re
    for x in vec_all:
        vec_per.insert(int(x) , {
                                 "id" : int(x) ,
                                 "time" : int(float(vec_all[x][3])),
                                 "speed" : float(vec_all[x][0]),
                                 "xpos"  : float(vec_all[x][1]),
                                 "ypos"  : float(vec_all[x][2]),
                                 "in_range" : [],
                                 "sensing_resource" :sen_all_re[int(x)],
                                 "packet_resource" : [],
                                 "resource" : resource_list[int(x)],
                                 "tran_boo" : 0,
                                 "reselected_counter" : rc_ilst[int(x)],
                                 "inrange_dis" : {},
                                 "select_time" : select_time_list[int(x)],
                                 
                                })
def vec_in_range():
    for x in range(0 , len(vec_per)) :
        for y in range(0 , len(vec_per)):
            dis = hypot(vec_per[y]["xpos"] - vec_per[x]["xpos"] , vec_per[y]["ypos"] - vec_per[x]["ypos"])
            if 0< dis < 300 :
                vec_per[x]["in_range"].append(y)
                vec_per[x]["inrange_dis"][y] = dis


def get_resource(vec_id):
    global counter_total
    if vec_per[vec_id]["reselected_counter"] == 0 :
        counter_total += 1
        select_resource(vec_id)
        rc_ilst[vec_id] = random.randint(5,15)
    

def select_resource(vec_id):
    re_pool = []
    resource_list[vec_id] = -1
    global re_error
    for x in range(0,50):
        add_boo = 1
        for y in range(0,9):
            if x in vec_per[vec_id]["sensing_resource"][y]:
                add_boo = 0
        if add_boo == 1:
            re_pool.append(x)
    if len(re_pool) < 50 * 0.2:
        for x in range(ceil(50*0.2) - len(re_pool)):
            sort_temp = 0
            id_temp = -1
            for y in vec_per[vec_id]["inrange_dis"].keys():
                if vec_per[y]["resource"] not in re_pool: 
                    if vec_per[vec_id]["inrange_dis"][y] > sort_temp:
                        sort_temp = vec_per[vec_id]["inrange_dis"][y]
                        id_temp = y
            if id_temp != -1:
                re_pool.append(vec_per[id_temp]["resource"])
                del vec_per[vec_id]["inrange_dis"][id_temp]
    # print(re_pool)
     #rc方法的排除資源
    """
    for x in rm_sensing_list[vec_id]:
        # print(x)
        if x in re_pool:
            re_pool.remove(x)
    """
    #RC方法排除資源
    if len(re_pool) == 0:
        re_error += 1
    else:
        # print(re_pool)
        resource_list[vec_id] = random.choice(re_pool)


    
def get_packet_resource(vec_id):
    for x in vec_per[vec_id]["in_range"]:
        if vec_per[x]["tran_boo"] == 1:
            vec_per[vec_id]["packet_resource"].insert(x , vec_per[x]["resource"])

def get_sensing_resource(vec_id):
    global sen_all_re

    for x in vec_per[vec_id]["packet_resource"]:
        if (vec_per[vec_id]["time"])>1000 and (vec_per[vec_id]["time"]%100) ==0:
            sen_all_re[vec_id][(vec_per[vec_id]["time"]//100) % 10] = []

        if x not in sen_all_re[vec_id][(vec_per[vec_id]["time"]//100) % 10]:
            sen_all_re[vec_id][(vec_per[vec_id]["time"]//100) % 10].append(x)
        

