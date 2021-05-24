# This Python file uses the following encoding: utf-8
import sys, io
from PyQt5.QtWidgets import QWidget, QGraphicsScene, QGraphicsPixmapItem
from PyQt5 import uic
from PyQt5.QtGui import QPixmap, QImage
from PyQt5.QtCore import QObject, pyqtSignal, pyqtSlot, QBuffer, Qt, QPoint
from PIL import ImageEnhance, Image, ImageQt
import numpy as np
#from ui_configform import Ui_Form

class ConfigWindow(QWidget):
    def __init__(self):
        super().__init__()
        self.ui = uic.loadUi("configform.ui", self)
        #self.ui = Ui_Form()
        #self.ui.setupUi(self)

        self.ui.brigthnesSlider.valueChanged.connect(self.brigthnesSlot)
        self.ui.contrastSlider.valueChanged.connect(self.contrastSlot)

        self.ui.brigthnessLcd.valueChanged.connect(self.setBrightSlider)
        self.ui.contrastLcd.valueChanged.connect(self.setContastSlider)

        self.ui.colorSlider.valueChanged.connect(self.colorSlot)
        self.ui.sharpnessSlider.valueChanged.connect(self.sharpnessSlot)

        self.ui.colorLcd.valueChanged.connect(self.setColorSlider)
        self.ui.sharpnessLcd.valueChanged.connect(self.setSharpnessSlider)



        self.scene = QGraphicsScene()
        self.pixmap = QPixmap()
        self.pixmapItem = QGraphicsPixmapItem()
        self.scene.addItem(self.pixmapItem)
        self.ui.view.setScene(self.scene)
        #self.ui.view.fitInView(self.pixmapItem,Qt.KeepAspectRatio)
        #self.pixmap.load("Calibrate_Test_1.png")
        self.buffer = QBuffer()
        self.pilBufferImg = "/tmp/scan2foldertempimg.png"



        self.bright = self.ui.brigthnesSlider.maximum()/2
        self.contast = self.ui.contrastSlider.maximum()/2


    def wheelEvent(self, event):

        degrees = event.angleDelta() / 8

        if self.pixmapItem.isUnderMouse():

            if degrees.y()/15 > 0:
                self.ui.view.scale(1.25, 1.25)
            else:
                self.ui.view.scale(0.8, 0.8)

    @pyqtSlot(int)
    def colorSlot(self,value):
        val =value/10
        self.ui.colorLcd.blockSignals(True)
        self.ui.colorLcd.setValue(val)
        self.ui.colorLcd.blockSignals(False)
        color = self.ui.colorSlider.value()/10
        #self.enhanceImage(None, None,color,None)
        self.enhanceImage()

    @pyqtSlot(int)
    def sharpnessSlot(self,value):
        val =value/10
        self.ui.sharpnessLcd.blockSignals(True)
        self.ui.sharpnessLcd.setValue(val)
        self.ui.sharpnessLcd.blockSignals(False)
        sharp = self.ui.sharpnessSlider.value()/10
        #self.enhanceImage(None, None,None,sharp)
        self.enhanceImage()

    @pyqtSlot(float)
    def setSharpnessSlider(self,val):
        value = val*10
        self.ui.sharpnessSlider.blockSignals(True)
        self.ui.sharpnessSlider.setValue(int(value))
        self.ui.sharpnessSlider.blockSignals(False)

    @pyqtSlot(float)
    def setColorSlider(self,val):
        value = val*10
        self.ui.colorSlider.blockSignals(True)
        self.ui.colorSlider.setValue(int(value))
        self.ui.colorSlider.blockSignals(False)

    @pyqtSlot(int)
    def brigthnesSlot(self,int):
        
        val =int/10
        self.ui.brigthnessLcd.blockSignals(True)
        self.ui.brigthnessLcd.setValue(val)
        self.ui.brigthnessLcd.blockSignals(False)
        contrast = self.ui.contrastSlider.value()/10
        #self.enhanceImage(None,contrast,None,None)
        self.enhanceImage()
    
    @pyqtSlot(int)
    def contrastSlot(self,int):
        val =int/10
        self.ui.contrastLcd.blockSignals(True)
        self.ui.contrastLcd.setValue(val)
        self.ui.contrastLcd.blockSignals(False)
        bright = self.ui.brigthnesSlider.value()/10
        #self.enhanceImage(bright,None,None,None)
        self.enhanceImage()

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

    def enhanceImage(self):
        cont = self.ui.contrastSlider.value()/10
        sharp = self.ui.sharpnessSlider.value()/10
        bright = self.ui.brigthnesSlider.value()/10
        color = self.ui.colorSlider.value()/10

        pilImg = self.pilBufferImg

        brightness = ImageEnhance.Brightness(pilImg)
        pilImg = brightness.enhance(bright)
        contrast = ImageEnhance.Contrast(pilImg)
        pilImg = contrast.enhance(cont)
        colour = ImageEnhance.Color(pilImg)
        pilImg = colour.enhance(color)
        sharpness = ImageEnhance.Sharpness(pilImg)
        pilImg = sharpness.enhance(sharp)

        self.pixmapItem.setPixmap(self.pixmap.fromImage(ImageQt.ImageQt(pilImg.convert('RGBA'))))
    

        
    def setBufferImage(self):
        img = self.pixmapItem.pixmap()
        self.buffer.open(QBuffer.ReadWrite)
        img.save(self.buffer,"PNG")
        self.pilBufferImg = Image.open(io.BytesIO(self.buffer.data()))
        self.buffer.close()
