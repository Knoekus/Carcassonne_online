import PyQt6.QtGui     as QtG
import PyQt6.QtWidgets as QtW
import PyQt6.QtCore    as QtC
import firebase_admin

import sys
if r"..\..\files_lib" not in sys.path:
    sys.path.append(r"..\..\files_lib")
import PyQt6_Extra     as QtE

class Expansions():
    def __init__(self, game):
        self.game = game
        self.lobby_key = game.lobby.lobby_key
        
        expansions = self.game.Refs('expansions').get()
        if expansions[r'The Abbot'] == 1:
            self._Exp_The_Abbot()
        if expansions[r'The River'] == 1:
            self._Exp_The_River
        if expansions[r'Inns && Cathedrals'] == 1:
            self._Exp_Inns_Cathedrals()
    
    def Find_empty_cell(self, grid, rows=int(1e6), cols=int(1e6)):
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
            return None
    
    def _Exp_The_Abbot(self):
        # Add abbot meeple to inventory
        tile_size = 50
        if self.lobby_key == 'test':
            file = r'..\Images\Meeples\Blue\AB.png'
        else: # call from lobby
            file = r'.\Images\Meeples\Blue\AB.png'
        pixmap = QtE.GreenScreenPixmap(file)
        
        row, col = self.Find_empty_cell(self.game.inventory, cols=3)
        self.game.meeples_abbot = QtE.ClickableImage(pixmap, tile_size, tile_size)
        self.game.inventory.addWidget(self.game.meeples_abbot, row, col, alignment=QtC.Qt.AlignmentFlag.AlignCenter)
    
    def _Exp_The_River(self):
        None
    
    def _Exp_Inns_Cathedrals(self):
        # Add big meeple to inventory
        tile_size = 50
        if self.lobby_key == 'test':
            file = r'..\Images\Meeples\Blue\BF.png'
        else: # call from lobby
            file = r'.\Images\Meeples\Blue\BF.png'
        pixmap = QtE.GreenScreenPixmap(file)
        
        row, col = self.Find_empty_cell(self.game.inventory, cols=3)
        self.game.meeples_big = QtE.ClickableImage(pixmap, tile_size, tile_size)
        self.game.inventory.addWidget(self.game.meeples_big, row, col, alignment=QtC.Qt.AlignmentFlag.AlignCenter)