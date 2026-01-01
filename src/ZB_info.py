# -*- coding:utf-8 -*-
"""
Created on 12 juin 2011

@author: Bureau
"""
import os.path as osp
import copy,shutil
from codecs import *
import win32api, win32con
        
Classe inutilisée

class Info:
    def __init__(self,nom,etoile,comment,infos):
        self._nom = nom
        self._etoiles = etoile
        self._infos = infos
        vals = {'Sharp':False,'Traite':False,'Pano':False,'Retouche':False}
        if ';' in comment:
            for c in comment.split(';'):
                v = c.split('=')
                if v[1] == 'True': vals[v[0]] = True
                elif v[1] == 'False': vals[v[0]] = False
                else: vals[v[0]] = v[1]
        self._nettete = vals['Sharp']
        self._traite = vals['Traite']
        self._panorama = vals['Pano']
        self._retouche = vals['Retouche']
        
    def setNom(self,nom):
        self._nom = nom
        
    def getEtoiles(self):
        return self._etoiles
    
    def setEtoiles(self,n,b):
        prec = self._etoiles
        self._etoiles = n
        self._infos.setModifiees(b)
        self._infos.modifieNbInfosTotaux(prec,-1)
        self._infos.modifieNbInfosTotaux(n,+1)
        
    def imposeEtoiles(self,n):
        # pour initialiser 
        self._etoiles = n
        self._infos.modifieNbInfosTotaux(n,+1)
        
    def getNettete(self):
        return self._nettete
    
    def setNettete(self,n,b):
        self._nettete = n
        self._infos.setModifiees(b)
        self._infos.modifieNbInfosTotaux(6,1*(n==True)-1*(n==False))
    
    def getTraite(self):
        return self._traite
    
    def setTraite(self,n,b):
        if self._traite != n:
            self._traite = n
            self._infos.setModifiees(b)
            self._infos.setNbTraites(1*(n==True)-1*(n==False))
        
    def getPano(self):
        return self._panorama
    
    def setPano(self,n,b):
        self._panorama = n
        self._infos.setModifiees(b)
        self._infos.modifieNbInfosTotaux(4,1*(n==True)-1*(n==False))
    
    def getRetouche(self):
        return self._retouche
    
    def setRetouche(self,n,b):
        self._retouche = n
        self._infos.setModifiees(b)
        self._infos.modifieNbInfosTotaux(5,1*(n==True)-1*(n==False))
    
    def ecrire(self):
        entete = '<item:'+self._nom+'>'
        etoile = '<Favourite_Photo>"'+str(self._etoiles)+'"</Favourite_Photo>'
        comment = '<comment>"Sharp='+str(self._nettete)+';Traite='+str(self._traite)+';Pano='+str(self._panorama)+';Retouche='+str(self._retouche)+'"</comment>'
        fin = '</item:'+self._nom+'>'
        return entete+'\n'+etoile+'\n'+comment+'\n'+fin+'\n'
    
    def __repr__(self):
        return self._nom+' ('+str(self._etoiles)+' '+str(self._nettete)+' '+str(self._traite)+')'
        
