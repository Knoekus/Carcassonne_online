#%% Imports
# PyQt6
import PyQt6.QtCore    as QtC
import PyQt6.QtGui     as QtG
import PyQt6.QtWidgets as QtW
import PyQt6_Extra     as QtE

# Custom classes
import Classes.Expansions #as Expansions
import Classes.Possessions #as Possessions
import Classes.Tiles #as Tiles
from Dialogs.YesNo import YesNoDialog

# Other packages
import random
import time

#%% Game screen functionality
class Game_screen_func():
    def __init__(self, Carcassonne):
        self.Carcassonne = Carcassonne
        self.game_vis = self.Carcassonne.game_vis
        self.Carcassonne.stacked_widget.addWidget(self.game_vis)
        self.Carcassonne.stacked_widget.setCurrentWidget(self.game_vis)
        
        # Client task: classes
        self.Classes_init()
        
        # Connect buttons
        self.Connect_buttons()
        
        # Admin task: set starting player
        self.Admin_starting_player()
    
    def Admin_starting_player(self):
        if self.Carcassonne.username == self.Carcassonne.Refs('admin').get():
            # Choose a random starting player
            for idx in range(50):
                player_list_dict = self.Carcassonne.Refs('connections').get()
                if type(player_list_dict) == type(dict()):
                    player_list = player_list_dict.keys()
                    break
                else:
                    time.sleep(0.1)
            else:
                raise Exception('No connections found after 5 seconds.')
            starting_player = random.choice(list(player_list))
            self._Feed_send_pass_turn(0, starting_player)
    
    def Connect_buttons(self):
        # Game buttons
        self.game_vis.leave_button.clicked.connect(self._Leave_game)
        self.game_vis.button_end_turn.clicked.connect(self._End_turn)
        
        # Meeple buttons
        for meeple_type in self.Carcassonne.meeples.keys():
            for meeple in self.Carcassonne.meeples[meeple_type]:
                meeple.clicked.connect(self._Meeple_clicked(meeple))
        
    def Classes_init(self):
        # Initialisations
        self.Carcassonne.Expansions  = Classes.Expansions.Expansions(self.Carcassonne)
        self.Carcassonne.Possessions = Classes.Possessions.Possessions(self.Carcassonne)
        self.Carcassonne.Tiles       = Classes.Tiles.Tiles(self.Carcassonne)
        
        # Calls
        self.Carcassonne.Expansions.Setup()
        self.Carcassonne.Possessions.Setup() # This needs material information gathered in the Expansions setup
    
    def _End_turn(self):
        previous_player = self.Carcassonne.username # this button can only be pressed by the player at turn
        
        # Get player list
        for idx in range(50):
            player_list_dict = self.Carcassonne.Refs('connections').get()
            if type(player_list_dict) == type(dict()):
                player_list = player_list_dict.keys()
                break
            else:
                time.sleep(0.1)
        else:
            raise Exception('No connections found after 5 seconds.')
        
        # Get previous player index
        previous_index = player_list.index(previous_player)
        if previous_index == len(player_list):
            next_player = player_list[0]
        else:
            next_player = player_list[previous_index+1]
        
        # Send feed message
        self._Feed_send_pass_turn(previous_player, next_player)
    
    def _End_turn_old(self, init=False):
        # Give turn to the next player
        if self.lobby.lobby_key == 'test2':
            next_player = self.current_player
        else:
            current_player_idx = self.player_list.index(self.current_player)
            next_player_idx = (current_player_idx + 1) % len(self.player_list)
            next_player = self.player_list[next_player_idx]
            
        if init == True:
            print('not switching player')
            self.Player_at_turn(self.current_player)
        else:
            self.Player_at_turn(next_player)

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
    
    def _Meeple_clicked(self, meeple):
        def clicked():
            # if meeple.meeple_type == 'standard':
            #     # In no instance can this meeple be placed on another tile but the
            #     # placed tile, so no need to highlight options before opening dialog.
            #     meepleWindow = Meeples.MeeplePlaceWindow(self.last_placed_tile, self, meeple)
            #     result = meepleWindow.exec()
            #     if result == QtW.QDialog.DialogCode.Accepted:
            #         meepleWindow.Meeple_placed()
            #         # meepleWindow.Meeple_placed_event()
            #         Meeples.En_dis_able_meeples(self, enable=False) # disable all meeples
            # else:
            #     raise Exception(f'Unknown meeple type: {meeple.meeple_type}')
            pass
        return clicked

    def _Take_new_tile(self, start_tile=False):
        if start_tile == True:
        # Place initial start tile
            if r'The River' not in self.Carcassonne.expansions:
                # Default start with tile H
                file = self.Carcassonne.Tiles.Choose_tile(1, 'H')[2]
                self._Feed_send_tile_taken(file, 1, 'H')
                # self.Carcassonne.Tiles.Place_tile(file, 1, 'H', 0, 0)
                self._Feed_send_tile_placed(0, 0, file, 1, 'H', 0)
            else:
                # Start with a spring
                file = self.Carcassonne.Tiles.Choose_tile(2, 'D')[2]
                self._Feed_send_tile_taken(file, 2, 'D')
                # self.Carcassonne.Tiles.Place_tile(file, 2, 'D', 0, 0)
                self._Feed_send_tile_placed(0, 0, file, 2, 'D', 0)
        
        # Take new tile
        if 2 in self.Carcassonne.tiles.keys():
        # If there are The River tiles left, take them first
            self.Carcassonne.Tiles.New_tile(2)
        else:
        # Take any tile
            self.Carcassonne.Tiles.New_tile()

    #%% Feed handling, sending
    def _Feed_send_player_left_game(self):
        # Make feed message
        event = {'event':'player_left_lobby',
                 'user':self.Carcassonne.username}
        
        # Send message to feed
        self.Carcassonne.feed.Event_send(event)
    
    def _Feed_send_pass_turn(self, previous_player, next_player):
        # Make feed message
        event = {'event':'pass_turn',
                 'previous_player':previous_player,
                 'next_player':next_player}
        
        # Send message to feed
        self.Carcassonne.feed.Event_send(event)
    
    def _Feed_send_tile_placed(self, row, col, file, tile_idx, tile_letter, rotation):
        # FIXME: event not implemented in feed
        # Do client visualisation for speed improvement
        self.game_vis.Tile_placed(row, col, file, tile_idx, tile_letter, rotation)
        
        # Make feed message
        event = {'event':'tile_taken',
                 'user':self.Carcassonne.username,
                 'row':row,
                 'col':col,
                 'file':file,
                 'tile_idx':tile_idx,
                 'tile_letter':tile_letter,
                 'rotation':rotation}
        
        # Send message to feed
        self.Carcassonne.feed.Event_send(event)
    
    def _Feed_send_tile_taken(self, file, tile_idx, tile_letter):
        # Do client visualisation for speed improvement
        self.game_vis.Tile_taken(self.Carcassonne.username, file, tile_idx, tile_letter)
        
        # Make feed message
        event = {'event':'tile_taken',
                 'user':self.Carcassonne.username,
                 'file':file,
                 'tile_idx':tile_idx,
                 'tile_letter':tile_letter}
        
        # Send message to feed
        self.Carcassonne.feed.Event_send(event)
    
    #%% Feed handling, receiving
    def _Feed_receive_pass_turn(self, data):
        # Import data
        previous_player = data['previous_player']
        next_player = data['next_player']
        
        if previous_player == self.Carcassonne.username:
            # Do stuff
            pass
        
        elif next_player == self.Carcassonne.username:
            # Take a new tile, send it to feed
            if self.Carcassonne.last_placed_tile == None:
            # Place start tile if there are no tiles yet
                self._Take_new_tile(start_tile=True)
            else:
                self._Take_new_tile()
            print('FEED RECEIVE EVENT: pass turn')