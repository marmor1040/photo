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
from . import preferences as PREFERENCES
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
#         self.__fenetre = fenetre
#         self.__pout = pout
#         self.__continue = True
#         threading.Thread.__init__(self)
        
#     def run(self):
#         while self.__continue:
#             nom = self.__pout.recv()
#             if nom == '##down##':
#                 self.__fenetre.avanceDiaporama()
#             elif nom == '##up##':
#                 self.__fenetre.reculeDiaporama()
#             if nom == '##quitter##':
#                 #Le message quitter vient de la classe Quitter
#                 self.__continue = False
#             if nom == '##0_Etoile##':
#                 #on ne peut appeler directement self.__fenetre.setEtoiles car c'est un autre thread
#                 self.__fenetre.obj_signal.emit(QtCore.SIGNAL("afficheEtoiles(int)"),0)
#             elif nom == '##1_Etoile##':
#                 #on ne peut appeler directement self.__fenetre.setEtoiles car c'est un autre thread
#                 self.__fenetre.obj_signal.emit(QtCore.SIGNAL("afficheEtoiles(int)"),1)
#             elif nom == '##2_Etoiles##':
#                 #on ne peut appeler directement self.__fenetre.setEtoiles car c'est un autre thread
#                 self.__fenetre.obj_signal.emit(QtCore.SIGNAL("afficheEtoiles(int)"),2)
#             elif nom == '##3_Etoiles##':
#                 #on ne peut appeler directement self.__fenetre.setEtoiles car c'est un autre thread
#                 self.__fenetre.obj_signal.emit(QtCore.SIGNAL("afficheEtoiles(int)"),3)
#             elif nom == '##change_ecran##':
#                 self.__fenetre.changeEcran()
    
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
        self.__titre = None
        self.__fenetre_infos = FenetreInfos(self)
        self.__fenetre_arbo = None
        self.__fenetre_selection = None
        self.__fenetre_PREFERENCES = FenetrePreferences(self)
        self.__couper = None
        self.__quitter_ok = False
        self.__filtre_obligatoire = False
        self.__num_ecran = PREFERENCES.ECRAN_DEFAULT_MINIATURE
        self.__album = None
        self.__infos_sauvees = True
        self.__largeur = PREFERENCES.LARGEUR_IMAGE + 40 
        self.__fenetre_photo = FenetreVisionneuse(None)        
        self.__liste_thumbs = ListeThumbs(self,self.__fenetre_photo)    
        self.__fenetre_photo.link(self.__liste_thumbs)        
        self.__fenetre_arbo = FenetreArborescence.Ihm(self)
        self.__gestion_ecrans = Ecrans.Affichage(self,2,x0=330,y0=30,kw=0.83,kh=0.5,type_ihm=Ecrans.Affichage.MINIATURES)

        # ss thread

        self.__gestion_ecrans.affiche()
