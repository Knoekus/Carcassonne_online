#%% Imports
# PyQt6
import PyQt6.QtCore    as QtC

# Custom classes
import Functionalities.Lobby_screen_func as LobbyFunc

#%% Feed functionality
class Feed_func():
    def __init__(self, Carcassonne):
        self.Carcassonne = Carcassonne
        self.Refs = self.Carcassonne.Refs
        
    # def Feed_start(self):
        self.Refs(f'players/{self.Carcassonne.username}/feed').listen(self._Event_receive)
    
    def Event_send(self, count, event):
        # Update the feed count
        feed_count = self.Refs('feed_count').get()
        self.Refs('feed_count').set(feed_count+1)
        
        # Push event to each player
        connections = self.Refs('connections').get()
        for player in connections:
            self.Refs(f'players/{player}/feed/{count}').set(event)
    
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
        else:
        # When an event is removed, data == None. The client should move on to the next event
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
            if event.data['event'] == 'player_joined':
                '''A new player joined the lobby and should be added to the players list.'''
                self.Carcassonne.lobby_vis._Feed_receive_player_joined(event.data)
                
            elif event.data['event'] == 'colour_button_clicked':
                '''In the lobby, a colour button got clicked and should therefore be occupied.'''
                self.Carcassonne.lobby_vis._Feed_receive_colour_button_clicked(event.data)
                self.Carcassonne.lobby_func._Feed_receive_colour_button_clicked(event.data)
                
            else:
                print('unknown event type:', event.data['event'])
            
            # Cleanup
            self.Refs(f'players/{self.Carcassonne.username}/feed/{path}').delete()
        
        
        
        # self.Refs('feed').set(0)
        
        # self.Refs('feed').push({'type':'init'})
        
        # # Listener
        # self.feed_listener = FeedUpdater(self.Refs)
        # self.feed_listener.updateSignal.connect()
        # self.feed_listener.listen_for_updates()
        # self.feed_listener.start()

# class FeedUpdater(QtC.QThread):
#     updateSignal = QtC.pyqtSignal(list)

#     def __init__(self, refs):
#         super().__init__()
#         self.Refs = refs

#     def run(self):
#         # Get list of colours
#         self.updateSignal.emit()
    
#     def listen_for_updates(self):
#         # when these references update, they trigger a function
#         self.Refs('colours').listen(self.on_player_colours_update)
    
#     def on_player_colours_update(self, event):
#         if event.data is not None:
#             self.run()