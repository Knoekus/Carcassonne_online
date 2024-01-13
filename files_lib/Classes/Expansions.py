import PyQt6.QtGui     as QtG
import PyQt6.QtWidgets as QtW
import PyQt6.QtCore    as QtC
import PyQt6_Extra     as QtE

import string
import sys

class Expansions():
    def __init__(self, game):
        self.game = game
        self.lobby_key = game.lobby.lobby_key
        
        self.expansions = self.game.expansions
        if self.expansions[r'The Abbot'] == 1:
            self._Exp_The_Abbot()
        if self.expansions[r'The River'] == 1:
            self._Exp_The_River()
        if self.expansions[r'Inns && Cathedrals'] == 1:
            self._Exp_Inns_Cathedrals()
        
        self.game.Tiles.Update_tiles_left_label()
    
    def _Exp_The_Abbot(self):
        #%% Add abbot meeple to inventory
        tile_size = 50
        if self.lobby_key == 'test2':
            file = r'..\Images\Meeples\Blue\AB.png'
        else: # call from lobby
            file = r'.\Images\Meeples\Blue\AB.png'
        pixmap = QtE.GreenScreenPixmap(file)
        
        row, col = self._Find_empty_cell(self.game.inventory, cols=3)
        self.game.meeples_abbot = QtE.ClickableImage(pixmap, tile_size, tile_size)
        self.game.inventory.addWidget(self.game.meeples_abbot, row, col, alignment=QtC.Qt.AlignmentFlag.AlignCenter)
        
        #%% Tiles
        numbers = [1 for x in range(8)]
        self.game.Tiles.Add_tiles(4, numbers)
        
        #%% Game properties
        self.game.materials += ['garden']
        self.game.meeple_types += ['abbot']
        #%%
    
    def _Exp_The_River(self):
        #%% Tiles
        numbers = [1 for x in range(12)]
        self.game.Tiles.Add_tiles(2, numbers)
        
        #%% Game properties
        self.game.materials += ['water']
        #%%
    
    def _Exp_Inns_Cathedrals(self):
        #%% Add big meeple to inventory
        tile_size = 50
        if self.lobby_key == 'test2':
            file = r'..\Images\Meeples\Blue\BF.png'
        else: # call from lobby
            file = r'.\Images\Meeples\Blue\BF.png'
        pixmap = QtE.GreenScreenPixmap(file)
        
        row, col = self._Find_empty_cell(self.game.inventory, cols=3)
        self.game.meeples_big = QtE.ClickableImage(pixmap, tile_size, tile_size)
        self.game.inventory.addWidget(self.game.meeples_big, row, col, alignment=QtC.Qt.AlignmentFlag.AlignCenter)
        
        #%% Tiles
        numbers = [1 for x in range(10)] + [2] + [1 for x in range(6)]
        self.game.Tiles.Add_tiles(3, numbers)
        
        #%% Game properties
        self.game.materials += ['cathedral', 'inn']
        self.game.meeple_types += ['big']
        #%%
    
    def _Find_empty_cell(self, grid, rows=int(1e6), cols=int(1e6)):
        '''
        Finds the row and column index of the first empty cell in a QGridLayout.
        
        Returns
        -------
        row, col : (int, int)
        '''
        row, col = 0, 0
        flag = False
        for row in range(rows):
            for col in range(cols):
                cell = grid.itemAtPosition(row, col)
                if cell == None: # found empty cell
                    flag = True
                    break
            if flag == True: break
        if flag == True:
            return row, col
        else:
            raise Warning('Could not find an empty cell in a 1-million square layout. You have a big layout.')
            return None