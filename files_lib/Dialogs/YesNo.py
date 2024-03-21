import PyQt6.QtWidgets as QtW

class YesNoDialog(QtW.QDialog):
    def __init__(self, Carcassonne, parent=None, title=None, text=None):
        super().__init__(parent)
        self.Carcassonne = Carcassonne
    
        self.setWindowTitle(title)

        label = QtW.QLabel(text)
        font = self.Carcassonne.Properties.Font(size=0, bold=False)
        label.setFont(font)
        
        self.y_button = QtW.QPushButton('Yes')
        font = self.Carcassonne.Properties.Font(size=-2, bold=False)
        self.y_button.setFont(font)
        self.y_button.clicked.connect(self.accept)
        
        self.n_button = QtW.QPushButton('No')
        font = self.Carcassonne.Properties.Font(size=-2, bold=False)
        self.n_button.setFont(font)
        self.n_button.clicked.connect(self.close)
        
        layout = QtW.QVBoxLayout()
        layout = QtW.QGridLayout()
        layout.addWidget(label, 0, 0, 1, 2)
        layout.addWidget(self.n_button, 1, 0)
        layout.addWidget(self.y_button, 1, 1)

        self.setLayout(layout)

    def get_username(self):
        return self.username_input.text()

    def setMinWidth(self, width):
        self.setStyleSheet(f"QLabel{{min-width: {width}px;}}");