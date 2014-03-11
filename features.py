import math
import numpy as np

def features(scale,sbin):
    eps = 0.0001
    uu = [1.0000,0.9397,0.7660,0.500,0.1736,-0.1736,-0.5000,-0.7660,-0.9397]
    vv = [0.0000,0.3420,0.6428,0.8660,0.9848,0.9848,0.8660,0.6428,0.3420]
    dims = scale.shape
    blocks = [int(round(dims[1]*1.0/sbin)),int(round(dims[2]*1.0/sbin))]
    out = [1+4+27,max(blocks[0]-2,0),max(blocks[1]-2,0)]
    visible = [blocks[0]*sbin,blocks[1]*sbin]
    hist = np.zeros((18,blocks[0],blocks[1]))
    norm = np.zeros((blocks[0],blocks[1]))
    feat = np.zeros(out)
    for x in range(1,int(visible[1]-1)):
        for y in range(1,int(visible[0]-1)):
            sx = min(x, dims[2]-2)
            sy = min(y, dims[1]-2)
            dy1 = scale[0][sy+1][sx] - scale[0][sy-1][sx]
            dx1 = scale[0][sy][sx+1] - scale[0][sy][sx-1]
            v1 = 0.0
            v1 = dy1*dy1+dx1*dx1
            dy2 = scale[1][sy+1][sx] - scale[1][sy-1][sx]
            dx2 = scale[1][sy][sx+1] - scale[1][sy][sx-1]
            v2 = 0.0
            v2 = dy2*dy2+dx2*dx2

            dy3 = scale[2][sy+1][sx] - scale[2][sy-1][sx]
            dx3 = scale[2][sy][sx+1] - scale[2][sy][sx-1]
            v3 = 0.0
            v3 = dy3*dy3+dx3*dx3


            if v3>v1:
                v1 = v3
                dy1 = dy3
                dx1 = dx3
            if v2>v1:
                v1 = v2
                dy1 = dy2
                dx1 = dx2

            best_dot = 0
            best_o = 0
            for o in range(9):
                dot = uu[o]*dx1+vv[o]*dy1
                if dot>best_dot:
                    best_dot = dot
                    best_o = o
                elif -dot>best_dot:
                    best_dot =-dot
                    best_o = o+9



            xp = (x+0.5)/sbin - 0.5
            yp = (y+0.5)/sbin - 0.5
            #print y
            ixp = int(math.floor(xp))
            iyp = int(math.floor(yp))
            vx0 = xp - ixp
            vy0 = yp - iyp
            vx1 = 1 - vx0
            vy1 = 1 - vy0
            v1 = math.sqrt(v1)
            #if iyp==0 and ixp==0:
             #   print hist[0][0][0],"(",x,y,")",v1,vx0,vy0
            if ixp>=0 and iyp>=0:
                hist[best_o][iyp][ixp]+=vx1*vy1*v1

            if ixp+1<blocks[1] and iyp>=0:
                hist[best_o][iyp][ixp+1]+=vx0*vy1*v1

            if ixp>=0 and iyp+1<blocks[0]:
                hist[best_o][iyp+1][ixp]+=vx1*vy0*v1

            if ixp+1<blocks[1] and iyp+1<blocks[0]:
                hist[best_o][iyp+1][ixp+1]+=vx0*vy0*v1
    #print hist[0][0][0]
    for o in range(9):
        for i in range(blocks[0]*blocks[1]):
            indy = int(i/blocks[1])
            indx = i%blocks[1]
            norm[indy][indx] += (hist[o][indy][indx]+hist[o+9][indy][indx])**2

    for x in range(out[2]):
        for y in range(out[1]):
            n1 = 1/math.sqrt(norm[y+1][x+1]+norm[y+2][x+1]+norm[y+1][x+2]+norm[y+2][x+2]+eps)
            n2 = 1/math.sqrt(norm[y][x+1]+norm[y+1][x+1]+norm[y][x+2]+norm[y+1][x+2]+eps)
            n3 = 1/math.sqrt(norm[y+1][x]+norm[y+2][x]+norm[y+1][x+1]+norm[y+2][x+1]+eps)
            n4 = 1/math.sqrt(norm[y][x]+norm[y+1][x]+norm[y][x+1]+norm[y+1][x+1]+eps)
            t1 = 0
            t2 = 0
            t3 = 0
            t4 = 0

            for o in range(18):
                h1 = min(hist[o][y+1][x+1]*n1,0.2)
                h2 = min(hist[o][y+1][x+1]*n2,0.2)
                h3 = min(hist[o][y+1][x+1]*n3,0.2)
                h4 = min(hist[o][y+1][x+1]*n4,0.2)
                feat[o][y][x] = 0.5*(h1+h2+h3+h4)
                t1 += h1
                t2 += h2
                t3 += h3
                t4 += h4

            for o in range(9):
                sum = hist[o][y+1][x+1]+hist[o+9][y+1][x+1]
                h1 = min(sum*n1,0.2)
                h2 = min(sum*n2,0.2)
                h3 = min(sum*n3,0.2)
                h4 = min(sum*n4,0.2)
                feat[o+18][y][x] = 0.5*(h1+h2+h3+h4)

            feat[27][y][x] = 0.2357 * t1
            feat[28][y][x] = 0.2357 * t2
            feat[29][y][x] = 0.2357 * t3
            feat[30][y][x] = 0.2357 * t4
            feat[31][y][x] = 0

    return feat
