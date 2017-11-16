#!/usr/bin/python3
import bluepy
from bluepy import sensortag
from bluepy.btle import Scanner, DefaultDelegate
import time
import sys

# Generic Access Profile Data Type Value
COMPLETE_LOCAL_NAME = 0X09
CALI_OFFSET_SAMPLES=50
CALI_POS_SAMPLES=20 # number of samples collected at each position
CALI_MAG_POSITION=5
CALI_ITER=10 # number of iterations for calibration
CALI_FILE='Positions.txt'

class ScanDelegate(DefaultDelegate):
    def __init__(self):
        DefaultDelegate.__init__(self)

    def handleDiscovery(self, dev, isNewDev, isNewData):
        if isNewDev:
            print("Discover device", dev.addr)
        elif isNewData:
            print("Received new data from", dev.addr)

def main():
    scanner = Scanner().withDelegate(ScanDelegate())
    devices = scanner.scan(10.0)
   
    tags = []

    for dev in devices:
        completeLocalName = dev.getValueText(COMPLETE_LOCAL_NAME)
        if completeLocalName == "CC2650 SensorTag":
            print("Connecting to {0} {1} ({2}), RSSI={3} dB".format(completeLocalName, dev.addr, dev.addrType, dev.rssi))
            tags.append(sensortag.SensorTag(dev.addr))


    for i in range(0, len(tags)):
        tags[i].magnetometer.enable()

    time.sleep(3.0)
    endTime = time.time() + 10
    
    data = len(tags)*[[]]
    
    '''
    while time.time() < endTime:
        #for i in range(0, len(tags)):
        data.append(tags[0].magnetometer.read())
    '''
    print('Calculating Offsets...')
    pos_dict=cali_funcs.parse_input(CALI_FILE)
    pos_m=[]
    h=[]
    
    for i in range(CALI_MAG_POSITION):
        for p in range(CALI_POS_SAMPLES):
            pos_m.append(pos_dict['MagPos'+str(i)])
            h.append(pos_dict['MagOrien'+str(i)])
    #print(pos_m)  
    while i < CALI_OFFSET_SAMPLES:
        for index in range(len(tags)):
            #data[index].append(tags[index].magnetometer.read())
            data[index].append([20,20,20])
        i=i+1

    offsets=len(tags)*[[0,0,0]]
    for i in range(len(tags)):
        offsets[i]=cali_funcs.cali_offset(data[i])
    
    print('Calibrating...')
    data=[]
    for i in range(len(tags)):
        data.append([])
    for pos in range(CALI_MAG_POSITION):
        
        print('Place Mag at  position ',pos)
        tmp=input('Press Enter to continue')
        for index in range(len(tags)):
            for i in range(CALI_POS_SAMPLES):
                #data[index].append(tags[index].magnetometer.read())
                data[index].append([20+(index+i)*10,20+(index+i)*10,20+10*(index+i)])
    cali_para=[]
    #print(pos_m)
    for i in range(len(tags)):
        cali_para.append([])
        pos_l=pos_dict['Sensor'+str(i)].copy()
        cali_para[i]=cali_funcs.calibrateSensor(data[i],pos_m, h, pos_l,CALI_ITER, offsets[i]).copy()

    print('Calibration Finished')
    tmp=input('Press Enter to continue')
        
        
        
    '''
    print(len(data))
    for i in range(0, len(tags)):
        tags[i].disconnect()
    del tags[:]
    '''

if __name__ == "__main__":
    main()
