# -*- coding: utf-8 -*-

import pygame, sys, eyed3, time
from pygame import mixer
from PyQt5.QtWidgets import QMessageBox
from pygame.compat import as_unicode, filesystem_encode


class MyMusicPlayer(object):
    def __init__(self, parent=None):
        self.playing = False
        self.forward = 0.0;
        pygame.init()
        self.mixer = pygame.mixer
        try:
            self.mixer.init()
        except:
            # info=sys.exc_info()
            print("?")

    def loadMusic(self, path):
        print(path)
        # self.sound=self.mixer.Sound(path.encode("gbk"))
        self.sound = eyed3.load(path)
        self.mixer.music.load(open(path, 'rb'))

    def play(self):
        if self.playing:
            self.mixer.music.pause()
            self.playing = False
        else:
            if self.mixer.music.get_busy():
                self.mixer.music.unpause()
            else:
                self.mixer.music.play()
            self.playing = True

    def goToAndPlay(self, value, func):
        if not self.playing:
            self.playing = True
        print("goToAndPlay:", value)
        self.forward = value;
        self.mixer.music.pause()
        self.mixer.music.rewind()
        time.sleep(0.1)
        self.mixer.music.play(start=value)
        func()

    def getCurrentTime(self):
        return self.mixer.music.get_pos() + self.forward * 1000

    def getTotalTime(self):
        return self.sound.info.time_secs
