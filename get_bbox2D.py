import os
import json
import numpy as np
import scipy.io

mat = scipy.io.loadmat('./SUNRGBDMeta2DBB_v2.mat')
meta2Dbb = mat['SUNRGBDMeta2DBB'][0]

bbox2D={}
idx=0
for i in range(len(meta2Dbb)):
    if meta2Dbb[i][1].shape[1]<=0: # ensure contain 2D bbox
        continue
    img_path = '/home/zju/lkj/data/'+'/'.join(meta2Dbb[i][3][0].split('/')[5:])  # the image and depth path should be changed according to your path
    img = cv2.imread(img_path)
    ih,iw,ic=img.shape
    depth_path = '/home/zju/lkj/data/'+'/'.join(meta2Dbb[i][2][0].split('/')[5:])
    bbox2D[idx]={'image':img_path,'depth':depth_path,'annotation':{}}
    ibox=0
    for ele in meta2Dbb[i][1][0]:
        name = ele[2][0]
        x,y,w,h=ele[1][0].tolist()
        bbox=[max(int(x),0),max(int(y),0),min(int(x+w),iw),min(int(y+h),ih)]
        if bbox[0]>=bbox[2] or bbox[1]>=bbox[3]:
            continue
        bbox2D[idx]['annotation'][ibox]={'bbox':bbox,'class_name':name.lower()}
        ibox = ibox+1
    idx=idx+1
with open('./lables_bbox2D.json', 'w') as fileObject:
        json.dump(bbox2D,fileObject) 