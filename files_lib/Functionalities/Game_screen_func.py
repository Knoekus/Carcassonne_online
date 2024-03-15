#%% Imports
# PyQt6
import PyQt6.QtGui     as QtG
import PyQt6.QtWidgets as QtW
import PyQt6.QtCore    as QtC
import PyQt6_Extra     as QtE

# Custom classes
from Dialogs.YesNo import YesNoDialog

# Other packages
# ...

#%% Game screen functionality
class Game_screen_func():
    def __init__(self, Carcassonne):
        self.Carcassonne = Carcassonne
        self.game_vis = self.Carcassonne.game_vis
        self.Carcassonne.stacked_widget.addWidget(self.game_vis)
        self.Carcassonne.stacked_widget.setCurrentWidget(self.game_vis)
        
        # Connect buttons
        self.Connect_buttons()
    
    def Connect_buttons(self):
        # Game buttons
        self.game_vis.leave_button.clicked.connect(self._Leave_game)
    
    def _Leave_game(self, close_event=False):
        title = 'Leave game?'
        text = 'Are you sure you want to leave the game?'
        yesNoDialog = YesNoDialog(self.Carcassonne, self.game_vis, title, text)
        result = yesNoDialog.exec()
        if result == QtW.QDialog.DialogCode.Accepted:
            self._Feed_send_player_left_game()
            self.Carcassonne.stacked_widget.setCurrentWidget(self.Carcassonne.menu_vis) # Go back to menu screen
        
        if close_event == True:
            return result

    #%% Feed handling, sending
    def _Feed_send_player_left_game(self):
        # Make feed message
        event = {'event':'player_left_lobby',
                 'user':self.Carcassonne.username}
        
        # Send message to feed
        self.Carcassonne.feed.Event_send(event)
    
    #%% Feed handling, receiving
    