# 
        self.setGeometry(700,0,500,500)
        #self.show()
        
    def changeEcran(self):
        self.__gestion_ecrans.changeEcran()
        self.__fenetre_arbo.changeEcran()

    def resizeFenentre(self,num_ecran,x,y,w,h):
        self.__gestion_ecrans.resize(num_ecran,x,y,w,h)
        
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
        if self.__album: self.__album.sauveInfos()
        self.__fenetre_photo.close()
        self.close()
        self.__fenetre_arbo.close()
        
    def getListeAffichees(self):
        rep = self.__album.repertoire()
        return [osp.join(rep,f) for f in self.__liste_thumbs.getListePhotos()]
    
    def creerWidgetThumbs(self):
        liste_noms_thumbs = self.__liste_thumbs.getListePhotos()

        #☺self.__pipe_fenetre_photo.send('##photos##'+str(liste_noms_thumbs))
        #if len(self.__liste_thumbs) > 0:
        #    self.__liste_thumbs.getFirst().select(True)
        # destruction des widgets précédents
        nb = self.images.count()
        for i in range(nb):
            tn = self.images.takeAt(0)
            if tn and tn.widget():
                w = tn.widget()
                self.images.removeWidget(w)
                w.deleteLater()
                w.repaint()
                
        # cr�ation des nouveaux widgets
        nl,nc,nc_max = 0,0,PREFERENCES.nbColMiniatures()
        if len(self.__liste_thumbs) > 0:
            ptr = self.__liste_thumbs.getPtrPhoto(0)
            while ptr:
                self.images.addWidget(ptr.value.getWidget(),nl,nc)
                nc += 1; 
                if nc >= nc_max: 
                    nc = 0
                    nl += 1
                ptr = self.__liste_thumbs.nextPtr(ptr)
        self.__liste_thumbs.select(self.__liste_thumbs.getFirst())
        #self.afficheCommentaire()
       
    def rafraichirThumbs(self,min=None,max=None):
        if min and min < len(self.__liste_thumbs):
            ptr = self.__liste_thumbs.getPtrPhoto(min)
        else:
            min,ptr = 0,self.__liste_thumbs.firstPtr()
        if max and max < len(self.__liste_thumbs):
            ptr_max = self.__liste_thumbs.getPtrPhoto(max)
        else:
            ptr_max = self.__liste_thumbs.lastPtr()
        nc_max = PREFERENCES.nbColMiniatures()
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
            ptr = self.__liste_thumbs.nextPtr(ptr)
            QApplication.instance().processEvents()
    
    def reinitialise(self):
        #self.__pipe_fenetre_photo.send('##reinitialise##')
        pass
        
    def filtreObligatoire(self,b):
        self.__filtre_obligatoire = b
        
    def afficheCommentaire(self):
        if not self.__liste_thumbs: return
        nb_tot = self.__liste_thumbs.getNbPhotos()
        (nb_trait_tot,nb_trait_courant,nb_trait_aff) = self.__liste_thumbs.getNbTraites()
        nb_aff = len(self.__liste_thumbs)
        nb_infos_tot = self.__liste_thumbs.getNbInfosTotaux()
        nb_infos_aff = self.__liste_thumbs.getNbInfosAffiches()
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
        self.__liste_thumbs.appliquerInfos(info,toutes)
        self.majTitre()
        #self.afficheCommentaire()
    
    def getSelected(self):   
        return self.__liste_thumbs.getSelected()
    
    def getSelectedPhotos(self):
        selection = copy.copy(self.getSelected())
        lphotos = [self.__liste_thumbs.getPhoto(num).getName() for num in selection]
        return lphotos


    def keyPressEvent(self,event):
        if PREFERENCES.PRINT_TOUCHE:
            print('clavier',event.key())
        touche = event.key()
        selection = self.getSelected()
        #print event.modifiers(),event.modifiers() == Qt.ControlModifier
        if touche == Qt.Key_F2:
            self.__gestion_ecrans.pleinEcran()
            self.__gestion_ecrans.affiche()
        elif touche == PREFERENCES.ETOILE0:
            self.setEtoiles(0)
        elif touche == PREFERENCES.ETOILE1:
            self.setEtoiles(1)
        elif touche == PREFERENCES.ETOILE2:
            self.setEtoiles(2)
        elif touche == PREFERENCES.ETOILE3:
            self.setEtoiles(3)
        elif touche == PREFERENCES.NETTE:
            for courant in selection:
                courant.setNettete(not courant.getNettete())
        elif touche == PREFERENCES.NOM:
            for courant in selection:
                courant.setName(self.getNom())
        elif touche == Qt.Key_S and event.modifiers() == Qt.ControlModifier:
            self.sauverInfos()
        elif touche == Qt.Key_X and event.modifiers() == Qt.ControlModifier:
            self.__couper = copy.copy(selection)
        elif touche == Qt.Key_V and event.modifiers() == Qt.ControlModifier:
            selection = copy.copy(self.__liste_thumbs.getFirstSelected())
            if selection in self.__couper:
                QMessageBox.warning(None,'Coller','La selection ne pas pas faire partie des images coup�es')
            else:
                self.__liste_thumbs.unselectAll()  
                self.__liste_thumbs.deplacer(self.__couper,selection)
                pmin = min(min(self.__couper),selection)
                pmax = max(max(self.__couper),selection)
                self.rafraichirThumbs(pmin,pmax)    
                    #self.infosModifiees()
            #self.afficheCommentaire()
        if touche == Qt.Key_Down or touche == PREFERENCES.SUIV:
            self.__liste_thumbs.selectNext()
        elif touche == Qt.Key_Up or touche == PREFERENCES.PREC:
            self.__liste_thumbs.selectPrevious()

    @pyqtSlot(int)
    def setEtoiles(self,num):
        courant = self.__liste_thumbs.getCurrent()
        courant.setEtoiles(num)
        courant.setTraite(True)
        self.__liste_thumbs.selectNext()
        self.majTitre()
        #�self.infosModifiees()
        #self.afficheCommentaire()
        
    def majTitreInfosModifiees(self,b=True):
        if self.__titre:
            if b:
                self.setWindowTitle(self.__titre+' *')
            else:
                self.setWindowTitle(self.__titre)
    
