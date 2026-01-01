# -*- coding: utf-8
"""
Created on 5 juin 2011

@author: Bureau
"""
import glob,os,math,shutil,sys,pickle
from PyQt5 import QtCore,QtWidgets,QtGui
from PyQt5.QtCore import Qt,QObject
from PyQt5.QtWidgets import QDesktopWidget,QMessageBox,QApplication
from PyQt5.QtGui import QIcon,QImage,QPixmap
import os.path as osp
from src import preferences as PREFERENCES
from common import scanRep
from src.Album import Album
from .fileModel import MyQFileSystemModel,MyTreeView
from .filtre import Filtre
from . import renommage
from FenetreArborescence import compression
from src import Ecrans
from Ihm.fen_arborescence import Ui_Arborescence as FormClass
from PyQt5.QtWidgets import QMainWindow as BaseClass
    
class Ihm(BaseClass,FormClass):
    __fenetre_thumbs = None
    __rep_deplacement = None
    __nom_deplacement = ""
    def __init__(self,parent):
        BaseClass.__init__(self, None)
        self.setupUi(self)
        Ihm.__fenetre_thumbs = parent
        self._album_selectionne = None
        self._album_affiche = None
        self._retour = None
        self._busy = False
        self._progress_stoppe = False
        self._aide = None
        self._renommage = renommage.dataRenommage(self)
        self._compression = compression.dataCompression(self)
        self._cursor = self.cursor()
        self._ctrl_x = None
        self._rep_a_copier = None
        self._rep_a_couper = None
        self.actionQuitter.triggered.connect(self.quitter)
        self.cb_toutes.toggled.connect(self.choixToutes)
        self.gb_infos.toggled.connect(self.choixDetails)
        self.gb_dates.toggled.connect(self.choixDetails)
        self.gb_nums.toggled.connect(self.choixDetails)
        self.btAfficher.clicked.connect(self.afficher)
        self.btAddWorkspace.clicked.connect(self.addWorkspace)
        self.btRetirerWorkspace.clicked.connect(self.retirerWorkspace)
        self.comboWorkspace.currentIndexChanged.connect(self.modifierChoixWorkspace)
        self.btRecreerMiniatures.clicked.connect(self.recreerMiniatures)
        self.btDetruireTriPhotos.clicked.connect(self.detruireTriPhotos)
        self.bt_annuler_progress.clicked.connect(self.annulerProgress)
        self.tabWidget.currentChanged.connect(self.tabChanged)
        # gestion repertoires
        self.btCreerRepertoire.clicked.connect(self.creerRepertoire)
        self.btViderRepertoire.clicked.connect(self.viderRepertoire)
        # renommage
        self.btDetruire.clicked.connect(self.detruireFichiers)
        self.btRefresh.clicked.connect(self.refreshRenommage)
        self.btTester.clicked.connect(self.testerRenommage)
        self.btValider.clicked.connect(self.validerRenommage)
        self.btAide.clicked.connect(self.aideRenommage)
        self.btAuto.clicked.connect(self.autoRenommage)
        # compression
        self.bt_repertoire.clicked.connect(self.repertoireCompression)
        #QObject.connect(self.bt_filtre,QtCore.SIGNAL("clicked()"),self.choixFiltre)
        self.sb_reduction.valueChanged.connect(self.afficheCompressionEstime)
        self.sb_qualite.valueChanged.connect(self.afficheCompressionEstime)
        self.rb_toutes.toggled.connect(self.compressionToutes)
        self.rb_affichees.toggled.connect(self.compressionAffichees)
        self.rb_selection.toggled.connect(self.compressionSelection)
        self.bt_copie.toggled.connect(self.afficheCompressionEstime)
        self.bt_compression.toggled.connect(self.afficheCompressionEstime)
        self.btValiderCompression.clicked.connect(self.validerCompression)
        self.btAfficherCompression.clicked.connect(self.afficherCompression)
        # icon
        self.btRefresh.setStyleSheet("QPushButton{background: transparent;}")
        self.btRefresh.setIcon(QIcon(PREFERENCES.getIcon('refresh.png')))
        self.btAide.setStyleSheet("QPushButton{background: transparent;}")
        self.btAide.setIcon(QIcon(PREFERENCES.getIcon('help.png')))
        self.btRetirerWorkspace.setStyleSheet("QPushButton{background: transparent;}")
        self.btRetirerWorkspace.setIcon(QIcon(PREFERENCES.getIcon('interdit.png')))
        self.icon1.setStyleSheet("QPushButton{background: transparent;}")
        self.icon2.setStyleSheet("QPushButton{background: transparent;}")
        self.icon3.setStyleSheet("QPushButton{background: transparent;}")
        self.icon4.setStyleSheet("QPushButton{background: transparent;}")
        self.icon5.setStyleSheet("QPushButton{background: transparent;}")
        self.icon6.setStyleSheet("QPushButton{background: transparent;}")
        self.icon7.setStyleSheet("QPushButton{background: transparent;}")
        self.icon1.setPixmap(QtGui.QPixmap(PREFERENCES.getIcon('vide.png')))
        self.icon2.setPixmap(QtGui.QPixmap(PREFERENCES.getIcon('repImage.png')))
        self.icon3.setPixmap(QtGui.QPixmap(PREFERENCES.getIcon('repVideo.png')))
        self.icon4.setPixmap(QtGui.QPixmap(PREFERENCES.getIcon('album.png')))
        self.icon5.setPixmap(QtGui.QPixmap(PREFERENCES.getIcon('album-attention.png')))
        self.icon6.setPixmap(QtGui.QPixmap(PREFERENCES.getIcon('album-non-vide.png')))
        self.icon7.setPixmap(QtGui.QPixmap(PREFERENCES.getIcon('album-non-vide.png')))
        
        self.arborescence = MyTreeView(self)
        self.verticalLayoutArbo.insertWidget(0,self.arborescence)
        self.setFileModel()
        self.arborescence.setColumnHidden(1,True)
        self.arborescence.setColumnHidden(2,True)
        self.arborescence.setColumnHidden(3,True)
        self.progressBar.hide()
        self.bt_annuler_progress.hide()
        self.fichier_progress.hide()
        self._gestion_ecrans = Ecrans.Affichage(self,2,x0=0,y0=30,w0=300,kh=0.8,type_ihm=Ecrans.Affichage.ARBO)
        self._selection = None
        #self._num_ecran = PREFERENCES.ECRAN_DEFAULT_ARBO
        self.comboWorkspace.addItems(PREFERENCES.getWorkspaces())
        self._gestion_ecrans.affiche()
        self.majIhmSelection()
        self.show()
    
    def changeEcran(self):
        self._gestion_ecrans.changeEcran()
        
    def setFileModel(self):
        self.fileModel = MyQFileSystemModel()
        self.arborescence.setModel(self.fileModel)
        self._workspace = self.workspaceCourant()
        if self._workspace:
            PREFERENCES.addWorkspace(self._workspace)
            self.fileModel.setRootPath(self._workspace)
            self.arborescence.setRootIndex(self.fileModel.index(self._workspace))
            
    def  majTabAffichage(self):
        self.cb_autre.setCheckState(Qt.PartiallyChecked)
        self.cb_traitee.setCheckState(Qt.PartiallyChecked)
        self.cb_panorama.setCheckState(Qt.PartiallyChecked)
        self.cb_retouche.setCheckState(Qt.PartiallyChecked)
        self.cb_paysage.setCheckState(Qt.PartiallyChecked)
        self.sb_min.setValue(0)
        self.sb_max.setValue(0)
        self.liste_dates.clear()
        liste_fich = self._album_selectionne.listeJPG()
        dates = self._album_selectionne.getListeDates()
        self.progressBar.hide()
        self.bt_annuler_progress.hide()
        self.fichier_progress.hide()
        self._progress_stoppe = False
        Ihm.__nb_photos = len(liste_fich)
        self.sb_max.setValue(Ihm.__nb_photos)
        self.cbox_selections.clear()
        self.edtFiltreNomAffichage.setText("*.*")
        if liste_fich:
            self.liste_dates.addItems(dates)
            filtre = Filtre()
            #if PREFERENCES.isModeTri():
            f = PREFERENCES.getFiltreDefaut()
            if f: filtre = f
            if filtre.choixToutes():
                self.cb_toutes.setChecked(True)
            else:
                if filtre.choixInfos():
                    self.gb_infos.setChecked(True)
                    etoiles = filtre.getEtoiles()
                    self.cb_0_etoile.setChecked(etoiles[0])
                    self.cb_1_etoile.setChecked(etoiles[1])
                    self.cb_2_etoiles.setChecked(etoiles[2])
                    self.cb_3_etoiles.setChecked(etoiles[3])
                    self.setCBValue(self.cb_autre,filtre.getAutre())
                    self.setCBValue(self.cb_traitee,filtre.getTraitees())
                    self.setCBValue(self.cb_panorama,filtre.getPanorama())
                    self.setCBValue(self.cb_retouche,filtre.getRetouche())
                    self.setCBValue(self.cb_paysage,filtre.getPaysage())
                if filtre.choixNums():
                    self.gb_nums.setChecked(True)
                    self.sb_min.setValue(filtre.getNumPhotos()[0])
                    self.sb_max.setValue(filtre.getNumPhotos()[1])
                if filtre.choixDates():
                    self.gb_dates.setChecked(True)
                    l = filtre.getListeDates()
                    for n in range(self.liste_dates.count()):
                        item = self.liste_dates.item(n)
                        if item.text() in l:
                            item.setSelected(True)
            self.cbox_selections.addItems(["aucune"]+[n.replace('.sel','') for n in self._album_selectionne.listeSelections()])
        
    def majIhmSelection(self):
        if self._album_selectionne:
            isalbum = self._album_selectionne.estUnAlbum()
            self.btAfficher.setEnabled(isalbum)
            self.btViderRepertoire.setEnabled(True)
            self.btDetruireTriPhotos.setEnabled(isalbum)
        else:
            self.btAfficher.setEnabled(False)
            self.btViderRepertoire.setEnabled(False)
            self.btDetruireTriPhotos.setEnabled(False)
    
    def justeFiltre(self):
        self.arborescence.hide()
        
