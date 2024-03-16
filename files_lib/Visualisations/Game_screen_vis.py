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

#%% Game screen visualisation
class Game_screen_vis(QtW.QWidget):
    def __init__(self, Carcassonne):
        super().__init__()
        self.Carcassonne = Carcassonne
    
        self.Window_properties()
        self.Parameters()
        self.Layout()
    
    def Window_properties(self):
        self.Carcassonne.setWindowTitle('Carcassonne Online')
    
    def Parameters(self):
        # Presets
        # ...
        pass
    
    def Layout(self):
        # Layout components
        def _Game_players():
            # Put each player in the row with points indicator
            self.players_grid = QtW.QGridLayout()
            self.players_name_labels = dict()
            self.players_name_anims = dict()
            self.players_points = dict()
            
            # Get player list
            for idx in range(10):
                player_list_dict = self.Carcassonne.Refs('connections').get()
                if type(player_list_dict) == type(dict()):
                    player_list = player_list_dict.keys()
                    break
            else:
                raise Exception('No connections found after 10 tries.')
            
            # Add each player to player list
            for idx, player in enumerate(player_list):
                self.Carcassonne.Refs(f'players/{player}/points').set(0)
                
                player_hbox = QtW.QHBoxLayout()
                colour = QtW.QLabel('', alignment=QtC.Qt.AlignmentFlag.AlignRight)
                colour.setScaledContents(True)
                colour.setFixedSize(25, 25)
                font = self.Carcassonne.Properties.Font(size=1, bold=False)
                colour.setFont(font)
                file = './Images/Colour_indicator.png'
                if self.Carcassonne.lobby_key == 'test2':
                    file = '.'+file
                hex_col = self.Carcassonne.Refs(f'players/{player}/colour').get()
                rgb_col = tuple(int(hex_col[i:i+2], 16) for i in (0, 2, 4, 6))
                col_pixmap = QtE.GreenScreenPixmap(file, (255, 0, 0), rgb_col)
                colour.setPixmap(col_pixmap)
                
                name = QtW.QLabel(f'{player}', alignment=QtC.Qt.AlignmentFlag.AlignCenter)
                font = self.Carcassonne.Properties.Font(size=1, bold=False)
                name.setFont(font)
                
                player_hbox.addWidget(colour, alignment=QtC.Qt.AlignmentFlag.AlignRight)
                player_hbox.addWidget(name, alignment=QtC.Qt.AlignmentFlag.AlignLeft)
                
                points = QtW.QLabel('0', alignment=QtC.Qt.AlignmentFlag.AlignCenter)
                font = self.Carcassonne.Properties.Font(size=1, bold=False)
                points.setFont(font)
                
                self.players_grid.addLayout(player_hbox, 1, idx)
                self.players_grid.addWidget(points,      2, idx)
                
                
                # # Blinking animation
                # if self.lobby.lobby_key == 'test2':
                #     animation = Animations.Animation(name)
                #     animation.add_blinking(1, 0.1, 2500, 200)
                #     self.players_name_anims[player] = animation
                
                # Save references
                self.players_name_labels[player] = name
                self.players_points[player] = points
            
            # Fill in the blank spots, so float all players to left
            # for padding in range(idx, len(prop_s.colours)-1):
            #     players.addWidget(QtW.QLabel(), 1, padding)
                
            return self.players_grid
        
        def _Game_left_column():
            # New tile
            new_tile_size = 200
            # if __name__ == '__main__': # independent call
            #     self.new_tile = QtE.Tile(r'..\Images\tile_logo.png', new_tile_size, game=self, rotating=True)
            # else: # call from lobby
            self.new_tile = QtE.Tile(r'.\Images\tile_logo.png', new_tile_size, game=self, rotating=True)
            
            # self.new_tile_anim = Animations.Animation(self.new_tile)
            # self.new_tile_anim = Animations.New_tile_swap(self, self.new_tile)
            
            # Tiles left
            self.tiles_left = 0
            self.tiles_left_label = QtW.QLabel('... tiles left.', alignment=QtC.Qt.AlignmentFlag.AlignCenter)
            font = self.Carcassonne.Properties.Font(size=0, bold=False)
            self.tiles_left_label.setFont(font)
            
            # Inventory
            self.inventory_label = QtW.QLabel('Inventory', alignment=QtC.Qt.AlignmentFlag.AlignCenter)
            font = self.Carcassonne.Properties.Font(size=2, bold=True)
            self.inventory_label.setFont(font)
            
            #===== Initial inventory =====#
            self.meeples_standard = dict()
            self.meeples_standard_layout = QtW.QGridLayout()
            self.meeples_standard_layout.setHorizontalSpacing(0)
            self.meeples_standard_layout.setVerticalSpacing(0)
            
            # Start with 7 standard meeples
            self.meeple_types = ['meeples_standard']
            for idx in range(7):
                meeple = Meeples.Meeple_standard(self.Carcassonne)
                self.meeples_standard[idx] = meeple
                self.meeples_standard_layout.addWidget(meeple, np.floor((idx)/4).astype(int), idx%4, 1, 1)
            # FIXME: maybe it's more convenient to add these to self.Carcassonne instead.
            # FIXME: when doing that, change self._Meeples_enable accordingly.
            # self.Carcassonne.meeple_types = ['meeples_standard']
            # for idx in range(7):
            #     meeple = Meeples.Meeple_standard(self.Carcassonne)
            #     self.Carcassonne.meeples_standard[idx] = meeple
            #     self.Carcassonne.meeples_standard_layout.addWidget(meeple, np.floor((idx)/4).astype(int), idx%4, 1, 1) # max 4 per row
            
            self.inventory = QtW.QGridLayout()
            self.inventory.addLayout(self.meeples_standard_layout, 0, 0, 1, 3)
            
            # End turn
            self.button_end_turn = QtW.QPushButton('End turn')
            font = self.Carcassonne.Properties.Font(size=2, bold=False)
            self.button_end_turn.setFont(font)
            self.button_end_turn.setEnabled(False)
            
            # Left column
            self.leftColumn = QtW.QVBoxLayout()
            self.leftColumn.addWidget(self.new_tile)
            self.leftColumn.addWidget(self.tiles_left_label)
            self.leftColumn.addWidget(QtE.QHSeparationLine(colour=(80,80,80), height=1))
            self.leftColumn.addWidget(self.inventory_label)
            self.leftColumn.addLayout(self.inventory)
            
            self.leftColumn.addStretch()
            self.leftColumn.addWidget(QtE.QHSeparationLine(colour=(80,80,80), height=10))
            self.leftColumn.addWidget(self.button_end_turn)
            
            return self.leftColumn
        
        def _Game_right_column():
            # Board
            self.board_widget = QtW.QWidget()
            self.board_base = QtW.QVBoxLayout()
            self.board_base.setSpacing(self.Carcassonne.Properties.tile_spacing)
            
            self.board_scroll_area = QtW.QScrollArea()
            self.board_scroll_area.setWidget(self.board_widget)
            self.board_scroll_area.setWidgetResizable(True)
            
            # Right column
            self.rightColumn = QtW.QVBoxLayout()
            self.rightColumn.addWidget(self.board_scroll_area)
            return self.rightColumn
        
        def _Leave_button():
            self.leave_button = QtW.QPushButton('Leave')
            font = self.Carcassonne.Properties.Font(size=0, bold=False)
            self.leave_button.setFont(font)
            return self.leave_button
        
        def _Title():
            self.title_label = QtW.QLabel("Carcassonne Online", alignment=QtC.Qt.AlignmentFlag.AlignCenter)
            font = self.Carcassonne.Properties.Font(size=5, bold=True)
            self.title_label.setFont(font)
            return self.title_label
        
        # Layout
        self.main_layout = QtW.QGridLayout()
        self.setLayout(self.main_layout)
        self.main_layout.addWidget(_Leave_button(),                           0, 0, 1, 3)
        self.main_layout.addWidget(_Title(),                                  1, 0, 1, 3)
        self.main_layout.addWidget(QtE.QHSeparationLine(colour=(80, 80, 80)), 2, 0, 1, 3) # slightly grey line
        self.main_layout.addLayout(_Game_players(),                           3, 0, 1, 3)
        self.main_layout.addLayout(_Game_left_column(),                       4, 0, 1, 1) # leave column 1 out for correct padding around board
        self.main_layout.addLayout(_Game_right_column(),                      4, 2, 1, 1)
    
    def _Add_meeple_to_inventory(self, meeple_type):
        if meeple_type == 'standard':
            meeple = Meeples.Meeple_standard(self.Carcassonne)
            self.meeples['standard'] += [meeple]
            self.meeples_standard_layout.addWidget(self.meeples_standard[idx], np.floor((idx)/4).astype(int), idx%4, 1, 1)
        pass
        
    def _Meeples_enable(self, enable):
        '''
        enable : bool
            True: will enable all available meeples
            False: will disable all meeples
        '''
        available_meeple_types = self.Carcassonne.game_vis.meeple_types
        for meeple_type in ['meeples_standard', 'meeples_abbot', 'meeples_big']:
            # Check if meeple type is in game
            if meeple_type in available_meeple_types:
                # Get all meeples from the type
                meeples = getattr(self.Carcassonne.game_vis, meeple_type)
                for meeple in meeples.values():
                    if enable == True:
                        # If meeple is available, enable it to be clicked on
                        if meeple.available == True:
                            meeple.enable()
                    else: # When disabling, all should be disabled
                        meeple.disable()
    
    #%% Feed handling, receiving
    def _Feed_receive_pass_turn(self, data):
        # Import data
        previous_player = data['previous_player']
        next_player = data['next_player']
        
        # Function
        # # Blinking animation
        # if self.Carcassonne.lobby_key == 'test':
        #     animation = Animations.Animation(name)
        #     animation.add_blinking(1, 0.1, 2500, 200)
        #     self.players_name_anims[player] = animation
        
        if previous_player == self.Carcassonne.username:
            # Disable clickable stuff
            pass
        
        elif next_player == self.Carcassonne.username:
            # Enable clickable stuff
            self._Meeples_enable(True)
            pass