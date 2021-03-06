import os
import argparse
import glob
import xml.etree.ElementTree as ET
import json
import cv2

classes = ['black_backpack', 'nine_west_bag', 'meixuan_brown_handbag', 'sm_bdrew_grey_handbag', 'wine_red_handbag', 'sm_bclarre_blush_crossbody', 'mk_brown_wrislet', 'black_plain_bag', 'lmk_brown_messenger_bag', 'sm_peach_backpack', 'black_ameligalanti', 'white_bag']   

if __name__=='__main__':

    ap = argparse.ArgumentParser(description='Convert PASCAL VOC format dataset to COCO style dataset')
    ap.add_argument("-d", "--pascal_dir", required=True, help="Path to the PASCAL VOC style dataset")
    args = vars(ap.parse_args())
    
    images, anns = [], []
    ann_index = 0
    
    for i, f in enumerate(glob.glob(os.path.join(args['pascal_dir'], 'JPEGImages/*.png'))):
        annot = os.path.join(args['pascal_dir'], 'Annotations', f.split('/')[-1][:-3]+'xml')
        tree = ET.parse(annot)
        root = tree.getroot()         
    
        img = cv2.imread(f)
        height, width, _ = img.shape
        dic = {'file_name': os.path.abspath(f), 'id': i, 'height': height, 'width': width}
        images.append(dic)

        for obj in root.findall('object'):
       
            cls_id = classes.index(obj.find('name').text)+1
            bx = [int(obj.find('bndbox').find('xmax').text), int(obj.find('bndbox').find('ymax').text), int(obj.find('bndbox').find('xmin').text), int(obj.find('bndbox').find('ymin').text)]
            pts = [bx[2], bx[3], bx[0], bx[3], bx[0], bx[1], bx[2], bx[1]]
            area = (bx[0]-bx[2])*(bx[1]-bx[3])
            dic2 = {'segmentation': pts, 'area': area, 'iscrowd':0, 'image_id':i, 'bbox':bx, 'category_id': cls_id, 'id': ann_index}
            ann_index+=1
            anns.append(dic2)

    data = {'images':images, 'annotations':anns, 'categories':[]}

    with open('pascal_dataset.json', 'w') as outfile:
        json.dump(data, outfile)
