#%% Imports
# PyQt6
import PyQt6.QtGui     as QtG
import PyQt6.QtWidgets as QtW
import PyQt6.QtCore    as QtC
import PyQt6_Extra     as QtE

# Custom classes
from Dialogs.YesNo import YesNoDialog

# Other packages
# ...

# Old imports
# import Classes.Animations as Animations
# import Classes.Tiles as Tiles
# import prop_s
import tile_data

import numpy
import PIL
from PIL.ImageQt import ImageQt

#%% Meeple classes
class Meeple(QtE.ClickableImage):
    def __init__(self, Carcassonne, meeple_type):
        self.Carcassonne = Carcassonne
        self.meeple_type = meeple_type
        
        self.init_vars()
        super().__init__(self.pixmap, self.size, self.size)
    
    def init_vars(self):
        self.available = True
        
        self.size = 50
        colour = self.Carcassonne.Refs(f'players/{self.Carcassonne.username}/colour').get()
        file = self._Get_file()
        
        # Main image
        self.pixmap_original = self._Colour_fill_file(file, colour)
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
    
    def _Get_file(self):
        if self.meeple_type == 'standard':
            file = './Images/Meeples/_Default/SF.png'
        elif self.meeple_type == 'big':
            file = './Images/Meeples/_Default/BF.png'
        elif self.meeple_type == 'abbot':
            file = './Images/Meeples/_Default/AB.png'
        else:
            raise Exception(f'Meeple type {self.meeple_type} unknown.')
        return file
    
    def _Colour_fill_file(self, file, colour):
        '''Recolours the default meeple images to the proper colours.'''
        pixmap = QtE.GreenScreenPixmap(file)
        all_colours = self.Carcassonne.Properties.colours
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
    
    def make_available(self):
        self.available = True
        self.setPixmap(self.pixmap_original)
    
    def make_unavailable(self):
        self.available = False
        self.setPixmap(self.pixmap_grey)
            
class Meeple_standard(Meeple):
    def __init__(self, Carcassonne):
        super().__init__(Carcassonne, meeple_type='standard')
        self.power = 1

class Meeple_big(Meeple):
    def __init__(self, Carcassonne):
        super().__init__(Carcassonne, meeple_type='big')
        pass

class Meeple_abbot(Meeple):
    def __init__(self, Carcassonne):
        super().__init__(Carcassonne, meeple_type='abbot')
        pass

# def Meeple_bounding_box(len_mat, sub_length, pixmap, meeple_pos):
#     width, height = pixmap.width(), pixmap.height()
#     if meeple_pos[1] == 0: # start all the way on the left
#         x_start = 0
#     elif meeple_pos[1] == len_mat-1: # start all the way on the right
#         x_start = prop_s.tile_size - width
#     else:
#         x_start = meeple_pos[1]*sub_length + (sub_length-width)/2
    
#     if meeple_pos[0] == 0: # start all the way at the top
#         y_start = 0
#     elif meeple_pos[0] == len_mat-1: # start all the way at the bottom
#         y_start = prop_s.tile_size - height
#     else:
#         y_start = meeple_pos[0]*sub_length + (sub_length-height)/2
    
#     return x_start, y_start, width, height

# def En_dis_able_meeples(game, enable):
#     '''
#     enable : bool
#         True: will enable all available meeples
#         False: will disable all meeples
#     '''
#     available_meeple_types = game.__dict__
#     for meeple_type in ['meeples_standard', 'meeples_abbot', 'meeples_big']:
#         # Check if meeple type is in game
#         if meeple_type in available_meeple_types:
#             # Get all meeples from the type
#             meeples = getattr(game, meeple_type)
#             for meeple in meeples.values():
#                 if enable == True:
#                     # If meeple is available, enable it to be clicked on
#                     if meeple.available == True:
#                         meeple.enable()
#                 else: # When disabling, all should be disabled
#                     meeple.disable()

# def Meeple_placed_event(game, event_data):
#     # Extract event data
#     event, meeple_type, original_tile_info, sub_length, sub_tile, username = event_data.values()
#     rotation, index, letter, og_coords, file, rotation = original_tile_info
#     og_row, og_col = og_coords
    
#     pixmap_og = QtG.QPixmap(file)
#     pixmap_og = pixmap_og.transformed(QtG.QTransform().rotate(rotation), QtC.Qt.TransformationMode.FastTransformation)
    
#     player = username
    