class ZBinfo:
    def __init__(self,rep):
        self._liste_photos = [] # liste des noms pour l'ordre des photos
        self._ht_photos = {}    # ht pour récupérer une photo par son nom
        self._modifiees = False
        self._nb_traites = 0
        self._nb_infos_tot = [0,0,0,0,0,0,0]
        self._nb_infos_aff = [0,0,0,0,0,0,0]
        self._add = True
        self._rep = rep
        if osp.isfile(self.chemin()):
            self.lire()
        self.maj()
        
    def maj(self):
        from RepertoirePhotos import RepPhotos as Rep
        l = Rep.listeJPG()
        if len(l) != len(self._ht_photos):
            l.sort()
            for p in l:
                nom = osp.basename(p)
                if nom not in self._ht_photos:
                    self.new(nom)
                        
    def chemin(self):
        from RepertoirePhotos import RepPhotos as Rep
        return Rep.fichierInfos()
    
    def lire(self):
        fich=open(self.chemin(),'r','utf16')
        num = 0
        self._liste_photos = []
        while True:
            ligne=fich.readline()
            if not(ligne):
                break
            if '<item:' in ligne:
                nom = ligne.split(':')[1].split('>')[0]
                nb_etoile,comment = ('','')
            elif '<Favourite_Photo>' in ligne:
                nb_etoile = int(ligne.split('"')[1])
                self._nb_infos_tot[nb_etoile] += 1
            elif '<comment>' in ligne:
                comment = ligne.split('"')[1]
            elif '</item:' in ligne:
                info = Info(nom,nb_etoile,comment,self)
                self._liste_photos.append(nom)
                self._ht_photos[nom] = info
                self._nb_traites += self._ht_photos[nom].getTraite()
                # il ne faut pas calculer les totaux pano, retouche, nettete
                # ce sera fait en selectionnant les checkbox
                self._nb_infos_tot[4] += self._ht_photos[nom].getPano()
                self._nb_infos_tot[5] += self._ht_photos[nom].getRetouche()
                self._nb_infos_tot[6] += self._ht_photos[nom].getNettete()
            num += 1
        fich.close()
    
    def get(self,nom):
        if nom in self._ht_photos:
            return self._ht_photos[nom]
        else:
            self.new(nom)
            
    def new(self,nom):
            info = Info(nom,0,"",self)
            self._ht_photos[nom] = info
            self._liste_photos.append(nom)
            return info
    
    def getListe(self,liste_miniatures):
        from RepertoirePhotos import RepPhotos as Rep   
        liste_miniatures.sort()
        for photo in copy.copy(self._liste_photos):
            if not osp.isfile(Rep.repPhotos()+photo):
                self.retire(photo)
        for m in liste_miniatures:
            nom = osp.basename(m)
            if not nom in self._liste_photos:
                self.get(nom)
        return self._liste_photos
    
    def deplacer(self,liste,avant):
        # liste : noms a deplacer
        # avant : nom de la photo qui se retrouve a la suite
        index = self._liste_photos.index(avant)
        for p in liste:
            self._liste_photos.insert(index,self._liste_photos.pop(self._liste_photos.index(p)))
        self._modifiees = True
        
    def remplacer(self,liste,liste1):
        lindex,n = [],0
        for p in liste:
            lindex.append(self._liste_photos.index(p))
        for i in lindex:
            self._liste_photos[i] = liste1[n]
            n += 1
        self._modifiees = True
            
    def retire(self,nom):
        if nom in self._ht_photos:
            self._liste_photos.remove(nom)
            del self._ht_photos[nom]
            self._modifiees = True
        
    def renommer(self,old,new):
        if old in self._ht_photos:
            i = self._liste_photos.index(old)
            self._liste_photos.insert(i,new)
            self._liste_photos.remove(old)
            self._ht_photos[new]=self._ht_photos.pop(old)
            self._ht_photos[new].setNom(new)
            self._modifiees = True
    
    def fichierExiste(self):
        return osp.isfile(self.chemin())
    
    def ecrire(self):
        if osp.isfile(self.chemin()):
            win32api.SetFileAttributes(self.chemin(),win32con.FILE_ATTRIBUTE_NORMAL)
        fich=open(self.chemin(),'w','utf16')
        for photo in self._liste_photos:
            fich.write(self._ht_photos[photo].ecrire())
        fich.close()
        #win32api.SetFileAttributes(self.chemin(),win32con.FILE_ATTRIBUTE_HIDDEN)
        self._modifiees = False
    
#    def reinit(self,new):
#        if osp.isfile(self.chemin()):
#            win32api.SetFileAttributes(self.chemin(),win32con.FILE_ATTRIBUTE_NORMAL)
#        shutil.copyfile(self.chemin(),new)
#        self.chemin() = new
#        #win32api.SetFileAttributes(self.chemin(),win32con.FILE_ATTRIBUTE_HIDDEN)
#        self.init()
        
    def setNbTraites(self,delta):
        self._nb_traites += delta

    def getNbTraites(self):
        return self._nb_traites
    
    def getNbInfosTotaux(self):
        return self._nb_infos_tot
    
    def getNbInfosAffiches(self):
        return self._nb_infos_aff
    
    def stopCalculTotaux(self,b):
        # il faut stopper l'ajout pendant la création des miniatures
        self._add = not b
        
    def modifieNbInfosTotaux(self,ind,val):
        self._nb_infos_tot[ind] += val * self._add
        self._nb_infos_aff[ind] += val
        
    def getNbPhotos(self):
        return len(self._ht_photos)
    
    def modifiees(self):
        return self._modifiees
    
    def setModifiees(self,b):
        self._modifiees = b
        
    def __repr__(self):
        return str(self._ht_photos)
    
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
