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
        cred = fb.credentials.Certificate({
            'type': 'service_account',
            'project_id': 'clientserver1',
            'private_key_id': 'd3927e4c28b101022c7a60fb5db99c1c90cedb3f',
            'private_key': '-----BEGIN PRIVATE KEY-----\nMIIEvAIBADANBgkqhkiG9w0BAQEFAASCBKYwggSiAgEAAoIBAQCyBl5P0adDGBsK\nm42BD7nhuJB24/X/r3rIn+LQ2hMBFb5UlJbD5DIQDpO2uTFNEFZ1AvZrF+qJTMfc\nBPVIVKWfINl/1G1U2EE31XL+24K93TIkKw3Reci2psc+Ix5yLOc+gv8ZzotFknqo\nDm1+kZqSNnCnCbVVTLKhMs8OvpQApKPkMjC95zuP7jaIPariFkbuMS7An9qOJoLM\nxHWSJlT7cpwmkd9a2dJMNNZhDg+BtU5TYCC13LpRte7xaKd49v0FW7J2t1Msva9w\np3ojsBKztxhNIKRiolI4Ol9hg/dZ1YGRF0MBUJ/ExiPsJOs7VmnboTmUN0B34cpI\nOpOULSPJAgMBAAECggEABLFNSB5XIdofUFrEUpwXAr+qMzAUGm7GNkacpHOzH4qy\nrykRhk1cEndH5n+gMI9XMBNpam5BdOgMtpx82LC+guDLSubPEPb4VR/vvY8MtbOA\ncFqgLR7gLwxbYSRs14aee9PZJJWAr09Ko2Zp9XWiFOuRcZ28ZWi1prEfqxxT62Zg\nU3A2cEu/wkZLuvqsfyw2C6OM+OrLc6BrOE4tcNeK8P79og0j+UwtzIRmVyHWMCzb\nBoUQrHO//B47wSnJlN4Qv0ashGNOdCrWjXgdSzxp1ucvMJFrvxsQYIv4ghRQJNod\n8+BUJHcvY6oR0/q4WZnKLeHhdHNHBEVeKi23UM+0twKBgQDiY1nKpBsBCqIPfkwH\nz5AlxQ8+bsmoq4A6bFqToDSDM5ddnuLqJoWjGobohMID1nqOFGYCHUuc7Qiwxoj3\na9aruEsjgKKO2vnSZo4oFqzZ5o2FGowvgDVu25GgYjJQ22ICqqocDb9jcokzOpfR\nHK4FtHzmtLSn27utpAWeMvT/FwKBgQDJT5DqNjj+IRy7CnoM50uixqU4MnRogWGe\ncT+clrxHzyC6Cn7dua2adI7ne8xn14g5ogeAjDRIUGqTZIOM+yxgz3wHD5ibM0TB\nzQT6tuIEEpYcdYu9pG976H/8RFQP+0NvyR3w918rJ0TLo3dE5kAY66JiYlQRrMNt\nGi9BBvfAHwKBgFU+PaAs3LIus8kLsEs8n7VpFw1WH/6v3Q+inxR5PWytr3AkFKNA\nMA+zPFsvKfLR/sGi8qoXJ9KF+kC98PLhGyr7sOdEV3FdCLZtwVdc+mbuBhm5XlHA\nf94nNRVkBDgn8ya35me70XX7uaedh27I0sn5JRKltmSCO4/tc+QWoeOvAoGAP7du\nT6M/4LeMR2smfEUM/IVRL/tQOu+QfTys/Jv9FeFqI1hFFVq6puNzg7L8XHWsiUlO\nhJJbzfOd9+7dcFbjkfS59eYq0BynC4wfolcWLGHRn0pZI3oTSy2orKjXzoMhshT+\n5BD3z0nLjYS8sFMMQJb8O5WRtFJxPGwIPtW8vtMCgYA/uIGvgXHBwJxVxcsejcpP\ny0sWI6768o+M4Szw7wBymKkL0osWHJ4SEOs+BZNZmpTrAsMlKo5n8hKfBk/x/sbv\nGsOdKStbaGge4hLgpGqB22isHEklbQVIgPio8TQjw7pO41q9hfC+6ZoqZMJ3VMN0\nmRre/8Td4cXwElrWoWETAw==\n-----END PRIVATE KEY-----\n',
            'client_email': 'firebase-adminsdk-roo18@clientserver1.iam.gserviceaccount.com',
            'client_id': '108137925135950690842',
            'auth_uri': 'https://accounts.google.com/o/oauth2/auth',
            'token_uri': 'https://oauth2.googleapis.com/token',
            'auth_provider_x509_cert_url': 'https://www.googleapis.com/oauth2/v1/certs',
            'client_x509_cert_url': 'https://www.googleapis.com/robot/v1/metadata/x509/firebase-adminsdk-roo18%40clientserver1.iam.gserviceaccount.com',
            'universe_domain': 'googleapis.com'
            })
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
        # Ignore close event
            event.ignore()
            OK_dialog = OKDialog(self, self, title, text)
            OK_dialog.exec()
        else:
        # Properly exit the program
            sys.exit()
        
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
        self.test = False
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
