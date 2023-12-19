import prop_s

import PyQt6.QtGui as QtG
import PyQt6.QtWidgets as QtW
import PyQt6.QtCore as QtC

class UsernameDialog(QtW.QDialog):
    def __init__(self, parent=None):
        super().__init__(parent)
    
        self.setWindowTitle('Enter username')

        layout = QtW.QVBoxLayout()
        
        label = QtW.QLabel('Your username should have 2-20 characters.')
        label.setFont(QtG.QFont(prop_s.font, prop_s.font_sizes[0+parent.font_size]))
        
        self.username_input = QtW.QLineEdit(alignment=QtC.Qt.AlignmentFlag.AlignCenter)
        self.username_input.setFont(QtG.QFont(prop_s.font, prop_s.font_sizes[0+parent.font_size]))
        self.username_input.setPlaceholderText('Enter username...')
        
        self.ok_button = QtW.QPushButton('OK')
        self.ok_button.setFont(QtG.QFont(prop_s.font, prop_s.font_sizes[-2+parent.font_size]))
        self.ok_button.clicked.connect(self.button_clicked)
        
        layout.addWidget(label)
        layout.addWidget(self.username_input)
        layout.addWidget(self.ok_button)
        self.setLayout(layout)

    def get_username(self):
        return self.username_input.text().strip()
    
    def button_clicked(self):
        # Check if username is okay
        name = self.username_input.text().strip()
        if len(name) < 2:
            QtW.QMessageBox.warning(self, 'Username too short', 'That username is too short. Please choose a longer username.')
        elif len(name) > 20:
            QtW.QMessageBox.warning(self, 'Username too long', 'That username is too long. Please choose a shorter username.')
        else:
            self.accept()