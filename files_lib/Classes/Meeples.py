#%% Imports
# PyQt6
import PyQt6.QtGui     as QtG
import PyQt6.QtWidgets as QtW
import PyQt6.QtCore    as QtC
import PyQt6_Extra     as QtE

# Custom classes
# ...

# Other packages
import PIL
from PIL.ImageQt import ImageQt

#%% Meeple classes
class Meeple(QtE.ClickableImage):
    def __init__(self, Carcassonne, meeple_type):
        self.Carcassonne = Carcassonne
        self.meeple_type = meeple_type
        
        self.init_vars()
        super().__init__(self.pixmap, self.size, self.size)
        self.disable()
    
    def init_vars(self):
        self.available = True
        
        self.size = 50
        colour = self.Carcassonne.Refs(f'players/{self.Carcassonne.username}/colour').get()
        file = Get_meeple_file(self.Carcassonne, self.meeple_type)
        
        # Main image
        self.pixmap_original = Colour_fill_file(self.Carcassonne, file, colour)
        self.pixmap = self.pixmap_original
        
        # Black and white image
        img1 = PIL.Image.fromqpixmap(self.pixmap_original)
        pixels1 = img1.load()
        for i in range(img1.size[0]): # for every pixel:
            for j in range(img1.size[1]):
                col = pixels1[i,j]
                grey = int(0.299*col[0] + 0.587*col[1] + 0.114*col[2])
                pixels1[i,j] = (grey, grey, grey, col[3])
        img2 = ImageQt(img1).copy()
        self.pixmap_grey = QtG.QPixmap.fromImage(img2)
    
    def make_available(self):
        self.available = True
        self.setPixmap(self.pixmap_original)
    
    def make_unavailable(self):
        self.available = False
        self.setPixmap(self.pixmap_grey)

#%% Meeple functions
def Colour_fill_file(Carcassonne, file, colour):
    '''Recolours the given file to the proper colours.'''
    pixmap = QtE.GreenScreenPixmap(file) # make (0, 255, 0, 255), green, transparent
    
    all_colours = Carcassonne.Properties.colours
    if colour == all_colours[1]: # red
        pixmap = QtE.GreenScreenPixmap(pixmap, (0, 0, 255), (181, 0, 0))
        
    elif colour == all_colours[2]: # orange
        pixmap = QtE.GreenScreenPixmap(pixmap, (255, 0, 0), (255, 127, 40))
        pixmap = QtE.GreenScreenPixmap(pixmap, (0, 0, 255), (200, 100, 30))
            
    elif colour == all_colours[3]: # yellow
        pixmap = QtE.GreenScreenPixmap(pixmap, (255, 0, 0), (240, 240, 20))
        pixmap = QtE.GreenScreenPixmap(pixmap, (0, 0, 255), (204, 204, 17))
        
    elif colour == all_colours[4]: # green
        pixmap = QtE.GreenScreenPixmap(pixmap, (255, 0, 0), (0, 220, 0))
        pixmap = QtE.GreenScreenPixmap(pixmap, (0, 0, 255), (0, 175, 0))
        
    elif colour == all_colours[5]: # blue
        pixmap = QtE.GreenScreenPixmap(pixmap, (255, 0, 0), (50, 50, 255))
        pixmap = QtE.GreenScreenPixmap(pixmap, (0, 0, 255), (38, 38, 191))
        
    elif colour == all_colours[6]: # magenta
        pixmap = QtE.GreenScreenPixmap(pixmap, (255, 0, 0), (234, 63, 247))
        pixmap = QtE.GreenScreenPixmap(pixmap, (0, 0, 255), (181, 49, 191))
            
    else:
        raise Exception(f'The colour {colour} is not available.')
    return pixmap

def Get_meeple_file(Carcassonne, meeple_type, material=None):
    if material == None:
    # Meeple image for inventory
        if meeple_type == 'standard':
            file = './Images/Meeples/_Default/SF.png'
        elif meeple_type == 'big':
            file = './Images/Meeples/_Default/BF.png'
        elif meeple_type == 'abbot':
            file = './Images/Meeples/_Default/AB.png'
        else:
            raise Exception(f'Meeple type {meeple_type} unknown.')
    else:
    # Meeple image for on the board
        if meeple_type == 'standard':
            if material != 'grass':
                file = './Images/Meeples/_Default/1SF_1.png'
            else:
                file = './Images/Meeples/_Default/1SF_2.png'
        elif meeple_type == 'big':
            if material != 'grass':
                file = './Images/Meeples/_Default/3BF_1.png'
            else:
                file = './Images/Meeples/_Default/3BF_2.png'
        elif meeple_type == 'abbot':
            file = './Images/Meeples/_Default/4AB.png'
        else:
            raise Exception(f'Meeple type {meeple_type} unknown.')
    file = Carcassonne.image_path(file)
    return file

def Get_meeple_on_tile_pixmap(Carcassonne, pixmap_tile, pixmap_meeple, len_mat, sub_length, meeple_pos):
    # Get bounding box to replace with meeple image
    width, height = pixmap_meeple.width(), pixmap_meeple.height()
    if meeple_pos[1] == 0: # start all the way on the left
        x_start = 0
    elif meeple_pos[1] == len_mat-1: # start all the way on the right
        x_start = Carcassonne.Properties.tile_size - width
    else:
        x_start = meeple_pos[1]*sub_length + (sub_length-width)/2
    
    if meeple_pos[0] == 0: # start all the way at the top
        y_start = 0
    elif meeple_pos[0] == len_mat-1: # start all the way at the bottom
        y_start = Carcassonne.Properties.tile_size - height
    else:
        y_start = meeple_pos[0]*sub_length + (sub_length-height)/2
    
    # Load (1) meeple pixmap and (2) tile pixmap
    img1 = PIL.Image.fromqpixmap(pixmap_meeple)
    pixels1 = img1.load()
    img2 = PIL.Image.fromqpixmap(pixmap_tile)
    pixels2 = img2.load()
    
    # Paste meeple on tile in calculated bounding box
    for x in range(width):
        for y in range(height):
            if pixels1[x,y][3] > 0: # only copy if not transparent
                pixels2[x+x_start, y+y_start] = pixels1[x, y]
    img3 = ImageQt(img2).copy()
    new_pixmap = QtG.QPixmap.fromImage(img3)
    
    return new_pixmap