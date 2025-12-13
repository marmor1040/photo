# -*- coding:utf-8 -*-
"""
Created on 5 juin 2011

@author: Bureau
"""
from . import preferences

#from PyQt5.uic import loadUiType
#FormClass, BaseClass = loadUiType(osp.join(osp.dirname(osp.realpath(__file__)),
#                                           '../Ihm/fen_preferences.ui'))
from Ihm.fen_preferences import Ui_Preferences as FormClass
from PyQt5.QtWidgets import QDialog as BaseClass

class FenetrePreferences(BaseClass,FormClass):
    __fenetre_thumbs = None
    def __init__(self,parent):
        BaseClass.__init__(self, parent)
        self.setupUi(self)
        FenetrePreferences.__fenetre_thumbs = parent

    def affiche(self):
        self.sbThumbs_x.setValue(preferences.THUMBS_GEOMETRY[0])
        self.sbThumbs_y.setValue(preferences.THUMBS_GEOMETRY[1])
        self.sbThumbs_larg.setValue(preferences.THUMBS_GEOMETRY[2])
        self.sbThumbs_haut.setValue(preferences.THUMBS_GEOMETRY[3])
        self.sbPhoto_x.setValue(preferences.PHOTO[0])
        self.sbPhoto_y.setValue(preferences.PHOTO[1])
        self.sbPhoto_larg.setValue(preferences.PHOTO[2])
        self.sbPhoto_haut.setValue(preferences.PHOTO[3])
        self.show()

    def accept(self):
        print('toto')
        
    def reject(self):
        print('titi')
        
    def update(self):
        preferences.THUMBS = (self.sbThumbs_x.value(),self.sbThumbs_y.value(),\
            self.sbThumbs_larg.value(),self.sbThumbs_haut.value())
        preferences.PHOTO = (self.sbPhoto_x.value(),self.sbPhoto_y.value(),\
            self.sbPhoto_larg.value(),self.sbPhoto_haut.value())
        FenetrePreferences.__fenetre_thumbs.updateSize(preferences.THUMBS_GEOMETRY,preferences.PHOTO)
        
        
        
        
        