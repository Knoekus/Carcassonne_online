import PyQt6.QtGui     as QtG
import PyQt6.QtWidgets as QtW
import PyQt6.QtCore    as QtC
import PyQt6_Extra     as QtE
import string
import prop_s

import os
import random as rnd


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
    
    def New_tile(self, tile_idx=None, tile_letter=None):
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
        
        # Update tiles left
        self.Update_tiles_left_label()
    
        return tile_idx, tile_letter, file
    
    def Place_tile(self, file, tile_idx, tile_letter, row, col):
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
        self.game.board_tiles[row][col].set_tile(file, tile_idx, tile_letter, self.game)
        self.game.board_widget.setLayout(self.game.board_base)
        
        # Update tiles left
        if self.game.tiles[tile_idx][tile_letter] > 1:
            self.game.tiles[tile_idx][tile_letter] -= 1 # decrease number of tiles by 1
        else:
            if len(self.game.tiles[tile_idx].keys()) > 1:
                self.game.tiles[tile_idx].pop(tile_letter) # delete tile if none left
            else:
                self.game.tiles.pop(tile_idx) # delete expansion if no tiles left
            
        self.game.lobby.send_feed_message(event          = 'placed_tile',
                                          tile_idx       = tile_idx,
                                          tile_letter    = tile_letter,
                                          row = row, col = col)
    
    def _New_tile(self, row, col):
        empty_tile = QtE.Tile(None, prop_s.tile_size)
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
        for col_idx in range(self.game.board_cols[0], self.game.board_cols[1]+1):
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
            insert_idx = new_col_idx+1-self.game.board_cols[0]
            self.game.board_cols[1] += 1
        
        # Add column to each row
        for row_idx in range(self.game.board_rows[0], self.game.board_rows[1]+1):
            row = self.game.board[row_idx]
            row.insertWidget(insert_idx, self._New_tile(row_idx, new_col_idx))