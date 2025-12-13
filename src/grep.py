# -*- coding:utf-8 -*-
#!/bin/python
"""
Created on 11 juil. 2011

@author: Bureau
"""

import os.path as osp
import glob
import sys


def grep(ch,l):
    for f in l:
        if osp.isfile(f):
            of = open(f)
            n=0
            lines = of.readlines()
            for l in lines:
                if ch in l:
                    print(f,'('+str(n)+') :',l[:-1]))
                n+=1
            of.close()

if __name__=='__main__':
    ch = sys.argv[1]
    print('Recherche de',ch)
    l = glob.glob(sys.argv[2])
    grep(ch,l)
