# -*- coding: utf-8
"""
Created on 5 juin 2011

@author: Bureau
"""
from PyQt5 import QtCore, QtWidgets
from PyQt5.QtCore import Qt
from PyQt5.QtWidgets import QFileSystemModel,QTreeView
from PyQt5.QtGui import QPixmap
import os.path as osp
import os
from common import scanRep
from src import preferences as PREFERENCES

class MyQFileSystemModel(QFileSystemModel):
    def __init__(self):
        super(MyQFileSystemModel, self).__init__()
        self.__selection = None
        self.__affichage = None
        self.__Album = QPixmap(PREFERENCES.getIcon("album.png"))
        self.__Album_attention = QPixmap(PREFERENCES.getIcon("album-attention.png"))
        self.__Album_nonVide = QPixmap(PREFERENCES.getIcon("album-non-vide.png"))
        self.__Album_ok = QPixmap(PREFERENCES.getIcon("album3.png"))
        self.__Image = QPixmap(PREFERENCES.getIcon("repImage.png"))
        self.__Video = QPixmap(PREFERENCES.getIcon("repVideo.png"))
        self.__RepNormal = QPixmap(PREFERENCES.getIcon("vide1.png"))
        self.__Vide = QPixmap(PREFERENCES.getIcon("vide.png"))
        self.setNameFilters(["*.jpg"])
        self.setNameFilterDisables(True)
        
    def data(self,index,role):
        if role == Qt.DecorationRole:
            rep = str(self.filePath(index))
            if osp.isdir(rep):
                jpg = scanRep.first(rep,'.JPG')
                if jpg:
#                     ld = [d for d in os.listdir(rep) if os.path.isdir(rep+'/'+d)]
#                     if "TriPhotos" in ld: ld.remove("TriPhotos")
#                     if ld: return self.__Album_attention
                    if osp.isdir(rep+'/TriPhotos'):
                        if scanRep.first(rep+'/TriPhotos/Pano','.JPG') or \
                            scanRep.first(rep+'/TriPhotos/Recuperation','.JPG') or \
                            scanRep.first(rep+'/TriPhotos/Retouche','.JPG'):
                            return self.__Album_nonVide
                        else:
                            return self.__Album
                    else:
                        return self.__Image
                else:
                    mov = scanRep.first(rep,'.MOV')
                    if mov:
                        return self.__Video
#                     elif scanRep.first(rep):
#                         return self.__Normal    
                    elif os.listdir(rep):
                        return self.__RepNormal
                    else:
                        return self.__Vide
        return QFileSystemModel.data(self,index, role)
    
    def flags(self,index):
        return QFileSystemModel.flags(self,index) | Qt.ItemIsEditable
    
try:
    _fromUtf8 = QtCore.QString.fromUtf8
except AttributeError:
    def _fromUtf8(s):
        return s
        
class MyTreeView(QTreeView):
    def __init__(self,ihm_arbo):
        super(MyTreeView, self).__init__(ihm_arbo.centralwidget)
        self._ihm_arbo = ihm_arbo
        sizePolicy = QtWidgets.QSizePolicy(QtWidgets.QSizePolicy.Preferred, QtWidgets.QSizePolicy.Expanding)
        sizePolicy.setHorizontalStretch(0)
        sizePolicy.setVerticalStretch(0)
        sizePolicy.setHeightForWidth(self.sizePolicy().hasHeightForWidth())
        self.setSizePolicy(sizePolicy)
        self.setMinimumSize(QtCore.QSize(300, 0))
        self.setExpandsOnDoubleClick(False)
        self.setObjectName(_fromUtf8("arborescence"))
        self.clicked.connect(self.select)
        
    def currentChanged(self,current,previous):
        self._ihm_arbo.select(current)
        
    def select(self,model_index):
        pass
        