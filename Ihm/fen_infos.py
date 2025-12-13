# -*- coding: utf-8 -*-

# Form implementation generated from reading ui file '../Ihm\fen_infos.ui'
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

class Ui_Infos(object):
    def setupUi(self, Infos):
        Infos.setObjectName(_fromUtf8("Infos"))
        Infos.resize(289, 348)
        self.horizontalLayout_3 = QtWidgets.QHBoxLayout(Infos)
        self.horizontalLayout_3.setObjectName(_fromUtf8("horizontalLayout_3"))
        self.verticalLayout = QtWidgets.QVBoxLayout()
        self.verticalLayout.setObjectName(_fromUtf8("verticalLayout"))
        self.horizontalLayout_2 = QtWidgets.QHBoxLayout()
        self.horizontalLayout_2.setObjectName(_fromUtf8("horizontalLayout_2"))
        self.verticalLayout_4 = QtWidgets.QVBoxLayout()
        self.verticalLayout_4.setObjectName(_fromUtf8("verticalLayout_4"))
        self.etoiles = QtWidgets.QGroupBox(Infos)
        self.etoiles.setCheckable(True)
        self.etoiles.setObjectName(_fromUtf8("etoiles"))
        self.horizontalLayout = QtWidgets.QHBoxLayout(self.etoiles)
        self.horizontalLayout.setObjectName(_fromUtf8("horizontalLayout"))
        self.cb_0_etoile = QtWidgets.QRadioButton(self.etoiles)
        self.cb_0_etoile.setObjectName(_fromUtf8("cb_0_etoile"))
        self.horizontalLayout.addWidget(self.cb_0_etoile)
        self.cb_1_etoile = QtWidgets.QRadioButton(self.etoiles)
        self.cb_1_etoile.setObjectName(_fromUtf8("cb_1_etoile"))
        self.horizontalLayout.addWidget(self.cb_1_etoile)
        self.cb_2_etoiles = QtWidgets.QRadioButton(self.etoiles)
        self.cb_2_etoiles.setObjectName(_fromUtf8("cb_2_etoiles"))
        self.horizontalLayout.addWidget(self.cb_2_etoiles)
        self.cb_3_etoiles = QtWidgets.QRadioButton(self.etoiles)
        self.cb_3_etoiles.setObjectName(_fromUtf8("cb_3_etoiles"))
        self.horizontalLayout.addWidget(self.cb_3_etoiles)
        self.verticalLayout_4.addWidget(self.etoiles)
        self.traitee = QtWidgets.QGroupBox(Infos)
        sizePolicy = QtWidgets.QSizePolicy(QtWidgets.QSizePolicy.Preferred, QtWidgets.QSizePolicy.Preferred)
        sizePolicy.setHorizontalStretch(0)
        sizePolicy.setVerticalStretch(0)
        sizePolicy.setHeightForWidth(self.traitee.sizePolicy().hasHeightForWidth())
        self.traitee.setSizePolicy(sizePolicy)
        self.traitee.setMinimumSize(QtCore.QSize(0, 55))
        self.traitee.setCheckable(True)
        self.traitee.setObjectName(_fromUtf8("traitee"))
        self.verticalLayout_2 = QtWidgets.QVBoxLayout(self.traitee)
        self.verticalLayout_2.setObjectName(_fromUtf8("verticalLayout_2"))
        self.cb_traitee = QtWidgets.QCheckBox(self.traitee)
        self.cb_traitee.setObjectName(_fromUtf8("cb_traitee"))
        self.verticalLayout_2.addWidget(self.cb_traitee)
        self.verticalLayout_4.addWidget(self.traitee)
        self.panorama = QtWidgets.QGroupBox(Infos)
        sizePolicy = QtWidgets.QSizePolicy(QtWidgets.QSizePolicy.Preferred, QtWidgets.QSizePolicy.Preferred)
        sizePolicy.setHorizontalStretch(0)
        sizePolicy.setVerticalStretch(0)
        sizePolicy.setHeightForWidth(self.panorama.sizePolicy().hasHeightForWidth())
        self.panorama.setSizePolicy(sizePolicy)
        self.panorama.setMinimumSize(QtCore.QSize(0, 55))
        self.panorama.setCheckable(True)
        self.panorama.setObjectName(_fromUtf8("panorama"))
        self.verticalLayout_6 = QtWidgets.QVBoxLayout(self.panorama)
        self.verticalLayout_6.setObjectName(_fromUtf8("verticalLayout_6"))
        self.cb_panorama = QtWidgets.QCheckBox(self.panorama)
        self.cb_panorama.setObjectName(_fromUtf8("cb_panorama"))
        self.verticalLayout_6.addWidget(self.cb_panorama)
        self.verticalLayout_4.addWidget(self.panorama)
        self.retouche = QtWidgets.QGroupBox(Infos)
        sizePolicy = QtWidgets.QSizePolicy(QtWidgets.QSizePolicy.Preferred, QtWidgets.QSizePolicy.Preferred)
        sizePolicy.setHorizontalStretch(0)
        sizePolicy.setVerticalStretch(0)
        sizePolicy.setHeightForWidth(self.retouche.sizePolicy().hasHeightForWidth())
        self.retouche.setSizePolicy(sizePolicy)
        self.retouche.setMinimumSize(QtCore.QSize(0, 55))
        self.retouche.setCheckable(True)
        self.retouche.setObjectName(_fromUtf8("retouche"))
        self.verticalLayout_7 = QtWidgets.QVBoxLayout(self.retouche)
        self.verticalLayout_7.setObjectName(_fromUtf8("verticalLayout_7"))
        self.cb_retouche = QtWidgets.QCheckBox(self.retouche)
        self.cb_retouche.setObjectName(_fromUtf8("cb_retouche"))
        self.verticalLayout_7.addWidget(self.cb_retouche)
        self.verticalLayout_4.addWidget(self.retouche)
        self.autre = QtWidgets.QGroupBox(Infos)
        self.autre.setCheckable(True)
        self.autre.setObjectName(_fromUtf8("autre"))
        self.verticalLayout_5 = QtWidgets.QVBoxLayout(self.autre)
        self.verticalLayout_5.setObjectName(_fromUtf8("verticalLayout_5"))
        self.cb_autre = QtWidgets.QCheckBox(self.autre)
        self.cb_autre.setObjectName(_fromUtf8("cb_autre"))
        self.verticalLayout_5.addWidget(self.cb_autre)
        self.verticalLayout_4.addWidget(self.autre)
        self.horizontalLayout_2.addLayout(self.verticalLayout_4)
        self.groupBox_2 = QtWidgets.QGroupBox(Infos)
        self.groupBox_2.setObjectName(_fromUtf8("groupBox_2"))
        self.verticalLayout_3 = QtWidgets.QVBoxLayout(self.groupBox_2)
        self.verticalLayout_3.setObjectName(_fromUtf8("verticalLayout_3"))
        self.bt_toutes = QtWidgets.QPushButton(self.groupBox_2)
        self.bt_toutes.setObjectName(_fromUtf8("bt_toutes"))
        self.verticalLayout_3.addWidget(self.bt_toutes)
        self.bt_selection = QtWidgets.QPushButton(self.groupBox_2)
        self.bt_selection.setObjectName(_fromUtf8("bt_selection"))
        self.verticalLayout_3.addWidget(self.bt_selection)
        self.horizontalLayout_2.addWidget(self.groupBox_2)
        self.verticalLayout.addLayout(self.horizontalLayout_2)
        self.buttonBox = QtWidgets.QDialogButtonBox(Infos)
        self.buttonBox.setOrientation(QtCore.Qt.Horizontal)
        self.buttonBox.setStandardButtons(QtWidgets.QDialogButtonBox.Close)
        self.buttonBox.setObjectName(_fromUtf8("buttonBox"))
        self.verticalLayout.addWidget(self.buttonBox)
        self.horizontalLayout_3.addLayout(self.verticalLayout)

        self.retranslateUi(Infos)
        QtCore.QObject.connect(self.buttonBox, QtCore.SIGNAL(_fromUtf8("accepted()")), Infos.accept)
        QtCore.QObject.connect(self.buttonBox, QtCore.SIGNAL(_fromUtf8("rejected()")), Infos.reject)
        QtCore.QMetaObject.connectSlotsByName(Infos)

    def retranslateUi(self, Infos):
        Infos.setWindowTitle(_translate("Infos", "Modification Infos", None))
        self.etoiles.setTitle(_translate("Infos", "Etoiles", None))
        self.cb_0_etoile.setText(_translate("Infos", "0", None))
        self.cb_1_etoile.setText(_translate("Infos", "1", None))
        self.cb_2_etoiles.setText(_translate("Infos", "2", None))
        self.cb_3_etoiles.setText(_translate("Infos", "3", None))
        self.traitee.setTitle(_translate("Infos", "Traitée", None))
        self.cb_traitee.setText(_translate("Infos", "Traitée", None))
        self.panorama.setTitle(_translate("Infos", "Panorama", None))
        self.cb_panorama.setText(_translate("Infos", "Panorama", None))
        self.retouche.setTitle(_translate("Infos", "Retouche", None))
        self.cb_retouche.setText(_translate("Infos", "Retouche", None))
        self.autre.setTitle(_translate("Infos", "autre", None))
        self.cb_autre.setText(_translate("Infos", "Autre", None))
        self.groupBox_2.setTitle(_translate("Infos", "Appliquer", None))
        self.bt_toutes.setText(_translate("Infos", "Toutes", None))
        self.bt_selection.setText(_translate("Infos", "Selection", None))


if __name__ == "__main__":
    import sys
    app = QtWidgets.QApplication(sys.argv)
    Infos = QtWidgets.QDialog()
    ui = Ui_Infos()
    ui.setupUi(Infos)
    Infos.show()
    sys.exit(app.exec_())

