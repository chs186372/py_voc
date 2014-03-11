import math
import numpy as np

def resize1dtran(pic,s_height,d_height,s_width,s_chan,flag):
    scale = d_height*1.0/s_height
    invscale = s_height*1.0/d_height
    length = int(math.ceil(d_height*invscale)+2*d_height)
    ofs=range(length)
    k=0
    for dy in range(d_height):
        fsy1 = dy * invscale
        fsy2 = fsy1 + invscale
        sy1 = int(math.ceil(fsy1))
        sy2 = int(math.floor(fsy2))
        if sy1-fsy1 >1e-3:
            ofs[k]={}
            ofs[k]["di"]=dy
            ofs[k]["si"]=sy1-1
            ofs[k]["alpha"]=(sy1 - fsy1) * scale
            k+=1

        for sy in range(sy1,sy2):
            #if k==125:
              #  print dy,sy,d_height
            ofs[k]={}
            ofs[k]["di"]=dy
            ofs[k]["si"]=sy
            ofs[k]["alpha"]=scale
            k+=1

        if fsy2-sy2>1e-3:
            ofs[k]={}
            ofs[k]["di"]=dy
            ofs[k]["si"]=sy2
            ofs[k]["alpha"]=(fsy2 - sy2)*scale
            k+=1
    if flag:
        dst = np.zeros((s_chan,d_height,s_width))
    else:
        dst = np.zeros((s_chan,s_width,d_height))
    for c in range(s_chan):
        for x in range(s_width):
            for ind in range(k):
               # if ofs[ind]["di"]==80:
                #    print c,x,ofs[k-1]["di"],ofs[k-1]["si"],dst.shape
                if flag:
                    dst[c][ofs[ind]["di"]][x] += ofs[ind]["alpha"]*pic[c][ofs[ind]["si"]][x]
                else:
                    dst[c][x][ofs[ind]["di"]] += ofs[ind]["alpha"]*pic[c][x][ofs[ind]["si"]]
    return dst

def resize(pic,scale):
    (s_chan,s_height,s_width)=pic.shape
    d_height = int(round(s_height*scale))
    d_width = int(round(s_width*scale))
    #print (s_height,s_width),(d_height,d_width)
    tmp = resize1dtran(pic,s_height,d_height,s_width,s_chan,True)
    result = resize1dtran(tmp,s_width,d_width,d_height,s_chan,False)
    return result