#
# progress bar
#
    def progressStoppe(self):
        return self._progress_stoppe
    
    def annulerProgress(self):
        self._progress_stoppe = True

    def initProgressBar(self,nb):
        self.setCursor(Qt.BusyCursor)
        self.progressBar.show()
        self.bt_annuler_progress.show()
        self.fichier_progress.show()
        self.progressBar.setValue(0)
        self.progressBar.setMaximum(nb)
        self._progress_stoppe = False
        
    def avanceProgressBar(self,n,ch):
        self.progressBar.setValue(n)
        self.fichier_progress.setText(ch)
        QApplication.instance().processEvents()
        if self.progressStoppe():
            return True
        return False
    
    def stopProgressBar(self):
        self.progressBar.hide()
        self.fichier_progress.hide()
        self.bt_annuler_progress.hide()
        self._progress_stoppe = True
        self.setCursor(self._cursor)
        
#     def ok(self):
#         self._event_loop.exit()
#         self._retour = True
#         self.hide()
        
    def afficher(self):
        if self._album_affiche:
            self._album_affiche.sauveInfos()
        self._album_affiche = self._album_selectionne
        print(self._album_affiche.repertoire())
        #self.fileModel.setAffichage(self._album_affiche.repertoire())
        tri_par_date = self.cbAffTrierParDate.checkState() == QtCore.Qt.Checked
        Ihm.__fenetre_thumbs.appliquerFiltre(self._album_affiche,self.getFiltre(),self,tri_par_date)
        
    def quitter(self):
        self.hide()
        Ihm.__fenetre_thumbs.quitter()