#     def infosModifiees(self,b=True):
#         if Rep.getInfos():
#             Rep.getInfos().setModifiees(b)
#         self.majTitreInfosModifiees(b)
        
    def majTitre(self):
        self.__titre = self.__album.basename()
        if not self.__album.infosSauvees():self.__titre+="*"
        self.setWindowTitle(self.__titre)
        
#     def choisirRepertoireFiltre(self):
#         # Callback modifier repertoire ou filtre
#         if self.__liste_thumbs:
#             self.__liste_thumbs.sauverInfos(False)
#         
#         if not self.__fenetre_arbo:
#             self.__fenetre_arbo = FenetreFiltre(self,Rep.repPhotos())
#         print "affichage"
#         ret = self.__fenetre_arbo.retour()
#         if ret:
#             filtre = self.__fenetre_arbo.getFiltre()
#             self.appliquerFiltre(filtre)
    
    def appliquerFiltre(self,album,filtre,ihm_arbo,tri_par_date):
        #self.__pipe_fenetre_photo.send('##repertoire##'+album.repertoire())
        try:
            self.__album = album
            self.__liste_thumbs.chargeThumbs(album,filtre,ihm_arbo,tri_par_date)
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
            Photo.creerMiniatures(self.__fenetre_arbo,self.album)
            # cr�ation du fichier contenant les dates
            if osp.isfile(self.album.fichierDates()):
                os.remove(self.album.fichierDates())
        
    def getNom(self):
        return str(QtWidgets.QInputDialog.getText(self.parent(),'Renommage','Nom'))
        
    def preferences(self):
        self.__fenetre_preferences.affiche()
        
#     def closeEvent(self,event):
#         #print 'close'
#         self.quitter()
#         
#     def quitter(self):
#         #callback
#         print self.__quitter_ok
#         if not self.__quitter_ok:
#             self.__quitter_ok = True
#             if self.__liste_thumbs and PREFERENCES.isModeTri():
#                 self.__liste_thumbs.sauverInfos(False)
#             if self.__fenetre_arbo:
#                 self.__fenetre_arbo.hide()
#             self.__pin_visio.send('##quitter##')
#             self.__pipe_fenetre_photo.send('##quitter##')
#             while self.__attente.isAlive():
#                 time.sleep(0.1)
#             #print 'attente alive',self.__attente.isAlive()
#             self.window().close()
    
    def afficher(self,num_ecran):
        print("toto2")
        #afficherFenetre(self,num_ecran)
        self.__gestion_ecrans.affiche()
        
    def afficherFiltre(self,num_ecran):
        if not self.__filtre_obligatoire:
            afficherFenetre(self.__fenetre_arbo,num_ecran)
                    
    def cacheFiltre(self):
        if not self.__filtre_obligatoire:
            self.__fenetre_arbo.hide()
                    
    def nouvelleSelection(self):
        self.__liste_thumbs.sauverInfos(False)
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
            self.__liste_thumbs.rechargerInfos()
            self.afficheCommentaire()
            self.infosModifiees()

    def chargerSelection(self):
        lFich = QtWidgets.QFileDialog.getOpenFileNames(self,"Chargement d'une selection",Rep.repSelections(),"*.info")
        if lFich:
            chemin = str(lFich[0])
            nom = osp.basename(chemin)
            self.__liste_thumbs.sauverInfos(False)
            Rep.setFichierInfos(nom)
            self.majTitre()
            Rep.getInfos().lire()
            self.__liste_thumbs.rechargerInfos()
            self.afficheCommentaire()   
            self.infosModifiees(False)
        
    def sauverInfos(self):
        self.__album.sauveInfos()
        self.majTitre()
