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

#%% Lobby screen functionality
class Lobby_screen_func():
    def __init__(self, Carcassonne):
        self.Carcassonne = Carcassonne
        self.lobby_vis = self.Carcassonne.lobby_vis
        self.Carcassonne.stacked_widget.addWidget(self.lobby_vis)
        self.Carcassonne.stacked_widget.setCurrentWidget(self.lobby_vis)
        
        # Connect buttons
        self.Connect_buttons()
    
    def Connect_buttons(self):
        # Colour picker buttons
        for colour in self.lobby_vis.colour_picker_buttons.keys():
            button = self.lobby_vis.colour_picker_buttons[colour]
            button.clicked.connect(self.Select_colour(colour))
    
    def _Select_colour(self, button_colour):
        """Function for all colour buttons. When a button is clicked, its colour is assigned to the player that selected it."""
        def select_new_colour():
            current_colour = self.current_colour.get()
            
            # If new colour selected and it's still free or it's blank
            if button_colour != current_colour and\
               (self.Carcassonne.Refs(f'colours/{button_colour}').get() == 0 or button_colour == self.all_colours[0]):
                # Remove checkmark from old selected colour
                self.colour_picker_buttons[current_colour].setIcon(QtG.QIcon())
                
                # Add checkmark to new selected colour
                self.colour_picker_buttons[button_colour].setIcon(QtG.QIcon(r'.\Images\checkmark_icon.png'))
                self.colour_picker_buttons[button_colour].setIconSize(QtC.QSize(50,50))
                
                # If current colour not blank, set old colour to be free and occupy new colour
                colours_update = {}
                if current_colour != self.all_colours[0]:
                    colours_update[current_colour] = 0
                if button_colour != self.all_colours[0]:
                    colours_update[button_colour] = 1
                self.Carcassonne.Refs('colours').update(colours_update) # update to only cause 1 event change
                
                # Set selected colour
                self.Carcassonne.Refs(f'players/{self.Carcassonne.username}/colour').set(button_colour)
                self.current_colour.set(button_colour)
        return select_new_colour
    
    def _Colour_picker_func(self):
        # Listener
        self.player_colours_updater = PlayerColoursUpdater(self.Carcassonne.Refs)
        self.player_colours_updater.updateSignal.connect(self.colour_picker_vis._Draw_colours)
        self.player_colours_updater.listen_for_updates()
        self.player_colours_updater.start()

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