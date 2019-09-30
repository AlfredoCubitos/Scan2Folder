# -*- coding: utf-8 -*-

# Form implementation generated from reading ui file 'configform.ui'
#
# Created by: PyQt5 UI code generator 5.13.1
#
# WARNING! All changes made in this file will be lost!


from PyQt5 import QtCore, QtGui, QtWidgets


class Ui_Form(object):
    def setupUi(self, Form):
        Form.setObjectName("Form")
        Form.resize(868, 596)
        self.groupBox_2 = QtWidgets.QGroupBox(Form)
        self.groupBox_2.setGeometry(QtCore.QRect(20, 10, 411, 261))
        self.groupBox_2.setObjectName("groupBox_2")
        self.brigthnessLabel = QtWidgets.QLabel(self.groupBox_2)
        self.brigthnessLabel.setGeometry(QtCore.QRect(10, 40, 71, 18))
        self.brigthnessLabel.setObjectName("brigthnessLabel")
        self.brigthnesSlider = QtWidgets.QSlider(self.groupBox_2)
        self.brigthnesSlider.setGeometry(QtCore.QRect(100, 40, 201, 16))
        self.brigthnesSlider.setAutoFillBackground(False)
        self.brigthnesSlider.setMaximum(20)
        self.brigthnesSlider.setSingleStep(1)
        self.brigthnesSlider.setSliderPosition(10)
        self.brigthnesSlider.setOrientation(QtCore.Qt.Horizontal)
        self.brigthnesSlider.setInvertedAppearance(False)
        self.brigthnesSlider.setTickPosition(QtWidgets.QSlider.TicksBothSides)
        self.brigthnesSlider.setTickInterval(1)
        self.brigthnesSlider.setObjectName("brigthnesSlider")
        self.brigthnessLcd = QtWidgets.QDoubleSpinBox(self.groupBox_2)
        self.brigthnessLcd.setGeometry(QtCore.QRect(330, 30, 62, 27))
        self.brigthnessLcd.setFrame(True)
        self.brigthnessLcd.setReadOnly(False)
        self.brigthnessLcd.setButtonSymbols(QtWidgets.QAbstractSpinBox.PlusMinus)
        self.brigthnessLcd.setKeyboardTracking(False)
        self.brigthnessLcd.setProperty("showGroupSeparator", False)
        self.brigthnessLcd.setSingleStep(0.1)
        self.brigthnessLcd.setProperty("value", 1.0)
        self.brigthnessLcd.setObjectName("brigthnessLcd")
        self.label = QtWidgets.QLabel(self.groupBox_2)
        self.label.setGeometry(QtCore.QRect(10, 90, 58, 18))
        self.label.setObjectName("label")
        self.contrastSlider = QtWidgets.QSlider(self.groupBox_2)
        self.contrastSlider.setGeometry(QtCore.QRect(100, 90, 201, 16))
        self.contrastSlider.setAutoFillBackground(False)
        self.contrastSlider.setMaximum(20)
        self.contrastSlider.setSingleStep(1)
        self.contrastSlider.setSliderPosition(10)
        self.contrastSlider.setOrientation(QtCore.Qt.Horizontal)
        self.contrastSlider.setInvertedAppearance(False)
        self.contrastSlider.setTickPosition(QtWidgets.QSlider.TicksBothSides)
        self.contrastSlider.setTickInterval(1)
        self.contrastSlider.setObjectName("contrastSlider")
        self.contrastLcd = QtWidgets.QDoubleSpinBox(self.groupBox_2)
        self.contrastLcd.setGeometry(QtCore.QRect(330, 80, 62, 27))
        self.contrastLcd.setFrame(True)
        self.contrastLcd.setReadOnly(False)
        self.contrastLcd.setButtonSymbols(QtWidgets.QAbstractSpinBox.PlusMinus)
        self.contrastLcd.setKeyboardTracking(False)
        self.contrastLcd.setProperty("showGroupSeparator", False)
        self.contrastLcd.setSingleStep(0.1)
        self.contrastLcd.setProperty("value", 1.0)
        self.contrastLcd.setObjectName("contrastLcd")
        self.saveButton = QtWidgets.QPushButton(self.groupBox_2)
        self.saveButton.setGeometry(QtCore.QRect(320, 210, 80, 26))
        self.saveButton.setObjectName("saveButton")
        self.groupBox = QtWidgets.QGroupBox(Form)
        self.groupBox.setGeometry(QtCore.QRect(440, 10, 421, 561))
        self.groupBox.setObjectName("groupBox")
        self.scrollArea = QtWidgets.QScrollArea(self.groupBox)
        self.scrollArea.setGeometry(QtCore.QRect(0, 20, 421, 541))
        self.scrollArea.setWidgetResizable(True)
        self.scrollArea.setObjectName("scrollArea")
        self.scrollAreaWidgetContents = QtWidgets.QWidget()
        self.scrollAreaWidgetContents.setGeometry(QtCore.QRect(0, 0, 419, 539))
        self.scrollAreaWidgetContents.setObjectName("scrollAreaWidgetContents")
        self.image = QtWidgets.QLabel(self.scrollAreaWidgetContents)
        self.image.setGeometry(QtCore.QRect(0, 0, 411, 531))
        self.image.setText("")
        self.image.setScaledContents(True)
        self.image.setObjectName("image")
        self.scrollArea.setWidget(self.scrollAreaWidgetContents)
        self.scanButton = QtWidgets.QPushButton(Form)
        self.scanButton.setGeometry(QtCore.QRect(340, 280, 80, 26))
        self.scanButton.setObjectName("scanButton")

        self.retranslateUi(Form)
        QtCore.QMetaObject.connectSlotsByName(Form)

    def retranslateUi(self, Form):
        _translate = QtCore.QCoreApplication.translate
        Form.setWindowTitle(_translate("Form", "Form"))
        self.groupBox_2.setTitle(_translate("Form", "Image Enhacement"))
        self.brigthnessLabel.setText(_translate("Form", "Brigthness"))
        self.label.setText(_translate("Form", "Contrast"))
        self.saveButton.setText(_translate("Form", "Save"))
        self.groupBox.setTitle(_translate("Form", "Image View"))
        self.scanButton.setText(_translate("Form", "Scan"))


if __name__ == "__main__":
    import sys
    app = QtWidgets.QApplication(sys.argv)
    Form = QtWidgets.QWidget()
    ui = Ui_Form()
    ui.setupUi(Form)
    Form.show()
    sys.exit(app.exec_())
