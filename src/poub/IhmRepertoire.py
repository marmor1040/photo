# -*- coding: latin-1
"""
Created on 5 juin 2011

@author: Bureau
"""
from PyQt5 import QtWidgets,QtCore
from PyQt5.QtCore import Qt,QObject
from PyQt5.QtWidgets import QDialogButtonBox
from src import preferences
from IhmFiltre import Filtre
#from PyQt5.uic import loadUiType
#FormClass, BaseClass = loadUiType(osp.join(osp.dirname(osp.realpath(__file__)),
#                                           '../Ihm/choix_repertoire.ui'))
from choix_repertoire import Ui_ChoixRepertoire as FormClass 
from PyQt5.QtWidgets import QDialog as BaseClass

class FenetreRepertoire(BaseClass,FormClass):
    __fenetre_thumbs = None
    def __init__(self,parent):
        BaseClass.__init__(self)
        self.setupUi(self)
        FenetreRepertoire.__fenetre_thumbs = parent
        QObject.connect(self.bt_repertoire,QtCore.SIGNAL("clicked()"),self.choixRepertoire)
        self.__defaut = preferences.getRepertoireDefaut()
        if self.__defaut:
            self.repertoire.setText(self.__defaut)
            self.okcancel.button(QDialogButtonBox.Ok).setEnabled(True)
        else:
            self.okcancel.button(QDialogButtonBox.Ok).setEnabled(False)
        if preferences.isModeTri():
            self.cb_arbo.setHidden(True)
        #self.setWindowFlags(Qt.FramelessWindowHint |Qt.WindowStaysOnTopHint)
                    
    def choixRepertoire(self):
        rep = QtWidgets.QFileDialog.getExistingDirectory(self,"R�pertoire des images",
                                                          self.__defaut,    
                                                          QtWidgets.QFileDialog.ShowDirsOnly)
        if rep:
            self.repertoire.setText(rep)
            self.okcancel.button(QDialogButtonBox.Ok).setEnabled(True)
        
    def getRepertoires(self):
        ret = str(self.repertoire.text())
        if ret[-1] != '/':
            ret += '/'
        if self.__defaut != ret:
            preferences.setRepertoireDefaut(ret)
            preferences.setFiltreDefaut(Filtre([True,False,False,False]))
        self.repertoire.setText('')
        self.okcancel.button(QDialogButtonBox.Ok).setEnabled(False)
        arbo = self.cb_arbo.isChecked()
        preferences.setArborescence(arbo)
        return ret,arbo
        
def choisirRepertoire():
    #Choix = QtWidgets.QDialog()
    Choix = FenetreRepertoire(None)
    Choix.show()
    ret = Choix.exec_()
    if ret:
        return Choix.getRepertoires()
    return ''

if __name__ == '__main__':
    from PyQt5.QtWidgets import QApplication
    app = QApplication([])
    app.setStyle("plastique")
    rep = choisirRepertoire()
    print(rep)
        
        