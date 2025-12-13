# -*- coding: latin-1
"""
Created on 5 juin 2011

@author: Bureau
"""
import glob,os,math,shutil,sys
import pickle
from PyQt5 import QtCore,QtWidgets
from PyQt5.QtCore import Qt,QObject,QString
from PyQt5.QtWidgets import QDialogButtonBox,QFileSystemModel,QMessageBox,QDesktopWidget
from PyQt5.QtGui import QIcon,QImage,QPixmap
import os.path as osp
from src import preferences as PREFERENCES
from common import GestionPhoto,Exif,scanRep
from RepertoirePhotos import RepPhotos as Rep
from choix_filtre import Ui_MainWindow as FormClass
from PyQt5.QtWidgets import QMainWindow as BaseClass

class MyQFileSystemModel(QFileSystemModel):
    def __init__(self):
        super(MyQFileSystemModel, self).__init__()
        
    def data(self,index,role):
        if role == Qt.DecorationRole:
            rep=str(self.filePath(index))
            if osp.isdir(rep):
                jpg = scanRep.first(rep,'.JPG')
                if jpg:
                    if osp.isdir(rep+'/triPhotos'):
                        return QPixmap("Data/repTri.png")
                    else:
                        return QPixmap("Data/repImage.png")
                else:
                    mov = scanRep.first(rep,'.MOV')
                    if mov:
                        return QPixmap("Data/repVideo.png")
                    else:
                        return QPixmap("Data/repNormal.png")       
        return QFileSystemModel.data(self,index, role)
    
class FenetreFiltre(BaseClass,FormClass):
    __fenetre_thumbs = None
    __dates = None
    __rep_deplacement = None
    __nom_deplacement = ""
    def __init__(self,parent,rep_photo=None):
        BaseClass.__init__(self, None)
        self.setupUi(self)
        FenetreFiltre.__fenetre_thumbs = parent
        self.__liste_rep,self.__rep_photo = PREFERENCES.getRepertoireDefaut()
        if rep_photo:
            Rep.change(rep_photo)
        elif self.__rep_photo:
            Rep.change(self.__rep_photo)
        self.__retour = None
        self.__busy = False
        self.__progress_stoppe = False
        QObject.connect(self.actionQuitter,QtCore.SIGNAL("triggered()"),self.quitter)
        QObject.connect(self.cb_toutes,QtCore.SIGNAL("toggled(bool)"),self.choixToutes)
        QObject.connect(self.gb_infos,QtCore.SIGNAL("toggled(bool)"),self.choixDetails)
        QObject.connect(self.gb_dates,QtCore.SIGNAL("toggled(bool)"),self.choixDetails)
        QObject.connect(self.gb_nums,QtCore.SIGNAL("toggled(bool)"),self.choixDetails)
        QObject.connect(self.bt_ok,QtCore.SIGNAL("clicked()"),self.afficher)
        QObject.connect(self.bt_repertoire,QtCore.SIGNAL("clicked()"),self.choixRepertoire)
        QObject.connect(self.bt_retirer_repertoire,QtCore.SIGNAL("clicked()"),self.retirerRepertoire)
        QObject.connect(self.cb_repertoire,QtCore.SIGNAL("currentIndexChanged(QString)"),self.modifierChoixRepertoire)
        QObject.connect(self.actionRecreerMiniatures,QtCore.SIGNAL("triggered()"),self.recreerMiniatures)
        QObject.connect(self.actionRecreerDates,QtCore.SIGNAL("triggered()"),self.recreerDates)
        QObject.connect(self.actionDeplacerPhotos,QtCore.SIGNAL("triggered()"),self.deplacerPhotos)
        QObject.connect(self.actionDetruire,QtCore.SIGNAL("triggered()"),self.detruire)
        QObject.connect(self.actionReinitialiser,QtCore.SIGNAL("triggered()"),self.reinitialiserRepertoire)
        QObject.connect(self.actionRenommer_fichiers,QtCore.SIGNAL("triggered()"),self.renommerFichiers)
        QObject.connect(self.bt_annuler_progress,QtCore.SIGNAL("clicked()"),self.annulerProgress)
        QObject.connect(self.btCreerRepertoire,QtCore.SIGNAL("clicked()"),self.creerRepertoire)
        QObject.connect(self.btDeplacerImages,QtCore.SIGNAL("clicked()"),self.deplacerImages)
        QObject.connect(self.btSupprimerRepertoire,QtCore.SIGNAL("clicked()"),self.supprimerRepertoire)
        self.setFileModel()
        self.arborescence.setColumnHidden(1,True)
        self.arborescence.setColumnHidden(2,True)
        self.arborescence.setColumnHidden(3,True)
        QtCore.QObject.connect(self.arborescence,QtCore.SIGNAL("clicked(QModelIndex)"),self.select)
        self._selection = None
        self.__num_ecran = 1
        if self.__liste_rep:
            self.cb_repertoire.addItems(self.__liste_rep)
            #self.charger()
        if PREFERENCES.isModeVisionneuse():
            self.setWindowFlags(Qt.FramelessWindowHint |Qt.WindowStaysOnTopHint)
            taille = QDesktopWidget().screenGeometry(0)
            self.move(0,taille.height() - self.height())

        self.show()
            #self.setWindowModality(Qt.ApplicationModal)
            #self.__event_loop = QtCore.QEventLoop()
    
    def changeEcran(self):
        if QDesktopWidget().numScreens() > 1:
            self.__num_ecran = 1 + self.__num_ecran % 2
            self.setGeometry(*PREFERENCES.ARBO_GEOMETRY[self.__num_ecran-1])
     
    def repCourant(self):
        if self.__liste_rep:
            return self.cb_repertoire.currentText()
        else:
            return QtCore.QString()
        
    def setFileModel(self):
        self.fileModel = MyQFileSystemModel()
        #self.fileModel = QtWidgets.QDirModel(['*'],QtCore.QDir.Dirs | QtCore.QDir.NoDotAndDotDot,QtCore.QDir.Name)
        self.arborescence.setModel(self.fileModel)
        if self.repCourant():
            self.fileModel.setRootPath(self.repCourant())
            self.arborescence.setRootIndex(self.fileModel.index(self.repCourant()))
        if Rep.ok():
            self.arborescence.setCurrentIndex(self.fileModel.index(Rep.repPhotos()))
            
