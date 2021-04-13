import xml.etree.ElementTree as ET

def changetext(a , b , final_trace_file):
    with open(final_trace_file,'r') as f:
        lines=[] 
        for line in f.readlines():
            if line!='\n':
                lines.append(line)
        f.close()
    with open(final_trace_file,'w') as f:
        for line in lines:
            if a in line:
                line = b 
                f.write('%s\n' %line)
            else:
                f.write('%s' %line) 

def delete_xml(final_trace_file):
    changetext('<xmlns:xsi="http://www.w3.org/2001/XMLSchema-instance" xsi:noNamespaceSchemaLocation="mobility_trace.xsd">' , '' , final_trace_file)



