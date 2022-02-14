from PyQt5.QtWidgets import QWidget, QRubberBand, QHBoxLayout, QVBoxLayout, QSizeGrip, QSplitter
from PyQt5.QtCore import *
from PyQt5.QtGui import QPainter, QBrush, QColor, QPalette, QIcon
##
# https://stackoverflow.com/questions/55307811/select-region-from-an-image-but-resizable-qrubberband-doesnt-resize
##
'''
NOTE: make sure that in QGraphicsView dragmode is RubberBandDrag!
'''
class HSizeGrip(QSizeGrip):
    def __init__(self, parent=None):
        super(HSizeGrip, self).__init__(parent)
        self.setMinimumSize(5,5)
        self.setStyleSheet("background-color: grey;")

    def enterEvent(self, event):
        self.setCursor(Qt.SizeVerCursor)
        super(HSizeGrip,self).enterEvent(event)

class VSizeGrip(QSizeGrip):
    def __init__(self, parent=None):
        super(VSizeGrip, self).__init__(parent)
        self.setMinimumSize(5,5)
        self.setStyleSheet("background-color: grey;")

    def enterEvent(self, event):
        self.setCursor(Qt.SizeHorCursor)
        super(VSizeGrip,self).enterEvent(event)



class RubberBand(QWidget):
    def __init__(self, parent=None):
        super().__init__(parent)

        self.draggable = True
        self.dragging_threshold = 5
        self.mousePressPos = None
        self.mouseMovePos = None

        self.parent = parent

        self.setWindowFlags(Qt.SubWindow)
        layout = QVBoxLayout()
        layout.setContentsMargins(0, 0, 0, 0)


        top = QHBoxLayout()
        top.setContentsMargins(0, 0, 0, 0)
        top.addWidget( QSizeGrip(self), 0, Qt.AlignLeft | Qt.AlignTop)
        top.addWidget( HSizeGrip(self), 0, Qt.AlignHCenter | Qt.AlignTop)
        top.addWidget( QSizeGrip(self), 0, Qt.AlignRight | Qt.AlignTop)
        layout.addLayout(top)

        center = QHBoxLayout()
        center.setContentsMargins(0, 0, 0, 0)
        center.addWidget( VSizeGrip(self), 0, Qt.AlignLeft | Qt.AlignVCenter)
        center.addWidget( VSizeGrip(self), 0, Qt.AlignRight | Qt.AlignVCenter)
        layout.addLayout(center)

        bottom = QHBoxLayout()
        bottom.setContentsMargins(0, 0, 0, 0)
        bottom.addWidget( QSizeGrip(self), 0, Qt.AlignLeft | Qt.AlignBottom)
        bottom.addWidget( HSizeGrip(self), 0, Qt.AlignHCenter | Qt.AlignBottom)
        bottom.addWidget( QSizeGrip(self), 0, Qt.AlignRight | Qt.AlignBottom)
        layout.addLayout(bottom)

        self.setLayout(layout)

        self.rubberband = QRubberBand(QRubberBand.Rectangle, self)
        #self.rubberband.show()

        #self.show()

    cropSignal = pyqtSignal()
    sizeSignal = pyqtSignal(QRect)


    def resizeEvent(self, event):
        self.rubberband.resize(self.size())
        #super(RubberBand, self).resizeEvent(event)


    def paintEvent(self, event):
        ## Get current window size
        window_size = self.size()
        qp = QPainter()
        bg = QColor(170,210,235,100)
        qp.begin(self)
        ## background
        qp.setBrush(bg)
        ## border lines
        qp.setPen(QColor(70,130,255,70))

        qp.setRenderHint(QPainter.Antialiasing, True)

        qp.drawRect(0, 0, window_size.width(), window_size.height())
        qp.end()

    def mousePressEvent(self, event):

        if self.draggable and self.underMouse():
            self.mousePressPos = event.globalPos()                # global
            self.mouseMovePos = event.globalPos() - self.pos()    # local


    def mouseDoubleClickEvent(self, event):
        self.cropSignal.emit()



    def mouseMoveEvent(self, event):

        if self.draggable and self.underMouse():
            globalPos = event.globalPos()
            moved = globalPos - self.mousePressPos
            if moved.manhattanLength() > self.dragging_threshold:
                # Move when user drag window more than dragging_threshold
                diff = globalPos - self.mouseMovePos
                self.move(diff)
                self.mouseMovePos = globalPos - self.pos()


    def mouseReleaseEvent(self, event):
        if self.mousePressPos is not None:
            if event.button() == Qt.RightButton:
                moved = event.globalPos() - self.mousePressPos
                if moved.manhattanLength() > self.dragging_threshold:
                    # Do not call click event or so on
                    event.ignore()
                self.mousePressPos = None

    def resizeEvent(self,event):
        #print('rubber geo : ',self.geometry())
        self.sizeSignal.emit(self.geometry())

    def moveEvent(self, event):
        self.sizeSignal.emit(self.geometry())

