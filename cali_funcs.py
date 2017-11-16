'''
Functions used for calibration purpose
'''
import math
import scipy
import numpy


def get_b(p, h, ps): #position vector p, orientation h, location sensor ps
    const=1 # ur u0 Mt /4pi
    #print(p,h,pl)
    #print(len(p),len(h),len(pl))
    tmp_p=numpy.array(p)
    tmp_h=numpy.array(h)
    tmp_ps=numpy.array(ps)
    pl=tmp_ps-tmp_p
    rl=numpy.linalg.norm(pl)
    b=[0,0,0]
    #if rl==0:
        #return b
    b=const*(3*numpy.dot(h,pl)*pl/(rl**5)-tmp_h/(rl**3))
    return b

def get_all_b(arr_p, arr_h, ps): #arr_p arr_h have n*3 elements
    n=len(arr_p)
    arr_b=n*[[0,0,0]]
    for i in range(n):
        arr_b[i]=get_b(arr_p[i],arr_h[i],ps)
    return arr_b
        

def cali_offset(data): #data: n*3 array
    offsets = [0, 0, 0]
    sumx = 0
    sumy = 0
    sumz = 0
    for sample in data:
        sumx = sumx + sample[0]
        sumy = sumy + sample[1]
        sumz = sumz + sample[2]
    offsets[0] = sumx / len(data)
    offsets[1] = sumy / len(data)
    offsets[2] = sumz / len(data)
    return offsets


def cali_k(data, b_th): # data, b_th n*3 array
    sumx = 0
    sumy = 0
    sumz = 0
    sumb = [0, 0, 0]
    
    for index in range(len(data)):            
        sumx = sumx + data[index][0] * b_th[index][0]
        sumy = sumy + data[index][1] * b_th[index][1]
        sumz = sumz + data[index][2] * b_th[index][2]
        sumb[0] = sumb[0] + b_th[index][0] * b_th[index][0]
        sumb[1] = sumb[1] + b_th[index][1] * b_th[index][1]
        sumb[2] = sumb[2] + b_th[index][2] * b_th[index][2];

    kx = sumx / sumb[0]
    ky = sumy / sumb[1]
    kz = sumz / sumb[2]
    print(sumx, sumy, sumz)
    return [kx, ky, kz]

def cali_P(v, pos_m, h, pos_l, k, M):
    return [0,0,0]

def cali_RM(b,v,k): # B,V n*3, k 1*3
    B1=numpy.transpose(b)
    B2=v
    for row in B2:
        row[0] = row[0] / k[0]
        row[1] = row[1] / k[1]
        row[2] = row[2] / k[2]
    B=numpy.matmul(B1,B2)
    V=numpy.linalg.inv(numpy.matmul(numpy.transpose(B2),B2))
    return numpy.matmul(B,V)

def calibrateSensor(data, pos_m, h, pos_l,iterations,offsets):
    '''
    calibrate a single sensor, i.e. pos_l is a vector
    pos_m=n*3[x,y,z], location of magnet
    h=n*3[m,n,p], orientation of mag
    pos_l=[xl,yl,zl], location of the sensor of interest
    data n*3
    '''
    n=len(data)
    k=[1,1,1]
    M=[[1,0,0],[0,1,0],[0,0,1]]
    #offsets=len(data)*[cali_offset(data)]
    new_data=numpy.array(data)-offsets
    #print('offsets: ',offsets, '\nnew data: ', new_data)
    count=0;
    while(count<iterations):
        arr_b_th=get_all_b(pos_m, h, pos_l)
        arr_b_th2=arr_b_th.copy()
        #print('arr_b_th',arr_b_th)
        #print('arr_b_th2',arr_b_th2)
        for i in range(0,n):
            arr_b_th2[i]=numpy.matmul(numpy.linalg.inv(M),arr_b_th[i])
        
        #print('arr_b_th2',arr_b_th2)
        k=cali_k(new_data, arr_b_th2)
        pos_l=cali_P(new_data, pos_m, h, pos_l, k, M) #updata pos_l
        arr_b_th=get_all_b(pos_m, h, pos_l) #update Bx,y,z
        print('K: ',k)
        M=cali_RM(arr_b_th,new_data,k)
        count=count+1
        #print('K: ',k)
    return [k,pos_l,M]

def parse_input(file_name):
    file=open(file_name,'r')
    pos_dict={}
    for line in file:
        (key, val_txt)=line.split(':')
        tmp=val_txt.split()
        tmp2=tmp[0]
        val_txt2=tmp2.split(',')
        val=[0,0,0]
        for i in range(len(val)):
            val[i]=float(val_txt2[i])
        pos_dict[key]=val;
    return pos_dict

def cali_main():
    data=[[10,20,30],[10,30,40],[10,40,30],[10,40,20]]
    pos_m=4*[[2,2,2]]
    h=4*[[0,0,1]]
    pos_l=[5,5,0]
    calibrateSensor(data, pos_l, h, pos_l,len(data),[0,0,0])

if __name__=='__main__':
    cali_main()