#      
#     def annuler(self):
#         self._event_loop.exit()
#         self._retour = False
#         self.hide()
#     
#     def retour(self):
#         self.show()
#         self._event_loop.exec_()
#         return self._retour
    
    def choixToutes(self):
        if self.cb_toutes.isChecked():
            self.gb_infos.setChecked(False)
            self.gb_nums.setChecked(False)
            self.gb_dates.setChecked(False)
            
    def choixDetails(self):
        if self.gb_infos.isChecked() or self.gb_nums.isChecked() or self.gb_dates.isChecked():
            self.cb_toutes.setChecked(False)
        else:
            self.cb_toutes.setChecked(True)
    #
    #        gestion workspace
    #
    def workspaceCourant(self):
        try:
            return self.comboWorkspace.currentText()
        except:
            return ""
                          
    def retirerWorkspace(self):
        wksp = self.workspaceCourant()
        self.comboWorkspace.removeItem(self.comboWorkspace.findText(wksp))
        PREFERENCES.removeWorkspace(wksp)
    
    def addWorkspace(self):
        wksp = str(QtWidgets.QFileDialog.getExistingDirectory(self,"Répertoire des images",
                                                          self.workspaceCourant(),    
                                                          QtWidgets.QFileDialog.ShowDirsOnly))
        if wksp:
            if self.comboWorkspace.findText(wksp) == -1:
                self.comboWorkspace.addItem(wksp)
            PREFERENCES.addWorkspace(wksp)
            self.comboWorkspace.setCurrentIndex(self.comboWorkspace.findText(wksp))
            self.modifierChoixWorkspace()
            
    def modifierChoixWorkspace(self):
        cursor = self.cursor()
        self.setCursor(Qt.BusyCursor)
        self.setFileModel()
        #self.initialise()
        self.setCursor(cursor)
    
