import os
from xml.dom import minidom

from utp.getConfig import getConfig

def checkSuccess():
    config = getConfig()
    
    output = os.path.join(os.getcwd(), config.get("artifactsDir") ,'output.xml')
    
    if os.path.exists(output) == False :
        return False
    
    file = minidom.parse(output)

    #use getElementsByTagName() to get tag
    statistics = file.getElementsByTagName('statistics')
    total = statistics[0].getElementsByTagName('total')
    stats = total[0].getElementsByTagName('stat')

    fails = 0
    passes = 0
    for stat in stats:
        fails += int(stat.getAttribute('fail'))
        passes += int(stat.getAttribute('pass'))
        
    print("fails: ", fails)
    print("passes: ", passes)
    return fails == 0 and passes > 0
        