# -*- coding:utf-8 -*-
"""
Created on 26 août 2011

@author: Bureau
"""
from PyQt5.uic import compileUi
import glob

def comp(fich):
    f=open(fich.replace(".ui",".py"),'w')
    print('Compilation de :',fich,'...', end=' ')
    compileUi(fich,f,True)
    print('ok')

print(glob.glob("Ihm/*.ui"))
for f in glob.glob("Ihm/*.ui"):
    comp(f)
    
#     comp('../Ihm/choix_filtre')
# comp('../Ihm/choix_repertoire')
# comp('../Ihm/choix_selection')
# comp('../Ihm/fen_diaporama')
# comp('../Ihm/fen_infos')
# comp('../Ihm/fen_miniatures')
# comp('../Ihm/fen_preferences')
# comp('../Ihm/fen_visionneuse')
# comp('../Ihm/fen_etoiles')
# comp('../Ihm/widget_miniature_hor')
# comp('../Ihm/widget_miniature_vert')
# comp('../Ihm/widget_miniature')
