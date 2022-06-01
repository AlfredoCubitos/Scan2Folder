# This Python file uses the following encoding: utf-8
import sys, io
from PyQt5.QtWidgets import QWidget, QGraphicsScene, QGraphicsPixmapItem, QGraphicsView
from PyQt5 import uic
from PyQt5.QtGui import QPixmap, QImage
from PyQt5.QtCore import QObject, pyqtSignal, pyqtSlot, QBuffer, Qt, QPoint, QRect, QPointF, QVariant, QMimeData, QSize
from PIL import ImageEnhance, Image, ImageQt
import numpy as np
import cv2

from rubberband import RubberBand

#from ui_configform import Ui_Form
class GraphicsScene(QGraphicsScene):
    def __init__(self, parent=None):
        super(GraphicsScene, self).__init__(parent)

        self.parent = parent

        self.origin = QPoint()
        self.region = QRect()


    def mousePressEvent(self, event):

        if self.parent.rubberBand.isVisible():
            self.parent.rubberBand.hide()

    def mouseReleaseEvent(self, event):

        if event.button() == Qt.LeftButton:
           # self.rubberBand.hide()
            self.region = QRect(self.origin, event.screenPos()).normalized()

    def mouseMoveEvent(self, event):
        #print('mouse move')
        if not event.buttons() == Qt.LeftButton:
            return


    def dragEnterEvent(self,event):
        #print(event.mimeData().text())
        typ = event.mimeData().text().split('.').pop().lower()
        if typ in self.parent.imageTypes:
            event.acceptProposedAction()

    ## needed to get drop events from outside!
    def dragMoveEvent(self,event):
        event.acceptProposedAction()

    def dropEvent(self, event):
        typ = event.mimeData().text().split('.').pop().lower()
        if typ in self.parent.imageTypes:
            event.accept()
            imgpath = event.mimeData().text().lstrip("file:")
            pix = QPixmap(imgpath)
            #self.parent.pixmapItem.setPixmap(pix.scaled(int(pix.width()*0.5),int(pix.height()*0.5),Qt.KeepAspectRatio))
            self.parent.pixmapItem.setPixmap(pix)
            self.parent.ui.view.fitInView(self.parent.pixmapItem,Qt.KeepAspectRatio)
            img = Image.open(imgpath)
            #self.parent.pilBufferImg = img.resize((int(img.width*0.5),int(img.height*0.5)))
            self.parent.pilBufferImg = img
            print()
            rect = self.parent.ui.view.mapFromScene(0.0,0.0, float(img.size[0]),float(img.size[1])).boundingRect()
            self.parent.rubberBand.setMaximumSize(QSize(rect.width(),rect.height()))
            self.parent.enhanceImage()



