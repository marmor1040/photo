# -*- coding: utf-8 -*-

# Form implementation generated from reading ui file '../Ihm\choix_repertoire.ui'
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

class Ui_ChoixRepertoire(object):
    def setupUi(self, ChoixRepertoire):
        ChoixRepertoire.setObjectName(_fromUtf8("ChoixRepertoire"))
        ChoixRepertoire.resize(533, 114)
        self.verticalLayout_2 = QtWidgets.QVBoxLayout(ChoixRepertoire)
        self.verticalLayout_2.setObjectName(_fromUtf8("verticalLayout_2"))
        self.horizontalLayout = QtWidgets.QHBoxLayout()
        self.horizontalLayout.setSizeConstraint(QtWidgets.QLayout.SetFixedSize)
        self.horizontalLayout.setObjectName(_fromUtf8("horizontalLayout"))
        self.label = QtWidgets.QLabel(ChoixRepertoire)
        sizePolicy = QtWidgets.QSizePolicy(QtWidgets.QSizePolicy.Preferred, QtWidgets.QSizePolicy.Fixed)
        sizePolicy.setHorizontalStretch(0)
        sizePolicy.setVerticalStretch(0)
        sizePolicy.setHeightForWidth(self.label.sizePolicy().hasHeightForWidth())
        self.label.setSizePolicy(sizePolicy)
        self.label.setObjectName(_fromUtf8("label"))
        self.horizontalLayout.addWidget(self.label)
        self.repertoire = QtWidgets.QLineEdit(ChoixRepertoire)
        self.repertoire.setObjectName(_fromUtf8("repertoire"))
        self.horizontalLayout.addWidget(self.repertoire)
        self.bt_repertoire = QtWidgets.QPushButton(ChoixRepertoire)
        sizePolicy = QtWidgets.QSizePolicy(QtWidgets.QSizePolicy.Fixed, QtWidgets.QSizePolicy.Fixed)
        sizePolicy.setHorizontalStretch(0)
        sizePolicy.setVerticalStretch(0)
        sizePolicy.setHeightForWidth(self.bt_repertoire.sizePolicy().hasHeightForWidth())
        self.bt_repertoire.setSizePolicy(sizePolicy)
        self.bt_repertoire.setMinimumSize(QtCore.QSize(40, 0))
        self.bt_repertoire.setMaximumSize(QtCore.QSize(40, 16777215))
        self.bt_repertoire.setObjectName(_fromUtf8("bt_repertoire"))
        self.horizontalLayout.addWidget(self.bt_repertoire)
        self.verticalLayout_2.addLayout(self.horizontalLayout)
        self.cb_arbo = QtWidgets.QCheckBox(ChoixRepertoire)
        self.cb_arbo.setObjectName(_fromUtf8("cb_arbo"))
        self.verticalLayout_2.addWidget(self.cb_arbo)
        self.horizontalLayout_3 = QtWidgets.QHBoxLayout()
        self.horizontalLayout_3.setSizeConstraint(QtWidgets.QLayout.SetFixedSize)
        self.horizontalLayout_3.setObjectName(_fromUtf8("horizontalLayout_3"))
        self.verticalLayout_2.addLayout(self.horizontalLayout_3)
        spacerItem = QtWidgets.QSpacerItem(20, 40, QtWidgets.QSizePolicy.Minimum, QtWidgets.QSizePolicy.Expanding)
        self.verticalLayout_2.addItem(spacerItem)
        self.okcancel = QtWidgets.QDialogButtonBox(ChoixRepertoire)
        self.okcancel.setOrientation(QtCore.Qt.Horizontal)
        self.okcancel.setStandardButtons(QtWidgets.QDialogButtonBox.Cancel|QtWidgets.QDialogButtonBox.Ok)
        self.okcancel.setObjectName(_fromUtf8("okcancel"))
        self.verticalLayout_2.addWidget(self.okcancel)

        self.retranslateUi(ChoixRepertoire)
        QtCore.QObject.connect(self.okcancel, QtCore.SIGNAL(_fromUtf8("accepted()")), ChoixRepertoire.accept)
        QtCore.QObject.connect(self.okcancel, QtCore.SIGNAL(_fromUtf8("rejected()")), ChoixRepertoire.reject)
        QtCore.QMetaObject.connectSlotsByName(ChoixRepertoire)

    def retranslateUi(self, ChoixRepertoire):
        ChoixRepertoire.setWindowTitle(_translate("ChoixRepertoire", "Choix du repertoire des photos", None))
        self.label.setText(_translate("ChoixRepertoire", "Répertoire", None))
        self.bt_repertoire.setText(_translate("ChoixRepertoire", "...", None))
        self.cb_arbo.setText(_translate("ChoixRepertoire", "arborescence", None))


if __name__ == "__main__":
    import sys
    app = QtWidgets.QApplication(sys.argv)
    ChoixRepertoire = QtWidgets.QDialog()
    ui = Ui_ChoixRepertoire()
    ui.setupUi(ChoixRepertoire)
    ChoixRepertoire.show()
    sys.exit(app.exec_())

