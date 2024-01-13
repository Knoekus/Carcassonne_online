import PyQt6.QtGui     as QtG
import PyQt6.QtWidgets as QtW
import PyQt6.QtCore    as QtC
import PyQt6_Extra     as QtE

from Classes.Animations import Animation
import prop_s
import tile_data

import numpy

class Meeple(QtE.ClickableImage):
    def __init__(self, game, meeple_type):
        self.init_vars(game, meeple_type)
        super().__init__(self.pixmap, self.size, self.size)
    
    def init_vars(self, game, meeple_type):
        self.available = True
        self.enabled = False
        self.game = game
        
        self.size = 50
        colour = self.game.lobby.Refs(f'players/{self.game.lobby.username}/colour').get()
        colour_string = self.Colour_string(colour)
        if meeple_type == 'standard':
            file = f'./Images/Meeples/{colour_string}/SF.png'
        
        # When launching game screen directly, go up an extra folder
        if 'test' in self.game.lobby.lobby_key:
            file = '.'+file
        
        self.pixmap = QtE.GreenScreenPixmap(file)
    
    def Colour_string(self, colour):
        '''Convert a HEX colour code to a string.'''
        if colour == prop_s.colours[1]:
            return 'Red'
        elif colour == prop_s.colours[2]:
            return 'Orange'
        elif colour == prop_s.colours[3]:
            return 'Yellow'
        elif colour == prop_s.colours[4]:
            return 'Green'
        elif colour == prop_s.colours[5]:
            return 'Blue'
        elif colour == prop_s.colours[6]:
            return 'Magenta'
        else:
            raise Exception(f'The colour {colour} is not available.')
            
class Meeple_standard(Meeple):
    def __init__(self, game):
        super().__init__(game, meeple_type='standard')
        self.power = 1

class MeeplePlaceWindow(QtW.QDialog):
    def __init__(self, tile, meeple_type, game, parent=None):
        super().__init__(parent)
        self.setWindowTitle('Place your meeple')
        self.game = game
        self.original_tile = tile
        self.sub_tile_selected = None
        
        # Tile layout
        self.main_tile = self.Recreate_tile(tile, self.game.materials)
        tile_layout = self.Split_layout()
        
        # Buttons
        self.y_button = QtW.QPushButton('Confirm')
        self.y_button.setFont(QtG.QFont(prop_s.font, prop_s.font_sizes[-2+parent.font_size]))
        self.y_button.clicked.connect(self.accept)
        self.y_button.setEnabled(False)
        
        self.n_button = QtW.QPushButton('Cancel')
        self.n_button.setFont(QtG.QFont(prop_s.font, prop_s.font_sizes[-2+parent.font_size]))
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
        self.tile_layout.setSpacing(prop_s.tile_spacing)
        self.sub_tiles = dict()
        
        pixmap_size = self.pixmap.width()
        pixels = len(tile_data.tiles[1]['A']['grass'])
        sub_length = round(pixmap_size/pixels)
        for row in range(pixels):
            row_b = row*sub_length
            for col in range(pixels):
                col_b = col*sub_length
                
                sub_pixmap = self.pixmap.copy(col_b, row_b, sub_length, sub_length)
                self.Make_sub_tile(sub_pixmap, sub_length, row, col)
        
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
        new_tile = QtE.Tile(None, 160)
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
        self.material_data = new_tile.material_data
            
        return new_tile
    
    def Make_sub_tile(self, pixmap, length, row, col):
        # Find out if material patch is occupied
        for material in self.main_tile.material_data.keys():
            mat_idx = self.main_tile.material_data[material][row][col]
            if mat_idx > 0:
            # Material patch found
                pos_idx = self.original_tile.possessions[material][mat_idx]
                pos = self.game.possessions[material][pos_idx]
                player_strength = pos['player_strength']
                total_strengths = [sum(player_strength[meeple].values()) for meeple in player_strength.keys()]
                if sum(total_strengths) == 0:
                # Possession has not yet been claimed
                    sub_tile = QtE.ClickableImage(pixmap, length, length)
                    sub_tile.clicked.connect(self.Position_selected(sub_tile, material, mat_idx, pos_idx))
                    sub_tile.enable()
                    self.tile_layout.addWidget(sub_tile, row, col)
                else:
                # Possession has been claimed, so blur out
                    sub_tile = QtE.QImage(pixmap, length, length)
                    self.tile_layout.addWidget(sub_tile, row, col)
                    
                    # Blur layer
                    overlay_layer = QtG.QImage(length, length, QtG.QImage.Format.Format_RGBA64)
                    colour = QtG.QColor(255, 255, 255, 100)
                    overlay_layer.fill(colour)
                    overlay_widget = QtE.QImage(overlay_layer, length, length)
                    self.tile_layout.addWidget(overlay_widget, row, col)
                    
                self.sub_tiles[(row, col)] = sub_tile
        
    def Position_selected(self, sub_tile, material, mat_idx, pos_idx):
        # sub_tile callback function
        def clicked():
            # Material patch selected update
            self.sub_tile_selected = (material, mat_idx, pos_idx)
            
            # Visualise
            # ...
            # Paint meeple on corresponding material patch
            
            # Enable and default the confirm button
            self.y_button.setEnabled(True)
            self.y_button.setDefault(True)
        return clicked

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