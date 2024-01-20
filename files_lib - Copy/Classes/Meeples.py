import PyQt6.QtGui     as QtG
import PyQt6.QtWidgets as QtW
import PyQt6.QtCore    as QtC
import PyQt6_Extra     as QtE

import Classes.Animations as Animations
import Classes.Tiles as Tiles
import prop_s
import tile_data

import numpy
import PIL
from PIL.ImageQt import ImageQt

class Meeple(QtE.ClickableImage):
    def __init__(self, game, meeple_type):
        self.init_vars(game, meeple_type)
        super().__init__(self.pixmap, self.size, self.size)
    
    def init_vars(self, game, meeple_type):
        self.available = True
        self.game = game
        self.meeple_type = meeple_type
        
        self.size = 50
        colour = self.game.lobby.Refs(f'players/{self.game.lobby.username}/colour').get()
        if self.meeple_type == 'standard':
            file = './Images/Meeples/_Default/SF.png'
        elif self.meeple_type == 'big':
            file = './Images/Meeples/_Default/BF.png'
        elif self.meeple_type == 'abbot':
            file = './Images/Meeples/_Default/AB.png'
        else:
            raise Exception(f'Meeple type {self.meeple_type} unknown.')
        
        # When launching game screen directly, go up an extra folder
        if self.game.lobby.lobby_key == 'test2':
            file = '.'+file
        
        # Main image
        # self.pixmap_original = self.Colour_fill_meeple(file, colour)
        self.pixmap_original = Colour_fill_file(file, colour)
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
            
class Meeple_standard(Meeple):
    def __init__(self, game):
        super().__init__(game, meeple_type='standard')
        self.power = 1

