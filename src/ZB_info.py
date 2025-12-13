# -*- coding:utf-8 -*-
"""
Created on 12 juin 2011

@author: Bureau
"""
import os.path as osp
import copy,shutil
from codecs import *
import win32api, win32con
        
class Info:
    def __init__(self,nom,etoile,comment,infos):
        self.__nom = nom
        self.__etoiles = etoile
        self.__infos = infos
        vals = {'Sharp':False,'Traite':False,'Pano':False,'Retouche':False}
        if ';' in comment:
            for c in comment.split(';'):
                v = c.split('=')
                if v[1] == 'True': vals[v[0]] = True
                elif v[1] == 'False': vals[v[0]] = False
                else: vals[v[0]] = v[1]
        self.__nettete = vals['Sharp']
        self.__traite = vals['Traite']
        self.__panorama = vals['Pano']
        self.__retouche = vals['Retouche']
        
    def setNom(self,nom):
        self.__nom = nom
        
    def getEtoiles(self):
        return self.__etoiles
    
    def setEtoiles(self,n,b):
        prec = self.__etoiles
        self.__etoiles = n
        self.__infos.setModifiees(b)
        self.__infos.modifieNbInfosTotaux(prec,-1)
        self.__infos.modifieNbInfosTotaux(n,+1)
        
    def imposeEtoiles(self,n):
        # pour initialiser 
        self.__etoiles = n
        self.__infos.modifieNbInfosTotaux(n,+1)
        
    def getNettete(self):
        return self.__nettete
    
    def setNettete(self,n,b):
        self.__nettete = n
        self.__infos.setModifiees(b)
        self.__infos.modifieNbInfosTotaux(6,1*(n==True)-1*(n==False))
    
    def getTraite(self):
        return self.__traite
    
    def setTraite(self,n,b):
        if self.__traite != n:
            self.__traite = n
            self.__infos.setModifiees(b)
            self.__infos.setNbTraites(1*(n==True)-1*(n==False))
        
    def getPano(self):
        return self.__panorama
    
    def setPano(self,n,b):
        self.__panorama = n
        self.__infos.setModifiees(b)
        self.__infos.modifieNbInfosTotaux(4,1*(n==True)-1*(n==False))
    
    def getRetouche(self):
        return self.__retouche
    
    def setRetouche(self,n,b):
        self.__retouche = n
        self.__infos.setModifiees(b)
        self.__infos.modifieNbInfosTotaux(5,1*(n==True)-1*(n==False))
    
    def ecrire(self):
        entete = '<item:'+self.__nom+'>'
        etoile = '<Favourite_Photo>"'+str(self.__etoiles)+'"</Favourite_Photo>'
        comment = '<comment>"Sharp='+str(self.__nettete)+';Traite='+str(self.__traite)+';Pano='+str(self.__panorama)+';Retouche='+str(self.__retouche)+'"</comment>'
        fin = '</item:'+self.__nom+'>'
        return entete+'\n'+etoile+'\n'+comment+'\n'+fin+'\n'
    
    def __repr__(self):
        return self.__nom+' ('+str(self.__etoiles)+' '+str(self.__nettete)+' '+str(self.__traite)+')'
        
