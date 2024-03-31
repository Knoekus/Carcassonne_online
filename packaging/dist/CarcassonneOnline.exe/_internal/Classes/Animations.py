#%% Imports
# PyQt6
import PyQt6.QtCore    as QtC
import PyQt6.QtGui     as QtG
import PyQt6.QtWidgets as QtW
import PyQt6_Extra     as QtE

# Custom classes
from Dialogs.OK_dialog    import OKDialog

# Other packages
# ...

#%% Expansions classes
class AnimationGroup_parallel(QtC.QParallelAnimationGroup):
    def __init__(self, loop_count=-1):
        super().__init__()
        self.repeat = False
        self.finished.connect(self._reset)
        
        if loop_count == -1:
            self.setLoopCount(1)
        else:
            self.setLoopCount(loop_count) # -1: run until stopped
    
    def add(self, animation):
        self.addAnimation(animation)
    
    def start_animation(self):
        self.repeat = True
        self.start()
    
    def stop_animation(self):
        self.repeat = False
    
    def _reset(self):
        if self.repeat == True:
            self.start()

class Animation(QtC.QSequentialAnimationGroup):
    def __init__(self, parent):
        super().__init__(parent)
        self.parent_obj = parent
        self.repeat = False
        self.finished.connect(self._reset)
    
    def add_blinking(self, op_start, op_end, time, pause, loop_count=-1):
        # Define effect type
        effect = QtW.QGraphicsOpacityEffect(self.parent_obj)
        self.parent_obj.setGraphicsEffect(effect)
        
        # Fade out
        animation1 = QtC.QPropertyAnimation(effect, b"opacity")
        animation1.setEasingCurve(QtC.QEasingCurve.Type.InQuad)
        animation1.setEndValue(op_end)
        animation1.setStartValue(op_start)
        animation1.setDuration(time/2)
        
        # Fade in
        animation2 = QtC.QPropertyAnimation(effect, b"opacity")
        animation2.setEasingCurve(QtC.QEasingCurve.Type.OutQuad)
        animation2.setEndValue(op_start)
        animation2.setStartValue(op_end)
        animation2.setDuration(time/2)
        
        # Add both fades to the animation
        self.addAnimation(animation1)
        self.addAnimation(animation2)
        self.addPause(pause)
        if loop_count == -1:
            self.setLoopCount(1)
            self.repeat = True
        else:
            self.setLoopCount(loop_count) # -1: run until stopped
    
    def swap_image(self, new_image, tile_idx, tile_letter, time):
        if type(self.parent_obj) != type(QtE.Tile(None)):
            raise Exception("Swap image of a QtE.Tile object.")
        
        # Swap image
        def Redraw_image():
            self.parent_obj.set_tile(new_image, tile_idx, tile_letter, self.parent_obj.parent().materials)
            self.removeAnimation(animation1)
            self.addAnimation(animation2)
            self.finished.disconnect()
            self.finished.connect(self._reset)
            self.start()
        
        # Blink in and out
        effect = QtW.QGraphicsOpacityEffect(self.parent_obj)
        self.parent_obj.setGraphicsEffect(effect)
        
        animation1 = QtC.QPropertyAnimation(effect, b"opacity")
        animation1.setEasingCurve(QtC.QEasingCurve.Type.InQuad)
        animation1.setStartValue(1)
        animation1.setEndValue(0)
        animation1.setDuration(time/2)
        
        animation2 = QtC.QPropertyAnimation(effect, b"opacity")
        animation2.setEasingCurve(QtC.QEasingCurve.Type.OutQuad)
        animation2.setStartValue(0)
        animation2.setEndValue(1)
        animation2.setDuration(time/2)
        
        self.addAnimation(animation1)
        self.finished.disconnect()
        self.finished.connect(Redraw_image)
        self.start()
    
    def start_loop(self):
        self.repeat = True
        self.start()
        
    def stop_loop(self):
        self.repeat = False
    
    def _reset(self):
        if self.repeat == True:
            self.start()
            self.State.Running

