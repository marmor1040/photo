# -*- coding: latin-1
'''
Created on 26 f�vr. 2020

@author: marc
'''
from PyQt5.QtWidgets import QDesktopWidget
from PyQt5.QtCore import  Qt

class Affichage:
    
    nb_ecran = None
    ecrans = None
    
    def __init__(self,ihm,num_ecran,x0=0,y0=0,w0=100,h0=100,kw=None,kh=None,plein_ecran=False):
        if not Affichage.nb_ecran:
            Affichage.nb_ecran = QDesktopWidget().numScreens()
            Affichage.ecrans = [QDesktopWidget().screenGeometry(0)]
            if Affichage.nb_ecran > 1:
                Affichage.ecrans.append(QDesktopWidget().screenGeometry(1))
        self.ihm = ihm
        self.num_ecran = num_ecran
        self.kw = kw
        self.kh = kh
        taille_ecran = self.getTailleEcran()
        self.x = x0 + taille_ecran[0]
        self.y = y0 + taille_ecran[1]
        self.w = w0
        self.h = h0
        self.plein_ecran = plein_ecran
        self.affiche()
        self.ihm.show()
        
#     def charger(self,):
#         import pickle
#         with open(self.fichier,"rb") as f:
#             self.kw = pickle.load(f)
#             self.kh = pickle.load(f)
#             self.x = pickle.load(f)
#             self.y = pickle.load(f)
#             self.w = pickle.load(f)
#             self.h = pickle.load(f)
#             self.plein_ecran = pickle.load(f)
#         
#     def sauver(self):
#         import pickle
#         with open(self.fichier,"wb") as f:
#             print self.kw,self.kh,self.x,self.y,self.w,self.h,self.plein_ecran
#             pickle.dump(self.kw,f)
#             pickle.dump(self.kh,f)
#             pickle.dump(self.x,f)
#             pickle.dump(self.y,f)
#             pickle.dump(self.w,f)
#             pickle.dump(self.h,f)
#             pickle.dump(self.plein_ecran,f)            
            
    def numEcran(self):
        if Affichage.nb_ecran > 1:
            return self.num_ecran-1
        else:
            return 1
        
    def getTailleEcran(self):
        try:
            return list(Affichage.ecrans[self.numEcran()].getRect())
        except:
            return list(Affichage.ecrans[0].getRect())
            
    def affiche(self):
        taille_ecran = self.getTailleEcran()
        if self.plein_ecran:
            self.ihm.setGeometry(*taille_ecran)
            self.ihm.setWindowState(Qt.WindowFullScreen)
        else:
            self.ihm.setWindowState(Qt.WindowNoState)
            if self.kw:
                self.w = taille_ecran[2] * self.kw
            if self.kh:
                self.h = taille_ecran[3] * self.kh
            self.ihm.setGeometry(self.x,self.y,self.w,self.h)
    
    def resize(self,x,y,w,h):
        self.x,self.y,self.w,self.h = x,y,w,h
        
    def changeEcran(self):
        if Affichage.nb_ecran > 1:
            taille_ecran = Affichage.ecrans[self.numEcran()].getRect()
            x = self.x - taille_ecran[0]
            y = self.y - taille_ecran[1]
            self.num_ecran = 1 + self.num_ecran % 2
            taille_ecran = Affichage.ecrans[self.numEcran()].getRect()
            self.x = x + taille_ecran[0]
            self.y = y + taille_ecran[1]
            self.affiche()
            return True
        return False
    
    def pleinEcran(self):
        from PyQt5.QtCore import Qt
        self.plein_ecran = not self.plein_ecran
        self.affiche()
        
class AffichageMiniature(Affichage):
    def __init__(self,ihm,num_ecran):
        Affichage.__init__(self,ihm,num_ecran)
        
        
if __name__ == "__main__":
    from PyQt5.QtWidgets import QWidget,QApplication
    from miniature_visionneuse import Ui_Form
    app = QApplication([])
    app.setStyle("plastique")
    Form = QWidget()
    ui = Ui_Form()
    ui.setupUi(Form)
    aff = Affichage(Form,1,x0=100,y0=100,w0=500,h0=500)
    print("init",aff.x,aff.y,aff.w,aff.h)
    aff.changeEcran()
    print("24p",aff.x,aff.y,aff.w,aff.h)
    aff.pleinEcran()
    print("plein ecran",aff.x,aff.y,aff.w,aff.h)
    aff.changeEcran()
    print("17p",aff.x,aff.y,aff.w,aff.h)
    aff.pleinEcran()
    print("petiet",aff.x,aff.y,aff.w,aff.h)
    Form.show()
    app.exec_()