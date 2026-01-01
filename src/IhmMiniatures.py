# -*- coding: utf-8
"""
Created on 3 juin 2011

@author: Bureau
"""

import os.path as osp
import os,glob,sys,time,copy,shutil
from PyQt5 import QtCore,QtWidgets
from PyQt5.QtCore import Qt,QObject,pyqtSlot
from PyQt5.QtWidgets import QDesktopWidget,QMessageBox,QInputDialog,QApplication
from .ListeThumbs import ListeThumbs
from .IhmPreferences import FenetrePreferences
from . import preferences as PREF
from .IhmInfos import FenetreInfos
#from IhmFiltre import FenetreFiltre
import FenetreArborescence
import FenetreVisionneuse
from FenetreVisionneuse.IhmVisionneuse import FenetreVisionneuse
from .IhmSelection import FenetreSelection
from .IhmDiaporama import FenetreDiaporama
from common import Photo
from . import Ecrans
#import Quitter
from .Album import Album

from Ihm.fen_miniatures import Ui_Miniatures as FormClass
from PyQt5.QtWidgets import QMainWindow as BaseClass

# class Attente(threading.Thread):
#     def  __init__(self,fenetre,pout):
#         self._fenetre = fenetre
#         self._pout = pout
#         self._continue = True
#         threading.Thread.__init__(self)
        
#     def run(self):
#         while self._continue:
#             nom = self._pout.recv()
#             if nom == '##down##':
#                 self._fenetre.avanceDiaporama()
#             elif nom == '##up##':
#                 self._fenetre.reculeDiaporama()
#             if nom == '##quitter##':
#                 #Le message quitter vient de la classe Quitter
#                 self._continue = False
#             if nom == '##0_Etoile##':
#                 #on ne peut appeler directement self._fenetre.setEtoiles car c'est un autre thread
#                 self._fenetre.obj_signal.emit(QtCore.SIGNAL("afficheEtoiles(int)"),0)
#             elif nom == '##1_Etoile##':
#                 #on ne peut appeler directement self._fenetre.setEtoiles car c'est un autre thread
#                 self._fenetre.obj_signal.emit(QtCore.SIGNAL("afficheEtoiles(int)"),1)
#             elif nom == '##2_Etoiles##':
#                 #on ne peut appeler directement self._fenetre.setEtoiles car c'est un autre thread
#                 self._fenetre.obj_signal.emit(QtCore.SIGNAL("afficheEtoiles(int)"),2)
#             elif nom == '##3_Etoiles##':
#                 #on ne peut appeler directement self._fenetre.setEtoiles car c'est un autre thread
#                 self._fenetre.obj_signal.emit(QtCore.SIGNAL("afficheEtoiles(int)"),3)
#             elif nom == '##change_ecran##':
#                 self._fenetre.changeEcran()
    
#    def quitter(self):
#        #Le message quitter vient de la fenetre de tri
#        print 'quitter Attente'
                
