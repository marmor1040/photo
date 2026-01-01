## -*- coding: utf-8 -*-
#"""
#Created on 5 juin 2011
#
#@author: Bureau
#"""
#
import time,sys,copy
from PyQt5 import QtCore,QtWidgets
from PyQt5.QtWidgets import QApplication,QDesktopWidget
from PyQt5.QtGui import QPixmap
from PyQt5.QtCore import Qt,QObject,pyqtSlot
try:
    from src import preferences as PREFERENCES
    from src import Ecrans
except:
    from ..src import preferences as PREFERENCES
    from ..src import Ecrans

from Ihm.fen_visionneuse import Ui_Visionneuse as FormClass
from PyQt5.QtWidgets import QWidget as BaseClass
from PyQt5 import QtWidgets

class FenetreVisionneuse(BaseClass,FormClass,QObject):
    def __init__(self,parent):
        BaseClass.__init__(self,parent)
        self.setupUi(self)
        self._num_ecran = 2
        self._liste_thumbs = None
        self._timer = None
        self._timer_wheel = None
#         self.mode_tri = bModeTri
        self._redraw = False
        self._miniature_aff = False
        self._filtre_aff = False
        self._num_wheel = 0
        self._quitter_ok = False
        self.obj_signal =  QObject(None)
        self.aide = "F1 : aide\n"+\
                    "F2 : bascule plein ecran / fenetre\n"+\
                    "F3 : bascule ecran 1 / ecran 2\n"+\
                    "<up> ou a : image précédente\n"+\
                    "<down> ou z : image suivante\n"+\
                    "<roue souris> : image précédente/suivante\n"+\
                    "<0> : note 0\n"+\
                    "<1> : note 1\n"+\
                    "<2> : note 2\n"+\
                    "<3> : note 3\n"
        self._gestion_ecrans = Ecrans.Affichage(self,1,x0=100,y0=100,kw=0.5,kh=0.5,plein_ecran=True,type_ihm=Ecrans.Affichage.VISIONNEUSE)
        self._gestion_ecrans.affiche()
#         self._miniature_aff = True
        #sender.value_changed.connect(self.affichePhoto)
        #self.show()
    
    def link(self,liste_thumbs):
        self._liste_thumbs = liste_thumbs

    def deplaceAutreEcran(self,o=None):
        if not o:o=self
        sg = QDesktopWidget().screenGeometry(1)
        if o.x() < sg.x():
            self.move(o.x()+sg.x(),o.y())
        else:
            self.move(o.x()-sg.x(),o.y())

    @pyqtSlot(str,str)
    def affichePhoto(self,nom=False,etoile=False):
        if nom:
            self.pixmap = QPixmap(nom)
            scaled = self.pixmap.scaled(self.label.size(),Qt.KeepAspectRatio,Qt.SmoothTransformation)
            self.label.setPixmap(scaled)
    
        #code de la visionneuse 2025
        # pm = QPixmap(nom)

        # taille = self.size()
        # p_larg = taille.width()
        # p_haut = taille.height()
        # if p_larg != 0 and p_haut != 0 :
        #     pr = float(p_larg)/float(p_haut)
        #     ir = float(pm.width())/float(pm.height())
        #     if ir>pr :
        #         w = p_larg
        #         h = int(p_larg/ir)
        #     else :
        #         h = p_haut
        #         w = int(h*ir)
        #     #self.label.setPixmap(pm.scaled(p_larg,p_haut,Qt.KeepAspectRatio,Qt.SmoothTransformation))
        #     self.label.setPixmap(pm.scaled(w,h))
        #     #self.label.setScaledContents(True)
        # else:
        #     print("image vide")
        if etoile: self.lbl_etoiles.setText(etoile)
        else: self.lbl_etoiles.setText("")
            
    def changeEcran(self):
        self._gestion_ecrans.changeEcran()

    def keyPressEvent(self,event):
        touche = event.key()
        if touche == Qt.Key_F1:
            QtWidgets.QMessageBox.warning(self.window(),'Aide',self.aide)
        if touche == Qt.Key_F2:
            self._gestion_ecrans.pleinEcran()
            self._gestion_ecrans.affiche()
        elif touche == Qt.Key_F3:
            self._gestion_ecrans.changeEcrans()
        elif touche == Qt.Key_Up or touche == PREFERENCES.PREC:
            self._liste_thumbs.selectPrevious()
        elif touche == Qt.Key_Down or touche == PREFERENCES.SUIV:
            self._liste_thumbs.selectNext()
        elif touche == PREFERENCES.ETOILE0:
            print("self._Pin.send('##0_Etoile##')")
        elif touche == PREFERENCES.ETOILE1:
            print("self._Pin.send('##1_Etoile##')")
        elif touche == PREFERENCES.ETOILE2:
            print("self._Pin.send('##2_Etoiles##')")
        elif touche == PREFERENCES.ETOILE3:
            print("self._Pin.send('##3_Etoiles##')")

    def wheelEvent(self,event):
        print('wheelEvent')
