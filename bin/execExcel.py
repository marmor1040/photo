# -*- coding:utf-8 -*-
"""
Created on 19 mars 2011

@author: Bureau
"""
import os
import placements
import config

def run():
    os.chdir(config.rep_cible)
    os.system(config.excel+' '+placements.fichierComptes+' '+placements.fichierCM+' '+
              placements.fichierSG+' '+placements.fichierPEG+' '+placements.fichierMAIF)
    
if __name__ == '__main__':
    run()