#     def deplacerPhotos(self):
#         self._fenetre_thumbs.filtreObligatoire(True)
#         cursor = self.cursor()
#         self.setCursor(Qt.BusyCursor)
#         rep_cible = unicode(QtWidgets.QFileDialog.getExistingDirectory(self,"R�pertoire des images",
#                                                                Ihm.__rep_deplacement or self._liste_rep[0],    
#                                                                QtWidgets.QFileDialog.ShowDirsOnly))
#         if rep_cible: 
#             rep_cible += '/'   
#             Ihm.__rep_deplacement = rep_cible
#             l_photo = Rep.listeJPG()
#             if l_photo:
#                 nom,ok = QtWidgets.QInputDialog.getText(self,'Renommage photo','Nom',
#                                                     QtWidgets.QLineEdit.Normal,
#                                                     Ihm.__nom_deplacement or Rep.nomCommun(rep_cible))    
#                 nom = unicode(nom)
#                 Ihm.__nom_deplacement = nom
#                 if nom[-1] != '_': nom += '_'
#                 if ok:
#                     l_existant = glob.glob(rep_cible+nom+'*.jpg')
#                     nbe = len(l_existant)
#                     nb = len(l_photo)
#                     digit = int(math.log10(nbe + nb)) + 1
#                     format = '%.'+str(digit)+'i'
#                     if l_existant:
#                         digit_prec = int(math.log10(nbe)) + 1
#                         if digit != digit_prec:
#                             # il faut renommer les pr�c�dents
#                             for i in range(nbe):
#                                 nnom = nom + (format % (i+1)) + '.jpg.temp'
#                                 self.deplaceFichier(l_existant[i],rep_cible+nnom)
#                             for i in range(nbe):
#                                 nnom = nom + (format % (i+1)) + '.jpg'
#                                 self.deplaceFichier(rep_cible+nnom+'.temp',rep_cible+nnom)
#                     # deplacement des photos
#                     for i in range(nb):
#                         nnom = nom + (format % (nbe+i+1)) + '.jpg'
#                         self.deplaceFichier(l_photo[i],rep_cible+nnom)
#             l_video = glob.glob(Rep.repPhotos()+'/*.mov')
#             if l_video:
#                 nb = len(l_video)
#                 # deplacement des videos
#                 for i in range(nb):
#                     self.deplaceFichier(l_video[i],rep_cible+osp.basename(l_video[i]))
#             # pour reinitialiser
#             Rep.change(Rep.repPhotos())
#             Rep.detruireSiVide()
#             self.arborescence.clearSelection()
#         self.setCursor(cursor)
#         self._fenetre_thumbs.filtreObligatoire(False)
#         self.majIhm()
        
    def deplaceFichier(self,f,f1):
        if osp.isfile(f1):
            print('fichier existant')
        else:
            shutil.move(f,f1)
        
    def recreerMiniatures(self):
        if self._album_selectionne and self._album_selectionne.estUnAlbum():
            self._album_selectionne.detruireMiniatures()
            self._album_selectionne.refresh()
            self.majTabAffichage()
            self.majIhmSelection()
        else:
            for rep,sub,files in os.walk(self._selection):
                alb = Album(rep,self)
                if alb.getFirstPhoto():
                    print("création miniature",rep)
                    if alb.estUnAlbum():
                        alb.detruireMiniatures()
                    QApplication.instance().processEvents()
                    alb.refresh()
                    self.majTabAffichage()
                    self.majIhmSelection()
                    QApplication.instance().processEvents()
        
    def majMiniatures(self):
        if self._album_selectionne and self._album_selectionne.estUnAlbum():
            self._album_selectionne.refresh()
            self.majTabAffichage()
            self.majIhmSelection()
            
