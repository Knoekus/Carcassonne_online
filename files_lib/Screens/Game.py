if __name__ == '__main__': # direct test call
    import PyQt5.QtGui     as QtG
    import PyQt5.QtWidgets as QtW
    import PyQt5.QtCore    as QtC
    
    import firebase_admin
    from firebase_admin import credentials, db
    
    import sys
    if r"..\..\files_lib" not in sys.path:
        sys.path.append(r"..\..\files_lib")
    import PyQt5_Extra     as QtE
    import prop_s
    
    if r"..\Dialogs" not in sys.path:
        sys.path.append(r"..\..\Dialogs")
    from Dialogs.YesNo import YesNoDialog
    
    def FirebaseInit():
        if not firebase_admin._apps: # only initialize if app doesn't exist
            # Initialize Firebase Admin SDK
            cred = credentials.Certificate(r'..\..\SDK_KEY_KEEP_SAFE\clientserver1-firebase-adminsdk-roo18-d3927e4c28.json')
            firebase_admin.initialize_app(cred, {
                'databaseURL': 'https://clientserver1-default-rtdb.europe-west1.firebasedatabase.app/'
            })
else: # call from lobby
    import PyQt5.QtGui     as QtG
    import PyQt5.QtWidgets as QtW
    import PyQt5.QtCore    as QtC
    import PyQt5_Extra     as QtE
    from firebase_admin import db

    import prop_s    
    import sys
    if r"..\Dialogs" not in sys.path:
        sys.path.append(r"..\Dialogs")
    from Dialogs.YesNo import YesNoDialog

#%% Game screen
class GameScreen(QtW.QWidget):
    #%% Visuals
    def __init__(self, lobby):
        super().__init__()
        self.menu_screen = lobby.menu_screen
        self.lobby = lobby
        
        self._Game_init()
        self._Game_layout()
        
        self.setLayout(self.mainLayout)
    
    def _Game_init(self):
        # References from lobby
        self.username = self.lobby.username
        self.Refs = self.lobby.Refs
        self.font_size = self.lobby.font_size
    
    def _Game_layout(self):
        self.mainLayout = QtW.QGridLayout()
        self.mainLayout.addWidget(self._Game_title(),                        0, 0, 1, 3)
        self.mainLayout.addWidget(QtE.QHSeparationLine(colour=(80, 80, 80)), 1, 0, 1, 3) # slightly grey line
        self.mainLayout.addLayout(self._Game_players(),                      2, 0, 1, 3)
        self.mainLayout.addWidget(QtE.QHSeparationLine(colour=(80, 80, 80)), 3, 0, 1, 3)
        self.mainLayout.addLayout(self._Game_left_column(),                  4, 0, 1, 1) # leave column 1 out for correct padding around board
        self.mainLayout.addLayout(self._Game_right_column(),                 4, 2, 1, 1)
    
    def _Game_title(self):
        title = QtW.QLabel("Carcassonne Online")
        title.setFont(QtG.QFont(prop_s.font,prop_s.font_sizes[5+self.font_size], QtG.QFont.Bold))
        title.setAlignment(QtC.Qt.AlignCenter)
        return title

    def _Game_players(self):
        if __name__ == '__main__':
            # player_list = [f'Player {idx}' for idx in range(1, len(prop_s.colours))]
            player_list = [f'Player {idx}' for idx in range(1, 5)]
        else:
            # Get a new player list
            players = self.lobby.Refs('connections').get()
            player_list = [player for player in players if player is not None]
        
        self.players = QtW.QGridLayout()
        for idx, player in enumerate(player_list):
            name   = QtW.QLabel(f'{player}')
            name.setFont(QtG.QFont(prop_s.font,prop_s.font_sizes[1+self.font_size], QtG.QFont.Bold))
            name.setAlignment(QtC.Qt.AlignCenter)
            points = QtW.QLabel('0')
            points.setFont(QtG.QFont(prop_s.font,prop_s.font_sizes[1+self.font_size]))
            points.setAlignment(QtC.Qt.AlignCenter)
            
            self.players.addWidget(name,   1, idx)
            self.players.addWidget(points, 2, idx)
        
        # Fill in the blank spots, so float all players to left
        # for padding in range(idx, len(prop_s.colours)-1):
        #     players.addWidget(QtW.QLabel(), 1, padding)
            
        return self.players
    
    def _Game_inventory(self):
        # Label
        inventory_label = QtW.QLabel('Inventory')
        inventory_label.setFont(QtG.QFont(prop_s.font, prop_s.font_sizes[2+self.lobby.font_size], QtG.QFont.Bold))
        
        self.inventory = QtW.QGridLayout()
        self.inventory.addWidget(inventory_label, 0, 0)
        
    def _Game_left_column(self):
        # New tile
        tile_size = 200
        if __name__ == '__main__': # independent call
            self.new_tile = QtE.QImage(r'..\Images\tile_logo.png', tile_size, tile_size)
        else: # call from lobby
            self.new_tile = QtE.QImage(r'.\Images\tile_logo.png', tile_size, tile_size)
        
        # Tiles left
        self.tiles_left = QtW.QLabel('0 tiles left.')
        self.tiles_left.setFont(QtG.QFont(prop_s.font, prop_s.font_sizes[0+self.lobby.font_size]))
        self.tiles_left.setAlignment(QtC.Qt.AlignCenter)
        
        # Inventory
        self._Game_inventory()
        
        # End turn
        self.button_end_turn = QtW.QPushButton('End turn')
        self.button_end_turn.setFont(QtG.QFont(prop_s.font, prop_s.font_sizes[2+self.lobby.font_size]))
        
        # Left column
        self.leftColumn  = QtW.QVBoxLayout()
        self.leftColumn.addWidget(self.new_tile)
        self.leftColumn.addWidget(self.tiles_left)
        self.leftColumn.addWidget(QtE.QHSeparationLine(colour=(80,80,80), height=1))
        self.leftColumn.addLayout(self.inventory)
        
        self.leftColumn.addStretch()
        self.leftColumn.addWidget(QtE.QHSeparationLine(colour=(80,80,80), height=10))
        self.leftColumn.addWidget(self.button_end_turn)
        
        return self.leftColumn
        
    def _Game_right_column(self):
        # Board
        self.board = QtW.QScrollArea()
        '''The board will consist of rows of QHBoxLayouts, where we can insert widgets at index i.'''
        
        # Right column
        self.rightColumn = QtW.QVBoxLayout()
        self.rightColumn.addWidget(self.board)
        return self.rightColumn
    
    #%% Functionality
    def closeEvent(self, event):
        if __name__ != '__main__':
            title = 'Close program?'
            text = 'Are you sure you want to close the program?'
            yesNoDialog = YesNoDialog(self, title, text)
            result = yesNoDialog.exec_()
            
            # Ignore if not accepted, else continue (close)
            if result != QtW.QDialog.Accepted:
                event.ignore()
            else:
                self.lobby.remove_connection(self.username)