class MeeplePlaceWindow(QtW.QDialog):
    def __init__(self, tile, game, meeple):
        super().__init__(game)
        self.meeple = meeple
        self.setWindowTitle('Place your meeple')
        self.game = game
        self.original_tile = tile
        self.sub_tile_selected = None
        self.patches = {material:dict() for material in self.game.materials}
        self.animation_groups = [Animations.AnimationGroup_parallel(), Animations.AnimationGroup_parallel()]
        
        # Tile layout
        self.main_tile = self.Recreate_tile(tile, self.game.materials)
        tile_layout = self.Split_layout()
        
        # Buttons
        self.y_button = QtW.QPushButton('Confirm')
        self.y_button.setFont(QtG.QFont(prop_s.font, prop_s.font_sizes[-2+game.font_size]))
        self.y_button.clicked.connect(self.accept)
        self.y_button.setEnabled(False)
        
        self.n_button = QtW.QPushButton('Cancel')
        self.n_button.setFont(QtG.QFont(prop_s.font, prop_s.font_sizes[-2+game.font_size]))
        self.n_button.clicked.connect(self.close)
        
        # Final layout
        layout = QtW.QGridLayout()
        layout.addLayout(tile_layout,   0, 0, 1, 2)
        layout.addWidget(self.n_button, 1, 0)
        layout.addWidget(self.y_button, 1, 1)
        self.setLayout(layout)
        
        # Wrap it up
        self.show()
        self.setFixedSize(self.width(), self.height())
    
    def Split_layout(self):
        main_layout = QtW.QHBoxLayout()
        main_layout.addStretch()
        
        # Tile layout
        self.tile_layout = QtW.QGridLayout()
        self.tile_layout.setSpacing(0)
        self.sub_tiles = dict()
        
        pixmap_size = self.pixmap.width()
        pixels = len(tile_data.tiles[1]['A']['grass'])
        self.sub_length = round(pixmap_size/pixels)
        for row in range(pixels):
            row_b = row*self.sub_length
            for col in range(pixels):
                col_b = col*self.sub_length
                
                sub_pixmap = self.pixmap.copy(col_b, row_b, self.sub_length, self.sub_length)
                self.Make_sub_tile(sub_pixmap, row, col)
        
        # Final stretch column
        main_layout.addLayout(self.tile_layout)
        main_layout.addStretch()
        
        return main_layout
    
    def Recreate_tile(self, tile, all_materials):
        # Properties
        file = tile.file
        letter = tile.letter
        index = tile.index
        rotation = tile.rotation
        
        # Making tile
        new_tile = QtE.Tile(None, 160, self.game)
        new_tile.set_tile(file, index, letter, all_materials)
        
        # Rotating
        rotations = int(numpy.floor(rotation/90))
        if rotations < 0:
            for idx in range(-rotations):
                new_tile.rotate(-90)
        elif rotations > 0:
            for idx in range(rotations):
                new_tile.rotate(90)
        
        self.pixmap = new_tile.pixmap.transformed(QtG.QTransform().rotate(rotation), QtC.Qt.TransformationMode.FastTransformation)
        self.pixmap_og = self.pixmap.copy()
        self.material_data = new_tile.material_data
            
        return new_tile
    
    def Make_sub_tile(self, pixmap, row, col):
        # Find out if material patch is occupied
        for material in self.main_tile.material_data.keys():
            mat_idx = self.main_tile.material_data[material][row][col]
            if mat_idx > 0:
            # Material patch found
                # Add subtile to patch
                try:
                    self.patches[material][mat_idx] += [(row, col)]
                except:
                    self.patches[material][mat_idx] = [(row, col)]
                
                # Get strength information
                pos_idx = self.original_tile.possessions[material][mat_idx]
                pos = self.game.possessions[material][pos_idx]
                player_strength = pos['player_strength']
                total_strengths = [sum(player_strength[meeple].values()) for meeple in player_strength.keys()]
                if sum(total_strengths) == 0:
                # Possession has not yet been claimed
                    sub_tile = QtE.ClickableImage(pixmap, self.sub_length, self.sub_length)
                    sub_tile.clicked.connect(self.Position_selected(sub_tile, material, mat_idx, pos_idx))
                    sub_tile.enable()
                    self.tile_layout.addWidget(sub_tile, row, col)
                else:
                # Possession has been claimed, so blur out
                    sub_tile = QtE.QImage(pixmap, self.sub_length, self.sub_length)
                    self.tile_layout.addWidget(sub_tile, row, col)
                    
                    # Blur layer
                    overlay_layer = QtG.QImage(self.sub_length, self.sub_length, QtG.QImage.Format.Format_RGBA64)
                    colour = QtG.QColor(0, 0, 0, 150)
                    overlay_layer.fill(colour)
                    overlay_widget = QtE.QImage(overlay_layer, self.sub_length, self.sub_length)
                    self.tile_layout.addWidget(overlay_widget, row, col)
                    
                self.sub_tiles[(row, col)] = sub_tile
        
    def Position_selected(self, sub_tile, material, mat_idx, pos_idx):
        # sub_tile callback function
        def clicked():
            # Material patch selected update
            self.sub_tile_selected = (material, mat_idx, pos_idx)
            
            # Visualise
            # ...
            # OR Paint meeple on corresponding material patch
            # OR Make material patch blink
            if self.animation_groups[0].repeat == True:
            # Animation 1 is running, so let it finish while using 2
                self.animation_groups[0].stop_animation()
                animation_group = self.animation_groups[1]
            else:
            # Animation 1 can be used
                self.animation_groups[1].stop_animation()
                animation_group = self.animation_groups[0]
            animation_group.clear()
            
            patch_tiles = self.patches[material][mat_idx]
            for coords in patch_tiles:
                sub_tile = self.sub_tiles[coords]
                animation = Animations.Animation(sub_tile)
                animation.add_blinking(1, 0.6, 2000, 0)
                animation_group.add(animation)
            animation_group.start_animation()
            
            # Enable and default the confirm button
            self.y_button.setEnabled(True)
            self.y_button.setDefault(True)
        return clicked

    def Meeple_placed(self, event_push=True):
        # Remove meeple from inventory
        self.meeple.make_unavailable()
        
        # Push to event log
        original_tile_info = (self.original_tile.rotation, self.original_tile.index, self.original_tile.letter, self.original_tile.coords, self.original_tile.file, self.original_tile.rotation)
        self.game.send_feed_message(event              = 'placed_meeple',
                                    meeple_type        = self.meeple.meeple_type,
                                    sub_length         = self.sub_length,
                                    sub_tile           = self.sub_tile_selected,
                                    original_tile_info = original_tile_info)
        
    # def Meeple_placed_event(self, event_data):
    #     # Extract event data
    #     event, meeple_type, original_tile_info, sub_tile, username = event_data.values()
    #     rotation, index, letter, og_coords, file, rotation = original_tile_info
    #     og_row, og_col = og_coords
        
    #     pixmap_og = QtG.QPixmap(file)
    #     pixmap_og = pixmap_og.transformed(QtG.QTransform().rotate(rotation), QtC.Qt.TransformationMode.FastTransformation)
    #     print(file, rotation)
        
    #     player = username
        
    #     # Add strength to possession
    #     material, mat_idx, pos_idx = sub_tile
    #     pos_n = self.game.possessions[material][pos_idx]
    #     pos_n['player_strength'][player][meeple_type] += 1 # self.meeple.power
        
    #     # # Remove meeple from inventory
    #     # self.meeple.make_unavailable()
        
    #     # Find meeple subtile position
    #     meeple_position = tile_data.tiles[index][f'{letter}_m'][material][mat_idx]
    #     self.len_mat = len(tile_data.tiles[index][letter][material][0]) # number of rows/cols in tile data
    #     for rotate in range(int(numpy.floor(rotation%360/90))):
    #         # Find subtile position for meeple placement according to
    #         # (1,1) -> (1,5) -> (5,5) -> (5,1)
    #         # (1,2) -> (2,5) -> (5,4) -> (4,1)
    #         # (0,1) -> (1,6) -> (6,5) -> (5,0)
    #         # (x,y) -> (y,len-1-x)
    #         meeple_position = (meeple_position[1], self.len_mat-1-meeple_position[0])
        
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
        
    #     if 'test' in self.game.lobby.lobby_key:
    #         file = '.'+file
        
    #     colour = self.game.lobby.Refs(f'players/{player}/colour').get()
    #     pixmap = Colour_fill_file(file, colour)
    #     img1 = PIL.Image.fromqpixmap(pixmap)
    #     pixels1 = img1.load()
        
    #     # Get bounding box to replace with meeple image
    #     x_start, y_start, width, height = self.Meeple_bounding_box(pixmap, meeple_position)
        
    #     # Make full tile image
    #     if False:
    #         # meeple_overlay contains just the meeple on transparent tile
    #         tile_layer = QtG.QImage(320, 320, QtG.QImage.Format.Format_RGBA64)
    #         tile_layer.fill(QtG.QColor(0, 0, 0, 0))
    #         img2 = PIL.Image.fromqimage(tile_layer)
    #         pixels2 = img2.load()
    #         for x in range(width):
    #             for y in range(height):
    #                 pixels2[x+x_start, y+y_start] = pixels1[x, y]
    #         img3 = ImageQt(img2).copy()
    #         pixmap = QtG.QPixmap.fromImage(img3)
    #         meeple_overlay = QtE.Tile(pixmap, 320*prop_s.tile_size, self.game)
            
    #         # Find tile coords on board
    #         row, col = Tiles.Board_tile_coords(self.original_tile, self.game.board)
            
    #         # FIXME: This probably has to be a stacked widget, such that, when a 
    #         # FIXME: meeple is given back, its layer can be removed.
    #         # FIXME: That might mean that each tile has to be a separate 
    #         # FIXME: QGridLayout, because that can display multiple widgets at once
    #         row_layout = self.game.board.itemAt(row).layout()
    #         row_layout.replaceWidget(self.original_tile, meeple_overlay)
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
    #         self.game.board_tiles[og_row][og_col].setPixmap(pixmap)
        
    #     # Set tile information
    #     # self.game.board_tiles[row][col].meeples[material][mat_idx] = self.meeple.meeple_type
    #     self.game.board_tiles[og_row][og_col].meeples[player] += [(material, mat_idx, meeple_type)] # FIXME: add stacked layer later
        
    #     # Finish possession if you claimed a finished possession
    #     if pos_n['open'] == False: # finished!
    #         self.game.pos_class.Possession_finished(pos_n, material)
    
