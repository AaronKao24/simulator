from math import hypot
import parameter
import random
import copy

def rc_method(rc_method_list):
    temp_re_list = []
    temp_re_list1 = []
    be_choiced_list = {}
    vec_choice = {}
    temp_resource_dict = {}
    counter = 1
    # print(rc_method_list)
    # print(type(rc_method_list[1]["in_range"][0]))
    # print(rc_method_list[1]["in_range"])
    
    for x in rc_method_list:
        temp_resource_dict[str(x["id"])] = x["resource"]
    if len(rc_method_list) == 2:
        if rc_method_list[1]["id"] in rc_method_list[0]["in_range"]:
            temp_re_list.insert(rc_method_list[0]["id"] , {
                                                            "id" : rc_method_list[0]["id"] , 
                                                            "resource" : rc_method_list[1]["resource"],
                                                            })
            temp_re_list.insert(rc_method_list[1]["id"] , {
                                                            "id" : rc_method_list[1]["id"] , 
                                                            "resource" : rc_method_list[0]["resource"],
                                                            })

    if len(rc_method_list) > 2:
        temp_rc_list =[]
        temp_rc_list = copy.deepcopy(rc_method_list)
        for x in temp_rc_list:
            vec_choice[str(x["id"])] = get_choice(x["in_range"] ,x["xpos"] , x["ypos"], temp_rc_list)

        temp_rc_list = copy.deepcopy(rc_method_list)
        for x in temp_rc_list:
            be_choiced_list[str(x["id"])] = get_be_choiced(vec_choice , x["xpos"] , x["ypos"] , temp_rc_list , x["id"])

        temp_rc_list = copy.deepcopy(rc_method_list)
        temp_re_list1 = get_fianl_list(vec_choice , be_choiced_list ,temp_rc_list)

        # print(temp_re_list1)
        for x in temp_re_list1:
            if x["select_re"] != -1:
                temp_re_list.insert(x["id"] , {
                                                    "id" : x["id"] ,
                                                    "resource" : temp_resource_dict[str(x["select_re"])]
                                                    })
        
    # print("re_list:    " , temp_re_list)
    return temp_re_list , counter

def get_choice(temp_in_range , xpos , ypos , temp_rc_list):
    choice_list = []
    parameter.para()
    for y in range(0,(parameter.rc_small//2)):
        max = 0   
        max_id = -1                         #rssi 用距離取代 
        for x in temp_rc_list:                                      
            if x["id"] in temp_in_range:
                if max < hypot(xpos - x["xpos"] , ypos - x["ypos"]):
                    max = hypot(xpos - x["xpos"] , ypos - x["ypos"])
                    max_id = x["id"]
        if max_id != -1:
            temp_in_range.remove(max_id)
            choice_list.append(max_id)
    return choice_list
def get_be_choiced(choice_list , xpos , ypos , temp_rc_list , id):
    parameter.para()
    be_counter = 0
    temp_be_list = []
    temp_be_list_final = []
    
    for i in range(parameter.rc_small//2):
        for x in temp_rc_list:
            if len(choice_list[str(x["id"])]) > be_counter:
                if choice_list[str(x["id"])][be_counter] == id:
                    temp_be_list.append(x["id"]) 
            
        be_counter += 1
    for i in range(0,(parameter.rc_small//2)):
        temp_vec = -1
        max_rssi = 0
        if len(temp_be_list) >0 :
            for x in temp_be_list:
                if len(choice_list[str(x)]) == 1:
                    temp_vec = x
                    break
                else:
                    for y in temp_rc_list:
                        if y["id"] == x:
                            if max_rssi < hypot(xpos - y["xpos"] , ypos - y["ypos"]):
                                temp_vec = x
                                max_rssi = hypot(xpos - y["xpos"] , ypos - y["ypos"])
            temp_be_list_final.append(temp_vec)
            temp_be_list.remove(temp_vec)

    return temp_be_list_final

def get_fianl_list(vec_choice , be_choiced_list , temp_rc_list):
    # print("vec_choice : " , vec_choice)
    # print("be_list : " , be_choiced_list)
    select_re_list = []
    same_list = []
    temp_already = []
    for x in temp_rc_list:
        select_re_list.append({
            "id" : x["id"],
            "select_re" : -1,
        })
        same_list.append({
            "id" : x["id"],
            "be_counter" : 0,
        })
    for i in range(parameter.rc_small//2):
        for x in same_list:
            x["be_counter"] = 0
        for x in temp_rc_list:
            for y in select_re_list:
                if x["id"] == y["id"]:
                    if len(vec_choice[str(x["id"])])>i:
                        if y["select_re"] == -1 and vec_choice[str(x["id"])][i] not in temp_already:
                            y["select_re"] = vec_choice[str(x["id"])][i]
                            for z in same_list:
                                if z["id"] == vec_choice[str(x["id"])][i]:
                                    z["be_counter"]+=1
        for x in same_list:
            if x["be_counter"] >1:
                for y in select_re_list:
                    if y["select_re"] == x["id"]:
                        if y["id"] != be_choiced_list[str(x["id"])][i]:
                            y["select_re"] = -1
        for x in select_re_list:
            if x["select_re"] != -1:
                temp_already.append(x["id"])
    # print("final list : " , select_re_list)    
    
    return select_re_list
