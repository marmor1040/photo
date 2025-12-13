# -*- coding: utf-8 -*-

# Form implementation generated from reading ui file '../Ihm\widget_miniature_vert.ui'
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

class Ui_MiniatureVer(object):
    def setupUi(self, MiniatureVer):
        MiniatureVer.setObjectName(_fromUtf8("MiniatureVer"))
        MiniatureVer.resize(269, 190)
        self.horizontalLayout_2 = QtWidgets.QHBoxLayout(MiniatureVer)
        self.horizontalLayout_2.setMargin(1)
        self.horizontalLayout_2.setObjectName(_fromUtf8("horizontalLayout_2"))
        self.frame = QtWidgets.QFrame(MiniatureVer)
        self.frame.setEnabled(True)
        self.frame.setFrameShape(QtWidgets.QFrame.Panel)
        self.frame.setObjectName(_fromUtf8("frame"))
        self.horizontalLayout = QtWidgets.QHBoxLayout(self.frame)
        self.horizontalLayout.setContentsMargins(0, 0, 0, 0)
        self.horizontalLayout.setSpacing(0)
        self.horizontalLayout.setObjectName(_fromUtf8("horizontalLayout"))
        self.label = QtWidgets.QLabel(self.frame)
        self.label.setText(_fromUtf8(""))
        self.label.setObjectName(_fromUtf8("label"))
        self.horizontalLayout.addWidget(self.label)
        self.verticalLayout_1 = QtWidgets.QVBoxLayout()
        self.verticalLayout_1.setObjectName(_fromUtf8("verticalLayout_1"))
        spacerItem = QtWidgets.QSpacerItem(20, 40, QtWidgets.QSizePolicy.Minimum, QtWidgets.QSizePolicy.Expanding)
        self.verticalLayout_1.addItem(spacerItem)
        self.verticalLayout = QtWidgets.QVBoxLayout()
        self.verticalLayout.setObjectName(_fromUtf8("verticalLayout"))
        self.nom_pano = QtWidgets.QLabel(self.frame)
        font = QtWidgets.QFont()
        font.setPointSize(12)
        font.setBold(True)
        font.setWeight(75)
        self.nom_pano.setFont(font)
        self.nom_pano.setText(_fromUtf8(""))
        self.nom_pano.setObjectName(_fromUtf8("nom_pano"))
        self.verticalLayout.addWidget(self.nom_pano)
        self.etoile = QtWidgets.QLabel(self.frame)
        self.etoile.setObjectName(_fromUtf8("etoile"))
        self.verticalLayout.addWidget(self.etoile)
        self.traitee = QtWidgets.QCheckBox(self.frame)
        self.traitee.setObjectName(_fromUtf8("traitee"))
        self.verticalLayout.addWidget(self.traitee)
        self.panorama = QtWidgets.QCheckBox(self.frame)
        self.panorama.setObjectName(_fromUtf8("panorama"))
        self.verticalLayout.addWidget(self.panorama)
        self.retouche = QtWidgets.QCheckBox(self.frame)
        self.retouche.setObjectName(_fromUtf8("retouche"))
        self.verticalLayout.addWidget(self.retouche)
        self.autre = QtWidgets.QCheckBox(self.frame)
        self.autre.setObjectName(_fromUtf8("autre"))
        self.verticalLayout.addWidget(self.autre)
        self.verticalLayout_1.addLayout(self.verticalLayout)
        self.horizontalLayout.addLayout(self.verticalLayout_1)
        self.horizontalLayout_2.addWidget(self.frame)

        self.retranslateUi(MiniatureVer)
        QtCore.QMetaObject.connectSlotsByName(MiniatureVer)

    def retranslateUi(self, MiniatureVer):
        MiniatureVer.setWindowTitle(_translate("MiniatureVer", "Form", None))
        self.etoile.setText(_translate("MiniatureVer", "etoile", None))
        self.traitee.setText(_translate("MiniatureVer", "traitée", None))
        self.panorama.setText(_translate("MiniatureVer", "panorama", None))
        self.retouche.setText(_translate("MiniatureVer", "retouche", None))
        self.autre.setText(_translate("MiniatureVer", "autre", None))


if __name__ == "__main__":
    import sys
    app = QtWidgets.QApplication(sys.argv)
    MiniatureVer = QtWidgets.QWidget()
    ui = Ui_MiniatureVer()
    ui.setupUi(MiniatureVer)
    MiniatureVer.show()
    sys.exit(app.exec_())

