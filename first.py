# -*- coding: utf-8 -*-

"""
Module implementing MainWindow.
"""

import _thread
import time
import json
import os
from PyQt5 import QtCore, QtGui, QtWidgets
from PyQt5.QtCore import pyqtSlot, QFileInfo, QPoint
from PyQt5.QtGui import QColor
from PyQt5.QtWidgets import QMainWindow, QMenu, QAction
from PyQt5.QtWidgets import QListWidgetItem
from PyQt5.QtWidgets import QFileDialog, QMessageBox, QColorDialog

from Ui_first import Ui_MainWindow
from music import MyMusicPlayer
from new_person import Dialog


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
        self.player = MyMusicPlayer()
        self.played = False
        self.sliderPress = False
        self.edit = False
        self.insert = False
        self.person = []
        # self.person.append({"name": "春", "color": "#FF0000"})
        # self.person.append({"name": "班", "color": "#00FF00"})
        self.subtitle = []
        # self.subtitle.append({"who": 0, "when": 2000.0, "what": "哈哈"})
        # self.subtitle.append({"who": 1, "when": 4000.0, "what": "si ki"})

    @pyqtSlot(QListWidgetItem)
    def on_personal_itemDoubleClicked(self, item):
        row = self.personal.currentRow()
        newColor = QColorDialog.getColor()
        cyanInk = hex(QColor(newColor).red())[2:4].zfill(2)
        magentaInk = hex(QColor(newColor).green())[2:4].zfill(2)
        yellowInk = hex(QColor(newColor).blue())[2:4].zfill(2)
        color = "#" + cyanInk + magentaInk + yellowInk
        color = color.upper()

        self.person[row]["color"] = color;
        self.set_list_item(self.person[row]["name"], self.person[row]["color"], item)

    @pyqtSlot()
    def on_personDButton_clicked(self):
        row = self.personal.currentRow()
        del self.person[row]
        self.refresh_person()

    @pyqtSlot(QListWidgetItem)
    def on_listWidget_itemDoubleClicked(self, item):
        self.selectSubtitlePositsion = self.listWidget.currentRow()
        dict = self.subtitle[self.selectSubtitlePositsion]
        self.comboBox.setCurrentIndex(dict['who'])
        self.addSubtitleText.setText(dict['what'])
        self.edit = True
        self.insert = True
        self.insertBtn.setEnabled(True)

    @pyqtSlot()
    def on_playButton_clicked(self):
        self.player.play()
        self.startUpdateShowTime()

    @pyqtSlot()
    def on_horizontalSlider_sliderReleased(self):
        go = self.horizontalSlider.value() / 1000 * self.player.getTotalTime()
        self.player.goToAndPlay(go, self.startUpdateShowTime)
        self.sliderPress = False;

    @pyqtSlot()
    def on_horizontalSlider_sliderPressed(self):
        self.sliderPress = True

    @pyqtSlot()
    def on_timeDButton_clicked(self):
        # QMessageBox.warning(self, "Waring", "DirectSoundCreate: No audio device found")
        go = self.player.getCurrentTime() - float(self.lineEdit.text()) * 1000
        go /= 1000
        if go <= 0:
            return
        self.player.goToAndPlay(go, self.startUpdateShowTime)

    @pyqtSlot()
    def on_timeIButton_clicked(self):
        go = self.player.getCurrentTime() + float(self.lineEdit.text()) * 1000
        go /= 1000
        if go >= self.player.getTotalTime():
            return
        self.player.goToAndPlay(go, self.startUpdateShowTime)

    @pyqtSlot()
    def on_personIButton_clicked(self):
        ui = Dialog(self.add_person)
        ui.show()
        ui.exec_()

    @pyqtSlot()
    def on_submit_clicked(self):
        dict = {}
        dict['who'] = self.comboBox.currentIndex()
        dict['what'] = self.addSubtitleText.text()

        if self.edit:
            dict['when'] = self.subtitle[self.selectSubtitlePositsion]['when']
            self.subtitle[self.selectSubtitlePositsion].update(dict)
            self.edit = False;
        else:
            when = self.player.getCurrentTime()
            dict['when'] = when
            self.subtitle.append(dict)
            self.listWidget.addItem(self.get_subtitle_list_item(dict))

        self.refresh_subtitle()
        self.auto_save()

        self.addSubtitleText.clear()
        self.insert = False
        self.insertBtn.setEnabled(False)

    @pyqtSlot()
    def on_action_triggered(self):
        musicPath, filetype = QFileDialog.getOpenFileName(self, "open mp3", "", "Images (*.mp3)")
        if musicPath != '':
            self.player.loadMusic(musicPath)
            self.loadMusicFinish()

    @pyqtSlot()
    def on_actionOpen_Subtitle_triggered(self):
        path, filetype = QFileDialog.getOpenFileName(self, "open subtile", "", "BanSubtitle (*.bst)")
        if path != '':
            self.load_subtitle_info(path)

    @pyqtSlot()
    def on_Save_clicked(self):
        self.save_subtitle_info()

    @pyqtSlot(QPoint)
    def on_listWidget_customContextMenuRequested(self, pos):
        popMenu = QMenu(self.listWidget)
        popMenu.addAction(QAction("Delete", self, triggered=self.delete_subtitle))
        popMenu.exec_(QtGui.QCursor.pos())

    @pyqtSlot()
    def on_insertBtn_clicked(self):
        print("click")
        if self.insert:
            my_dict = dict()
            my_dict['when'] = self.player.getCurrentTime() - 1500  # 先听到声音再按，并把时间推前1.5秒
            go_next = False
            if self.subtitle[self.selectSubtitlePositsion]['when'] > my_dict['when']:
                go_next = True

            self.subtitle[self.selectSubtitlePositsion].update(my_dict)
            self.refresh_subtitle()
            self.auto_save()

            if go_next:
                self.listWidget.setCurrentRow(self.selectSubtitlePositsion + 1)
            else:
                self.listWidget.setCurrentRow(self.selectSubtitlePositsion)

            self.on_listWidget_itemDoubleClicked(None)

    @pyqtSlot()
    def on_setBtn_clicked(self):
        try:
            print(self.plainTextEdit.toPlainText())
            j = json.loads(self.plainTextEdit.toPlainText())
        except:
            my_data = dict()
            my_data['person'] = self.person
            my_data['subtitle'] = self.subtitle
            self.plainTextEdit.clear()
            self.plainTextEdit.appendPlainText(json.dumps(my_data, indent=2, separators=(',', ':')))
            QMessageBox.warning(self, "Waring", "Json wrong format")
            return
        self.person = j['person']
        self.subtitle = j['subtitle']
        self.refresh_person()

    #
    # 非自动生成的代码
    #
    def startUpdateShowTime(self):
        if not self.played:
            self.played = True
            _thread.start_new_thread(self.update_timeshow, ("thread1",))
        if self.player.playing:
            self.playButton.setText("Pause")
        else:
            self.playButton.setText("Play")

    def loadMusicFinish(self):
        totalTime = str(int(self.player.getTotalTime() // 60)).zfill(2) + ":" + str(int(
            self.player.getTotalTime() % 60)).zfill(2)
        self.timeShow.setText("00:00/" + totalTime)
        self.playButton.setText("Play")

    def update_timeshow(self, name):
        print("totalTime:", self.player.getTotalTime())
        totalTime = str(int(self.player.getTotalTime() // 60)).zfill(2) + ":" + str(int(
            self.player.getTotalTime() % 60)).zfill(2)
        while self.player.playing or self.player.mixer.music.get_busy():
            if self.player.getCurrentTime() < 0:
                self.player.playing = False
            if (self.player.playing and not self.sliderPress):
                currentTime = str(int(self.player.getCurrentTime() / 1000 // 60)).zfill(2) + ":" + str(int(
                    self.player.getCurrentTime() / 1000 % 60)).zfill(2)
                showText = currentTime + "/" + totalTime
                print(showText)
                self.timeShow.setText(showText)
                # 进度条
                self.horizontalSlider.setValue(self.player.getCurrentTime() / self.player.getTotalTime())
            else:
                print("pause")
            time.sleep(0.5)
        self.played = False

    # 设置好list item并返回
    def get_list_item(self, text, color):
        red = int(color[1:3], 16)
        green = int(color[3:5], 16)
        blue = int(color[5:7], 16)

        item = QtWidgets.QListWidgetItem()
        if red == 0xff and green == 0xff and blue == 0xff:  # 为白色的话
            text += "(白色字体)"
        else:
            brush = QtGui.QBrush(QtGui.QColor(red, green, blue))
            brush.setStyle(QtCore.Qt.SolidPattern)
            item.setForeground(brush)
        item.setText(text)

        return item

    # 设置list item
    def set_list_item(self, text, color, item):
        red = int(color[1:3], 16)
        green = int(color[3:5], 16)
        blue = int(color[5:7], 16)

        brush = QtGui.QBrush(QtGui.QColor(red, green, blue))
        brush.setStyle(QtCore.Qt.SolidPattern)
        item.setForeground(brush)
        item.setText(text)

    # 取字幕item
    def get_subtitle_list_item(self, dict):
        who = dict['who']
        when = dict['when']
        what = dict['what']

        color = "#000000"
        for i, item in enumerate(self.person):
            if who == i:
                color = item['color']
                break

        time = str(int(when / 1000 // 60)).zfill(2) + ":" + str(int(when / 1000 % 60)).zfill(2)
        text = "[" + time + "] " + what
        return self.get_list_item(text, color)

    # 添加人物
    def add_person(self, item):
        self.person.append(item)
        self.comboBox.addItem(item['name'])
        self.personal.addItem(self.get_list_item(item['name'], item['color']))
        self.auto_save()

    # 刷新字幕列表
    def refresh_subtitle(self):
        self.subtitle = sorted(self.subtitle, key=lambda d: d['when'])

        self.listWidget.clear()
        for i, item in enumerate(self.subtitle):
            self.listWidget.addItem(self.get_subtitle_list_item(item))

    # 刷新人物列表
    def refresh_person(self):
        self.comboBox.clear()
        self.personal.clear()
        for i, item in enumerate(self.person):
            self.comboBox.addItem(item['name'])
            self.personal.addItem(self.get_list_item(item['name'], item['color']))
        self.refresh_subtitle()

    # 保存文件
    def save_subtitle_info(self):
        info = {"person": self.person, "subtitle": self.subtitle}
        infoString = json.dumps(info, indent=2, separators=(',', ':'))

        filePath, filetype = QFileDialog.getSaveFileName(self, "save subtitle info", "", "BanSubtitle (*.bst)")

        if filePath != '':
            saveFile = open(filePath, "w")
            saveFile.write(infoString)
            saveFile.close()
        else:
            QMessageBox.warning(self, "Cannot save file",
                                "Please enter a valid filename.", QMessageBox.Cancel,
                                QMessageBox.NoButton, QMessageBox.NoButton)

    # 自动保存
    def auto_save(self):
        path = "untitle.bst"
        try:
            if self.subtitlePath != '':
                path = self.subtitlePath
        except:
            print("未载入字幕文件")

        info = {"person": self.person, "subtitle": self.subtitle}
        infoString = json.dumps(info, indent=2, separators=(',', ':'))
        saveFile = open(path, "w")
        saveFile.write(infoString)
        saveFile.close()

        self.plainTextEdit.clear()
        self.plainTextEdit.appendPlainText(infoString)

    # 载入字幕信息
    def load_subtitle_info(self, path):
        file = open(path, 'r')
        j = json.loads(file.read())
        self.person = j['person']
        self.subtitle = j['subtitle']

        self.refresh_person()
        self.subtitlePath = path
        self.plainTextEdit.clear()
        self.plainTextEdit.appendPlainText(json.dumps(j, indent=2, separators=(',', ':')))

    def delete_subtitle(self):
        del self.subtitle[self.listWidget.currentRow()]
        self.refresh_subtitle()


if __name__ == "__main__":
    import sys

    i = "♠♡♢♣♤♥♦♧"
    app = QtWidgets.QApplication(sys.argv)
    ui = MainWindow()
    ui.show()
    sys.exit(app.exec_())
