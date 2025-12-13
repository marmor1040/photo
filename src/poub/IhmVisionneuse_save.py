## -*- coding: latin-1
#"""
#Created on 5 juin 2011
#
#@author: Bureau
#"""
#
import time,sys,copy
from multiprocessing import Process, Pipe
import threading
from PyQt5.QtWidgets import QApplication,QDesktopWidget,QPainter
from PyQt5.QtGui import QIcon,QImage,QPixmap
from PyQt5.QtCore import QString,Qt,QPoint,QSize,QRect
from IhmPreferences import preferences
from IhmDiaporama import FenetreDiaporama
from IhmEtoiles import FenetreEtoiles

from fen_visionneuse import Ui_Visionneuse as FormClass
from PyQt5.QtWidgets import QWidget as BaseClass
from PyQt5 import QtWidgets
 
class FenetreVisionneuse(BaseClass,FormClass):    
    def __init__(self,parent,Pin,Pout,bModeTri):
        BaseClass.__init__(self,parent)
        self.setupUi(self)
        self.__plein_ecran = False
        self.__save_geometry = None
        self.__screen_geometry = QDesktopWidget().screenGeometry(0)
        self.__num_ecran = 1
        self.__Pin = Pin
        self.__Pout = Pout
        if not bModeTri:
            self.__diaporama = FenetreDiaporama(self)
        self.__timer = None
        self.__timer_wheel = None
        self.mode_tri = bModeTri
        self.__redraw = False
        self.__miniature_aff = False
        self.__filtre_aff = False
        self.__num_wheel = 0
        self.__quitter_ok = False
        
        rect = preferences.VISIONNEUSE_GEOMETRY
        self.move(rect.topLeft())
        self.resize(rect.size())
        self.aide = "F1 : aide\n"+\
                    "F2 : bascule plein ecran / fenetre\n"+\
                    "F3 : bascule ecran 1 / ecran 2\n"+\
                    "<up> ou a : image pr�c�dente\n"+\
                    "<down> ou z : image suivante\n"+\
                    "<roue souris> : image pr�c�dente/suivante\n"+\
                    "<espace> : arr�t/reprise diaporama\n"
        if bModeTri:
            self.aide += "<0> : note 0\n"+\
                         "<1> : note 1\n"+\
                         "<2> : note 2\n"+\
                         "<2> : note 3\n"
        #self.show()
        
    def keyPressEvent(self,event):
        #print 'clavier',event.key(),Qt.Key_Up,Qt.Key_Down
        touche = event.key()
        if touche == Qt.Key_F1:
            QtWidgets.QMessageBox.warning(self.window(),'Aide',self.aide)
        if touche == Qt.Key_F2:
            self.__plein_ecran = not self.__plein_ecran
            if self.__plein_ecran:
                self.__save_geometry = self.saveGeometry()
                self.setWindowFlags(Qt.FramelessWindowHint)
                self.move(self.__screen_geometry.topLeft())
                self.resize(self.__screen_geometry.size())
            else:
                self.setWindowFlags(Qt.Window)
                self.restoreGeometry(self.__save_geometry)
                if not self.__screen_geometry.contains(self.pos()):
                    self.deplaceAutreEcran()
            self.show()
        elif touche == Qt.Key_F3:
            if QDesktopWidget().numScreens() > 0:
                if self.__num_ecran == 1:
                    self.__num_ecran = 2
                else:
                    self.__num_ecran = 1
                self.__screen_geometry = QDesktopWidget().screenGeometry(self.__num_ecran-1)
                if self.__plein_ecran:
                    self.move(self.__screen_geometry.topLeft())
                    self.resize(self.__screen_geometry.size())
                else:
                    self.deplaceAutreEcran()
                self.show()
        elif touche == Qt.Key_Up or touche == preferences.PREC:
            self.__Pin.send('##up##')
        elif touche == Qt.Key_Down or touche == preferences.SUIV:
            self.__Pin.send('##down##')
        elif touche == preferences.ETOILE0:
            self.__Pin.send('##0_Etoile##')
        elif touche == preferences.ETOILE1:
            self.__Pin.send('##1_Etoile##')
        elif touche == preferences.ETOILE2:
            self.__Pin.send('##2_Etoiles##')
        elif touche == preferences.ETOILE3:
            self.__Pin.send('##3_Etoiles##')
        elif touche == Qt.Key_Space:
            self.__diaporama.go_stop()

    def deplaceAutreEcran(self,o=None):
        if not o:o=self
        sg = QDesktopWidget().screenGeometry(1)
        if o.x() < sg.x():
            self.move(o.x()+sg.x(),o.y())
        else:
            self.move(o.x()-sg.x(),o.y())
        
    def wheelEvent(self,event):
