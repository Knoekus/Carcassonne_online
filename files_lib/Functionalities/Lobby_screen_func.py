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
        self.feed = FeedFunc.Feed_func(self.Carcassonne)
    
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
            if True:
                self._Feed_send_colour_button_clicked(button_colour)
            else:
                player_colour_ref = self.lobby_vis.player_colour_ref
                
                # If new colour selected and it's still free or it's blank
                if button_colour != player_colour_ref.get() and\
                   (self.Carcassonne.Refs(f'colours/{button_colour}').get() == 0 or button_colour == self.lobby_vis.all_colours[0]):
                    # Remove checkmark from old selected colour
                    self.lobby_vis.colour_picker_buttons[player_colour_ref.get()].setIcon(QtG.QIcon())
                    
                    # Add checkmark to new selected colour
                    self.lobby_vis.colour_picker_buttons[button_colour].setIcon(QtG.QIcon(r'.\Images\checkmark_icon.png'))
                    self.lobby_vis.colour_picker_buttons[button_colour].setIconSize(QtC.QSize(50,50))
                    
                    # If current colour not blank, set old colour to be free and occupy new colour
                    colours_update = {}
                    if player_colour_ref.get() != self.lobby_vis.all_colours[0]:
                        colours_update[player_colour_ref.get()] = 0
                    if button_colour != self.lobby_vis.all_colours[0]:
                        colours_update[button_colour] = 1
                    # self.Carcassonne.Refs('colours').update(colours_update) # update to only cause 1 event change
                    
                    # Set selected colour
                    # self.Carcassonne.Refs(f'players/{self.Carcassonne.username}/colour').set(button_colour)
                    # player_colour_ref.set(button_colour)
                    
                    # FIXME: test
                    # Make the above code into an event push to the database, monitoring if everybody has processed the event and only then moving on to the next event.
                
        return select_new_colour
    
    def _Colour_picker_func(self):
        # Listener
        self.player_colours_updater = PlayerColoursUpdater(self.Carcassonne.Refs)
        self.player_colours_updater.updateSignal.connect(self.colour_picker_vis._Draw_colours)
        self.player_colours_updater.listen_for_updates()
        self.player_colours_updater.start()
    
    
    
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
        self.feed.Event_send(count, event)

    def _Feed_receive_colour_button_clicked(self, data):
        # Import data
        old_colour = data['old_colour']
        new_colour = data['new_colour']
        player_clicked = data['user']
        
        # Function
        if False: # old
            player_colour_ref = self.lobby_vis.player_colour_ref
            
            # If new colour selected and it's still free or it's blank
            if button_colour != player_colour_ref.get() and\
               (self.Carcassonne.Refs(f'colours/{button_colour}').get() == 0 or button_colour == self.lobby_vis.all_colours[0]):
                # Remove checkmark from old selected colour
                self.lobby_vis.colour_picker_buttons[player_colour_ref.get()].setIcon(QtG.QIcon())
                
                # Add checkmark to new selected colour
                self.lobby_vis.colour_picker_buttons[button_colour].setIcon(QtG.QIcon(r'.\Images\checkmark_icon.png'))
                self.lobby_vis.colour_picker_buttons[button_colour].setIconSize(QtC.QSize(50,50))
                
                # If current colour not blank, set old colour to be free and occupy new colour
                colours_update = {}
                if player_colour_ref.get() != self.lobby_vis.all_colours[0]:
                    colours_update[player_colour_ref.get()] = 0
                if button_colour != self.lobby_vis.all_colours[0]:
                    colours_update[button_colour] = 1
        else: # new
            if new_colour != self.lobby_vis.all_colours[0]:
            # If other than blank colour was clicked
                if self.Carcassonne.Refs(f'colours/{new_colour}').get() == 1:
                # If selected non-blank colour is occupied, don't do anything
                    return
                
            if self.Carcassonne.username == player_clicked:
            # This player changed the colour
                # Free up previously selected colour
                self.lobby_vis.colour_picker_buttons[old_colour].setIcon(QtG.QIcon())
                if old_colour != self.lobby_vis.all_colours[0]:
                # If the old colour was not blank
                    self.Carcassonne.Refs(f'colours/{old_colour}').set(0)
                
                # Occupy newly selected colour
                self.lobby_vis.colour_picker_buttons[new_colour].setIcon(QtG.QIcon(r'.\Images\checkmark_icon.png'))
                self.lobby_vis.colour_picker_buttons[new_colour].setIconSize(QtC.QSize(50,50))
                if new_colour != self.lobby_vis.all_colours[0]:
                # If the new colour is not blank
                    self.Carcassonne.Refs(f'colours/{new_colour}').set(1)
                    self.Carcassonne.Refs(f'players/{player_clicked}/colour').set(new_colour)
            else:
            # This player did not change the colour
                # Enable the old colour button
                self.lobby_vis.colour_picker_buttons[old_colour].setEnabled(True)
                
                # Disable the new colour button
                self.lobby_vis.colour_picker_buttons[new_colour].setEnabled(False)
        
        

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