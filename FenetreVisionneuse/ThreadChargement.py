## -*- coding: utf-8 -*-
#"""
#Created on 5 juin 2011
#
#@author: Bureau
#"""
#
import time,sys,copy
from multiprocessing import Process, Pipe
import threading
from PyQt5 import QtCore,QtWidgets
from PyQt5.QtGui import QImage
from src import preferences as PREFERENCES
from src.IhmDiaporama import FenetreDiaporama

from Ihm.fen_visionneuse import Ui_Visionneuse as FormClass
from PyQt5.QtWidgets import QWidget as BaseClass
from PyQt5 import QtWidgets
 
class ThreadPhoto(threading.Thread):
    courant = None
    nb = 0
    ht_pos = {}    
    rep_photos = None
    liste_fichiers = None
    charges = {}
    lock = threading.Lock()

    def __init__(self):
        threading.Thread.__init__(self)
        
    def reinit(self):
        self.courant = None
        self.nb = 0
        self.ht_pos = {}    
        self.rep_photos = None
        self.liste_fichiers = None
        self.charges = {}
    
    def get(self,nom):
        self.locker()
        self.courant = ThreadPhoto.ht_pos[nom]
        self.delocker()
        if not self.contient(self.courant):
            self.charger(self.courant)
        ret = self.revoie(self.courant)
        return ret
    
    def decharger(self,l_num):
        self.locker()
        while len(l_num) > 0:
            ThreadPhoto.charges.pop(l_num.pop())
        self.delocker()
         
    def charger(self,num):
        self.locker()
        if num>-1 and num<ThreadPhoto.nb:
            f = ThreadPhoto.liste_fichiers[num]
            if ThreadPhoto.rep_photos:
                f = ThreadPhoto.rep_photos+'/'+f
            ThreadPhoto.charges[num] = QImage(f,'JPG')
            #image = Image.open(ThreadPhoto.rep_photos+'/'+f)
            #print getDesciptionImage(image)
            #sys.stdout.flush()
        self.delocker()
         
    def revoie(self,n):
        self.locker()
        ret = ThreadPhoto.charges[n]
        self.delocker()
        return ret
        
    def contient(self,n):
        self.locker()
        ret = n in ThreadPhoto.charges
        self.delocker()
        return ret
        
    def listeCharges(self):
        self.locker()
        charges = list(ThreadPhoto.charges.keys())
        self.delocker()
        return charges

    @staticmethod
    def locker():
        while ThreadPhoto.lock.locked():
            time.sleep(0.001)
        ThreadPhoto.lock.acquire()

    @staticmethod
    def delocker():
        ThreadPhoto.lock.release()
        
class Charge(ThreadPhoto):
    
    def __init__(self,bModeTri=True):
        ThreadPhoto.__init__(self)
        self.__cont = True
        self.__quitter_ok = False
        self.__mode_tri = bModeTri
        #self.repertoire = None
        
    def initialise(self,rep):
        # lock pour ne pas faire un get tant que ht_pos n'est pas valorisee
        ThreadPhoto.locker() 
        ThreadPhoto.rep_photos = rep
        
    def clear(self):
        self.initialise([])
        
    def getListeFichiers(self):
        while not ThreadPhoto.liste_fichiers:
            time.sleep(0.01)
        return ThreadPhoto.liste_fichiers
        
    def initialiseListeFichiers(self,liste_fichiers=[]):
        if liste_fichiers:
            ThreadPhoto.liste_fichiers = liste_fichiers
        else:
            from common import scanRep
            ThreadPhoto.liste_fichiers = scanRep.listeFichiers(ThreadPhoto.rep_photos,'JPG',bPath=False)
        ThreadPhoto.nb = len(ThreadPhoto.liste_fichiers)
        #ThreadPhoto.liste_fichiers.sort()
        i=0
        ThreadPhoto.ht_pos = {}
        ThreadPhoto.charges = {}
        for f in ThreadPhoto.liste_fichiers:
            ThreadPhoto.ht_pos[f]=i
            i+=1
        self.courant = 0
        # on peut delocker car ht_pos ok
        if ThreadPhoto.lock.locked(): ThreadPhoto.delocker()
        
    def run(self):
        if not self.__mode_tri:
            self.initialiseListeFichiers()
        while self.__cont:
            #try:
            charges = self.listeCharges()
            # monprint(charges)
            if type(self.courant) is int:
                a_charger = PREFERENCES.AUTO_CHARGEMENT+self.courant
                reste_a_charger = list(set(a_charger).difference(set(charges)))
                if reste_a_charger:
                    # chargement
                    while len(reste_a_charger) > 0:
                        pos = reste_a_charger.pop(0)
                        if pos>-1 and pos<self.nb:
                            self.charger(pos)  
                # dechargement
                a_decharger = set(charges).difference(set(a_charger))
                if a_decharger:
                    self.decharger(a_decharger)
            #except:
            #    print traceback.print_stack()
            #    print 'reinit charge'
            #    self.reinit()
            time.sleep(0.1)
        self.__quitter_ok = True
        
    def stop(self):
        self.__cont = False
        while not self.__quitter_ok:
            time.sleep(0.01)
