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
from FenetreVisionneuse.ThreadChargement import Charge as ChargePhoto
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
                    "F4 : cr�e les miniatures\n"+\
                    "F5 : chargement d'une s�lection\n"+\
                    "F6 : affiche le nom de la photo courante\n"+\
                    "<up> ou a : image pr�c�dente\n"+\
                    "<down> ou z : image suivante\n"+\
                    "<roue souris> : image pr�c�dente/suivante\n"+\
                    "<espace> : arr�t/reprise diaporama\n"

        self.photo_courante = None
        self.repertoire = None
        self.liste_photos = None
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
        self.affichage = Ecrans.Affichage(self,1,x0=100,y0=100,w0=500,h0=500)
        self.scrollThumbs = FenetreThumbVisionneuse(self)
        self.scrollThumbs.setPosition(self.affichage.w-200,self.affichage.h)
        self.threadChargement = ChargePhoto(bModeTri=False)
        self._occupe = False
        self.show()
    
    def initialiseEtAffiche(self,rep,photo):
        self.repertoire = rep
        self.threadChargement.initialise(self.repertoire)
        self.threadChargement.start()
        QApplication.setOverrideCursor(Qt.WaitCursor)
        QApplication.instance().processEvents()
        if not self.liste_photos:
            self.liste_photos = self.threadChargement.getListeFichiers()
            self.affichePhoto(photo)
            QApplication.instance().processEvents()
            self.scrollThumbs.creer(self.repertoire,self.liste_photos)
        QApplication.restoreOverrideCursor()
        
    def affichePhoto(self,nom_photo,bLoad=True):
        self.photo_courante = nom_photo
        if bLoad:
            self.pixmap = QPixmap.fromImage(self.threadChargement.get(nom_photo))
        taille = self.size()
        fen_larg,fen_haut = taille.width(),taille.height()
        pm_larg,pm_haut = self.pixmap.width(),self.pixmap.height()
        if fen_larg != 0 and fen_haut != 0 :
            pr = float(fen_larg)/float(fen_haut)
            ir = float(pm_larg)/float(pm_haut)
            if ir>pr :
                w = fen_larg
                h = int(fen_larg/ir)
                y = (fen_haut - h)/2
                x = 0
            else :
                h = fen_haut
                w = int(h*ir)
                x = (fen_larg - w)/2
                y = 0
            self.label.setPixmap(self.pixmap.scaled(w-2,h-2))
            self.label.setGeometry(x,y,w,h)
        else:
            print("image vide")
        QApplication.instance().processEvents()
        self.numero = self.liste_photos.index(nom_photo)
            
    def setNumero(self):
        self.numero = self.liste_photos.index(self.photo_courante)
        
    def keyPressEvent(self,event):
        #print 'clavier',event.key(),Qt.Key_Up,Qt.Key_Down
        touche = event.key()
        if touche == Qt.Key_F1:
            QtWidgets.QMessageBox.warning(self.window(),'Aide',self.aide)
        if touche == Qt.Key_F2:
            self._occupe = True
            self.affichage.pleinEcran()
            self.affichePhoto(self.photo_courante,bLoad=False)
            rect = self.geometry()
            self.scrollThumbs.setPosition(rect.width()-200,rect.height())
            self._occupe = False
        elif touche == Qt.Key_F3:
            self._occupe = True
            self.affichage.changeEcran()
            self.affichePhoto(self.photo_courante,bLoad=False)
            rect = self.geometry()
            self.scrollThumbs.setPosition(rect.width()-200,rect.height())
            self._occupe = False
        elif touche == Qt.Key_F4:
            self._occupe = True
            if not osp.isdir(self.repertoire+"/TriPhotos"):
                QApplication.setOverrideCursor(Qt.WaitCursor)
                self.album = Album.Album(self.repertoire,None,True)
                self.liste_photos = self.threadChargement.getListeFichiers()
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
                self.threadChargement.initialiseListeFichiers(self.liste_photos)
                self.scrollThumbs.creer(self.repertoire,self.liste_photos)
                self.affichePhoto(self.liste_photos[0])
            self._occupe = False
        elif touche == Qt.Key_F6:
            QtWidgets.QMessageBox.warning(self.window(),'Photo actuelle',self.liste_photos[self.numero])
        elif touche == Qt.Key_Up or touche == Qt.Key_A:
            self.numero -= 1
            self.affichePhoto(self.liste_photos[self.numero])
        elif touche == Qt.Key_Down or touche == Qt.Key_Z:
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
        self.numero += 1
        self.affichePhoto(self.liste_photos[self.numero])    

    def timerCursorEvent(self):
        self.setCursor(Qt.BlankCursor)
        
    def wheelEvent(self,event):
        #print self.numero
        if event.delta() > 0:
            if self.numero == 0: return
            self.numero -= 1
        else:
            if self.numero+1 == len(self.liste_photos): return
            self.numero += 1
        if self.numero >= 0 and self.numero < len(self.liste_photos):
            self.affichePhoto(self.liste_photos[self.numero])
            
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
      
    def resizeEvent(self,event):
        if not self._occupe:
            rect = self.geometry()
            self.affichePhoto(self.photo_courante,bLoad=False)
            self.affichage.resize(rect.x(),rect.y(),rect.width(),rect.height())
            self.scrollThumbs.setPosition(rect.width()-200,rect.height())
            self._occupe = False
        
    def moveEvent(self,event):
        if not self._occupe:
            self._occupe = True
            rect = self.geometry()
            self.affichage.resize(rect.x(),rect.y(),rect.width(),rect.height())
            self.scrollThumbs.setPosition(rect.width()-200,rect.height())
            self._occupe = False
        
    def quitter(self,rm=False):
        if self.miniatures_crees:
            rep = QMessageBox.question(None,"Warning","D�truire les miniatures ?",QMessageBox.Ok | QMessageBox.No)
            if rep == QMessageBox.Ok:
                shutil.rmtree(self.album.repTriPhotos())
        self.threadChargement.stop()
        self.window().close()
        
if __name__ == "__main__":
    import time
    print(sys.argv)
    if len(sys.argv) < 2:
        rep_photo,nom_photo = "C:/Users/marc/Documents/Dossiers personnel/Mes images/2020/2020-02_Birmanie/","Birmanie_0784_13-02-2020.JPG"
        rep_photo,nom_photo = "C:/Users/marc/Documents/Dossiers personnel/Mes images/EOS-77D/2020-06/","IMG_9813.JPG"
    else:
        rep_photo,nom_photo = osp.dirname(sys.argv[1]),osp.basename(sys.argv[1])
    print(rep_photo,nom_photo)
    app = QApplication([])
    app.setStyle("plastique")
    os.chdir("C:/Users/marc/Pictures/tirage 2025")
    print(os.getcwd())
    ihm = FenetrePhoto(None)
    ihm.initialiseEtAffiche(rep_photo,nom_photo)
    ret = app.exec_()
    sys.exit(ret)

        