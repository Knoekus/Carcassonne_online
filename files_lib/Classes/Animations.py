import PyQt6.QtGui     as QtG
import PyQt6.QtWidgets as QtW
import PyQt6.QtCore    as QtC
import PyQt6_Extra     as QtE

class Animation(QtC.QSequentialAnimationGroup):
    def __init__(self, parent):
        super().__init__(parent)
        self.repeat = False
        self.finished.connect(self._reset)
    
    #%% Effects
    def add_blinking(self, op_start, op_end, time, pause, loop_count=-1):
        # Define effect type
        effect = QtW.QGraphicsOpacityEffect(self.parent())
        self.parent().setGraphicsEffect(effect)
        
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
        parent = self.parent()
        if type(parent) != type(QtE.Tile(None)):
            raise Exception("Swap image of a QtE.Tile object.")
        
        # Swap image
        def Redraw_image():
            # parent.draw_image(new_image)
            print(new_image)
            parent.set_tile(new_image, tile_idx, tile_letter, parent.parent())
            self.removeAnimation(animation1)
            self.addAnimation(animation2)
            self.finished.disconnect()
            self.finished.connect(self._reset)
            self.start()
        
        # Blink in and out
        effect = QtW.QGraphicsOpacityEffect(self.parent())
        self.parent().setGraphicsEffect(effect)
        
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
        
    #%% Stopping
    def stop_animation(self):
        self.repeat = False
    
    def _reset(self):
        if self.repeat == True:
            self.start()