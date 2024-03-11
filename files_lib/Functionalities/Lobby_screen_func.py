#%% Imports
# PyQt6
import PyQt6.QtGui     as QtG
import PyQt6.QtWidgets as QtW
import PyQt6.QtCore    as QtC
import PyQt6_Extra     as QtE

# Custom classes
import Functionalities.Feed_func as FeedFunc
from Dialogs.YesNo import YesNoDialog

# Other packages
import random

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
        
        # Player list buttons
        for username_label in self.lobby_vis.player_list_usernames.values():
            # username = username_label.text()
            username_label.clicked.connect(self._New_admin_clicked(username_label))
        
        # Expansion buttons
        for expansion_switch in self.lobby_vis.expansions_switches.values():
            expansion = expansion_switch.text()
            expansion_switch.clicked.connect(self._Expansions_clicked(expansion))
        
        # Lobby buttons
        self.lobby_vis.leave_button.clicked.connect(self._Leave_lobby)
        self.lobby_vis.start_button.clicked.connect(self._Start_game)
        
        # For testing: add player button
        if self.Carcassonne.test == True:
            self.lobby_vis.add_player_button.clicked.connect(self._Add_player_testing)
            
            self.lobby_vis.send_button.clicked.connect(self._Feed_send_chat_message)
            self.lobby_vis.chat_input.returnPressed.connect(self.lobby_vis.send_button.click)
    
    def _Expansions_clicked(self, expansion):
        def clicked():
            # Function
            button = self.lobby_vis.expansions_switches[expansion]
            state = button.checkState()
            if state == QtC.Qt.CheckState.Unchecked: # unchecked
                self.Carcassonne.Refs(f'expansions/{expansion}').set(0)
            elif state == QtC.Qt.CheckState.Checked: # checked
                self.Carcassonne.Refs(f'expansions/{expansion}').set(1)
            else:
                raise Warning('CheckState not implemented:', state)
            
            # Send feed event
            self._Feed_send_expansions_update(expansion)
            
        return clicked
    
    def _Leave_lobby(self, close_event=False):
        title = 'Leave lobby?'
        text = 'Are you sure you want to leave the lobby?'
        yesNoDialog = YesNoDialog(self.Carcassonne, self.lobby_vis, title, text)
        result = yesNoDialog.exec()
        if result == QtW.QDialog.DialogCode.Accepted:
            self._Feed_send_player_left()
            self.Carcassonne.stacked_widget.setCurrentWidget(self.Carcassonne.menu_vis) # Go back to menu screen
        
        if close_event == True:
            return result
    
    def _New_admin_clicked(self, username_label):
        def clicked():
            new_admin = username_label.text()
            self.Carcassonne.Refs('admin').set(new_admin)
            self._Feed_send_new_admin(new_admin)
        return clicked
            
    def _Select_colour(self, button_colour):
        """Function for all colour buttons. When a button is clicked, its colour is assigned to the player that selected it."""
        def select_new_colour():
            self._Feed_send_colour_button_clicked(button_colour)
        return select_new_colour
    
    def _Start_game(self):
        if self.Carcassonne.test == True:
            self.lobby_vis.chat_input.setText('--> Game started!')
            self._Feed_send_chat_message()
    
    def _Add_player_testing(self):
        # When testing
        username = 'user2'
        idx = 2*int(username[-1]) # user1: orange, user2: green
        blank_colour = self.Carcassonne.Properties.colours[idx]
        
        self.Carcassonne.Refs(f'colours/{blank_colour}').set(1)
            
        # Player attributes
        self.Carcassonne.Refs(f'connections/{username}').set(0)
        self.Carcassonne.Refs(f'players/{username}/colour').set(blank_colour)
        self.Carcassonne.Refs(f'players/{username}/points').set(0)
        self.Carcassonne.Refs(f'players/{username}/feed').set({'init':True})
        
        # Disable button
        self.lobby_vis.add_player_button.setEnabled(False)
        
        # Make feed message
        event = {'event':'player_joined',
                 'user':'user2'}
        
        # Send message to feed
        self.Carcassonne.feed.Event_send(event)
    
    #%% Feed handling, sending
    def _Feed_send_chat_message(self):
        message = self.lobby_vis.chat_input.text().strip()
        if len(message)>0:
            # Make feed message
            event = {'event':'chat_message',
                     'user':self.Carcassonne.username,
                     'message':message}
            
            # Send message to feed
            self.Carcassonne.feed.Event_send(event)
            
            # Database
            if self.Carcassonne.Refs('chat').push(message):
                self.lobby_vis.chat_input.clear()
        
    def _Feed_send_colour_button_clicked(self, button_colour):
        old_colour = self.lobby_vis.player_colour_ref.get()
        new_colour = button_colour
        
        if old_colour == new_colour:
        # No change, so don't do anything
            return
        
        # Make feed message
        event = {'event':'colour_button_clicked',
                 'user':self.Carcassonne.username,
                 'old_colour':old_colour,
                 'new_colour':new_colour}
        
        # Send message to feed
        self.Carcassonne.feed.Event_send(event)
    
    def _Feed_send_expansions_update(self, expansion):
        # Make feed message
        event = {'event':'expansion_clicked',
                 'expansion':expansion}
        
        # Send message to feed
        self.Carcassonne.feed.Event_send(event)
    
    def _Feed_send_new_admin(self, new_admin):
        # Make feed message
        event = {'event':'new_admin',
                 'new_admin':new_admin}
        
        # Send message to feed
        self.Carcassonne.feed.Event_send(event)
        
    def _Feed_send_player_joined(self):
        # Make feed message
        event = {'event':'player_joined',
                 'user':self.Carcassonne.username}
        
        # Send message to feed
        self.Carcassonne.feed.Event_send(event)
    
    def _Feed_send_player_left(self):
        # Make feed message
        event = {'event':'player_left',
                 'user':self.Carcassonne.username}
        
        # Send message to feed
        self.Carcassonne.feed.Event_send(event)

    #%% Feed handling, receiving
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
    
    def _Feed_receive_player_left(self, data):
        # Import data
        player_left = data['user']
        
        # Function
        conns = self.Carcassonne.Refs('connections').get()
        if conns == None:
            return
        else:
            lobby_conns = list(conns.keys())
        
        if player_left not in lobby_conns:
        # Double check to make sure the player who left is still in the database
            if player_left == self.Carcassonne.username:
            # Remove link to lobby if you are the player who left
                self.Carcassonne.lobby_key = None
            return
        
        if len(lobby_conns) > 1:
        # If there are more connections, only remove the one
            # Make colour available again
            colour = self.Carcassonne.Refs(f'players/{player_left}/colour').get()
            if colour != self.Carcassonne.Properties.colours[0]:
            # If colour was not transparent
                self.Carcassonne.Refs(f'colours/{colour}').set(0) # available again
            
            # Delete data from database
            self.Carcassonne.Refs(f'connections/{player_left}').delete()
            self.Carcassonne.Refs(f'players/{player_left}').delete()
            
            # If the lost connection was admin, choose a random new admin
            if self.Carcassonne.Refs('admin').get() == player_left:
                lobby_conns.remove(player_left)
                new_admin = random.choice(lobby_conns)
                self.Carcassonne.Refs('admin').set(new_admin)
                self._Feed_send_new_admin(new_admin)

        else:
        # Lost connection was the only one in the lobby, so remove it
            self.Carcassonne.Refs(f'lobbies/{self.Carcassonne.lobby_key}', prefix='').delete()
        
        if player_left == self.Carcassonne.username:
        # Remove link to lobby if you are the player who left
            self.Carcassonne.lobby_key = None