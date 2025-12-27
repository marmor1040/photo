# -*- coding:utf-8 -*-
"""
Created on 3 juin 2011

@author: Bureau
"""

from math import *
import os.path as osp
from PyQt5.Qt import Qt
from PyQt5 import QtCore, QtWidgets
from PyQt5.QtCore import QObject
from PyQt5.QtGui import QImage,QPixmap
from . import preferences
from common import Exif

#from PyQt5.uic import loadUiType
#FormClassVert, BaseClassVert = loadUiType(osp.join(osp.dirname(osp.realpath(__file__)),
#                                           '../Ihm/widget_miniature_vert.ui'))
from Ihm.widget_miniature_vert import Ui_MiniatureVer as FormClassVert
from PyQt5.QtWidgets import QWidget as BaseClassVert

class widgetThumbnailVert(BaseClassVert, FormClassVert):    
    def __init__(self,parent,thumb):
        BaseClassVert.__init__(self, parent)
        self.setupUi(self)
        self.__thumb = thumb
    
    def mousePressEvent(self,event):
        self.__thumb.mousePressEvent(event)
        
from Ihm.widget_miniature import Ui_Miniature as FormClass
from PyQt5.QtWidgets import QWidget as BaseClass

class widgetThumbnail(BaseClass, FormClass):    
    def __init__(self,parent,thumb):
        BaseClassVert.__init__(self, parent)
        self.setupUi(self)
        self.__thumb = thumb
    
    def mousePressEvent(self,event):
        self.__thumb.mousePressEvent(event)
        
#FormClassHor, BaseClassHor = loadUiType(osp.join(osp.dirname(osp.realpath(__file__)),
#                                           '../Ihm/widget_miniature_hor.ui'))
from Ihm.widget_miniature_hor import Ui_MiniatureHor as FormClassHor
from PyQt5.QtWidgets import QWidget as BaseClassHor

class widgetThumbnailHor(BaseClassHor, FormClassHor):    
    def __init__(self,parent,thumb):
        BaseClassHor.__init__(self, parent)
        self.setupUi(self)
        self.__thumb = thumb
    
    def mousePressEvent(self,event):
        self.__thumb.mousePressEvent(event)

class thumbnail():
    liste_thumbs = None
    #pipe_fenetre_photo = None
    numero = 0
    ht = {}
    
    def __init__(self, ihm,album,nom):
        self.__ihm_miniature = ihm
        self.__album = album
        self.__nom = nom
        self.__ok = False # il ne faut pas considerer que les infos ont été modifiées
        self.creerWidget(ihm.scrollArea)
        self.__num = thumbnail.numero
        thumbnail.numero += 1
#         print info
#         self.__info = info
        self.afficherInfos()
        self.__ok = True
        self.__nom_pano = ""
        
    def creerWidget(self, parent):
        self.__chemin = self.__album.getJPGThumb(self.__nom)
        if self.__chemin:
            image = QImage((self.__chemin),'JPG')
            isHor = image.height()<image.width()
            if preferences.isModeVisionneuse():
                self.__widget = widgetThumbnail(parent,self)
            else:
                if isHor:
                    self.__widget = widgetThumbnailHor(parent,self)
                else:
                    self.__widget = widgetThumbnailVert(parent,self)