#        self.fileModel.setRootPath(self.__rep_images)
#        self.arborescence.setModel(self.fileModel)
#        if self.__rep_photo:
#            self.arborescence.setCurrentIndex(self.fileModel.index(self.__rep_photo))
            
    def initialise(self):
        self.cb_nettete.setCheckState(Qt.PartiallyChecked)
        self.cb_traitee.setCheckState(Qt.PartiallyChecked)
        self.cb_panorama.setCheckState(Qt.PartiallyChecked)
        self.cb_retouche.setCheckState(Qt.PartiallyChecked)
        self.sb_min.setValue(0)
        self.sb_max.setValue(0)
        self.liste_dates.clear()
        liste_fich = Rep.listeJPG()
        self.progressBar.hide()
        self.bt_annuler_progress.hide()
        self.fichier_progress.hide()
        self.__progress_stoppe = False
        FenetreFiltre.__nb_photos = len(liste_fich)
        self.sb_max.setValue(FenetreFiltre.__nb_photos)
        self.cbox_selections.clear()
        if liste_fich:
            self.creerDates()
            self.liste_dates.addItems(FenetreFiltre.__dates)
            filtre = Filtre()
            if PREFERENCES.isModeTri():
                f = PREFERENCES.getFiltreDefaut()
                if f:
                    filtre = f
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
                    self.setCBValue(self.cb_nettete,filtre.getNettete())
                    self.setCBValue(self.cb_traitee,filtre.getTraitees())
                    self.setCBValue(self.cb_panorama,filtre.getPanorama())
                    self.setCBValue(self.cb_retouche,filtre.getRetouche())
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
            self.cbox_selections.addItems([n.replace('.info','') for n in Rep.listeSelections()])
        self.majIhm()
        
    def majIhm(self):
        if Rep.ok():
            self.bt_ok.setEnabled(True)
            self.actionRecreerMiniatures.setEnabled(True)
            self.actionRecreerDates.setEnabled(True)
            self.actionDeplacerPhotos.setEnabled(True)
            self.actionReinitialiser.setEnabled(True)
        else:
            self.bt_ok.setEnabled(False)
            self.actionRecreerMiniatures.setEnabled(False)
            self.actionRecreerDates.setEnabled(False)
            self.actionDeplacerPhotos.setEnabled(False)
            self.actionReinitialiser.setEnabled(False)
    
    def justeFiltre(self):
        self.arborescence.hide()
        
    def progressStoppe(self):
        return self.__progress_stoppe
    
    def annulerProgress(self):
        self.__progress_stoppe = True

    def creerDates(self):
        liste_fich = Rep.listeJPG()
        if liste_fich:
            if osp.isfile(Rep.fichierDates()):
                with open(Rep.fichierDates(),'r') as fd:
                    FenetreFiltre.__dates = pickle.load(fd)
            else:
                FenetreFiltre.__dates,ld1,ld2 = [],[],[]
                for f in liste_fich:
                    try:
                        j = Rep.getExif(f)['date']
                    except:
                        j = 'aucune'
                    if not j in ld1:
                        jr = j.split('/')
                        jr.reverse()
                        ld1.append(j)
                        ld2.append('/'.join(jr))
                z = list(zip(ld2,ld1))
                z.sort()
                jr,FenetreFiltre.__dates = list(zip(*z))
                with open(Rep.fichierDates(),'w') as fd:
                    pickle.dump(FenetreFiltre.__dates,fd)

