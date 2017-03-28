# -*- coding: utf-8 -*-

# Form implementation generated from reading ui file 'resolutionHelp.ui'
#
# Created: Fri May 20 16:52:19 2016
#      by: pyside-uic 0.2.15 running on PySide 1.2.4
#
# WARNING! All changes made in this file will be lost!

from PySide import QtCore, QtGui

class Ui_Dialog(object):
    def setupUi(self, Dialog):
        Dialog.setObjectName("Dialog")
        Dialog.resize(625, 545)
        self.gridLayout = QtGui.QGridLayout(Dialog)
        self.gridLayout.setObjectName("gridLayout")
        self.verticalLayout = QtGui.QVBoxLayout()
        self.verticalLayout.setObjectName("verticalLayout")
        self.label = QtGui.QLabel(Dialog)
        self.label.setWordWrap(True)
        self.label.setObjectName("label")
        self.verticalLayout.addWidget(self.label)
        self.gridLayout_2 = QtGui.QGridLayout()
        self.gridLayout_2.setObjectName("gridLayout_2")
        self.label_2 = QtGui.QLabel(Dialog)
        self.label_2.setObjectName("label_2")
        self.gridLayout_2.addWidget(self.label_2, 1, 0, 1, 1)
        self.label_5 = QtGui.QLabel(Dialog)
        self.label_5.setAlignment(QtCore.Qt.AlignCenter)
        self.label_5.setObjectName("label_5")
        self.gridLayout_2.addWidget(self.label_5, 0, 1, 1, 1)
        self.label_7 = QtGui.QLabel(Dialog)
        self.label_7.setObjectName("label_7")
        self.gridLayout_2.addWidget(self.label_7, 2, 1, 1, 1)
        self.label_6 = QtGui.QLabel(Dialog)
        self.label_6.setObjectName("label_6")
        self.gridLayout_2.addWidget(self.label_6, 2, 0, 1, 1)
        self.label_4 = QtGui.QLabel(Dialog)
        self.label_4.setObjectName("label_4")
        self.gridLayout_2.addWidget(self.label_4, 1, 1, 1, 1)
        self.label_3 = QtGui.QLabel(Dialog)
        self.label_3.setAlignment(QtCore.Qt.AlignCenter)
        self.label_3.setObjectName("label_3")
        self.gridLayout_2.addWidget(self.label_3, 0, 0, 1, 1)
        self.label_8 = QtGui.QLabel(Dialog)
        self.label_8.setObjectName("label_8")
        self.gridLayout_2.addWidget(self.label_8, 3, 0, 1, 1)
        self.label_9 = QtGui.QLabel(Dialog)
        self.label_9.setObjectName("label_9")
        self.gridLayout_2.addWidget(self.label_9, 3, 1, 1, 1)
        self.label_10 = QtGui.QLabel(Dialog)
        self.label_10.setObjectName("label_10")
        self.gridLayout_2.addWidget(self.label_10, 4, 0, 1, 1)
        self.label_12 = QtGui.QLabel(Dialog)
        self.label_12.setObjectName("label_12")
        self.gridLayout_2.addWidget(self.label_12, 5, 0, 1, 1)
        self.label_11 = QtGui.QLabel(Dialog)
        self.label_11.setObjectName("label_11")
        self.gridLayout_2.addWidget(self.label_11, 4, 1, 1, 1)
        self.label_13 = QtGui.QLabel(Dialog)
        self.label_13.setObjectName("label_13")
        self.gridLayout_2.addWidget(self.label_13, 5, 1, 1, 1)
        self.label_14 = QtGui.QLabel(Dialog)
        self.label_14.setObjectName("label_14")
        self.gridLayout_2.addWidget(self.label_14, 6, 0, 1, 1)
        self.label_15 = QtGui.QLabel(Dialog)
        self.label_15.setObjectName("label_15")
        self.gridLayout_2.addWidget(self.label_15, 6, 1, 1, 1)
        self.verticalLayout.addLayout(self.gridLayout_2)
        self.buttonBox = QtGui.QDialogButtonBox(Dialog)
        self.buttonBox.setOrientation(QtCore.Qt.Horizontal)
        self.buttonBox.setStandardButtons(QtGui.QDialogButtonBox.Ok)
        self.buttonBox.setObjectName("buttonBox")
        self.verticalLayout.addWidget(self.buttonBox)
        self.gridLayout.addLayout(self.verticalLayout, 0, 0, 1, 1)

        self.retranslateUi(Dialog)
        QtCore.QObject.connect(self.buttonBox, QtCore.SIGNAL("accepted()"), Dialog.accept)
        QtCore.QObject.connect(self.buttonBox, QtCore.SIGNAL("rejected()"), Dialog.reject)
        QtCore.QMetaObject.connectSlotsByName(Dialog)

    def retranslateUi(self, Dialog):
        Dialog.setWindowTitle(QtGui.QApplication.translate("Dialog", "Dialog", None, QtGui.QApplication.UnicodeUTF8))
        self.label.setText(QtGui.QApplication.translate("Dialog", "The resolution setting for the 34401 takes two parameters. First is \"max\" which is the point at which the DMM returns and overload result. Make sure to set this higher than your measurement is likely to go. An example would be setting this to \"15\" to measure a 12v source. Another would be \"200\" if you were measuring the frequency of a US AC outlet.\n"
"\n"
"The second part of the resolution setting is where the decimal point is in relation to how large of a sample you are going to take. You can set 4.5 to 6.5 digits of resolution. You cannot sample at less than 4.5 digits. The easiest way to think about setting is to treat it like a \"minimum\" setting that get overruled. If you set max to \"1\" and set the decimal to \"0.1\" you will still get a result like this \"0.0000\" because you can\'t sample below 4.5 digits. When setting this value take into account the the maximum you set. If ou are measuring an 80V signal and set max to \"100\" you cannot set the decimal below \"0.0001\" because you have locked some digits in the max. If you wanted to get a maximum decimal reading you could set max to \"1\" and the decimal to \"0.000001\"\n"
"\n"
"The higher the number of digits the longer it takes to finish the sample collection. Below is a chart from the manual that gives the best estimates of times for different digits. (Note: The slow readings seems to be the most common)", None, QtGui.QApplication.UnicodeUTF8))
        self.label_2.setText(QtGui.QApplication.translate("Dialog", "4.5 Fast", None, QtGui.QApplication.UnicodeUTF8))
        self.label_5.setText(QtGui.QApplication.translate("Dialog", "Sample Time", None, QtGui.QApplication.UnicodeUTF8))
        self.label_7.setText(QtGui.QApplication.translate("Dialog", "16.7 ms", None, QtGui.QApplication.UnicodeUTF8))
        self.label_6.setText(QtGui.QApplication.translate("Dialog", "4.5 Slow", None, QtGui.QApplication.UnicodeUTF8))
        self.label_4.setText(QtGui.QApplication.translate("Dialog", "400 us", None, QtGui.QApplication.UnicodeUTF8))
        self.label_3.setText(QtGui.QApplication.translate("Dialog", "Digits", None, QtGui.QApplication.UnicodeUTF8))
        self.label_8.setText(QtGui.QApplication.translate("Dialog", "5.5 Fast", None, QtGui.QApplication.UnicodeUTF8))
        self.label_9.setText(QtGui.QApplication.translate("Dialog", "3 ms", None, QtGui.QApplication.UnicodeUTF8))
        self.label_10.setText(QtGui.QApplication.translate("Dialog", "5.5 Slow", None, QtGui.QApplication.UnicodeUTF8))
        self.label_12.setText(QtGui.QApplication.translate("Dialog", "6.5 Fast", None, QtGui.QApplication.UnicodeUTF8))
        self.label_11.setText(QtGui.QApplication.translate("Dialog", "167 ms", None, QtGui.QApplication.UnicodeUTF8))
        self.label_13.setText(QtGui.QApplication.translate("Dialog", "167 ms", None, QtGui.QApplication.UnicodeUTF8))
        self.label_14.setText(QtGui.QApplication.translate("Dialog", "6.5 Slow", None, QtGui.QApplication.UnicodeUTF8))
        self.label_15.setText(QtGui.QApplication.translate("Dialog", "1.67 s", None, QtGui.QApplication.UnicodeUTF8))

