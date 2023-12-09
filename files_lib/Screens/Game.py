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
        
        self.mainLayout.addWidget(self._Game_new_tile(),  0, 0, 4, 1)
        self.mainLayout.addWidget(self._Game_title(),     0, 1, 1, 1)
        self.mainLayout.addWidget(QtE.QHSeparationLine(), 1, 1, 1, 1)
        self.mainLayout.addLayout(self._Game_players(),   2, 1, 1, 1)
        self.mainLayout.addWidget(self._Game_board(),     3, 1, 2, 1)
        
        self.mainLayout.setRowStretch(0, 1)
        self.mainLayout.setRowStretch(1, 0)
        self.mainLayout.setRowStretch(2, 2)
        self.mainLayout.setRowStretch(3, 1)
        self.mainLayout.setRowStretch(self.mainLayout.rowCount()-1, 9)
        
    def _Game_new_tile(self):
        if __name__ == '__main__': # independent call
            new_tile = QtE.QImage(r'..\Images\tile_logo.png', 250, 250)
        else: # call from lobby
            new_tile = QtE.QImage(r'.\Images\tile_logo.png')
        new_tile.setStyleSheet("padding:10") 
        return new_tile
    
    def _Game_title(self):
        title = QtW.QLabel("Carcassonne Online")
        title.setFont(QtG.QFont(prop_s.font,prop_s.font_sizes[5+self.font_size], QtG.QFont.Bold))
        title.setAlignment(QtC.Qt.AlignCenter)
        return title

    def _Game_players(self):
        if __name__ == '__main__':
            player_list = [f'Player {idx}' for idx in range(1, len(prop_s.colours))]
        else:
            # Get a new player list
            players = self.lobby.Refs('connections').get()
            player_list = [player for player in players if player is not None]
        
        players = QtW.QGridLayout()
        for idx, player in enumerate(player_list):
            name   = QtW.QLabel(f'{player}')
            name.setFont(QtG.QFont(prop_s.font,prop_s.font_sizes[1+self.font_size], QtG.QFont.Bold))
            name.setAlignment(QtC.Qt.AlignCenter)
            points = QtW.QLabel('0')
            points.setFont(QtG.QFont(prop_s.font,prop_s.font_sizes[1+self.font_size]))
            points.setAlignment(QtC.Qt.AlignCenter)
            
            players.addWidget(name,   1, idx)
            players.addWidget(points, 2, idx)
        
        # Go from left to right, so fill in the blank spots
        for padding in range(idx, len(prop_s.colours)-1):
            players.addWidget(QtW.QLabel(), 1, padding)
            
        # players.setRowStretch(0, 1)
        # players.setRowStretch(1, 1)
        players.setRowStretch(3, 1)
            
        return players
    
    def _Game_board(self):
        board = QtW.QScrollArea()
        return board
    
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