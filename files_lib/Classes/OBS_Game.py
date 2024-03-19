#%% Imports
if __name__ == '__main__': # direct test call
    import PyQt6.QtGui     as QtG
    import PyQt6.QtWidgets as QtW
    import PyQt6.QtCore    as QtC
    
    import firebase_admin
    from firebase_admin import credentials, db
    
    import numpy as np
    import time
    
    import sys
    if r"..\..\files_lib" not in sys.path:
        sys.path.append(r"..\..\files_lib")
    import PyQt6_Extra     as QtE
    import prop_s
    
    if r"..\Classes" not in sys.path:
        sys.path.append(r"..\..\Classes")
    import Classes.Animations as Animations
    from Classes.Expansions import Expansions
    from Classes.Tiles import Tiles
    import Classes.Meeples as Meeples
    import Classes.Possessions as Possessions
    
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
    import time
    
    
    import sys
    # if r"Screens" not in sys.path:
    #     sys.path.append(r"..\Classes")
    import Classes.Animations as Animations
    from Classes.Expansions import Expansions
    from Classes.Tiles import Tiles
    import Classes.Meeples as Meeples
    import Classes.Possessions as Possessions
    
    # if r"..\Dialogs" not in sys.path:
    #     sys.path.append(r"..\Dialogs")
    from Dialogs.YesNo import YesNoDialog

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
        self._Game_start()
        self.setLayout(self.mainLayout)
        
        # Admin leads setup
        if self.username == self.Refs('admin').get():
            # Wait until everybody is ready
            while True:
                players_loading = sum(self.Refs('connections').get().values())
                if players_loading == 0:
                    break
                else:
                    time.sleep(0.1)
            
            # Game phase 1: starting player
            if self.lobby.lobby_key == 'test2':
                self.current_player = 'user1'
                # self.Player_at_turn('user1', init=True)
            else:
                starting_player = np.random.choice(self.player_list)
                self.current_player = starting_player
                # self.Player_at_turn(starting_player, init=True)
            
            # Game phase 2: initial tile
            if r'The River' not in self.expansions:
                # Default start with tile H
                file = self.Tiles.Choose_tile(1, 'H')[2]
                self.Tiles.Place_tile(file, 1, 'H', 0, 0)
            else:
                # Start with a spring
                file = self.Tiles.Choose_tile(2, 'D')[2]
                self.Tiles.Place_tile(file, 2, 'D', 0, 0)
                # self.Tiles.New_tile(2) # First finish all The River tiles
            
            self.End_turn(init=True)
            # Game phase 3: make next tile available
            # self.Tiles.New_tile(1)
            # self.Tiles.New_tile(1, 'P')
    
    def _Game_start(self):
        # Board
        self.Tiles.Board_init()
        
        # Expansions
        expansions = self.Refs('expansions').get()
        self.expansions = [exp for exp in expansions.keys() if expansions[exp] == 1]
        self.Expansions = Expansions(self)
        
        # Listen to feed
        self.feed_messages = []
        self.Refs('feed').listen(self.feed_event)
        
        # Set yourself ready with setup
        self.Refs(f'connections/{self.username}').set(0)
    
    def _Game_init(self):
        # References from lobby
        self.username = self.lobby.username
        self.Refs = self.lobby.Refs
        self.font_size = self.lobby.font_size
        
        # Classes
        self.pos_class = Possessions.Possessions(self)
        
        # Connections
        self.connections = self.Refs('connections').get()
        self.player_list = [player for player in self.connections if player is not None]
        
        # Tiles
        self.Tiles = Tiles(self)
        numbers = [8, 9, 4, 1, 3, 3, 3, 4, 5, 4, 2, 1, 2, 3, 2, 3, 2, 3, 2, 3, 1, 1, 2, 1]
        self.Tiles.Add_tiles(1, numbers)
        self.options = set()
        
        # Materials
        self.materials = ['grass', 'road', 'city', 'monastery']
        self.possessions = {material:dict() for material in self.materials}
    
    def _Game_layout(self):
        # Title
        title = QtW.QLabel("Carcassonne Online", alignment=QtC.Qt.AlignmentFlag.AlignCenter)
        font = QtG.QFont(prop_s.font, prop_s.font_sizes[5+self.font_size])
        font.setBold(True)
        title.setFont(font)
        
        # Players
        def _Game_players(self):
            # Put each player in the row with points indicator
            self.players = QtW.QGridLayout()
            self.players_name_labels = dict()
            self.players_name_anims = dict()
            self.players_points = dict()
            for idx, player in enumerate(self.player_list):
                self.Refs(f'players/{player}/points').set(0)
                
                player_hbox = QtW.QHBoxLayout()
                colour = QtW.QLabel('', alignment=QtC.Qt.AlignmentFlag.AlignRight)
                colour.setScaledContents(True)
                colour.setFixedSize(25, 25)
                # colour = QtE.QImage(None, 25, 25)
                font = QtG.QFont(prop_s.font, prop_s.font_sizes[1+self.lobby.font_size])
                # font.setBold(True)
                colour.setFont(font)
                # colour.setFixedSize(colour.height(), colour.height())
                file = './Images/Coin_icon - Copy.png'
                if self.lobby.lobby_key == 'test2':
                    file = '.'+file
                hex_col = self.Refs(f'players/{player}/colour').get()
                rgb_col = tuple(int(hex_col[i:i+2], 16) for i in (0, 2, 4, 6))
                col_pixmap = QtE.GreenScreenPixmap(file, (255, 0, 0), rgb_col)
                colour.setPixmap(col_pixmap)
                
                name = QtW.QLabel(f'{player}', alignment=QtC.Qt.AlignmentFlag.AlignCenter)
                # name = QtW.QLabel(f'{player}', alignment=QtC.Qt.AlignmentFlag.AlignLeft)
                font = QtG.QFont(prop_s.font, prop_s.font_sizes[1+self.lobby.font_size])
                # font.setBold(True)
                name.setFont(font)
                
                player_hbox.addWidget(colour, alignment=QtC.Qt.AlignmentFlag.AlignRight)
                player_hbox.addWidget(name, alignment=QtC.Qt.AlignmentFlag.AlignLeft)
                
                points = QtW.QLabel('0', alignment=QtC.Qt.AlignmentFlag.AlignCenter)
                points.setFont(QtG.QFont(prop_s.font, prop_s.font_sizes[1+self.font_size]))
                
                # self.players.addWidget(colour, 1, idx*2,   1, 1)
                # self.players.addWidget(name,   1, idx*2+1, 1, 1)
                # self.players.addWidget(points, 2, idx*2,   1, 2)
                self.players.addLayout(player_hbox, 1, idx)
                self.players.addWidget(points,      2, idx)
                
                
                # Blinking animation
                if self.lobby.lobby_key == 'test2':
                    animation = Animations.Animation(name)
                    animation.add_blinking(1, 0.1, 2500, 200)
                    self.players_name_anims[player] = animation
                
                # Save references
                self.players_name_labels[player] = name
                self.players_points[player] = points
            
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
            self.new_tile = QtE.Tile(r'..\Images\tile_logo.png', new_tile_size, game=self, rotating=True)
        else: # call from lobby
            self.new_tile = QtE.Tile(r'.\Images\tile_logo.png', new_tile_size, game=self, rotating=True)
        # self.new_tile_anim = Animations.Animation(self.new_tile)
        # self.new_tile_anim = Animations.New_tile_swap(self, self.new_tile)
        
        # Tiles left
        self.tiles_left = 0
        self.tiles_left_label = QtW.QLabel('... tiles left.', alignment=QtC.Qt.AlignmentFlag.AlignCenter)
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
        self.button_end_turn.setEnabled(0)
        self.button_end_turn.clicked.connect(self.End_turn)
        
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
        self.meeples_standard = dict()
        self.meeples_standard_layout = QtW.QGridLayout()
        self.meeples_standard_layout.setHorizontalSpacing(0)
        self.meeples_standard_layout.setVerticalSpacing(0)
        
        # Start with 7 standard meeples
        self.meeple_types = ['standard']
        for idx in range(7):
            meeple = Meeples.Meeple_standard(self)
            meeple.clicked.connect(self.Meeple_clicked(meeple)) # connect function
            self.meeples_standard[idx] = meeple
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
        else:
            self.Refs(f'lobbies/{self.lobby.lobby_key}', prefix='').delete()
    
    def feed_event(self, event):
        if (event.data is not None) and (event.path not in self.feed_messages):
            if event.path == '/':
            # Initial startup (extract all previous messages)
                print('\nRETRIEVING ALL PRIOR MESSAGES')
                paths = list(self.Refs('feed').get().keys())
                for idx, path in enumerate(paths):
                    feed_event = self.Refs(f'feed/{path}').get()
                    # ...
                    pass
                
            else:
            # New message
                self.feed_messages += [event.path]
                feed_event = event.data
                print(f'\nNew event: {feed_event["event"]}')
                if feed_event['event'] == 'new_tile':
                # event, file, tile_idx, tile_letter, username
                    self.Tiles.New_tile_event(feed_event)
                    
                elif feed_event['event'] == 'placed_tile':
                # col, event, file, rotation, row, tile_idx, tile_letter, username
                    self.Tiles.Place_tile_event(feed_event)
                
                elif feed_event['event'] == 'new_tile_rotated':
                # Do this for everybody who is NOT at turn
                    if feed_event['username'] != self.username:
                        rotation = feed_event['rotation']
                        self.new_tile.rotate(rotation)
                        # if feed_event['username'] == self.username:
                            # self.Tiles.Show_options()
                            # self.new_tile.game.Tiles.Show_options()
                
                elif feed_event['event'] == 'placed_meeple':
                # event, meeple_type, original_tile_info, sub_tile, username
                    Meeples.Meeple_placed_event(self, feed_event)
                
                elif feed_event['event'] == 'next_player_turn':
                # current_player, event, next_player, username = event_data
                    self.Player_at_turn_event(feed_event)
    
    def send_feed_message(self, **kwargs):
        if len(kwargs.keys()) > 0: # call from internal game
            chat_message = {'username': self.username}
            for arg in kwargs.keys():
                chat_message[arg] = kwargs[arg]
            self.Refs('feed').push(chat_message)
            
        else: # call from the chat input box
            message = self.chat_input.text().strip()
            if len(message)>0:
                chat_message = {
                    'username': self.username,
                    'message': message
                }
                if self.Refs('feed').push(chat_message):
                    print('sent')
                
    def End_turn(self, init=False):
        # Give turn to the next player
        if self.lobby.lobby_key == 'test2':
            next_player = self.current_player
        else:
            current_player_idx = self.player_list.index(self.current_player)
            next_player_idx = (current_player_idx + 1) % len(self.player_list)
            next_player = self.player_list[next_player_idx]
            
        if init == True:
            print('not switching player')
            self.Player_at_turn(self.current_player)
        else:
            self.Player_at_turn(next_player)
        
    def Player_at_turn(self, next_player, init=False):
        # Stop current player
        # if init == False:
        self.Refs(f'connections/{self.current_player}').set(0)
        # self.players_name_anims[self.current_player].stop_animation()
        
        # New player at turn
        self.Refs(f'connections/{next_player}').set(1)
        # self.players_name_anims[next_player].start()
        # self.current_player = next_player
        
        self.send_feed_message(event          = 'next_player_turn',
                               current_player = self.current_player,
                               next_player    = next_player)
    
    def Player_at_turn_event(self, event_data):
        current_player, event, next_player, username = event_data.values()
        
        if self.lobby.lobby_key == 'test2' and False:
        # For some reason, this animation breaks when in lobby
            if self.players_name_anims[current_player].state() == QtC.QSequentialAnimationGroup.State.Running:
                self.players_name_anims[current_player].stop_animation() # stop current
            self.players_name_anims[next_player].start() 
            self.current_player = next_player
        else:
            font_normal = QtG.QFont(prop_s.font, prop_s.font_sizes[1+self.lobby.font_size])
            font_normal.setBold(False)
            font_at_turn = QtG.QFont(prop_s.font, prop_s.font_sizes[3+self.lobby.font_size])
            font_at_turn.setBold(True)
            
            name = self.players_name_labels[current_player]
            name.setFont(font_normal)
            
            name = self.players_name_labels[next_player]
            name.setFont(font_at_turn)
            self.current_player = next_player
        
        # Take new tile
        if r'The River' in self.expansions:
            try: self.Tiles.New_tile(2)
            except:
                self.Tiles.New_tile()
        else:
            # self.Tiles.New_tile(1)
            try:
                self.Tiles.New_tile(1, 'H')
            except:
                self.Tiles.New_tile(1)
        
    def Meeple_clicked(self, meeple):
        def clicked():
            if meeple.meeple_type == 'standard':
                # In no instance can this meeple be placed on another tile but the
                # placed tile, so no need to highlight options before opening dialog.
                meepleWindow = Meeples.MeeplePlaceWindow(self.last_placed_tile, self, meeple)
                result = meepleWindow.exec()
                if result == QtW.QDialog.DialogCode.Accepted:
                    meepleWindow.Meeple_placed()
                    # meepleWindow.Meeple_placed_event()
                    Meeples.En_dis_able_meeples(self, enable=False) # disable all meeples
            else:
                raise Exception(f'Unknown meeple type: {meeple.meeple_type}')
        return clicked

