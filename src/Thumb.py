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
from PyQt5.QtGui import QImage,QPixmap,QTransform
from . import preferences as PREF
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
        self._thumb = thumb
    
    def mousePressEvent(self,event):
        self._thumb.mousePressEvent(event)
        
from Ihm.widget_miniature import Ui_Miniature as FormClass
from PyQt5.QtWidgets import QWidget as BaseClass

class widgetThumbnail(BaseClass, FormClass):    
    def __init__(self,parent,thumb):
        BaseClassVert.__init__(self, parent)
        self.setupUi(self)
        self._thumb = thumb
    
    def mousePressEvent(self,event):
        self._thumb.mousePressEvent(event)
        
#FormClassHor, BaseClassHor = loadUiType(osp.join(osp.dirname(osp.realpath(__file__)),
#                                           '../Ihm/widget_miniature_hor.ui'))
from Ihm.widget_miniature_hor import Ui_MiniatureHor as FormClassHor
from PyQt5.QtWidgets import QWidget as BaseClassHor

class widgetThumbnailHor(BaseClassHor, FormClassHor):    
    def __init__(self,parent,thumb):
        BaseClassHor.__init__(self, parent)
        self.setupUi(self)
        self._thumb = thumb
    
    def mousePressEvent(self,event):
        self._thumb.mousePressEvent(event)

class thumbnail():
    liste_thumbs = None
    #pipe_fenetre_photo = None
    numero = 0
    ht = {}
    
    def __init__(self, ihm,album,nom):
        self._ihm_miniature = ihm
        self._album = album
        self._nom = nom
        self._ok = False # il ne faut pas considerer que les infos ont été modifiées
        self._parent = ihm.scrollArea
        self.creerWidget()
        self._num = thumbnail.numero
        thumbnail.numero += 1
#         print info
#         self._info = info
        self.afficherInfos()
        self._ok = True
        self._nom_pano = ""
        
    def creerWidget(self):
        self._chemin = self._album.getJPGThumb(self._nom)
        if self._chemin:
            image = QImage((self._chemin),'JPG')
            isHor = image.height()<image.width()
            if PREF.MODE != PREF.MODE_TRI:
                self._widget = widgetThumbnail(self._parent,self)
            else:
                if isHor:
                    self._widget = widgetThumbnailHor(self._parent,self)
                else:
                    self._widget = widgetThumbnailVert(self._parent,self)
#                     self._widget.autre.setVisible(False)
#                     self._widget.etoile.setVisible(False)
#                     self._widget.panorama.setVisible(False)
#                     self._widget.retouche.setVisible(False)
#                     self._widget.traitee.setVisible(False)
                self._widget.autre.stateChanged.connect(self.clickAutre)
                self._widget.traitee.stateChanged.connect(self.clickTraite)
                self._widget.panorama.stateChanged.connect(self.clickPano)
                self._widget.retouche.stateChanged.connect(self.clickRetouche)
                
            self._widget.frame.setForegroundRole(3)
            # migration Qt5 15/12/2025
            #self._widget.setFocusPolicy(Qt.ClickFocus)
            pix = QPixmap.fromImage(image)
            self._widget.label.setPixmap(pix)
            self.creerToolTip()
            #self._next = None
        #self._prev = None
    
    def pivoterImage(self):
        transform = QTransform()
        transform.rotate(90)
        rotated = self._widget.label.pixmap().transformed(transform,QtCore.Qt.SmoothTransformation)
        self._widget.label.setPixmap(rotated)
        self._widget.label.update()

    def creerToolTip(self):
        tooltip = self._nom+'\n'
        #self._exif_data = Exif.getExifData(self._chemin)
        for (nom,value) in list(self.getExif().items()):
            if nom != 'orientation':
                tooltip += nom +' : '+str(value)+'\n'
            if nom == 'focale':
                if value not in thumbnail.ht:
                    thumbnail.ht[value]=1
                else:
                    thumbnail.ht[value]+=1
                    
        #print thumbnail.ht
        self._widget.label.setToolTip(tooltip)
        
    def getExif(self):
        return self._album.getExif(self._nom)
    
    def afficherInfos(self):
        if PREF.MODE == PREF.MODE_TRI:
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
        self._info = info
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
            self._widget.frame.setForegroundRole(0)
            # if affiche:
            #     pass#self._ihm_miniature.affichePhoto(self)
            #     #thumbnail.pipe_fenetre_photo.send('##affiche##'+self._nom+';'+str(self.getEtoiles())+';'+str(self.getTraitee()))
            self._ihm_miniature.scrollArea.ensureWidgetVisible(self._widget,0,500)
        elif self._widget:
            self._widget.frame.setForegroundRole(3)
            
    def getName(self):
        return self._nom
    
    def setName(self,n):
        self._chemin = osp.dirname(self._chemin)+'/'+n
        self._nom = n
        self.creerToolTip()
        
    def nouveauNom(self,ch,num,nb):
        date,date1,date2 = '','',''
        if 'date' in self._exif_data:
            date = self._exif_data['date']
            date = date[:10].replace('/','-')
            date1 = date[:6]+date[8:]
            date2 = date[:5]
        ch_num = '%0'+str(int(log10(nb)+1))+'i'
        return ch.replace('<num>',ch_num % num).replace('<date>',date).replace('<date1>',date1).replace('<date2>',date2)
    
    def getNumero(self):
        return self._num
    
    @staticmethod
    def reinitNumero():
        thumbnail.numero = 0
        
    def getWidget(self):
        return self._widget
    
    def getChemin(self):
        return self._chemin
    
