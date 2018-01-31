# -*- coding: utf-8 -*-

"""
Module implementing MainWindow.
"""
import os
from configparser import ConfigParser

from PyQt5 import QtWidgets
from PyQt5.QtCore import pyqtSlot
from PyQt5.QtWidgets import QFileDialog
from PyQt5.QtWidgets import QMainWindow
from PyQt5.QtWidgets import QMessageBox

from Ui_main import Ui_MainWindow
from tool import KuxToMP4Tool


class MainWindow(QMainWindow, Ui_MainWindow):
    """
    Class documentation goes here.
    """

    def __init__(self, parent=None):
        """
        Constructor
        
        @param parent reference to the parent widget
        @type QWidget
        """
        super(MainWindow, self).__init__(parent)
        self.setupUi(self)
        self.ffmpeg = ""
        self.output = ""
        self.input_list = []
        self.__init_my_data()

    def __init_my_data(self):
        self.cf = ConfigParser()
        self.cf.read("config.ini")
        if len(self.cf.sections()) != 0:
            info = self.cf.options("info")
            if "ffmpeg" in info:
                self.ffmpeg = self.cf.get("info", "ffmpeg")
                self.ffmpegText.setText(self.ffmpeg)
            else:
                print("无ffmpeg数据")
            if "output" in info:
                self.output = self.cf.get("info", "output")
                self.outputText.setText(self.output)
            else:
                print("无output数据")

    @pyqtSlot()
    def on_addFilesButton_pressed(self):
        self.input_list.clear()
        input = QFileDialog.getExistingDirectory(self, "请选择输入文件夹")
        for root, dirs, files in os.walk(input):
            for name in files:
                filepath = os.path.join(root, name)
                if os.path.splitext(filepath)[1] == ".kux":
                    self.input_list.append(filepath)
        print("选择输入文件夹路径为:%s" % input)

        # 刷新列表
        self.listWidget.clear()
        for item in self.input_list:
            self.listWidget.addItem(item)
        self.__check_exec_button_enable()

    @pyqtSlot()
    def on_execButton_pressed(self):
        self.execButton.setEnabled(False)

        tool = KuxToMP4Tool(self.ffmpeg, self.output)
        success_list = []
        for i, file_path in enumerate(self.input_list):
            if tool.transcoding(file_path):
                success_list.append(file_path)
                self.progressBar.setValue(int((i + 1) / len(self.input_list) * 100))

        success_count = len(success_list)
        for i in success_list:
            self.input_list.remove(i)
        QMessageBox.information(self, "信息", "成功转码%d个文件,失败%d个" % (success_count, len(self.input_list)))
        self.execButton.setEnabled(True)
        self.progressBar.setValue(0)

        # 刷新列表
        self.listWidget.clear()
        for item in self.input_list:
            self.listWidget.addItem(item)
        return

    @pyqtSlot()
    def on_setFFmpegPath_pressed(self):
        self.ffmpeg = QFileDialog.getOpenFileName(self, "请选择ffmpeg.exe", "", "ffmpeg(*.exe)")[0]
        self.ffmpegText.setText(self.ffmpeg)
        if len(self.cf.sections()) == 0:
            self.cf.add_section("info")
        self.cf.set("info", "ffmpeg", self.ffmpeg)
        self.cf.write(open("config.ini", "w"))
        print("选择ffmpeg.exe路径为:%s" % self.ffmpeg)
        self.__check_exec_button_enable()

    @pyqtSlot()
    def on_setOutputPath_pressed(self):
        self.output = QFileDialog.getExistingDirectory(self, "请选择输出文件夹")
        self.outputText.setText(self.output)
        if len(self.cf.sections()) == 0:
            self.cf.add_section("info")
        self.cf.set("info", "output", self.output)
        self.cf.write(open("config.ini", "w"))
        print("选择输出文件夹路径为:%s" % self.output)
        self.__check_exec_button_enable()

    @pyqtSlot()
    def on_clearAllButton_pressed(self):
        self.input_list.clear()
        self.listWidget.clear()
        self.__check_exec_button_enable()

    def __check_exec_button_enable(self):
        if self.ffmpeg == "" or self.output == "" or len(self.input_list) == 0:
            self.execButton.setEnabled(False)
        else:
            self.execButton.setEnabled(True)


if __name__ == "__main__":
    import sys

    app = QtWidgets.QApplication(sys.argv)
    ui = MainWindow()
    ui.show()
    sys.exit(app.exec_())
