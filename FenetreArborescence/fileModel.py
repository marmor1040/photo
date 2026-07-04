# -*- coding: utf-8
"""
Created on 5 juin 2011

@author: Bureau
"""
from PyQt5 import QtCore, QtWidgets
from PyQt5.QtCore import Qt
from PyQt5.QtWidgets import QFileSystemModel,QTreeView
from PyQt5.QtGui import QPixmap
from PyQt5.QtCore import pyqtSlot
import os.path as osp
import os
from common import scanRep
from src import preferences as PREFERENCES

class MyQFileSystemModel(QFileSystemModel):
    def __init__(self,tree_view):
        super(MyQFileSystemModel, self).__init__()
        self._tree_view = tree_view
        self._Folder = QPixmap(PREFERENCES.getIcon("folder.png")).scaled(25,20)
        self._Photo = QPixmap(PREFERENCES.getIcon("folderBleu.png")).scaled(25,20)
        self._Video = QPixmap(PREFERENCES.getIcon("folderBleu.png")).scaled(25,20)
        self._Album_photo = QPixmap(PREFERENCES.getIcon("FolderVideo.png")).scaled(25,20)
        self._Album_video = QPixmap(PREFERENCES.getIcon("FolderVideo.png")).scaled(25,20)
        self._Album_photo_trait = QPixmap(PREFERENCES.getIcon("AlbumPhotoTrait.png")).scaled(25,20)
        self._Album_video_trait = QPixmap(PREFERENCES.getIcon("AlbumVideoTrait.png")).scaled(25,20)
        self._Album_photo_ok = QPixmap(PREFERENCES.getIcon("AlbumPhotoOk.png")).scaled(25,20)
        self._Album_video_ok = QPixmap(PREFERENCES.getIcon("AlbumVideoOk.png")).scaled(25,20)
        self.setNameFilters(["*.jpg"])
        self.setNameFilterDisables(True)
        self.fileRenamed.connect(self.on_file_renamed)

    @pyqtSlot(str, str, str)
    def on_file_renamed(self, path, old_name, new_name):
        old_path = os.path.join(path, old_name)
        new_path = os.path.join(path, new_name)
        if osp.isdir(new_path):
            self._tree_view.updateSelection()

    def data(self,index,role):
        if role == Qt.DecorationRole:
            rep = str(self.filePath(index))
            if osp.isdir(rep):
                jpg = scanRep.first(rep,'.jpg')
                mp4 = scanRep.first(rep,'.mp4')
                tri = osp.isdir(rep+'/TriPhotos')
                trait = scanRep.first(rep+'/TriPhotos/Pano','.jpg') or \
                        scanRep.first(rep+'/TriPhotos/Recuperation','.jpg') or \
                        scanRep.first(rep+'/TriPhotos/Retouche','.jpg')
                ok = osp.isfile(rep+'/TriPhotos/Ok')
                if not jpg and not mp4:            return self._Folder
                elif jpg and not mp4 and not tri:  return self._Photo
                elif mp4 and not tri:              return self._Video
                elif jpg and not mp4 and tri:      return self._Album_photo
                elif mp4 and tri:                  return self._Album_video
                elif jpg and not mp4 and tri and trait:    return self._Album_photo_trait
                elif mp4 and tri and trait:                return self._Album_video_trait
                elif jpg and not mp4 and tri and ok:       return self._Album_photo_ok
                elif mp4 and tri and ok:                   return self._Album_video_ok
#                 if jpg:
# #                     ld = [d for d in os.listdir(rep) if os.path.isdir(rep+'/'+d)]
# #                     if "TriPhotos" in ld: ld.remove("TriPhotos")
# #                     if ld: return self._Album_attention
#                     if osp.isdir(rep+'/TriPhotos'):
#                         if scanRep.first(rep+'/TriPhotos/Pano','.JPG') or \
#                             scanRep.first(rep+'/TriPhotos/Recuperation','.JPG') or \
#                             scanRep.first(rep+'/TriPhotos/Retouche','.JPG'):
#                             return self._Album_nonVide
#                         else:
#                             return self._Album
#                     else:
#                         return self._Image
#                 else:
#                     mov = scanRep.first(rep,'.MOV')
#                     if mov:
#                         return self._Video
# #                     elif scanRep.first(rep):
# #                         return self._Normal    
#                     elif os.listdir(rep):
#                         return self._RepNormal
#                     else:
#                         return self._Vide
        return QFileSystemModel.data(self,index, role)
    
    def flags(self,index):
        return QFileSystemModel.flags(self,index) | Qt.ItemIsEditable
    
    
class MyTreeView(QTreeView):
    def __init__(self,ihm_arbo):
        super(MyTreeView, self).__init__(ihm_arbo.centralwidget)
        self._ihm_arbo = ihm_arbo
        self.current = None
        sizePolicy = QtWidgets.QSizePolicy(QtWidgets.QSizePolicy.Preferred, QtWidgets.QSizePolicy.Expanding)
        sizePolicy.setHorizontalStretch(0)
        sizePolicy.setVerticalStretch(0)
        sizePolicy.setHeightForWidth(self.sizePolicy().hasHeightForWidth())
        self.setSizePolicy(sizePolicy)
        self.setMinimumSize(QtCore.QSize(300, 0))
        self.setExpandsOnDoubleClick(False)
        self.setObjectName("arborescence")
        self.clicked.connect(self.select)
        
    def updateSelection(self):
        if self.current:
            self._ihm_arbo.select(self.current)

    def currentChanged(self,current,previous):
        self.current = current
        self._ihm_arbo.select(current)
        
    def fileRenamed(self,path,oldName,newName):
        print("renamed1:",path, oldName, "->", newName)

    def select(self,model_index):
        print("select MyTreeView")
        pass
        