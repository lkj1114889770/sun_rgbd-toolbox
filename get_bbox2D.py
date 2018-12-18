import os
import json
import numpy as np
import cv2

root_dir = '/home/zju/lkj/data/SUNRGBD/'  # root directory of the sun-rgbd dataset, it should be changed to your directory
all_paths= os.walk(root_dir)
all_paths=list(all_paths)
imgs_path=[]

# Traverses all subpaths to find all image path
for maindir, subdir, file_name_list in all_paths:
    if 'seg.mat' in file_name_list:
        image_path = os.path.join(maindir,'image/')
        assert len(os.listdir(image_path))==1 # aseert only 1 image in dir 'image/'
        image_path = os.listdir(image_path)[0] 
        img_path = os.path.join(maindir,'image/'+image_path) 
        imgs_path.append(img_path)
        
annotations_path=[]
for img_path in imgs_path:
    annotation_file_path  = '/'.join(img_path.split('/')[:-2])+'/annotation/index.json'
    assert os.path.exists(annotation_file_path)
    annotations_path.append(annotation_file_path)

def get_annotations(imgs_path,annotations_path):
    print('start to index...')
    bbox2Dfiles = {}
    idx=0
    for img_path,annotation_file_path in zip(imgs_path,annotations_path):
        img = cv2.imread(img_path)
        H,W,C=img.shape
        depth = os.listdir('/'.join(img_path.split('/')[:-2])+'/depth/')[0]
        depth_path = os.path.join('/'.join(img_path.split('/')[:-2])+'/depth/',depth)
        assert os.path.exists(depth_path)
        bbox2Dfiles[idx]={"image":img_path,"depth":depth_path,"annotation":{}}
		
        try:
            with open(annotation_file_path) as open_file:
                data = json.load(open_file)
        except:  # some of the json file can not be loaded, just skip
            continue
        if len(data['objects'])<=max(list(map(lambda x: x['object'],data["frames"][0]["polygon"]))):
            continue
        numberOfAnot = len(data["frames"][0]["polygon"])
        objs={}
        for i in range(0,numberOfAnot):
            x = data["frames"][0]["polygon"][i]["x"]
            y = data["frames"][0]["polygon"][i]["y"]
            if x==[] or not isinstance(x,list):  # skip when x==[] or x is not a list without more than 2 elements
                continue
            idxObj = data["frames"][0]["polygon"][i]["object"]
            pts2 = np.array([x,y], np.int32)
            pts2 = np.transpose(pts2)
            
            x1,x2=int(np.min(pts2[:,0])),int(np.max(pts2[:,0]))
            y1,y2=int(np.min(pts2[:,1])),int(np.max(pts2[:,1]))
            
            if idxObj not in objs.keys():
                objs[idxObj]={'class_name':data['objects'][idxObj]["name"],'bbox':[max(x1,0),max(y1,0),min(x2,W),min(y2,H)]}
            else:
                x11,y11,x22,y22=objs[idxObj]['bbox']
                objs[idxObj]['bbox']=[max(min(x11,x1),0),max(min(y11,y1),0),min(max(x22,x2),W),min(max(y22,y2),H)]
        bbox2Dfiles[idx]['annotation']=objs
        idx = idx +1
    print('There are %d index.json have been indexed!'%(idx))
    return bbox2Dfiles
#     print(idx)
annotations = get_annotations(imgs_path,annotations_path)  

with open('./lables_bbox2D.json', 'w') as fileObject:
        json.dump(annotations,fileObject)    