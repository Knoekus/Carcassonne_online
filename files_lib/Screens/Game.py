#%% Imports
if __name__ == '__main__': # direct test call
    import PyQt6.QtGui     as QtG
    import PyQt6.QtWidgets as QtW
    import PyQt6.QtCore    as QtC
    
    import firebase_admin
    from firebase_admin import credentials, db
    
    import numpy as np
    import string
    
    import sys
    if r"..\..\files_lib" not in sys.path:
        sys.path.append(r"..\..\files_lib")
    import PyQt6_Extra     as QtE
    import prop_s
    
    if r"..\Screens" not in sys.path:
        sys.path.append(r"..\..\Screens")
    from Screens.Expansions import Expansions
    from Screens.Tiles import Tiles
    
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
    import PyQt6.QtGui     as QtG
    import PyQt6.QtWidgets as QtW
    import PyQt6.QtCore    as QtC
    import PyQt6_Extra     as QtE
    from firebase_admin import db

    import prop_s
    import numpy as np
    import string
    
    import sys
    # if r"Screens" not in sys.path:
    #     sys.path.append(r"..\Screens")
    from Screens.Expansions import Expansions
    from Screens.Tiles import Tiles
    
    # if r"..\Dialogs" not in sys.path:
    #     sys.path.append(r"..\Dialogs")
    # from Dialogs.YesNo import YesNoDialog

