
import random
import collision_judge as cj
from math import ceil

global total_resource
total_resource = 50

def main(vec_info , time , error_data):
    
    vec_per = vec_info
    error_count = error_data[0]
    sec_error_count = error_data[1]
    total_count = error_data[2]
    sec_total_count = error_data[3]
    

    for vec in vec_per:
        if time % 100 ==0:
            get_resource(vec)
        if (vec["resource"] // (total_resource/100)) == (time%100):
            vec["tran_boo"] = 1
            vec["reselected_counter"] = vec["reselected_counter"] -1
    
    for vec in vec_per:
        get_packet_resource(vec , vec_per)
        get_sensing_resource(vec , time)
        

    for vec in vec_per:
        error_boo = 0
        error_boo_tra = 0
        if vec["tran_boo"] == 1:
            for y in vec["in_range"]:
                ###傳輸有錯率###
                error_boo = cj.error_main(vec_per[y]["packet_resource"] , vec["resource"])
                if error_boo == 1:
                    sec_error_count[vec["id"]] += 1
                    if error_boo_tra ==0:
                        error_boo_tra = 1
                    
            if error_boo_tra == 1:
                error_count[vec["id"]] += 1

            total_count[vec["id"]] += 1
            sec_total_count[vec["id"]] += len(vec["in_range"])
            # print(error_count[vec["id"]] ,total_count[vec["id"]] )
    error_list = [error_count , total_count, sec_error_count , sec_total_count]
    return error_list , vec_per
def get_resource(vec):
    if vec["reselected_counter"] == 0:
        if vec["status"] == "normal":
            select_resource(vec)
        else:
            select_special_resource(vec)
        vec["reselected_counter"] = random.randint(5,15)
def select_special_resource(vec):
    pool = list()
    for i in range(vec["resource_pool"][0] , vec["resource_pool"][1]+1):
        pool.append(i)
    # print(pool)
    # print( vec["status"], vec["position"],vec["ave_speed"], vec["history_ave_speed"] , vec["number_same_direction"] , vec["higher_ave"])
    vec["resource"] = random.choice(pool)
    # print(vec["resource"])
def select_resource(vec):
    pool = list()
    resource_enough = []

    print(range(vec["resource_pool"][0] , vec["resource_pool"][1]))
    for x in range(vec["resource_pool"][0] , vec["resource_pool"][1]):
        add_boo = 1
        for i in range(0,10):
            if x in vec["sensing_resource"][i]:
                add_boo = 0
        if add_boo == 1:
            pool.append(x)
    if len(pool) < total_resource * 0.2:    #資源少於全部20%  增加到20%
            
        for i in range(total_resource):
            if i not in pool:
                if len(resource_enough) < ceil(total_resource*0.2) - len(pool):
                    resource_enough.append(i)
                elif len(resource_enough) > ceil(total_resource*0.2) - len(pool):
                    for j in resource_enough:
                        if vec_per[id]["resource_dis"][j] < vec_per[id]["resource_dis"][i]:
                            
                            resource_enough.remove(j)
                            resource_enough.append(i)
                            break
        
        for i in resource_enough:
            pool.append(i)
    vec["resource"] = random.choice(pool)

def get_packet_resource(vec , vec_per):
    for x in vec["in_range"]:
        if vec_per[x]["tran_boo"] == 1:
            vec["packet_resource"].insert(x , vec_per[x]["resource"])

def get_sensing_resource(vec , time):

    for x in vec["packet_resource"]:
        if (vec["time"])>1000 and (vec["time"]%100) ==0:
            vec["sensing_resource"][(vec["time"]//100) % 10] = []

        if x not in vec["sensing_resource"][(vec["time"]//100) % 10]:
            vec["sensing_resource"][(vec["time"]//100) % 10].append(x)

    