





import get_trace as g
import delete_illegal_xml as delxml
import get_data
import write_xml as wx
import mode4_sps as sps
import two_hop_method as thm
import cut_file
from xml.etree import ElementTree as ET
import parameter




# write xml file


"""
wx.write_node("simulation.nod.xml")
wx.write_edge("simulation.edg.xml")
wx.write_connection("simulation.con.xml")
wx.write_type("simulation.typ.xml")
wx.write_netc("simulation.netccfg" , "simulation.nod.xml" , "simulation.edg.xml" , "simulation.con.xml" , "simulation.typ.xml" , "simulation.net.xml")
wx.write_route("simulation.rou.xml")
wx.exc_netc("simulation.netccfg")
wx.write_cfg("simulation.sumocfg" , "simulation.net.xml" , "simulation.rou.xml" , 0 , 600)



# write xml file 

g.get_trace("simulation_trace.xml" , "simulation.sumocfg")
print("get trace : OK")
g.tran_trace("simulation_final_trace.xml" , "simulation_trace.xml")
print("get final : OK")
delxml.delete_xml("simulation_final_trace.xml")
print("del error : OK")
cut_file.Main()


for x in range(1,4962):
    get_data.set_time("split/"+str(x)+".xml")
print("set time : OK")


"""
# dom = get_data.get_data("split/1.xml")

vec = {}

####test####
# c = dom.findall('waypoint')







"""
for x in c:
        nodeid = x.find('nodeid').text
        time = x.find('time').text
        speed = x.find('speed').text
        print(' * {} [{}] {}'.format(
            nodeid,time,speed
        ))

"""

###simulation###

time = int(0)
test = 0
end_time = int(100000)
result = []
error_count = []
total_count = []
sec_error_count = []
sec_total_count = []
re_error = 0
all_error = 0
all_total = 0
all_sec_error = 0
all_sec_total = 0
all_percent = 0
temp_error = [0]*(parameter.vec_num*2)
temp_total = [0]*(parameter.vec_num*2)
sec_temp_error = [0]*(parameter.vec_num*2)
sec_temp_total = [0]*(parameter.vec_num*2)
end_time = 0

for file_count in range(1,4962):

    dom = get_data.get_data("split/"+str(file_count)+".xml")
    c = dom.findall('waypoint')

    realtime = dom.findall('waypoint/time')
    end_time_list = dom.findall('destroy/time')
    if len(end_time_list):
        break                           #判斷是否有車輛結束，有的話跳出迴圈
    while time <= int(realtime[-1].text):
        
##########################mode 4################################### 
        """
        for x in c:
            if  int(x.find('time').text)== time:
                vec[x.find('nodeid').text] = x.find('speed').text , x.find('destination/xpos').text , x.find('destination/ypos').text , x.find('time').text
                 
        result =  sps.mode_main(vec , time)

        # print(time , x.find('time').text)
        test += 1
        re_error = re_error + result[2]
        # if time % 1000 == 0:
        #     print(time,"  :  OK")
        if time % 10000 ==0:
            te=0
            tt=0
            ste=0
            stt=0
            for x in range(parameter.vec_num*2):
                te = te + (result[0][x] - temp_error[x])
                tt = tt + (result[1][x] - temp_total[x])
                ste = ste + (result[3][x] - sec_temp_error[x])
                stt = stt + (result[4][x] - sec_temp_total[x])
                temp_error[x] = result[0][x]
                temp_total[x] = result[1][x]
                sec_temp_error[x] = result[3][x]
                sec_temp_total[x] = result[4][x]
                
            if tt !=0:
                print('te: {} tt: {}\nste: {}  stt:{}'.format(te,tt,ste,stt))
                print('{} error percent : {:.3f}%'.format(time , float(te)*100/float(tt)))
                print('{} second error percent : {:.3f}%'.format(time , float(ste)*100/float(stt)))
                print(time,"'s greater 3 counter : ",result[5])

        time = time + 1 
# print(result[1])

#######最後一波檢測#########
te=0
tt=0
for x in range(parameter.vec_num*2):
    te = te + (result[0][x] - temp_error[x])
    tt = tt + (result[1][x] - temp_total[x])
    temp_error[x] = result[0][x]
    temp_total[x] = result[1][x]
if tt != 0:
    print('{} error percent : {:.3f}%'.format(time , float(te)*100/float(tt)))
######最後一波檢測#########

error_count = result[0]
total_count = result[1]
sec_error_count = result[3]
sec_total_count = result[4]
print("total compute : " , test)
for x in range(parameter.vec_num*2):
    all_error = all_error + error_count[x]
    all_total = all_total + total_count[x]
    all_sec_error += sec_error_count[x]
    all_sec_total += sec_total_count[x]
    if total_count[x]>0:
        print('{} : {:.3f}%'.format(x , float(error_count[x])*100 / float(total_count[x])))
print('total error percent : {:.3f}%'.format(float(all_error)*100/float(all_total)))
print('total error percent : {:.3f}%'.format(float(all_sec_error)*100/float(all_sec_total)))
print(time,"'s RC counter : ",result[5])
print("total selected counter : " , result[6])
print("total error / total " , all_sec_error ," / ", all_sec_total)
print("total same time counter : " , result[7])
print("total same time : " , result[8])
print("same rate : " , float(result[7])*100/float(result[8]))

print("rc total : " , result[9] , "; mode 4 : " , result[10] , " ; out len counter : " , result[12])
print("len counter : " , result[11])
print("total selected counter : " , result[13])

print("RC方法有相同資源的問題 : " , result[14])
#print(vec)
"""
##########################mode 4###################################

##########################two hop###################################

        for x in c:
            if  int(x.find('time').text)== time:
                vec[x.find('nodeid').text] = x.find('speed').text , x.find('destination/xpos').text , x.find('destination/ypos').text , x.find('time').text
                 
        result =  thm.main(vec , time)
        time = time + 1 

##########################two hop###################################

###simulation###

