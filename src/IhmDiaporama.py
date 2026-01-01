# -*- coding: utf-8
"""
Created on 5 juin 2011

@author: Bureau
"""
from PyQt5 import QtCore
from PyQt5.QtCore import QObject

from PyQt5.QtCore import Qt
#from PyQt5.uic import loadUiType
#FormClass, BaseClass = loadUiType(osp.join(osp.dirname(osp.realpath(__file__)),
#                                           '../Ihm/fen_diaporama.ui'))
from Ihm.fen_diaporama import Ui_Diaporama as FormClass
from PyQt5.QtWidgets import QDialog as BaseClass
from PyQt5.QtWidgets import QMessageBox as Message

class FenetreDiaporama(BaseClass, FormClass):
    def __init__(self,parent):
        BaseClass.__init__(self, parent)
        self.setupUi(self)
        self._fenetre = parent
        self._en_cours = False
        self._timer = None
        QObject.connect(self.bt_go_stop,QtCore.SIGNAL("clicked()"),self.go_stop)
        QObject.connect(self.sb_tempo,QtCore.SIGNAL("valueChanged(int)"),self.change_tempo)
        QObject.connect(self.bt_quitter,QtCore.SIGNAL("clicked()"),self.quitter)
        # on retire la bordure et devant 
        self.setWindowFlags(Qt.FramelessWindowHint)
        self.move(100,0)
            
    def timerEvent(self,timer):
        self._fenetre.avanceDiaporama()
        
    def go_stop(self):
        if self._en_cours:
            self.killTimer(self._timer)
            self._timer = None
            self.bt_go_stop.setText('Lancer')
            self._en_cours = False
        else:
            self._timer = self.startTimer(self.sb_tempo.value()*1000)
            self.bt_go_stop.setText('Stop')
            self._en_cours = True
            
    def change_tempo(self,v):
        if self._timer:
            self.killTimer(self._timer)
            self._timer = self.startTimer(self.sb_tempo.value()*1000)
        
    def done(self,v):
        if self._timer:
            self.killTimer(self._timer)
        self.hide()

    def quitter(self):
        ret = False
        if not self._fenetre.mode_tri:
            ret = Message.question(self.window(),'Destruction miniatures','D�truire les miniatures',Message.Ok|Message.Cancel,Message.Cancel)
        self._fenetre.quitter(ret == Message.Ok)

        