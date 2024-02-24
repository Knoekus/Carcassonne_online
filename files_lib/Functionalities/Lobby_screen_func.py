#%% Imports
# PyQt6
import PyQt6.QtGui     as QtG
import PyQt6.QtWidgets as QtW
import PyQt6.QtCore    as QtC
import PyQt6_Extra     as QtE

# Custom classes
import Functionalities.Feed_func as FeedFunc
# ...

# Other packages
# ...

#%% Lobby screen functionality
class Lobby_screen_func():
    def __init__(self, Carcassonne):
        self.Carcassonne = Carcassonne
        self.lobby_vis = self.Carcassonne.lobby_vis
        self.Carcassonne.stacked_widget.addWidget(self.lobby_vis)
        self.Carcassonne.stacked_widget.setCurrentWidget(self.lobby_vis)
        
        # Database feed
        self.Connect_feed()
        
        # Connect buttons
        self.Connect_buttons()
    
    def Connect_feed(self):
        self.Carcassonne.feed = FeedFunc.Feed_func(self.Carcassonne)
        
        # Send join event to feed
        self._Feed_send_player_joined()
    
    def Connect_buttons(self):
        # Colour picker buttons
        for colour in self.lobby_vis.colour_picker_buttons.keys():
            button = self.lobby_vis.colour_picker_buttons[colour]
            
            # Enable/disable according to currently picked colour
            if self.Carcassonne.Refs(f'colours/{colour}').get() == 1 and colour != self.lobby_vis.player_colour_ref.get(): # don't disable current colour
            # Selected by someone else, so disable
                button.setEnabled(False)
            else:
            # Not selected, so enable
                button.setEnabled(True)
                button.setCursor(QtG.QCursor(QtC.Qt.CursorShape.PointingHandCursor))
            
            # Connect function
            button.clicked.connect(self._Select_colour(colour))
    
    def _Select_colour(self, button_colour):
        """Function for all colour buttons. When a button is clicked, its colour is assigned to the player that selected it."""
        def select_new_colour():
            self._Feed_send_colour_button_clicked(button_colour)
        return select_new_colour
    
    # def _Colour_picker_func(self):
    #     # Listener
    #     self.player_colours_updater = PlayerColoursUpdater(self.Carcassonne.Refs)
    #     self.player_colours_updater.updateSignal.connect(self.colour_picker_vis._Draw_colours)
    #     self.player_colours_updater.listen_for_updates()
    #     self.player_colours_updater.start()
    
    
    #%% Feed handling
    def _Feed_send_player_joined(self):
        # Make feed message
        count = self.Carcassonne.Refs('feed_count').get() + 1
        event = {'event':'player_joined',
                 'user':self.Carcassonne.username}
        
        # Send message to feed
        self.Carcassonne.feed.Event_send(count, event)
        
    def _Feed_send_colour_button_clicked(self, button_colour):
        old_colour = self.lobby_vis.player_colour_ref.get()
        new_colour = button_colour
        
        if old_colour == new_colour:
        # No change, so don't do anything
            return
        
        # Make feed message
        count = self.Carcassonne.Refs('feed_count').get() + 1
        event = {'event':'colour_button_clicked',
                 'user':self.Carcassonne.username,
                 'old_colour':old_colour,
                 'new_colour':new_colour}
        
        # Send message to feed
        self.Carcassonne.feed.Event_send(count, event)

    def _Feed_receive_colour_button_clicked(self, data):
        # Import data
        old_colour = data['old_colour']
        new_colour = data['new_colour']
        player_clicked = data['user']
        
        # Function
        if self.Carcassonne.username == player_clicked:
        # This player changed the colour
            if new_colour != self.lobby_vis.all_colours[0] and self.Carcassonne.Refs(f'colours/{new_colour}').get() == 1:
            # If selected non-blank colour is occupied, don't do anything
                return
            
            # Free up previously selected colour
            if old_colour != self.lobby_vis.all_colours[0]:
            # If the old colour was not blank
                self.Carcassonne.Refs(f'colours/{old_colour}').set(0)
            
            # Occupy newly selected colour
            self.Carcassonne.Refs(f'players/{player_clicked}/colour').set(new_colour)
            if new_colour != self.lobby_vis.all_colours[0]:
            # If the new colour is not blank
                self.Carcassonne.Refs(f'colours/{new_colour}').set(1)
        else:
        # This player did not change the colour
            pass # only visualisation
        
        

class PlayerColoursUpdater(QtC.QThread):
    updateSignal = QtC.pyqtSignal(list)

    def __init__(self, refs):
        super().__init__()
        self.Refs = refs

    def run(self):
        # Get list of colours
        # --> could try doing something smart with only updating necessary colours
        colours = self.Refs('colours').get()
        self.updateSignal.emit(list(colours.keys()))
    
    def listen_for_updates(self):
        # when these references update, they trigger a function
        self.Refs('colours').listen(self.on_player_colours_update)
    
    def on_player_colours_update(self, event):
        if event.data is not None:
            self.run()