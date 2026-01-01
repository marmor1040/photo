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
from PyQt5.QtWidgets import QApplication,QDesktopWidget
from PyQt5.QtCore import Qt,QPoint,QSize,QRect,pyqtSlot,pyqtSignal
from PyQt5.QtCore import QObject
from src import preferences as PREFERENCES
from src.IhmDiaporama import FenetreDiaporama

from Ihm.fen_visionneuse import Ui_Visionneuse as FormClass
from PyQt5.QtWidgets import QWidget as BaseClass
from PyQt5 import QtWidgets
from .ThreadChargement import ThreadPhoto

class Affiche(ThreadPhoto,QObject):
    value_changed = pyqtSignal(str,str)
    
    def __init__(self,charge,Pout):
        ThreadPhoto.__init__(self)
        QObject.__init__(self,None)
        self._charge = charge
        self._pipe_out = Pout
        self._tab={}

    def affiche(self,v):
        print("nom =",v)
        
    def run(self):
        cont = True
        nom = None
        while cont:
           # try:
            #print 'recv',self._pipe_out
            nom = self._pipe_out.recv()
            if nom == '##quitter##':
                self._charge.stop()
                cont = False
                #if self._ihm.isVisible():
            elif '##repertoire##' in nom:
                rep = nom.replace('##repertoire##','')
                # pour arreter le chargement auto des photos
                self._charge.courant = None
                # changement du repertoire
                self._charge.initialise(rep)
            elif '##photos##' in nom:
                liste = eval(nom.replace('##photos##',''))
                # création de la liste des photos
                #print 'photos :',liste
                if liste:
                    self._charge.initialiseListeFichiers(liste)
            elif '##geometrie##' in nom:
                taille= eval(nom.replace('##geometrie##',''))
                self._ihm.setGeometry(taille)
            elif '##affiche##' in nom:
                if ThreadPhoto.rep_photos:
                    nom,etoiles,traite = nom.replace('##affiche##','').split(';')
                    if traite == "False":
                        etoiles = ""
                    else:
                        etoiles += "*"
                    if not self._pipe_out.poll():
                        # appel la methode affichePhoto de IhmVisionneuse
                        self.value_changed.emit(nom,etoiles)
            elif '##reinitialise##' in nom:
                #self._ihm.label.clear()
                self._charge.clear()
##            except:
##                print 'erreur', nom
##                while self._pipe_out.poll():
##                    print self._pipe_out.recv()
##                print 'sortie'
        #print 'stop affiche'
        #self._ihm.quitter()
