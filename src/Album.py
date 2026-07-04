# -*- coding: utf-8

try:
    from common import Photo,scanRep,Exif,Video
except:
    import importlib,sys
    sys.path.append("common")
    Photo = importlib.import_module("Photo")
    scanRep = importlib.import_module("scanRep")
    Exif = importlib.import_module("Exif")
    Video = importlib.import_module("Video")
import os.path as osp
import os,glob,shutil,pickle
import win32api, win32con
from PyQt5.QtCore import Qt

class ElementAlbum():

    def __init__(self,path,ht_exifs=None,ht_infos=None):
        self._path = path
        self._exif_album = ht_exifs
        self._info_album = ht_infos
        try:
            self._exif = self._exif_album[osp.basename(path)]
        except:
            self._exif = None
        try:
            self._info = self._info_album[osp.basename(path)]
        except:
            self._info = None
        self._index = None
        
    def getPath(self):
        return self._path
    
    def getThumbPath(self):
        return osp.join(osp.dirname(self._path),'TriPhotos','Thumbs',osp.basename(self._path).replace('mp4','jpg')).replace('\\','/')

    def getName(self):
        return osp.basename(self._path)
    
    def getExif(self):
        return self._exif
    
    def getInfo(self):
        if not self._info:
            self._info = {"etoiles" : 0,"traitee":False,"cochee":False,"pano":False,"retouche":False}
        return self._info
    
    def setEtoiles(self,n):
        self._info["etoiles"] = n

    def setTraite(self,b=True):
        self._info["traitee"] = b

    def deplacer(self, to_rep,only_remove=False):
        if only_remove:
            os.remove(self.getPath())
        else:
            Photo.deplacerPhoto(self._path,to_rep)
        os.remove(self.getThumbPath())
        if self.getName() in self._exif_album:
            del self._exif_album[self.getName()]
        if self.getName() in self._info_album:
            del self._info_album[self.getName()]

    def __lt__(self,other):
        dc = Exif.getChTriDate(self._exif)
        do = Exif.getChTriDate(other._exif)
        return dc < do

class PhotoAlbum(ElementAlbum):
    def __init__(self,path,ht_exifs=None,ht_infos=None):
        super().__init__(path,ht_exifs,ht_infos)

    def getExif(self):
        if not self._exif:
            self._exif = Exif.getHt(image=self._path)
            self._exif_album[osp.basename(self._path)] = self._exif
        return self._exif
    
    def creerThumbnail(self):
        Photo.creerThumbnail(self._path,self.getThumbPath())

    def verifExtension(self):
        if self._path.endswith('.JPG'):
            newpath = self._path[:-3] + 'jpg'
            shutil.move(self._path,newpath)
            self._path = newpath

class VideoAlbum(ElementAlbum):
    def __init__(self,path,ht_exifs=None,ht_infos=None):
        super().__init__(path,ht_exifs,ht_infos)

    def getExif(self):
        if not self._exif:
            self._exif = Video.get_metadata_ffmpeg(self._path)
            self._exif_album[osp.basename(self._path)] = self._exif
        return self._exif
    
    def creerThumbnail(self):
        Video.creerThumbnail(self._path,self.getThumbPath())

    def verifExtension(self):
        if self._path.endswith('.MP4'):
            newpath = self._path[:-3] + 'mp4'
            shutil.move(self._path,newpath)
            self._path = newpath