class New_tile_swap(QtC.QSequentialAnimationGroup):
    def __init__(self, game, new_tile, time=500):
        super().__init__(new_tile)
        self.game = game
        self.new_tile = new_tile
        self.time = time
        # self.finished.connect(self.stopped)
        
        # Effect
        self.effect = QtW.QGraphicsOpacityEffect(self.new_tile)
        self.new_tile.setGraphicsEffect(self.effect)
        
        # # Blink out
        # self.animation1 = QtC.QPropertyAnimation(self.effect, b"opacity")
        # self.animation1.setEasingCurve(QtC.QEasingCurve.Type.InQuad)
        # self.animation1.setStartValue(1)
        # self.animation1.setEndValue(0)
        # self.animation1.setDuration(self.time/2)
        
        # # Blink in
        # self.animation2 = QtC.QPropertyAnimation(self.effect, b"opacity")
        # self.animation2.setEasingCurve(QtC.QEasingCurve.Type.OutQuad)
        # self.animation2.setStartValue(0)
        # self.animation2.setEndValue(1)
        # self.animation2.setDuration(self.time/2)
    
    def _Finish1(self):
        print('Checkpoint 2')
        self.new_tile.set_tile(self.file, self.index, self.letter)
        self.removeAnimation(self.animation1)
        
        # Blink in
        self.animation2 = QtC.QPropertyAnimation(self.effect, b"opacity")
        self.animation2.setEasingCurve(QtC.QEasingCurve.Type.OutQuad)
        self.animation2.setStartValue(0)
        self.animation2.setEndValue(1)
        self.animation2.setDuration(self.time/2)
        
        self.addAnimation(self.animation2)
        self.finished.disconnect()
        self.finished.connect(self._Finish2)
        self.start()
        print('Checkpoint 3')
    
    def _Finish2(self):
        print('Checkpoint 4')
        if self.game.username == self.player:
            self.new_tile.enable()
        self.removeAnimation(self.animation2)
        self.finished.disconnect()
        print('Checkpoint 5')
    
    def swap(self, file, index, letter, player):
        self.file = file
        self.index = index
        self.letter = letter
        self.player = player
        
        # Set up sequence
        self.finished.connect(self._Finish1)
        
        # Blink out
        self.animation1 = QtC.QPropertyAnimation(self.effect, b"opacity")
        self.animation1.setEasingCurve(QtC.QEasingCurve.Type.InQuad)
        self.animation1.setStartValue(1)
        self.animation1.setEndValue(0)
        self.animation1.setDuration(self.time/2)
        
        self.addAnimation(self.animation1)
        self.start()
        print('Checkpoint 1')
    
    def stopped(self):
        print('Finished animation')

class Final_animation():
    def __init__(self, Carcassonne):
        self.Carcassonne = Carcassonne
        self.animations = dict()
        self.count = 0
        
    def add_possession(self, pos_n, winners, points, material):
        '''Add possession to list of possessions to be animated.'''
        self.animations[len(self.animations)] = [pos_n, winners, points, material]
    
    def start(self):
        '''Animate all possessions in the animations list.'''
        self.animate_possession()
    
    def animate_possession(self):
        '''Animate the possession of the current self.count counter.'''
        pos_n, winners, points, material = self.animations[self.count]
        
        # Change points labels
        for winner_player in winners:
            points_label = self.Carcassonne.game_vis.players_points[winner_player]
            points_before = int(points_label.text())
            
            # Intermediate label
            points_label.setText(f'{points_before} + {int(points)}') # int() to ignore possible floats
            
            # Database
            if winner_player == self.Carcassonne.username: # Do this only once per player
                self.Carcassonne.Refs(f'players/{winner_player}/points').set(points_before + points)
                
        # Make animation for blinking possession
        self.animation_group = AnimationGroup_parallel(3)
        for tile in pos_n['tiles']:
            if type(tile[0]) == QtE.Tile:
            # Single entry, so tuple
                animation = Animation(tile[0])
            else:
            # Multiple entries, so list of tuples
                animation = Animation(tile[0][0])
            animation.add_blinking(1, 0.6, 1000, 0, 1)
            self.animation_group.add(animation)
        
        # Play animation
        self.animation_group.finished.connect(self._inter_finished)
        self.animation_group.start()
    
    def _inter_finished(self):
        '''After each animation, process end result and check for next animation.'''
        # End current animation
        pos_n, winners, points, material = self.animations[self.count]
        
        # End state of points
        for winner_player in winners:
            points_label = self.Carcassonne.game_vis.players_points[winner_player]
            points_after = eval(points_label.text())
            points_label.setText(f'{points_after}')
            
        # Give back meeples
        self.Carcassonne.Possessions.Give_back_meeples(winners, pos_n, material)
        
        if self.count+1 in self.animations.keys():
        # Start next animation
            self.count += 1
            self.animate_possession()
        else:
        # Next animation does not exist
            self._on_finished()
    
    def _on_finished(self):
        '''When all animations are finished, end the game.'''
        # Dialog box for the winner
        winner = (None, 0)
        for player in self.Carcassonne.Possessions.Connections():
            points = self.Carcassonne.Refs(f'players/{player}/points').get()
            if points > winner[1]:
                winner = (player, points)
                
        title = f'{player} won!'
        text = f'Congratulations to {player} for winning the game!'
        OK_dialog = OKDialog(self.Carcassonne, self.Carcassonne.game_vis, title, text)
        OK_dialog.exec()
        