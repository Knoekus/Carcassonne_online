# import COproperties

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
  def __init__(self, height=20, scale=1):
    super().__init__()
    self.setMinimumWidth(1)
    self.setFixedHeight(height)
    self.setFrameShape(QtW.QFrame.HLine)
    self.setFrameShadow(QtW.QFrame.Sunken)
    # self.setSizePolicy(QtW.QSizePolicy.Preferred, QtW.QSizePolicy.Minimum)
    # policy = QtW.QSizePolicy.setHorizontalStretch(self, 0.8)
    return

class QVSeparationLine(QtW.QFrame):
  '''
  a vertical separation line\n
  '''
  def __init__(self, width=20, scale=1):
    super().__init__()
    self.setFixedWidth(width)
    self.setMinimumHeight(1)
    self.setFrameShape(QtW.QFrame.VLine)
    self.setFrameShadow(QtW.QFrame.Sunken)
    self.setSizePolicy(QtW.QSizePolicy.Minimum, QtW.QSizePolicy.Preferred)
    return