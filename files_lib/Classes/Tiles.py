import PyQt6.QtGui     as QtG
import PyQt6.QtWidgets as QtW
import PyQt6.QtCore    as QtC
import PyQt6_Extra     as QtE
import string
import prop_s
import tile_data

# from Classes.Animations import Animation

import os
import random as rnd
import copy

class Tiles():
    def __init__(self, game):
        self.game = game
        self.lobby_key = game.lobby.lobby_key
        self.game.tiles = dict()
    
    def Add_tiles(self, prefix, numbers):
        self.game.tiles[prefix] = dict()
        for idx, number in enumerate(numbers):
            letter = string.ascii_uppercase[idx]
            self.game.tiles[prefix][letter] = number
    
    def Update_tiles_left_label(self):
        self.game.tiles_left = sum([sum(expansion.values()) for expansion in self.game.tiles.values()])
        self.game.tiles_left_label.setText(f'{self.game.tiles_left} tiles left.')
    
    def New_tile(self, tile_idx_in=None, tile_letter_in=None):
        while True:
            tile_idx, tile_letter, file = self.Choose_tile(tile_idx_in, tile_letter_in)

            # Give new tile the material data            
            for material in self.game.materials:
                try:
                    self.game.new_tile.material_data[material] = tile_data.tiles[tile_idx][tile_letter][material]
                except: None # ignore material if it's not in the game (shouldn't be able to happen)
            
            # Allow tile if there are options to place it
            options = set()
            for idx in range(4): # try each orientation
                self.game.new_tile.clicked_l.emit()
                options |= self.Tile_options(tile_idx, tile_letter)
                if len(options) > 0: break # if options are found before trying all rotations, don't try the rest
            if len(options) > 0:
                self.game.new_tile.rotation = 0 # reset rotation
                break
        
        # Update tiles left
        self.game.new_tile_anim.swap_image(file, tile_idx, tile_letter, 1000) # replaces set_tile, maybe relocate to QtE
        self.game.new_tile.enable()
        if self.game.tiles[tile_idx][tile_letter] > 1:
            self.game.tiles[tile_idx][tile_letter] -= 1 # decrease number of tiles by 1
        else:
            if len(self.game.tiles[tile_idx].keys()) > 1:
                self.game.tiles[tile_idx].pop(tile_letter) # delete tile if none left
            else:
                self.game.tiles.pop(tile_idx) # delete expansion if no tiles left
        
        # Update tiles left label
        self.Update_tiles_left_label()
        
        # Show placement options
        self.Show_options()
    
    # def Show_options(self, tile_idx, tile_letter):
    def Show_options(self):
        tile_idx, tile_letter = self.game.new_tile.index, self.game.new_tile.letter
        
        # Clear old options
        for option in self.game.options:
            row, col = option
            tile = self.game.board_tiles[row][col]
            tile.disable()
            tile.set_tile(None, None, None, self.game)
            # self.game.board_tiles[row][col].swap_image(None, None, None, 1000) # replaces set_tile, maybe relocate to QtE
        
        # Get new options
        self.game.options = self.Tile_options(tile_idx, tile_letter)
        
        # Get image
        if self.lobby_key == 'test2':
            file = '..\\Images\\tile_available'
        else: # call from lobby
            file = '.\\Images\\tile_available'
        
        # Set options' images
        for option in self.game.options:
            row, col = option
            tile = self.game.board_tiles[row][col]
            tile.enable()
            tile.set_tile(file, None, None, self.game)
            try: tile.clicked.disconnect()
            except: None
            tile.clicked.connect(self.Option_clicked(row, col))
            # tile.swap_image(file, None, None, 1000) # replaces set_tile, maybe relocate to QtE
            
    def Option_clicked(self, row, col):
        def clicked():
            new_tile = self.game.new_tile
            
            # Get image and information
            file        = copy.deepcopy(new_tile.file)
            tile_idx    = copy.deepcopy(new_tile.index)
            tile_letter = copy.deepcopy(new_tile.letter)
            rotation    = copy.deepcopy(new_tile.rotation)
            
            # Place tile
            self.Place_tile(file, tile_idx, tile_letter, row, col, rotation)
            # print(self.game.board_tiles[row][col], self.game.board_tiles[row][col].file)
            # self.game.board_tiles[row][col].rotate(rotation)
            
            # Reset new tile
            if self.lobby_key == 'test2':
                file = r'..\Images\tile_logo.png'
            else: # call from lobby
                file = r'.\Images\tile_logo.png'
            new_tile.reset(file)
            # self.New_tile(1)
            
            # Clear old options
            for option in self.game.options:
                opt_row, opt_col = option
                tile = self.game.board_tiles[opt_row][opt_col]
                tile.disable()
                tile.set_tile(None, None, None, self.game)
        return clicked
        
    def Rotate_deprecated(self, angle, visual=True):
        def rotate():
            new_tile = self.game.new_tile
            new_tile.rotation += angle
            
            pixmap = new_tile.pixmap
            material_data = new_tile.material_data
            
            # Pixmap
            if visual == True:
                pixmap_new = pixmap.transformed(QtG.QTransform().rotate(new_tile.rotation), QtC.Qt.TransformationMode.FastTransformation)
                new_tile.setPixmap(pixmap_new)
            
            # Material data
            material_data_new = dict()
            for material in material_data.keys():
                material_data_new[material] = list()
                for row in range(len(material_data[material])):
                    new_row = []
                    for col in range(len(material_data[material])):
                        if angle == -90: # for left hand rotation
                            new_row += [material_data[material][col][len(material_data[material])-1-row]]
                        elif angle == 90: # for right hand rotation
                            new_row += [material_data[material][len(material_data[material])-1-col][row]]
                    material_data_new[material] += [new_row]
                    
            new_tile.material_data = material_data_new
            self.Show_options(new_tile.index, new_tile.letter)
        
        # Only allow rotations if a tile is shown
        if self.lobby_key == 'test2':
            file = r'..\Images\tile_logo.png'
        else: # call from lobby
            file = r'.\Images\tile_logo.png'
            
        if self.game.new_tile.pixmap != QtG.QPixmap(file):
            return rotate

    def Choose_tile(self, tile_idx=None, tile_letter=None):
        # Choose new tile
        if tile_idx == None and tile_letter == None:
            # New idx and letter
            tile_idx    = rnd.choice(list(self.game.tiles.keys()))
            tile_letter = rnd.choice(list(self.game.tiles[tile_idx].keys()))
        elif tile_idx != None and tile_letter == None: # if only expansion is given (e.g. for river building)
            # Only new letter
            tile_letter = rnd.choice(list(self.game.tiles[tile_idx].keys()))
            
        # Get expansion title
        tile_title  = prop_s.tile_titles[tile_idx-1]
        
        # Get tile folder
        if self.lobby_key == 'test2':
            path = f'..\\Images\\{tile_title}\\{tile_idx}{tile_letter}'
        else: # call from lobby
            path = f'.\\Images\\{tile_title}\\{tile_idx}{tile_letter}'
        
        # Choose a random design
        number_of_pngs = len([name for name in os.listdir(path) if os.path.isfile(os.path.join(path, name))])-1
        number = rnd.choice(range(number_of_pngs))
        
        # Get file
        file = path+f'\\{number}.png'
        
        return tile_idx, tile_letter, file
    
    def Tile_options(self, tile_idx, tile_letter):
        '''Find all options a tile to be placed. Includes rotation!'''
        #FIXME: function is currently not finding all proper options.
        new_tile_material_data = self.game.new_tile.material_data
        
        # Find all empty neighbour tiles
        neighbour_tiles = set()
        for row in self.game.board_tiles.keys():
            for col in self.game.board_tiles[row].keys():
                tile = self.game.board_tiles[row][col]
                # Add all tiles that are not empty
                if len(tile.material_data) != 0:
                    
                    # Check if neighbours are free: north, east, south, west
                    for idx, (row_n, col_n) in enumerate([(-1, 0), (0, 1), (1, 0), (0, -1)]):
                        try:
                            neighbour = self.game.board_tiles[row_n][col_n]
                            if len(neighbour.material_data) == 0:
                                raise Exception() # square is empty: check edges!
                        except:
                            # If neighbour tile doesn't exist or has no material data, it is a possibility
                            # Check if the materials along the edge corresponds
                            neighbour_tiles.add((row_n, col_n))
                            for material in new_tile_material_data.keys():
                                new = new_tile_material_data[material]
                                pixels = len(new)-1
                                
                                # only check for this material if it is present on the edges
                                edge_sum = sum(new[0]) # first row
                                edge_sum += sum(new[pixels]) # last row
                                edge_sum += sum([new[x][0] for x in range(len(new))]) # first column
                                edge_sum += sum([new[x][pixels] for x in range(len(new))]) # last column
                                
                                try:
                                    if edge_sum == 0: # material is not on edges: ignore
                                        raise Exception('Material is not on edges')
                                    
                                    old = tile.material_data[material]
                                    for pixel in range(1, pixels-1): # skip corners
                                        if idx == 0: # new tile is north
                                            material_new = new[pixels][pixel] # south
                                            material_old = old[0][pixel] # north
                                        elif idx == 1: # new tile is east
                                            material_new = new[pixel][0] # west
                                            material_old = old[pixel][pixels] # east
                                        elif idx == 2: # new tile is south
                                            material_new = new[0][pixel] # north
                                            material_old = old[pixels][pixel] # south
                                        elif idx == 3: # new tile is west
                                            material_new = new[pixel][pixels] # east
                                            material_old = old[pixel][0] # west
                                        if (bool(material_new > 0) != bool(material_old > 0)): # either both true or both false is okay
                                            raise Exception(f'material {material} ~ {material_new}.{material_old}, {pixel}')
                                        # else:
                                        #     print(f'good: {material_new} {material_old}')
                                except Exception as e:
                                    # print(f'Error: {e}')
                                    # Material is not the same, discard possibility
                                    neighbour_tiles.remove((row_n, col_n))
                                    break
        return neighbour_tiles # type set
    
    def Place_tile(self, file, tile_idx, tile_letter, row, col, rotation=0):
        # # Add new row if necessary
        # if row < self.game.board_rows[0]:
        #     self._Board_new_row_above()
        # elif row > self.game.board_rows[1]:
        #     self._Board_new_row_below()
        
        # # Add new col if necessary
        # if col < self.game.board_cols[0]:
        #     self._Board_new_col_left()
        # elif col > self.game.board_cols[1]:
        #     self._Board_new_col_right()
        
        # Place tile
        board_tile = self.game.board_tiles[row][col]
        board_tile.set_tile(file, tile_idx, tile_letter, self.game)
        
        board_tile.rotating = True
        import numpy
        rotations = int(numpy.floor(rotation/90))
        print(rotations)
        if rotations < 0:
            for idx in range(-rotations):
                board_tile.rotate(-90)
        elif rotations > 0:
            for idx in range(rotations):
                board_tile.rotate(90)
        # board_tile.rotate(rotation)
        print('rotated,', board_tile.rotation)
        board_tile.rotating = False
        # self.game.board_tiles[row][col].rotate(rotation)
        
        self.game.board_widget.setLayout(self.game.board_base)
        self.game.new_tile.disable()
            
        self.game.lobby.send_feed_message(event          = 'placed_tile',
                                          tile_idx       = tile_idx,
                                          tile_letter    = tile_letter,
                                          row = row, col = col)
        
        # Add new row if necessary
        if row < self.game.board_rows[0]:
            self._Board_new_row_above()
            print('new row above')
        elif row > self.game.board_rows[1]:
            self._Board_new_row_below()
            print('new row below')
        
        # Add new col if necessary
        if col < self.game.board_cols[0]:
            self._Board_new_col_left()
            print('new column left')
        elif col > self.game.board_cols[1]:
            self._Board_new_col_right()
            print('new column right')
    
    def _New_tile(self, row, col):
        if self.lobby_key == 'test2':
            file = '..\\Images\\Coin_icon.png'
        else: # call from lobby
            file = '.\\Images\\Coin_icon.png'
            
        empty_tile = QtE.Tile(file, prop_s.tile_size, self.game)
        self.game.board_tiles[row][col] = empty_tile
        return empty_tile
    
    def Board_init(self):
        '''
        board_base  : the core QVBoxLayout
        board       : all QHBoxLayouts
        board_tiles : all references to tile widgets
        '''
        self.game.board = dict()
        self.game.board_tiles = dict()
        self.game.board_rows = [1,0]
        self.game.board_cols = [0,0]
        
        # Initial layout
        self.game.board_base.addStretch(1)
        self._Board_new_row_above()
        self._Board_new_row_above()
        self._Board_new_row_below()
        self.game.board_base.addStretch(1)
    
    def _Board_new_row_above(self):
        self.__Board_new_row(1)
    
    def _Board_new_row_below(self):
        self.__Board_new_row(-2)
        
    def __Board_new_row(self, place):
        if place == 1: # above
            new_row_idx = self.game.board_rows[0]-1
            insert_idx = 1
            self.game.board_rows[0] -= 1
        elif place == -2: # below
            new_row_idx = self.game.board_rows[1]+1
            insert_idx = new_row_idx+1-self.game.board_rows[0]
            self.game.board_rows[1] += 1
        
        # Make new row index available
        self.game.board_tiles[new_row_idx] = dict()
            
        # Empty row
        new_row = self.game.board[new_row_idx] = QtW.QHBoxLayout()
        new_row.setSpacing(prop_s.tile_spacing)
        new_row.setSizeConstraint(QtW.QLayout.SizeConstraint.SetFixedSize)
        
        # Fill row with necessary empty tiles
        new_row.addStretch(0)
        for col_idx in range(self.game.board_cols[0]-1, self.game.board_cols[1]+2):
            new_row.addWidget(self._New_tile(new_row_idx, col_idx))
        new_row.addStretch(0)
        
        # Add row to vertical base
        self.game.board_base.insertLayout(insert_idx, new_row)
    
    def _Board_new_col_left(self):
        self.__Board_new_col(1)
    
    def _Board_new_col_right(self):
        self.__Board_new_col(-2)
        
    def __Board_new_col(self, place):
        if place == 1: # left
            new_col_idx = self.game.board_cols[0]-1
            insert_idx = 1
            self.game.board_cols[0] -= 1
        elif place == -2: # right
            new_col_idx = self.game.board_cols[1]+1
            insert_idx = new_col_idx+1+2-self.game.board_cols[0]
            self.game.board_cols[1] += 1
        
        # Add column to each row
        try:
            for row_idx in range(self.game.board_cols[0]-1, self.game.board_cols[1]+2-1):
                row = self.game.board[row_idx]
                row.insertWidget(insert_idx, self._New_tile(row_idx, new_col_idx))
        except Exception as e:
            None