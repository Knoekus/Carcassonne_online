#%% Imports
# PyQt6
import PyQt6.QtCore    as QtC
import PyQt6.QtGui     as QtG
import PyQt6.QtWidgets as QtW
import PyQt6_Extra     as QtE

# Custom classes
import Visualisations.Lobby_screen_vis as LobbyVis
import Functionalities.Lobby_screen_func as LobbyFunc
from Dialogs.Username import UsernameDialog
from Dialogs.YesNo    import YesNoDialog

# Other packages
import random
import string

#%% Menu screen functionality
class Menu_screen_func():
    def __init__(self, Carcassonne):
        self.Carcassonne = Carcassonne
        self.menu_vis = self.Carcassonne.menu_vis
        self.Carcassonne.stacked_widget.addWidget(self.menu_vis)
        
        # Connect buttons
        self.Connect_buttons()
    
    def Connect_buttons(self):
        # Create lobby
        self.menu_vis.create_lobby_button.clicked.connect(self.Create_lobby)
        
        # Join lobby
        self.menu_vis.join_lobby_button.clicked.connect(self.Join_lobby)
        self.menu_vis.lobby_key_input.returnPressed.connect(self.menu_vis.join_lobby_button.click)
        
        # Close program
        self.menu_vis.close_button.clicked.connect(self.Close_program)
    
    def Close_program(self):
        title = 'Close Carcassonne Online?'
        text = 'Are you sure you want to close Carcassonne Online?'
        yesNoDialog = YesNoDialog(self.Carcassonne, self.menu_vis, title, text)
        result = yesNoDialog.exec()
        if result == QtW.QDialog.DialogCode.Accepted:
            self.Carcassonne.close()
    
    def Create_lobby(self):
        if self.Carcassonne.test == True: # test mode
            self.Carcassonne.lobby_key = 'test'
            self.Carcassonne.username = 'user1'
            
            self._Save_lobby_to_database()
            self._Open_lobby_screen()
        else:
            # Open the username dialog
            username_dialog = UsernameDialog(self.Carcassonne, self.menu_vis)
            
            # In the meantime, create the actual lobby
            self.Carcassonne.lobby_key = self._Generate_lobby_key()
            
            # Retrieve username info
            result = username_dialog.exec()
            if result == QtW.QDialog.DialogCode.Accepted:
                self.Carcassonne.username = username_dialog.get_username()
                self._Save_lobby_to_database()
                self._Open_lobby_screen()
            else:
                # User canceled the username dialog
                pass
    
    def _Generate_lobby_key(self):
        lobbies = self.Carcassonne.Refs('', prefix='lobbies').get()
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
        if self.Carcassonne.username in self.Carcassonne.Refs('connections').get():
            return False
        else: return True
    
    def Join_lobby(self):
        if self.Carcassonne.test == True: # test mode
            self.Carcassonne.lobby_key = 'test'
            self.Carcassonne.username = 'user2'
            
            self._Save_connection_to_lobby()
            self._Open_lobby_screen()
        else:
            lobby_key = self.menu_vis.lobby_key_input.text().strip().upper()
            if lobby_key in self.Carcassonne.Refs('', prefix='lobbies').get():
                # In the meantime, create the references to the lobby
                self.Carcassonne.lobby_key = lobby_key
                if self.Carcassonne.Refs('open').get() == True:
                    username_dialog = UsernameDialog(self.Carcassonne, self.menu_vis)
                    result = username_dialog.exec()
                    if result == QtW.QDialog.DialogCode.Accepted:
                        self.Carcassonne.username = username_dialog.get_username()
                        if self._Is_username_free():
                            self._Save_connection_to_lobby()
                            self._Open_lobby_screen()
                        else:
                            QtW.QMessageBox.warning(self.menu_vis, 'Username taken', 'That username is already taken in the lobby. Please choose a different username.')
                    else:
                        # User canceled the username dialog
                        pass
                else:
                    QtW.QMessageBox.warning(self.menu_vis, 'Lobby closed', 'The specified lobby is not open to new users.')
            else:
                QtW.QMessageBox.warning(self.menu_vis, 'Invalid lobby key', 'Please enter a valid lobby key.')

    def _Open_lobby_screen(self):
        # Visualisation
        self.Carcassonne.lobby_vis = LobbyVis.Lobby_screen_vis(self.Carcassonne)
        
        # Functionality
        self.Carcassonne.lobby_func = LobbyFunc.Lobby_screen_func(self.Carcassonne)
    
    def _Save_connection_to_lobby(self):
        if self.Carcassonne.test == True:
            # When testing
            idx = 2*int(self.Carcassonne.username[-1]) # user1: orange, user2: green
            blank_colour = self.Carcassonne.Properties.colours[idx]
            
            self.Carcassonne.Refs(f'colours/{blank_colour}').set(1)
        else:
            blank_colour = self.Carcassonne.Properties.colours[0] # start with blank colour
            
        # Player attributes
        self.Carcassonne.Refs(f'connections/{self.Carcassonne.username}').set(0)
        self.Carcassonne.Refs(f'players/{self.Carcassonne.username}/colour').set(blank_colour)
        self.Carcassonne.Refs(f'players/{self.Carcassonne.username}/points').set(0)
        self.Carcassonne.Refs(f'players/{self.Carcassonne.username}/feed').set({'init':True})
        
    def _Save_lobby_to_database(self):
        # Lobby attributes
        self.Carcassonne.Refs('active_player').set(self.Carcassonne.username) # FIXME: only add this once the game is started? maybe
        self.Carcassonne.Refs('admin').set(self.Carcassonne.username)
        self.Carcassonne.Refs('open').set(True)
        for colour in self.Carcassonne.Properties.colours[1:]:
            self.Carcassonne.Refs(f'colours/{colour}').set(0)
        for expansion in self.Carcassonne.Properties.expansions:
            self.Carcassonne.Refs(f'expansions/{expansion}').set(0)
        self.Carcassonne.Refs('feed_count').set(0)
            
        # Save player to lobby
        self._Save_connection_to_lobby()