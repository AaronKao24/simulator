
vec_per = []
vec_all = {}
def main(vec , time):
    global vec_all
    global vec_per
    vec_all = vec
    add_vec_info()
    if time % 1000 == 0 :
        for x in vec_per:
            print(x["id"] ," : " , x["direction"])
    vec_per = [] 
    return 1

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