def Meeple_bounding_box(len_mat, sub_length, pixmap, meeple_pos):
    width, height = pixmap.width(), pixmap.height()
    if meeple_pos[1] == 0: # start all the way on the left
        x_start = 0
    elif meeple_pos[1] == len_mat-1: # start all the way on the right
        x_start = prop_s.tile_size - width
    else:
        x_start = meeple_pos[1]*sub_length + (sub_length-width)/2
    
    if meeple_pos[0] == 0: # start all the way at the top
        y_start = 0
    elif meeple_pos[0] == len_mat-1: # start all the way at the bottom
        y_start = prop_s.tile_size - height
    else:
        y_start = meeple_pos[0]*sub_length + (sub_length-height)/2
    
    return x_start, y_start, width, height

def En_dis_able_meeples(game, enable):
    '''
    enable : bool
        True: will enable all available meeples
        False: will disable all meeples
    '''
    available_meeple_types = game.__dict__
    for meeple_type in ['meeples_standard', 'meeples_abbot', 'meeples_big']:
        # Check if meeple type is in game
        if meeple_type in available_meeple_types:
            # Get all meeples from the type
            meeples = getattr(game, meeple_type)
            for meeple in meeples.values():
                if enable == True:
                    # If meeple is available, enable it to be clicked on
                    if meeple.available == True:
                        meeple.enable()
                else: # When disabling, all should be disabled
                    meeple.disable()