class ZBinfo:
    def __init__(self,rep):
        self.__liste_photos = [] # liste des noms pour l'ordre des photos
        self.__ht_photos = {}    # ht pour récupérer une photo par son nom
        self.__modifiees = False
        self.__nb_traites = 0
        self.__nb_infos_tot = [0,0,0,0,0,0,0]
        self.__nb_infos_aff = [0,0,0,0,0,0,0]
        self.__add = True
        self.__rep = rep
        if osp.isfile(self.chemin()):
            self.lire()
        self.maj()
        
    def maj(self):
        from RepertoirePhotos import RepPhotos as Rep
        l = Rep.listeJPG()
        if len(l) != len(self.__ht_photos):
            l.sort()
            for p in l:
                nom = osp.basename(p)
                if nom not in self.__ht_photos:
                    self.new(nom)
                        
    def chemin(self):
        from RepertoirePhotos import RepPhotos as Rep
        return Rep.fichierInfos()
    
    def lire(self):
        fich=open(self.chemin(),'r','utf16')
        num = 0
        self.__liste_photos = []
        while True:
            ligne=fich.readline()
            if not(ligne):
                break
            if '<item:' in ligne:
                nom = ligne.split(':')[1].split('>')[0]
                nb_etoile,comment = ('','')
            elif '<Favourite_Photo>' in ligne:
                nb_etoile = int(ligne.split('"')[1])
                self.__nb_infos_tot[nb_etoile] += 1
            elif '<comment>' in ligne:
                comment = ligne.split('"')[1]
            elif '</item:' in ligne:
                info = Info(nom,nb_etoile,comment,self)
                self.__liste_photos.append(nom)
                self.__ht_photos[nom] = info
                self.__nb_traites += self.__ht_photos[nom].getTraite()
                # il ne faut pas calculer les totaux pano, retouche, nettete
                # ce sera fait en selectionnant les checkbox
                self.__nb_infos_tot[4] += self.__ht_photos[nom].getPano()
                self.__nb_infos_tot[5] += self.__ht_photos[nom].getRetouche()
                self.__nb_infos_tot[6] += self.__ht_photos[nom].getNettete()
            num += 1
        fich.close()
    
    def get(self,nom):
        if nom in self.__ht_photos:
            return self.__ht_photos[nom]
        else:
            self.new(nom)
            
    def new(self,nom):
            info = Info(nom,0,"",self)
            self.__ht_photos[nom] = info
            self.__liste_photos.append(nom)
            return info
    
    def getListe(self,liste_miniatures):
        from RepertoirePhotos import RepPhotos as Rep   
        liste_miniatures.sort()
        for photo in copy.copy(self.__liste_photos):
            if not osp.isfile(Rep.repPhotos()+photo):
                self.retire(photo)
        for m in liste_miniatures:
            nom = osp.basename(m)
            if not nom in self.__liste_photos:
                self.get(nom)
        return self.__liste_photos
    
    def deplacer(self,liste,avant):
        # liste : noms a deplacer
        # avant : nom de la photo qui se retrouve a la suite
        index = self.__liste_photos.index(avant)
        for p in liste:
            self.__liste_photos.insert(index,self.__liste_photos.pop(self.__liste_photos.index(p)))
        self.__modifiees = True
        
    def remplacer(self,liste,liste1):
        lindex,n = [],0
        for p in liste:
            lindex.append(self.__liste_photos.index(p))
        for i in lindex:
            self.__liste_photos[i] = liste1[n]
            n += 1
        self.__modifiees = True
            
    def retire(self,nom):
        if nom in self.__ht_photos:
            self.__liste_photos.remove(nom)
            del self.__ht_photos[nom]
            self.__modifiees = True
        
    def renommer(self,old,new):
        if old in self.__ht_photos:
            i = self.__liste_photos.index(old)
            self.__liste_photos.insert(i,new)
            self.__liste_photos.remove(old)
            self.__ht_photos[new]=self.__ht_photos.pop(old)
            self.__ht_photos[new].setNom(new)
            self.__modifiees = True
    
    def fichierExiste(self):
        return osp.isfile(self.chemin())
    
    def ecrire(self):
        if osp.isfile(self.chemin()):
            win32api.SetFileAttributes(self.chemin(),win32con.FILE_ATTRIBUTE_NORMAL)
        fich=open(self.chemin(),'w','utf16')
        for photo in self.__liste_photos:
            fich.write(self.__ht_photos[photo].ecrire())
        fich.close()
        #win32api.SetFileAttributes(self.chemin(),win32con.FILE_ATTRIBUTE_HIDDEN)
        self.__modifiees = False
    
#    def reinit(self,new):
#        if osp.isfile(self.chemin()):
#            win32api.SetFileAttributes(self.chemin(),win32con.FILE_ATTRIBUTE_NORMAL)
#        shutil.copyfile(self.chemin(),new)
#        self.chemin() = new
#        #win32api.SetFileAttributes(self.chemin(),win32con.FILE_ATTRIBUTE_HIDDEN)
#        self.init()
        
    def setNbTraites(self,delta):
        self.__nb_traites += delta

    def getNbTraites(self):
        return self.__nb_traites
    
    def getNbInfosTotaux(self):
        return self.__nb_infos_tot
    
    def getNbInfosAffiches(self):
        return self.__nb_infos_aff
    
    def stopCalculTotaux(self,b):
        # il faut stopper l'ajout pendant la création des miniatures
        self.__add = not b
        
    def modifieNbInfosTotaux(self,ind,val):
        self.__nb_infos_tot[ind] += val * self.__add
        self.__nb_infos_aff[ind] += val
        
    def getNbPhotos(self):
        return len(self.__ht_photos)
    
    def modifiees(self):
        return self.__modifiees
    
    def setModifiees(self,b):
        self.__modifiees = b
        
    def __repr__(self):
        return str(self.__ht_photos)
    
if __name__ == "__main__":
    rep='C:\Documents and Settings\Bureau\Mes documents\Developpement logiciels\Workspace\Photo\photos\Thumbs/'
    zb=ZBinfo(rep)
    zb.lire()
    print(zb)
    elem = zb.get('Vietnam_20110426_0201.JPG')
    elem.setEtoiles(3)
    print(elem)
    print(zb)
    zb.ecrire()
    
    #nt.stat_result(st_mode=33206, st_ino=0L, st_dev=0, st_nlink=0, st_uid=0, st_gid=0, st_size=572L, st_atime=1307916000L, st_mtime=1307939092L, st_ctime=1307859932L)
    #nt.stat_result(st_mode=33206, st_ino=0L, st_dev=0, st_nlink=0, st_uid=0, st_gid=0, st_size=556L, st_atime=1307916000L, st_mtime=1307939554L, st_ctime=1307859932L)
