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
    
    def rescale(self, scale):
        self.setFixedWidth(self.width() * scale)
        self.setFixedHeight(self.height() * scale)
    
    def draw_image(self, file):
        if type(file) == str:
            # Only change file string if it's actually a tile, not the logo
            if 'tile_' not in file:
                self.file = file
            
            self.pixmap = QtG.QPixmap(file)
            self.setPixmap(self.pixmap)
        elif type(file) == type(QtG.QPixmap()):
            # self.file = None
            self.setPixmap(file)
        elif file == None:
            # self.file = None
            self.setPixmap(QtG.QPixmap())
            
        elif type(file) == type(QtG.QImage()):
            self.pixmap = QtG.QPixmap.fromImage(file)
            self.setPixmap(self.pixmap)
        else:
            raise Exception(f'Unknown file type for QtE.QImage object: {type(file)}, {type(QtG.QImage())}')
  
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
        self.possessions = dict()
        self.coords = ()
    
    def update_possessions(self, material, mat_idx, pos_idx):
        if material not in self.possessions.keys():
        # Make material entry in possessions list if it doesn't exist yet
            self.possessions[material] = dict()
        
        # Give possession index for material index
        self.possessions[material][mat_idx] = pos_idx
    
    def mousePressEvent(self, QMouseEvent):
        if self.clickable == True:
            self.clicked.emit()
            if self.rotating == True:
                if QMouseEvent.button() == QtC.Qt.MouseButton.LeftButton:
                    self.rotate(-90)
                elif QMouseEvent.button() == QtC.Qt.MouseButton.RightButton:
                    self.rotate(90)
                if self.game != None:
                    self.game.Tiles.Show_options()
    
    def reset(self, image=None):
        self.disable()
        self.index = None
        self.letter = None
        self.rotation = 0
        self.material_data = dict()
        
        # if image != None:
        #     self.draw_image(image)
    
    def set_tile(self, file, tile_idx, tile_letter, all_materials):
        self.index = tile_idx
        self.letter = tile_letter
        
        self.draw_image(file)
        if tile_idx != None: # only do this if an actual tile is set
            # for material in all_materials:
            #     try:
            #         self.material_data[material] = tile_data.tiles[tile_idx][tile_letter][material]
            #     except: None # ignore material if it's not in the game or the tile has no information about it
            self.material_data = tile_data.tiles[tile_idx][tile_letter]
            self.meeples = {material:
                                {mat_idx:0 for mat_idx in range(1, max(max(self.material_data[material]))+1)}
                            for material in self.material_data.keys()}
        
    def rotate(self, angle):
        if angle not in [-90, 90]:
            raise Exception('The rotation angle must be either -90 or 90.')
        self.rotation = (self.rotation + angle) % 360
        
        # Pixmap
        pixmap_old = QtG.QPixmap(self.file)
        pixmap_new = pixmap_old.transformed(QtG.QTransform().rotate(self.rotation), QtC.Qt.TransformationMode.FastTransformation)
        self.setPixmap(pixmap_new)
        
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

def GreenScreenPixmap(file, before=(0, 255, 0, 255), after=(0, 0, 0, 0)):
    if len(before) == 3:
        before = tuple([x for x in before] + [255]) # full opacity
    if len(after) == 3:
        after = tuple([x for x in after] + [255]) # full opacity
    
    if type(file) == str:
        img1 = PIL.Image.open(file)
    elif type(file) == type(QtG.QPixmap()):
        # img1 = file.toImage()
        img1 = PIL.Image.fromqpixmap(file)
        
    pixels1 = img1.load()
    for i in range(img1.size[0]): # for every pixel:
        for j in range(img1.size[1]):
            if pixels1[i,j] == before: # if full green
                pixels1[i,j] = after      # make transparent
    
    img2 = ImageQt(img1).copy()
    pixmap = QtG.QPixmap.fromImage(img2)
    return pixmap