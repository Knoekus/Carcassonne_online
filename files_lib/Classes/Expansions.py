#%% Imports
# PyQt6
import PyQt6.QtGui     as QtG
import PyQt6.QtWidgets as QtW
import PyQt6.QtCore    as QtC
import PyQt6_Extra     as QtE

# Custom classes
import Classes.Meeples as Meeples

# Other packages
import numpy as np

#%% Expansions class
class Expansions():
    def __init__(self, game):
        self.game = game
        self.lobby_key = game.lobby.lobby_key
        
        self.expansions = self.game.expansions
        if True: # Always include base game
            self._Base_game()
        if r'The River' in self.expansions:
            self._Exp_The_River()
        if r'Inns && Cathedrals' in self.expansions:
            self._Exp_Inns_Cathedrals()
        if r'The Abbot' in self.expansions:
            self._Exp_The_Abbot()
        
        self.game.Tiles.Update_tiles_left_label()
    
    def _Base_game(self):
        # Make standard meeple layout
        self.game_vis.meeples_standard_layout = QtW.QGridLayout()
        self.game_vis.meeples_standard_layout.setHorizontalSpacing(0)
        self.game_vis.meeples_standard_layout.setVerticalSpacing(0)
        
        # Add standard meeples to inventory
        self.game_vis.meeples['standard'] = dict()
        n_cols = self.Carcassonne.standard_meeple_cols
        for idx in range(7):
            meeple = Meeples.Meeple_standard(self.Carcassonne)
            self.game_vis['standard'][idx] = meeple
            self.game_vis.meeples_standard_layout.addWidget(meeple, np.floor((idx)/n_cols).astype(int), idx%n_cols, 1, 1)
        self.game_vis.inventory.addLayout(self.game_vis.meeples_standard_layout, 0, 0, 1, 3)
                
        # Tiles
        numbers = [8, 9, 4, 1, 3, 3, 3, 4, 5, 4, 2, 1, 2, 3, 2, 3, 2, 3, 2, 3, 1, 1, 2, 1]
        self.game.Tiles.Add_tiles(1, numbers)
        self.game.materials += ['city', 'grass', 'monastery', 'grass']
        # self.game.meeple_types += ['standard']
    
    def _Exp_The_River(self):
        # Tiles
        numbers = [1 for x in range(12)]
        self.game.Tiles.Add_tiles(2, numbers)
        self.game.materials += ['water']
    
    def _Exp_Inns_Cathedrals(self):
        # Add big meeple to inventory
        self.game_vis.meeples['big'] = dict()
        for idx in range(1):
            meeple = Meeples.Meeple_big(self.Carcassonne)
            self.game_vis['big'][idx] = meeple
            row, col = self._Find_empty_ìnventory_position(cols=self.Carcassonne.inventory_cols)
            self.game_vis.inventory.addWidget(meeple, row, col, alignment=QtC.Qt.AlignmentFlag.AlignCenter)
        
        # Tiles
        numbers = [1 for x in range(10)] + [2] + [1 for x in range(6)]
        self.game.Tiles.Add_tiles(3, numbers)
        self.game.materials += ['cathedral', 'inn']
        # self.game.meeple_types += ['big']
        
    def _Exp_The_Abbot(self):
        # Add abbot meeple to inventory
        self.game_vis.meeples['abbot'] = dict()
        for idx in range(1):
            meeple = Meeples.Meeple_abbot(self.Carcassonne)
            self.game_vis['abbot'][idx] = meeple
            row, col = self._Find_empty_ìnventory_position(cols=self.Carcassonne.inventory_cols)
            self.game_vis.inventory.addWidget(meeple, row, col, alignment=QtC.Qt.AlignmentFlag.AlignCenter)
        
        # Tiles
        numbers = [1 for x in range(8)]
        self.game.Tiles.Add_tiles(4, numbers)
        self.game.materials += ['garden']
        # self.game.meeple_types += ['abbot']
    
    def _Find_empty_ìnventory_position(self, rows=int(1e6), cols=int(1e6)):
        '''
        Finds the row and column index of the first empty cell in a QGridLayout.
        
        Returns
        -------
        row, col : (int, int)
        '''
        inventory = self.game_vis.inventory
        
        row, col = 0, 0
        flag = False
        for row in range(rows):
            for col in range(cols):
                cell = inventory.itemAtPosition(row, col)
                if cell == None: # found empty cell
                    flag = True
                    break
            if flag == True: break
        if flag == True:
            return row, col
        else:
            raise Warning('Could not find an empty cell in a 1-million square layout. You have a big layout.')
            return None