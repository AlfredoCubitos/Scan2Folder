#!/usr/bin/python3
# This Python file uses the following encoding: utf-8

from PyQt5.QtWidgets import QApplication, QMainWindow, QPushButton, QComboBox, QDialog, QFileDialog, QMessageBox, QCompleter
from PyQt5 import uic
from PyQt5.QtCore import QProcess, QSettings, QThreadPool, pyqtSignal, pyqtSlot, Qt
from PyQt5.QtGui import QPixmap, QImage

import sys
import time
import sane
from urllib.request import urlopen
import bs4
import glob
import os
from PIL import ImageEnhance, ImageQt

from ui_dialog import Ui_Dialog
from multithread import Worker, WorkerSignals
from imagecalibrate import ConfigWindow

#from ui_mainwindow import Ui_MainWindow
import resources



try:
    os.chdir(sys._MEIPASS)
    print(sys._MEIPASS)
except:
    pass

XML_PATH = '/hp/device/notifications.xml'


class MainWindow(QMainWindow):

    def __init__(self):
        super().__init__()

        
        self.mode = ['lineart','gray','color']
        self.resolution = ['75','100','150','200','300','600','1200']
        self.compression = ['None','JPEG']
        self.scanFolder = "/tmp/"
        self.ver = sane.init()
        
        self.ui = uic.loadUi("mainwindow.ui", self)
        #self.ui = Ui_MainWindow()
        #self.ui.setupUi(self)
        
        self.dialog = QDialog()
        self.message = QMessageBox()
        
        self.threadpool = QThreadPool()

        self.settings = QSettings("bibuweb.de","Scan2Folder")


        self.configWin = ConfigWindow()
        self.configWin.ui.scanButton.clicked.connect(self.configScan)
        

                
        self.ui.resolutions.addItems(self.resolution)
        self.ui.resolutions.setCurrentIndex(self.ui.resolutions.findText('300'))

        self.ui.btnOpenDir.clicked.connect(self.openDir)
        self.ui.btnStartscan.clicked.connect(self.startScanJob)
        self.ui.actionCalibrate.triggered.connect(self.configureWindow)
        self.configWin.ui.saveButton.clicked.connect(self.saveConfig)
        # Change Color back after error
        self.ui.filename.cursorPositionChanged.connect(self.leditcolor)

        self.ui.scanpath.cursorPositionChanged.connect(self.leditcolor)

        self.is_dev = True
        self.dev_available = False
        self.adf = False
        self.dev = None
        self.devices = []
        self.scanStatus = False
        self.btnStyle = ""

        self.contrast = 1
        self.brightness = 1
        self.color = 1
        self.sharpness = 1
        self.scanPath = ""

        

        if self.settings.contains("path"):
            self.ui.scanpath.setText(self.settings.value("path"))
            self.scanPath = self.settings.value("path")
            self.createCompleter()
        
        if self.settings.contains('contrast'):
            self.brightness = self.settings.value('brightness')
            
            self.contrast = self.settings.value('contrast')
            self.configWin.ui.brigthnessLcd.setValue(float(self.brightness))
            self.configWin.ui.brigthnesSlider.setValue(int(float(self.brightness)*10))
            self.configWin.ui.contrastLcd.setValue(float(self.contrast))
            self.configWin.ui.contrastSlider.setValue(int(float(self.contrast)*10))

    def closeEvent(self, event):
        #if not set, process keeps running in background
        self.scanStatus = False


    def openDir(self):
        fileDlg = QFileDialog()
        self.scanFolder = fileDlg.getExistingDirectory(self,'Scan Folder')
        self.ui.scanpath.setText(self.scanFolder)
        self.settings.setValue("path",self.scanFolder)
        self.settings.sync()
        


    def startThread(self, fn, resultFn=None, complete=None):
        worker = Worker(fn) # Any other args, kwargs are passed to the run function
        if resultFn is not None:
            worker.signals.result.connect(resultFn)
        if complete is not None:
            worker.signals.finished.connect(complete)
        #worker.signals.progress.connect(self.scannerProgress)
        self.threadpool.start(worker)
        

    
    def thread_complete(self):
        self.scannerProgress(100)
        time.sleep(1)
        self.dialog.close()
        
        if self.dev_available:
            self.show()
        else:
            #TODO: put error dlg here
            self.message.setText("No scanner found\n Check your Configuration!")
            self.message.exec()
            print("Error: No Devices found")
            
     
        print("THREAD COMPLETE! ", self.threadpool.activeThreadCount())

    def createCompleter(self):
        ff = glob.glob(self.scanPath+"/*.pdf")
        files = []
        for f in ff:
            files.append(os.path.basename(f).split('.')[0])
        completer = QCompleter(files)
        completer.setCaseSensitivity(Qt.CaseInsensitive)
        self.ui.filename.setCompleter(completer)


    def scannerLookup(self):

        #self.dialog.setModal(True)

        self.uidlg = Ui_Dialog()
        self.uidlg.setupUi(self.dialog)
    
        self.dialog.show()
    
    def checkScanMode(self):
        mode = ""
        if self.ui.btnBuW.isChecked():
            mode = self.ui.btnBuW.text()
        elif self.ui.btnGray.isChecked():
            mode = self.ui.btnGray.text()
        elif self.ui.btnColor.isChecked():
            mode = self.ui.btnColor.text()
        print(mode)
        return mode
    
    
    
    def scannerAddToDlg(self,result):
        self.devices = result
        if len(self.devices) > 0:
            self.dev_available = True
            for i, dev in enumerate(result):
                self.ui.comboBox.addItem(dev[i])
        else:
            return


    def scannerProgress(self,val):
        self.uidlg.progressBar.setValue(val)
        
       
    def scanners(self):
        self.scannerLookup()
        self.startThread(sane.get_devices,self.scannerAddToDlg, self.thread_complete)

    def scannerCheck(self):
        self.statusBar().showMessage("looking up for scanner ....")
        print(self.devices[0])
        
        while  self.is_dev:
    
            try:
                #ToDo: check index from
                
                self.dev = sane.open(self.devices[0][0])
                
               
            except:
                print("no scanner connected, waiting...",self.dev)
            if self.dev is not None:
                self.is_dev = False
                print("scanner connected")
            time.sleep(3)
    
    def commonThreadEnd(self):
        print("Thread ended")
    
    def scanDocThreadEnded(self):
        self.statusBar().showMessage("Job stopped")
        self.scanStatus = False
        self.setLedStatus()
    
    def scannerCheckThreadEnd(self):
        print("Lookup Thread ended")
        self.startThread(self.scanDocuments,None,self.scanDocThreadEnded)

    def setScannerStatus(self):
        self.setLedStatus()
        self.statusBar().showMessage("Scanner connected",10)
        self.setScanButton("running")
    
    def setLedStatus(self):
        if self.scanStatus:
            pix = QPixmap(":/images/square_green.svg")
        else:
            pix = QPixmap(":/images/square_red.svg")

        self.ui.statusLed.setPixmap(pix)


    def scanDocuments(self):
        ip = self.devices[0][0].split('=')[1]
        print(ip)
        url = 'http://' + ip + XML_PATH
        self.dev.mode = self.checkScanMode()
        self.dev.resolution = int(self.ui.resolutions.currentText())
        imgNr = 0
        savePath = self.ui.scanpath.text()+"/"
        imgPrefix = self.ui.filename.text()+"_"
        #self.dev.contrast = 900
        #self.dev.brightness = self.brightness
        while self.scanStatus:
            btnreq = urlopen(url)
            soup = bs4.BeautifulSoup(str(btnreq.read()),'lxml')
            if soup.startscan.string == str(1):
                #print("Pressed")
                if soup.adfloaded.string == str(1):
                    self.adf=True
                    print("ADF Source")
                    self.dev.source = 'ADF'
                    imIter = self.dev.multi_scan()
                    
                    while self.adf:
                        try: 
                            im = imIter.next()
                            imgNr = imgNr+1
                            img = imgPrefix+str(imgNr)+".png"
                            im.save(savePath+img)
                        except:
                            self.adf=False
                            break
                else:
                    self.adf=False
                    imgNr = imgNr+1
                    img = imgPrefix+str(imgNr)+".png"
                    self.dev.start()
                    im = self.dev.snap()
                    brightness = ImageEnhance.Brightness(im)
                    im = brightness.enhance(float(self.brightness))
                    contrast = ImageEnhance.Contrast(im)
                    im = contrast.enhance(float(self.contrast))
                    print("image saved ",self.ui.scanpath.text()+"/"+img)
                    im.save(savePath+img)
            time.sleep(3)
    # Slot
    def leditcolor(self):
        self.ui.scanpath.setStyleSheet("background-color:rgb(255, 255, 255)")
        self.ui.filename.setStyleSheet("background-color:rgb(255, 255, 255)")

    def startScanJob(self):
        
        # print("Path: ",self.scanpath.text())
        # print("Mode: ",mode)
        # print("Resolution: ", self.resolutions.currentText())
        # print("File: ", self.filename.text())

        if len(self.ui.scanpath.text()) == 0:
            msg = QMessageBox()
            msg.setText("Please enter file path!")
            msg.exec()
            self.ui.scanpath.setStyleSheet("background-color:rgb(255, 170, 127)")
            return
        
        if len(self.ui.filename.text()) == 0:
            msg = QMessageBox()
            msg.setText("Please enter file name prefix!")
            msg.exec()
            self.ui.filename.setStyleSheet("background-color:rgb(255, 170, 127)")
            return



        if not self.scanStatus:
            self.setScanButton("starting")
            self.startThread(self.scannerCheck,self.setScannerStatus, self.scannerCheckThreadEnd)
            self.scanStatus = True
            self.ui.scanpath.setEnabled(False)
            self.ui.filename.setEnabled(False)
        else:
            self.scanStatus = False
            self.setScanButton("stopped")
            self.ui.scanpath.setEnabled(True)
            self.ui.filename.setEnabled(True)
            self.ui.filename.clear()
    
    def setScanButton(self,status):

        if status == "starting":
            self.btnStyle = self.ui.btnStartscan.styleSheet()
            
            self.ui.btnStartscan.setStyleSheet("background-color: yellow")
            self.ui.btnStartscan.setText("Starting...")

        if status == "running":
            self.ui.btnStartscan.setStyleSheet("background-color: red")
            self.ui.btnStartscan.setText("Stop")
            self.statusBar().showMessage("Scan job is running..")
        
        if status == "stopped":
            self.ui.btnStartscan.setText("Sart Scan")
            self.ui.btnStartscan.setStyleSheet(self.btnStyle)
    
    def configureWindow(self):  

        if self.dev is not None:
            self.configWin.ui.scanButton.setEnabled(True)
        else:
            self.configWin.ui.scanButton.setEnabled(False)
        
        self.configWin.show()


    
    def configScan(self):
        self.dev.resolution=150
        self.dev.mode=self.checkScanMode()
        self.dev.start()
        im = self.dev.snap()
        pix = ImageQt.ImageQt(im.convert('RGBA'))
        #self.configWin.im = im
        #self.configWin.ui.view.setPixmap(self.configWin.pixmap.fromImage(pix))
        self.configWin.pixmapItem.setPixmap(self.configWin.pixmap.fromImage(pix))
        self.configWin.ui.view.fitInView(self.configWin.pixmapItem,Qt.KeepAspectRatio)
        self.configWin.pixmapItem.grabMouse()
        self.configWin.setBufferImage()
        self.configWin.enhanceImage()
        #im = None
    
    @pyqtSlot()
    def saveConfig(self):
        self.brightness     = self.configWin.ui.brigthnessLcd.value()
        self.contrast       = self.configWin.ui.contrastLcd.value()
        self.color          = self.configWin.ui.colorLcd.value()
        self.sharpness      = self.configWin.ui.sharpnessLcd.value()

        self.settings.setValue('brightness',self.brightness)
        self.settings.setValue('contrast',self.contrast)
        self.settings.setValue('color',self.color)
        self.settings.setValue('sharpness',self.sharpness)
        self.settings.sync()
        self.configWin.close()


def main():
    app = QApplication(sys.argv)
    window = MainWindow()
    window.scanners()
    
    #window.show()
    
    sys.exit(app.exec())


if __name__ == '__main__':
    main()