#        if self.__timer_wheel:
#            self.__num_wheel += 1
#            print self.__num_wheel,'ajout'
#            sys.stdout.flush()
#        else:
#            print 'envoi',self.__num_wheel
#            self.__num_wheel = 0
#            self.__timer_wheel = self.startTimer(1000)
#            self.killTimer(self.__timer_wheel)
        self.__Pin.send(str(event.delta()))
        if event.delta() > 0:
            self.__Pin.send('##up##')
        else:
            self.__Pin.send('##down##')
            
    def mouseMoveEvent(self,event):
        if self.__redraw:
            #print '##redraw##'
            #sys.stdout.flush()
            self.__Pin.send('##redraw##')
            self.__redraw = False
        if not self.mode_tri:
            x = event.x()
            xm = self.width()
            y = event.y()
            ym = self.height()
            if x > xm * 0.8 and y < ym * 0.2:
                if not self.__miniature_aff:
                    self.__Pin.send('##affiche_miniatures##')
                    self.__Pin.send(self.__num_ecran)
                    self.__miniature_aff = True
            else:
                self.__Pin.send('##cache_miniatures##')
                self.__miniature_aff = False
            w,h = self.__diaporama.x()+self.__diaporama.width(),self.__diaporama.y()+self.__diaporama.height()
            if y < h and x < w:
                self.__diaporama.show()
            else:
                self.__diaporama.hide()
            if x < xm * 0.2 and y > ym * 0.8:
                if not self.__filtre_aff:
                    self.__Pin.send('##affiche_filtre##')
                    self.__Pin.send(self.__num_ecran)
                    self.__filtre_aff = True
            else:
                self.__Pin.send('##cache_filtre##')
                self.__filtre_aff = False
        if self.__timer:
            self.killTimer(self.__timer)
            self.setCursor(Qt.ArrowCursor)
        self.__timer = self.startTimer(3000)
    
    def timerEvent(self,timer):
        self.setCursor(Qt.BlankCursor)
        
    def closeEvent(self,event):
        # fermeture de la fenetre visionneuse
        if self.__timer:
            pass
            # erreur quand on tue le timer
            # voir si c'est utile en mode tri photo
            #print 'je tue le timer'
            #self.killTimer(self.__timer)
        self.quitter()
      
    def resizeEvent(self,event):
        self.__redraw = True
        
    def avanceDiaporama(self):
        self.__Pin.send('##down##')
        
    def quitter(self,rm=False):
        if not self.__quitter_ok:
            #print 'fermer visio'
            self.__quitter_ok = True
            self.window().close()
#        self.__Pin.send('##quitter##')
#        self.__Pin.send(rm)
#        self.__Pout.send('##quitter##')
                
