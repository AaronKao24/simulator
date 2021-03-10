

from xml.etree import ElementTree
import os

def get_data(final_trace_file):
    full_file = os.path.abspath(os.path.join(final_trace_file))
    global dom
    dom = ElementTree.parse(full_file)

    return dom

def out_data():
    c = dom.findall('waypoint')

    for x in c:
        nodeid = x.find('nodeid').text
        time = x.find('time').text
        speed = x.find('speed').text

        print(' * {} [{}] {}'.format(
            nodeid,time,speed
        ))

def set_time(file_name):
    updateTree = ElementTree.parse(file_name)   
    root = updateTree.getroot()
    time = root.findall('waypoint/time')
    end_time = root.findall('destroy/time')

    for x in time:
        x.text = str(int(float(x.text)*1000))
    for y in end_time:
        y.text = str(int(float(x.text)*1000))

    updateTree.write(file_name)     