## -*- coding: utf-8 -*-
#"""
#Created on 5 juin 2011
#
#@author: Bureau
#"""
#
import sys,os,time,shutil
import os.path as osp
from PyQt5.QtWidgets import QApplication,QMessageBox,QFileDialog
from PyQt5.QtGui import QIcon,QPixmap
from PyQt5.QtCore import Qt,QTimer
from src import preferences as PREFERENCES
from src import Ecrans
from FenetreVisionneuse.ThumbVisionneuse import FenetreThumbVisionneuse
from src import Album

from Ihm.fen_visionneuse import Ui_Visionneuse as FormClass
from PyQt5.QtWidgets import QWidget as BaseClass
from PyQt5 import QtWidgets

class FenetrePhoto(BaseClass,FormClass):
    def __init__(self,parent):
        BaseClass.__init__(self,parent)
        self.setupUi(self)
        self.setWindowTitle("Visionneuse Photo")
        self.setWindowIcon(QIcon(PREFERENCES.getIcon('image.ico')))
        self.aide = "Esc : Quitter\n"+\
                    "F1 : aide\n"+\
                    "F2 : bascule plein ecran / fenetre\n"+\
                    "F3 : bascule ecran 1 / ecran 2\n"+\
                    "F4 : crée les miniatures\n"+\
                    "F5 : chargement d'une sélection\n"+\
                    "F6 : affiche le nom de la photo courante\n"+\
                    "F7 : change de répertoire\n"+\
                    "<up> ou a : image précédente\n"+\
                    "<down> ou z : image suivante\n"+\
                    "<roue souris> : image précédente/suivante\n"+\
                    "<espace> : arrêt/reprise diaporama\n"

        self.photo_courante = None
        self.repertoire = None
        self.liste_photos = None
        self.index_photo = None
        self.numero = None
        self.diaporama_en_cours = False
        self.__timer = None
        self.__timer_cursor = QTimer()
        self.__timer_cursor.setInterval(500)
        self.__timer_cursor.start()
        self.__timer_cursor.timeout.connect(self.timerCursorEvent)
        self._occupe = True
        self.pixmap = None
        self.album = None
        self.miniatures_crees = False
        self.scrollThumbs = FenetreThumbVisionneuse(self)
        self.affichage = Ecrans.Affichage(self,1,x0=100,y0=100,w0=500,h0=500,type_ihm=Ecrans.Affichage.VISIONNEUSE)
        self.scrollThumbs.setPosition(self.affichage.w-200,self.affichage.h)
        self._occupe = False
        self.show()
    
    def initialiseEtAffiche(self,rep,photo):
        if rep and osp.isdir(rep):
            self.repertoire = rep
            self.album = Album(self.repertoire,None)
            if not self.album.miniaturesOk():
                bcreer = QMessageBox.question(None,"Création des miniatures", "voulez-vous créer les miniatures pour cet album ?", QMessageBox.Ok | QMessageBox.Cancel)
                if bcreer == QMessageBox.Ok:
                    QApplication.setOverrideCursor(Qt.WaitCursor)
                    self.album.refresh()
                    QApplication.restoreOverrideCursor()
            self.liste_photos = self.album.listeJPG()
            self.index_photo = self.album.listeIndexJPG()
            QApplication.setOverrideCursor(Qt.WaitCursor)
            QApplication.instance().processEvents()
            if photo:
                self.affichePhoto(self.repertoire+'/'+photo)
            else:
                self.affichePhoto(self.liste_photos[0])
            QApplication.instance().processEvents()
            self.scrollThumbs.creer(self.album)
            QApplication.restoreOverrideCursor()
        
    def affichePhoto(self,nom_photo=False,etoile=False):
        if nom_photo or self.photo_courante:
            if not nom_photo:
                nom_photo = self.photo_courante
            else:
                self.photo_courante = nom_photo
            self.pixmap = QPixmap(nom_photo)
            scaled = self.pixmap.scaled(self.label.size(),Qt.KeepAspectRatio,Qt.SmoothTransformation)
            self.label.setPixmap(scaled)
            QApplication.instance().processEvents()
            self.numero = self.index_photo[nom_photo]
            
    def setNumero(self):
        self.numero = self.index_photo[self.photo_courante]
        
    def keyPressEvent(self,event):
        #print 'clavier',event.key(),Qt.Key_Up,Qt.Key_Down
        touche = event.key()
        if touche == Qt.Key_F1:
            QtWidgets.QMessageBox.warning(self.window(),'Aide',self.aide)
        if touche == Qt.Key_F2:
            self._occupe = True
            self.hide() #pour eviter le warning de QT
            self.affichage.pleinEcran()
            rect = self.geometry()
            self.scrollThumbs.setPosition(rect.width()-200,rect.height())
            self.show()
            self._occupe = False
        elif touche == Qt.Key_F3:
            self._occupe = True
            self.hide() #pour eviter le warning de QT
            self.affichage.changeEcran()
            rect = self.geometry()
            self.scrollThumbs.setPosition(rect.width()-200,rect.height())
            self.show()
            self._occupe = False
        elif touche == Qt.Key_F4:
            self._occupe = True
            if not osp.isdir(self.repertoire+"/TriPhotos"):
                QApplication.setOverrideCursor(Qt.WaitCursor)
                self.album = Album.Album(self.repertoire,None,True)
                self.scrollThumbs.creer(self.liste_photos)
                QApplication.restoreOverrideCursor()
                self.miniatures_crees = True
            self._occupe = False
        elif touche == Qt.Key_F5:
            self._occupe = True
            if not self.album: self.album = Album.Album(self.repertoire,None,True)
            fileName = QFileDialog.getOpenFileName(self,"Open Selection",self.album.repSelections(),"Selection (*.sel)")
            if fileName:
                self.liste_photos = self.album.lireSelection(fileName)
                self.scrollThumbs.creer(self.repertoire,self.liste_photos)
                self.affichePhoto(self.liste_photos[0])
            self._occupe = False
        elif touche == Qt.Key_F6:
            QtWidgets.QMessageBox.warning(self.window(),'Photo actuelle',self.liste_photos[self.numero])
        elif touche == Qt.Key_F7:
            rep_photo = QtWidgets.QFileDialog.getExistingDirectory(None,"Répertoire des images à visualiser","C:/Users/Marc/Pictures",QtWidgets.QFileDialog.ShowDirsOnly)
            self.initialiseEtAffiche(rep_photo,None)
        elif touche == Qt.Key_Up or touche == Qt.Key_A:
            if self.numero == 0: return
            self.numero -= 1
            self.affichePhoto(self.liste_photos[self.numero])
        elif touche == Qt.Key_Down or touche == Qt.Key_Z:
            if self.numero+1 == len(self.liste_photos): return
            self.numero += 1
            self.affichePhoto(self.liste_photos[self.numero])
        elif touche == Qt.Key_Space:
            if self.diaporama_en_cours:
                self.killTimer(self.__timer)
                self.__timer = None
                self.diaporama_en_cours = False
                self.setCursor(Qt.ArrowCursor)
            else:
                self.__timer = self.startTimer(2*1000)
                self.diaporama_en_cours = True
                self.setCursor(Qt.BlankCursor)
        elif touche == Qt.Key_Escape:
            self.close()
    
    def timerEvent(self,timer):
        if self.numero+1 == len(self.liste_photos): 
            self.killTimer(self.__timer)
            self.__timer = None
            self.diaporama_en_cours = False
            self.setCursor(Qt.ArrowCursor)
        else:
            self.numero += 1
            self.affichePhoto(self.liste_photos[self.numero])    

    def timerCursorEvent(self):
        self.setCursor(Qt.BlankCursor)
        
    def wheelEvent(self,event):
        # print(self.numero, event.angleDelta())
        if not self.scrollThumbs.estAffiche:
            if event.angleDelta().y() > 0:
                if self.numero == 0: return
                self.numero -= 1
            else:
                if self.numero+1 == len(self.liste_photos): return
                self.numero += 1
            if self.numero >= 0 and self.numero < len(self.liste_photos):
                self.affichePhoto(self.liste_photos[self.numero])
            
    def resizeEvent(self,event):
        self.__redraw = True
        rect = self.geometry()
        self.label.setGeometry(0,0,rect.width(),rect.height())
        self.scrollThumbs.setPosition(rect.width()-200,rect.height())
        self.affichePhoto()

    def mouseMoveEvent(self,event):
        self.setCursor(Qt.ArrowCursor)
        x = event.x()
        xm = self.width()
        y = event.y()
        ym = self.height()
        if x > xm * 0.8 and y < ym * 0.2:
            self.scrollThumbs.affiche(True)
            self.setCursor(Qt.ArrowCursor)
            self.__timer_cursor.stop()
        elif self.scrollThumbs.isVisible():
            self.scrollThumbs.affiche(False)
            self.__timer_cursor.start()
        
    def closeEvent(self,event):
        self.quitter()
      
    # def resizeEvent(self,event):
    #     if not self._occupe:
    #         rect = self.geometry()
    #         self.affichePhoto(self.photo_courante,bLoad=False)
    #         self.affichage.resize(rect.x(),rect.y(),rect.width(),rect.height())
    #         self.scrollThumbs.setPosition(rect.width()-200,rect.height())
    #         self._occupe = False
        
    def moveEvent(self,event):
        if not self._occupe:
            self._occupe = True
            rect = self.geometry()
            self.affichage.resize(rect.x(),rect.y(),rect.width(),rect.height())
            self.scrollThumbs.setPosition(rect.width()-200,rect.height())
            self._occupe = False
        
    def quitter(self,rm=False):
        if self.miniatures_crees:
            rep = QMessageBox.question(None,"Warning","Détruire les miniatures ?",QMessageBox.Ok | QMessageBox.No)
            if rep == QMessageBox.Ok:
                shutil.rmtree(self.album.repTriPhotos())
        self.window().close()
        
if __name__ == "__main__":
    import time
    app = QApplication([])
    if len(sys.argv) < 2:
        rep_photo = QtWidgets.QFileDialog.getExistingDirectory(None,"Répertoire des images à visualiser","C:/Users/Marc/Pictures",QtWidgets.QFileDialog.ShowDirsOnly)
        nom_photo = None
    else:
        rep_photo,nom_photo = osp.dirname(sys.argv[1]),osp.basename(sys.argv[1])
    print(rep_photo,nom_photo)
    app.setStyle("plastique")
    ihm = FenetrePhoto(None)
    ihm.initialiseEtAffiche(rep_photo,nom_photo)
    ret = app.exec_()
    sys.exit(ret)

        