#%% Imports
import sys
import string
import random
import time
import firebase_admin
from firebase_admin import credentials, db

import PyQt5.QtGui     as QtG
import PyQt5.QtWidgets as QtW
import PyQt5.QtCore    as QtC
import PyQt5_Extra     as QtE

import prop_s
from Screens.Lobby    import LobbyScreen
from Dialogs.Username import UsernameDialog
from Dialogs.YesNo    import YesNoDialog

#%% Scaling
if hasattr(QtC.Qt, 'AA_EnableHighDpiScaling'):
    QtW.QApplication.setAttribute(QtC.Qt.AA_EnableHighDpiScaling, True)

if hasattr(QtC.Qt, 'AA_UseHighDpiPixmaps'):
    QtW.QApplication.setAttribute(QtC.Qt.AA_UseHighDpiPixmaps, True)

#%% Code
class MenuScreen(QtW.QMainWindow):
    #%% Visuals
    def _Menu_init(self):
        #%% Window settings
        self.setWindowTitle('Menu')
        self.setGeometry(100, 100, 400, 300)
        self.showMaximized()
        self.font_size = 5 # 0-15
        
        #%% Firebase reference preparation
        self.refs = {
            'lobbies':db.reference('lobbies'),
            }
        
    def _Menu_title(self):
        self.title_label = QtW.QLabel('Menu')
        self.title_label.setStyleSheet("padding:10") 
        self.title_label.setAlignment(QtC.Qt.AlignCenter)
        self.title_label.setFont(QtG.QFont(prop_s.font, prop_s.font_sizes[6+self.font_size], QtG.QFont.Bold)) # size 20
    
    def _Menu_lobby(self):
        self.create_lobby_button = QtW.QPushButton('Create lobby')
        self.create_lobby_button.setFont(QtG.QFont(prop_s.font, prop_s.font_sizes[0+self.font_size]))
        self.create_lobby_button.clicked.connect(self.create_lobby)

        self.join_lobby_button = QtW.QPushButton('Join lobby')
        self.join_lobby_button.setFont(QtG.QFont(prop_s.font, prop_s.font_sizes[0+self.font_size]))
        self.join_lobby_button.clicked.connect(self.join_lobby)

        self.lobby_key_input = QtW.QLineEdit()
        self.lobby_key_input.setFont(QtG.QFont(prop_s.font, prop_s.font_sizes[0+self.font_size]))
        self.lobby_key_input.setAlignment(QtC.Qt.AlignCenter)
        self.lobby_key_input.setPlaceholderText('Enter lobby key...')
        self.lobby_key_input.returnPressed.connect(self.join_lobby_button.click)
    
    def _Menu_close(self):
        self.close_button = QtW.QPushButton('Close program')
        self.close_button.setFont(QtG.QFont(prop_s.font, prop_s.font_sizes[0+self.font_size]))
        self.close_button.clicked.connect(self.close)
        
    def __init__(self, test):
        super().__init__()
        self.test = test
        
        self._Menu_init()
        self._Menu_title()
        self._Menu_lobby()
        self._Menu_close()

        layout = QtW.QGridLayout()
        layout.setColumnStretch(0, 1) # equal-sized columns
        layout.setColumnStretch(1, 1) # equal-sized columns
        layout.addWidget(self.title_label,         1, 0, 1, 2)
        layout.addWidget(QtE.QHSeparationLine(),   2, 0, 1, 2)
        layout.addWidget(self.create_lobby_button, 3, 0, 1, 2)
        layout.addWidget(self.lobby_key_input,     4, 0, 1, 1)
        layout.addWidget(self.join_lobby_button,   4, 1, 1, 1)
        layout.addWidget(QtE.QHSeparationLine(),   5, 0, 1, 2)
        layout.addWidget(self.close_button,        6, 0, 1, 2)
        
        layout.setRowStretch(0, 1)
        layout.setRowStretch(100, 1)
        
        self.mainWidget = QtW.QWidget()
        self.mainWidget.setLayout(layout)
        self.setCentralWidget(self.mainWidget)
    
    def closeEvent(self, event):
        if self.test != 1:
            title = 'Close program?'
            text = 'Are you sure you want to close the program?'
            yesNoDialog = YesNoDialog(self, title, text)
            result = yesNoDialog.exec_()
            
            # Ignore if not accepted, else continue (close)
            if result != QtW.QDialog.Accepted:
                event.ignore()

    #%% Functionality
    def create_lobby(self):
        if self.test == True: # test mode
            self.lobby_key = 'test'
            self.username = 'user1'
            
            self.save_lobby_to_database()
            self.open_lobby_screen()
        else:
            # Open the username dialog
            username_dialog = UsernameDialog(self)
            
            # In the meantime, create the actual lobby
            self.lobby_key = self.generate_lobby_key()
            
            # Retrieve username info
            result = username_dialog.exec_()
            if result == QtW.QDialog.Accepted:
                self.username = username_dialog.get_username()
                self.save_lobby_to_database()
                self.open_lobby_screen()
            else:
                # User canceled the username dialog
                pass

    def join_lobby(self):
        if self.test == True: # test mode
            self.lobby_key = 'test'
            self.username = 'user2'
            
            self.save_connection_to_lobby()
            self.open_lobby_screen()
        else:
            lobby_key = self.lobby_key_input.text().strip().upper()
            if lobby_key in self.Refs('', prefix='lobbies').get():
                # In the meantime, create the references to the lobby
                self.lobby_key = lobby_key
                if self.Refs('open').get() == True:
                    username_dialog = UsernameDialog(self)
                    result = username_dialog.exec_()
                    if result == QtW.QDialog.Accepted:
                        self.username = username_dialog.get_username()
                        if not self.is_username_taken():
                            self.save_connection_to_lobby()
                            self.open_lobby_screen()
                        else:
                            QtW.QMessageBox.warning(self, 'Username taken', 'That username is already taken in the lobby. Please choose a different username.')
                    else:
                        # User canceled the username dialog
                        pass
                else:
                    QtW.QMessageBox.warning(self, 'Lobby closed', 'The specified lobby is not open to new users.')
            else:
                QtW.QMessageBox.warning(self, 'Invalid lobby key', 'Please enter a valid lobby key.')
    
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
        
    def is_username_taken(self):
        if self.username in self.Refs('connections').get():
            return True
        else: return False

    def generate_lobby_key(self):
        if self.test == True: # test mode
            return 'testLobby'
        
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

    def save_lobby_to_database(self):
        self.Refs('open').set(True)
        self.Refs('admin').set(self.username)
        for colour in prop_s.colours[1:]:
            self.Refs(f'colours/{colour}').set(0)
        for expansion in prop_s.expansions:
            self.Refs(f'expansions/{expansion}').set(0)
        self.save_connection_to_lobby()

    def save_connection_to_lobby(self):
        self.Refs(f'connections/{self.username}').set(0)
        self.Refs(f'players/{self.username}/colour').set(prop_s.colours[0]) # start with blank colour

    def remove_connection(self, username):
        time.sleep(random.randint(0, 10)/10) # hopefully make removing multiple connections more asynchronous
        lobby_conns = list(self.Refs('connections').get().keys())
        # If there are more connections, only remove the one
        if len(lobby_conns) > 1:
            # Make colour available again
            colour = self.Refs(f'players/{username}/colour').get()
            if colour != prop_s.colours[0]:
                self.Refs(f'colours/{colour}').set(0) # available again
            
            self.Refs(f'connections/{username}').delete()
            self.Refs(f'players/{username}').delete()
            
            # If the lost connection was admin, choose a random new admin
            if self.Refs('admin').get() == username:
                lobby_conns.remove(username)
                self.Refs('admin').set(random.choice(lobby_conns))
        # Lost connection was the only one in the lobby, so remove it
        else:
            self.Refs(f'lobbies/{self.lobby_key}', prefix='').delete()

    def open_lobby_screen(self):
        lobby_screen = LobbyScreen(self)
        self.hide()
        lobby_screen.show()

#%% Firebase initialization
def FirebaseInit():
    if not firebase_admin._apps: # only initialize if app doesn't exist
        # Initialize Firebase Admin SDK
        cred = credentials.Certificate(r'..\SDK_KEY_KEEP_SAFE\clientserver1-firebase-adminsdk-roo18-d3927e4c28.json')
        firebase_admin.initialize_app(cred, {
            'databaseURL': 'https://clientserver1-default-rtdb.europe-west1.firebasedatabase.app/'
        })

#%% Main
if __name__ == '__main__':
    FirebaseInit()
    
    app = QtW.QApplication(sys.argv)
    app.setStyle('Breeze') # ['Breeze', 'Oxygen', 'QtCurve', 'Windows', 'Fusion']
    app.setWindowIcon(QtG.QIcon(r'.\Images\Coin_icon.png'))
    
    menu_screen = MenuScreen(test=1)
    menu_screen.show()
    menu_screen.activateWindow()
    menu_screen.raise_() # raise to top
    sys.exit(app.exec_())