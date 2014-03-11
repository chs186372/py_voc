import numpy as np
import resize
import test
import features
import featpyramid
import datetime

pic,model=test.getFile()
starttime = datetime.datetime.now()
result = featpyramid.featpyramid(pic,model)
endtime = datetime.datetime.now()
print (endtime - starttime).seconds