class Album():
    def __init__(self,rep,ihm_arbo,verif_album=False):
        # lien vers l'ihm pour la progressbar
        if rep[-1] != '/':
            self._repertoire = rep +"/"
        self._infos = None
        self._exifs = None
        self._dates = []
        self.initMetadata()
        self._liste_elements = []
        self._liste_noms_elements = []
        self._liste_thumbs = []
        self._ht_noms_elements = {}
        self.creerListeElements()
        self.listeThumbs()
        self._ihm = ihm_arbo
        self._infos_sauvees = True
        if verif_album:
            self.refresh()
        
    def initMetadata(self):    
        self.lireDates()
        self.lireExifs()
        self.lireInfos()

    def refresh(self):
        self._liste_noms_elements = []
        elem = self.getFirstPhoto()
        if elem:
            self.creerDossiers()
            self.verifExtensions()
            self.recuperationPhotos()
            if not self.miniaturesOk():
                self.majMiniatures()
            else:
                print("Miniatures OK",len(self._liste_elements))           
        else:
            self.detruireDossiers()
    
    def change(self,rep):
        self._repertoire = rep
        self._infos = {}
        self._exifs = {}
        self._dates = []
        self._liste_noms_elements = []
        self._liste_thumbs = []
        if rep:
            self.creerDossiers()
    
    def creerDossiers(self):
        if not osp.isdir(self.repTriPhotos()):
            creer(self.repTriPhotos())
            win32api.SetFileAttributes(self.repTriPhotos(),win32con.FILE_ATTRIBUTE_HIDDEN)
            creer(self.repThumbs())
            creer(self.repPano())
            creer(self.repRecup())
            creer(self.repRetouche())
            creer(self.repSelections())
    
    def detruireDossiers(self):
        if not self.getFirstPhoto():
            detruire(self.repTriPhotos())
            detruire(self.repThumbs())
            detruire(self.repPano())
            detruire(self.repRecup())
            detruire(self.repRetouche())
            detruire(self.repSelections())
    
    def verifExtensions(self):
        # verifie que les extensions des fichiers correspondent bien
        # sinon renomme les fichiers
        for elem in self._liste_elements:
            elem.verifExtension()

    def basename(self):
        if self._repertoire[-1] == '/':
            rep = self._repertoire[:-1]
        else:
            rep = self._repertoire
        return osp.basename(rep)
            
    def majMiniatures(self):
        if self._ihm:
            self._ihm.initProgressBar(len(self._liste_elements))
        n=0
        i=0
        print("Maj miniatures album",len(self._liste_elements))
        for elem in self._liste_elements:
            name = elem.getName()
            if self._ihm:
                stop = self._ihm.avanceProgressBar(n,name)
                if stop: break
            thumbPath = elem.getThumbPath()
            if not osp.isfile(thumbPath) or not elem.getExif():
                # creation de la miniature qui n'existe pas
                # exif
                exif = elem.getExif()
                if 'pivoter' in exif and exif['pivoter']:
                    elem._exif = Photo.fairePivoterPhoto(elem.getPath(),exif)
                # date
                if 'date' in exif:
                    date = exif['date']
                    if not date in self._dates:
                        self._dates.append(date)
                # infos
                self._infos[name] = {"etoiles" : 0,"traitee":False,"cochee":False,"pano":False,"retouche":False}
                # thumb
                if not osp.isfile(thumbPath):
                    elem.creerThumbnail()
                    i+=1
                    #self.ajouteJPGThumbs(thumbPath)
            n+=1
        # destruction des miniatures en trop
        min_trop = self.miniaturesEnTrop()
        if min_trop:
            self.detruirePhotos(lbasename(min_trop))
        self.sauverExifsInfosDates(False)
        print("Miniatures créées :",i)
        if self._ihm:
            self._ihm.stopProgressBar()
            
    def sauverExifsInfosDates(self,recreer_dates=True):
        self.sauveExifs()
        self.sauveInfos()
        if recreer_dates:
            self.recreerDates()
        self.sauveDates()

    def creerListeElements(self,chemin=True):
        if self._repertoire:
            for chemin in scanRep.listeFichiers(self._repertoire,['JPG','MP4']):
                if chemin.lower().endswith('.jpg'):
                    self._liste_elements.append(PhotoAlbum(chemin,self._exifs,self._infos))
                elif chemin.lower().endswith('.mp4'):
                    self._liste_elements.append(VideoAlbum(chemin,self._exifs,self._infos))
        self._liste_elements.sort(key=lambda x: x.getPath())

    def listeObjElements(self):
        return self._liste_elements
    
    def listePathElements(self):
        return [elem.getPath() for elem in self._liste_elements]
    
    def listeNomsElements(self):
        return [elem.getName() for elem in self._liste_elements]
    
    def pivoterPhoto(self,thumb):
        name_photo = thumb.getName()
        elem = self.getObjElement(name_photo)
        exif_ht = elem.getExif()
        if type(elem) == PhotoAlbum:
            photo = elem.getPath()
            exif_ht = Photo.fairePivoterPhoto(photo,exif_ht)
            elem.creerThumbnail()
        else:
            video = elem.getPath()
            if 'pivoter' in exif_ht:
                exif_ht['pivoter'] = exif_ht['pivoter'] + 90
            else:
                exif_ht['pivoter'] = 90
            self._exifs[video] = exif_ht
            self.sauveExifs()
        elem._exif = exif_ht
    #     def getInfos(self):