#
# Infos Etoiles
#
    def getEtoiles(self):
        return self._album.getInfo(self._nom)["etoiles"]
    
    def setEtoiles(self,n):
        if PREF.MODE == PREF.MODE_TRI:
            self._album.setInfo(self._nom,"etoiles",n)
            self._album.setInfo(self._nom,"traitee",True)
            #self._info.setEtoiles(n,self._ok)
            #self._info.setTraite(True,self._ok)
            self.afficheEtoiles(n)
            #☻self._ihm_miniature.afficheCommentaire()
        
    def afficheEtoiles(self,n):
        if n == 1:
            etoile = QImage(PREF.getIcon('etoile.bmp'),'BMP')
        elif n == 2:
            etoile = QImage(PREF.getIcon('2etoiles.bmp'),'BMP')
        elif n == 3:
            etoile = QImage(PREF.getIcon('3etoiles.bmp'),'BMP')
        else:
            etoile = QImage()
        pix = QPixmap.fromImage(etoile)
        self._widget.etoile.setPixmap(pix)
#         if not self._ok: # pendant la création de la miniature
#             self._info.imposeEtoiles(n)
        
#
# Infos Traitee
#
    def getTraitee(self):
        return self._album.getInfo(self._nom)["traitee"]
        
    def setTraite(self,n):
        if self.getTraitee() != n:
            self._album.getInfo(self._nom)["traitee"] = n
        self.afficheTraite(n)

    def afficheTraite(self,n):
        if n:
            self._widget.traitee.setCheckState(Qt.Checked)
        else:
            self._widget.traitee.setCheckState(Qt.Unchecked)

    def clickTraite(self,value):
        self.setTraite(value == Qt.Checked)
        
#
# Infos Etoiles
#
    def getAutre(self):
        return self._album.getInfo(self._nom)["cochee"]
         
    def setAutre(self,n):
        if self.getAutre() != n:
            self._album.getInfo(self._nom)["cochee"] = n
        self.afficheAutre(n)
 
    def afficheAutre(self,n):
        if n:
            self._widget.autre.setCheckState(Qt.Checked)
        else:
            self._widget.autre.setCheckState(Qt.Unchecked)
 
    def clickAutre(self,value):
        self.setAutre(value == Qt.Checked)
#         self._ihm_miniature.infosModifiees()
#         self._ihm_miniature.afficheCommentaire()
    
#
# Infos Pano
#
    def getPano(self):
        return self._album.getInfo(self._nom)["pano"]
    
    def setPano(self,n):
        self._album.getInfo(self._nom)["pano"] = n
        self.affichePano(n)
        if not n: self.setNomPano("")

    def affichePano(self,n):
        if n:
            self._widget.panorama.setCheckState(Qt.Checked)
        else:
            self._widget.panorama.setCheckState(Qt.Unchecked)

    def clickPano(self,value):
        self.setPano(value == Qt.Checked)
        #self._ihm_miniature.infosModifiees()
        #self._ihm_miniature.afficheCommentaire()
    
    def setNomPano(self,nom):
        self._nom_pano = nom
        self._widget.nom_pano.setText(nom)
        
    def getNomPano(self):
        return self._nom_pano
#
# Infos Retouche
#
    def getRetouche(self):
        return self._album.getInfo(self._nom)["retouche"]
    
    def setRetouche(self,n):
        self._album.getInfo(self._nom)["retouche"] = n
        self.afficheRetouche(n)

    def afficheRetouche(self,n):
        if n:
            self._widget.retouche.setCheckState(Qt.Checked)
        else:
            self._widget.retouche.setCheckState(Qt.Unchecked)

    def clickRetouche(self,value):
        self.setRetouche(value == Qt.Checked)
#         self._ihm_miniature.infosModifiees()
#         self._ihm_miniature.afficheCommentaire()
    
    def __repr__(self):
        return 'Thumb['+self._nom +", "+str(self._num)+']'
    
    def __eq__(self,th):
        return self._num == th._num
