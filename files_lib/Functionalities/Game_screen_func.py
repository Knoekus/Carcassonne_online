#%% Imports
# PyQt6
import PyQt6.QtGui     as QtG
import PyQt6.QtWidgets as QtW
import PyQt6.QtCore    as QtC
import PyQt6_Extra     as QtE

# Custom classes
from Dialogs.YesNo import YesNoDialog

# Other packages
import random

#%% Game screen functionality
class Game_screen_func():
    def __init__(self, Carcassonne):
        self.Carcassonne = Carcassonne
        self.game_vis = self.Carcassonne.game_vis
        self.Carcassonne.stacked_widget.addWidget(self.game_vis)
        self.Carcassonne.stacked_widget.setCurrentWidget(self.game_vis)
        
        # Connect buttons
        self.Connect_buttons()
        
        # Client task: gather all necessary tiles
        self.Tiles_init()
        
        # Admin task: set starting player
        self.Admin_starting_player()
    
    def Admin_starting_player(self):
        if self.Carcassonne.username == self.Carcassonne.Refs('admin').get():
            # Choose a random starting player
            for idx in range(10):
                player_list_dict = self.Carcassonne.Refs('connections').get()
                if type(player_list_dict) == type(dict()):
                    player_list = player_list_dict.keys()
                    break
            else:
                raise Exception('No connections found after 10 tries.')
            starting_player = random.choice(list(player_list))
            self._Feed_send_pass_turn(0, starting_player)
    
    def Connect_buttons(self):
        # Game buttons
        self.game_vis.leave_button.clicked.connect(self._Leave_game)
        # self.game_vis.button_end_turn.clicked.connect(self._End_turn_old)
        self.game_vis.button_end_turn.clicked.connect(self._End_turn)
        
        # Meeple buttons, standard
        for idx in range(7):
            meeple = self.game_vis.meeples_standard[idx]
            meeple.clicked.connect(self._Meeple_clicked(meeple)) # connect function # FIXME: func
        
    def Tiles_init(self):
        pass
    
    def _End_turn(self):
        previous_player = self.Carcassonne.username # this button can only be pressed by the player at turn
        
        # Get player list
        for idx in range(10):
            player_list_dict = self.Carcassonne.Refs('connections').get()
            if type(player_list_dict) == type(dict()):
                player_list = player_list_dict.keys()
                break
        else:
            raise Exception('No connections found after 10 tries.')
        
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

    def _Take_new_tile(self):
        pass

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
    
    #%% Feed handling, receiving
    def _Feed_receive_pass_turn(self, data):
        # Import data
        previous_player = data['previous_player']
        next_player = data['next_player']
        
        if previous_player == self.Carcassonne.username:
            # Disable clickable stuff
            pass
        
        elif next_player == self.Carcassonne.username:
            # Take a new tile, send it to feed
            pass