#         return self._infos
#     
#     
#     def getInfo(self,nom):
#         if '/' in nom:
#             nom = osp.basename(nom)
#         return self._infos.get(nom)
#     
#     
    def setCommentaire(self,commentaire):
        if osp.isdir(self.repTriPhotos()):
            with open(self.repTriPhotos()+'Commentaire.dat','w') as f:
                f.write(commentaire.replace('\n\n','\n'))

    def getCommentaire(self):
        commentaire = ''
        try:
            with open(self.repTriPhotos()+'Commentaire.dat','r') as f:
                commentaire = f.read()
        except:
            pass
        return commentaire
#
#  Infos
#
    def fichierInfos(self):
        return self.repTriPhotos()+'Infos.dat'
    
    def lireInfos(self):
        import json
        try:
            with open(self.fichierInfos(),'r') as f:
                self._infos = json.load(f)
        except:
            self._infos = {}
        
    def verif_infos(self):
        if self._infos:
            if len(self._infos[list(self._infos.keys())[0]]) < 5:
                for nom,ht in list(self._infos.items()):
                    if not "etoiles" in list(ht.keys()):
                        self._infos[nom]["etoiles"] = 0
                    if not "traitee" in list(ht.keys()):
                        self._infos[nom]["traitee"] = False
                    if not "cochee" in list(ht.keys()):
                        self._infos[nom]["cochee"] = False
                    if not "pano" in list(ht.keys()):
                        self._infos[nom]["pano"] = False
                    if not "retouche" in list(ht.keys()):
                        self._infos[nom]["retouche"] = False
                self.sauveInfos()
            
    def sauveInfos(self):
        import json
        if osp.isdir(self.repTriPhotos()):
            with open(self.fichierInfos(),'w') as f:
                json.dump(self._infos,f,indent=2)
        self._infos_sauvees = True
    
    def getInfos(self):
        return self._infos
    
    def getInfo(self,nom):
        try:
            if '/' in nom:
                nom = osp.basename(nom)
            return self._infos[nom]
        except:
            print("Info",nom,"introuvable")
            return {"etoiles" : 0,"traitee":False,"cochee":False,"pano":False,"retouche":False}
    
    def setInfo(self,nom,cle,val):
        if nom not in self._infos:
            self._infos[nom] = {"etoiles" : 0,"traitee":False,"cochee":False,"pano":False,"retouche":False}
        self._infos[nom][cle] = val
        self._infos_sauvees = False
        
    def infosSauvees(self):
        return self._infos_sauvees

#
# selection
#   

    def repSelections(self):
        return self.repTriPhotos()+'Selections/'
    
    def listeSelections(self):
        return lbasename(glob.glob(self.repSelections()+'*.sel'))
    
    def sauveSelection(self,fich,liste_photos):
        if not fich.endswith('.sel'): fich += '.sel'
        with open(fich,'w') as f:
            for p in liste_photos:
                f.write(p+"\n")
    
    def lireSelection(self,fich):
        if not '/' in fich: fich = self.repSelections() + fich
        with open(fich,'r') as f:
            return [s.replace("\n","") for s in f.readlines()]
        
#
#  Exifs
#
    def lireExifs(self):
        import json
        if self._exifs: print("Exif",self._exifs.keys())
        try:
            with open(self.fichierExifs(),'r') as f:
                self._exifs = json.load(f)
        except:
            self._exifs = {}
        
    def getExifs(self):
        return self._exifs
    
    def getExif(self,nom):
        try:
            if '/' in nom:
                nom = osp.basename(nom)
            return self._exifs[nom]
        except:
            print("Exif",nom,"introuvable")
            return None
    
    def setExifs(self,ht):
        self._exifs = ht
        
    def fichierExifs(self):
        return self.repTriPhotos()+'Exifs.dat'
    
    def sauveExifs(self):
        import json
        with open(self.fichierExifs(),'w') as f:
            json.dump(self._exifs,f,indent=2)

    def ajouteExif(self,chemin_photo):
        exif_im = Exif.loadExif(chemin_photo)
        self._exifs[osp.basename(chemin_photo)] = Exif.getHt(exif_im)
    