#     def recreerDates(self):
#         cursor = self.cursor()
#         self.setCursor(Qt.BusyCursor)
#         self.liste_dates.clear()
#         os.remove(Rep.fichierDates())
#         self.creerDates()
#         self.liste_dates.addItems(Ihm.__dates)
#         self.setCursor(cursor)
#         self.majIhm()
        
    def detruire(self):
        mess = "T'es sûr de vouloir détruire ?"
        ret = QMessageBox.warning(self,'Destruction',mess,QMessageBox.Ok,QMessageBox.Cancel) 
        if ret == QMessageBox.Ok:
            self.arborescence.clearSelection()
            shutil.rmtree(Rep.repPhotos())
        self.majIhm()
             
    def detruireTriPhotos(self):
        rep_vide = not (self._album_selectionne.listeSelections() or 
                        self._album_selectionne.listePano() or 
                        self._album_selectionne.listeRecup() or 
                        self._album_selectionne.listeRetouche())
        if not rep_vide:
            mess = 'Attention '
            if self._album_selectionne.listeSelections(): mess += 'les selections'
            if self._album_selectionne.listePano(): mess += ', les panoramas'
            if self._album_selectionne.listeRecup(): mess += ', les recups'
            if self._album_selectionne.listeRetouche(): mess += ', les retouches'
            mess += ' vont �tre d�truites'
            ret = QMessageBox.warning(self,'R�initialisation',mess,QMessageBox.Ok,QMessageBox.Cancel) 
        if rep_vide or ret == QMessageBox.Ok:
            self.arborescence.clearSelection()
            self._album_selectionne.reinitialiser()
        self.majIhmSelection()
        
    def getFiltre(self):
        rep_images = str(self.workspaceCourant())
        if rep_images[-1] != '/':
            rep_images += '/'
        #if self._liste_rep[0] != rep_images:
        #    PREFERENCES.setRepertoireDefaut(self._liste_rep[0],self._workspace)
        type_choix = [self.cb_toutes.isChecked(),self.gb_infos.isChecked(),\
                      self.gb_nums.isChecked(),self.gb_dates.isChecked()]
        etoiles = (self.cbCochee(self.cb_0_etoile),\
                   self.cbCochee(self.cb_1_etoile),\
                   self.cbCochee(self.cb_2_etoiles),\
                   self.cbCochee(self.cb_3_etoiles))
        autre = self.getCBValue(self.cb_autre)
        traitee = self.getCBValue(self.cb_traitee)
        pano = self.getCBValue(self.cb_panorama)
        retouche = self.getCBValue(self.cb_retouche)
        paysage = self.getCBValue(self.cb_paysage)
        vmin = self.sb_min.value()
        vmax = self.sb_max.value()
        liste_dates = [str(v.text()) for v in self.liste_dates.selectedItems()]
        nom_selection = str(self.cbox_selections.itemText(self.cbox_selections.currentIndex()))
        filtre_nom = self.edtFiltreNomAffichage.text()
        filtre = Filtre(type_choix,etoiles,autre,traitee,pano,retouche,paysage,[vmin,vmax],liste_dates,nom_selection,filtre_nom)
        PREFERENCES.setFiltreDefaut(filtre)
        return filtre

    def cbCochee(self,cb):
        return (cb.checkState() == Qt.Checked)
        
    def getCBValue(self,cb):
        cbv = cb.checkState()
        return ((cbv == Qt.PartiallyChecked or cbv == Qt.Unchecked),
                (cbv == Qt.PartiallyChecked or cbv == Qt.Checked))

    def setCBValue(self,cb,val):
        if val[0] and val[1]:
            cb.setCheckState(Qt.PartiallyChecked)
        elif val[0]:
            cb.setCheckState(Qt.Unchecked)
        else:
            cb.setCheckState(Qt.Checked)
    
    #
    # selection d'un item du treeview
    #
    def select(self,model_index):
        if not self._busy:
            self._busy = True
            select = str(self.fileModel.filePath(model_index))
            jpg = None
            #self.fileModel.setSelection(None)
            if osp.isdir(select):
