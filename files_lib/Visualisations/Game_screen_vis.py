#%% Imports
# PyQt6
import PyQt6.QtCore    as QtC
import PyQt6.QtGui     as QtG
import PyQt6.QtWidgets as QtW
import PyQt6_Extra     as QtE

# Custom classes
import Classes.Meeples as Meeples

# Other packages
import numpy as np
import time

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
            for idx in range(50):
                player_list_dict = self.Carcassonne.Refs('connections').get()
                if type(player_list_dict) == type(dict()):
                    player_list = player_list_dict.keys()
                    break
                else:
                    time.sleep(0.1)
            else:
                raise Exception('No connections found after 5 seconds.')
            
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
            # self.new_tile = QtE.Tile(r'.\Images\tile_logo.png', new_tile_size, Carcassonne=self.Carcassonne, rotating=True)
            self.new_tile = QtE.NewTile(r'.\Images\tile_logo.png', new_tile_size, self.Carcassonne)
            
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
            self.Carcassonne.meeples = dict()
            self.Carcassonne.materials = list()
            
            # self.meeples_standard = dict()
            # self.meeples_standard_layout = QtW.QGridLayout()
            # self.meeples_standard_layout.setHorizontalSpacing(0)
            # self.meeples_standard_layout.setVerticalSpacing(0)
            
            # Start with 7 standard meeples
            # self.meeple_types = ['meeples_standard']
            # for idx in range(7):
            #     meeple = Meeples.Meeple_standard(self.Carcassonne)
            #     self.meeples_standard[idx] = meeple
            #     self.meeples_standard_layout.addWidget(meeple, np.floor((idx)/4).astype(int), idx%4, 1, 1)
            # FIXME: maybe it's more convenient to add these to self.Carcassonne instead.
            # FIXME: when doing that, change self._Meeples_enable accordingly.
            # self.Carcassonne.meeple_types = ['meeples_standard']
            # for idx in range(7):
            #     meeple = Meeples.Meeple_standard(self.Carcassonne)
            #     self.Carcassonne.meeples_standard[idx] = meeple
            #     self.Carcassonne.meeples_standard_layout.addWidget(meeple, np.floor((idx)/4).astype(int), idx%4, 1, 1) # max 4 per row
            
            self.inventory = QtW.QGridLayout()
            # self.inventory.addLayout(self.meeples_standard_layout, 0, 0, 1, 3)
            
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
    
    def Tile_placed(self, row, col, file, tile_idx, tile_letter, rotation):
        # Add new row if necessary
        if row < self.Carcassonne.board_rows[0]:
            # self._Board_new_row_above()
            self.Carcassonne.Tiles._Board_new_row_above()
        elif row > self.Carcassonne.board_rows[1]:
            # self._Board_new_row_below()
            self.Carcassonne.Tiles._Board_new_row_below()
        
        # Add new col if necessary
        if col < self.Carcassonne.board_cols[0]:
            # self._Board_new_col_left()
            self.Carcassonne.Tiles._Board_new_col_left()
        elif col > self.Carcassonne.board_cols[1]:
            # self._Board_new_col_right()
            self.Carcassonne.Tiles._Board_new_col_right()
            
        # Place tile
        board_tile = self.Carcassonne.board_tiles[row][col]
        board_tile.coords = (row, col)
        # board_tile.set_tile(file, tile_idx, tile_letter, self.Carcassonne.materials)
        board_tile.set_tile(file, tile_idx, tile_letter)
        board_tile.disable()
        self.Carcassonne.last_placed_tile = board_tile
        
        # Rotating
        rotations = int(np.floor(rotation%360/90))
        if rotations < 0:
            for idx in range(-rotations):
                board_tile.rotate(-90)
        elif rotations > 0:
            for idx in range(rotations):
                board_tile.rotate(90)
        board_tile.rotating = False
        
        # Update possessions
        self.Carcassonne.Possessions.Update_possessions(board_tile.material_data, row, col)
        
        # Reset new tile
        file = r'.\Images\tile_logo.png'
        self.new_tile.draw_image(file)
        self.new_tile.disable()
    
    def Tile_rotated(self, player, rotation):
        # Rotate new_tile
        self.new_tile.rotate(rotation)
        
        # Show options after rotating
        if player == self.Carcassonne.username:
            self.Carcassonne.Tiles.Show_options()

    def Tile_taken(self, player, file, tile_idx, tile_letter):
        '''Handle feed event when a new tile is taken.'''
        # Swap out new_tile image for new tile
        # self.game.new_tile_anim.swap_image(file, tile_idx, tile_letter, 500)
        # self.game.new_tile_anim.swap(file, tile_idx, tile_letter, username)
        self.new_tile.set_tile(file, tile_idx, tile_letter)
        if player == self.Carcassonne.username:
            self.new_tile.enable()
            self.Carcassonne.Tiles.Show_options()
        else:
            self.new_tile.disable()
            
        # Update tiles left
        if self.Carcassonne.tiles[tile_idx][tile_letter] > 1:
            self.Carcassonne.tiles[tile_idx][tile_letter] -= 1 # decrease number of tiles by 1
        else:
            if len(self.Carcassonne.tiles[tile_idx].keys()) > 1:
                self.Carcassonne.tiles[tile_idx].pop(tile_letter) # delete tile if none left
            else:
                self.Carcassonne.tiles.pop(tile_idx) # delete expansion if no tiles left
        
        # Update tiles left label
        self.Carcassonne.Tiles.Update_tiles_left_label()
        
    def _Meeples_enable(self, enable):
        '''
        enable : bool
            True: will enable all available meeples
            False: will disable all meeples
        '''
        # available_meeple_types = self.Carcassonne.game_vis.meeple_types
        # for meeple_type in ['meeples_standard', 'meeples_abbot', 'meeples_big']:
        #     # Check if meeple type is in game
        #     if meeple_type in available_meeple_types:
        #         # Get all meeples from the type
        #         meeples = getattr(self.Carcassonne.game_vis, meeple_type)
        #         for meeple in meeples.values():
        #             if enable == True:
        #                 # If meeple is available, enable it to be clicked on
        #                 if meeple.available == True:
        #                     meeple.enable()
        #             else: # When disabling, all should be disabled
        #                 meeple.disable()
        available_meeple_types = self.Carcassonne.meeples.keys()
        for meeple_type in available_meeple_types:
        # Get all selected meeple types
            for meeple in self.Carcassonne.meeples[meeple_type]:
            # Get all meeples from the type
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
            self.button_end_turn.setEnabled(False)
        
        elif next_player == self.Carcassonne.username:
            # Enable clickable stuff
            # self._Meeples_enable(True)
            pass
    
    def _Feed_receive_tile_placed(self, data):
        # Import data
        player = data['user']
        row = data['row']
        col = data['col']
        file = data['file']
        tile_idx = data['tile_idx']
        tile_letter = data['tile_letter']
        rotation = data['rotation']
        
        # Function
        if player == self.Carcassonne.username:
        # The player who sent this event has performed this action already.
            return
        else:
            self.Tile_placed(row, col, file, tile_idx, tile_letter, rotation)
    
    def _Feed_receive_tile_rotated(self, data):
        # Import data
        player = data['user']
        rotation = data['rotation']
        
        # Function
        if player == self.Carcassonne.username:
        # The player who sent this event has performed this action already.
            return
        else:
            self.Tile_rotated(player, rotation)
    
    def _Feed_receive_tile_taken(self, data):
        # Import data
        player = data['user']
        file = data['file']
        tile_idx = data['tile_idx']
        tile_letter = data['tile_letter']
        
        # Function
        if player == self.Carcassonne.username:
        # The player who sent this event has performed this action already.
            return
        else:
            self.Tile_taken(player, file, tile_idx, tile_letter)