#                     self.__widget.autre.setVisible(False)
#                     self.__widget.etoile.setVisible(False)
#                     self.__widget.panorama.setVisible(False)
#                     self.__widget.retouche.setVisible(False)
#                     self.__widget.traitee.setVisible(False)
                self.__widget.autre.stateChanged.connect(self.clickAutre)
                self.__widget.traitee.stateChanged.connect(self.clickTraite)
                self.__widget.panorama.stateChanged.connect(self.clickPano)
                self.__widget.retouche.stateChanged.connect(self.clickRetouche)
                
            self.__widget.frame.setForegroundRole(3)
            # migration Qt5 15/12/2025
            #self.__widget.setFocusPolicy(Qt.ClickFocus)
            pix = QPixmap.fromImage(image)
            self.__widget.label.setPixmap(pix)
            self.creerToolTip()
            #self.__next = None
        #self.__prev = None
    
    def creerToolTip(self):
        tooltip = self.__nom+'\n'
        #self.__exif_data = Exif.getExifData(self.__chemin)
        for (nom,value) in list(self.getExif().items()):
            if nom != 'orientation':
                tooltip += nom +' : '+str(value)+'\n'
            if nom == 'focale':
                if value not in thumbnail.ht:
                    thumbnail.ht[value]=1
                else:
                    thumbnail.ht[value]+=1
                    
        #print thumbnail.ht
        self.__widget.label.setToolTip(tooltip)
        
    def getExif(self):
        return self.__album.getExif(self.__nom)
    
    def afficherInfos(self):
        if preferences.isModeTri():
            self.afficheEtoiles(self.getEtoiles())
            self.afficheAutre(self.getAutre())
            self.afficheTraite(self.getTraitee())
            self.affichePano(self.getPano())
            self.afficheRetouche(self.getRetouche())
        
    def appliquerInfos(self,infos):
        etoiles = infos[0]
        traites = infos[1]
        pano = infos[2]
        retouche = infos[3]
        autres = infos[4]
        if etoiles[0]: self.setEtoiles(etoiles[1])
        if traites[0]: self.setTraite(traites[1])
        if pano[0]:    self.setPano(pano[1])
        if retouche[0]:    self.setRetouche(retouche[1])
        if autres[0]:    self.setAutre(autres[1])
    
    def setInfo(self,info):
        self.__info = info
        self.afficherInfos()
        
    def mousePressEvent(self,event):
        #print event.button(),event.modifiers() == Qt.ControlModifier
        if event.button() == Qt.LeftButton:
            if event.modifiers() == Qt.ControlModifier:
                thumbnail.liste_thumbs.ajouteSelect(self)
            elif event.modifiers() == Qt.ShiftModifier:
                thumbnail.liste_thumbs.ajouteSelect(self,True)
            else:
                thumbnail.liste_thumbs.select(self)
            
    def select(self,ok):
        if ok:
            self.__widget.frame.setForegroundRole(0)
            # if affiche:
            #     pass#self.__ihm_miniature.affichePhoto(self)
            #     #thumbnail.pipe_fenetre_photo.send('##affiche##'+self.__nom+';'+str(self.getEtoiles())+';'+str(self.getTraitee()))
            self.__ihm_miniature.scrollArea.ensureWidgetVisible(self.__widget,0,500)
        elif self.__widget:
            self.__widget.frame.setForegroundRole(3)
            
    def getName(self):
        return self.__nom
    
    def setName(self,n):
        self.__chemin = osp.dirname(self.__chemin)+'/'+n
        self.__nom = n
        self.creerToolTip()
        
    def nouveauNom(self,ch,num,nb):
        date,date1,date2 = '','',''
        if 'date' in self.__exif_data:
            date = self.__exif_data['date']
            date = date[:10].replace('/','-')
            date1 = date[:6]+date[8:]
            date2 = date[:5]
        ch_num = '%0'+str(int(log10(nb)+1))+'i'
        return ch.replace('<num>',ch_num % num).replace('<date>',date).replace('<date1>',date1).replace('<date2>',date2)
    
    def getNumero(self):
        return self.__num
    
    @staticmethod
    def reinitNumero():
        thumbnail.numero = 0
        
    def getWidget(self):
        return self.__widget
    
    def getChemin(self):
        return self.__chemin
    
