# import prop_s

import PyQt5.QtGui as QtG
import PyQt5.QtWidgets as QtW
import PyQt5.QtCore as QtC

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
    
    self.setFrameShape(QtW.QFrame.HLine)
    # self.setFrameShadow(QtW.QFrame.Sunken)
    self.setFrameShadow(QtW.QFrame.Plain)
    # self.setSizePolicy(QtW.QSizePolicy.Preferred, QtW.QSizePolicy.Minimum)
    # policy = QtW.QSizePolicy.setHorizontalStretch(self, 0.8)
    
    # self.setStyleSheet(f'''QFrame{{
    #                                 border: 5 px;
    #                                 border-color: rgb{colour};
    #                              }}''')
    pal = self.palette()
    pal.setColor(QtG.QPalette.WindowText, QtG.QColor(colour[0], colour[1], colour[2]))
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
    
    self.setFrameShape(QtW.QFrame.VLine)
    # self.setFrameShadow(QtW.QFrame.Sunken)
    self.setFrameShadow(QtW.QFrame.Plain)
    # self.setSizePolicy(QtW.QSizePolicy.Minimum, QtW.QSizePolicy.Preferred)
    
    pal = self.palette()
    pal.setColor(QtG.QPalette.WindowText, QtG.QColor(colour[0], colour[1], colour[2]))
    self.setPalette(pal)
    return

class QImage(QtW.QLabel):
  '''
  an image in a label\n
  '''
  def __init__(self, file, width=None, height=None):
      super().__init__()
      image = QtG.QPixmap(file)
      self.setPixmap(image)
      self.setScaledContents(True)
      if width is not None:
          self.setFixedWidth(width)
      if height is not None:
          self.setFixedHeight(height)
      return