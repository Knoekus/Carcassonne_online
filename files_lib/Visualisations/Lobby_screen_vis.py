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

#%% Lobby screen visualisation
class Lobby_screen_vis(QtW.QWidget):
    def __init__(self, Carcassonne):
        self.Carcassonne = Carcassonne
        super().__init__()