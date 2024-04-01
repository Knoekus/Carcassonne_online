import PyQt6.QtWidgets as QtW

class OKDialog(QtW.QDialog):
    def __init__(self, Carcassonne, parent=None, title=None, text=None):
        super().__init__(parent)
        self.Carcassonne = Carcassonne
    
        self.setWindowTitle(title)

        label = QtW.QLabel(text)
        font = self.Carcassonne.Properties.Font(size=0, bold=False)
        label.setFont(font)
        
        self.ok_button = QtW.QPushButton('OK')
        font = self.Carcassonne.Properties.Font(size=-2, bold=False)
        self.ok_button.setFont(font)
        self.ok_button.clicked.connect(self.close)
        
        layout = QtW.QGridLayout()
        layout.addWidget(label, 0, 0, 1, 3)
        layout.addWidget(self.ok_button, 1, 1) # Put button in center

        self.setLayout(layout)

    def setMinWidth(self, width):
        self.setStyleSheet(f"QLabel{{min-width: {width}px;}}");