#                 print osp.basename(select)
                if osp.basename(select) == "TriPhotos":
                    # rep est visible, il ne devrait pas
                    import win32api, win32con
                    win32api.SetFileAttributes(select,win32con.FILE_ATTRIBUTE_HIDDEN)
                self._album_selectionne = Album(select,self,verif_album=True)
                rep = select + '/'
                self.majTabAffichage()
                #self.charger()
                jpg = scanRep.first(rep,'.JPG')
                self.btCreerRepertoire.setEnabled(True)
                self.tabWidget.setEnabled(True)
                #self.fileModel.setSelection(select)
            elif (select[-4:].lower() == '.jpg'):     
                self._album_selectionne = None
                rep = osp.dirname(select)
                jpg = osp.basename(select)
                self.btCreerRepertoire.setEnabled(False)
                self.tabWidget.setEnabled(False)
            self.majIhmSelection()
            if jpg:
                if osp.isfile(rep+'/TriPhotos/Thumbs/'+jpg):
                    image = QImage(rep+'/TriPhotos/Thumbs/'+jpg,'JPG')
                else:
                    image = QImage(select,'JPG')
                    if image.width() > image.height():
                        image = image.scaledToWidth(PREFERENCES.LARGEUR_IMAGE)
                    else:
                        image = image.scaledToHeight(PREFERENCES.LARGEUR_IMAGE)
                pix = QPixmap.fromImage(image)
                self.photo.setPixmap(pix)
            else:
                self.photo.clear()
            self._selection = select
            
            # mise � jour du tabWidget selectionne
            tab = self.tabWidget.currentIndex()
            if tab == 2: #renommage
                self._renommage.majFenetre(self._album_selectionne)
            if tab == 3: #compression
                self._compression.majFenetre(self._album_selectionne)
