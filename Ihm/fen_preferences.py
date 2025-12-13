# -*- coding: utf-8 -*-

# Form implementation generated from reading ui file '../Ihm\fen_preferences.ui'
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

class Ui_Preferences(object):
    def setupUi(self, Preferences):
        Preferences.setObjectName(_fromUtf8("Preferences"))
        Preferences.resize(322, 193)
        self.verticalLayout_3 = QtWidgets.QVBoxLayout(Preferences)
        self.verticalLayout_3.setObjectName(_fromUtf8("verticalLayout_3"))
        self.horizontalLayout_11 = QtWidgets.QHBoxLayout()
        self.horizontalLayout_11.setObjectName(_fromUtf8("horizontalLayout_11"))
        self.groupBox = QtWidgets.QGroupBox(Preferences)
        self.groupBox.setObjectName(_fromUtf8("groupBox"))
        self.layoutWidget = QtWidgets.QWidget(self.groupBox)
        self.layoutWidget.setGeometry(QtCore.QRect(10, 30, 117, 44))
        self.layoutWidget.setObjectName(_fromUtf8("layoutWidget"))
        self.verticalLayout = QtWidgets.QVBoxLayout(self.layoutWidget)
        self.verticalLayout.setObjectName(_fromUtf8("verticalLayout"))
        self.cb_thumbs = QtWidgets.QCheckBox(self.layoutWidget)
        self.cb_thumbs.setChecked(True)
        self.cb_thumbs.setObjectName(_fromUtf8("cb_thumbs"))
        self.verticalLayout.addWidget(self.cb_thumbs)
        self.cb_photo = QtWidgets.QCheckBox(self.layoutWidget)
        self.cb_photo.setChecked(True)
        self.cb_photo.setObjectName(_fromUtf8("cb_photo"))
        self.verticalLayout.addWidget(self.cb_photo)
        self.horizontalLayout_11.addWidget(self.groupBox)
        self.verticalLayout_3.addLayout(self.horizontalLayout_11)
        self.buttonBox = QtWidgets.QDialogButtonBox(Preferences)
        self.buttonBox.setOrientation(QtCore.Qt.Horizontal)
        self.buttonBox.setStandardButtons(QtWidgets.QDialogButtonBox.Apply|QtWidgets.QDialogButtonBox.Cancel|QtWidgets.QDialogButtonBox.Ok)
        self.buttonBox.setObjectName(_fromUtf8("buttonBox"))
        self.verticalLayout_3.addWidget(self.buttonBox)

        self.retranslateUi(Preferences)
        QtCore.QObject.connect(self.buttonBox, QtCore.SIGNAL(_fromUtf8("accepted()")), Preferences.accept)
        QtCore.QObject.connect(self.buttonBox, QtCore.SIGNAL(_fromUtf8("rejected()")), Preferences.reject)
        QtCore.QObject.connect(self.buttonBox, QtCore.SIGNAL(_fromUtf8("clicked(QAbstractButton*)")), Preferences.update)
        QtCore.QMetaObject.connectSlotsByName(Preferences)

    def retranslateUi(self, Preferences):
        Preferences.setWindowTitle(_translate("Preferences", "Préférences", None))
        self.groupBox.setTitle(_translate("Preferences", "Plein écran", None))
        self.cb_thumbs.setText(_translate("Preferences", "Fenêtre miniatures", None))
        self.cb_photo.setText(_translate("Preferences", "fenêtre photo", None))


if __name__ == "__main__":
    import sys
    app = QtWidgets.QApplication(sys.argv)
    Preferences = QtWidgets.QDialog()
    ui = Ui_Preferences()
    ui.setupUi(Preferences)
    Preferences.show()
    sys.exit(app.exec_())