#     # Add strength to possession
#     material, mat_idx, pos_idx = sub_tile
#     pos_n = game.possessions[material][pos_idx]
#     pos_n['player_strength'][player][meeple_type] += 1 # self.meeple.power
    
#     # # Remove meeple from inventory
#     # self.meeple.make_unavailable()
    
#     # Find meeple subtile position
#     meeple_position = tile_data.tiles[index][f'{letter}_m'][material][mat_idx]
#     len_mat = len(tile_data.tiles[index][letter][material][0]) # number of rows/cols in tile data
#     for rotate in range(int(numpy.floor(rotation%360/90))):
#         # Find subtile position for meeple placement according to
#         # (1,1) -> (1,5) -> (5,5) -> (5,1)
#         # (1,2) -> (2,5) -> (5,4) -> (4,1)
#         # (0,1) -> (1,6) -> (6,5) -> (5,0)
#         # (x,y) -> (y,len-1-x)
#         meeple_position = (meeple_position[1], len_mat-1-meeple_position[0])
    
#     # Compare meeple image size to subtile size
#     if meeple_type == 'standard':
#         if material == 'grass':
#             file = './Images/Meeples/_Default/1SF_2.png'
#         else:
#             file = './Images/Meeples/_Default/1SF_1.png'
#     elif meeple_type == 'big':
#         if material == 'grass':
#             file = './Images/Meeples/_Default/1BF_2.png'
#         else:
#             file = './Images/Meeples/_Default/1BF_1.png'
#     elif meeple_type == 'abbot':
#         file = './Images/Meeples/_Default/AB.png'
#     else:
#         raise Exception(f'Meeple type {meeple_type} unknown.')
    
#     if game.lobby.lobby_key == 'test2':
#         file = '.'+file
    
#     colour = game.lobby.Refs(f'players/{player}/colour').get()
#     pixmap = Colour_fill_file(file, colour)
#     img1 = PIL.Image.fromqpixmap(pixmap)
#     pixels1 = img1.load()
    
#     # Get bounding box to replace with meeple image
#     x_start, y_start, width, height = Meeple_bounding_box(len_mat, sub_length, pixmap, meeple_position)
    
#     # Make full tile image
#     if False:
#         pass
#         # # meeple_overlay contains just the meeple on transparent tile
#         # tile_layer = QtG.QImage(320, 320, QtG.QImage.Format.Format_RGBA64)
#         # tile_layer.fill(QtG.QColor(0, 0, 0, 0))
#         # img2 = PIL.Image.fromqimage(tile_layer)
#         # pixels2 = img2.load()
#         # for x in range(width):
#         #     for y in range(height):
#         #         pixels2[x+x_start, y+y_start] = pixels1[x, y]
#         # img3 = ImageQt(img2).copy()
#         # pixmap = QtG.QPixmap.fromImage(img3)
#         # meeple_overlay = QtE.Tile(pixmap, 320*prop_s.tile_size, game)
        
#         # # Find tile coords on board
#         # row, col = Tiles.Board_tile_coords(original_tile, game.board)
        
#         # # FIXME: This probably has to be a stacked widget, such that, when a 
#         # # FIXME: meeple is given back, its layer can be removed.
#         # # FIXME: That might mean that each tile has to be a separate 
#         # # FIXME: QGridLayout, because that can display multiple widgets at once
#         # row_layout = game.board.itemAt(row).layout()
#         # row_layout.replaceWidget(original_tile, meeple_overlay)
#     else:
#         img2 = PIL.Image.fromqpixmap(pixmap_og)
#         pixels2 = img2.load()
#         for x in range(width):
#             for y in range(height):
#                 if pixels1[x,y][3] > 0: # only copy if not transparent
#                     pixels2[x+x_start, y+y_start] = pixels1[x, y]
#         img3 = ImageQt(img2).copy()
#         pixmap = QtG.QPixmap.fromImage(img3)
#         # meeple_tile = QtE.Tile(pixmap, 320*prop_s.tile_size)
#         game.board_tiles[og_row][og_col].setPixmap(pixmap)
    
#     # Set tile information
#     # self.game.board_tiles[row][col].meeples[material][mat_idx] = self.meeple.meeple_type
#     game.board_tiles[og_row][og_col].meeples[player] += [(material, mat_idx, meeple_type)] # FIXME: add stacked layer later
    
#     # Finish possession if you claimed a finished possession
#     if pos_n['open'] == False: # finished!
#         game.pos_class.Possession_finished(pos_n, material)