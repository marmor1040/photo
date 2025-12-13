#!/usr/bin/env python

from PyQt5.QtWidgets import QApplication
from IhmMiniatures import FenetreThumbs 
from FenetreVisionneuse import IhmVisionneuse
from multiprocessing import freeze_support, Pipe
from src import preferences

if __name__ == "__main__":
    freeze_support()
    app = QApplication([])
    app.setStyle("plastique")
    preferences.setMode('visionneuse')
    # creation d'un pipe pour communiquer entre la visionneuse et les miniatures
    Pout_visio,Pin_visio = Pipe()
    # creation d'un pipe pour communiquer entre les miniatures et la visionneuse
    Pout_mini,Pin_mini = Pipe()
    # lancement de la fenetre photo
    process = IhmVisionneuse.start(Pout_mini,Pin_visio,preferences.isModeTri())
    # lancement de la fenetre des miniatures
    ihmThumbs = FenetreThumbs(Pin_mini,Pin_visio,Pout_visio)
    app.exec_()
    IhmVisionneuse.stop(process)