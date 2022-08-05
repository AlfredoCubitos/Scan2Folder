#!/usr/bin/python3
# This Python file uses the following encoding: utf-8

from PyQt5.QtWidgets import QApplication, QMainWindow, QPushButton, QComboBox, QDialog, QFileDialog, QMessageBox, QCompleter, QProgressDialog, QProgressBar
from PyQt5 import uic
from PyQt5.QtCore import QProcess, QSettings, QThreadPool, pyqtSignal, pyqtSlot, Qt
from PyQt5.QtGui import QPixmap, QImage

import sys
import time
import sane
from urllib.request import urlopen
import bs4
import glob
import os, io
from PIL import ImageEnhance
import ocrtools as ocrt
import tempfile


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
        self.scanFolder = os.getcwd()
        self.ver = sane.init()
        
        self.ui = uic.loadUi("mainwindow.ui", self)
        #self.ui = Ui_MainWindow()
        #self.ui.setupUi(self)
        
        self.dialog = QDialog()
        self.message = QMessageBox()
        
        self.threadpool = QThreadPool()

        self.settings = QSettings("bibuweb.de","Scan2Folder")

        self.progressBar = None

        #self.configWin = ConfigWindow(self)
        #self.configWin.ui.scanButton.clicked.connect(self.configScan)
        

                
        self.ui.resolutions.addItems(self.resolution)
        self.ui.resolutions.setCurrentIndex(self.ui.resolutions.findText('300'))

        self.ui.btnOpenDir.clicked.connect(self.openDir)
        self.ui.btnStartscan.clicked.connect(self.startScanJob)
        self.ui.btnOcr.clicked.connect(self.ocr_startProcess)

        self.ui.actionCalibrate.triggered.connect(self.configureWindow)
        #self.configWin.ui.saveButton.clicked.connect(self.saveConfig)


        # Change Color back after error
        self.ui.filename.cursorPositionChanged.connect(self.leditcolor)

        self.ui.scanpath.cursorPositionChanged.connect(self.leditcolor)
        self.ui.scanpath.textChanged.connect(self.scanPathCanged)

        self.is_dev = True
        self.dev_available = False
        self.dev_connected = False
        self.adf = False
        self.dev = None
        self.devices = []
        self.scanStatus = False
        self.btnStyle = ""

        self.contrast = 1
        self.brightness = 1
        self.color = 1
        self.sharpness = 1
        self.gamma = 1
        self.scanPath = ""
        self.ocr = False
        self.crop = False
        self.cropSize = {'left':1,'top':1,'width':1,'height':1}
        self.ocrFiles = []
        self.tempocr = None
        self.configWin = None


        if self.settings.contains("ocr"):
            if self.settings.value('ocr') == 'true':
                self.ocr = True
                self.ui.actionEnable_OCR.setChecked(True)
            else:
                self.ui.actionEnable_OCR.setChecked(False)
            ## connect Signal here and not before loading settings
            ## if not, you never will get the stored value because QAction is triggered when ever the value changed

        if self.settings.contains('crop'):
            if self.settings.value('crop') == 'true':
                self.crop = True

        if self.settings.contains('cropSize'):
            #print(self.settings.value('cropSize'))
            self.cropSize = self.settings.value('cropSize')


        if self.settings.contains("path"):
            self.ui.scanpath.setText(self.settings.value("path"))
            self.scanPath = self.settings.value("path")
            self.createCompleter()
        
        if self.settings.contains('contrast'):
            self.brightness = self.settings.value('brightness')
            
            self.contrast = self.settings.value('contrast')

        if self.settings.contains('color'):
            self.color = self.settings.value('color')

        if self.settings.contains("sharpness"):
            self.sharpness = self.settings.value('sharpness')

        if self.settings.contains("gamma"):
            self.gamma = self.settings.value('gamma')


    def setConfigWinSettings(self):

        if self.settings.contains("ocr"):
            if self.settings.value('ocr') == 'true':
                self.configWin.ui.OCR_Enabled.setChecked(True)
                self.configWin.ui.OCR_Box.setEnabled(True)

            else:
                self.configWin.ui.OCR_Enabled.setChecked(False)
                self.configWin.ui.OCR_Box.setEnabled(False)
            ## connect Signal here and not before loading settings
            ## if not, you never will get the stored value because QAction is triggered when ever the value changed
            self.configWin.ui.OCR_Enabled.stateChanged.connect(self.ocrConfig)

        if self.settings.contains('crop'):
            self.configWin.ui.checkCrop.setChecked(self.crop)

        if self.settings.contains('cropSize'):
            self.configWin.ui.cropX.setValue(self.cropSize['left'])
            self.configWin.ui.cropY.setValue(self.cropSize['top'])
            self.configWin.ui.cropW.setValue(self.cropSize['width'])
            self.configWin.ui.cropH.setValue(self.cropSize['height'])

        if self.settings.contains('contrast'):
            self.configWin.ui.brigthnessLcd.setValue(float(self.brightness))
            self.configWin.ui.brigthnesSlider.setValue(int(float(self.brightness)*10))
            self.configWin.ui.contrastLcd.setValue(float(self.contrast))
            self.configWin.ui.contrastSlider.setValue(int(float(self.contrast)*10))

        if self.settings.contains('color'):
            self.configWin.ui.colorLcd.setValue(float(self.color))
            self.configWin.ui.colorSlider.setValue(int(float(self.color)*10))

        if self.settings.contains("sharpness"):
            self.configWin.ui.sharpnessLcd.setValue(float(self.sharpness))
            self.configWin.ui.sharpnessSlider.setValue(int(float(self.sharpness)*10))

        if self.settings.contains("gamma"):
            self.configWin.ui.gammaLcd.setValue(float(self.gamma))
            self.configWin.ui.gammaSlider.setValue(int(float(self.gamma)*10))

    def closeEvent(self, event):
        #if not set, process keeps running in background
        self.scanStatus = False


    def openDir(self):
        fileDlg = QFileDialog()
        self.scanFolder = fileDlg.getExistingDirectory(self,'Scan Folder',self.scanFolder, QFileDialog.DontUseNativeDialog)
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


    @pyqtSlot(str)
    def scanPathCanged(self,path):
        self.scanPath = path
        self.createCompleter()

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
        count = 0
        while  self.is_dev:

            try:
                #ToDo: check index from
                
                self.dev = sane.open(self.devices[0][0])
                
               
            except:
                print("no scanner connected, waiting...",self.dev)
            if self.dev is not None:
                self.is_dev = False
                self.dev_connected = True
                print("scanner connected")
            time.sleep(3)
            ## Stop process after 3 times to avoid endless loop if no device is available
            ## due started as thread
            count += 1
            if count > 2:
                self.is_dev = False
                self.statusBar().showMessage("No Scanner connected!")
    
    def commonThreadEnd(self):
        print("Thread ended")
    
    def scanDocThreadEnded(self):
        self.statusBar().showMessage("Job stopped")
        self.scanStatus = False
        self.setLedStatus()
    
    def scannerCheckThreadEnd(self):
        print("Lookup Thread ended")

        if self.dev_connected:
            self.startThread(self.scanDocuments,None,self.scanDocThreadEnded)

    def setScannerStatus(self):
        if self.dev_connected:
            self.setLedStatus()
            self.statusBar().showMessage("Scanner connected",10)
            self.setScanButton("running")
        else:
            self.setScanButton('stopped')

    
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
                            if self.ocr:
                                self.ocrFiles.append(savePath+img)
                        except:
                            self.adf=False
                            break
                else:
                    self.adf=False
                    imgNr = imgNr+1
                    img = imgPrefix+str(imgNr)+".png"
                    self.dev.start()
                    im = self.dev.snap()
                    self.enhanceImage(im,savePath,img)
                    if self.ocr:
                        self.ocrFiles.append(savePath+img)
            time.sleep(3)

    def enhanceImage(self,image,path,pf):
        brightness = ImageEnhance.Brightness(image)
        image = brightness.enhance(float(self.brightness))
        contrast = ImageEnhance.Contrast(image)
        image = contrast.enhance(float(self.contrast))
        colour = ImageEnhance.Color(image)
        image = colour.enhance(float(self.color))
        sharpness = ImageEnhance.Sharpness(image)
        image = sharpness.enhance(float(self.sharpness))

        print("Gamma: ", self.gamma)
        gamma = float(self.gamma)
        image = image.point(self.gamma_table( gamma, gamma, gamma))

        print("image saved ",self.ui.scanpath.text()+"/"+pf)
        image.save(path+pf)

    @pyqtSlot()
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

            if self.ocr and len(self.ocrFiles) > 0:
                self.ui.btnOcr.setEnabled(True)
                self.tempocr =  tempfile.NamedTemporaryFile(delete=False)
                for f in self.ocrFiles:
                    self.tempocr.write(str(f+"\n").encode())
                self.tempocr.close()
    
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

        self.configWin = ConfigWindow(self)
        self.configWin.ui.scanButton.clicked.connect(self.configScan)
        self.configWin.ui.saveButton.clicked.connect(self.saveConfig)
        self.setConfigWinSettings()

        if self.dev is not None:
            self.configWin.ui.scanButton.setEnabled(True)
            self.configWin.ui.scanButton.setText("Start Scan")
        else:
            self.configWin.ui.scanButton.setEnabled(False)
            self.configWin.ui.scanButton.setText("Sart Scan Service first")
        
        self.configWin.show()

    def ocr_startProcess(self):
        self.progressDlg = QProgressDialog(self)
        self.progressDlg.setWindowTitle("OCR Process")
        self.progressDlg.setLabelText("OCR Process in Progress ...")
        self.progressDlg.setAutoClose(False)
        self.progressDlg.setAutoReset(False)
        self.progressDlg.setModal(True)
        self.startThread(self.ocr_process,None,self.ocr_stopped)

    def gamma_table(self, gamma_r, gamma_g, gamma_b, gain_r=1.0, gain_g=1.0, gain_b=1.0):
        r_tbl = [min(255, int((x / 255.) ** (1. / gamma_r) * gain_r * 255.)) for x in range(256)]
        g_tbl = [min(255, int((x / 255.) ** (1. / gamma_g) * gain_g * 255.)) for x in range(256)]
        b_tbl = [min(255, int((x / 255.) ** (1. / gamma_b) * gain_b * 255.)) for x in range(256)]

        return r_tbl + g_tbl + b_tbl

    def ocr_process(self):

        if len(self.ocrFiles) > 0:

            val = 0
            ### add one more for pdf create process
            max = len(self.ocrFiles) + 1
            self.progressDlg.setRange(0,max)

            for f in self.ocrFiles:
                val += 1

                self.progressDlg.setValue(val)

                #TODO: if is checked
                ocrt.deskew(f)
                #TODO: if is checked
                #NOTE: this is crop and resize in one step
                #      size and dpi are predifined to A4 300
                print(self.cropSize)
                if self.cropSize['width'] > 1:
                    ocrt.crop_resize(f,self.cropSize["left"],self.cropSize["top"], self.cropSize["width"],self.cropSize["height"])
                #TODO: if is checked
                ocrt.check_orientation(f)



            print(self.tempocr.name)
            ## works in python 3.9+
            #pdfname = self.ocrFiles[0].removesuffix("_1.png")
            pdfname, suff = self.ocrFiles[0].rsplit("_1.png")
            # print(pdfname)
            ### this runs in its own process
            self.progressDlg.setLabelText("OCR Process finishing ...")
            ocrt.create_pdf(self.tempocr.name, pdfname)
            ####
            ## Workaround to get a correct finished process
            ## while pytesseract uses subprocces which can not be handled in this thread
            ####
            while not os.path.isfile(pdfname+".pdf"):
                time.sleep(3)
            self.progressDlg.setValue(val+1)
            os.unlink(self.tempocr.name)
            self.ocrFiles.clear()
        else:
            return

    def ocr_stopped(self):
        print("OCR finished")
        self.progressDlg.close()
    
    def configScan(self):
        pixmap = QPixmap()
        self.dev.resolution=int(self.ui.resolutions.currentText())
        self.dev.mode=self.checkScanMode()
        self.dev.start()
        im = self.dev.snap()

        convertImg = io.BytesIO()
        im.save(convertImg,"BMP")
        pixmap.loadFromData(convertImg.getvalue(), "BMP")
        self.configWin.pixmapItem.setPixmap(pixmap)


        #self.configWin.pixmapItem.setPixmap(QPixmap.fromImage(pix))
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
        self.gamma          = self.configWin.ui.gammaLcd.value()
        self.crop           = self.configWin.ui.checkCrop.isChecked()

        self.settings.setValue('brightness',self.brightness)
        self.settings.setValue('contrast',self.contrast)
        self.settings.setValue('color',self.color)
        self.settings.setValue('sharpness',self.sharpness)
        self.settings.setValue('gamma',self.gamma)
        self.settings.setValue('ocr', self.ocr)
        self.settings.setValue('crop', self.crop)
        self.settings.setValue('cropSize',self.cropSize)
        self.settings.sync()
        self.configWin.close()

    @pyqtSlot(int)
    def ocrConfig(self,state):
        if state == Qt.Checked:
            self.ocr = True
            self.configWin.ui.OCR_Box.setEnabled(True)
        else:
            self.ocr = False
            self.configWin.ui.OCR_Box.setEnabled(False)


    def closeEvent(self,e):
        if self.tempocr is not None:
            if os.path.exists(self.tempocr.name):
                os.unlink(self.tempocr.name)
        if self.configWin is not None:
            if self.configWin.isVisible():
                self.configWin.close()


        e.accept()
def main():

    app = QApplication(sys.argv)
    window = MainWindow()
    window.scanners()
    
    #window.show()
    
    sys.exit(app.exec())


if __name__ == '__main__':
    main()
