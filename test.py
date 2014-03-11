import Image
import numpy as np
import scipy.io as sio

def getFile():
    matfn=u'D:/voc-release4.01/models/car_card_final.mat'
    model=sio.loadmat(matfn)
    filename=r'D:\voc-release4.01\target\solo\1.jpg'
    img = Image.open(filename)
    img.load()
    img.load()
    r,g,b = img.split()
    r=np.array(r,dtype='int32')
    g=np.array(g,dtype='int32')
    b=np.array(b,dtype='int32')
    mtr =np.array([r,g,b])
    return (mtr,model["model"])