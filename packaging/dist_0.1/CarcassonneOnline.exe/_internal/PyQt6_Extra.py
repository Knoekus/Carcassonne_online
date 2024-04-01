#%% Imports
# PyQt6
import PyQt6.QtCore    as QtC
import PyQt6.QtGui     as QtG
import PyQt6.QtWidgets as QtW

# Custom classes
import tile_data

# Other packages
import PIL
from PIL.ImageQt import ImageQt
import time

#%% PyQt6 Extra
class QLabel(QtW.QLabel):
    def __init__(self, text, font, alignment='center'):
        # Alignment
        if alignment == 'center':
            align = QtC.Qt.AlignmentFlag.AlignCenter
        elif alignment == 'left':
            align = QtC.Qt.AlignmentFlag.AlignLeft
        elif alignment == 'right':
            align = QtC.Qt.AlignmentFlag.AlignRight
        else:
            raise Exception('Alignment type not implemented.')
            
        # Make label
        super().__init__(text, alignment=align)
        
        # Set font
        self.setFont(font)

class ClickableLabel(QtW.QLabel):
    clicked = QtC.pyqtSignal()
    def __init__(self, parent=None, enabled=False):
        super().__init__(parent)
        self.enabled = enabled
        if self.enabled == True:
            self.setCursor(QtG.QCursor(QtC.Qt.CursorShape.PointingHandCursor))
    
    def mousePressEvent(self, event):
        if self.enabled == True:
            self.clicked.emit()
    
    def enable(self):
        self.setCursor(QtG.QCursor(QtC.Qt.CursorShape.PointingHandCursor))
        self.enabled = True
    
    def disable(self):
        self.setCursor(QtG.QCursor(QtC.Qt.CursorShape.ArrowCursor))
        self.enabled = False
        
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
            self.setPixmap(file)
        elif file == None:
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
    # Maybe:
    # test = QtW.QStackedLayout()
    # test.setStackingMode(QtW.QStackedLayout.StackingMode.StackAll)
    # 
    # or:
    # QtW.QGraphicsView()
    # def __init__(self, file, size=None, Carcassonne=None, rotating=False):
        
    def __init__(self, file, size=None, Carcassonne=None):
        super().__init__(file, size, size)
        self.Carcassonne = Carcassonne
        self.index = None
        self.letter = None
        self.rotation = 0
        self.coords = ()
        self.material_data = dict()
        self.possessions = dict()
    
    def mousePressEvent(self, QMouseEvent):
        if self.clickable == True and self.index == None and self.letter == None:
        # Option tile
            self.clicked.emit()
        elif self.clickable == True:
        # Tile placed on the board
            '''Open meeple placement window, for example when there are multiple tiles that a meeple can be placed on.'''
            pass
    
    def reset_image(self):
        # Pixmap
        pixmap_old = QtG.QPixmap(self.file)
        pixmap_new = pixmap_old.transformed(QtG.QTransform().rotate(self.rotation), QtC.Qt.TransformationMode.FastTransformation)
        self.setPixmap(pixmap_new)
    
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
        self.material_data = material_data_new
    
    def set_tile(self, file, tile_idx, tile_letter):
        self.index = tile_idx
        self.letter = tile_letter
        self.rotation = 0 # start with a fresh file, so no rotation
        
        self.draw_image(file)
        
        if tile_letter != None: # only do this if an actual tile is set
            # Add material data
            self.material_data = tile_data.tiles[tile_idx][tile_letter]
            
            # Add meeple list for each connection
            for idx in range(50):
                player_list_dict = self.Carcassonne.Refs('connections').get()
                if type(player_list_dict) == type(dict()):
                    player_list = player_list_dict.keys()
                    break
                else:
                    time.sleep(0.1)
            else:
                raise Exception('No connections found after 5 seconds.')
            self.meeples = {player:list() for player in player_list}
    
    def update_possessions(self, material, mat_idx, pos_idx):
        if material not in self.possessions.keys():
        # Make material entry in possessions list if it doesn't exist yet
            self.possessions[material] = dict()
        
        # Give possession index for material index
        self.possessions[material][mat_idx] = pos_idx
        
class NewTile(ClickableImage):
    def __init__(self, file, size, Carcassonne):
        super().__init__(file, size, size)
        self.Carcassonne = Carcassonne
        self.index = None
        self.letter = None
        self.rotation = 0
        self.material_data = dict()
        self.possessions = dict()
    
    def mousePressEvent(self, QMouseEvent):
        if self.clickable == True:
            self.clicked.emit()
            if QMouseEvent.button() == QtC.Qt.MouseButton.LeftButton:
                rotation = -90
            elif QMouseEvent.button() == QtC.Qt.MouseButton.RightButton:
                rotation = 90
                
            # Event push for the rest
            self.Carcassonne.game_func._Feed_send_tile_rotated(rotation)
        
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
        self.material_data = material_data_new
    
    def set_tile(self, file, tile_idx, tile_letter):
        # Draw image
        self.index = tile_idx
        self.letter = tile_letter
        self.rotation = 0
        self.draw_image(file)
        
        # Material data
        self.material_data = tile_data.tiles[tile_idx][tile_letter]
        
        # Add meeple list for each connection
        for idx in range(10):
            player_list_dict = self.Carcassonne.Refs('connections').get()
            if type(player_list_dict) == type(dict()):
                player_list = player_list_dict.keys()
                break
            else:
                time.sleep(0.1)
        else:
            raise Warning('No connections found after 1 second.')
        self.meeples = {player:list() for player in player_list}
    
    def update_possessions(self, material, mat_idx, pos_idx):
        if material not in self.possessions.keys():
        # Make material entry in possessions list if it doesn't exist yet
            self.possessions[material] = dict()
        
        # Give possession index for material index
        self.possessions[material][mat_idx] = pos_idx

def GreenScreenPixmap(file, before=(0, 255, 0, 255), after=(0, 0, 0, 0)):
    if len(before) == 3:
        before = tuple([x for x in before] + [255]) # full opacity
    if len(after) == 3:
        after = tuple([x for x in after] + [255]) # full opacity
    
    if type(file) == str:
        img1 = PIL.Image.open(file)
    elif type(file) == type(QtG.QPixmap()):
        img1 = PIL.Image.fromqpixmap(file)
        
    pixels1 = img1.load()
    for i in range(img1.size[0]): # for every pixel:
        for j in range(img1.size[1]):
            if pixels1[i,j] == before: # if full green
                pixels1[i,j] = after      # make transparent
    
    img2 = ImageQt(img1).copy()
    pixmap = QtG.QPixmap.fromImage(img2)
    return pixmap