def Colour_fill_file(file, colour):
    '''Recolours the default meeple images to the proper colours.'''
    pixmap = QtE.GreenScreenPixmap(file)
    if colour == prop_s.colours[1]: # red
        pixmap = QtE.GreenScreenPixmap(pixmap, (0, 0, 255), (181, 0, 0))
        
    elif colour == prop_s.colours[2]: # orange
        pixmap = QtE.GreenScreenPixmap(pixmap, (255, 0, 0), (255, 127, 40))
        pixmap = QtE.GreenScreenPixmap(pixmap, (0, 0, 255), (200, 100, 30))
            
    elif colour == prop_s.colours[3]: # yellow
        pixmap = QtE.GreenScreenPixmap(pixmap, (255, 0, 0), (240, 240, 20))
        pixmap = QtE.GreenScreenPixmap(pixmap, (0, 0, 255), (204, 204, 17))
        
    elif colour == prop_s.colours[4]: # green
        pixmap = QtE.GreenScreenPixmap(pixmap, (255, 0, 0), (0, 220, 0))
        pixmap = QtE.GreenScreenPixmap(pixmap, (0, 0, 255), (0, 175, 0))
        
    elif colour == prop_s.colours[5]: # blue
        pixmap = QtE.GreenScreenPixmap(pixmap, (255, 0, 0), (50, 50, 255))
        pixmap = QtE.GreenScreenPixmap(pixmap, (0, 0, 255), (38, 38, 191))
        
    elif colour == prop_s.colours[6]: # magenta
        pixmap = QtE.GreenScreenPixmap(pixmap, (255, 0, 0), (234, 63, 247))
        pixmap = QtE.GreenScreenPixmap(pixmap, (0, 0, 255), (181, 49, 191))
            
    else:
        raise Exception(f'The colour {colour} is not available.')
    return pixmap