#                 if self.tabWidget.currentIndex() == 1:  
#                     self.autoRenommage()
#                 self.lblNbPano.setText(str(len(self._album_selectionne.listePano())))
#                 self.lblNbPano_2.setText(str(len(self._album_selectionne.listePano())))
#                 self.lblNbRetouche.setText(str(len(self._album_selectionne.listeRetouche())))
#                 self.lblNbRecup.setText(str(len(self._album_selectionne.listeRecup())))
            self._busy=False
            #print self._album_selectionne
    
    def tabChanged(self,tab):
        if self._album_selectionne: 
            if tab == 2: #renommage
                self._renommage.majFenetre(self._album_selectionne)
            if tab == 3: #compression
                self._compression.majFenetre(self._album_selectionne)
         
    #
    # gestion répertoires
    #
    def creerRepertoire(self):
        rep,nom_ok = QtWidgets.QInputDialog.getText(self,"Créer",'Nom du nouveau répertoire\n/<nom> pour créer à la racine',QtWidgets.QLineEdit.Normal,'')
        if not nom_ok: return
        rep = str(rep)
        if rep[0] == '/':
            new_rep = str(self._workspace + rep)
        else:
            if not self._selection:return
            new_rep = os.path.join(self._selection,rep)
        if not os.path.isdir(new_rep):
            os.mkdir(new_rep)
            
    def deplacerRepertoire(self):
        import win32api, win32con
        if not self._ctrl_x or not self._selection:return
        msgBox = QMessageBox(self)
        but_repertoire = msgBox.addButton(self.tr("Répertoire"), QMessageBox.ActionRole)
        but_contenu = msgBox.addButton(self.tr("Contenu"), QMessageBox.ActionRole)
        but_abort = msgBox.addButton(self.tr("Annuler"),QMessageBox.RejectRole)
        msgBox.setText("D�placer "+osp.basename(self._ctrl_x)+" dans "+osp.basename(self._selection))
        msgBox.setInformativeText("Déplacer le repertoire ou seulement le contenu ?")
        ret = msgBox.exec_()
        #print self._album_selectionne
        if msgBox.clickedButton() == but_repertoire:
            # copie de tout le repertoire
            #shutil.copytree(self._ctrl_x,osp.join(self._selection,osp.basename(self._ctrl_x)))
            #self.supprimerRepertoire(self._ctrl_x)
            shutil.move(self._ctrl_x,osp.join(self._selection,osp.basename(self._ctrl_x)))
        elif msgBox.clickedButton() == but_contenu:
            # copie du contenu
            l = os.listdir(self._ctrl_x)
            for e in l:
                if e != "TriPhotos":
                    source = osp.join(self._ctrl_x,e)
                    cible = osp.join(self._selection,e)
                    if osp.isfile(osp.join(self._ctrl_x,e)):
                        shutil.move(source,cible)
                    else:
                        try:
                            shutil.copytree(source,cible)
                            self.supprimerRepertoire(source)
                        except:
                            print("deplacement impossible")
                            import traceback
                            print(traceback.format_exc(1))
            # si des répertoires "TriPhotos" ont été copiés, il faut les cacher
            for rep,subrep,files in os.walk(self._selection):
                if osp.basename(rep) == "TriPhotos":
                    win32api.SetFileAttributes(rep,win32con.FILE_ATTRIBUTE_HIDDEN)
            Album(self._ctrl_x,self,verif_album=True)
            self._album_selectionne = Album(self._selection,self,verif_album=True)
    
    def getSelectedPhotos(self):
        return Ihm.__fenetre_thumbs.getSelectedPhotos()
    
    def copierImages(self):
        from common import Photo
        lphotos = Ihm.__fenetre_thumbs.getPhotos(Ihm.__fenetre_thumbs.selectionAcopier)
        for photo in lphotos:
            Photo.deplacerPhoto(osp.join(self._album_affiche.repertoire(),photo),self._album_selectionne.repertoire(),remove=False)
            
        self._album_selectionne.refresh()
        
    def deplacerImages(self):
        from common import Photo
        lphotos = Ihm.__fenetre_thumbs.getPhotos(Ihm.__fenetre_thumbs.selectionAcouper)
        for photo in lphotos:
            Photo.deplacerPhoto(osp.join(self._album_affiche.repertoire(),photo),self._album_selectionne.repertoire())
            
        self._album_selectionne.refresh()
        self._album_affiche.refresh()
        Ihm.__fenetre_thumbs.detruirePhoto(force=True)
    
    def supprimerRepertoire(self,rep_a_detruire=None):
        if not rep_a_detruire:
            ok = QMessageBox.question(self.btSupprimerRepertoire,r"Détruire répertoire","Le répertoire "+osp.basename(self._selection)+" va être définitivement détruit !!",QMessageBox.Ok |QMessageBox.Cancel)
            if not ok == QMessageBox.Ok: return
            rep_a_detruire = self._selection
        if os.path.isdir(rep_a_detruire):
            for rep,srep,files in os.walk(rep_a_detruire):
                for f in files:
                    os.remove(rep+"/"+f)
                if osp.basename(rep) == "TriPhotos":
                    shutil.rmtree(rep, ignore_errors=True)
            for rep,srep,files in os.walk(rep_a_detruire):
                self.fileModel.rmdir(self.fileModel.index(rep))
            self.fileModel.rmdir(self.fileModel.index(rep_a_detruire))
            self.fileModel.setRootPath("");
            self.fileModel.setRootPath(self.workspaceCourant())
            self.arborescence.setCurrentIndex(self.fileModel.index(rep_a_detruire + "/../"))
            if not rep_a_detruire:
                # si on est au niveau du root la methode select n'est pas appel�e
                self._selection = rep_a_detruire + "/../"

    def viderRepertoire(self):
        rep_a_detruire = self._selection
        if os.path.isdir(rep_a_detruire):
            for rep,srep,files in os.walk(rep_a_detruire):
                for f in files:
                    os.remove(rep+"/"+f)
                if osp.basename(rep) == "TriPhotos":
                    shutil.rmtree(rep, ignore_errors=True)
            for rep,srep,files in os.walk(rep_a_detruire):
                print(rep)
                if rep != rep_a_detruire:
                    self.fileModel.rmdir(self.fileModel.index(rep))
            #self.fileModel.setRootPath("");
            #self.fileModel.setRootPath(self.workspaceCourant())

    #
    # renommage des fichiers
    #
    def detruireFichiers(self):
        self._renommage.detruireFichiers()

    def refreshRenommage(self):
        self._renommage.afficherFichiers()
        
    def testerRenommage(self):
        self._renommage.tester()
        
    def validerRenommage(self):
        self._renommage.valider()
        self._renommage.afficherFichiers()
                
    def autoRenommage(self):
        import time
        t0=time.time()
        self._renommage.afficherFichiers()
        #print time.time()-t0
        self._renommage.auto()
        #print time.time()-t0
        
    def aideRenommage(self):
        from .renommage import aideRenommage
        # il faut mettre dans un attribut de la classe sinon la fen�tre disparait imm�diatement
        if not self._aide:
            self._aide = aideRenommage(self.geometry())
        self._aide.show()

    #
    # compression
    #
    def repertoireCompression(self):
        self._compression.choixRepertoire()
        pass
    
    def afficheCompressionEstime(self):
        self._compression.majListe()
    
    def compressionToutes(self):
        self._compression.majListe()
            
    def compressionAffichees(self):
        self._compression.majListe()
        
    def compressionRenommage(self):
        self._compression.majListe()
        
    def compressionSelection(self):
        self._compression.majListe()

    def validerCompression(self):
        self._compression.valider()
        
    def afficherCompression(self):
        self._compression.majListe()
    
    def keyPressEvent(self,event):
        touche = event.key()
        print(touche)
        if touche == Qt.Key_F3:
            self._gestion_ecrans.changeEcrans()
        elif touche == Qt.Key_Delete:
            ret = QMessageBox.question(self,"Destruction répertoire",
                                           f"Etes vous sûr de détruie le répertoire {self._album_selectionne.repertoire()} ?",
                                           QMessageBox.Ok | QMessageBox.Cancel)
            if  ret == QMessageBox.Ok:
                shutil.rmtree(self._album_selectionne.repertoire())
        elif touche == Qt.Key_C and event.modifiers() == Qt.ControlModifier:
            try:
                self.rep_a_copier = self._album_selectionne.repertoire()
                self.rep_a_couper = None
            except:
                return
            print("Copie images vers ",self.rep_a_copier)

        elif touche == Qt.Key_X and event.modifiers() == Qt.ControlModifier:
            try:
                self.rep_a_couper = self._album_selectionne.repertoire()
                self.rep_a_copier = None
            except:
                return
        elif touche == Qt.Key_V and event.modifiers() == Qt.ControlModifier:
            if Ihm.__fenetre_thumbs.selectionAcouper:
                ret = QMessageBox.question(self,"Déplacement images",
                                           f"Etes vous sûr de déplacer les {len(Ihm.__fenetre_thumbs.selectionAcouper)} images ?",
                                           QMessageBox.Ok | QMessageBox.Cancel)
                if  ret == QMessageBox.Ok:
                    self.deplacerImages()
            elif Ihm.__fenetre_thumbs.selectionAcopier:
                ret = QMessageBox.question(self,"Copie images",
                                           f"Etes vous sûr de copier les {len(Ihm.__fenetre_thumbs.selectionAcopier)} images ?",
                                           QMessageBox.Ok | QMessageBox.Cancel)
                if ret == QMessageBox.Ok:
                    self.copierImages()
            elif self.rep_a_copier:
                try:
                    cible = self._album_selectionne.repertoire()
                except:
                    return
                ret = QMessageBox.question(self,"Copie répertoire",
                                           f"Copier le répertoire {self.rep_a_copier} dans {cible} ?",
                                           QMessageBox.Ok | QMessageBox.Cancel)
                if ret == QMessageBox.Ok:
                    shutil.copytree(self.rep_a_copier,cible+'/'+osp.basename(self.rep_a_copier))
            elif self.rep_a_couper:
                try:
                    cible = self._album_selectionne.repertoire()
                except:
                    return
                ret = QMessageBox.question(self,"Déplacement répertoire",
                                           f"Déplacer le répertoire {osp.basename(self.rep_a_couper)} dans {osp.basename(cible)} ?",
                                           QMessageBox.Ok | QMessageBox.Cancel)
                if ret == QMessageBox.Ok:
                    shutil.move(self.rep_a_couper,cible+'/'+osp.basename(self.rep_a_couper))
            self.rep_a_copier = None
            self.rep_a_couper = None
            Ihm.__fenetre_thumbs.selectionAcopier = []
            Ihm.__fenetre_thumbs.selectionAcouper = []
            Ihm.__fenetre_thumbs.majTitre()
        else:
            super(Ihm,self).keyPressEvent(event)