#
#  Dates
#
    def lireDates(self):
        try:
            with open(self.fichierDates(),'rb') as f:
                self._dates = pickle.load(f)
        except:
            self._dates = []
                
    def getDates(self):
        if not self._dates:
            self.lireDates()
        return self._dates
        
    def recreerDates(self):
        self._dates = []
        for name,exif in list(self._exifs.items()):
            date = exif['date']
            if not date in self._dates:
                self._dates.append(date)
                    
    def getListeDates(self):
        from datetime import date
        vdates = set(self.getDates())
        if 'unknown' in vdates:
            vdates.remove('unknown')
            add = ['unknown']
        else:
            add = []
        d = [date(int(l[2]),int(l[1]),int(l[0])) for l in [k.split('/') for k in vdates]]
        d.sort()
        return [g.strftime("%d/%m/%Y") for g in d] + add
        
    def sauveDates(self): 
        import json
        with open(self.fichierDates(),'w') as f:
            json.dump(self._dates,f,indent=2)
        
    def fichierDates(self):
        return self.repTriPhotos()+'Dates.dat'
    
#
#  Gestion des r�pertoires
#
    def repertoire(self):
        from pathlib import Path
        return Path(self._repertoire).as_posix()
    
    def estUnAlbum(self):
        return bool(self._repertoire and osp.isdir(self._repertoire) and self.listePathElements() and osp.isdir(self.repTriPhotos()))
    
    def repTriPhotos(self):
        return self._repertoire+'TriPhotos/'
   
    def repThumbs(self):
        return self.repTriPhotos()+'Thumbs/'
   
    def repPano(self):
        return self.repTriPhotos()+'Pano/'

    def listePano(self):
        return scanRep.listeFichiers(self.repPano(),['JPG'])
        #return os.listdir(self.repPano())

    def repRecup(self):
        return self.repTriPhotos()+'Recuperation/'

    def listeRecup(self):
        return scanRep.listeFichiers(self.repRecup(),['JPG'])
        #return os.listdir(self.repRecup())

    def repRetouche(self):
        return self.repTriPhotos()+'Retouche/'
    
    def listeRetouche(self):
        return scanRep.listeFichiers(self.repRetouche(),['JPG'])
        #return os.listdir(self.repRetouche())

    def getFirstPhoto(self):
        return scanRep.first(self._repertoire,'.jpg') or scanRep.first(self._repertoire,'.mp4')
    
    def retireJPG(self,photo):
        l = self._liste_noms_elements
        if photo in l:
            l.pop(l.index(photo))
    
    def listeObjTrieParDate(self):
        ltri=[]
        for elem in self.listeObjElements():
            exif = elem.getExif()
            ltri.append((Exif.getChTriDate(exif),elem))
        ltri.sort()
        return [v[1] for v in ltri]
            
    def reinitListeElements(self):
        self._liste_noms_elements = []
        self._liste_thumbs = []
    
    def listeThumbs(self):
        if not self._liste_thumbs:
            self._liste_thumbs = scanRep.listeFichiers(self.repThumbs(),['JPG'])
        return self._liste_thumbs
    
    def getJPGThumb(self,nom):
        return self.repThumbs()+nom
    
    def getJPGPath(self,nom):
        return osp.join(self._repertoire,nom)
    
    def getObjElement(self,nom):
        for elem in self._liste_elements:
            if elem.getName() == nom:
                return elem
        return None
        
    def ajouteJPGThumbs(self,thumb):
        self._liste_thumbs.append(thumb)
    
    def retireJPGThumbs(self,photo):
        l = self._liste_thumbs
        if photo in l:
            l.pop(l.index(photo))
    
    def listeIndexJPG(self):
        return self._ht_noms_elements
    
    def miniaturesOk(self):
        for elem in self._liste_elements:
            if not osp.isfile(elem.getThumbPath()):
                return False
            if not elem.getName() in self._exifs:
                return False        
        return True
        # s = set(lbasename(self.listePathElements()))
        # sm = set(lbasename(self.listeThumbs()))
        # nb = len(self._exifs)
        # return s == sm and len(s)== nb
    
    def miniaturesEnTrop(self):
        s = set([elem.getThumbPath() for elem in self._liste_elements])
        sm = set(self.listeThumbs())
        return sm.difference(s)
    
    def listeJPGRecup(self):
        return glob.glob(self.repRecup()+'*.JPG')
    
    def recuperationPhotos(self):
        l = self.listeJPGRecup()
        for f in l:
            # deplacement avec indi�age
            Photo.deplacerPhoto(f,self._repertoire)
    
    def listeJPGFiltres(self,filtre):
        lret = []
        n=0
        for chemin in self.listePathElements():
            nom = osp.basename(chemin)
            exif = self._exifs[nom]
            info = self._infos[nom]
            ok = filtre.isOk(chemin,info,exif,n)
            if ok:
                lret.append(chemin)
            n+=1
        return lret
    
    def listeJPGFiltresNom(self,filtre_nom):
        import re
        lret = []
        filtre_nom = filtre_nom.replace('*',".*").replace('.',r"\.").replace('?',".")
        for chemin in self.listePathElements():
            nom = osp.basename(chemin)
            if re.findall(filtre_nom,nom):
                lret.append(chemin)
        return lret
    
    # video MP4
    def listeMP4(self,chemin=True):
        if self._repertoire and not self._liste_mp4:
            self._liste_mp4,self._ht_noms_elements = scanRep.listeFichiers(self._repertoire,['MP4'],bIndex=True)
        if chemin:
            return self._liste_mp4
        else:
            return lbasename(self._liste_mp4)
        
    def reinitialiser(self):
        detruire(self.repTriPhotos())
    
    def detruireMiniatures(self):
        detruire(self.repThumbs())
        self._liste_thumbs = []
        self._exifs = {}
        self._dates = []
        self._infos = {}
        creer(self.repThumbs())
        
    def deplacerPanorama(self,nom,str_num):
        shutil.move(self.repertoire()+nom,self.repPano() + str_num + "_" + nom)
            
    def renommerPhoto(self,nom,nom1):
        shutil.move(self.repertoire()+nom,self.repertoire()+nom1)
        shutil.move(self.repThumbs()+nom,self.repThumbs()+nom1)
        self._liste_noms_elements.remove(self.repertoire()+nom)
        self._liste_thumbs.remove(self.repThumbs()+nom)
        self._liste_noms_elements.append(self.repertoire()+nom1)
        self._liste_thumbs.append(self.repThumbs()+nom1)
        self._exifs[nom1] = self._exifs[nom]
        self._infos[nom1] = self._infos[nom]
        del self._exifs[nom]
        del self._infos[nom]
        self.sauverExifsInfosDates()
        
