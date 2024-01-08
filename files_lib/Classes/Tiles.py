import PyQt6.QtGui     as QtG
import PyQt6.QtWidgets as QtW
import PyQt6.QtCore    as QtC
import PyQt6_Extra     as QtE
import string
import prop_s
import tile_data

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
                options |= self.Tile_options(tile_idx, tile_letter)
                if len(options) > 0: 
                    # if options are found before trying all rotations, don't try the rest and rotate back
                    for idx2 in range(idx):
                        self.game.new_tile.rotate(-90)
                    break
                else:
                    # self.game.new_tile.clicked_l.emit()
                    self.game.new_tile.rotate(90)
            if len(options) > 0:
                # self.game.new_tile.rotation = 0 # reset rotation
                break
            elif True:
                print(f'\n{tile_idx}{tile_letter} is infeasible\n')
        
        # Update tiles left
        self.game.new_tile_anim.swap_image(file, tile_idx, tile_letter, 500) # replaces set_tile, maybe relocate to QtE
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
            self.game.options.remove((row, col))
            # self.game.board_tiles[row][col].rotate(rotation)
            
            # Reset new tile
            if self.lobby_key == 'test2':
                file = r'..\Images\tile_logo.png'
            else: # call from lobby
                file = r'.\Images\tile_logo.png'
            new_tile.reset(file)
            
            # Clear old options
            for option in self.game.options:
                opt_row, opt_col = option
                tile = self.game.board_tiles[opt_row][opt_col]
                tile.disable()
                tile.set_tile(None, None, None, self.game)
            
            # Test purposes
            self.New_tile(1)
        return clicked

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
        """Find all empty neighbour tiles where the new tile can be placed."""
        def get_edge(data, pos:str):
            if pos == 'N': # north
                edge = data[0][1:-1]
            elif pos == 'E': # east
                edge = [data[x][-1] for x in range(len(data))][1:-1]
            elif pos == 'S': # south
                edge = data[-1][1:-1]
            elif pos == 'W': # west
                edge = [data[x][0] for x in range(len(data))][1:-1]
            elif pos == 'all': # all edges
                edge = get_edge(data, 'N') + get_edge(data, 'E') + get_edge(data, 'S') + get_edge(data, 'W')
            else:
                raise Exception("Unknown position of tile.")
            # convert to booleans to only consider yes/no material, not number of material patch
            return [bool(x) for x in edge]
        
        options = set()
        options_deleted = set()
        # Find all tiles in the board
        for row in range(self.game.board_rows[0], self.game.board_rows[1]+1):
            for col in range(self.game.board_cols[0], self.game.board_cols[1]+1):
                tile = self.game.board_tiles[row][col]
                
                # Find all empty neighbours
                if len(tile.material_data) > 0: # if tile not empty
                    neighbours = [(row-1, col), (row, col+1), (row+1, col), (row, col-1)]
                    for pos, coords in enumerate(neighbours):
                        neighbour_tile = self.game.board_tiles[coords[0]][coords[1]]
                        
                        # Check empty neighbour for feasibility
                        if len(neighbour_tile.material_data) == 0 and coords not in options_deleted: # if tile empty
                            data_n_all = self.game.new_tile.material_data
                            data_t_all = tile.material_data
                            
                            options.add(coords)
                            # Check all materials
                            for material in self.game.materials:
                                # Ignore material if it's not in either tile
                                if material not in data_n_all.keys() and material not in data_t_all.keys():
                                    continue
                                
                                # Material is in both tiles
                                elif material in data_n_all.keys() and material in data_t_all.keys():
                                    data_n = data_n_all[material]
                                    data_t = data_t_all[material]
                                    if pos == 0: # north
                                        # south of neighbour should match north of tile
                                        edge_n = get_edge(data_n, 'S')
                                        edge_t = get_edge(data_t, 'N')
                                    elif pos == 1: # east
                                        # west of neighbour should match east of tile
                                        edge_n = get_edge(data_n, 'W')
                                        edge_t = get_edge(data_t, 'E')
                                    elif pos == 2: # south
                                        # north of neighbour should match south of tile
                                        edge_n = get_edge(data_n, 'N')
                                        edge_t = get_edge(data_t, 'S')
                                    elif pos == 3: # west
                                        # east of neighbour should match west of tile
                                        edge_n = get_edge(data_n, 'E')
                                        edge_t = get_edge(data_t, 'W')
                                    else:
                                        raise Exception("Unknown position of tile.")
                                    if edge_n != edge_t:
                                        # print(f'   {material} does not match {coords}: \n     {[int(x) for x in edge_n]}\n     {[int(x) for x in edge_t]}')
                                        options.remove(coords)
                                        options_deleted.add(coords)
                                        break # stop trying materials
                                
                                # Material is only in new tile
                                elif material in data_n_all.keys():
                                    data_n = data_n_all[material]
                                    if pos == 0: # north
                                        # south of neighbour should match north of tile
                                        edge_n = get_edge(data_n, 'S')
                                    elif pos == 1: # east
                                        # west of neighbour should match east of tile
                                        edge_n = get_edge(data_n, 'W')
                                    elif pos == 2: # south
                                        # north of neighbour should match south of tile
                                        edge_n = get_edge(data_n, 'N')
                                    elif pos == 3: # west
                                        # east of neighbour should match west of tile
                                        edge_n = get_edge(data_n, 'E')
                                    else:
                                        raise Exception("Unknown position of tile.")
                                        
                                    if sum(edge_n) > 0:
                                        # Remove option if unique material is on edge of importance
                                        # print(f'   {material} is unique in NEW and does not match {coords}')
                                        options.remove(coords)
                                        options_deleted.add(coords)
                                        break # stop trying materials
                                
                                # Material is only in old tile
                                elif material in data_t_all.keys():
                                    data_t = data_t_all[material]
                                    if pos == 0: # north
                                        # south of neighbour should match north of tile
                                        edge_t = get_edge(data_t, 'N')
                                    elif pos == 1: # east
                                        # west of neighbour should match east of tile
                                        edge_t = get_edge(data_t, 'E')
                                    elif pos == 2: # south
                                        # north of neighbour should match south of tile
                                        edge_t = get_edge(data_t, 'S')
                                    elif pos == 3: # west
                                        # east of neighbour should match west of tile
                                        edge_t = get_edge(data_t, 'W')
                                    else:
                                        raise Exception("Unknown position of tile.")
                                        
                                    if sum(edge_t) > 0:
                                        # Remove option if unique material is on edge of importance
                                        # print(f'   {material} is unique in TILE and does not match {coords}')
                                        options.remove(coords)
                                        options_deleted.add(coords)
                                        break # stop trying materials
        return options
    
    def Place_tile(self, file, tile_idx, tile_letter, row, col, rotation=0):
        # Add new row if necessary
        if row < self.game.board_rows[0]:
            self._Board_new_row_above()
        elif row > self.game.board_rows[1]:
            self._Board_new_row_below()
        
        # Add new col if necessary
        if col < self.game.board_cols[0]:
            self._Board_new_col_left()
        elif col > self.game.board_cols[1]:
            self._Board_new_col_right()
            
        # Place tile
        board_tile = self.game.board_tiles[row][col]
        board_tile.set_tile(file, tile_idx, tile_letter, self.game)
        self.game.new_tile.disable()
        
        # Rotating
        board_tile.rotating = True
        import numpy
        rotations = int(numpy.floor(rotation/90))
        if rotations < 0:
            for idx in range(-rotations):
                board_tile.rotate(-90)
        elif rotations > 0:
            for idx in range(rotations):
                board_tile.rotate(90)
        board_tile.rotating = False
            
        # Push message to event log
        self.game.lobby.send_feed_message(event          = 'placed_tile',
                                          tile_idx       = tile_idx,
                                          tile_letter    = tile_letter,
                                          row = row, col = col)
    
    def _New_tile(self, row, col):
        # if self.lobby_key == 'test2':
        #     file = '..\\Images\\Coin_icon.png'
        # else: # call from lobby
        #     file = '.\\Images\\Coin_icon.png'
        file = None
        
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
        self.game.board_rows = [0,0]
        self.game.board_cols = [0,0]
        
        # Initial layout
        self.game.board_base.addStretch(1)
        self.game.board_tiles[-1] = dict()
        self.__Board_new_row(-1, -1)
        self.game.board_tiles[ 0] = dict()
        self.__Board_new_row( 0, -1)
        self.game.board_tiles[ 1] = dict()
        self.__Board_new_row( 1, -1)
        self.game.board_base.addStretch(1)
        
        # Set board to ScrollArea widget
        self.game.board_widget.setLayout(self.game.board_base)
    
    def _Board_new_row_above(self):
        self.game.board_rows[0] -= 1
        new_row_idx = self.game.board_rows[0]-1
        insert_idx = 1
        self.__Board_new_row(new_row_idx, insert_idx)
    
    def _Board_new_row_below(self):
        self.game.board_rows[1] += 1
        new_row_idx = self.game.board_rows[1]+1
        insert_idx = len(self.game.board_base)-1
        self.__Board_new_row(new_row_idx, insert_idx)
    
    def __Board_new_row(self, new_row_idx, insert_idx):
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
        # print(f'Added row {new_row_idx} at {insert_idx}')
    
    def _Board_new_col_left(self):
        # self.__Board_new_col(1)
        self.game.board_cols[0] -= 1
        new_col_idx = self.game.board_cols[0]-1
        insert_idx = 1
        self.__Board_new_col(new_col_idx, insert_idx)
    
    def _Board_new_col_right(self):
        # self.__Board_new_col(-2)
        self.game.board_cols[1] += 1
        new_col_idx = self.game.board_cols[1]+1
        insert_idx = len(self.game.board[0])-1
        self.__Board_new_col(new_col_idx, insert_idx)
        
    def __Board_new_col(self, new_col_idx, insert_idx):
        # In each row add a column
        for row_idx in range(self.game.board_rows[0]-1, self.game.board_rows[1]+2):
            row = self.game.board[row_idx]
            row.insertWidget(insert_idx, self._New_tile(row_idx, new_col_idx))
        # print(f'Added col {new_col_idx} at {insert_idx}')