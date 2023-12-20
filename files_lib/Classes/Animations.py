import PyQt6.QtGui     as QtG
import PyQt6.QtWidgets as QtW
import PyQt6.QtCore    as QtC
import PyQt6_Extra     as QtE

class Animation(QtC.QSequentialAnimationGroup):
    def __init__(self, parent):
        super().__init__(parent)
        self.stopped = False
        self.finished.connect(self._reset)
    
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
        else:
            self.stop_animation()
            self.setLoopCount(loop_count) # -1: run until stopped
    
    def stop_animation(self):
        self.stopped = True
    
    def _reset(self):
        if self.stopped == False:
            self.start()
        else:
            self.stopped = False