# -*- coding:utf-8 -*-
"""
Created on 23 déc. 2013

@author: Bureau
"""

import os,glob
import win32api, win32con

for root,dirs,files in os.walk('C:/Documents and Settings/Bureau/Mes documents/Dossiers Personnels/Mes images/'):
    for d in dirs:
        if d == 'Thumbs':
            rep = root+'/'+d
            print(rep)
            for f in glob.glob(rep+'/*'):
                win32api.SetFileAttributes(f,win32con.FILE_ATTRIBUTE_HIDDEN)
            win32api.SetFileAttributes(rep,win32con.FILE_ATTRIBUTE_HIDDEN)
print('ok')