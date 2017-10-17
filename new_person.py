# -*- coding: utf-8 -*-

"""
Module implementing Dialog.
"""

from PyQt5.QtCore import pyqtSlot
from PyQt5.QtWidgets import QDialog
from PyQt5.QtGui import QColor
from PyQt5.QtWidgets import QColorDialog

from Ui_new_person import Ui_Dialog


class Dialog(QDialog, Ui_Dialog):
    """
    Class documentation goes here.
    """

    def __init__(self, func, parent=None):
        """
        Constructor
        
        @param parent reference to the parent widget
        @type QWidget
        """
        super(Dialog, self).__init__(parent)
        self.setupUi(self)
        self.add = func
        self.name = "某"
        self.color = "#000000"

    @pyqtSlot()
    def on_buttonBox_accepted(self):
        self.name = self.lineEdit.text()
        dict = {"name": self.name, "color": self.color}
        self.add(dict)

    @pyqtSlot()
    def on_colorButton_clicked(self):
        newColor = QColorDialog.getColor()
        cyanInk = hex(QColor(newColor).red())[2:4].zfill(2)
        magentaInk = hex(QColor(newColor).green())[2:4].zfill(2)
        yellowInk = hex(QColor(newColor).blue())[2:4].zfill(2)

        color = "#" + cyanInk + magentaInk + yellowInk
        self.color = color.upper()
