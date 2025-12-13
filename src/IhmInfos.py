# -*- coding: latin-1
"""
Created on 5 juin 2011

@author: Bureau
"""
from PyQt5 import QtCore
from PyQt5.QtCore import QObject,Qt,QLocale

#from PyQt5.uic import loadUiType
#FormClass, BaseClass = loadUiType(osp.join(osp.dirname(osp.realpath(__file__)),
#                                           '../Ihm/fen_infos.ui'))
from Ihm.fen_infos import Ui_Infos as FormClass
from PyQt5.QtWidgets import QDialog as BaseClass

class FenetreInfos(BaseClass,FormClass):
    __fenetre_thumbs = None
    def __init__(self,parent):
        BaseClass.__init__(self, None)
        self.setupUi(self)
        
        self.buttonBox.setLocale(QLocale(QLocale.French))
        FenetreInfos.__fenetre_thumbs = parent
        QObject.connect(self.bt_toutes,QtCore.SIGNAL("clicked()"),self.appliquerToutes)
        QObject.connect(self.bt_selection,QtCore.SIGNAL("clicked()"),self.appliquerSelection)
                    
    def appliquerToutes(self):
        FenetreInfos.__fenetre_thumbs.appliquerInfos(self.getInfos(),True)

    def appliquerSelection(self):
        FenetreInfos.__fenetre_thumbs.appliquerInfos(self.getInfos(),False)
        
    def getInfos(self):
        if self.cb_0_etoile.isChecked():
            etoiles = 0
        elif self.cb_1_etoile.isChecked():
            etoiles = 1
        elif self.cb_2_etoiles.isChecked():
            etoiles = 2
        else:
            etoiles = 3
        autre = (self.cb_autre.checkState() == Qt.Checked)
        traitee = (self.cb_traitee.checkState() == Qt.Checked)
        pano = (self.cb_panorama.checkState() == Qt.Checked)
        retouche = (self.cb_retouche.checkState() == Qt.Checked)
        res = ((self.etoiles.isChecked(),etoiles),\
                (self.traitee.isChecked(),traitee),\
                (self.panorama.isChecked(),pano),\
                (self.retouche.isChecked(),retouche),\
                (self.autre.isChecked(),autre))
        return res

    def affiche(self):
        self.show()

    def accept(self):
        self.hide()

        
        
        
        