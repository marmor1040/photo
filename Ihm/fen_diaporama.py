# -*- coding: utf-8 -*-

# Form implementation generated from reading ui file '../Ihm\fen_diaporama.ui'
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

class Ui_Diaporama(object):
    def setupUi(self, Diaporama):
        Diaporama.setObjectName(_fromUtf8("Diaporama"))
        Diaporama.resize(428, 72)
        self.verticalLayout = QtWidgets.QVBoxLayout(Diaporama)
        self.verticalLayout.setObjectName(_fromUtf8("verticalLayout"))
        self.horizontalLayout = QtWidgets.QHBoxLayout()
        self.horizontalLayout.setObjectName(_fromUtf8("horizontalLayout"))
        self.bt_quitter = QtWidgets.QPushButton(Diaporama)
        font = QtWidgets.QFont()
        font.setPointSize(10)
        font.setBold(True)
        font.setWeight(75)
        self.bt_quitter.setFont(font)
        self.bt_quitter.setObjectName(_fromUtf8("bt_quitter"))
        self.horizontalLayout.addWidget(self.bt_quitter)
        self.label_2 = QtWidgets.QLabel(Diaporama)
        self.label_2.setObjectName(_fromUtf8("label_2"))
        self.horizontalLayout.addWidget(self.label_2)
        self.sb_tempo = QtWidgets.QSpinBox(Diaporama)
        sizePolicy = QtWidgets.QSizePolicy(QtWidgets.QSizePolicy.Minimum, QtWidgets.QSizePolicy.Fixed)
        sizePolicy.setHorizontalStretch(0)
        sizePolicy.setVerticalStretch(0)
        sizePolicy.setHeightForWidth(self.sb_tempo.sizePolicy().hasHeightForWidth())
        self.sb_tempo.setSizePolicy(sizePolicy)
        self.sb_tempo.setMinimumSize(QtCore.QSize(60, 0))
        self.sb_tempo.setObjectName(_fromUtf8("sb_tempo"))
        self.horizontalLayout.addWidget(self.sb_tempo)
        self.bt_go_stop = QtWidgets.QPushButton(Diaporama)
        font = QtWidgets.QFont()
        font.setPointSize(10)
        font.setBold(True)
        font.setWeight(75)
        self.bt_go_stop.setFont(font)
        self.bt_go_stop.setObjectName(_fromUtf8("bt_go_stop"))
        self.horizontalLayout.addWidget(self.bt_go_stop)
        self.verticalLayout.addLayout(self.horizontalLayout)

        self.retranslateUi(Diaporama)
        QtCore.QMetaObject.connectSlotsByName(Diaporama)

    def retranslateUi(self, Diaporama):
        Diaporama.setWindowTitle(_translate("Diaporama", "Diaporama", None))
        self.bt_quitter.setText(_translate("Diaporama", "Quitter", None))
        self.label_2.setText(_translate("Diaporama", "Temporisation (sec)", None))
        self.bt_go_stop.setText(_translate("Diaporama", "Lancer", None))


if __name__ == "__main__":
    import sys
    app = QtWidgets.QApplication(sys.argv)
    Diaporama = QtWidgets.QDialog()
    ui = Ui_Diaporama()
    ui.setupUi(Diaporama)
    Diaporama.show()
    sys.exit(app.exec_())

