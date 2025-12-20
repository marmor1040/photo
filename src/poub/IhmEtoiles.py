# -*- coding: utf-8
"""
Created on 5 juin 2011

@author: Bureau
"""

from PyQt5.QtCore import Qt
#from PyQt5.uic import loadUiType
#FormClass, BaseClass = loadUiType(osp.join(osp.dirname(osp.realpath(__file__)),
#                                           '../Ihm/fen_diaporama.ui'))

from fen_etoiles import Ui_Etoiles as FormClass
from PyQt5.QtWidgets import QDialog as BaseClass

class FenetreEtoiles(BaseClass, FormClass):
    def __init__(self,parent):
        BaseClass.__init__(self, parent)
        self.setupUi(self)
        self.setWindowFlags(Qt.FramelessWindowHint)
        self.move(10,10)
        self.show()
    
    def afficheEtoiles(self,n,traite):
        s = str(n)
        if traite:
            s += '*'
        self.label.setText(s)