# -*- coding: latin-1
"""
Created on 4 juin 2011

@author: Bureau
"""

import glob,os,shutil
import datetime as dt
import os.path as osp
import copy
from PyQt5 import QtWidgets
from PyQt5.QtWidgets import QApplication,QMessageBox
from PyQt5.QtCore import Qt,QObject
from .Thumb import thumbnail
from src.ListeChainee import chainList
from common import Exif
from src.Album import Album
import src.preferences as PREFERENCES

class ListeThumbs():
    def __init__(self,ihm_miniature,pipe_fen_photo):
        self.__ihm_min = ihm_miniature
        self.__liste = chainList()
        self.__nb_traitees= [None,None,None]
        self.__album = None
        self.__filtre = None
        self.__ihm_arbo = None
        self.__tri_date = None
        thumbnail.pipe_fenetre_photo = pipe_fen_photo
        
    def chargeThumbs(self,album,filtre,ihm_arbo,tri_date):
        self.__album = album
        self.__filtre = filtre
        self.__ihm_arbo = ihm_arbo
        self.__tri_date = tri_date
        self.refresh()
        
    def refresh(self):
        repertoire_thumbs = self.__album.repThumbs()
        if self.__tri_date:
            liste_jpg = self.__album.listeJPGTrieParDate(chemin=False)
        else:
            liste_jpg = self.__album.listeJPG(chemin=False)
        if not liste_jpg:return
        #self.__album.setFichierInfos(filtre.getNonSelection())
        #self.__album.lireInfos()
        #self.infos = self.__album.getInfos()
        # si des photos ont �t� ajout�es ou retir�es le fichier exifs n'est plus � jour
        #self.__album.majExifs()
        self.exifs = self.__album.getExifs()
        selection = self.__filtre.getNomSelection()
        if selection != "aucune.sel":
            liste_fich = self.__album.lireSelection(selection)
            btoutes = False
        else:
            liste_fich = liste_jpg
            btoutes = True
        #print liste_fich
        self.__ihm_arbo.initProgressBar(len(liste_fich))
        #aff_traitees = 0
        n=0
        self.__liste = chainList()
        #self.infos.stopCalculTotaux(True)
        stop = False
        thumbnail.reinitNumero()
        for nom in liste_fich:
            if not stop and (btoutes or nom in liste_jpg):
                chemin = repertoire_thumbs + nom
                info = self.__album.getInfo(nom)
                exif = self.exifs[nom]
                ok = self.__filtre.isOk(chemin,info,exif,n)
                if ok:
                    tn = thumbnail(self.__ihm_min,self.__album,nom)
                    self.__liste.append(tn)
                    #aff_traitees += tn.getTraite()
                n+=1
                stop = self.__ihm_arbo.avanceProgressBar(n,nom)
        thumbnail.liste_thumbs = self
        #self.infos.stopCalculTotaux(False)
        #self.__nb_traitees = [self.infos.getNbTraites(),self.infos.getNbTraites(),aff_traitees]
        self.__ihm_arbo.stopProgressBar()
        if self.__liste:
            self.__liste.select(0,True)
    
#     def listeParDate(self,liste_jpg):
#         l = []
#         now = dt.datetime.now()
#         progress = QtWidgets.QProgressDialog('','Arr�ter',0,len(liste_jpg))
#         progress.setWindowTitle('Tri par date')
#         progress.setValue(0)
#         progress.show()
#         n=0
#         QApplication.instance().processEvents()
#         for nom in liste_jpg:
#             if not progress.wasCanceled():
#                 d = Exif.getChTriDate(self.exifs[nom])
#                 l.append((d,nom))
#                 n += 1
#                 progress.setValue(n)
#                 progress.setLabelText(nom)
#                 QApplication.instance().processEvents()
#         l.sort()
#         return list(zip(*l)[1])
    
    def appliquerInfos(self,info,toutes):
        self.__liste.apply(toutes,thumbnail.appliquerInfos,info)

    def afficherInfos(self,toutes):
        self.__liste.apply(toutes,thumbnail.afficherInfos)

    def rechargerInfos(self):
        for th in self.__liste:
            th.setInfo(self.__album.getInfo(th.getName()))

    def getNbTraites(self):
        self.__nb_traitees[1] = self.infos.getNbTraites()
        return self.__nb_traitees

    def getNbInfosTotaux(self):
        return self.infos.getNbInfosTotaux()
    
    def getNbInfosAffiches(self):
        return self.infos.getNbInfosAffiches()
    
    def getNbPhotos(self):
        return self.infos.getNbPhotos()

    # pour faire des boucles sur la liste
    def firstPtr(self):
        return self.__liste.firstPtr()
    
    def lastPtr(self):
        return self.__liste.ptr(-1)
    
    def nextPtr(self,ptr):
        return self.__liste.nextPtr(ptr)
    #####
    def getPtrPhoto(self,num):
        return self.__liste.ptr(num)
    
    def getPhoto(self,num):
        return self.__liste[num]
    
    def getListePhotos(self):
        return self.__liste.apply(True,thumbnail.getName)
        
    def __len__(self):
        return len(self.__liste)
    
    def selectNext(self):
        l = self.__liste.getSelected()
        index = min(l) + 1
        if index < len(self.__liste):
            self.unselectAll()
            self.__liste.select(index,True)
            self.__liste[index].select(True)
        
    def selectPrevious(self):
        l = self.__liste.getSelected()
        index = min(l) - 1
        if index > -1:
            self.unselectAll()
            self.__liste.select(index,True)
            self.__liste[index].select(True)

    def getFirst(self):
        return self.__liste[0]
    
    def getCurrent(self):
        return self.__liste.ptr(self.__liste.getFirstSelected()).value
    
    def getSelected(self):
        return self.__liste.getSelected()
    
    def getFirstSelected(self):
        return self.__liste.getFirstSelected()
    
    def deplacer(self,num_photo,avant_photo):
        l1 = chainList()
        # il faut retirer en partant de la fin
        l_num = list(num_photo)
        l_num.sort()
        l_num.reverse()
        for n in l_num:
            l1.insert(0,self.__liste.remove(n))
            if n < avant_photo:
                avant_photo -= 1
        #self.infos.deplacer(l1.apply(True,thumbnail.getName),self.__liste[avant_photo].getName())
        self.__liste.insert(avant_photo,l1)
        self.__liste.select(avant_photo+len(l1),True)
        self.__liste[avant_photo+len(l1)].select(True)

    def detruire(self,num_photo):
        ptr = self.__liste.remove(num_photo)
        #nom = ptr.getName()
        #self.infos.retire(nom)
        #Photo.detruirePhoto(self.__album,nom)
        return ptr
        
    def renommer(self,old,new):
        self.infos.renommer(old,new)
        self.exifs[new] = self.exifs.pop(old)
        
    def unselectAll(self):
        l = self.__liste.getSelected()
        for i in copy.copy(l):
            self.__liste.select(i,False)
            self.__liste[i].select(False)
                
    def select(self,thumb):
        self.unselectAll()
        self.__liste.select(thumb,True)
        thumb.select(True)
        
    def ajouteSelect(self,thumb,entre=False):
        l = self.__liste.getSelected()
        if entre and len(l)>0:
            n1 = min(l)
            n2 = self.__liste.index(thumb)
            if n1 > n2:
                n1,n2 = n2,n1
            for i in range(n1,n2+1):
                self.__liste.select(i,True)
                self.__liste[i].select(True)
        else:
            b = self.__liste.isSelected(thumb)
            self.__liste.select(thumb,not b)
            thumb.select(not b)
        
    def sauverInfos(self,force=True):
        if force:
#             self.infos.ecrire()
            self.__album.sauveInfos()
#         elif self.infos.modifiees():
#             res = QMessageBox.warning(None,"Sauvegarde informations","La selection "+Rep.getFichierInfos()+" a �t� modifi�e,\n tu veux sauver ?",
#                                             QtWidgets.QMessageBox.Yes,QtWidgets.QMessageBox.No)
#             if res == QMessageBox.Yes:
#                 self.infos.ecrire()
#             else:
#                 self.infos.setModifiees(False)
    
    def sauverExif(self):
        Rep.sauveExifs()
        
    def deplacerPanorama(self):
        for th in self.__liste:
            if th.getPano():
                nom = th.getName()
                num_pano = th.getNomPano().split('_')[1]
                self.__album.deplacerPanorama(nom,num_pano)
#                 # deplacement de la photo
#                 shutil.move(rep_photo+nom,rep_cible)
#                 # destruction de la miniature
#                 os.remove(th.getChemin())
#                 # retrait des infos
#                 self.infos.retire(nom)
        self.__album.refresh()
        
    def renommerPanorama(self):
        print("renommerPanorama")
        prec = None
        try:
            nums = set([int(s.split('_')[1]) for s in self.__album.listePano()])
            num_pano = max(nums) + 1
        except:
            num_pano = 0
        num_photo = 1
        for th in self.__liste:
            if th.getPano():
                nom = th.getName()
                exif = self.__album.getExif(nom)
                cour = Exif.getChTriDate(exif)
                if not prec or abs(cour-prec) > dt.timedelta(0,5):
                    num_pano += 1
                    num_photo = 1
                self.__album.renommerPhoto(nom,PREFERENCES.NOM_PANO+str(num_pano)+"_"+str(num_photo)+".JPG")
                prec = cour
                num_photo += 1
                #self.__album.deplacerPanorama(nom)
        self.__album.sauveInfos()
        self.__album.refresh()
                
    def copieRetouche(self,rep_photo,rep_cible):
        for th in self.__liste:
            if th.getRetouche():
                nom = th.getName()
                #new_nom =  "%s_2%s" % osp.splitext(nom)
                # copie de la photo, on garde le m�me nom car quand on r�cup�re on incr�mente
                shutil.copy(osp.join(rep_photo,nom),osp.join(rep_cible,nom))
                
    def detectionAutomatique(self,debut=None,num_init=None):
        # debut est positionn� quand la fonction est appel� depuis la fonction renommerPanorama de IhmMiniatures
        l = []
        ok = True
        for th in self.__liste:
            if debut: ok = th.getNumero() >= debut
            if ok:
                exif = self.__album.getExif(th.getName())
                l.append([Exif.getChTriDate(exif),exif['correction'],th])
        ok = False 
        li = []
        if num_init:
            num_pano = num_init
        else:
            lpano = [int(osp.basename(p).split('_')[0]) for p in self.__album.listePano()]
            num_pano = 1
            if lpano: num_pano += 1 + max(set(lpano))
        for i in range(len(l)-1):
            #print abs(l[i][0]-l[i+1][0]),abs(l[i][0]-l[i+1][0]) < dt.timedelta(0,5)
            if abs(l[i][0]-l[i+1][0]) < dt.timedelta(0,5):
                ok = True
                li.append(i)
            else:
                ok = False
            if i == len(l)-2 and ok: 
                li.append(i+1)
                ok = False
            if li and not ok:
                li.append(i)
                lc = [l[j][1] for j in li]
                bpano = (lc == [lc[0]] * len(lc))
                #print bpano
                for j in li:
                    if bpano:
                        l[j][2].setPano(True)
                        l[j][2].setNomPano("pano_" + str(num_pano))
                    else:
                        l[j][2].setRetouche(True)
                li = []
                num_pano += 1

        