class ThreadPhoto(threading.Thread):
    courant = None
    nb = 0
    ht_pos = {}    
    rep_photos = None
    liste_fichiers = None
    charges = {}
    lock = threading.Lock()

    def __init__(self):
        threading.Thread.__init__(self)
        
    def reinit(self):
        self.courant = None
        self.nb = 0
        self.ht_pos = {}    
        self.rep_photos = None
        self.liste_fichiers = None
        self.charges = {}
    
    def get(self,nom):
        self.courant = ThreadPhoto.ht_pos[nom]
        if not self.contient(self.courant):
            self.charger(self.courant)
        ret = self.revoie(self.courant)
        return ret
    
    def decharger(self,l_num):
        self.locker()
        while len(l_num) > 0:
            ThreadPhoto.charges.pop(l_num.pop())
        self.delocker()
         
    def charger(self,num):
        self.locker()
        if num>-1 and num<ThreadPhoto.nb:
            f = ThreadPhoto.liste_fichiers[num]
            ThreadPhoto.charges[num] = QImage(QString(ThreadPhoto.rep_photos+'/'+f),'JPG')
            #image = Image.open(ThreadPhoto.rep_photos+'/'+f)
            #print getDesciptionImage(image)
            #sys.stdout.flush()
        self.delocker()
         
    def revoie(self,n):
        self.locker()
        ret = ThreadPhoto.charges[n]
        self.delocker()
        return ret
        
    def contient(self,n):
        self.locker()
        ret = n in ThreadPhoto.charges
        self.delocker()
        return ret
        
    def listeCharges(self):
        self.locker()
        charges = list(ThreadPhoto.charges.keys())
        self.delocker()
        return charges

    def locker(self):
        while ThreadPhoto.lock.locked():
            time.sleep(0.001)
        ThreadPhoto.lock.acquire()

    def delocker(self):
        ThreadPhoto.lock.release()
        
class Charge(ThreadPhoto):
    
    def __init__(self):
        ThreadPhoto.__init__(self)
        self.__cont = True
        self.__quitter_ok = False
        
    def initialise(self,fichiers):
        ThreadPhoto.liste_fichiers = fichiers
        ThreadPhoto.nb = len(ThreadPhoto.liste_fichiers)
        ThreadPhoto.liste_fichiers.sort()
        i=0
        ThreadPhoto.ht_pos = {}
        ThreadPhoto.charges = {}
        for f in ThreadPhoto.liste_fichiers:
            ThreadPhoto.ht_pos[f]=i
            i+=1
        self.courant = 0
        
    def clear(self):
        self.initialise([])
        
    def run(self):
        import traceback
        while self.__cont:
            try:
                charges = self.listeCharges()
                # monprint(charges)
                if type(self.courant) is int:
                    a_charger = preferences.AUTO_CHARGEMENT+self.courant
                    reste_a_charger = list(set(a_charger).difference(set(charges)))
                    if reste_a_charger:
                        # chargement
                        while len(reste_a_charger) > 0:
                            pos = reste_a_charger.pop(0)
                            if pos>-1 and pos<self.nb:
                                self.charger(pos)  
                    # dechargement
                    a_decharger = set(charges).difference(set(a_charger))
                    if a_decharger:
                        self.decharger(a_decharger)
            except:
                print(traceback.print_stack()))
                print('reinit charge')
                self.reinit()
            time.sleep(0.1)
        #print 'stop charge'
        self.__quitter_ok = True
        
    def stop(self):
        self.__cont = False
        while not self.__quitter_ok:
            time.sleep(0.01)
        
