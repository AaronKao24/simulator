#取得sumo模擬的數值及將xml轉檔


import os

def get_trace(file_name , cfg_file):
    os.system("sumo -c " + cfg_file + " --fcd-output " + file_name)
    #print("sumo -c " + cfg_file + " --fcd-output " + file_name)

def tran_trace(file_name , trace_file):
    os.system("python3 traceExporter.py --fcd-input " + trace_file + " --omnet-output " + file_name)