#%% Game screen
class GameScreen(QtW.QWidget):
    #%% Visuals
    def __init__(self, lobby):
        super().__init__()
        self.menu_screen = lobby.menu_screen
        self.lobby = lobby
        
        # Initial setup
        self._Game_init()
        self._Game_layout()
        self.setLayout(self.mainLayout)
        
        # Expansions
        self.Expansions = Expansions(self)
        
        # Game phase 1
        self.Tiles.Board_init()
        if self.Expansions.expansions[r'The River'] == 0:
            # Default start with tile H
            self.Tiles.Place_tile((1, 'H'), 0, 0)
        else:
            # Start with a spring
            self.Tiles.Place_tile((2, 'D'), 0, 0)
            for i in range(1,6):
                self.Tiles.Place_tile((2, 'A'), 0, i)
            for i in [-1, 1, 2, -2]:
                self.Tiles.Place_tile((2, 'B'), i, 4)
    
    def _Game_init(self):
        # References from lobby
        self.username = self.lobby.username
        self.Refs = self.lobby.Refs
        self.font_size = self.lobby.font_size
        
        # Tiles
        self.Tiles = Tiles(self)
        numbers = [8, 9, 4, 1, 3, 3, 3, 4, 5, 4, 2, 1, 2, 3, 2, 3, 2, 3, 2, 3, 1, 1, 2, 1]
        self.Tiles.Add_tiles(1, numbers)
        
        # Materials
        self.materials = ['grass', 'road', 'city', 'monastery']
    
    def _Game_layout(self):
        # Title
        title = QtW.QLabel("Carcassonne Online", alignment=QtC.Qt.AlignmentFlag.AlignCenter)
        font = QtG.QFont(prop_s.font, prop_s.font_sizes[5+self.font_size])
        font.setBold(True)
        title.setFont(font)
        
        # Players
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
                name = QtW.QLabel(f'{player}', alignment=QtC.Qt.AlignmentFlag.AlignCenter)
                font = QtG.QFont(prop_s.font, prop_s.font_sizes[1+self.lobby.font_size])
                font.setBold(True)
                name.setFont(font)
                
                points = QtW.QLabel('0', alignment=QtC.Qt.AlignmentFlag.AlignCenter)
                points.setFont(QtG.QFont(prop_s.font, prop_s.font_sizes[1+self.font_size]))
                
                self.players.addWidget(name,   1, idx)
                self.players.addWidget(points, 2, idx)
            
            # Fill in the blank spots, so float all players to left
            # for padding in range(idx, len(prop_s.colours)-1):
            #     players.addWidget(QtW.QLabel(), 1, padding)
                
            return self.players
        
        # Layout
        self.mainLayout = QtW.QGridLayout()
        
        self.mainLayout.addWidget(title,                                     0, 0, 1, 3)
        self.mainLayout.addWidget(QtE.QHSeparationLine(colour=(80, 80, 80)), 1, 0, 1, 3) # slightly grey line
        self.mainLayout.addLayout(_Game_players(self),                       2, 0, 1, 3)
        self.mainLayout.addWidget(QtE.QHSeparationLine(colour=(80, 80, 80)), 3, 0, 1, 3)
        self.mainLayout.addLayout(self._Game_left_column(),                  4, 0, 1, 1) # leave column 1 out for correct padding around board
        self.mainLayout.addLayout(self._Game_right_column(),                 4, 2, 1, 1)
        
    def _Game_left_column(self):
        # New tile
        new_tile_size = 200
        if __name__ == '__main__': # independent call
            self.new_tile = QtE.QImage(r'..\Images\tile_logo.png', new_tile_size, new_tile_size)
        else: # call from lobby
            self.new_tile = QtE.QImage(r'.\Images\tile_logo.png', new_tile_size, new_tile_size)
        
        # Tiles left
        self.tiles_left = sum(self.tiles.values())
        self.tiles_left_label = QtW.QLabel(f'{self.tiles_left} tiles left.', alignment=QtC.Qt.AlignmentFlag.AlignCenter)
        self.tiles_left_label.setFont(QtG.QFont(prop_s.font, prop_s.font_sizes[0+self.lobby.font_size]))
        
        # Inventory
        self.inventory_label = QtW.QLabel('Inventory', alignment=QtC.Qt.AlignmentFlag.AlignCenter)
        font = QtG.QFont(prop_s.font, prop_s.font_sizes[2+self.lobby.font_size])
        font.setBold(True)
        self.inventory_label.setFont(font)
        self._Game_inventory()
        
        # End turn
        self.button_end_turn = QtW.QPushButton('End turn')
        self.button_end_turn.setFont(QtG.QFont(prop_s.font, prop_s.font_sizes[2+self.lobby.font_size]))
        
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
    
    def _Game_inventory(self):
        #===== Initial inventory =====#
        def _Meeple_standard():
            tile_size = 50
            if __name__ == '__main__': # independent call
                file = r'..\Images\Meeples\Blue\SF.png'
            else: # call from lobby
                file = r'.\Images\Meeples\Blue\SF.png'
            pixmap = QtE.GreenScreenPixmap(file)
            meeple = QtE.ClickableImage(pixmap, tile_size, tile_size)
            return meeple
        
        self.meeples_standard = dict()
        self.meeples_standard_layout = QtW.QGridLayout()
        self.meeples_standard_layout.setHorizontalSpacing(0)
        self.meeples_standard_layout.setVerticalSpacing(0)
        for idx in range(7): # start with 7 standard meeples
            self.meeples_standard[idx] = _Meeple_standard()
            self.meeples_standard_layout.addWidget(self.meeples_standard[idx], np.floor((idx)/4).astype(int), idx%4, 1, 1)
        
        self.inventory = QtW.QGridLayout()
        self.inventory.addLayout(self.meeples_standard_layout, 0, 0, 1, 3)
        
    def _Game_right_column(self):
        # Board
        self.board_widget = QtW.QWidget()
        self.board_base = QtW.QVBoxLayout()
        self.board_base.setSpacing(prop_s.tile_spacing)
        
        self.board_scroll_area = QtW.QScrollArea()
        self.board_scroll_area.setWidget(self.board_widget)
        self.board_scroll_area.setWidgetResizable(True)
        
        # Right column
        self.rightColumn = QtW.QVBoxLayout()
        self.rightColumn.addWidget(self.board_scroll_area)
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
            self.lobby_key = 'test2'

            # References
            self.Refs('admin').set('user1')
            for exp in prop_s.expansions:
                self.Refs(f'expansions/{exp}').set(1) # add all expansions
            self.Refs('open').set(False)
            self.Refs('connections').set({'user1':0, 'user2':0})
            self.Refs('players').set({'user1':{'colour':"ffffff00"}, 'user2':{'colour':"ffff00ff"}})
            self.Refs('feed').set([])
        
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
        
        def send_feed_message(self, **kwargs):
            print('\n', kwargs)
            if len(kwargs.keys()) > 0: # call from internal game
                chat_message = {'username': self.username}
                for arg in kwargs.keys():
                    chat_message[arg] = kwargs[arg]
                    
                if self.Refs('feed').push(chat_message):
                    print('sent')
                
            else: # call from the chat input box
                message = self.chat_input.text().strip()
    
                if len(message)>0:
                    chat_message = {
                        'username': self.username,
                        'message': message
                    }
                    if self.Refs('feed').push(chat_message):
                        print('sent')
    
    game_screen = GameScreen()
    game_screen.init_call(LobbyTest())
    
    game_screen.showMaximized()
    game_screen.activateWindow()
    game_screen.raise_() # raise to top
    game_screen.setWindowTitle('Carcassonne Online - Developer mode')
    sys.exit(app.exec())