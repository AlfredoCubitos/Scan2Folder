# This Python file uses the following encoding: utf-8
import sys, io
from PyQt5.QtWidgets import QWidget, QGraphicsScene, QGraphicsPixmapItem
from PyQt5 import uic
from PyQt5.QtGui import QPixmap, QImage
from PyQt5.QtCore import QObject, pyqtSignal, pyqtSlot, QBuffer, Qt
from PIL import ImageEnhance, Image, ImageQt
import numpy as np
from ui_configform import Ui_Form

class ConfigWindow(QWidget):
    def __init__(self):
        super().__init__()
        #self.ui = uic.loadUi("configform.ui", self)
        self.ui = Ui_Form()
        self.ui.setupUi(self)

        self.ui.brigthnesSlider.valueChanged.connect(self.brigthnesSlot)
        self.ui.contrastSlider.valueChanged.connect(self.contrastSlot)

        self.ui.brigthnessLcd.valueChanged.connect(self.setBrightSlider)
        self.ui.contrastLcd.valueChanged.connect(self.setContastSlider)

        self.scene = QGraphicsScene()
        self.pixmap = QPixmap()
        self.pixmapItem = QGraphicsPixmapItem()
        self.scene.addItem(self.pixmapItem)
        self.ui.view.setScene(self.scene)
        #self.ui.view.fitInView(self.pixmapItem,Qt.KeepAspectRatio)
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
       # self.im = None


    @pyqtSlot(int)
    def brigthnesSlot(self,int):
        
        val =int/10
        self.ui.brigthnessLcd.blockSignals(True)
        self.ui.brigthnessLcd.setValue(val)
        self.ui.brigthnessLcd.blockSignals(False)
        contrast = self.ui.contrastSlider.value()/10
        self.enhanceImage(val,contrast)
        
    
    @pyqtSlot(int)
    def contrastSlot(self,int):
        val =int/10
        self.ui.contrastLcd.blockSignals(True)
        self.ui.contrastLcd.setValue(val)
        self.ui.contrastLcd.blockSignals(False)
        bright = self.ui.brigthnesSlider.value()/10
        self.enhanceImage(bright,val)
       

    @pyqtSlot(float)
    def setBrightSlider(self,val):
        value = val*10
        self.ui.brigthnesSlider.blockSignals(True)
        self.ui.brigthnesSlider.setValue(int(value))
        self.ui.brigthnesSlider.blockSignals(False)
    
    @pyqtSlot(float)
    def setContastSlider(self,val):
        value = val*10
        self.ui.contrastSlider.blockSignals(True)
        self.ui.contrastSlider.setValue(int(value))
        self.ui.contrastSlider.blockSignals(False)
    
    def enhanceImage(self, bright, cont):
       # self.setBufferImage()
        brightness = ImageEnhance.Brightness(self.pilBufferImg)
        pilImg = brightness.enhance(bright)
        contrast = ImageEnhance.Contrast(pilImg)
        pilImg = contrast.enhance(cont)
        self.pixmapItem.setPixmap(self.pixmap.fromImage(ImageQt.ImageQt(pilImg.convert('RGBA'))))

        
    def setBufferImage(self):
        img = self.pixmapItem.pixmap()
        self.buffer.open(QBuffer.ReadWrite)
        img.save(self.buffer,"PNG")
        self.pilBufferImg = Image.open(io.BytesIO(self.buffer.data()))
        self.buffer.close()