class FenetreThumbs(BaseClass,FormClass):
    def __init__(self):
        BaseClass.__init__(self)
        self.setupUi(self)
        self.obj_signal = QObject()
        self.initCallback()
        self.setFocusPolicy(Qt.TabFocus)
        PREF.setMode(PREF.MODE_TRI_SS_CAC)
        self._titre = None
        self._fenetre_infos = FenetreInfos(self)
        self._fenetre_arbo = None
        self._fenetre_selection = None
        self._fenetre_PREF = FenetrePreferences(self)
        self.selectionAcouper = None
        self.selectionAcopier = None
        self._quitter_ok = False
        self._filtre_obligatoire = False
        self._num_ecran = PREF.ECRAN_DEFAULT_MINIATURE
        self._album = None
        self._infos_sauvees = True
        self._largeur = PREF.LARGEUR_IMAGE + 40
        self._fenetre_photo = FenetreVisionneuse(None)        
        self._liste_thumbs = ListeThumbs(self,self._fenetre_photo)
        self._liste_thumbs_affichees = []
        self._nb_colonnes = 1
        self._fenetre_photo.link(self._liste_thumbs)        
        self._fenetre_arbo = FenetreArborescence.Ihm(self)
        self._gestion_ecrans = Ecrans.Affichage(self,2,x0=330,y0=30,kw=0.83,kh=1,type_ihm=Ecrans.Affichage.MINIATURES)
        self._gestion_ecrans.affiche()

    def changeEcran(self):
        self._gestion_ecrans.changeEcran()

    def resizeFenentre(self,num_ecran,x,y,w,h):
        self._gestion_ecrans.resize(num_ecran,x,y,w,h)
        
    def initCallback(self):
        #QObject.connect(self.actionChoisir_repertoire,QtCore.SIGNAL("triggered()"),self.choisirRepertoireFiltre)
        # Fichier
        self.actionQuitter.triggered.connect(self.quitter)
        # Selection
        self.actionNouvelleSelection.triggered.connect(self.nouvelleSelection)
        self.actionSauverSelection.triggered.connect(self.sauverSelection)
        self.actionChargerSelection.triggered.connect(self.chargerSelection)
        self.actionSauverSelectionSous.triggered.connect(self.sauverSelectionSous)
        self.actionDetruireSelection.triggered.connect(self.detruireSelection)
        self.actionGenererSelection.triggered.connect(self.genererSelection)
        # Infos
        self.actionModifierInfos.triggered.connect(self.modifierInfos)
        self.actionSauverInfos.triggered.connect(self.sauverInfos)
        self.actionDetectionAutomatique.triggered.connect(self.detectionAutomatique)
        # Photos
        self.actionDetruire.triggered.connect(self.detruirePhoto)
        self.actionRenommage_auto.triggered.connect(self.renommageAuto)
        # Panorama
        self.actionRenommer_panorama.triggered.connect(self.renommerPanorama)
        self.actionDeplacer_panorama.triggered.connect(self.deplacePanorama)
        self.actionCopier_retouche.triggered.connect(self.copieRetouche)
        # Aide
        self.actionAide.triggered.connect(self.aide)
        # Etoile depuis le thread visionneuse
        # en commentaire pendant la migration PyQt5 : TODO
        # self.obj_signal.afficheEtoiles.connect(self.setEtoiles)

    def quitter(self):
        self.hide()
        if self._album: self._album.sauveInfos()
        self._fenetre_photo.close()
        self.close()
        self._fenetre_arbo.close()
        
    def getListeAffichees(self):
        rep = self._album.repertoire()
        return [osp.join(rep,f) for f in self._liste_thumbs.getListePhotos()]
    
    def creerWidgetThumbs(self):
        self.images.parentWidget().setUpdatesEnabled(False)
        liste_noms_thumbs = self._liste_thumbs.getListePhotos()
        # nb = self.images.count()
        # for i in range(nb):
        #     tn = self.images.takeAt(0)
        #     if tn and tn.widget():
        #         w = tn.widget()
        #         self.images.removeWidget(w)
        #         w.deleteLater()
        #         w.repaint()
        self._liste_thumbs_affichees = []
        while self.images.count():
            item = self.images.takeAt(0)
            widget = item.widget()
            if widget is not None:
                widget.deleteLater()
        # cr�ation des nouveaux widgets
        nl,nc = 0,0
        self._nb_colonnes = self.width() // (PREF.LARGEUR_IMAGE+20)
        if len(self._liste_thumbs) > 0:
            ptr = self._liste_thumbs.getPtrPhoto(0)
            while ptr:
                self._liste_thumbs_affichees.append(ptr.value.getWidget())
                self.images.addWidget(ptr.value.getWidget(),nl,nc)
                nc += 1; 
                if nc >= self._nb_colonnes: 
                    nc = 0
                    nl += 1
                ptr = self._liste_thumbs.nextPtr(ptr)
        self._liste_thumbs.select(self._liste_thumbs.getFirst())
        self.images.parentWidget().setUpdatesEnabled(True)

        #self.afficheCommentaire()
       
    def rafraichirThumbs(self,min=None,max=None):
        if min and min < len(self._liste_thumbs):
            ptr = self._liste_thumbs.getPtrPhoto(min)
        else:
            min,ptr = 0,self._liste_thumbs.firstPtr()
        if max and max < len(self._liste_thumbs):
            ptr_max = self._liste_thumbs.getPtrPhoto(max)
        else:
            ptr_max = self._liste_thumbs.lastPtr()
        nc_max = PREF.nbColMiniatures()
        nl = min / nc_max
        nc = min - nl * nc_max
        ok = True
        while ptr and ok:
            self.images.addWidget(ptr.value.getWidget(),nl,nc)
            nc += 1; 
            if nc >= nc_max: 
                nc = 0
                nl += 1
            ok = ptr!= ptr_max
            ptr = self._liste_thumbs.nextPtr(ptr)
            QApplication.instance().processEvents()
    
    def reinitialise(self):
        #self._pipe_fenetre_photo.send('##reinitialise##')
        pass
        
    def filtreObligatoire(self,b):
        self._filtre_obligatoire = b
        
    def afficheCommentaire(self):
        if not self._liste_thumbs: return
        nb_tot = self._liste_thumbs.getNbPhotos()
        (nb_trait_tot,nb_trait_courant,nb_trait_aff) = self._liste_thumbs.getNbTraites()
        nb_aff = len(self._liste_thumbs)
        nb_infos_tot = self._liste_thumbs.getNbInfosTotaux()
        nb_infos_aff = self._liste_thumbs.getNbInfosAffiches()
        if isinstance(nb_trait_tot,int):
            delta = nb_trait_courant-nb_trait_tot
            com = 'Nb photos affichées (%i/%i)' % (nb_aff,nb_tot)
            com += ' -  Traitées (%i/%i)' % (nb_trait_aff+delta,nb_trait_courant)
            com += ' -  0* (%i/%i)' % (nb_infos_aff[0],nb_infos_tot[0])
            com += ' - 1* (%i/%i)' % (nb_infos_aff[1],nb_infos_tot[1])
            com += ' - 2* (%i/%i)' % (nb_infos_aff[2],nb_infos_tot[2])
            com += ' - 3* (%i/%i)' % (nb_infos_aff[3],nb_infos_tot[3])
            com += '  -  Panorama (%i/%i)' % (nb_infos_aff[4],nb_infos_tot[4])
            com += '  -  Retouche (%i/%i)' % (nb_infos_aff[5],nb_infos_tot[5])
            com += '  -  Autre (%i/%i)' % (nb_infos_aff[6],nb_infos_tot[6])
