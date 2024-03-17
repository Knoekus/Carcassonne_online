#%% Imports
# PyQt6
import PyQt6.QtCore    as QtC
import PyQt6.QtGui     as QtG
import PyQt6.QtWidgets as QtW
import PyQt6_Extra     as QtE

# Custom classes
import Visualisations.Menu_screen_vis as MenuVis
import Functionalities.Menu_screen_func as MenuFunc
from Dialogs.OK_dialog    import OKDialog
import Properties

# Other packages
import sys
import firebase_admin as fb

#%% Functions
def Firebase_init():
    # Firebase initialisation
    if not fb._apps: # only initialize if app doesn't exist
        # Initialize Firebase Admin SDK
        cred = fb.credentials.Certificate(r'..\SDK_KEY_KEEP_SAFE\clientserver1-firebase-adminsdk-roo18-d3927e4c28.json')
        fb.initialize_app(cred, {
            'databaseURL': 'https://clientserver1-default-rtdb.europe-west1.firebasedatabase.app/'
        })

class Carcassonne_online(QtW.QMainWindow):
    def closeEvent(self, event):
        title = None
        if self.stacked_widget.currentIndex() == 1:
        # Lobby index = 1, don't force exit out of it.
            title = 'Leave lobby before exiting'
            text = 'Please leave the lobby before exiting the game.'
        elif self.stacked_widget.currentIndex() >= 2:
        # Game index = 2, don't exit out of it at all.
            title = 'Cannot leave lobby'
            text = 'You cannot leave the lobby when the game is still going.'
        
        if title != None:
            event.ignore()
            OK_dialog = OKDialog(self, self, title, text)
            OK_dialog.exec()
        
        
    def __init__(self):
        super().__init__()
        self._Window_properties()
        self._Parameters()
        self._Layout()
        self.Menu()
        
    def _Window_properties(self):
        self.setWindowTitle('Menu')
        self.setGeometry(100, 100, 400, 300)
        self.showMaximized()
    
    def _Parameters(self):
        # Own choice
        self.test = True
        self.default_font_size = 5 # 0-15
        
        # Classes
        self.Properties = Properties.Properties(self.default_font_size)
    
    def _Layout(self):
        '''
        The main layout is a stacked widget, such that we can stack the lobby and game screens when they are ready.
        '''
        # Stacked 
        self.stacked_widget = QtW.QStackedWidget()
        self.setCentralWidget(self.stacked_widget)
    
    def Menu(self):
        # Visualisation
        self.menu_vis = MenuVis.Menu_screen_vis(self)
        
        # Functionality
        self.menu_func = MenuFunc.Menu_screen_func(self)
    
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
            prefix = f'lobbies/{self.lobby_key}'
            
        if load == 'get_set':
            return fb.db.reference(f'{prefix}/{key}')
        elif load == 'add_del':
            entries = fb.db.reference(f'{prefix}/{key}').get()
            if type(entries) == dict:
                entries = list(entries.keys())
            if item in entries: # item should be deleted
                entries.remove(item)
            else: # item should be added
                entries.append(item)
            fb.db.reference(f'{prefix}/{key}').set(entries)
        
#%% Main
if __name__ == '__main__':
    # Firebase initialisation
    Firebase_init()
    
    # Setup application
    app = QtW.QApplication(sys.argv)
    app.setStyle('Breeze') # ['Breeze', 'Oxygen', 'QtCurve', 'Windows', 'Fusion']
    app.setWindowIcon(QtG.QIcon(r'.\Images\Coin_icon.png'))
    
    # Open menu screen
    Carcassonne = Carcassonne_online()
    Carcassonne.show()
    Carcassonne.activateWindow()
    Carcassonne.raise_()
    sys.exit(app.exec())