import prop_s

import PyQt6.QtGui as QtG
import PyQt6.QtWidgets as QtW
# import PyQt5.QtCore as QtC

class YesNoDialog(QtW.QDialog):
    def __init__(self, parent=None, title=None, text=None):
        super().__init__(parent)
        # super().__init__()
    
        self.setWindowTitle(title)
        # self.setFixedSize(300, 100)

        label = QtW.QLabel(text)
        label.setFont(QtG.QFont(prop_s.font, prop_s.font_sizes[0+parent.font_size]))
        
        self.y_button = QtW.QPushButton('Yes')
        self.y_button.setFont(QtG.QFont(prop_s.font, prop_s.font_sizes[-2+parent.font_size]))
        self.y_button.clicked.connect(self.accept)
        
        self.n_button = QtW.QPushButton('No')
        self.n_button.setFont(QtG.QFont(prop_s.font, prop_s.font_sizes[-2+parent.font_size]))
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