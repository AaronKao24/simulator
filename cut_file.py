
from datetime import datetime
 
def Main():
    source_dir = 'simulation_final_trace.xml'
    target_dir = 'split/'
 
    
    flag = 0
 
    
    name = 1
 
    
    dataList = []
 
    print("start")
    print(datetime.now().strftime('%Y-%m-%d %H:%M:%S'))
 
    with open(source_dir,'r') as f_source:
        for line in f_source:
          flag+=1
          dataList.append(line)
          if flag == 10000:
              with open(target_dir + str(name)+".xml",'w+') as f_target:
                  if name > 1 :
                      f_target.write("<mobility_trace>")
                  for data in dataList:
                      f_target.write(data)
                  f_target.write("</mobility_trace>")
              name+=1
              flag = 0
              dataList = []
                
    with open(target_dir +str(name)+".xml",'w+') as f_target:
        f_target.write("<mobility_trace>")
        for data in dataList:
            f_target.write(data)
 
    print("finish")
    print(datetime.now().strftime('%Y-%m-%d %H:%M:%S'))
 
if __name__ == "__main__":
    Main()
