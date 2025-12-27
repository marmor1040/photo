#!/usr/bin/env python

from PyQt5.QtWidgets import QApplication
from src.IhmMiniatures import FenetreThumbs 

if __name__ == "__main__":
    app = QApplication([])
    app.setStyle("plastique")
    # lancement de la fenetre des miniatures
    ihmThumbs = FenetreThumbs()
    app.exec_()
