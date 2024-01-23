#%% Imports
# PyQt6
import PyQt6.QtGui     as QtG
import PyQt6.QtWidgets as QtW
import PyQt6.QtCore    as QtC
import PyQt6_Extra     as QtE

# Custom classes
# ...

# Other packages
# ...

#%% Menu screen visualisation
class Menu_screen_vis(QtW.QWidget):
    def __init__(self, Carcassonne):
        super().__init__()
        self.Carcassonne = Carcassonne
        
        self.Window_properties()
        self.Parameters()
        self.Layout()
        
    def Window_properties(self):
        self.setWindowTitle('Menu')
    
    def Parameters(self):
        # Presets
        # ...
        pass
    
    def Layout(self):
        # Layout
        self.main_layout = QtW.QGridLayout()
        self.setLayout(self.main_layout)
        self.main_layout.setColumnStretch(0, 1) # equal-sized columns
        self.main_layout.setColumnStretch(1, 1) # equal-sized columns
        self.main_layout.setRowStretch(0, 1) # center vertically
        self.main_layout.setRowStretch(100, 1) # center vertically
        
        # Components
        self._Title()
        self._Create_lobby()
        self._Join_lobby()
        self._Close()
        
        # Insert components
        self.main_layout.addWidget(self.title_label,         1, 0, 1, 2)
        self.main_layout.addWidget(QtE.QHSeparationLine(),   2, 0, 1, 2)
        self.main_layout.addWidget(self.create_lobby_button, 3, 0, 1, 2)
        self.main_layout.addWidget(self.lobby_key_input,     4, 0, 1, 1)
        self.main_layout.addWidget(self.join_lobby_button,   4, 1, 1, 1)
        self.main_layout.addWidget(QtE.QHSeparationLine(),   5, 0, 1, 2)
        self.main_layout.addWidget(self.close_button,        6, 0, 1, 2)
    
    def _Title(self):
        # Label
        text = 'Menu'
        font = self.Carcassonne.Properties.Font(size=6, bold=True)
        alignment = 'center'
        self.title_label = QtE.QLabel(text, font, alignment)
        self.title_label.setStyleSheet("padding:10")
    
    def _Create_lobby(self):
        # Button
        self.create_lobby_button = QtW.QPushButton('Create lobby')
        font = self.Carcassonne.Properties.Font(size=0, bold=False)
        self.create_lobby_button.setFont(font)
    
    def _Join_lobby(self):
        # Button
        self.join_lobby_button = QtW.QPushButton('Join lobby')
        font = self.Carcassonne.Properties.Font(size=0, bold=False)
        self.join_lobby_button.setFont(font)
        # TODO: functionality: self.join_lobby_button.clicked.connect(self.join_lobby)
        
        # Line edit
        self.lobby_key_input = QtW.QLineEdit(alignment=QtC.Qt.AlignmentFlag.AlignCenter)
        font = self.Carcassonne.Properties.Font(size=0, bold=False)
        self.lobby_key_input.setFont(font)
        self.lobby_key_input.setPlaceholderText('Enter lobby key...')
        # TODO: functionality: self.lobby_key_input.returnPressed.connect(self.join_lobby_button.click)
        
    def _Close(self):
        # Button
        self.close_button = QtW.QPushButton('Close program')
        font = self.Carcassonne.Properties.Font(size=0, bold=False)
        self.close_button.setFont(font)
        # TODO: functionality: self.close_button.clicked.connect(self.close)