class Affiche(ThreadPhoto):
    def __init__(self,ihm,charge,Pout,bModeTri):
        ThreadPhoto.__init__(self)
        self.__ihm = ihm
        #self.__ihm.window().setWindowFlags(Qt.MSWindowsFixedSizeDialogHint)
        self.__charge = charge
        self.__pipe_out = Pout
        self.__tab={}
        self.__etoiles = None
        if bModeTri:
            self.__etoiles = FenetreEtoiles(ihm)
        
    def run(self):
        cont = True
        nom = None
        while cont:
            try:
                nom = self.__pipe_out.recv()
                if nom == '##quitter##':
                    self.__charge.stop()
                    cont = False
                    #if self.__ihm.isVisible():
                elif '##repertoire##' in nom:
                    rep = nom.replace('##repertoire##','')
                    # pour arreter le chargement auto des photos
                    self.__charge.courant = None
                    # changement du repertoire
                    ThreadPhoto.rep_photos = rep
                elif '##photos##' in nom:
                    liste = eval(nom.replace('##photos##',''))
                    # création de la liste des photos
                    if liste:
                        self.__charge.initialise(liste)
                elif '##geometrie##' in nom:
                    taille= eval(nom.replace('##geometrie##',''))
                    self.__ihm.setGeometry(taille)
                elif '##affiche##' in nom:
                    if ThreadPhoto.rep_photos:
                        nom,etoiles,traite = nom.replace('##affiche##','').split(';')
                        if self.__etoiles:
                            self.__etoiles.afficheEtoiles(etoiles,eval(traite))
                        if not self.__pipe_out.poll():
                            image = self.__charge.get(nom)
                            pix = QPixmap.fromImage(image)
                            self.affiche(pix)
                elif '##reinitialise##' in nom:
                    self.__ihm.label.clear()
                    self.__charge.clear()
            except:
                print('erreur', nom)
                while self.__pipe_out.poll():
                    print(self.__pipe_out.recv()
                print('sortie')
        #print 'stop affiche'
        self.__ihm.quitter()
    
    def affiche(self,pm):
        try:
            taille = self.__ihm.label.size()
            p_larg = taille.width()
            p_haut = taille.height()
            pr = float(p_larg)/float(p_haut)
            ir = float(pm.width())/float(pm.height())
            if ir>pr :
                w = p_larg
                h = int(p_larg/ir)
            else :
                h = p_haut
                w = int(h*ir)
            self.__ihm.label.setPixmap(pm.scaled(w-2,h-2))
        except:
            print('pb affiche')
        #p = QPainter(self.__ihm.label)
        #p.drawImage(0,0,pm)
        
def monprint(*obj):
    if False:
        print(obj)
        sys.stdout.flush()

def getDesciptionImage(photo):
    ret = {}
    info = photo._getexif()
    for tag, value in list(info.items()):
        decoded = TAGS.get(tag, tag)
        if decoded in preferences.INFOS_PHOTO:
            ret[decoded] = value
    return ret

def execute(Pout_mini,Pin_visio,bModeTri):
    app = QApplication([])
    app.setStyle("plastique")
    ihm = FenetreVisionneuse(None,Pin_visio,Pout_mini,bModeTri)
    ihm.show()
    thead_chargement = Charge()
    thead_chargement.start()
    thead_affichage = Affiche(ihm,thead_chargement,Pout_mini,bModeTri)
    thead_affichage.start()
    app.exec_()
        
def start(Pout_mini,Pin_visio,bModeTri):
    process = Process(target=execute,args=(Pout_mini,Pin_visio,bModeTri,))
    process.start()
    return process
    
def stop(process):
    time.sleep(3)
    process.terminate()
    #print 'terminate'
    
if __name__ == "__main__":
    app = QApplication([])
    app.setStyle("plastique")
    pipe_fen_photo = start()
    pipe_fen_photo.send('##repertoire##../photos/')
    pipe_fen_photo.send('Vietnam_20110426_0200.JPG')
    pipe_fen_photo.send('Vietnam_20110426_0201.JPG')
    pipe_fen_photo.send('Vietnam_20110426_0202.JPG')
    pipe_fen_photo.send('Vietnam_20110426_0203.JPG')
    pipe_fen_photo.send('##repertoire##../photos2/')
    pipe_fen_photo.send('comp_Cuba_(19_04_2010)_0656.JPG')
    pipe_fen_photo.send('comp_Cuba_(19_04_2010)_0657.JPG')
    pipe_fen_photo.send('comp_Cuba_(19_04_2010)_0658.JPG')
    pipe_fen_photo.send('##quitter##')