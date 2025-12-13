# -*- coding:utf-8 -*-
"""
Created on 19 mars 2011

@author: Bureau
"""
import os,shutil
rep_exe = 'TriPhoto'
dist_dir = 'D:/Documents and Settings/Bureau/Mes documents/Dossiers Personnels/Developpement logiciels/bin/'
if os.path.isdir(dist_dir+rep_exe):
    shutil.rmtree(dist_dir+rep_exe)
os.system('python setup.py py2exe --dist-dir '+rep_exe)
shutil.move(rep_exe, dist_dir+rep_exe)
shutil.rmtree('build')