class ConfigWindow(QWidget):
    def __init__(self,parent=None):
        super().__init__()
        self.ui = uic.loadUi("configform.ui", self)
        #self.ui = Ui_Form()
        #self.ui.setupUi(self)

        self.parent = parent

        self.ui.brigthnesSlider.valueChanged.connect(self.brigthnesSlot)
        self.ui.contrastSlider.valueChanged.connect(self.contrastSlot)

        self.ui.brigthnessLcd.valueChanged.connect(self.setBrightSlider)
        self.ui.contrastLcd.valueChanged.connect(self.setContastSlider)

        self.ui.colorSlider.valueChanged.connect(self.colorSlot)
        self.ui.sharpnessSlider.valueChanged.connect(self.sharpnessSlot)

        self.ui.colorLcd.valueChanged.connect(self.setColorSlider)
        self.ui.sharpnessLcd.valueChanged.connect(self.setSharpnessSlider)
        self.ui.checkCrop.stateChanged.connect(self.setCrop)


        self.rubberBand = RubberBand(self.ui.view)
        #self.rubberBand.setMaximumSize(QSize(397,552))
        self.ui.view.setRubberBandSelectionMode(Qt.IntersectsItemBoundingRect)
        self.ui.view.rubberBandChanged.connect(self.getCropRect)
        self.rubberBand.cropSignal.connect(self.crop)
        self.rubberBand.sizeSignal.connect(self.setSize)
        self.rubberBand.hide()

        self.scene = GraphicsScene(self)
        self.pixmap = QPixmap()
        self.pixmapItem = QGraphicsPixmapItem()
        self.scene.addItem(self.pixmapItem)
        self.ui.view.setScene(self.scene)
        #self.ui.view.fitInView(self.pixmapItem,Qt.KeepAspectRatio)
        #self.pixmap.load("Calibrate_Test_1.png")
        #self.buffer = QBuffer()
        self.pilBufferPath = "/tmp/scan2foldertempimg.png"
        self.pilBufferImg = Image.new('RGBA',(1,1))


        self.bright = self.ui.brigthnesSlider.maximum()/2
        self.contast = self.ui.contrastSlider.maximum()/2

        self.imageTypes = ['png','jpg','tiff','tif']




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
        self.ui.sharpnessSlider.valueChanged.emit(int(value))

    @pyqtSlot(float)
    def setColorSlider(self,val):
        value = val*10
        self.ui.colorSlider.blockSignals(True)
        self.ui.colorSlider.setValue(int(value))
        self.ui.colorSlider.blockSignals(False)
        self.ui.colorSlider.valueChanged.emit(int(value))

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
        self.ui.brigthnesSlider.valueChanged.emit(int(value))
    
    @pyqtSlot(float)
    def setContastSlider(self,val):
        value = val*10
        self.ui.contrastSlider.blockSignals(True)
        self.ui.contrastSlider.setValue(int(value))
        self.ui.contrastSlider.blockSignals(False)
        self.ui.contrastSlider.valueChanged.emit(int(value))

    @pyqtSlot(QRect, QPointF, QPointF)
    def getCropRect(self, rect, start, end):
        pass
        if self.ui.checkCrop.isChecked():
            self.rubberBand.show()
        srect = self.ui.view.mapToScene(rect).boundingRect().toRect()
        #print(srect)
        if rect.isEmpty():

            self.rubberBand.show()
        else:
            self.rubberBand.setGeometry(rect)

    @pyqtSlot()
    def crop(self):
        pass
        self.parent.cropSize["left"]   = self.ui.cropX.value()
        self.parent.cropSize["top"]    = self.ui.cropY.value()
        self.parent.cropSize["width"]  = self.ui.cropW.value()
        self.parent.cropSize["height"] = self.ui.cropH.value()
        self.rubberBand.hide()


    @pyqtSlot()
    def setCrop(self):
        pass
        ## ensure that RubberBandDrag dragmode is set
        ## if not rubberBand will not work correctly
        self.ui.view.setDragMode( QGraphicsView.RubberBandDrag)

    @pyqtSlot(QRect)
    def setSize(self,rect):
        ## this the offset to subtract from srect
        offset = 13
        srect = self.ui.view.mapToScene(rect).boundingRect().toRect()
        self.ui.cropX.setValue(srect.x()-offset)
        self.ui.cropY.setValue(srect.y()-offset)
        self.ui.cropH.setValue(srect.height()+-(offset*2))
        self.ui.cropW.setValue(srect.width()-(offset*2))
        pass


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
        #self.buffer.open(QBuffer.ReadWrite)
        #img.save(self.buffer,"PNG")
        img.save(self.pilBufferPath,"PNG")
        self.pilBufferImg = Image.open(self.pilBufferPath)
        #self.buffer.close()

    def wheelEvent(self, event):
        point = event.position()
        degrees = event.angleDelta() / 8

        self.pixmapItemScale = self.pixmapItem.scale()

        if self.pixmapItem.isUnderMouse():

            if degrees.y()/15 > 0:
                #self.ui.view.scale(1.25, 1.25)
                self.pixmapItem.setScale(self.pixmapItemScale+0.01)
            else:
                #self.ui.view.scale(0.8, 0.8)
                if self.pixmapItemScale > 0.15:
                    self.pixmapItem.setScale(self.pixmapItemScale-0.01)

    def closeEvent(self, event):
        self.scene.clear()
        event.accept()
