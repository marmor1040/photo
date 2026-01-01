# -*- coding: utf-8
"""
Created on 5 juin 2011

@author: Bureau
"""
from PyQt5 import QtWidgets,QtCore
# from PyQt5.QtWidgets import QDialogButtonBox
# from PyQt5.QtCore import QObject
import os.path as osp
# import glob
# from IhmPreferences import preferences
# #from IhmFiltre import FenetreFiltre
# import FenetreArborescence
from common import Photo
# #from PyQt5.uic import loadUiType
# #FormClass, BaseClass = loadUiType(osp.join(osp.dirname(osp.realpath(__file__)),
# #                                           '../Ihm/choix_selection.ui'))
# from choix_selection import Ui_ChoixSelection as FormClass
# from PyQt5.QtWidgets import QDialog as BaseClass

class dataCompression:
    def __init__(self,ihm):
        self.ihm = ihm
        self.album = None
        self.repertoire = None
        self.liste_photos = None
        self.liste_photos_compresse = None
        self.ihm.edtPrefixe.setText("comp_")
        self.ihm.bt_compression.setChecked(True)
        self.ihm.btValiderCompression.setEnabled(False)
        
    def setAlbum(self,alb):
        if alb and alb.estUnAlbum():
            self.album = alb
        else:
            self.album = None
            
    def majFenetre(self,alb):
        self.setAlbum(alb)
        self.majListe()
        
    def choixRepertoire(self):
        #print preferences.getRepertoireDefaut()[0]
        rep = QtWidgets.QFileDialog.getExistingDirectory(self.ihm,"Répertoire des images","",QtWidgets.QFileDialog.ShowDirsOnly)
        if rep:
            self.ihm.repertoire.setText(rep)
            self.repertoire = str(rep)
            #self.ihm.btValiderCompression.setEnabled(True)
    
    def sizeEstimee(self,taille):
        copie,reduc,qualite = self.ihm.bt_copie.isChecked(),self.ihm.sb_reduction.value(),self.ihm.sb_qualite.value()
        if copie:
            c = taille
        else:
            a = taille/pow(1.25,-1.73)
            b = a*pow(reduc,-1.73)
            c = b*pow(1+float(100-qualite)/10,-1.43)
        return size(c,"Mo")

    def majListe(self):
        self.liste_photos = []
        self.liste_photos_compresse = []
        if self.album:
            num=0
            self.liste_photos = self.album.listeJPG()
            if self.ihm.rb_toutes.isChecked():
                filtre_nom = str(self.ihm.edtFiltre.text())
                self.liste_photos_compresse = self.album.listeJPGFiltresNom(filtre_nom)
            elif self.ihm.rb_affichees.isChecked():
                self.liste_photos_compresse = self.album.listeJPGFiltres(self.ihm.getFiltre())
            elif self.ihm.rb_selection.isChecked():
                self.liste_photos_compresse = [self.album.repertoire() + f for f in self.ihm.getSelectedPhotos()]
        self.ihm.tableWidgetCompression.setRowCount(len(self.liste_photos))
        for f in self.liste_photos:
            self.ihm.tableWidgetCompression.setItem(num,0,QtWidgets.QTableWidgetItem(osp.basename(f)))
            self.ihm.tableWidgetCompression.setItem(num,1,QtWidgets.QTableWidgetItem(size(osp.getsize(f),"Mo")))
            if f in self.liste_photos_compresse:
                self.ihm.tableWidgetCompression.setItem(num,2,QtWidgets.QTableWidgetItem(self.sizeEstimee(osp.getsize(f))))
            else:
                self.ihm.tableWidgetCompression.setItem(num,2,QtWidgets.QTableWidgetItem(''))
            num+=1
        self.ihm.tableWidgetCompression.resizeColumnToContents(0)
        self.ihm.tableWidgetCompression.setColumnWidth(0,self.ihm.tableWidget.columnWidth(0)+30)
        self.ihm.btValiderCompression.setEnabled(bool(self.repertoire))
            
    def valider(self):
        print("valider")
        if self.repertoire:
            copie,reduc,qualite = self.ihm.bt_copie.isChecked(),self.ihm.sb_reduction.value(),self.ihm.sb_qualite.value()
            print(copie,reduc,qualite)
            pref = str(self.ihm.edtPrefixe.text())
            Photo.creerSelection(self.ihm,self.liste_photos_compresse,self.repertoire,pref,(copie,reduc,qualite))
        
