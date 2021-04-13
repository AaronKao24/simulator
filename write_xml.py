import math
import os

node_num = int(60)


def write_node(file_name):
    f = open(file_name , mode = "w")


    f.write("<nodes>\n")
    for x in range(1,node_num+1):
        f.write("<node id=\"" + str(x) + "\" x=\"" + str(2000*math.cos((x*6) * math.pi /180)) + "\" y=\"" + str(2000*math.sin((x*6) * math.pi / 180)) +"\" />\n")
    f.write("</nodes>\n")

    f.close()

def write_edge(file_name):
    f = open(file_name , mode = "w")
    f.write("<edges>\n")
    f.write("<edge id = \"P0\" from = \"60\" to = \"1\" type = \"a\" /> \n")
    f.write("<edge id = \"N0\" from = \"1\" to = \"60\" type = \"a\" /> \n")
    for x in range(1,node_num):
        f.write("<edge id = \"P" + str(x) + "\" from = \"" + str(x) +"\" to = \"" + str(x+1) + "\" type = \"a\" /> \n")
        f.write("<edge id = \"N" + str(x) + "\" from = \"" + str(node_num+1-x) +"\" to = \"" + str(node_num-x) + "\" type = \"a\" /> \n")
    f.write("</edges>\n")

    f.close()

def write_connection(file_name):
    f = open(file_name , mode = "w")
    f.write("<connections>\n")
    for x in range(0,node_num-1):
        for y in range(0,3):
            f.write("<connection from = \"P" + str(x) + "\" to = \"P" + str(x+1) + "\" fromLane = \"" + str(y) + "\" toLane = \"" + str(y) + "\"/> \n")
            f.write("<connection from = \"N" + str(x) + "\" to = \"N" + str(x+1) + "\" fromLane = \"" + str(y) + "\" toLane = \"" + str(y) + "\"/> \n")
    f.write("</connections>\n")

    f.close()
def write_type(file_name):
    f = open(file_name , mode = "w")
    f.write("<types>\n")
    f.write("   <type id=\"a\" priority=\"3\" numLanes=\"3\" speed=\"33\"/>\n")
    f.write("</types>\n")

    f.close()

def write_netc(file_name , node_file , edge_file , con_file , type_file , output_name):
    f = open(file_name , mode = "w")
    f.write("<configuration>\n")
    f.write("   <input>\n")
    f.write("       <edge-files value=\"" + edge_file + "\"/>\n")
    f.write("       <node-files value=\"" + node_file + "\"/>\n")
    f.write("       <type-files value=\"" + type_file + "\"/>\n")
    f.write("       <connection-files value=\"" + con_file + "\"/>\n")
    f.write("   </input>\n")
    f.write("   <output>\n")
    f.write("       <output-file value=\"" + output_name + "\"/>\n")
    f.write("   </output>\n")
    f.write("   <processing>\n")
    f.write("       <no-turnarounds value=\"true\"/>\n")
    f.write("   </processing>\n")
    f.write("</configuration>\n")

    f.close()

def exc_netc(netc_file):
    os.system("netconvert -c " + netc_file)
    


def write_route(file_name):
    y = 0.1
    f = open(file_name , mode = "w")
    f.write("<routes>\n")
    f.write("<vType accel=\"3.0\" decel=\"6.0\" id=\"CarA\" length=\"5.0\" minGap=\"2.5\" maxSpeed=\"33.333\" sigma=\"1\" departSpeed=\"25\" />\n")
    f.write("<route id = \"route0\" edges = \"")
    for x in range(0,node_num):
        f.write("P" + str(x) + " ")
    f.write("\" />\n")
    f.write("<route id = \"route1\" edges = \"")
    for x in range(0,node_num):
        f.write("N" + str(x) + " ")
    f.write("\" />\n")
    for x in range(0,node_num):
        f.write("<vehicle departLane=\"free\" depart=\"" + str(y) + "\" id = \"veh" + str(x) + "\" route = \"route0\" type = \"CarA\" />\n")
        f.write("<vehicle departLane=\"free\" depart=\"" + str(y) + "\" id = \"veh" + str(x+node_num) + "\" route = \"route1\" type = \"CarA\" />\n")
        y =y + 0.5
    # f.write("<vehicle depart=\"10\" id = \"veh0\" route = \"route0\" type = \"CarA\" />\n")
    # f.write("<vehicle depart=\"10\" id = \"veh1\" route = \"route1\" type = \"CarA\" />\n")
    f.write("</routes>\n")

    f.close()

def write_cfg(file_name , net_file , rou_file , begin_time , end_time):
    f = open(file_name , mode = "w")
    f.write("<configuration>\n")
    f.write("   <input>\n")
    f.write("       <net-file value=\"" + net_file + "\"/>\n")
    f.write("       <route-files value=\"" + rou_file + "\"/>\n")
    f.write("   </input>\n")
    f.write("   <time>\n")
    f.write("       <step-length value = \"0.001\" />\n")
    f.write("       <begin value = \"" + str(begin_time) +"\"/>\n")
    f.write("       <end value = \"" + str(end_time) +"\"/>\n")
    f.write("   </time>\n")
    f.write("</configuration>\n")
"""
write_node("test.nod.xml")
write_edge("test.edg.xml")
write_connection("test.con.xml")
write_route("test.rou.xml")
"""