#
#  Ajout / retrait photos
#
    def detruirePhotos(self,lphotos):
        for photo in lphotos:
            try:
                chemin_photo = self.repertoire()+photo
                if osp.isfile(chemin_photo):
                    os.remove(chemin_photo)
                    self.retireJPG(chemin_photo)
                chemin_min = self.repThumbs()+photo
                if osp.isfile(chemin_min):
                    os.remove(chemin_min)
                    self.retireJPGThumbs(chemin_min)
                if photo in self._exifs:
                    del self._exifs[photo]
            except:
                print('Erreur � la destruction de la photo :',photo)         
        self.sauverExifsInfosDates()
#
#  Autres
#

    def nomCommun(self,rep=None):
        # renvoi la partie commune des noms des photos d'un repertoire
        if not rep:
            l = lbasename(self.listePathElements())
        else:
            l = lbasename(glob.glob(rep+'/*.JPG'))
        nom = ''
        if l:
            nom = l[0]
            for n in l[1:]:
                nom = chCom(nom,n)
        return nom
        
    def __repr__(self):
        def aj(l,b=True):
            m = ""
            if not l:return ""
            for i in l:
                if b: m += " "+osp.basename(i)+" "
                else: m += " "+i+" "
            return m
        mess = osp.basename(self._repertoire[:-1]) + "\n"
        mess += aj(self._liste_noms_elements) + "\n"
        mess += aj(self._liste_thumbs) + "\n"
        mess += aj(list(self._exifs.keys())) + "\n"
        mess += aj(self._dates,False) + "\n"
        return mess
        
def creer(r):
    if not osp.isdir(r):
        os.mkdir(r)

def detruire(r):
    if osp.isdir(r):
        shutil.rmtree(r)
        
def chCom(s,s1):
    if s == s1[0:len(s)]:
        return s
    r = ''
    for i in range(0,min(len(s),len(s1))):
        if s[i] != s1[i]:
            return r
        else:
            r += s[i]
    return r

def lbasename(l):
    return [osp.basename(p) for p in l]

if __name__ == "__main__":
    a=Album("C:/Users/Marc/Pictures/EOS_77D/2024-06",None,False)
    print(a.repertoire())
    print(a.estUnAlbum())
    a.refresh()
    print()
    