# class FenetreSelection(BaseClass,FormClass):
#     def __init__(self,fen_thumbs,album):
#         BaseClass.__init__(self)
#         self.setupUi(self)
#         self._rep_cible = None
#         self._taille = 0
#         self._fenetre_thumbs = fen_thumbs
#         self._album = album
#         print album
#         self._liste_photos = album.listeJPG()
#         #self._liste_affichees = [album.repPhotos()+'/'+ph for ph in album.getListePhotos()]
#         self.initialiser()
#         self.afficheTaille()
#         
#     def initialiser(self):
#         QObject.connect(self.bt_repertoire,QtCore.SIGNAL("clicked()"),self.choixRepertoire)
#         QObject.connect(self.bt_filtre,QtCore.SIGNAL("clicked()"),self.choixFiltre)
#         QObject.connect(self.sb_reduction,QtCore.SIGNAL("valueChanged(int)"),self.afficheEstime)
#         QObject.connect(self.sb_qualite,QtCore.SIGNAL("valueChanged(int)"),self.afficheEstime)
#         QObject.connect(self.rb_toutes,QtCore.SIGNAL("toggled(bool)"),self.toutes)
#         QObject.connect(self.rb_affichees,QtCore.SIGNAL("toggled(bool)"),self.photosAffichees)
#         QObject.connect(self.rb_autres,QtCore.SIGNAL("toggled(bool)"),self.autres)
#         QObject.connect(self.bt_copie,QtCore.SIGNAL("toggled(bool)"),self.choixCopie)
#         QObject.connect(self.bt_compression,QtCore.SIGNAL("toggled(bool)"),self.choixCompression)
#         self.okcancel.button(QDialogButtonBox.Ok).setEnabled(False)
#         self.bt_copie.setChecked(True)
#         self.bt_filtre.setEnabled(False)
#         
#     def toutes(self,b):
#         if b:
#             self._liste_photos = self._album.listeJPG()
#             self.afficheTaille()
#         
#     def photosAffichees(self,b):
#         if b:
#             self._liste_photos = self._liste_affichees
#             self.afficheTaille()
#         
#     def autres(self,b):
#         self.bt_filtre.setEnabled(b)
#         self.afficheTaille()
#         
#     def afficheTaille(self):
#         self.nb_photos.setText(str(len(self._liste_photos))+' photos selectionn�es')
#         self._taille = self.taille_totale()
#         self.taille_init.setText(size(self._taille,'Mo')+' selectionn�s')
#         self.afficheEstime()
#         
#     def taille_totale(self):
#         tot = 0
#         for f in self._liste_photos:
#             tot += osp.getsize(f)
#         return tot
#     
#     def sizeEstimee(self,taille,options):
#         copie = options[0]
#         reduc = options[1]
#         qualite = options[2]
#         if copie:
#             c = taille
#         else:
#             a = taille/pow(1.25,-1.73)
#             b = a*pow(reduc,-1.73)
#             c = b*pow(1+float(100-qualite)/10,-1.43)
#         return c
#     
#     def afficheEstime(self):
#         t = self.sizeEstimee(self._taille,self.getOptions())
#         self.taille_finale.setText(size(t,'Mo')+' estim�s')
#         
#     def choixRepertoire(self):
#         #print preferences.getRepertoireDefaut()[0]
#         rep = QtWidgets.QFileDialog.getExistingDirectory(self,"Répertoire des images",
#                                                           "",#str(preferences.getRepertoireDefaut()[0]),    
#                                                           QtWidgets.QFileDialog.ShowDirsOnly)
#         if rep:
#             self.repertoire.setText(rep)
#             self._rep_cible = str(rep)
#             self.okcancel.button(QDialogButtonBox.Ok).setEnabled(True)
# 
#     def choixFiltre(self):
#         self._fenetre_filtre = FenetreArborescence.FenetreFiltre(self._fenetre_thumbs)
#         self._fenetre_filtre.justeFiltre()
#         ret = self._fenetre_filtre.retour()
#         if ret:
#             filtre = self._fenetre_filtre.getFiltre()
#             self._liste_photos = filtre.getPhotos()
#             self.afficheTaille()
#     
#     def choixCopie(self):
#         self.sb_reduction.setEnabled(False)
#         self.sb_qualite.setEnabled(False)
#         self.afficheTaille()
# 
#     def choixCompression(self):
#         self.sb_reduction.setEnabled(True)
#         self.sb_qualite.setEnabled(True)
#         self.afficheTaille()
# 
#     def getOptions(self):
#         return (self.bt_copie.isChecked(),self.sb_reduction.value(),self.sb_qualite.value())
# 
#     def accept(self):
#         Photo.creerSelection(self,self._liste_photos,self._rep_cible,self.getOptions())
#         self.hide()
# 
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
#     
# def creerSelection(liste_images,rep_cible,options):
#     import Image,os.path
#     qualite = 100
#     f = liste_images[3]
#     for reduc in [1,2,3,4,5,6,7,8,9,10]:
#         name = os.path.basename(f)
#         image = Image.open(f)
#         f_cible=rep_cible+'/reduc_'+str(reduc)+'_'+name
#         image = image.resize((int(image.size[0]/reduc),int(image.size[1]/reduc)))
#         image.save(f_cible,format="JPEG",quality=qualite)
#     reduc = 1
#     for qualite in [10,20,30,40,50,60,70,80,90,100]:
#         name = os.path.basename(f)
#         image = Image.open(f)
#         f_cible=rep_cible+'/qualite_'+str(qualite)+'_'+name
#         image = image.resize((int(image.size[0]/reduc),int(image.size[1]/reduc)))
#         image.save(f_cible,format="JPEG",quality=qualite)
#         
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