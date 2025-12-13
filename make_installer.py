# -*- coding:utf-8 -*-
"""
Created on 19 mars 2011

@author: Bureau
"""
import sys
sys.path.append("C:\\Users\marc\Documents\Dossiers personnel\Developpement logiciels\Workspace\Make")
import make_utils
    
rep_cible = "C:/Users/marc/Documents/Dossiers personnel/Developpement logiciels/bin/TriPhoto/"
exe = "TriPhoto.exe"
target = "triPhoto.py"
lData=[]
lDataNePasEcraser = []

make_utils.installer(target,exe,rep_cible,lData,lDataNePasEcraser)
        


