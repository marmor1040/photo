## -*- coding: latin-1 -*-
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
from PyQt5.QtCore import Qt,QPoint,QSize,QRect,pyqtSlot
from PyQt5.QtCore import QObject
from src import preferences as PREFERENCES
from src.IhmDiaporama import FenetreDiaporama

from Ihm.fen_visionneuse import Ui_Visionneuse as FormClass
from PyQt5.QtWidgets import QWidget as BaseClass
from PyQt5 import QtWidgets
from .ThreadChargement import ThreadPhoto

class Affiche(ThreadPhoto,QObject):
    def __init__(self,charge,Pout):
        ThreadPhoto.__init__(self)
        QObject.__init__(self,None)
        self.__charge = charge
        self.__pipe_out = Pout
        self.__tab={}

    def affiche(self,v):
        print("nom =",v)
        
    def run(self):
        cont = True
        nom = None
        while cont:
           # try:
            #print 'recv',self.__pipe_out
            nom = self.__pipe_out.recv()
            if nom == '##quitter##':
                self.__charge.stop()
                cont = False
                #if self.__ihm.isVisible():
            elif '##repertoire##' in nom:
                rep = nom.replace('##repertoire##','')
                # pour arreter le chargement auto des photos
                self.__charge.courant = None
                # changement du repertoire
                self.__charge.initialise(rep)
            elif '##photos##' in nom:
                liste = eval(nom.replace('##photos##',''))
                # création de la liste des photos
                #print 'photos :',liste
                if liste:
                    self.__charge.initialiseListeFichiers(liste)
            elif '##geometrie##' in nom:
                taille= eval(nom.replace('##geometrie##',''))
                self.__ihm.setGeometry(taille)
            elif '##affiche##' in nom:
                if ThreadPhoto.rep_photos:
                    nom,etoiles,traite = nom.replace('##affiche##','').split(';')
                    if traite == "False":
                        etoiles = ""
                    else:
                        etoiles += "*"
                    if not self.__pipe_out.poll():
                        # appel la methode affichePhoto de IhmVisionneuse
                        self.emit(QtCore.SIGNAL("changed(str,str)"),nom,etoiles)
            elif '##reinitialise##' in nom:
                #self.__ihm.label.clear()
                self.__charge.clear()
##            except:
##                print 'erreur', nom
##                while self.__pipe_out.poll():
##                    print self.__pipe_out.recv()
##                print 'sortie'
        #print 'stop affiche'
        #self.__ihm.quitter()