#
# Infos Etoiles
#
    def getEtoiles(self):
        return self.__album.getInfo(self.__nom)["etoiles"]
    
    def setEtoiles(self,n):
        if preferences.isModeTri():
            self.__album.setInfo(self.__nom,"etoiles",n)
            self.__album.setInfo(self.__nom,"traitee",True)
            #self.__info.setEtoiles(n,self.__ok)
            #self.__info.setTraite(True,self.__ok)
            self.afficheEtoiles(n)
            #☻self.__ihm_miniature.afficheCommentaire()
        
    def afficheEtoiles(self,n):
        from . import preferences as PREFERENCES
        if n == 1:
            etoile = QImage(PREFERENCES.getIcon('etoile.bmp'),'BMP')
        elif n == 2:
            etoile = QImage(PREFERENCES.getIcon('2etoiles.bmp'),'BMP')
        elif n == 3:
            etoile = QImage(PREFERENCES.getIcon('3etoiles.bmp'),'BMP')
        else:
            etoile = QImage()
        pix = QPixmap.fromImage(etoile)
        self.__widget.etoile.setPixmap(pix)
#         if not self.__ok: # pendant la création de la miniature
#             self.__info.imposeEtoiles(n)
        
#
# Infos Traitee
#
    def getTraitee(self):
        return self.__album.getInfo(self.__nom)["traitee"]
        
    def setTraite(self,n):
        if self.getTraitee() != n:
            self.__album.getInfo(self.__nom)["traitee"] = n
        self.afficheTraite(n)

    def afficheTraite(self,n):
        if n:
            self.__widget.traitee.setCheckState(Qt.Checked)
        else:
            self.__widget.traitee.setCheckState(Qt.Unchecked)

    def clickTraite(self,value):
        self.setTraite(value == Qt.Checked)
        
#
# Infos Etoiles
#
    def getAutre(self):
        return self.__album.getInfo(self.__nom)["cochee"]
         
    def setAutre(self,n):
        if self.getAutre() != n:
            self.__album.getInfo(self.__nom)["cochee"] = n
        self.afficheAutre(n)
 
    def afficheAutre(self,n):
        if n:
            self.__widget.autre.setCheckState(Qt.Checked)
        else:
            self.__widget.autre.setCheckState(Qt.Unchecked)
 
    def clickAutre(self,value):
        self.setAutre(value == Qt.Checked)
#         self.__ihm_miniature.infosModifiees()
#         self.__ihm_miniature.afficheCommentaire()
    
#
# Infos Pano
#
    def getPano(self):
        return self.__album.getInfo(self.__nom)["pano"]
    
    def setPano(self,n):
        self.__album.getInfo(self.__nom)["pano"] = n
        self.affichePano(n)
        if not n: self.setNomPano("")

    def affichePano(self,n):
        if n:
            self.__widget.panorama.setCheckState(Qt.Checked)
        else:
            self.__widget.panorama.setCheckState(Qt.Unchecked)

    def clickPano(self,value):
        self.setPano(value == Qt.Checked)
        #self.__ihm_miniature.infosModifiees()
        #self.__ihm_miniature.afficheCommentaire()
    
    def setNomPano(self,nom):
        self.__nom_pano = nom
        self.__widget.nom_pano.setText(nom)
        
    def getNomPano(self):
        return self.__nom_pano
#
# Infos Retouche
#
    def getRetouche(self):
        return self.__album.getInfo(self.__nom)["retouche"]
    
    def setRetouche(self,n):
        self.__album.getInfo(self.__nom)["retouche"] = n
        self.afficheRetouche(n)

    def afficheRetouche(self,n):
        if n:
            self.__widget.retouche.setCheckState(Qt.Checked)
        else:
            self.__widget.retouche.setCheckState(Qt.Unchecked)

    def clickRetouche(self,value):
        self.setRetouche(value == Qt.Checked)
#         self.__ihm_miniature.infosModifiees()
#         self.__ihm_miniature.afficheCommentaire()
    
    def __repr__(self):
        return 'Thumb['+self.__nom +", "+str(self.__num)+']'
    
    def __eq__(self,th):
        return self.__num == th.__num
