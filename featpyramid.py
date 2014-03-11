import math
import scipy as sp
import numpy as np
import features
import resize
import datetime


def featpyramid(pic,model):
    #?????
    pyra = {}
    padx = math.ceil(model["maxsize"][0][0][0][1])
    pady = math.ceil(model["maxsize"][0][0][0][0])
    sbin = model["sbin"][0][0][0][0]
    interval = model["interval"][0][0][0][0]
    sc = 2.0 **(1.0/interval)
    imsize = [pic.shape[1],pic.shape[2]]
    max_scale = int(1 + np.floor(math.log(min(imsize)/(5.0*sbin))/math.log(sc)))
    pyra["feat"] = list(range(int(max_scale + interval)))
    pyra["scales"] = np.zeros((max_scale + interval, 1))
    pyra["imsize"] = imsize
    time = 0
    for i in range(interval):
        starttime = datetime.datetime.now()
        scaled = resize.resize(pic,1.0/sc**i)
        endtime = datetime.datetime.now()
        tmp = features.features(scaled,sbin/2.0)
        time += (endtime - starttime).seconds
        size =[tmp.shape[0],tmp.shape[1]+2*pady+2,tmp.shape[2]+2*padx+2]
        pyra["feat"][i]=np.zeros(size)
        pyra["feat"][i][:,pady+1:size[1]-pady-1,padx+1:size[2]-padx-1] = tmp
        pyra["scales"][i] = 2.0/sc**(i)
        #starttime = datetime.datetime.now()
        tmp = features.features(scaled,sbin)
        #endtime = datetime.datetime.now()
        #time += (endtime - starttime).seconds
        size =[tmp.shape[0],tmp.shape[1]+2*pady+2,tmp.shape[2]+2*padx+2]
        pyra["feat"][i+interval]=np.zeros(size)
        pyra["feat"][i+interval][:,pady+1:size[1]-pady-1,padx+1:size[2]-padx-1] = tmp
        pyra["scales"][i+interval] = 1.0/sc**(i-1)
        for j in range(i+interval,max_scale,interval):
            starttime = datetime.datetime.now()
            scaled = resize.resize(scaled, 0.5)
            endtime = datetime.datetime.now()
            tmp = features.features(scaled,sbin)
            time += (endtime - starttime).seconds
            size =[tmp.shape[0],tmp.shape[1]+2*pady+2,tmp.shape[2]+2*padx+2]
            pyra["feat"][j+interval]=np.zeros(size)
            pyra["feat"][j+interval][:,pady+1:size[1]-pady-1,padx+1:size[2]-padx-1] = tmp
            pyra["scales"][j+interval] = 0.5/sc**(i-1)
    for i in range(len(pyra["feat"])):
        pyra["feat"][i][31,0:pady+1,:]=1
        end=pyra["feat"][i].shape
        pyra["feat"][i][31,end[1]-padx-1:end[1],:]=1
        pyra["feat"][i][31,:,0:padx+1]=1
        pyra["feat"][i][31,:,end[2]-pady-1:end[2]]=1

    print time
    pyra["padx"] = padx
    pyra["pady"] = pady
    return pyra
