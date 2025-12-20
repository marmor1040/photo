## -*- coding: utf-8 -*-

import time
import os.path as osp
from PyQt5.QtWidgets import QApplication,QPushButton
from PyQt5.QtGui import QIcon,QImage,QPixmap
from PyQt5.QtCore import Qt,QSize

from Ihm.miniature_visionneuse import Ui_widget as FormClass
from PyQt5.QtWidgets import QWidget as BaseClass
from PyQt5 import QtWidgets

class FenetreThumbVisionneuse(BaseClass,FormClass):
    
    def __init__(self,visionneuse):
        BaseClass.__init__(self,visionneuse)
        self.setupUi(self)
        self.setWindowFlags(Qt.FramelessWindowHint |Qt.WindowStaysOnTopHint)
        self.resize(225,500)
        sizePolicy = QtWidgets.QSizePolicy(QtWidgets.QSizePolicy.Fixed, QtWidgets.QSizePolicy.Preferred)
        sizePolicy.setHorizontalStretch(0)
        sizePolicy.setVerticalStretch(0)
        self.label.setSizePolicy(sizePolicy)
        self.ihmVisionneuse = visionneuse
        self.label.hide()
        self.lImageBt = []
        self.selectedName = None
        self.creationOk = False
        
    def vider(self):
        # destruction des widgets pr�c�dents
        nb = self.images.count()
        for i in range(nb):
            tn = self.images.takeAt(0)
            if tn and tn.widget():
                w = tn.widget()
                self.images.removeWidget(w)
                w.deleteLater()
                w.repaint()
                
    def creer(self,repertoire,liste_photos):
        self.vider()
        for p in liste_photos:
            self.ajoutePhoto(repertoire,p)
            QApplication.instance().processEvents()
        
    def setPosition(self,x,H):
        self.move(x,0)
        self.resize(200,H)

    def affiche(self,b):
        if b and self.creationOk: self.show()
        else: self.hide()
        
    def ajoutePhoto(self,rep,nom):
        thumb = rep+"/TriPhotos/Thumbs/"+nom
        if osp.isfile(thumb):
            Photo = QImage(QString(thumb),'JPG')
            pm = QPixmap.fromImage(Photo)
            #print time.time()-t0
            #lbl = QLabel(nom)
            #self.images.addWidget(lbl)
            ibt = imageButton(self.ihmVisionneuse,pm,nom)
            self.images.addWidget(ibt.button)
            self.lImageBt.append(ibt)
            #print time.time()-t0
            self.creationOk = True
        
class imageButton():
    def __init__(self,ihmVisionneuse,pixmap,photo):
        self.ihmVisionneuse = ihmVisionneuse
        self.photo = photo
        self.button = QPushButton()
        self.button.setIcon(QIcon(pixmap))
        self.button.setIconSize(QSize(200,140))
        self.button.setStyleSheet("padding:-10px 0px -5px 0px");
        self.button.clicked.connect(self.select)
        
    def select(self,checked):
        self.ihmVisionneuse.affichePhoto(self.photo)
        self.ihmVisionneuse.setNumero()
        
if __name__ == "__main__":
    app = QApplication([])
    app.setStyle("plastique")
    ihm = FenetreThumbVisionneuse(None)
    ihm.ajoutePhoto("C:/Users/marc/Documents/Dossiers personnel/Mes images/2020/2020-02_Birmanie/Birmanie_0019_10-02-2020.JPG")
    ihm.ajoutePhoto("C:/Users/marc/Documents/Dossiers personnel/Mes images/2020/2020-02_Birmanie/Birmanie_0020_10-02-2020.JPG")
    ihm.ajoutePhoto("C:/Users/marc/Documents/Dossiers personnel/Mes images/2020/2020-02_Birmanie/Birmanie_0021_10-02-2020.JPG")
    ihm.ajoutePhoto("C:/Users/marc/Documents/Dossiers personnel/Mes images/2020/2020-02_Birmanie/Birmanie_0022_10-02-2020.JPG")
    ihm.ajoutePhoto("C:/Users/marc/Documents/Dossiers personnel/Mes images/2020/2020-02_Birmanie/Birmanie_0021_10-02-2020.JPG")
#     ihm.affichePhoto("C:/Users/marc/Documents/Dossiers personnel/Mes images/2020/2020-02_Birmanie/Birmanie_0022_10-02-2020.JPG",5)
    ihm.show()
    app.exec_()
