## -*- coding: utf-8 -*-
#"""
#Created on 5 juin 2011
#
#@author: Bureau
#"""
#
import time,sys,copy
import vlc
from PyQt5 import QtCore,QtWidgets
from PyQt5.QtWidgets import QApplication,QDesktopWidget,QSizePolicy

from PyQt5.QtGui import QPixmap
from PyQt5.QtCore import Qt,QObject,pyqtSlot
try:
    from src import preferences as PREFERENCES
    from src import Ecrans
except:
    from ..src import preferences as PREFERENCES
    from ..src import Ecrans

from PyQt5.QtWidgets import QWidget
from PyQt5 import QtWidgets

class VideoWidget(QWidget):
    current_rotation = 90
    def __init__(self):
        super().__init__()
        self.instance = vlc.Instance("--no-video-title-show", "--quiet")
        self.player = self.instance.media_player_new()

    def showEvent(self, event):
        self.player.set_hwnd(int(self.winId()))

    def newRotatedInstance(self,rotation_angle):
        self.current_rotation = rotation_angle
        self.player.stop()
        self.instance = vlc.Instance("--no-video-title-show", "--quiet","--video-filter=transform",f"--transform-type={rotation_angle}")
        self.player = self.instance.media_player_new()
        self.player.set_hwnd(int(self.winId()))

from PyQt5.QtWidgets import QWidget, QLabel, QStackedWidget, QVBoxLayout
from PyQt5.QtGui import QPixmap

class Viewer(QWidget):
    def __init__(self):
        super().__init__()

        self.setStyleSheet("background-color: black; color: white; border: none;")
        self.stack = QStackedWidget(self)
        self.image_label = QLabel()
        self.image_label.setAlignment(Qt.AlignCenter)
        self.image_label.setSizePolicy(QSizePolicy.Ignored,QSizePolicy.Ignored)
        self.image_label.setMinimumSize(0, 0)
        self.video_widget = VideoWidget()
        self.video_widget.setSizePolicy(QSizePolicy.Expanding,QSizePolicy.Expanding)
        self.video_widget.setMinimumSize(0, 0)
        self.stack.setMinimumSize(0, 0)
        self.setMinimumSize(0, 0)
        self.stack.addWidget(self.image_label)
        self.stack.addWidget(self.video_widget)
        layout = QVBoxLayout(self)
        layout.setContentsMargins(0,0,0,0)
        layout.addWidget(self.stack)
        # mouvement souris
        self.setMouseTracking(True)
        for child in self.findChildren(QWidget):
            child.setMouseTracking(True)

        self._photo_pixmap = None

    def _update_image_size(self):
        if self._photo_pixmap and self.stack.currentIndex() == 0:
            print("scaled3")
            scaled = self._photo_pixmap.scaled(
                self.image_label.size(),
                Qt.KeepAspectRatio,
                Qt.SmoothTransformation
            )
            self.image_label.setPixmap(scaled)

    
class FenetreVisionneuse(Viewer):
    def __init__(self,parent):
        super().__init__()
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
        self.aide = """F1 : aide
F2 : bascule plein ecran / fenetre
F3 : bascule ecran 1 / ecran 2
<up> ou a : image précédente
<down> ou z : image suivante
<roue souris> : image précédente/suivante
<0> : note 0
<1> : note 1
<2> : note 2
<3> : note 3"""
        self._gestion_ecrans = Ecrans.Affichage(self,2,x0=100,y0=100,kw=0.5,kh=0.5,plein_ecran=False,type_ihm=Ecrans.Affichage.VISIONNEUSE)
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
    def affichePhotoVideo(self,elem_album=False,etoile=False):
        from src.Album import PhotoAlbum,VideoAlbum
        if isinstance(elem_album,PhotoAlbum):
            self.video_widget.player.stop()
            self._photo_pixmap = QPixmap(elem_album.getPath())
            self.stack.setCurrentIndex(0)
            print("scaled4")
            scaled = self._photo_pixmap.scaled(self.image_label.size(),Qt.KeepAspectRatio,Qt.SmoothTransformation)
            self.image_label.setPixmap(scaled)
    
        elif isinstance(elem_album,VideoAlbum):
            print(self.video_widget.current_rotation,elem_album.getExif().get("pivoter","none"))
            if "pivoter" in elem_album.getExif() and elem_album.getExif()["pivoter"] != 0:
                rotation_angle = elem_album.getExif()["pivoter"]
                self.video_widget.newRotatedInstance(rotation_angle)
            elif self.video_widget.current_rotation != 90:
                self.video_widget.newRotatedInstance(90)
            media = self.video_widget.instance.media_new(elem_album.getPath())
            self.video_widget.player.set_media(media)
            self.stack.setCurrentIndex(1)
            self.video_widget.player.play()

        #if etoile: self.lbl_etoiles.setText(etoile)
        #else: self.lbl_etoiles.setText("")
    
    def stoperVideo(self):
        self.video_widget.player.stop()
        
    def changeEcran(self):
        self._gestion_ecrans.changeEcran()

    def keyPressEvent(self,event):
        touche = event.key()
        print('clavier',touche)
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
        if self._timer:
            self.killTimer(self._timer)
            self.setCursor(Qt.ArrowCursor)
        self._timer = self.startTimer(3000)
    
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
        super().resizeEvent(event)
        print('resizeEvent visionneuse')
        self._update_image_size()
        
    def avanceDiaporama(self):
        self._Pin.send('##down##')
        
    def quitter(self,rm=False):
        if not self._quitter_ok:
            self._quitter_ok = True
            self.window().close()
        
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