#%% Main
if __name__ == '__main__':
    FirebaseInit()
    
    app = QtW.QApplication(sys.argv)
    app.setStyle('Breeze') # ['Breeze', 'Oxygen', 'QtCurve', 'Windows', 'Fusion']
    app.setWindowIcon(QtG.QIcon(r'..\..\files_lib\Images\Coin_icon.png'))
    
    class LobbyTest():
        def __init__(self):
            self.username = 'Knoekus'
            self.font_size = 5
            self.menu_screen = None
        
        def Refs(self, key, item=None, load='get_set', prefix='lobby'):
            '''load : reference type
                    "get_set" (default)
                        get a reference to perform a get() or set() actions on. Returns the reference.
                        
                    "add_del"
                        add or delete an item from a reference. Returns nothing.
                    
                prefix : reference type
                    "lobby" (default)
                        perform reference extraction on lobbies/{lobby_key}.'''
            if prefix == 'lobby':
                prefix = f'lobbies/{self.lobby_key}'
                
            if load == 'get_set':
                return db.reference(f'{prefix}/{key}')
            elif load == 'add_del':
                entries = db.reference(f'{prefix}/{key}').get()
                if type(entries) == dict:
                    entries = list(entries.keys())
                if item in entries: # item should be deleted
                    entries.remove(item)
                else: # item should be added
                    entries.append(item)
                db.reference(f'{prefix}/{key}').set(entries)
    
    game_screen = GameScreen(LobbyTest())
    game_screen.showMaximized()
    game_screen.activateWindow()
    game_screen.raise_() # raise to top
    sys.exit(app.exec_())