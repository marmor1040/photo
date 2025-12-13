# -*- coding: latin-1
"""
Created on 5 juin 2011

@author: Bureau
"""
from PyQt5 import QtWidgets,QtCore
from PyQt5.QtWidgets import QDialogButtonBox
from PyQt5.QtCore import QObject
import os.path as osp
import glob
from .IhmPreferences import preferences
#from IhmFiltre import FenetreFiltre
import FenetreArborescence
from common  import Photo
#from PyQt5.uic import loadUiType
#FormClass, BaseClass = loadUiType(osp.join(osp.dirname(osp.realpath(__file__)),
#                                           '../Ihm/choix_selection.ui'))
from Ihm.choix_selection import Ui_ChoixSelection as FormClass
from PyQt5.QtWidgets import QDialog as BaseClass

class FenetreSelection(BaseClass,FormClass):
    def __init__(self,fen_thumbs,ihm_arbo,album):
        BaseClass.__init__(self)
        self.setupUi(self)
        self.__rep_cible = None
        self.__taille = 0
        self.__fenetre_thumbs = fen_thumbs
        self.__ihm_arbo = ihm_arbo
        self.__album = album
        self.__liste_photos = album.listeJPG()
        #self.__liste_affichees = [album.repPhotos()+'/'+ph for ph in album.getListePhotos()]
        self.initialiser()
        self.afficheTaille()
        
    def initialiser(self):
        QObject.connect(self.bt_repertoire,QtCore.SIGNAL("clicked()"),self.choixRepertoire)
        QObject.connect(self.bt_filtre,QtCore.SIGNAL("clicked()"),self.choixFiltre)
        QObject.connect(self.sb_reduction,QtCore.SIGNAL("valueChanged(int)"),self.afficheEstime)
        QObject.connect(self.sb_qualite,QtCore.SIGNAL("valueChanged(int)"),self.afficheEstime)
        QObject.connect(self.rb_toutes,QtCore.SIGNAL("toggled(bool)"),self.toutes)
        QObject.connect(self.rb_affichees,QtCore.SIGNAL("toggled(bool)"),self.photosAffichees)
        QObject.connect(self.rb_autres,QtCore.SIGNAL("toggled(bool)"),self.autres)
        QObject.connect(self.bt_copie,QtCore.SIGNAL("toggled(bool)"),self.choixCopie)
        QObject.connect(self.bt_compression,QtCore.SIGNAL("toggled(bool)"),self.choixCompression)
        self.okcancel.button(QDialogButtonBox.Ok).setEnabled(False)
        self.bt_copie.setChecked(True)
        self.bt_filtre.setEnabled(False)
        
    def toutes(self,b):
        if b:
            self.__liste_photos = self.__album.listeJPG()
            self.afficheTaille()
        
    def photosAffichees(self,b):
        if b:
            self.__liste_photos = self.__fenetre_thumbs.getListeAffichees()
            self.afficheTaille()
        
    def autres(self,b):
        self.bt_filtre.setEnabled(b)
        self.afficheTaille()
        
    def afficheTaille(self):
        self.nb_photos.setText(str(len(self.__liste_photos))+' photos selectionn�es')
        self.__taille = self.taille_totale()
        self.taille_init.setText(size(self.__taille,'Mo')+' selectionn�s')
        self.afficheEstime()
        
    def taille_totale(self):
        tot = 0
        for f in self.__liste_photos:
            tot += osp.getsize(f)
        return tot
    
    def sizeEstimee(self,taille,options):
        copie = options[0]
        reduc = options[1]
        qualite = options[2]
        if copie:
            c = taille
        else:
            a = taille/pow(1.25,-1.73)
            b = a*pow(reduc,-1.73)
            c = b*pow(1+float(100-qualite)/10,-1.43)
        return c
    
    def afficheEstime(self):
        t = self.sizeEstimee(self.__taille,self.getOptions())
        self.taille_finale.setText(size(t,'Mo')+' estim�s')
        
    def choixRepertoire(self):
        #print preferences.getRepertoireDefaut()[0]
        rep = QtWidgets.QFileDialog.getExistingDirectory(self,"R�pertoire des images",
                                                          "",#str(preferences.getRepertoireDefaut()[0]),    
                                                          QtWidgets.QFileDialog.ShowDirsOnly)
        if rep:
            self.repertoire.setText(rep)
            self.__rep_cible = str(rep)
            self.okcancel.button(QDialogButtonBox.Ok).setEnabled(True)

    def choixFiltre(self):
        self.__fenetre_filtre = FenetreArborescence.FenetreFiltre(self.__fenetre_thumbs)
        self.__fenetre_filtre.justeFiltre()
        ret = self.__fenetre_filtre.retour()
        if ret:
            filtre = self.__fenetre_filtre.getFiltre()
            self.__liste_photos = filtre.getPhotos()
            self.afficheTaille()
    
    def choixCopie(self):
        self.sb_reduction.setEnabled(False)
        self.sb_qualite.setEnabled(False)
        self.afficheTaille()

    def choixCompression(self):
        self.sb_reduction.setEnabled(True)
        self.sb_qualite.setEnabled(True)
        self.afficheTaille()

    def getOptions(self):
        return (self.bt_copie.isChecked(),self.sb_reduction.value(),self.sb_qualite.value())

    def accept(self):
        Photo.creerSelection(self.__ihm_arbo,self.__liste_photos,self.__rep_cible,"select",self.getOptions())
        self.hide()

def size(val,dim="Ko"):
    if dim=="Go":
        ret='%.2f Go' % (float(int(val/107374182.4))/10)
    elif dim=="Mo":
        ret='%.2f Mo' % (float(int(val/104857.6))/10)
    elif dim=="Ko":
        ret='%.2f Ko' % (float(int(val/102.4))/10)
    else:
        ret=str(val)+" o"
    return ret
    
def creerSelection(liste_images,rep_cible,options):
    import Image,os.path
    qualite = 100
    f = liste_images[3]
    for reduc in [1,2,3,4,5,6,7,8,9,10]:
        name = os.path.basename(f)
        image = Image.open(f)
        f_cible=rep_cible+'/reduc_'+str(reduc)+'_'+name
        image = image.resize((int(image.size[0]/reduc),int(image.size[1]/reduc)))
        image.save(f_cible,format="JPEG",quality=qualite)
    reduc = 1
    for qualite in [10,20,30,40,50,60,70,80,90,100]:
        name = os.path.basename(f)
        image = Image.open(f)
        f_cible=rep_cible+'/qualite_'+str(qualite)+'_'+name
        image = image.resize((int(image.size[0]/reduc),int(image.size[1]/reduc)))
        image.save(f_cible,format="JPEG",quality=qualite)
        
#def choixSelection():
#    #Choix = QtWidgets.QDialog()
#    Choix = FenetreSelection(None)
#    Choix.show()
#    ret = Choix.exec_()
#    return None
#
#if __name__ == '__main__':
#    from PyQt5.QtWidgets import QApplication
#    app = QApplication([])
#    app.setStyle("plastique")
#    rep = choixSelection()
#    print rep