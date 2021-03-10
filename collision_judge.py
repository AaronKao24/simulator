
def error_main(resource_list , resource):
    error_judge = 0
    error_boo = 0
    for x in range(0 , len(resource_list)):
        if resource_list[x] == resource:
            error_judge += 1
            

    if error_judge >=2:
        error_boo = 1


    return error_boo 