#        if self._timer_wheel:
#            self._num_wheel += 1
#            print self._num_wheel,'ajout'
#            sys.stdout.flush()
#        else:
#            print 'envoi',self._num_wheel
#            self._num_wheel = 0
#            self._timer_wheel = self.startTimer(1000)
#            self.killTimer(self._timer_wheel)
        # self._Pin.send(str(event.delta()))
        # if event.delta() > 0:
        #     self._Pin.send('##up##')
        # else:
        #     self._Pin.send('##down##')
            
    def mouseMoveEvent(self,event):
        print('mouseMoveEvent')
        #if self._redraw:
            #print '##redraw##'
            #sys.stdout.flush()
            #self._Pin.send('##redraw##')
            #self._redraw = False
#         if not self.mode_tri:
#             x = event.x()
#             xm = self.width()
#             y = event.y()
#             ym = self.height()
#             if x > xm * 0.8 and y < ym * 0.2:
#                 if not self._miniature_aff:
#                     self._Pin.send('##affiche_miniatures##')
#                     self._Pin.send(self._num_ecran)
#                     self._miniature_aff = True
#             else:
#                 self._Pin.send('##cache_miniatures##')
#                 self._miniature_aff = False
#             w,h = self._diaporama.x()+self._diaporama.width(),self._diaporama.y()+self._diaporama.height()
#             if y < h and x < w:
#                 self._diaporama.show()
#             else:
#                 self._diaporama.hide()
#             if x < xm * 0.2 and y > ym * 0.8:
#                 if not self._filtre_aff:
#                     self._Pin.send('##affiche_filtre##')
#                     self._Pin.send(self._num_ecran)
#                     self._filtre_aff = True
#             else:
#                 self._Pin.send('##cache_filtre##')
#                 self._filtre_aff = False
#         if self._timer:
#             self.killTimer(self._timer)
#             self.setCursor(Qt.ArrowCursor)
#         self._timer = self.startTimer(3000)
    
    def timerEvent(self,timer):
        self.setCursor(Qt.BlankCursor)
        
    def closeEvent(self,event):
        # fermeture de la fenetre visionneuse
        if self._timer:
            pass
            # erreur quand on tue le timer
            # voir si c'est utile en mode tri photo
            #print 'je tue le timer'
            #self.killTimer(self._timer)
        self.quitter()
      
    def resizeEvent(self,event):
        self._redraw = True
        rect = self.geometry()
        self.label.setGeometry(0,0,rect.width(),rect.height())
        self.affichePhoto()
        
    def avanceDiaporama(self):
        self._Pin.send('##down##')
        
    def quitter(self,rm=False):
        if not self._quitter_ok:
            #print 'fermer visio'
            self._quitter_ok = True
            self.window().close()
#        self._Pin.send('##quitter##')
#        self._Pin.send(rm)
#        self._Pout.send('##quitter##')
        
def monprint(*obj):
    if False:
        print(obj)
        sys.stdout.flush()

def getDesciptionImage(photo):
    ret = {}
    info = photo._getexif()
    for tag, value in list(info.items()):
        decoded = TAGS.get(tag, tag)
        if decoded in PREFERENCES.INFOS_PHOTO:
            ret[decoded] = value
    return ret

# def execute(Pout_mini,Pin_visio):
#     app = QApplication([])
#     app.setStyle("plastique")
#     thread_chargement = Charge()
#     thread_affichage = Affiche(thread_chargement,Pout_mini)
#     ihm = FenetreVisionneuse(None,thread_chargement,thread_affichage,Pin_visio,Pout_mini)
#     thread_chargement.start()
#     thread_affichage.start()
#     #ihm.show()
#     app.exec_()
        
# def start(Pout_mini,Pin_visio):
#     process = Process(target=execute,args=(Pout_mini,Pin_visio,))
#     process.start()
#     return process
    
# def stop(process):
#     time.sleep(3)
#     process.terminate()
#     #print 'terminate'
    
if __name__ == "__main__":
    app = QApplication([])
    app.setStyle("plastique")
    time.sleep(5)
    pip= Pin_mini
    print('go',pip)
    pip.send('##repertoire##./Photos/')
    print('go')
    pip.send('##photos##["nettoyage_mur_01.JPG","nettoyage_mur_02.JPG","nettoyage_mur_03.JPG"]')
    print('go')
    pip.send('##affiche##nettoyage_mur_01.JPG;False;False')
    print('1')
    time.sleep(5)
    pip.send('##affiche##nettoyage_mur_02.JPG;False;False')
    print('2')
    time.sleep(5)
    pip.send('##affiche##nettoyage_mur_03.JPG;False;False')
    print('3')
    time.sleep(5)
    pip.send('##quitter##')
