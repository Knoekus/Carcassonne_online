# import prop_s

import PyQt6.QtGui as QtG
import PyQt6.QtWidgets as QtW
import PyQt6.QtCore as QtC
import tile_data

# import sys
# if r"Classes" not in sys.path:
#     sys.path.append(r"..\Classes")
# from Classes.Tiles import Tiles

import PIL
from PIL.ImageQt import ImageQt

class ClickableLabel(QtW.QLabel):
    clicked = QtC.pyqtSignal()
    def __init__(self, parent=None):
        super().__init__(parent)
        self.setCursor(QtG.QCursor(QtC.Qt.CursorShape.PointingHandCursor))
    
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
        self.file = None
        
        self.setScaledContents(True)
        if width is not None:
            self.setFixedWidth(width)
        if height is not None:
            self.setFixedHeight(height)
        
        if file != None:
            self.draw_image(file)
        
        #===== Uncomment for help during development =====#
        # self.setStyleSheet("background-color:rgba(255,0,0,100)")
        return
    
    def draw_image(self, file):
        if type(file) == str:
            self.file = file
            self.pixmap = QtG.QPixmap(file)
            self.setPixmap(self.pixmap)
        elif type(file) == type(QtG.QPixmap()):
            # self.file = None
            self.setPixmap(file)
        elif file == None:
            # self.file = None
            self.setPixmap(QtG.QPixmap())
  
class ClickableImage(QImage):
    clicked = QtC.pyqtSignal()
    clicked_l = QtC.pyqtSignal()
    clicked_r = QtC.pyqtSignal()
    def __init__(self, file, width=None, height=None):
        super().__init__(file, width, height)
        self.clickable = False
    
    def disable(self):
        self.setCursor(QtG.QCursor(QtC.Qt.CursorShape.ArrowCursor))
        self.clickable = False
    
    def enable(self):
        self.setCursor(QtG.QCursor(QtC.Qt.CursorShape.PointingHandCursor))
        self.clickable = True
    
    def mousePressEvent(self, QMouseEvent):
        if self.clickable == True:
            self.clicked.emit()
            if QMouseEvent.button() == QtC.Qt.MouseButton.LeftButton:
                self.clicked_l.emit()
            elif QMouseEvent.button() == QtC.Qt.MouseButton.RightButton:
                self.clicked_r.emit()

class Tile(ClickableImage):
    def __init__(self, file, size=None, game=None, rotating=False):
        super().__init__(file, size, size)
        self.reset()
        self.game = game
        self.rotating = rotating
        
        # self.disable()
        # self.index = None
        # self.letter = None
        # self.rotation = 0
        # self.material_data = dict()
    
    def mousePressEvent(self, QMouseEvent):
        if self.clickable == True:
            self.clicked.emit()
            if self.rotating == True:
                print('received mouseclick')
                if QMouseEvent.button() == QtC.Qt.MouseButton.LeftButton:
                    self.rotate(-90)
                elif QMouseEvent.button() == QtC.Qt.MouseButton.RightButton:
                    self.rotate(90)
    
    def reset(self, image=None):
        self.disable()
        self.index = None
        self.letter = None
        self.rotation = 0
        self.material_data = dict()
        
        if image != None:
            self.draw_image(image)
    
    def set_tile(self, file, tile_idx, tile_letter, game):
        self.index = tile_idx
        self.letter = tile_letter
        
        self.draw_image(file)
        for material in game.materials:
            try:
                self.material_data[material] = tile_data.tiles[tile_idx][tile_letter][material]
            except: None # ignore material if it's not in the game (shouldn't be able to happen)
        
    def rotate(self, angle):
        self.rotation += angle
        
        # Pixmap
        pixmap_new = self.pixmap.transformed(QtG.QTransform().rotate(self.rotation), QtC.Qt.TransformationMode.FastTransformation)
        # self.draw_image(pixmap_new)
        try: self.setPixmap(pixmap_new)
        except Exception as e: print(e)
        
        # Material data
        material_data_new = dict()
        try:
            for material in self.material_data.keys():
                material_data_new[material] = list()
                for row in range(len(self.material_data[material])):
                    new_row = []
                    for col in range(len(self.material_data[material])):
                        if angle == -90: # for left hand rotation
                            new_row += [self.material_data[material][col][len(self.material_data[material])-1-row]]
                        elif angle == 90: # for right hand rotation
                            new_row += [self.material_data[material][len(self.material_data[material])-1-col][row]]
                    material_data_new[material] += [new_row]
        except:
            None
                
        self.material_data = material_data_new
        self.game.Tiles.Show_options()

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