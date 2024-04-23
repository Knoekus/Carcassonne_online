#%% Imports
# PyQt6
import PyQt6.QtCore    as QtC
import PyQt6.QtGui     as QtG
import PyQt6.QtWidgets as QtW
import PyQt6_Extra     as QtE

# Custom classes
# ...

# Other packages
# ...

#%% Meeple placement screen functionality
class Meeple_placement_screen_func():
    def __init__(self, Carcassonne):
        self.Carcassonne = Carcassonne
        self.meeple_vis = self.Carcassonne.meeple_vis
        
        # Connect buttons
        self.Connect_buttons()
    
    def Connect_buttons(self):
        self.meeple_vis.y_button.clicked.connect(self._Accepted)
        self.meeple_vis.n_button.clicked.connect(self._Closed)
    
    def _Accepted(self):
        # Re-enable leave button
        self.Carcassonne.game_vis.button_end_turn.setEnabled(True)
        
        # Send feed message
        self._Feed_send_meeple_placed()
        
        # Accept dialog box
        self.meeple_vis.accept()
    
    def _Closed(self):
        # Re-enable buttons
        self.Carcassonne.game_vis.button_end_turn.setEnabled(True)
        self.Carcassonne.game_vis._Meeples_enable(True)
        
        # Close dialog box
        self.meeple_vis.close()

    #%% Feed handling, sending
    def _Feed_send_meeple_placed(self):
        # Package original tile info
        og_tile = self.meeple_vis.original_tile
        og_tile_info = (og_tile.index, og_tile.letter, og_tile.coords, og_tile.file, og_tile.rotation)
        
        # Do client visualisation for speed improvement
        self.meeple_vis._Meeple_placed() # make meeple unavailable to client
        self.Carcassonne.game_vis.Meeple_placed(self.Carcassonne.username, self.meeple_vis.meeple.meeple_type, og_tile_info, self.meeple_vis.sub_length, self.meeple_vis.sub_tile_selected)
        
        # Make feed message
        event = {'event':'meeple_placed',
                 'user':self.Carcassonne.username,
                 'meeple_type':self.meeple_vis.meeple.meeple_type,
                 'og_tile_info':og_tile_info,
                 'sub_length':self.meeple_vis.sub_length,
                 'sub_tile':self.meeple_vis.sub_tile_selected}
        
        # Send message to feed
        self.Carcassonne.feed.Event_send(event)