#%% Main
if __name__ == '__main__':
    FirebaseInit()
    
    app = QtW.QApplication(sys.argv)
    app.setStyle('Breeze') # ['Breeze', 'Oxygen', 'QtCurve', 'Windows', 'Fusion']
    app.setWindowIcon(QtG.QIcon(r'..\..\files_lib\Images\Coin_icon.png'))
    
    class LobbyTest():
        def __init__(self):
            self.username = 'user1'
            self.font_size = 5
            self.menu_screen = None
            self.lobby_key = 'test2'

            # References
            self.Refs('admin').set('user1')
            for exp in prop_s.expansions:
                self.Refs(f'expansions/{exp}').set(0) # add all expansions
            
            self.Refs('open').set(False)
            self.Refs('connections').set({'user1':0, 'user2':0})
            self.Refs('players').set({'user1':{'colour':prop_s.colours[2]}, 'user2':{'colour':prop_s.colours[5]}})
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
            # print('\n', kwargs)
            if len(kwargs.keys()) > 0: # call from internal game
                chat_message = {'username': self.username}
                for arg in kwargs.keys():
                    chat_message[arg] = kwargs[arg]
                    
                # if self.Refs('feed').push(chat_message):
                #     print('sent')
                self.Refs('feed').push(chat_message)
                
            else: # call from the chat input box
                message = self.chat_input.text().strip()
    
                if len(message)>0:
                    chat_message = {
                        'username': self.username,
                        'message': message
                    }
                    # if self.Refs('feed').push(chat_message):
                    #     print('sent')
    
    game_screen = GameScreen(LobbyTest())
    game_screen.showMaximized()
    game_screen.activateWindow()
    game_screen.raise_() # raise to top
    game_screen.setWindowTitle('Carcassonne Online - Developer mode')
    sys.exit(app.exec())