#            self.commentaire.setText('Total traitées : %i / %i' % (nb_trait_courant,nb_tot)\
#                                     +'  -  Affichées traitées : %i / %i' % (nb_trait_aff+delta,nb_aff)\
#                                     +'  -  Etoiles : 0(%i)  1*(%i)  2**(%i)  3***(%i)  -  Panorama : %i  -  Retouche : %i  -  Autre : %i' % tuple(nb_infos))
            self.commentaire.setText(com)
            
    def appliquerInfos(self,info,toutes):
        # applique le même info à toutes les miniatures
        self._liste_thumbs.appliquerInfos(info,toutes)
        self.majTitre()
        #self.afficheCommentaire()
    
    def getSelected(self):   
        return self._liste_thumbs.getSelected()
    
    def getSelectedPhotos(self):
        return self.getPhotos(copy.copy(self.getSelected()))

    def getPhotos(self,selection):
        return [self._liste_thumbs.getPhoto(num).getName() for num in selection]
    
    def resizeEvent(self,event):
        super().resizeEvent(event)
        nb_colonnes = self.width() // (PREF.LARGEUR_IMAGE+20)
        if nb_colonnes != self._nb_colonnes and self._liste_thumbs_affichees:
            self._nb_colonnes = nb_colonnes

            # nettoyage du layout
            while self.images.count():
                   self.images.takeAt(0)

            # désactiver les updates pour éviter le clignotement
            self.images.parentWidget().setUpdatesEnabled(False)
            liste_widget = enumerate(self._liste_thumbs_affichees)
            for i,w in liste_widget:
                self.images.addWidget(w, i // nb_colonnes, i % nb_colonnes)
            self.images.parentWidget().setUpdatesEnabled(True)


    def keyPressEvent(self,event):
        if PREF.PRINT_TOUCHE:
            print('clavier',event.key())
        touche = event.key()
        selection = self.getSelected()
        #print event.modifiers(),event.modifiers() == Qt.ControlModifier
        if touche == Qt.Key_F2:
            self._gestion_ecrans.pleinEcran()
            self._gestion_ecrans.affiche()
        elif touche == Qt.Key_F3:
            self._gestion_ecrans.changeEcrans()
        elif touche == PREF.ETOILE0:
            self.setEtoiles(0)
        elif touche == PREF.ETOILE1:
            self.setEtoiles(1)
        elif touche == PREF.ETOILE2:
            self.setEtoiles(2)
        elif touche == PREF.ETOILE3:
            self.setEtoiles(3)
        elif touche == PREF.NETTE:
            for courant in selection:
                courant.setNettete(not courant.getNettete())
        elif touche == PREF.NOM:
            for courant in selection:
                courant.setName(self.getNom())
        elif touche == Qt.Key_P and event.modifiers() == Qt.ControlModifier:
            for num_photo in self._liste_thumbs.getSelected():
                photo = self._liste_thumbs.getPtrPhoto(num_photo).value
                self._album.pivoterPhoto(photo)
                self._fenetre_photo.affichePhoto(self._album.getJPGPath(photo.getName()))
                self._liste_thumbs_affichees[num_photo]._thumb.pivoterImage()
                self.images.itemAt(num_photo).widget().update()
                QApplication.instance().processEvents()
        elif touche == Qt.Key_S and event.modifiers() == Qt.ControlModifier:
            self.sauverInfos()
        elif touche == Qt.Key_X and event.modifiers() == Qt.ControlModifier:
            self.selectionAcouper = copy.copy(selection)
            self.selectionAcopier = None
            self.majTitre()
        elif touche == Qt.Key_C and event.modifiers() == Qt.ControlModifier:
            self.selectionAcouper = None
            self.selectionAcopier = copy.copy(selection)
            self.majTitre()
        elif touche == Qt.Key_V and event.modifiers() == Qt.ControlModifier:
            selection = copy.copy(self._liste_thumbs.getFirstSelected())
            if not (self.selectionAcouper or self.selectionAcopier):
                return
            if selection in self.selectionAcouper:
                QMessageBox.warning(None,'Coller','La selection ne peut pas faire partie des images coup�es')
            else:
                self._liste_thumbs.unselectAll()  
                self._liste_thumbs.deplacer(self.selectionAcouper,selection)
                pmin = min(min(self.selectionAcouper),selection)
                pmax = max(max(self.selectionAcouper),selection)
                self.rafraichirThumbs(pmin,pmax)    
                    #self.infosModifiees()
            #self.afficheCommentaire()
            self.selectionAcouper = None
            self.selectionAcopier = None
            self.majTitre()
        if touche == Qt.Key_Down or touche == PREF.SUIV:
            self._liste_thumbs.selectNext()
        elif touche == Qt.Key_Up or touche == PREF.PREC:
            self._liste_thumbs.selectPrevious()

    @pyqtSlot(int)
    def setEtoiles(self,num):
        courant = self._liste_thumbs.getCurrent()
        courant.setEtoiles(num)
        courant.setTraite(True)
        self._liste_thumbs.selectNext()
        self.majTitre()
        #�self.infosModifiees()
        #self.afficheCommentaire()
        
    def majTitreInfosModifiees(self,b=True):
        if self._titre:
            if b:
                self.setWindowTitle(self._titre+' *')
            else:
                self.setWindowTitle(self._titre)
    
#     def infosModifiees(self,b=True):
#         if Rep.getInfos():
#             Rep.getInfos().setModifiees(b)
#         self.majTitreInfosModifiees(b)
        
    def majTitre(self):
        if self._album:
            self._titre = self._album.basename()
            if not self._album.infosSauvees():self._titre+="*"
            if self.selectionAcopier:
                s = "s" if len(self.selectionAcopier)>1 else ""
                self._titre+=f" -   {len(self.selectionAcopier)} image{s} copiée{s}"
            if self.selectionAcouper:
                s = "s" if len(self.selectionAcouper)>1 else ""
                self._titre+=f" -   {len(self.selectionAcouper)} image{s} coupée{s}"
            self.setWindowTitle(self._titre)
        
#     def choisirRepertoireFiltre(self):
#         # Callback modifier repertoire ou filtre
#         if self._liste_thumbs:
#             self._liste_thumbs.sauverInfos(False)
#         
#         if not self._fenetre_arbo:
#             self._fenetre_arbo = FenetreFiltre(self,Rep.repPhotos())
#         print "affichage"
#         ret = self._fenetre_arbo.retour()
#         if ret:
#             filtre = self._fenetre_arbo.getFiltre()
#             self.appliquerFiltre(filtre)
    
    def appliquerFiltre(self,album,filtre,ihm_arbo,tri_par_date):
        #self._pipe_fenetre_photo.send('##repertoire##'+album.repertoire())
        try:
            self._album = album
            self._liste_thumbs.chargeThumbs(album,filtre,ihm_arbo,tri_par_date)
            self.creerWidgetThumbs()
        except:
            print("Miniature : Erreur � la cr�ation des miniatures")
            import traceback
            traceback.print_exc()
        self.majTitre()
        #pour faire remonter la fenetre au premier plan
        self.hide()
        self.show()
            
    def creerMiniature(self,album=None):
        # recuperation des photos du repertoire Recuperation
        if album: 
            self.album = album
        #Photo.recuperationPhotos(self.album)
        nb_photos = len(self.album.listeJPG())
        nb_thumbs = len(self.album.listeJPGThumbs())
        if (nb_photos != nb_thumbs) or not osp.isfile(self.album.fichierExifs()):
            # cr�ation des miniatures
            Photo.creerMiniatures(self._fenetre_arbo,self.album)
            # cr�ation du fichier contenant les dates
            if osp.isfile(self.album.fichierDates()):
                os.remove(self.album.fichierDates())
        
    def getNom(self):
        return str(QtWidgets.QInputDialog.getText(self.parent(),'Renommage','Nom'))
        
    def preferences(self):
        self._fenetre_preferences.affiche()
        
#     def closeEvent(self,event):
#         #print 'close'
#         self.quitter()
#         
#     def quitter(self):
#         #callback
#         print self._quitter_ok
#         if not self._quitter_ok:
#             self._quitter_ok = True
#             if self._liste_thumbs and PREFERENCES.isModeTri():
#                 self._liste_thumbs.sauverInfos(False)
#             if self._fenetre_arbo:
#                 self._fenetre_arbo.hide()
#             self._pin_visio.send('##quitter##')
#             self._pipe_fenetre_photo.send('##quitter##')
#             while self._attente.isAlive():
#                 time.sleep(0.1)
#             #print 'attente alive',self._attente.isAlive()
#             self.window().close()
    
    def afficher(self,num_ecran):
        print("toto2")
        #afficherFenetre(self,num_ecran)
        self._gestion_ecrans.affiche()
        
    def afficherFiltre(self,num_ecran):
        if not self._filtre_obligatoire:
            afficherFenetre(self._fenetre_arbo,num_ecran)
                    
    def cacheFiltre(self):
        if not self._filtre_obligatoire:
            self._fenetre_arbo.hide()
                    
    def nouvelleSelection(self):
        self._liste_thumbs.sauverInfos(False)
        nom,ok = '',False
        mess = 'Nom :'
        while not ok:
            nom,nom_ok = QtWidgets.QInputDialog.getText(self,'Nouvelle selection',mess,QtWidgets.QLineEdit.Normal,'')
            if nom[-5:] != '.info': nom += '.info'
            ok = (not nom in Rep.listeSelections())
            mess = 'Nom existant !\nSaisir un autre Nom :'
        if nom_ok:
            Rep.setFichierInfos(str(nom))
            self.majTitre()
            Rep.lireInfos()
            self._liste_thumbs.rechargerInfos()
            self.afficheCommentaire()
            self.infosModifiees()

    def chargerSelection(self):
        lFich = QtWidgets.QFileDialog.getOpenFileNames(self,"Chargement d'une selection",Rep.repSelections(),"*.info")
        if lFich:
            chemin = str(lFich[0])
            nom = osp.basename(chemin)
            self._liste_thumbs.sauverInfos(False)
            Rep.setFichierInfos(nom)
            self.majTitre()
            Rep.getInfos().lire()
            self._liste_thumbs.rechargerInfos()
            self.afficheCommentaire()   
            self.infosModifiees(False)
        
    def sauverInfos(self):
        self._album.sauveInfos()
        self.majTitre()
#         self.infosModifiees(False)
#         self._liste_thumbs.sauverInfos()
        
    def sauverSelection(self):
        self.sauverSelectionSous()
    
    def sauverSelectionSous(self):
        fich = str(QtWidgets.QFileDialog.getSaveFileName(self,"Sauvegarde d'une selection\n toutes les photos affich�es seront dans la selection",self._album.repSelections(),"*.sel"))     
        if fich:
            self._album.sauveSelection(fich,self._liste_thumbs.getListePhotos())

    def detruireSelection(self):
        lFich = QtWidgets.QFileDialog.getOpenFileNames(self,"Destruction d'une selection",Rep.repSelections(),"*.info")   
        if lFich:
            os.remove(str(lFich[0]))

    def modifierInfos(self):
        self._fenetre_infos.affiche()     
        #self.infosModifiees()
        
    def genererSelection(self):
        self._fenetre_selection = FenetreSelection(self,self._fenetre_arbo,self._album)
        self._fenetre_selection.exec_()
        
    def fenetreDiaporama(self):
        FenetreDiaporama(None)
        
    def avanceDiaporama(self):
        self._liste_thumbs.selectNext()

    def reculeDiaporama(self):
        self._liste_thumbs.selectPrevious()
        
    def redraw(self):
        self._liste_thumbs.getCurrent().select(True)
        
    def renommerPanorama(self):
        num_pano,ok = QInputDialog.getInt(self, "Num�ro du panorama","Uniquement les photos selectionn�es seront renomm�es")
        if ok and len(self.getSelected()) > 1:
            selection = self.getSelected()
            for num in selection:
                th = self._liste_thumbs.getPhoto(num)
                th.setPano(True)
                th.setNomPano("pano_" + str(num_pano))
            
    def deplacePanorama(self):
        res = QtWidgets.QMessageBox.warning(self,"Panorama","Deplacer les panoramas dans le\nrépertoire Pano ?",
                                        QtWidgets.QMessageBox.Yes|QtWidgets.QMessageBox.Cancel)
        if res == QtWidgets.QMessageBox.Yes:
            self._liste_thumbs.deplacerPanorama()
            self._liste_thumbs.refresh()
            self.creerWidgetThumbs()
            
    def copieRetouche(self):
        res = QtWidgets.QMessageBox.warning(self,"Retouche","Copier les retouches dans le\nrépertoire Retouche ?",
                                        QtWidgets.QMessageBox.Yes|QtWidgets.QMessageBox.Cancel)
        if res == QtWidgets.QMessageBox.Yes:
            self._liste_thumbs.copieRetouche(self._album.repertoire(),self._album.repRetouche())
        
    def detectionAutomatique(self):
        self._liste_thumbs.detectionAutomatique()     
        self.majTitreInfosModifiees()
        
    def deplaceAutreEcran(self):
        ecran_1 = QDesktopWidget().screenGeometry(0)
        ecran_2 = QDesktopWidget().screenGeometry(1)
        #print ecran_1,ecran_2
        if self.x() < ecran_2.x():
            self.setGeometry(ecran_2.x()+ecran_2.width() - self._largeur-50,0,self._largeur,ecran_2.height())
        else:
            self.setGeometry(ecran_1.width() - self._largeur,0,self._largeur,ecran_1.height())
            
    def detruireMiniatures(self):
        GestionPhoto.detruireMiniatures(self._repertoire_thumbs)
        
    def detruirePhoto(self,force=False):
        if not force:
            ok = QMessageBox.question(self,'Destruction des photos','Les fichiers selectionnés seront définitivement détruits',QMessageBox.Ok |QMessageBox.Cancel)
        if force or ok == QMessageBox.Ok:
            selection = copy.copy(self.getSelected())
            #deselectionner les elements sinon on cherche � les deselectionner � la prochaine selection
            self._liste_thumbs.unselectAll()
            sl = list(selection)
            sl.sort()
            sl.reverse()
            lnames = []
            for p in sl:
                ptr = self._liste_thumbs.detruire(p)
                lnames.append(ptr.getName())
                ptr.getWidget().hide()
            #self.rafraichirThumbs(sl[-1])     
            #self.infosModifiees()
            #self.afficheCommentaire()
            # destruction des fichiers
            self._album.detruirePhotos(lnames)

    def renommageAuto(self):
        i=1
        for f in self._liste_thumbs.getListePhotos():
            nom = str(i)+".JPG"
            if not osp.isfile(self._album.repertoire()+"/"+nom):
                self._album.renommerPhoto(f,nom)
                i+=1
        self._liste_thumbs.refresh()
        self.creerWidgetThumbs()
        
    def aide(self):
        aide = "<up> ou a : photo pr�c�dente\n"+\
            "<down> ou z : photo suivante\n"+\
            "r : renommer\n"+\
            "n : nette\n"+\
            "Ctrl x : couper\n"+\
            "Ctrl v : coller\n"+\
            "Ctrl s : sauver\n"+\
            "<0> : note 0\n"+\
            "<1> : note 1\n"+\
            "<2> : note 2\n"+\
            "<2> : note 3\n"
        QtWidgets.QMessageBox.warning(self.window(),'Aide',aide)

def affichageProgressif(fenetre):
    try:
        if not fenetre.isVisible():
            fenetre.setWindowOpacity(0)
            fenetre.show()
            for i in range(21):
                j = float(i)
                fenetre.setWindowOpacity((j*j)/400)
    except:
        fenetre.setWindowOpacity(100)
        fenetre.show()  
    
def deplaceAutreEcran(fenetre):
    ecran_1 = QDesktopWidget().screenGeometry(0)
    ecran_2 = QDesktopWidget().screenGeometry(1)
    kw = float(ecran_2.width())/ecran_1.width()
    kh = float(ecran_2.height())/ecran_1.height()
    x,y,w,h = fenetre.x(),fenetre.y(),fenetre.width(),fenetre.height()
    if fenetre.x() < ecran_2.x():
        fenetre.move(ecran_2.x()+round(x*kw),round(y*kh))
        fenetre.resize(round(w*kw),round(h*kh))
    else:
        fenetre.move(round(float(x-ecran_2.x())/kw),round(float(y)/kh))
        fenetre.resize(round(float(w)/kw),round(float(h)/kh))
            
def afficherFenetre(fenetre,num_ecran):
    screen_geometry = QDesktopWidget().screenGeometry(num_ecran-1)
    print(screen_geometry)
    if not screen_geometry.contains(fenetre.pos()):
        deplaceAutreEcran(fenetre)
    affichageProgressif(fenetre)
    fenetre.activateWindow()
    fenetre.setFocus()
    
if __name__ == "__main__":
    app = QtWidgets.QApplication(sys.argv)
    app.setStyle("windows")
    window = QtWidgets.QMainWindow()
    from . import IhmInfos
    f=FenetreInfos(None)
    f.move(100,100)
    afficherFenetre(f,40,1)
    print(f.pos())
    afficherFenetre(f,40,2)
    print(f.pos())
    afficherFenetre(f,40,1)
    print(f.pos())
    sys.exit(app.exec_())
    