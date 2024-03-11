#%% Imports
# PyQt6
import PyQt6.QtCore    as QtC

# Other packages
from firebase_admin import db

#%% Feed functionality
class Feed_func():
    def __init__(self, Carcassonne):
        self.Carcassonne = Carcassonne
        self.Refs = self.Carcassonne.Refs
        
        self.Feed_start()
        
    def Feed_start(self):
        # Thread for listener
        self.feed_listener = FeedUpdater(self)
        self.feed_listener.updateSignal.connect(self._Event_receive)
        self.feed_listener.listen_for_updates()
    
    def Event_send(self, event):
        # Update the feed count
        feed_count = self.Refs('feed_count').get()+1
        self.Refs('feed_count').set(feed_count)
        
        # Push event to each player
        connections = self.Refs('connections').get()
        for player in connections:
            self.Refs(f'players/{player}/feed/{feed_count}').set(event)
    
    def _Event_receive(self, event):
        # Receive
        if False:
            # This is how to get event information
            print('event received:', event.data)
            
            path = event.path[1:]
            print('event recalled:', self.Refs(f'players/{self.Carcassonne.username}/feed/{path}').get())
        
        # Check the event
        if event.data != None:
        # There is data, so get event path and perform the event
            path = event.path[1:]
        elif self.Carcassonne.lobby_key == None:
        # If the player has left the lobby, the lobby key is None.
            return
        else:
        # When an event is removed, data == None. The client should move on to the next event.
        # Check if there is a next event to be processed
            feed_count = self.Refs('feed_count').get()
            feed_events = self.Refs(f'players/{self.Carcassonne.username}/feed').get()
            if feed_count in feed_events:
            # If more events exists, perform the event with lowest count (the next one up)
                path = min(x for x in feed_events if isinstance(x, int))
                event.data = self.Refs(f'players/{self.Carcassonne.username}/feed/{path}').get()
            else:
            # No more event exists, so return
                return
        
        # Process the event
        if 'init' not in event.data.keys():
        # Ignore the initialisation
            event_type = event.data['event']
            
            if event_type == 'chat_message':
                '''A chat message was sent and should be visualised.'''
                self.Carcassonne.lobby_vis._Feed_receive_chat_message(event)
                
            elif event_type == 'colour_button_clicked':
                '''In the lobby, a colour button got clicked and should therefore be occupied.'''
                self.Carcassonne.lobby_vis._Feed_receive_colour_button_clicked(event.data)
                self.Carcassonne.lobby_func._Feed_receive_colour_button_clicked(event.data)
            
            elif event_type == 'expansion_clicked':
                '''The admin clicked an expansion, so everybody has to switch the state of said expansion.'''
                self.Carcassonne.lobby_vis._Feed_receive_expansions_update(event.data)
                
            elif event_type == 'new_admin':
                '''A new player got assigned the admin role, so the player list should be updated.'''
                self.Carcassonne.lobby_vis._Feed_receive_new_admin(event.data)
            
            elif event_type == 'player_joined':
                '''A new player joined the lobby and should be added to the players list.'''
                self.Carcassonne.lobby_vis._Feed_receive_player_joined(event.data)
            
            elif event_type == 'player_left':
                '''A player left the lobby and should be removed from the players list. 
                   If it was the admin, a new admin should be assigned'''
                self.Carcassonne.lobby_vis._Feed_receive_player_left(event.data)
                self.Carcassonne.lobby_func._Feed_receive_player_left(event.data)
                
            else:
                print('Unknown event type:', event_type)
            
            # Cleanup
            self.Refs(f'players/{self.Carcassonne.username}/feed/{path}').delete()

class FeedUpdater(QtC.QThread):
    updateSignal = QtC.pyqtSignal(db.Event)

    def __init__(self, Feed_func):
        super().__init__()
        self.Feed_func = Feed_func
    
    def listen_for_updates(self):
        self.Feed_func.Refs(f'players/{self.Feed_func.Carcassonne.username}/feed').listen(self.on_event)
        self.start()
    
    def on_event(self, event):
        self.updateSignal.emit(event)
