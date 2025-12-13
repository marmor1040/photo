# -*- coding: utf-8 -*-

# Form implementation generated from reading ui file '../Ihm\widget_miniature_hor.ui'
#
# Created by: PyQt5 UI code generator 4.11.4
#
# WARNING! All changes made in this file will be lost!

from PyQt5 import QtCore, QtWidgets

try:
    _fromUtf8 = QtCore.QString.fromUtf8
except AttributeError:
    def _fromUtf8(s):
        return s

try:
    _encoding = QtWidgets.QApplication.UnicodeUTF8
    def _translate(context, text, disambig):
        return QtWidgets.QApplication.translate(context, text, disambig, _encoding)
except AttributeError:
    def _translate(context, text, disambig):
        return QtWidgets.QApplication.translate(context, text, disambig)

class Ui_MiniatureHor(object):
    def setupUi(self, MiniatureHor):
        MiniatureHor.setObjectName(_fromUtf8("MiniatureHor"))
        MiniatureHor.resize(285, 212)
        self.horizontalLayout_2 = QtWidgets.QHBoxLayout(MiniatureHor)
        self.horizontalLayout_2.setMargin(1)
        self.horizontalLayout_2.setObjectName(_fromUtf8("horizontalLayout_2"))
        self.frame = QtWidgets.QFrame(MiniatureHor)
        self.frame.setEnabled(True)
        self.frame.setFrameShape(QtWidgets.QFrame.Panel)
        self.frame.setObjectName(_fromUtf8("frame"))
        self.verticalLayout_4 = QtWidgets.QVBoxLayout(self.frame)
        self.verticalLayout_4.setMargin(0)
        self.verticalLayout_4.setSpacing(6)
        self.verticalLayout_4.setObjectName(_fromUtf8("verticalLayout_4"))
        self.label = QtWidgets.QLabel(self.frame)
        self.label.setText(_fromUtf8(""))
        self.label.setObjectName(_fromUtf8("label"))
        self.verticalLayout_4.addWidget(self.label)
        self.horizontalLayout = QtWidgets.QHBoxLayout()
        self.horizontalLayout.setSpacing(0)
        self.horizontalLayout.setObjectName(_fromUtf8("horizontalLayout"))
        spacerItem = QtWidgets.QSpacerItem(40, 20, QtWidgets.QSizePolicy.Expanding, QtWidgets.QSizePolicy.Minimum)
        self.horizontalLayout.addItem(spacerItem)
        self.cb1 = QtWidgets.QVBoxLayout()
        self.cb1.setObjectName(_fromUtf8("cb1"))
        spacerItem1 = QtWidgets.QSpacerItem(20, 40, QtWidgets.QSizePolicy.Minimum, QtWidgets.QSizePolicy.Expanding)
        self.cb1.addItem(spacerItem1)
        self.nom_pano = QtWidgets.QLabel(self.frame)
        font = QtWidgets.QFont()
        font.setPointSize(12)
        font.setBold(True)
        font.setWeight(75)
        self.nom_pano.setFont(font)
        self.nom_pano.setText(_fromUtf8(""))
        self.nom_pano.setObjectName(_fromUtf8("nom_pano"))
        self.cb1.addWidget(self.nom_pano)
        self.traitee = QtWidgets.QCheckBox(self.frame)
        self.traitee.setObjectName(_fromUtf8("traitee"))
        self.cb1.addWidget(self.traitee)
        self.panorama = QtWidgets.QCheckBox(self.frame)
        self.panorama.setObjectName(_fromUtf8("panorama"))
        self.cb1.addWidget(self.panorama)
        self.retouche = QtWidgets.QCheckBox(self.frame)
        self.retouche.setObjectName(_fromUtf8("retouche"))
        self.cb1.addWidget(self.retouche)
        self.horizontalLayout.addLayout(self.cb1)
        self.cb2 = QtWidgets.QVBoxLayout()
        self.cb2.setSpacing(0)
        self.cb2.setObjectName(_fromUtf8("cb2"))
        spacerItem2 = QtWidgets.QSpacerItem(20, 40, QtWidgets.QSizePolicy.Minimum, QtWidgets.QSizePolicy.Expanding)
        self.cb2.addItem(spacerItem2)
        self.etoile = QtWidgets.QLabel(self.frame)
        self.etoile.setObjectName(_fromUtf8("etoile"))
        self.cb2.addWidget(self.etoile)
        self.autre = QtWidgets.QCheckBox(self.frame)
        self.autre.setObjectName(_fromUtf8("autre"))
        self.cb2.addWidget(self.autre)
        self.horizontalLayout.addLayout(self.cb2)
        self.verticalLayout_4.addLayout(self.horizontalLayout)
        self.horizontalLayout_2.addWidget(self.frame)

        self.retranslateUi(MiniatureHor)
        QtCore.QMetaObject.connectSlotsByName(MiniatureHor)

    def retranslateUi(self, MiniatureHor):
        MiniatureHor.setWindowTitle(_translate("MiniatureHor", "Form", None))
        self.traitee.setText(_translate("MiniatureHor", "traitée", None))
        self.panorama.setText(_translate("MiniatureHor", "panorama", None))
        self.retouche.setText(_translate("MiniatureHor", "retouche", None))
        self.etoile.setText(_translate("MiniatureHor", "etoile", None))
        self.autre.setText(_translate("MiniatureHor", "autre", None))


if __name__ == "__main__":
    import sys
    app = QtWidgets.QApplication(sys.argv)
    MiniatureHor = QtWidgets.QWidget()
    ui = Ui_MiniatureHor()
    ui.setupUi(MiniatureHor)
    MiniatureHor.show()
    sys.exit(app.exec_())

