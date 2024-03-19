#%% Imports
# PyQt6
import PyQt6.QtCore    as QtC
import PyQt6.QtGui     as QtG
import PyQt6.QtWidgets as QtW
import PyQt6_Extra     as QtE

# Custom classes
# ...

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
            # self.repeat = True
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
    
    #%% Effects
    def add_blinking(self, op_start, op_end, time, pause, loop_count=-1):
        # Define effect type
        effect = QtW.QGraphicsOpacityEffect(self.parent_obj)
        self.parent_obj.setGraphicsEffect(effect)
        
        # Fade out
        animation1 = QtC.QPropertyAnimation(effect, b"opacity")
        animation1.setEasingCurve(QtC.QEasingCurve.Type.InQuad)
        animation1.setStartValue(op_start)
        animation1.setEndValue(op_end)
        animation1.setDuration(time/2)
        
        # Fade in
        animation2 = QtC.QPropertyAnimation(effect, b"opacity")
        animation2.setEasingCurve(QtC.QEasingCurve.Type.OutQuad)
        animation2.setStartValue(op_end)
        animation2.setEndValue(op_start)
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
            # parent.draw_image(new_image)
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
    
    def DEPRECATED_swap_image(self, file, tile_idx, tile_letter, time):
        if type(self.parent_obj) != type(QtE.Tile(None)):
            raise Exception("Swap image of a QtE.Tile object.")
        
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
        
        # Swap image
        def Redraw_image():
            # parent.draw_image(new_image)
            print('animation file:', file)
            self.parent_obj.set_tile(file, tile_idx, tile_letter, self.parent_obj.parent().materials)
            self.removeAnimation(animation1)
            self.addAnimation(animation2)
            self.finished.disconnect()
            self.finished.connect(self._reset)
            self.start()
        
        self.clear()
        self.addAnimation(animation1)
        self.finished.disconnect()
        self.finished.connect(Redraw_image)
        animation1.start()
        self.finished.connect(self.swap_finished)
        self.start()
    
    #%% Stopping
    def start_loop(self):
        self.repeat = True
        self.start()
        
    def stop_animation(self):
        self.repeat = False
    
    def _reset(self):
        if self.repeat == True:
            self.start()
            self.State.Running
        # else:
        #     # Enable button
        #     try: self.parent_obj.enable()
        #     except Exception as e:
        #         print(f'Error: {e}')
        #     print('Trying to reset animation, but ')

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

class New_tile_swap2(QtC.QPropertyAnimation):
    def __init__(self, game, new_tile, time=500):
        self.game = game
        self.new_tile = new_tile
        self.time = time
        
        effect = QtW.QGraphicsOpacityEffect(self.new_tile)
        self.new_tile.setGraphicsEffect(effect)
        
        super().__init__(effect, b"opacity")
        self.setDuration(self.time/2)
        
    def swap(self, file, index, letter, player):
        self.file = file
        self.index = index
        self.letter = letter
        self.player = player
        
        # Blink in
        self.setEasingCurve(QtC.QEasingCurve.Type.InQuad)
        self.setStartValue(1)
        self.setEndValue(0)
        self.finished.connect(self._Finish1)
        print('Checkpoint 1')
        self.start()
    
    def _Finish1(self):
        print('Checkpoint 2')
        # Replace tile
        self.new_tile.set_tile(self.file, self.index, self.letter)
        
        # Blink in
        self.setEasingCurve(QtC.QEasingCurve.Type.OutQuad)
        self.setStartValue(0)
        self.setEndValue(1)
        
        # self.finished.disconnect()
        self.finished.connect(self._Finish2)
        self.start()
        print('Checkpoint 3')
    
    def _Finish2(self):
        print('Checkpoint 4')
        self.finished.disconnect()
        if self.game.username == self.player:
            self.new_tile.enable()
        print('Checkpoint 5')
