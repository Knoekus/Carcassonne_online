#%% Imports
# PyQt6
import PyQt6.QtCore    as QtC
import PyQt6.QtGui     as QtG
import PyQt6.QtWidgets as QtW
import PyQt6_Extra     as QtE

# Custom classes
# import Classes.Animations as Animations
import tile_data

# Other packages
import copy
import os
import random as rnd
import string

#%% Tiles class
class Tiles():
    def __init__(self, Carcassonne):
        self.Carcassonne = Carcassonne
        self.game_vis = self.Carcassonne.game_vis
        
        self.Carcassonne.options = set()
        self.Carcassonne.tiles = dict()
        self.Carcassonne.last_placed_tile = None
        
        self.Board_init()
    
    def Add_tiles(self, prefix, numbers):
        self.Carcassonne.tiles[prefix] = dict()
        for idx, number in enumerate(numbers):
            letter = string.ascii_uppercase[idx]
            self.Carcassonne.tiles[prefix][letter] = number
    
    #%% New tile placement
    def Update_tiles_left_label(self):
        self.game_vis.tiles_left = sum([sum(expansion.values()) for expansion in self.Carcassonne.tiles.values()])
        self.game_vis.tiles_left_label.setText(f'{self.game_vis.tiles_left} tiles left.')
    
    def New_tile(self, tile_idx_in=None, tile_letter_in=None):
        '''Find a new tile that is placable on the current board. Place that tile in the new_tile position.'''
        self.game_vis.button_end_turn.setEnabled(0) # FIXME: should be unnecessary and done when turn ends
        self.game_vis._Meeples_enable(False) # FIXME: should be unnecessary and done when turn ends
        self.game_vis.new_tile.rotation = 0 # start a new tile with 0 rotation # FIXME: should be unnecessary and done when turn ends
        
        # Get a new tile
        while True:
            tile_idx, tile_letter, file = self.Choose_tile(tile_idx_in, tile_letter_in)
            # Give new tile the material data
            self.game_vis.new_tile.material_data = tile_data.tiles[tile_idx][tile_letter]
            
            # Allow tile if there are options to place it
            options = set()
            for idx in range(4): # try each orientation
                options |= self.Tile_options(tile_idx, tile_letter)
                if len(options) > 0: 
                    # if options are found before trying all rotations, don't try the rest and rotate back
                    for idx2 in range(idx):
                        self.game_vis.new_tile.rotate(-90)
                    break
                else:
                    self.game_vis.new_tile.rotate(90)
            if len(options) > 0:
                break
            elif True:
                print(f'\n{tile_idx}{tile_letter} is infeasible\n')
                # raise Exception('stop')
        
        # Make feed event
        self.Carcassonne.game_func._Feed_send_tile_taken(file, tile_idx, tile_letter)
    
    def Choose_tile(self, tile_idx=None, tile_letter=None):
        '''Choose a tile from the pile, and get its information.'''
        # Choose new tile
        if tile_idx == None and tile_letter == None:
            # New idx and letter
            tile_idx    = rnd.choice(list(self.Carcassonne.tiles.keys()))
            tile_letter = rnd.choice(list(self.Carcassonne.tiles[tile_idx].keys()))
        elif tile_idx != None and tile_letter == None: # if only expansion is given (e.g. for river building)
            # Only new letter
            tile_letter = rnd.choice(list(self.Carcassonne.tiles[tile_idx].keys()))
            
        # Get expansion title
        tile_title = self.Carcassonne.Properties.tile_titles[tile_idx-1]
        
        # Get tile folder
        path = f'.\\Images\\{tile_title}\\{tile_idx}{tile_letter}'
        
        # Choose a random design
        number_of_pngs = len([name for name in os.listdir(path) if os.path.isfile(os.path.join(path, name))])-1
        number = rnd.choice(range(number_of_pngs))
        
        # Get file
        file = path+f'\\{number}.png'
        
        return tile_idx, tile_letter, file
    
    def Option_clicked(self, row, col):
        def clicked():
            new_tile = self.game_vis.new_tile
            
            # Get image and information
            file        = copy.deepcopy(new_tile.file)
            tile_idx    = copy.deepcopy(new_tile.index)
            tile_letter = copy.deepcopy(new_tile.letter)
            rotation    = copy.deepcopy(new_tile.rotation)
            
            # Place tile and reset new tile
            self.Carcassonne.game_func._Feed_send_tile_placed(row, col, file, tile_idx, tile_letter, rotation)
            self.Carcassonne.options.remove((row, col))
            
            # Clear old options
            for option in self.Carcassonne.options:
                opt_row, opt_col = option
                tile = self.Carcassonne.board_tiles[opt_row][opt_col]
                tile.disable()
                # tile.set_tile(None, None, None, self.Carcassonne.materials)
                tile.set_tile(None, None, None)
            
            # Enable/disable 'end turn' button and meeples
            # if self.Carcassonne.username == self.Carcassonne.current_player:
            #     self.Carcassonne.button_end_turn.setEnabled(1)
            # else:
            #     self.Carcassonne.button_end_turn.setEnabled(0) # FIXME: should never occur since this function can only run if current player is yourself
            # Meeples.En_dis_able_meeples(self.game, enable=True)
            
            # self.game_vis.button_end_turn.setEnabled(True)
            # self.game_vis._Meeples_enable(True)
        return clicked
    
    #%% Options
    def Show_options(self):
        tile_idx, tile_letter = self.game_vis.new_tile.index, self.game_vis.new_tile.letter
        
        # Clear old options
        for option in self.Carcassonne.options:
            row, col = option
            tile = self.Carcassonne.board_tiles[row][col]
            tile.disable()
            tile.set_tile(None, None, None)
        
        # Get new options
        self.Carcassonne.options = self.Tile_options(tile_idx, tile_letter)
        
        # Get image
        file = '.\\Images\\tile_available'
        
        # Set options' images
        for option in self.Carcassonne.options:
            row, col = option
            tile = self.Carcassonne.board_tiles[row][col]
            tile.enable()
            # tile.set_tile(file, None, None, self.Carcassonne.materials)
            tile.set_tile(file, None, None)
            try: tile.clicked.disconnect()
            except: None
            tile.clicked.connect(self.Option_clicked(row, col))

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
        for row in range(self.Carcassonne.board_rows[0], self.Carcassonne.board_rows[1]+1):
            for col in range(self.Carcassonne.board_cols[0], self.Carcassonne.board_cols[1]+1):
                tile = self.Carcassonne.board_tiles[row][col]
                
                # Find all empty neighbours
                if len(tile.material_data) > 0: # if tile not empty
                    neighbours = [(row-1, col), (row, col+1), (row+1, col), (row, col-1)]
                    for pos, coords in enumerate(neighbours):
                        neighbour_tile = self.Carcassonne.board_tiles[coords[0]][coords[1]]
                        
                        # Check empty neighbour for feasibility
                        if (len(neighbour_tile.material_data) == 0) and (coords not in options_deleted): # if tile empty
                            data_n_all = self.game_vis.new_tile.material_data
                            data_t_all = tile.material_data
                            
                            options.add(coords)
                            # Check all materials
                            for material in self.Carcassonne.materials:
                                # Ignore material if it's not in either tile
                                if (material not in data_n_all.keys()) and (material not in data_t_all.keys()):
                                    continue
                                
                                # Material is in both tiles
                                elif (material in data_n_all.keys()) and (material in data_t_all.keys()):
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
                                elif (material in data_n_all.keys()) and (material not in data_t_all.keys()):
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
                                elif (material not in data_n_all.keys()) and (material in data_t_all.keys()):
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
    
    #%% Board
    def Board_init(self):
        '''
        board_base  : the core QVBoxLayout
        board       : all QHBoxLayouts
        board_tiles : all references to tile widgets
        '''
        self.Carcassonne.board = dict()
        self.Carcassonne.board_tiles = dict()
        self.Carcassonne.board_rows = [0,0]
        self.Carcassonne.board_cols = [0,0]
        
        # Initial layout
        self.game_vis.board_base.addStretch(1)
        self.Carcassonne.board_tiles[-1] = dict()
        self.__Board_new_row(-1, -1)
        self.Carcassonne.board_tiles[ 0] = dict()
        self.__Board_new_row( 0, -1)
        self.Carcassonne.board_tiles[ 1] = dict()
        self.__Board_new_row( 1, -1)
        self.game_vis.board_base.addStretch(1)
        
        # Set board to ScrollArea widget
        self.game_vis.board_widget.setLayout(self.game_vis.board_base)
    
    def _Board_new_row_above(self):
        self.Carcassonne.board_rows[0] -= 1
        new_row_idx = self.Carcassonne.board_rows[0]-1
        insert_idx = 1
        self.__Board_new_row(new_row_idx, insert_idx)
    
    def _Board_new_row_below(self):
        self.Carcassonne.board_rows[1] += 1
        new_row_idx = self.Carcassonne.board_rows[1]+1
        insert_idx = len(self.game_vis.board_base)-1
        self.__Board_new_row(new_row_idx, insert_idx)
    
    def __Board_new_row(self, new_row_idx, insert_idx):
        # Make new row index available
        self.Carcassonne.board_tiles[new_row_idx] = dict()
        
        # Empty row
        new_row = self.Carcassonne.board[new_row_idx] = QtW.QHBoxLayout()
        new_row.setSpacing(self.Carcassonne.Properties.tile_spacing)
        new_row.setSizeConstraint(QtW.QLayout.SizeConstraint.SetFixedSize)
        
        # Fill row with necessary empty tiles
        new_row.addStretch(0)
        for col_idx in range(self.Carcassonne.board_cols[0]-1, self.Carcassonne.board_cols[1]+2):
            new_row.addWidget(self._New_tile(new_row_idx, col_idx))
        new_row.addStretch(0)
        
        # Add row to vertical base
        self.game_vis.board_base.insertLayout(insert_idx, new_row)
        # print(f'Added row {new_row_idx} at {insert_idx}')
    
    def _Board_new_col_left(self):
        # self.__Board_new_col(1)
        self.Carcassonne.board_cols[0] -= 1
        new_col_idx = self.Carcassonne.board_cols[0]-1
        insert_idx = 1
        self.__Board_new_col(new_col_idx, insert_idx)
    
    def _Board_new_col_right(self):
        # self.__Board_new_col(-2)
        self.Carcassonne.board_cols[1] += 1
        new_col_idx = self.Carcassonne.board_cols[1]+1
        insert_idx = len(self.Carcassonne.board[0])-1
        self.__Board_new_col(new_col_idx, insert_idx)
        
    def __Board_new_col(self, new_col_idx, insert_idx):
        # In each row add a column
        for row_idx in range(self.Carcassonne.board_rows[0]-1, self.Carcassonne.board_rows[1]+2):
            row = self.Carcassonne.board[row_idx]
            row.insertWidget(insert_idx, self._New_tile(row_idx, new_col_idx))
        # print(f'Added col {new_col_idx} at {insert_idx}')
    
    def _New_tile(self, row, col):
        # if self.lobby_key == 'test2':
        #     file = '..\\Images\\Coin_icon.png'
        # else: # call from lobby
        #     file = '.\\Images\\Coin_icon.png'
        file = None
        size = self.Carcassonne.Properties.tile_size * 320 # 320 is the current px size for tiles
        empty_tile = QtE.Tile(file, size, self.Carcassonne)
        self.Carcassonne.board_tiles[row][col] = empty_tile
        return empty_tile
    
def Board_tile_coords(tile, board):
    """Find coordinates of tile in board."""
    for row in board.keys():
        row_layout = board[row]
        tile_count = row_layout.count()
        for col in range(tile_count-1):
            if row_layout.itemAt(col).widget() == tile:
                return row, col