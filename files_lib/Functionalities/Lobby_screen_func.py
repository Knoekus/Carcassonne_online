# Lobby screen functionality
class Lobby_screen_func():
    def __init__(self, Carcassonne):
        self.Carcassonne = Carcassonne
        self.lobby_vis = self.Carcassonne.lobby_vis
        
        # Set lobby to be visible
        self.Carcassonne.setWindowTitle(f'Lobby - {self.Carcassonne.lobby_key}')
        self.Carcassonne.stacked_widget.setCurrentWidget(self.Carcassonne.lobby_vis)
        
        # Connect buttons
        # ...