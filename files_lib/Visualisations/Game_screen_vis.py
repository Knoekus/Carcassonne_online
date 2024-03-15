#%% Imports
# PyQt6
import PyQt6.QtGui     as QtG
import PyQt6.QtWidgets as QtW
import PyQt6.QtCore    as QtC
import PyQt6_Extra     as QtE

# Custom classes
# ...

# Other packages
# ...

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
        
        def _Game_players():
            # Put each player in the row with points indicator
            self.players_grid = QtW.QGridLayout()
            self.players_name_labels = dict()
            self.players_name_anims = dict()
            self.players_points = dict()
            
            player_list = self.Carcassonne.Refs('connections').get().keys()
            for idx, player in enumerate(player_list):
                self.Carcassonne.Refs(f'players/{player}/points').set(0)
                
                player_hbox = QtW.QHBoxLayout()
                colour = QtW.QLabel('', alignment=QtC.Qt.AlignmentFlag.AlignRight)
                colour.setScaledContents(True)
                colour.setFixedSize(25, 25)
                font = self.Carcassonne.Properties.Font(size=1, bold=False)
                colour.setFont(font)
                file = './Images/Coin_icon - Copy.png'
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
        
        # Layout
        self.main_layout = QtW.QGridLayout()
        self.setLayout(self.main_layout)
        self.main_layout.addWidget(_Leave_button(),                           0, 0, 1, 3)
        self.main_layout.addWidget(_Title(),                                  1, 0, 1, 3)
        self.main_layout.addWidget(QtE.QHSeparationLine(colour=(80, 80, 80)), 2, 0, 1, 3) # slightly grey line
        self.main_layout.addLayout(_Game_players(),                           3, 0, 1, 3)
        self.main_layout.addWidget(QtE.QHSeparationLine(colour=(80, 80, 80)), 4, 0, 1, 3)
        # self.main_layout.addLayout(self._Game_left_column(),                  4, 0, 1, 1) # leave column 1 out for correct padding around board
        # self.main_layout.addLayout(self._Game_right_column(),                 4, 2, 1, 1)