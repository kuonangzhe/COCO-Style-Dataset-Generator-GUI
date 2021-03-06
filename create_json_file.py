import xml.etree.cElementTree as ET
import glob
import argparse
import os
import numpy as np
import json
import cv2
from segment import COCO_dataset_generator as cocogen

ap = argparse.ArgumentParser()
ap.add_argument("-i", "--image_dir", required=True, help="Path to the image dir")
args = vars(ap.parse_args())

classes = ['blue_perfume', 'black_perfume', 'double_speedstick', 'blue_speedstick', 'dove_blue', 'dove_perfume', 'dove_pink', 'green_speedstick', 'gear_deo', 'dove_black', 'grey_speedstick', 'choc_blue', 'choc_red', 'choc_yellow', 'black_cup', 'nyu_cup', 'ilny_white', 'ilny_blue', 'ilny_black', 'human']

images, anns = [], []

for i, f in enumerate(sorted(glob.glob(os.path.join(os.path.abspath(args["image_dir"]), '*.jpg')))):
    img = cv2.imread(f)
    height, width, _ = img.shape
    dic = {'file_name': f, 'id': i, 'height': height, 'width': width}
    images.append(dic)

ann_index = 0
for i, f in enumerate(sorted(glob.glob(os.path.join(os.path.abspath(args['image_dir']), '*.txt')))):
    
    ptr = 0
    with open(f, 'r') as g:
        s = g.read()
    s = s.split('\n')[4:-1]
    
    while(ptr<len(s)):
        
        cat_id = classes.index(s[ptr])+1
        area = float(s[ptr+1])
        poly = [[float(x) for x in s[ptr+2].split(' ')[:-1]]]
        
        if len(s)>ptr+3 and s[ptr+3] != '':
            ind = ptr + 3
            while (ind<len(s) and s[ind]!=''):
                poly.append([float(x) for x in s[ind].split(' ')[:-1]])
                ind+=1
            ptr = ind-3
        
        x1, x2, y1, y2 = None, None, None, None
        for p in poly:
            points = np.reshape(np.array(p), (int(len(p)/2), 2))
            
            if x1 is None:
                x1, y1 = points.min(0)
                x2, y2 = points.max(0)
            else:
                if points.min(0)[0]<x1:
                    x1 = points.min(0)[0]
                if points.min(0)[1]<y1:
                    y1 = points.min(0)[1]
                if points.max(0)[0]>x2:
                    x2 = points.max(0)[0]
                if points.max(0)[1]>y2:
                    y2 = points.max(0)[1]
                    
        bbox = [x2, y2, x1, y1]
        dic2 = {'segmentation': poly, 'area': area, 'iscrowd':0, 'image_id':i, 'bbox':bbox, 'category_id': cat_id, 'id': ann_index}
        ann_index+=1
        ptr+=4
        anns.append(dic2)

data = {'images':images, 'annotations':anns, 'categories':[]}

with open('dataset.json', 'w') as outfile:
    json.dump(data, outfile)
