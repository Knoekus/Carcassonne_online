import PyQt6.QtGui     as QtG
import PyQt6.QtWidgets as QtW
import PyQt6.QtCore    as QtC
import PyQt6_Extra     as QtE

import prop_s
import tile_data

class Meeple(QtE.ClickableImage):
    def __init__(self, game, meeple_type):
        self.init_vars(game, meeple_type)
        super().__init__(self.pixmap, self.size, self.size)
    
    def init_vars(self, game, meeple_type):
        self.available = True
        self.enabled = False
        self.game = game
        
        self.size = 50
        colour = self.game.lobby.Refs(f'players/{self.game.lobby.username}/colour').get()
        colour_string = self.Colour_string(colour)
        if meeple_type == 'standard':
            file = f'./Images/Meeples/{colour_string}/SF.png'
        
        # When launching game screen directly, go up an extra folder
        if 'test' in self.game.lobby.lobby_key:
            file = '.'+file
        
        self.pixmap = QtE.GreenScreenPixmap(file)
    
    def Colour_string(self, colour):
        '''Convert a HEX colour code to a string.'''
        if colour == prop_s.colours[1]:
            return 'Red'
        elif colour == prop_s.colours[2]:
            return 'Orange'
        elif colour == prop_s.colours[3]:
            return 'Yellow'
        elif colour == prop_s.colours[4]:
            return 'Green'
        elif colour == prop_s.colours[5]:
            return 'Blue'
        elif colour == prop_s.colours[6]:
            return 'Magenta'
        else:
            raise Exception(f'The colour {colour} is not available.')
            
class Meeple_standard(Meeple):
    def __init__(self, game):
        super().__init__(game, meeple_type='standard')
        self.power = 1

class MeeplePlaceWindow(QtW.QDialog):
    def __init__(self, tile, meeple_type, parent=None):
        super().__init__(parent)
    
        self.setWindowTitle('Place your meeple')
        # self.setFixedSize(300, 100)
        
        # Tile layout
        tile_layout = QtW.QGridLayout()
        # ...
        
        # Buttons
        self.y_button = QtW.QPushButton('Confirm')
        self.y_button.setFont(QtG.QFont(prop_s.font, prop_s.font_sizes[-2+parent.font_size]))
        self.y_button.clicked.connect(self.accept)
        self.y_button.setEnabled(False)
        
        self.n_button = QtW.QPushButton('Cancel')
        self.n_button.setFont(QtG.QFont(prop_s.font, prop_s.font_sizes[-2+parent.font_size]))
        self.n_button.clicked.connect(self.close)
        
        # Final layout
        layout = QtW.QGridLayout()
        layout.addLayout(tile_layout,   0, 0, 1, 2)
        layout.addWidget(self.n_button, 1, 0)
        layout.addWidget(self.y_button, 1, 1)
        self.setLayout(layout)
        self.show()
    
    def Position_select(self, pos):
        # Enable and default the confirm button
        self.y_button.setEnabled(True)
        self.y_button.setDefault(True)
        
        # Visualise
        # ...

    def setMinWidth(self, width):
        self.setStyleSheet(f"QLabel{{min-width: {width}px;}}");

def En_dis_able_meeples(game, enable):
    '''
    enable : bool
        True: will enable all available meeples
        False: will disable all meeples
    '''
    available_meeple_types = game.__dict__
    for meeple_type in ['meeples_standard', 'meeples_abbot', 'meeples_big']:
        # Check if meeple type is in game
        if meeple_type in available_meeple_types:
            # Get all meeples from the type
            meeples = getattr(game, meeple_type)
            for meeple in meeples.values():
                if enable == True:
                    # If meeple is available, enable it to be clicked on
                    if meeple.available == True:
                        meeple.enable()
                else: # When disabling, all should be disabled
                    meeple.disable()