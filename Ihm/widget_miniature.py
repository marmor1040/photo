# -*- coding: utf-8 -*-

# Form implementation generated from reading ui file '../Ihm\widget_miniature.ui'
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

class Ui_Miniature(object):
    def setupUi(self, Miniature):
        Miniature.setObjectName(_fromUtf8("Miniature"))
        Miniature.resize(337, 300)
        self.horizontalLayout = QtWidgets.QHBoxLayout(Miniature)
        self.horizontalLayout.setContentsMargins(0, 0, 0, 0)
        self.horizontalLayout.setObjectName(_fromUtf8("horizontalLayout"))
        self.frame = QtWidgets.QFrame(Miniature)
        self.frame.setFrameShape(QtWidgets.QFrame.Panel)
        self.frame.setFrameShadow(QtWidgets.QFrame.Plain)
        self.frame.setObjectName(_fromUtf8("frame"))
        self.verticalLayout = QtWidgets.QVBoxLayout(self.frame)
        self.verticalLayout.setObjectName(_fromUtf8("verticalLayout"))
        self.label = QtWidgets.QLabel(self.frame)
        self.label.setObjectName(_fromUtf8("label"))
        self.verticalLayout.addWidget(self.label)
        self.horizontalLayout.addWidget(self.frame)

        self.retranslateUi(Miniature)
        QtCore.QMetaObject.connectSlotsByName(Miniature)

    def retranslateUi(self, Miniature):
        Miniature.setWindowTitle(_translate("Miniature", "Form", None))
        self.label.setText(_translate("Miniature", "TextLabel", None))


if __name__ == "__main__":
    import sys
    app = QtWidgets.QApplication(sys.argv)
    Miniature = QtWidgets.QWidget()
    ui = Ui_Miniature()
    ui.setupUi(Miniature)
    Miniature.show()
    sys.exit(app.exec_())

