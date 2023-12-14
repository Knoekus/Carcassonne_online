# import prop_s

import PyQt6.QtGui as QtG
import PyQt6.QtWidgets as QtW
import PyQt6.QtCore as QtC

import PIL
from PIL.ImageQt import ImageQt

class ClickableLabel(QtW.QLabel):
    clicked = QtC.pyqtSignal()
    def __init__(self, parent=None):
        super().__init__(parent)
        self.setCursor(QtG.QCursor(QtC.Qt.PointingHandCursor))
    
    def mousePressEvent(self, event):
        self.new_admin = self.text()
        self.clicked.emit()
        
class QHSeparationLine(QtW.QFrame):
    '''
    a horizontal separation line\n
    '''
    def __init__(self, height=20, colour:tuple=(0,0,0)):
        super().__init__()
        self.setMinimumWidth(1)
        self.setFixedHeight(height)
        
        self.setFrameShape(QtW.QFrame.Shape.HLine)
        self.setFrameShadow(QtW.QFrame.Shadow.Plain)
        # self.setSizePolicy(QtW.QSizePolicy.Preferred, QtW.QSizePolicy.Minimum)
        # policy = QtW.QSizePolicy.setHorizontalStretch(self, 0.8)
        
        pal = self.palette()
        pal.setColor(QtG.QPalette.ColorRole.WindowText, QtG.QColor(colour[0], colour[1], colour[2]))
        self.setPalette(pal)
        return

class QVSeparationLine(QtW.QFrame):
    '''
    a vertical separation line\n
    '''
    def __init__(self, width=20, colour:tuple=(0,0,0)):
        super().__init__()
        self.setMinimumHeight(1)
        self.setFixedWidth(width)
        
        self.setFrameShape(QtW.QFrame.Shape.VLine)
        self.setFrameShadow(QtW.QFrame.Shadow.Plain)
        # self.setSizePolicy(QtW.QSizePolicy.Minimum, QtW.QSizePolicy.Preferred)
        
        pal = self.palette()
        pal.setColor(QtG.QPalette.ColorRole.WindowText, QtG.QColor(colour[0], colour[1], colour[2]))
        self.setPalette(pal)
        return

class QImage(QtW.QLabel):
    '''
    an image in a label\n
    '''
    def __init__(self, file, width=None, height=None):
        super().__init__()
        if type(file) == str:
            self.pixmap = QtG.QPixmap(file)
            self.setPixmap(self.pixmap)
        elif type(file) == type(QtG.QPixmap()):
            self.setPixmap(file)
            
        self.setScaledContents(True)
        if width is not None:
            self.setFixedWidth(width)
        if height is not None:
            self.setFixedHeight(height)
      
        #===== Uncomment for help during development =====#
        # self.setStyleSheet("background-color:rgba(255,0,0,100)")
        return
  
class ClickableImage(QImage):
    clicked = QtC.pyqtSignal()
    def __init__(self, file, width=None, height=None, parent=None):
        super().__init__(file, width, height)
        self.setCursor(QtG.QCursor(QtC.Qt.CursorShape.PointingHandCursor))
    
    def mousePressEvent(self, event):
        self.clicked.emit()

def GreenScreenPixmap(file):
    img1 = PIL.Image.open(file)
    pixels1 = img1.load()
    for i in range(img1.size[0]): # for every pixel:
        for j in range(img1.size[1]):
            if pixels1[i,j] == (0, 255, 0, 255): # if full green
                pixels1[i,j] = (0, 0, 0, 0)      # make transparent
    
    img2 = ImageQt(img1).copy()
    pixmap = QtG.QPixmap.fromImage(img2)
    return pixmap