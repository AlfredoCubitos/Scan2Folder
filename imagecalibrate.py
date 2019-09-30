# This Python file uses the following encoding: utf-8
import sys, io
from PyQt5.QtWidgets import QWidget
from PyQt5 import uic
from PyQt5.QtGui import QPixmap, QImage
from PyQt5.QtCore import QObject, pyqtSignal, pyqtSlot, QBuffer
from PIL import ImageEnhance, Image, ImageQt
import numpy as np
from ui_configform import Ui_Form

class ConfigWindow(QWidget):
    def __init__(self):
        super().__init__()
        #self.ui = uic.loadUi("configform.ui", self)
        self.ui = Ui_Form()
        self.ui.setupUi(self)

        self.ui.brigthnesSlider.sliderMoved.connect(self.brigthnesSlot)
        self.ui.contrastSlider.sliderMoved.connect(self.contrastSlot)

        self.ui.brigthnessLcd.valueChanged.connect(self.setBrightSlider)
        self.ui.contrastLcd.valueChanged.connect(self.setContastSlider)

        self.pixmap = QPixmap()
        #self.pixmap.load("Calibrate_Test_1.png")
        self.buffer = QBuffer()
        self.pilBufferImg = "/tmp/san2foldertempimg.png"

        self.brightSet=False
        self.contrastSet=False
        self.imChanged=False

        self.bright = self.ui.brigthnesSlider.maximum()/2
        self.contast = self.ui.contrastSlider.maximum()/2



       # self.im = Image.open("Calibrate_Test_1.png")
       # img = ImageQt.ImageQt(self.im.convert('RGBA'))
       # self.image.setPixmap(self.pixmap.fromImage(img))
        self.im = None


    @pyqtSlot(int)
    def brigthnesSlot(self,int):
        
        val =int/10
        self.ui.brigthnessLcd.setValue(val)
        self.brightSet=True

        if self.brightSet and self.contrastSet:
            if not self.imChanged:
                pix = self.image.pixmap()
                pix.save(self.pilBufferImg)
                self.imChanged=True

        if self.contrastSet:
            pix = Image.open(self.pilBufferImg)
            brightness = ImageEnhance.Brightness(pix)
        else:
            brightness = ImageEnhance.Brightness(self.im)

        pil = brightness.enhance(val)
    
        im = ImageQt.ImageQt(pil.convert('RGBA'))
        
        self.image.setPixmap(self.pixmap.fromImage(im))
    
    @pyqtSlot(int)
    def contrastSlot(self,int):
        val =int/10
        self.ui.contrastLcd.setValue(val)
        self.contrastSet=True

        if self.brightSet and self.contrastSet:
            if not self.imChanged:
                pix = self.image.pixmap()
                pix.save(self.pilBufferImg)
                self.imChanged=True

        if self.brightSet:
            pix = Image.open(self.pilBufferImg)
            contrast = ImageEnhance.Contrast(pix)
        else:
            contrast = ImageEnhance.Contrast(self.im)

        pil = contrast.enhance(val)
    
        im = ImageQt.ImageQt(pil.convert('RGBA'))
        
        self.image.setPixmap(self.pixmap.fromImage(im))

    @pyqtSlot(float)
    def setBrightSlider(self,val):
        value = val*10
        self.ui.brigthnesSlider.setValue(int(value))
    
    @pyqtSlot(float)
    def setContastSlider(self,val):
        value = val*10
        self.ui.contrastSlider.setValue(int(value))

        
    def setBufferImage(self):
        img = self.image.pixmap()
        self.buffer.open(QBuffer.ReadWrite)
        img.save(self.buffer,"PNG")
        self.pilBufferImg = Image.open(io.BytesIO(self.buffer.data()))
        self.buffer.close()
