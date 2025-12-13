
import os.path as osp
from common import Exif

class Filtre:
    def __init__(self,types_choix=[False,False,False,False],star=[None,None,None,None],autre=[None,None],\
            trait=[None,None],pano=[None,None],ret=[None,None],paysage=[None,None],nums=[0,0],dates=[],nom_selection='',filtre_nom="*.*"):
        """
        type_choix contient True si toutes ou infos ou nums ou dates est selectionne
        """
        self.__types_choix = types_choix
        self.__etoiles = star
        self.__autre = autre
        self.__traitee = trait
        self.__panorama = pano
        self.__retouche = ret
        self.__paysage = paysage
        self.__num_photos = nums
        self.__liste_dates = dates
        self.__selection = nom_selection
        self.__filtre_nom = filtre_nom
        
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
    
    def getAutre(self):
        return self.__autre
    
    def getTraitees(self):
        return self.__traitee
    
    def getPanorama(self):
        return self.__panorama
    
    def getRetouche(self):
        return self.__retouche
    
    def getPaysage(self):
        return self.__paysage
    
    def getNumPhotos(self):
        return self.__num_photos
    
    def getListeDates(self):
        return self.__liste_dates
    
    def getNomSelection(self):
        return self.__selection+'.sel'
    
    def getFiltreNom(self):
        return self.__filtre_nom
    
    def isOk(self,chemin,info,exif,n):
        from FenetreArborescence.renommage import chercheRe,cs
        import re as regExp
        if self.choixToutes():
            return True
        else:
            if self.getFiltreNom() != "*.*":
                nom_fich = osp.basename(chemin)
                filtre = str(self.getFiltreNom())
                ssf = cs(filtre)
                ssf = ssf.replace("*",".*")
                if not regExp.findall(ssf,nom_fich): return False
            if self.choixInfos():
                et = info["etoiles"]
                au = info["cochee"]
                tr = info["traitee"]
                pa = info["pano"]
                re = info["retouche"]
                ok_info = self.getEtoiles()[et] and self.getAutre()[au] and self.getTraitees()[tr] \
                        and self.getPanorama()[pa] and self.getRetouche()[re]
                try:
                    ok_info = ok_info and (self.getPaysage()[0] and not exif["paysage"] or self.getPaysage()[1] and exif["paysage"])
                except:
                    pass
                if not ok_info: return False
            if self.choixNums():
                nums = self.getNumPhotos()
                ok_num = (n >= nums[0]) and (n <= nums[1])
                if not ok_num: return False
            if self.choixDates():
                try:
                    j = exif['date']
                except:
                    j = 'aucune'
                ok_date = j in self.getListeDates()
                if not ok_date: return False
            return True
        
    def getPhotos(self,album):
        liste_tot = album.listeJPG()
        infos = album.getInfos()
        exifs = album.getExifs()
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