#     def ok(self):
#         self.__event_loop.exit()
#         self.__retour = True
#         self.hide()
        
    def afficher(self):
        FenetreFiltre.__fenetre_thumbs.appliquerFiltre(self.getFiltre())
        
    def quitter(self):
        self.hide()
        FenetreFiltre.__fenetre_thumbs.quitter()
#      
#     def annuler(self):
#         self.__event_loop.exit()
#         self.__retour = False
#         self.hide()
#     
#     def retour(self):
#         self.show()
#         self.__event_loop.exec_()
#         return self.__retour
    
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
                      
    def retirerRepertoire(self):
        rep = self.cb_repertoire.currentText()
        self.cb_repertoire.removeItem(self.cb_repertoire.findText(rep))
        self.__liste_rep.remove(rep)
        PREFERENCES.setRepertoireDefaut(self.__liste_rep,None)
    
    def choixRepertoire(self):
        rep = str(QtWidgets.QFileDialog.getExistingDirectory(self,"R�pertoire des images",
                                                          self.repCourant(),    
                                                          QtWidgets.QFileDialog.ShowDirsOnly))
        if rep:
            if self.cb_repertoire.findText(rep) == -1:
                self.cb_repertoire.addItem(rep)
                self.__liste_rep.append(rep)
                PREFERENCES.setRepertoireDefaut(self.__liste_rep,None)
            self.modifierChoixRepertoire()
            
    def modifierChoixRepertoire(self):
            cursor = self.cursor()
            self.setCursor(Qt.BusyCursor)
            self.__rep_photo = None
            self.setFileModel()
            self.initialise()
            self.setCursor(cursor)
    
    def deplacerPhotos(self):
        self.__fenetre_thumbs.filtreObligatoire(True)
        cursor = self.cursor()
        self.setCursor(Qt.BusyCursor)
        rep_cible = str(QtWidgets.QFileDialog.getExistingDirectory(self,"R�pertoire des images",
                                                               FenetreFiltre.__rep_deplacement or self.__liste_rep[0],    
                                                               QtWidgets.QFileDialog.ShowDirsOnly))
        if rep_cible: 
            rep_cible += '/'   
            FenetreFiltre.__rep_deplacement = rep_cible
            l_photo = Rep.listeJPG()
            if l_photo:
                nom,ok = QtWidgets.QInputDialog.getText(self,'Renommage photo','Nom',
                                                    QtWidgets.QLineEdit.Normal,
                                                    FenetreFiltre.__nom_deplacement or Rep.nomCommun(rep_cible))    
                nom = str(nom)
                FenetreFiltre.__nom_deplacement = nom
                if nom[-1] != '_': nom += '_'
                if ok:
                    l_existant = glob.glob(rep_cible+nom+'*.jpg')
                    nbe = len(l_existant)
                    nb = len(l_photo)
                    digit = int(math.log10(nbe + nb)) + 1
                    format = '%.'+str(digit)+'i'
                    if l_existant:
                        digit_prec = int(math.log10(nbe)) + 1
                        if digit != digit_prec:
                            # il faut renommer les pr�c�dents
                            for i in range(nbe):
                                nnom = nom + (format % (i+1)) + '.jpg.temp'
                                self.deplaceFichier(l_existant[i],rep_cible+nnom)
                            for i in range(nbe):
                                nnom = nom + (format % (i+1)) + '.jpg'
                                self.deplaceFichier(rep_cible+nnom+'.temp',rep_cible+nnom)
                    # deplacement des photos
                    for i in range(nb):
                        nnom = nom + (format % (nbe+i+1)) + '.jpg'
                        self.deplaceFichier(l_photo[i],rep_cible+nnom)
            l_video = glob.glob(Rep.repPhotos()+'/*.mov')
            if l_video:
                nb = len(l_video)
                # deplacement des videos
                for i in range(nb):
                    self.deplaceFichier(l_video[i],rep_cible+osp.basename(l_video[i]))
            # pour reinitialiser
            Rep.change(Rep.repPhotos())
            Rep.detruireSiVide()
            self.arborescence.clearSelection()
        self.setCursor(cursor)
        self.__fenetre_thumbs.filtreObligatoire(False)
        self.majIhm()
        
    def deplaceFichier(self,f,f1):
        if osp.isfile(f1):
            print('fichier existant')
        else:
            shutil.move(f,f1)
        
    def recreerMiniatures(self):
        Rep.detruireMiniatures()
        self.charger()
        self.majIhm()
        
    def recreerDates(self):
        cursor = self.cursor()
        self.setCursor(Qt.BusyCursor)
        self.liste_dates.clear()
        os.remove(Rep.fichierDates())
        self.creerDates()
        self.liste_dates.addItems(FenetreFiltre.__dates)
        self.setCursor(cursor)
        self.majIhm()
        
    def detruire(self):
        mess = "T'es s�r de vouloir d�truire ?"
        ret = QMessageBox.warning(self,'Destruction',mess,QMessageBox.Ok,QMessageBox.Cancel) 
        if ret == QMessageBox.Ok:
            self.arborescence.clearSelection()
            shutil.rmtree(Rep.repPhotos())
        self.majIhm()
             
    def reinitialiserRepertoire(self):
        rep_vide = not (Rep.listeSelections() or Rep.listePano() or Rep.listeRecup() or Rep.listeRetouche())
        if not rep_vide:
            mess = 'Attention '
            if Rep.listeSelections(): mess += 'les selections'
            if Rep.listePano(): mess += ', les panoramas'
            if Rep.listeRecup(): mess += ', les recups'
            if Rep.listeRetouche(): mess += ', les retouches'
            mess += ' vont �tre d�truites'
            ret = QMessageBox.warning(self,'R�initialisation',mess,QMessageBox.Ok,QMessageBox.Cancel) 
        if rep_vide or ret == QMessageBox.Ok:
            self.arborescence.clearSelection()
            Rep.reinitialiser()
        self.majIhm()
        
    def getFiltre(self):
        rep_images = str(self.cb_repertoire.currentText())
        if rep_images[-1] != '/':
            rep_images += '/'
        #if self.__liste_rep[0] != rep_images:
        #    PREFERENCES.setRepertoireDefaut(self.__liste_rep[0],self.__rep_photo)
        type_choix = [self.cb_toutes.isChecked(),self.gb_infos.isChecked(),\
                      self.gb_nums.isChecked(),self.gb_dates.isChecked()]
        etoiles = (self.cbCochee(self.cb_0_etoile),\
                   self.cbCochee(self.cb_1_etoile),\
                   self.cbCochee(self.cb_2_etoiles),\
                   self.cbCochee(self.cb_3_etoiles))
        nettete = self.getCBValue(self.cb_nettete)
        traitee = self.getCBValue(self.cb_traitee)
        pano = self.getCBValue(self.cb_panorama)
        retouche = self.getCBValue(self.cb_retouche)
        min = self.sb_min.value()
        max = self.sb_max.value()
        liste_dates = [str(v.text()) for v in self.liste_dates.selectedItems()]
        nom_selection = str(self.cbox_selections.itemText(self.cbox_selections.currentIndex()))
        filtre = Filtre(type_choix,etoiles,nettete,traitee,pano,retouche,[min,max],liste_dates,nom_selection)
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
    
    def select(self,model_index):
        if not self.__busy:
            self.__busy = True
            select = str(self.fileModel.filePath(model_index))
            jpg = None
            Rep.change(None)
            if osp.isdir(select):
                rep = select + '/'
                Rep.change(rep)
                self.charger()
                jpg = scanRep.first(rep,'.JPG')
                self.btCreerRepertoire.setEnabled(True)
                self.btDeplacerImages.setEnabled(True)
                self.btSupprimerRepertoire.setEnabled(True)
            elif (select[-4:].lower() == '.jpg'):
                rep = osp.dirname(select)
                jpg = osp.basename(select)
                self.btCreerRepertoire.setEnabled(False)
                self.btDeplacerImages.setEnabled(False)
                self.btSupprimerRepertoire.setEnabled(False)
            self.majIhm()
            if jpg:
                if osp.isfile(rep+'/TriPhotos/Thumbs/'+jpg):
                    image = QImage(QString(rep+'/TriPhotos/Thumbs/'+jpg),'JPG')
                else:
                    image = QImage(QString(select),'JPG')
                    if image.width() > image.height():
                        image = image.scaledToWidth(PREFERENCES.LARGEUR_IMAGE)
                    else:
                        image = image.scaledToHeight(PREFERENCES.LARGEUR_IMAGE)
                pix = QPixmap.fromImage(image)
                self.photo.setPixmap(pix)
            else:
                self.photo.clear()
            self._selection = select
            self.__busy=False
        
    def charger(self):
        cursor = self.cursor()
        self.setCursor(Qt.BusyCursor)
        if Rep.ok():
            FenetreFiltre.__fenetre_thumbs.creerMiniature()
        self.initialise()
        self.setCursor(cursor)
    
    def creerRepertoire(self):
        import os
        rep = str(self.edtNomRepertoire.text())
        new_rep = os.path.join(self._selection,rep)
        if not os.path.isdir(new_rep):
            os.mkdir(new_rep)
    
    def deplacerImages(self):
        ihm_miniatures = FenetreFiltre.__fenetre_thumbs
        ihm_miniatures.deplacerPhotos(self._selection)
    
    def supprimerRepertoire(self):
        if os.path.isdir(self._selection):
            for rep,srep,files in os.walk(self._selection):
                for f in files:
                    os.remove(rep+"/"+f)
                if osp.basename(rep) == "TriPhotos":
                    shutil.rmtree(rep, ignore_errors=True)
            for rep,srep,files in os.walk(self._selection):
                self.fileModel.rmdir(self.fileModel.index(rep))
            self.fileModel.rmdir(self.fileModel.index(self._selection))
            self.fileModel.setRootPath("");
            self.fileModel.setRootPath(self.repCourant())
            self.arborescence.setCurrentIndex(self.fileModel.index(self._selection + "/../"))

    def renommerFichiers(self):
        from Renommage import IhmRenommage  
        ihm = IhmRenommage(self._selection,self.__num_ecran)
        
