# -*- coding: latin-1
"""
Created on 4 juin 2011

@author: Bureau
"""
import os,glob,shutil,pickle
import os.path as osp
from PIL import Image
from common import Exif
import win32api, win32con
from PyQt5 import QtWidgets
from PyQt5.QtCore import Qt
from PyQt5.QtWidgets import QApplication,QMessageBox
from src import preferences as PREFERENCES
#from Album import Album

def creerThumbnail(ch_photo,ch_thumbnail,exif_im=None):
    im = Image.open(ch_photo)
    try:
        im.thumbnail((PREFERENCES.LARGEUR_IMAGE,PREFERENCES.LARGEUR_IMAGE), Image.ANTIALIAS)
    except:
        pass
    if exif_im:
        im.save(ch_thumbnail,"JPEG",exif=exif_im)
    else:
        im.save(ch_thumbnail,"JPEG")
    
# def creerMiniatures(parent,album):
#     sf
#     l = album.listeJPG()
#     l.sort()
#     parent.progressBar.show()
#     parent.bt_annuler_progress.show()
#     parent.fichier_progress.show()
#     parent.progressBar.setValue(0)
#     parent.progressBar.setMaximum(len(l))
#     n=0
#     ht_exif = {}
#     ht_exifs_prec = album.getExifs()
#     for im in l:
#         if parent.progressStoppe():
#             return
#         name = osp.basename(im)
#         parent.progressBar.setValue(n)
#         parent.fichier_progress.setText(name)
#         QApplication.instance().processEvents()
#         th = album.repThumbs()+name
#         if not osp.isfile(th):
#             # creation de la miniature qui n'existe pas
#             exif_im = Exif.loadExif(im)
#             exif_ht = Exif.getHt(exif_im)
#             if exif_ht.has_key('orientation'):
#                 orient = exif_ht['orientation']
#                 if orient:
#                     exif_im,exif_ht = fairePivoterPhoto(im,exif_ht,exif_im)
#             ht_exif[name] = exif_ht
#             creerThumbnail(im,th,(preferences.LARGEUR_IMAGE,preferences.LARGEUR_IMAGE),exif_im)
#             #Exif.saveExif(th,exif_im)
#             win32api.SetFileAttributes(th,win32con.FILE_ATTRIBUTE_HIDDEN)
#             album.ajouteJPGThumbs(th)
#         elif ht_exifs_prec.has_key(name):
#             # le thumb existe
#             ht_exif[name] = ht_exifs_prec[name]
#         else:
#             exif_im = Exif.loadExif(im)
#             exif_ht = Exif.getHt(exif_im)
#             ht_exif[name] = exif_ht
#         n+=1
#     # destruction des miniatures en trop
#     for i in album.miniaturesEnTrop():
#         os.remove(album.repThumbs()+osp.basename(i))
#         album.retireJPGThumbs(i)
#     #win32api.SetFileAttributes(album.repThumbs(),win32con.FILE_ATTRIBUTE_HIDDEN)
#     album.setExifs(ht_exif)
#     album.sauveExifs()
#     parent.progressBar.hide()
#     parent.fichier_progress.hide()
#     parent.bt_annuler_progress.hide()
#     parent.__progress_stoppe = True

#def creerExifPhotos():
#    l = Rep.listeJPG()
#    #l.sort()
#    progress = QtWidgets.QProgressDialog('Cr�ation des donn�es Exif','Annuler',0,len(l))
#    progress.setWindowTitle('Creation information Exif')
#    progress.setValue(0)
#    progress.show()
#    n=0
#    ht_exif = {}
#    for im in l:
#        if progress.wasCanceled():
#            return
#        name = osp.basename(im)
#        progress.setValue(n)
#        progress.setLabelText(name)
#        QApplication.instance().processEvents()
#        ht_exif[name] = Exif.getHt(Exif.getExif(im))
#        n+=1
#    saveExifPhotos(Rep.fichierExifs(),ht_exif) 

    
def fairePivoterPhoto(photo,exif_ht,exif_im):
    print('-> rotation de ',photo,exif_ht["pivoter"])
    image = Image.open(photo)
    im_rot = image.rotate(exif_ht["pivoter"])
    im_rot.save(photo,format="JPEG")
    exif_im[exif_ht["ifd_orientation"]][exif_ht["tag_orientation"]] = 0
    exif_ht['pivoter'] = 0
    Exif.saveExif(photo,exif_im)
    return exif_im,exif_ht
     
def creerSelection(ihm,liste_images,rep_cible,prefixe,options):
    copie = options[0]
    reduc = options[1]
    qualite = options[2]
    liste_images.sort()
    ihm.initProgressBar(len(liste_images))
    n=0
    for f in liste_images:
        name = os.path.basename(f)
        f_cible = rep_cible+'/'+prefixe+name
        if copie:
            shutil.copyfile(f,f_cible)
        else:
            image = Image.open(f)
            image = image.resize((int(image.size[0]/reduc),int(image.size[1]/reduc)))
            image.save(f_cible,format="JPEG",quality=qualite)

            Exif.saveExif(f_cible,Exif.loadExif(f))
        n+=1
        stop = ihm.avanceProgressBar(n,name)
        if stop: break
    ihm.stopProgressBar()

def detruirePhoto(album,nom):
    try:
        os.remove(album.repertoire()+"/"+nom)
        os.remove(album.repThumbs()+"/"+nom)
    except:
        print('impossible de detruire le fichier :',nom)
                
# def renommerPhoto(rep,nom_fich,nouveau):
#     if not osp.isfile(rep+nouveau):
#         os.rename(rep+nom_fich,rep+nouveau)
#         os.rename(album.repThumbs()+nom_fich,album.repThumbs()+nouveau)

def deplacerPhoto(path_photo,rep_cible,remove=True):
    if rep_cible[-1] != '/':
        rep_cible += '/'
    #si le fichier cible existe, on indice
    cible = rep_cible+osp.basename(path_photo)
    i = 1
    while osp.isfile(cible):
        if i == 1:
            cible = cible[:-4] + '_' + str(i) + cible[-4:]
        else:
            cible = cible[:-5] + str(i) + cible[-4:]
        i += 1
    # deplacement
    shutil.copy(path_photo,cible)
    if remove:
        os.remove(path_photo)

if __name__ == "__main__":
    #creerThumbnail('../photos/Vietnam_20110424_0054.JPG','thumb.jpg',(256,256))
    f = '../photos3/test 008'
    for q in range(11):
        print(q)
        image = Image.open(f+'.jpg')
        image.save(f+'.'+str(90+q)+'.jpg',format="JPEG",quality=90+q)
    
    
    