def Meeple_placed_event(game, event_data):
    # Extract event data
    event, meeple_type, original_tile_info, sub_length, sub_tile, username = event_data.values()
    rotation, index, letter, og_coords, file, rotation = original_tile_info
    og_row, og_col = og_coords
    
    pixmap_og = QtG.QPixmap(file)
    pixmap_og = pixmap_og.transformed(QtG.QTransform().rotate(rotation), QtC.Qt.TransformationMode.FastTransformation)
    
    player = username
    
    # Add strength to possession
    material, mat_idx, pos_idx = sub_tile
    pos_n = game.possessions[material][pos_idx]
    pos_n['player_strength'][player][meeple_type] += 1 # self.meeple.power
    
    # # Remove meeple from inventory
    # self.meeple.make_unavailable()
    
    # Find meeple subtile position
    meeple_position = tile_data.tiles[index][f'{letter}_m'][material][mat_idx]
    len_mat = len(tile_data.tiles[index][letter][material][0]) # number of rows/cols in tile data
    for rotate in range(int(numpy.floor(rotation%360/90))):
        # Find subtile position for meeple placement according to
        # (1,1) -> (1,5) -> (5,5) -> (5,1)
        # (1,2) -> (2,5) -> (5,4) -> (4,1)
        # (0,1) -> (1,6) -> (6,5) -> (5,0)
        # (x,y) -> (y,len-1-x)
        meeple_position = (meeple_position[1], len_mat-1-meeple_position[0])
    
    # Compare meeple image size to subtile size
    if meeple_type == 'standard':
        if material == 'grass':
            file = './Images/Meeples/_Default/1SF_2.png'
        else:
            file = './Images/Meeples/_Default/1SF_1.png'
    elif meeple_type == 'big':
        if material == 'grass':
            file = './Images/Meeples/_Default/1BF_2.png'
        else:
            file = './Images/Meeples/_Default/1BF_1.png'
    elif meeple_type == 'abbot':
        file = './Images/Meeples/_Default/AB.png'
    else:
        raise Exception(f'Meeple type {meeple_type} unknown.')
    
    if game.lobby.lobby_key == 'test2':
        file = '.'+file
    
    colour = game.lobby.Refs(f'players/{player}/colour').get()
    pixmap = Colour_fill_file(file, colour)
    img1 = PIL.Image.fromqpixmap(pixmap)
    pixels1 = img1.load()
    
    # Get bounding box to replace with meeple image
    x_start, y_start, width, height = Meeple_bounding_box(len_mat, sub_length, pixmap, meeple_position)
    
    # Make full tile image
    if False:
        pass
        # # meeple_overlay contains just the meeple on transparent tile
        # tile_layer = QtG.QImage(320, 320, QtG.QImage.Format.Format_RGBA64)
        # tile_layer.fill(QtG.QColor(0, 0, 0, 0))
        # img2 = PIL.Image.fromqimage(tile_layer)
        # pixels2 = img2.load()
        # for x in range(width):
        #     for y in range(height):
        #         pixels2[x+x_start, y+y_start] = pixels1[x, y]
        # img3 = ImageQt(img2).copy()
        # pixmap = QtG.QPixmap.fromImage(img3)
        # meeple_overlay = QtE.Tile(pixmap, 320*prop_s.tile_size, game)
        
        # # Find tile coords on board
        # row, col = Tiles.Board_tile_coords(original_tile, game.board)
        
        # # FIXME: This probably has to be a stacked widget, such that, when a 
        # # FIXME: meeple is given back, its layer can be removed.
        # # FIXME: That might mean that each tile has to be a separate 
        # # FIXME: QGridLayout, because that can display multiple widgets at once
        # row_layout = game.board.itemAt(row).layout()
        # row_layout.replaceWidget(original_tile, meeple_overlay)
    else:
        img2 = PIL.Image.fromqpixmap(pixmap_og)
        pixels2 = img2.load()
        for x in range(width):
            for y in range(height):
                if pixels1[x,y][3] > 0: # only copy if not transparent
                    pixels2[x+x_start, y+y_start] = pixels1[x, y]
        img3 = ImageQt(img2).copy()
        pixmap = QtG.QPixmap.fromImage(img3)
        # meeple_tile = QtE.Tile(pixmap, 320*prop_s.tile_size)
        game.board_tiles[og_row][og_col].setPixmap(pixmap)
    
    # Set tile information
    # self.game.board_tiles[row][col].meeples[material][mat_idx] = self.meeple.meeple_type
    game.board_tiles[og_row][og_col].meeples[player] += [(material, mat_idx, meeple_type)] # FIXME: add stacked layer later
    
    # Finish possession if you claimed a finished possession
    if pos_n['open'] == False: # finished!
        game.pos_class.Possession_finished(pos_n, material)