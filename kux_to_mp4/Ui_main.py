# -*- coding: utf-8 -*-

# Form implementation generated from reading ui file 'D:\Ban\PycharmProjects\bantest\kux_to_mp4\main.ui'
#
# Created by: PyQt5 UI code generator 5.10
#
# WARNING! All changes made in this file will be lost!

from PyQt5 import QtCore, QtGui, QtWidgets

class Ui_MainWindow(object):
    def setupUi(self, MainWindow):
        MainWindow.setObjectName("MainWindow")
        MainWindow.setEnabled(True)
        MainWindow.resize(623, 273)
        self.centralWidget = QtWidgets.QWidget(MainWindow)
        self.centralWidget.setEnabled(True)
        self.centralWidget.setStatusTip("")
        self.centralWidget.setObjectName("centralWidget")
        self.addFilesButton = QtWidgets.QPushButton(self.centralWidget)
        self.addFilesButton.setGeometry(QtCore.QRect(520, 10, 91, 21))
        self.addFilesButton.setObjectName("addFilesButton")
        self.execButton = QtWidgets.QPushButton(self.centralWidget)
        self.execButton.setEnabled(False)
        self.execButton.setGeometry(QtCore.QRect(520, 70, 91, 131))
        self.execButton.setObjectName("execButton")
        self.ffmpegText = QtWidgets.QLineEdit(self.centralWidget)
        self.ffmpegText.setGeometry(QtCore.QRect(110, 210, 391, 21))
        self.ffmpegText.setText("")
        self.ffmpegText.setObjectName("ffmpegText")
        self.setFFmpegPath = QtWidgets.QPushButton(self.centralWidget)
        self.setFFmpegPath.setGeometry(QtCore.QRect(520, 210, 91, 21))
        self.setFFmpegPath.setObjectName("setFFmpegPath")
        self.label = QtWidgets.QLabel(self.centralWidget)
        self.label.setGeometry(QtCore.QRect(10, 210, 101, 21))
        self.label.setAlignment(QtCore.Qt.AlignCenter)
        self.label.setWordWrap(False)
        self.label.setObjectName("label")
        self.setOutputPath = QtWidgets.QPushButton(self.centralWidget)
        self.setOutputPath.setGeometry(QtCore.QRect(520, 240, 91, 21))
        self.setOutputPath.setObjectName("setOutputPath")
        self.label_2 = QtWidgets.QLabel(self.centralWidget)
        self.label_2.setGeometry(QtCore.QRect(10, 240, 101, 21))
        self.label_2.setAlignment(QtCore.Qt.AlignCenter)
        self.label_2.setWordWrap(False)
        self.label_2.setObjectName("label_2")
        self.outputText = QtWidgets.QLineEdit(self.centralWidget)
        self.outputText.setGeometry(QtCore.QRect(110, 240, 391, 21))
        self.outputText.setObjectName("outputText")
        self.clearAllButton = QtWidgets.QPushButton(self.centralWidget)
        self.clearAllButton.setGeometry(QtCore.QRect(520, 40, 91, 21))
        self.clearAllButton.setObjectName("clearAllButton")
        self.listWidget = QtWidgets.QListWidget(self.centralWidget)
        self.listWidget.setGeometry(QtCore.QRect(15, 10, 491, 161))
        self.listWidget.setObjectName("listWidget")
        self.progressBar = QtWidgets.QProgressBar(self.centralWidget)
        self.progressBar.setGeometry(QtCore.QRect(20, 180, 481, 23))
        self.progressBar.setProperty("value", 0)
        self.progressBar.setObjectName("progressBar")
        MainWindow.setCentralWidget(self.centralWidget)

        self.retranslateUi(MainWindow)
        QtCore.QMetaObject.connectSlotsByName(MainWindow)

    def retranslateUi(self, MainWindow):
        _translate = QtCore.QCoreApplication.translate
        MainWindow.setWindowTitle(_translate("MainWindow", "KuxToMP4 by:Ban"))
        self.addFilesButton.setText(_translate("MainWindow", "添加文件夹"))
        self.execButton.setText(_translate("MainWindow", "转码"))
        self.setFFmpegPath.setText(_translate("MainWindow", "设置"))
        self.label.setText(_translate("MainWindow", "ffmpeg.exe路径:"))
        self.setOutputPath.setText(_translate("MainWindow", "设置"))
        self.label_2.setText(_translate("MainWindow", "文件输出目录:"))
        self.clearAllButton.setText(_translate("MainWindow", "清除全部"))


if __name__ == "__main__":
    import sys
    app = QtWidgets.QApplication(sys.argv)
    MainWindow = QtWidgets.QMainWindow()
    ui = Ui_MainWindow()
    ui.setupUi(MainWindow)
    MainWindow.show()
    sys.exit(app.exec_())

