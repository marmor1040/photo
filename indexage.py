# -*- coding: utf-8
'''
Created on 2 déc. 2018

@author: marc
'''

import glob
import os.path as osp
from common import scanRep

rep_images = "C:\\Users\marc\Documents\Dossiers personnel\Mes images"
for d in glob.glob(rep_images+"/*"):
    try:
        jpg = scanRep.first(d,"jpg")
        if jpg and not osp.isdir(d+"/TriPhotos"):
            print(d, "non traité")
        else:
            print(d, "ok")
    except:
        print("pb",d)