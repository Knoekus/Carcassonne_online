#%% Imports
# PyQt6
import PyQt6.QtGui     as QtG
import PyQt6.QtWidgets as QtW
import PyQt6.QtCore    as QtC
import PyQt6_Extra     as QtE

# Custom classes
import Visualisations.Lobby_screen_vis as LobbyVis
import Functionalities.Lobby_screen_func as LobbyFunc
from Dialogs.Username import UsernameDialog
from Dialogs.YesNo    import YesNoDialog

# Other packages
from firebase_admin import db
import random
import string

#%% Menu screen functionality
class Menu_screen_func():
    def __init__(self, Carcassonne):
        self.Carcassonne = Carcassonne
        self.menu_vis = self.Carcassonne.menu_vis
        
        # Connect buttons
        self.Connect_buttons()
    
    def Connect_buttons(self):
        # Create lobby
        self.menu_vis.create_lobby_button.clicked.connect(self._Create_lobby)
        
        # Join lobby
        self.menu_vis.join_lobby_button.clicked.connect(self._Join_lobby)
        self.menu_vis.lobby_key_input.returnPressed.connect(self.menu_vis.join_lobby_button.click)
    
    def _Create_lobby(self):
        if self.Carcassonne.test == True: # test mode
            self.Carcassonne.lobby_key = 'test'
            self.Carcassonne.username = 'user1'
            
            self._Save_lobby_to_database()
            self._Open_lobby_screen()
            
            # # Add player 2
            # self.Refs('connections/fake_user').set(0)
            # self.Refs('players/fake_user/colour').set(prop_s.colours[1]) # give colour
            # self.Refs(f'colours/{prop_s.colours[1]}').set(1)
        else:
            # Open the username dialog
            username_dialog = UsernameDialog(self)
            
            # In the meantime, create the actual lobby
            self.Carcassonne.lobby_key = self._Generate_lobby_key()
            
            # Retrieve username info
            result = username_dialog.exec()
            if result == QtW.QDialog.Accepted:
                self.Carcassonne.username = username_dialog.get_username()
                self._Save_lobby_to_database()
                self._Open_lobby_screen()
            else:
                # User canceled the username dialog
                pass
    
    def _Generate_lobby_key(self):
        lobbies = self.Refs('', prefix='lobbies').get()
        if lobbies != None:
            lobbies = list(lobbies.keys())
        else:
            lobbies = []
        while True: # make sure the lobby key doesn't exist yet
            letters = string.ascii_uppercase
            lobby_key = ''.join(random.choice(letters) for _ in range(8))
            if lobby_key not in lobbies:
                break
        return lobby_key
    
    def _Is_username_free(self):
        if self.Carcassonne.username in self.Refs('connections').get():
            return False
        else: return True
    
    def _Join_lobby(self):
        if self.Carcassonne.test == True: # test mode
            self.Carcassonne.lobby_key = 'test'
            self.Carcassonne.username = 'user2'
            
            self._Save_connection_to_lobby()
            self._Open_lobby_screen()
        else:
            lobby_key = self.menu_vis.lobby_key_input.text().strip().upper()
            if lobby_key in self.Refs('', prefix='lobbies').get():
                # In the meantime, create the references to the lobby
                self.Carcassonne.lobby_key = lobby_key
                if self.Refs('open').get() == True:
                    username_dialog = UsernameDialog(self)
                    result = username_dialog.exec()
                    if result == QtW.QDialog.Accepted:
                        self.Carcassonne.username = username_dialog.get_username()
                        if self._Is_username_free():
                            self._Save_connection_to_lobby()
                            self._Open_lobby_screen()
                        else:
                            QtW.QMessageBox.warning(self, 'Username taken', 'That username is already taken in the lobby. Please choose a different username.')
                    else:
                        # User canceled the username dialog
                        pass
                else:
                    QtW.QMessageBox.warning(self, 'Lobby closed', 'The specified lobby is not open to new users.')
            else:
                QtW.QMessageBox.warning(self, 'Invalid lobby key', 'Please enter a valid lobby key.')

    def _Open_lobby_screen(self):
        # Visualisation
        self.Carcassonne.lobby_vis = LobbyVis.Lobby_screen_vis(self.Carcassonne)
        self.Carcassonne.stacked_widget.addWidget(self.Carcassonne.lobby_vis)
        
        # Functionality
        self.Carcassonne.lobby_func = LobbyFunc.Lobby_screen_func(self.Carcassonne)
        pass
    
    def _Save_connection_to_lobby(self):
        # Player attributes
        self.Refs(f'connections/{self.Carcassonne.username}').set(0)
        blank_colour = self.Carcassonne.Properties.colours[0] # start with blank colour
        self.Refs(f'players/{self.Carcassonne.username}/colour').set(blank_colour)
        self.Refs(f'players/{self.Carcassonne.username}/points').set(0)
        
    def _Save_lobby_to_database(self):
        # Lobby attributes
        self.Refs('active_player').set(self.Carcassonne.username)
        self.Refs('admin').set(self.Carcassonne.username)
        self.Refs('feed').set([])
        self.Refs('open').set(True)
        for colour in self.Carcassonne.Properties.colours[1:]:
            self.Refs(f'colours/{colour}').set(0)
        for expansion in self.Carcassonne.Properties.expansions:
            self.Refs(f'expansions/{expansion}').set(0)
            
        # Save player to lobby
        self._Save_connection_to_lobby()
    
    #%% Helper functions
    def Refs(self, key, item=None, load='get_set', prefix='lobby'):
        '''load : reference type
                "get_set" (default)
                    get a reference to perform a get() or set() actions on. Returns the reference.
                    
                "add_del"
                    add or delete an item from a reference. Returns nothing.
                
            prefix : reference type
                "lobby" (default)
                    perform reference extraction on lobbies/{lobby_key}.'''
        # Set default prefix
        if prefix == 'lobby':
            prefix = f'lobbies/{self.Carcassonne.lobby_key}'
            
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