#         self.infosModifiees(False)
#         self.__liste_thumbs.sauverInfos()
        
    def sauverSelection(self):
        self.sauverSelectionSous()
    
    def sauverSelectionSous(self):
        fich = str(QtWidgets.QFileDialog.getSaveFileName(self,"Sauvegarde d'une selection\n toutes les photos affich�es seront dans la selection",self.__album.repSelections(),"*.sel"))     
        if fich:
            self.__album.sauveSelection(fich,self.__liste_thumbs.getListePhotos())

    def detruireSelection(self):
        lFich = QtWidgets.QFileDialog.getOpenFileNames(self,"Destruction d'une selection",Rep.repSelections(),"*.info")   
        if lFich:
            os.remove(str(lFich[0]))

    def modifierInfos(self):
        self.__fenetre_infos.affiche()     
        #self.infosModifiees()
        
    def genererSelection(self):
        self.__fenetre_selection = FenetreSelection(self,self.__fenetre_arbo,self.__album)
        self.__fenetre_selection.exec_()
        
    def fenetreDiaporama(self):
        FenetreDiaporama(None)
        
    def avanceDiaporama(self):
        self.__liste_thumbs.selectNext()

    def reculeDiaporama(self):
        self.__liste_thumbs.selectPrevious()
        
    def redraw(self):
        self.__liste_thumbs.getCurrent().select(True)
        
    def renommerPanorama(self):
        num_pano,ok = QInputDialog.getInt(self, "Num�ro du panorama","Uniquement les photos selectionn�es seront renomm�es")
        if ok and len(self.getSelected()) > 1:
            selection = self.getSelected()
            for num in selection:
                th = self.__liste_thumbs.getPhoto(num)
                th.setPano(True)
                th.setNomPano("pano_" + str(num_pano))
            
    def deplacePanorama(self):
        res = QtWidgets.QMessageBox.warning(self,"Panorama","Deplacer les panoramas dans le\nrépertoire Pano ?",
                                        QtWidgets.QMessageBox.Yes|QtWidgets.QMessageBox.Cancel)
        if res == QtWidgets.QMessageBox.Yes:
            self.__liste_thumbs.deplacerPanorama()
            self.__liste_thumbs.refresh()
            self.creerWidgetThumbs()
            
    def copieRetouche(self):
        res = QtWidgets.QMessageBox.warning(self,"Retouche","Copier les retouches dans le\nrépertoire Retouche ?",
                                        QtWidgets.QMessageBox.Yes|QtWidgets.QMessageBox.Cancel)
        if res == QtWidgets.QMessageBox.Yes:
            self.__liste_thumbs.copieRetouche(self.__album.repertoire(),self.__album.repRetouche())
        
    def detectionAutomatique(self):
        self.__liste_thumbs.detectionAutomatique()     
        self.majTitreInfosModifiees()
        
    def deplaceAutreEcran(self):
        ecran_1 = QDesktopWidget().screenGeometry(0)
        ecran_2 = QDesktopWidget().screenGeometry(1)
        #print ecran_1,ecran_2
        if self.x() < ecran_2.x():
            self.setGeometry(ecran_2.x()+ecran_2.width() - self.__largeur-50,0,self.__largeur,ecran_2.height())
        else:
            self.setGeometry(ecran_1.width() - self.__largeur,0,self.__largeur,ecran_1.height())
            
    def detruireMiniatures(self):
        GestionPhoto.detruireMiniatures(self.__repertoire_thumbs)
        
    def detruirePhoto(self,force=False):
        if not force:
            ok = QMessageBox.question(self,'Destruction des photos','Les fichiers selectionnés seront définitivement détruits',QMessageBox.Ok |QMessageBox.Cancel)
        if force or ok == QMessageBox.Ok:
            selection = copy.copy(self.getSelected())
            #deselectionner les elements sinon on cherche � les deselectionner � la prochaine selection
            self.__liste_thumbs.unselectAll()
            sl = list(selection)
            sl.sort()
            sl.reverse()
            lnames = []
            for p in sl:
                ptr = self.__liste_thumbs.detruire(p)
                lnames.append(ptr.getName())
                ptr.getWidget().hide()
            #self.rafraichirThumbs(sl[-1])     
            #self.infosModifiees()
            #self.afficheCommentaire()
            # destruction des fichiers
            self.__album.detruirePhotos(lnames)

    def renommageAuto(self):
        i=1
        for f in self.__liste_thumbs.getListePhotos():
            nom = str(i)+".JPG"
            if not osp.isfile(self.__album.repertoire()+"/"+nom):
                self.__album.renommerPhoto(f,nom)
                i+=1
        self.__liste_thumbs.refresh()
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
    