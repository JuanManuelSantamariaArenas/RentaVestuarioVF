# -*- coding: utf-8 -*-

# Form implementation generated from reading ui file 'dialogoDevolverPrenda.ui'
#
# Created by: PyQt5 UI code generator 5.15.7
#
# WARNING: Any manual changes made to this file will be lost when pyuic5 is
# run again.  Do not edit this file unless you know what you are doing.


from PyQt5 import QtCore, QtGui, QtWidgets


class Ui_DevolverPrenda(object):
    def setupUi(self, DevolverPrenda):
        DevolverPrenda.setObjectName("DevolverPrenda")
        DevolverPrenda.resize(400, 152)
        self.buttonBox = QtWidgets.QDialogButtonBox(DevolverPrenda)
        self.buttonBox.setGeometry(QtCore.QRect(230, 100, 161, 32))
        self.buttonBox.setOrientation(QtCore.Qt.Horizontal)
        self.buttonBox.setStandardButtons(QtWidgets.QDialogButtonBox.Cancel|QtWidgets.QDialogButtonBox.Ok)
        self.buttonBox.setObjectName("buttonBox")
        self.formLayoutWidget = QtWidgets.QWidget(DevolverPrenda)
        self.formLayoutWidget.setGeometry(QtCore.QRect(10, 30, 381, 61))
        self.formLayoutWidget.setObjectName("formLayoutWidget")
        self.formLayout = QtWidgets.QFormLayout(self.formLayoutWidget)
        self.formLayout.setContentsMargins(0, 0, 0, 0)
        self.formLayout.setObjectName("formLayout")
        self.label = QtWidgets.QLabel(self.formLayoutWidget)
        self.label.setTextFormat(QtCore.Qt.AutoText)
        self.label.setObjectName("label")
        self.formLayout.setWidget(0, QtWidgets.QFormLayout.LabelRole, self.label)
        self.le_cedula = QtWidgets.QLineEdit(self.formLayoutWidget)
        self.le_cedula.setObjectName("le_cedula")
        self.formLayout.setWidget(0, QtWidgets.QFormLayout.FieldRole, self.le_cedula)
        self.label_2 = QtWidgets.QLabel(self.formLayoutWidget)
        self.label_2.setObjectName("label_2")
        self.formLayout.setWidget(1, QtWidgets.QFormLayout.LabelRole, self.label_2)
        self.le_codigo = QtWidgets.QLineEdit(self.formLayoutWidget)
        self.le_codigo.setObjectName("le_codigo")
        self.formLayout.setWidget(1, QtWidgets.QFormLayout.FieldRole, self.le_codigo)

        self.retranslateUi(DevolverPrenda)
        self.buttonBox.accepted.connect(DevolverPrenda.accept) # type: ignore
        self.buttonBox.rejected.connect(DevolverPrenda.reject) # type: ignore
        QtCore.QMetaObject.connectSlotsByName(DevolverPrenda)

    def retranslateUi(self, DevolverPrenda):
        _translate = QtCore.QCoreApplication.translate
        DevolverPrenda.setWindowTitle(_translate("DevolverPrenda", "Dialog"))
        self.label.setText(_translate("DevolverPrenda", "C??dula:"))
        self.label_2.setText(_translate("DevolverPrenda", "C??digo:"))
