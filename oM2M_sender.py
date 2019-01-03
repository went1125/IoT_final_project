import serial
import time
import sys
import oM2M_requests as om2m

'''
data[0] is pm1.0
data[1] is pm2.5
data[2] is pm 10
data[3] is > 0.3um
data[4] is > 0.5um
data[5] is > 1um
data[6] is > 2.5um
data[7] is temperature
data[8] is humadity
data[9] is rpm
'''

port = "/dev/ttyACM0"

serialPort = serial.Serial(port, 9600, timeout=1)
time.sleep(5)
print('Starting reading arduino sensors....')

def isUnnormal(data):
    if len(data) < 10:
        return True
    
    elif min(data) < 0:
        return True
    
    elif sum(data) == 0 or data[1] > 100:
        return True
    
    return False

def stoi(x):
    return int(x)

def makeKeyValuePair(key, value):
    return '"' + key + '"' + ':"' + value + '"'

def encodeToJson(data):
    result = '{'
    result = result + makeKeyValuePair('pm1', data[0]) + ','  
    result = result + makeKeyValuePair('pm2.5', data[1]) + ','
    result = result + makeKeyValuePair('pm10', data[2]) + ','
    result = result + makeKeyValuePair('0.3um', data[3]) + ','
    result = result + makeKeyValuePair('0.5um', data[4]) + ','
    result = result + makeKeyValuePair('1um', data[5]) + ','
    result = result + makeKeyValuePair('2.5um', data[6]) + ','
    result = result + makeKeyValuePair('temperature', data[7]) + ','
    result = result + makeKeyValuePair('humidaty', data[8]) + ','
    result = result + makeKeyValuePair('rpm', data[9]) + '}'
    return result

while True:
    serialData = serialPort.readline().decode()
    stringData = serialData.split()
    intData = list(map(stoi, stringData))

    if not isUnnormal(intData):
        jsonData = encodeToJson(stringData)
        print(jsonData)
        om2m.createContainerInstance(jsonData, sys.argv[1], sys.argv[2])
    
    time.sleep(1)
    
serialPort.close()