class Filtre:
    def __init__(self,types_choix=[False,False,False,False],star=[None,None,None,None],net=[None,None],\
            trait=[None,None],pano=[None,None],ret=[None,None],nums=[0,0],dates=[],nom_selection=''):
        """
        type_choix contient True si toutes ou infos ou nums ou dates est selectionne
        """
        self.__types_choix = types_choix
        self.__etoiles = star
        self.__nettete = net
        self.__traitee = trait
        self.__panorama = pano
        self.__retouche = ret
        self.__num_photos = nums
        self.__liste_dates = dates
        self.__selection = nom_selection
        
    def choixToutes(self):
        return self.__types_choix[0]
    
    def choixInfos(self):
        return self.__types_choix[1]
    
    def choixNums(self):
        return self.__types_choix[2]
    
    def choixDates(self):
        return self.__types_choix[3]
    
    def getEtoiles(self):
        return self.__etoiles
    
    def getNettete(self):
        return self.__nettete
    
    def getTraitees(self):
        return self.__traitee
    
    def getPanorama(self):
        return self.__panorama
    
    def getRetouche(self):
        return self.__retouche
    
    def getNumPhotos(self):
        return self.__num_photos
    
    def getListeDates(self):
        return self.__liste_dates
    
    def getNonSelection(self):
        return self.__selection+'.info'
    
    def isOk(self,chemin,info,exif,n):
        if self.choixToutes():
            return True
        else:
            (ok_info,ok_num,ok_date) = (True,True,True)
            if self.choixInfos():
                et = info.getEtoiles()
                ne = info.getNettete()
                tr = info.getTraite()
                pa = info.getPano()
                re = info.getRetouche()
                ok_info = self.getEtoiles()[et] and self.getNettete()[ne] and self.getTraitees()[tr] \
                        and self.getPanorama()[pa] and self.getRetouche()[re]
            if self.choixNums():
                nums = self.getNumPhotos()
                ok_num = (n >= nums[0]) and (n <= nums[1])
            if self.choixDates():
                try:
                    j = exif['date']
                except:
                    j = 'aucune'
                ok_date = j in self.getListeDates()
            return ok_info and ok_num and ok_date
        
    def getPhotos(self):
        liste_tot = Rep.listeJPG()
        infos = Rep.getInfos()
        exifs = Rep.getExifs()
        liste = []
        n=1
        for f in liste_tot:
            name = osp.basename(f)
            info = infos.get(name)
            exif = exifs[name]
            if self.isOk(f,info,exif,n):
                liste.append(f)
            n+=1
        return liste

if __name__ == '__main__':
    from PyQt5.QtWidgets import QApplication
    app = QApplication([])
    app.setStyle("plastique")
    fen = FenetreFiltre(app,23,['toto','itit','tutu'])
    ret = fen.exec_()
    print(ret)
    if ret:
        filtre = fen.getFiltre()
        print(filtre.getListeDates(),filtre.choixDates()))
    print(dirIterator( "C:\\*.*" )