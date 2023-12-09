import sys
if __name__ != '__main__': # regular call
    import PyQt5.QtGui     as QtG
    import PyQt5.QtWidgets as QtW
    import PyQt5.QtCore    as QtC
    import PyQt5_Extra     as QtE
    from firebase_admin import db

    import time
    import sys
    import prop_s

    if r"..\Dialogs" not in sys.path:
        sys.path.append(r"..\Dialogs")
    from Dialogs.YesNo import YesNoDialog
    
else: # direct test call
    import PyQt5.QtGui     as QtG
    import PyQt5.QtWidgets as QtW
    import PyQt5.QtCore    as QtC
    
    import firebase_admin
    from firebase_admin import credentials, db
    
    if r"..\..\files_lib" not in sys.path:
        sys.path.append(r"..\..\files_lib")
    import PyQt5_Extra
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

#%% Game screen
# class GameScreen(QtW.QMainWindow):
class GameScreen(QtW.QWidget):
    #%% Visuals
    def __init__(self, lobby):
        super().__init__()
        self.menu_screen = lobby.menu_screen
        self.lobby = lobby
        
        self._Game_init()
        self._Game_layout()
        
        # self.mainWidget = QtW.QWidget()
        # self.mainWidget.setLayout(self.mainLayout)
        # self.setCentralWidget(self.mainWidget)
        self.setLayout(self.mainLayout)
        self.showMaximized()
        print("Hallo")
    
    def _Game_init(self):
        self.setWindowTitle('Carcassonne Online')
        
        # References from lobby
        self.username = self.lobby.username
        self.Refs = self.lobby.Refs
        self.font_size = self.lobby.font_size
    
    def _Game_layout(self):
        self.mainLayout = QtW.QGridLayout()
        
        if __name__ != '__main__':
            image = QtG.QPixmap(r'.\Images\tile_logo.png')
        else:
            image = QtG.QPixmap(r'..\Images\tile_logo.png')
        label = QtW.QLabel()
        label.setPixmap(image)
        
        self.mainLayout.addWidget(label, 0, 0, 1, 1)
        
        self.leave_button = QtW.QPushButton('Leave')
        self.mainLayout.addWidget(self.leave_button, 1, 0, 1, 1)
    
    #%% Functionality
    def closeEvent(self, event):
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
            
        def remove_connection(self, username):
            None
        
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
    game_screen.show()
    game_screen.activateWindow()
    game_screen.raise_() # raise to top
    sys.exit(app.exec_())