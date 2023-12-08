import PyQt5.QtGui as QtG
import PyQt5.QtWidgets as QtW
import PyQt5.QtCore as QtC
import PyQt5_Extra as QtE
from firebase_admin import db

import time
import sys
if r"..\Dialogs" not in sys.path:
    sys.path.append(r"..\Dialogs")
from Dialogs.YesNo import YesNoDialog

class PlayerList(QtW.QWidget):
# class PlayerList(QtW.QGridLayout):
    def __init__(self):
        super.__init__()
        
        self.player_list_header = QtW.QLabel('Player list')
        self.player_list_header.setFont(QtG.QFont(self.font, 16, QtG.QFont.Bold))
        
        self.player_list = QtW.QGridLayout()
        self.player_colours = dict()
        self.setLayout(self.player_list)
        
        # Listener
        self.player_list_updater = PlayerListUpdater(self.Refs)
        self.player_list_updater.updateSignal.connect(self.update_player_list)
        self.player_list_updater.listen_for_updates()
        self.player_list_updater.start()
    
    def update_player_list(self):
        for i in reversed(range(self.count())):
            self.player_list.itemAt(i).widget().setParent(None)
        
        admin = self.Refs('admin').get()
        
        # Enable start button for admin
        self.update_start_button()
        
        # Add player colour indicators
        self.draw_player_colours()
        
        # Add player labels
        for idx, player in enumerate(self):
            # allow admin to choose new admin
            if player == admin:
                label = QtW.QLabel('(leader)')
                label.setFont(QtG.QFont(self.font, 12))
                self.player_list.addWidget(label, idx, 0, alignment = QtC.Qt.AlignCenter)
            
            if self.username == admin and player != admin:
                label = QtE.ClickableLabel(self)
                label.clicked.connect(self.make_admin(player))
                label.setToolTip("Click to make lobby leader.")
            else:
                label = QtW.QLabel(player)
            label.setText(f'{player}')
            label.setFont(QtG.QFont(self.font, 12))
            self.addWidget(label, idx, 2, alignment=QtC.Qt.AlignLeft)
        self.player_list.setColumnMinimumWidth(0, 60)
        self.player_list.setColumnMinimumWidth(1, 40)
        self.player_list.setColumnStretch(2, 1000)
    
    def update_start_button(self):
        # Enable start button for admin
        if self.username == self.Refs('admin').get():
            connections = self.Refs('connections').get()
            if len(connections) == 1:
                # only one connection
                self.start_button.setEnabled(False)
                self.start_button.setToolTip('Need at least one more player to start.')
            else:
                # multiple connections
                for player in connections:
                    colour = self.Refs(f'players/{player}/colour').get()
                    if colour == self.colours[0]:
                        # not everybody chose a colour yet
                        self.start_button.setEnabled(False)
                        self.start_button.setToolTip('Not all players have chosen a colour yet.')
                        break
                else:
                    # everyone chose a colour
                    self.start_button.setEnabled(True)
        else:
            # for non-admins
            self.start_button.setEnabled(False)
            self.start_button.setToolTip('Only the lobby leader can start the game.')
    
    def draw_player_colours(self, player_list):
        for idx, player in enumerate(player_list):
            # Add colour indicator
            colour = self.Refs(f'players/{player}/colour').get()
            button = self.player_colours[player] = QtW.QPushButton()
            button.setEnabled(False)
            button.setStyleSheet(f'''QPushButton:disabled {{
                                        background-color: rgb{tuple(int(colour[1:][i:i+2], 16) for i in (0, 2, 4, 6))};
                                        min-width:  20px;
                                        max-width:  20px;
                                        min-height: 20px;
                                        max-height: 20px;
                                        border-radius: 14px;
                                        border-style: solid;
                                        border-width: 2px;
                                        border-color: rgb(50,50,50);
                                        padding: 2px;
                                    }}''')
            self.player_list.addWidget(button, idx, 1, alignment = QtC.Qt.AlignCenter)

class LobbyScreen(QtW.QMainWindow):
    #%% Visuals
    def _Lobby_init(self):
        # Window settings
        self.setWindowTitle('Lobby')
        self.setGeometry(100, 100, 400, 400)
        
        # References from menu screen
        self.lobby_key = self.menu_screen.lobby_key
        self.username = self.menu_screen.username
        self.Refs = self.menu_screen.Refs
        self.font = self.menu_screen.font
        self.colours = self.menu_screen.colours
        self.test = self.menu_screen.test
    
    def _Lobby_title(self):
        self.title_label = QtW.QLabel(f'Lobby: {self.lobby_key}')
        self.title_label.setFont(QtG.QFont(self.font, 20, QtG.QFont.Bold))
        
        self.joined_as_label = QtW.QLabel(f'Joined as: {self.username}')
        self.joined_as_label.setFont(QtG.QFont(self.font, 12))
    
    def _Lobby_colour_picker(self):
        self.colour_picker_header = QtW.QLabel('Pick your colour')
        self.colour_picker_header.setFont(QtG.QFont(self.font, 16, QtG.QFont.Bold))
        
        self.colour_selected = self.colours[0]
        self.colour_picker = QtW.QHBoxLayout()
        self.colour_picker_buttons = {x:None for x in self.colours}
        self.draw_colourPicker()
    
    def _Lobby_player_list(self):
        self.player_list_header = QtW.QLabel('Player list')
        self.player_list_header.setFont(QtG.QFont(self.font, 16, QtG.QFont.Bold))
        
        self.player_list = QtW.QGridLayout()
        self.player_colours = dict()
    
    def _Lobby_expansions(self):
        self.expansions_list_header = QtW.QLabel('Expansions')
        self.expansions_list_header.setFont(QtG.QFont(self.font, 16, QtG.QFont.Bold))
        
        self.draw_expansions_list(init=True)
    
    def _Lobby_leave_start(self):
        self.leave_button = QtW.QPushButton('Leave')
        self.leave_button.clicked.connect(self.leave_lobby)
        
        self.start_button = QtW.QPushButton('Start')
        self.start_button.clicked.connect(self.start_game_admin)
        self.start_button.setEnabled(False)
        self.start_button.setToolTip('Only the lobby leader can start the game.')
        
        self.continue_layout = QtW.QGridLayout()
        self.continue_layout.addWidget(self.leave_button,  0, 0)
        self.continue_layout.addWidget(self.start_button, 0, 4)
        
        # equal size for all columns
        for idx in range(5):
            self.continue_layout.setColumnStretch(idx, 1)
    
    def _Lobby_chat(self):
        if self.test == 1:
            self.chat_display = QtW.QTextEdit()
            self.chat_display.setReadOnly(True)
            self.chat_display.setFont(QtG.QFont(self.font, 12))
            
            self.chat_input = QtW.QLineEdit()
            self.chat_input.setPlaceholderText('Type here...')
            
            self.send_button = QtW.QPushButton('Send')
            self.send_button.clicked.connect(self.send_chat_message)
            self.chat_input.returnPressed.connect(self.send_button.click)
            
            self.input_layout = QtW.QHBoxLayout()
            self.input_layout.addWidget(self.chat_input)
            self.input_layout.addWidget(self.send_button)
        
    def __init__(self, menu_screen):
        super().__init__()
        self.menu_screen = menu_screen
        
        self._Lobby_init()
        self._Lobby_title()
        self._Lobby_colour_picker()
        self._Lobby_player_list()
        self._Lobby_expansions()
        self._Lobby_leave_start()
        self._Lobby_chat()

        # Create a layout and add the components
        self.main_layout = QtW.QGridLayout()
        self.main_layout.addWidget(self.title_label,            0, 0, alignment=QtC.Qt.AlignCenter)
        self.main_layout.addWidget(self.joined_as_label,        1, 0, alignment=QtC.Qt.AlignCenter)
        
        self.main_layout.addWidget(QtE.QHSeparationLine(),      2, 0)
        self.main_layout.addWidget(self.colour_picker_header,   3, 0)
        self.main_layout.addLayout(self.colour_picker,          4, 0)
        
        self.main_layout.addWidget(self.player_list_header,     5, 0)
        self.main_layout.addLayout(self.player_list,            6, 0)
        
        self.main_layout.addWidget(self.expansions_list_header, 7, 0)
        self.main_layout.addLayout(self.expansions_list,        8, 0)
        
        self.main_layout.addWidget(QtE.QHSeparationLine(),      9, 0)
        self.main_layout.addLayout(self.continue_layout,       10, 0)
        
        if self.test == 1:
            self.main_layout.addWidget(QtE.QHSeparationLine(),     11, 0)
            self.main_layout.addWidget(self.chat_display,          12, 0)
            self.main_layout.addLayout(self.input_layout,          13, 0)
        
        self.mainWidget = QtW.QWidget()
        self.mainWidget.setLayout(self.main_layout)
        self.setCentralWidget(self.mainWidget)
        
        # Updater threads
        self.start_game_updater = StartGameUpdater(self.Refs)
        self.start_game_updater.updateSignal.connect(self.start_game)
        self.start_game_updater.listen_for_updates()
        self.start_game_updater.start()
        
        self.player_list_updater = PlayerListUpdater(self.Refs)
        self.player_list_updater.updateSignal.connect(self.update_player_list)
        self.player_list_updater.listen_for_updates()
        self.player_list_updater.start()
        
        self.player_colours_updater = PlayerColoursUpdater(self.Refs)
        self.player_colours_updater.updateSignal.connect(self.update_player_colours)
        self.player_colours_updater.listen_for_updates()
        self.player_colours_updater.start()
        
        self.expansions_updater = ExpansionsUpdater(self.Refs)
        self.expansions_updater.updateSignal.connect(self.update_expansions_list)
        self.expansions_updater.listen_for_updates()
        self.expansions_updater.start()
        
        if self.test == 1:
            self.Refs('chat').listen(self.update_chat_display)
    
    #%% Functionality
    def draw_expansions_list(self, init=False):
        if init == True:
            # admin = self.Refs('admin').get()
            self.expansions_list = QtW.QGridLayout()
            self.expansions_list.setColumnMinimumWidth(0, 10) # extra 10px padding
            expansions = self.Refs('expansions').get().keys()
            self.expansions_switches = dict()
            for idx, expansion in enumerate(expansions):
                # Add a switch
                button = self.expansions_switches[expansion] = QtW.QCheckBox(expansion)
                button.setFont(QtG.QFont(self.font, 12))
                button.setChecked(self.Refs(f'expansions/{expansion}').get())
                self.expansions_list.addWidget(button, idx, 1)
                button.clicked.connect(self.Expansions_clicked(button))
                # if admin != self.username:
                button.setEnabled(False)
    
    def Expansions_clicked(self, button):
        def clicked():
            state = button.checkState()
            expansion = button.text()
            if state == 0: # unchecked
                self.Refs(f'expansions/{expansion}').set(0)
            elif state == 2: # checked
                self.Refs(f'expansions/{expansion}').set(1)
        return clicked
    
    def draw_colourPicker(self):
        for colour in self.colours:
            button = self.colour_picker_buttons[colour] = QtW.QPushButton(minimumHeight=100)
            button.clicked.connect(self.ColourPicker_select_colour(colour))
            button.setStyleSheet(f'''QPushButton {{
                                        background-color: rgb{tuple(int(colour[1:][i:i+2], 16) for i in (0, 2, 4, 6))};
                                        min-width:  80px;
                                        max-width:  80px;
                                        min-height: 80px;
                                        max-height: 80px;
                                        border-radius: 46px;
                                        border-style: solid;
                                        border-width: 2px;
                                        border-color: rgb(50,50,50);
                                        padding: 4px;
                                    }}
                                    QPushButton:pressed {{
                                        background-color: rgb{tuple(int(colour[1:][i:i+2], 16)/1.1 for i in (0, 2, 4))};
                                        border-width: 4px;
                                    }}
                                    QPushButton:disabled {{
                                        background-color: rgb{tuple(int(colour[1:][i:i+2], 16)/1.5 for i in (0, 2, 4))};
                                    }}''')
            if colour == self.colour_selected:
                button.setIcon(QtG.QIcon(r'.\Images\checkmark_icon.png'))
                button.setIconSize(QtC.QSize(50,50))
            elif colour not in self.Refs('colours').get() and colour != self.colours[0]:
                button.setEnabled(False)
            else:
                button.setCursor(QtG.QCursor(QtC.Qt.PointingHandCursor))
            self.colour_picker.addWidget(button)
    
    def ColourPicker_select_colour(self, button_colour):
        def select_new_colour():
            if button_colour != self.colour_selected:
                # Remove checkmark from old selected colour
                self.colour_picker_buttons[self.colour_selected].setIcon(QtG.QIcon())
                if self.colour_selected != self.colours[0]:
                    self.Refs('colours', item=self.colour_selected, load='add_del')
                
                # Add checkmark to new selected colour
                self.colour_selected = button_colour
                button = self.colour_picker_buttons[self.colour_selected]
                button.setIcon(QtG.QIcon(r'.\Images\checkmark_icon.png'))
                button.setIconSize(QtC.QSize(50,50))
                self.Refs(f'players/{self.username}/colour').set(self.colour_selected)
                if self.colour_selected != self.colours[0]:
                    self.Refs('colours', item=self.colour_selected, load='add_del')
            
        return select_new_colour
    
    def draw_player_colours(self, player_list):
        for idx, player in enumerate(player_list):
            # Add colour indicator
            colour = self.Refs(f'players/{player}/colour').get()
            button = self.player_colours[player] = QtW.QPushButton()
            button.setEnabled(False)
            button.setStyleSheet(f'''QPushButton:disabled {{
                                        background-color: rgb{tuple(int(colour[1:][i:i+2], 16) for i in (0, 2, 4, 6))};
                                        min-width:  20px;
                                        max-width:  20px;
                                        min-height: 20px;
                                        max-height: 20px;
                                        border-radius: 14px;
                                        border-style: solid;
                                        border-width: 2px;
                                        border-color: rgb(50,50,50);
                                        padding: 2px;
                                    }}''')
            self.player_list.addWidget(button, idx, 1, alignment = QtC.Qt.AlignCenter)
    
    def leave_lobby(self):
        title = 'Leave lobby?'
        text = 'Are you sure you want to leave the lobby?'
        yesNoDialog = YesNoDialog(self, title, text)
        result = yesNoDialog.exec_()
        if result == QtW.QDialog.Accepted:
            self.menu_screen.remove_connection(self.username)
            self.hide()
            self.menu_screen.show()
    
    def start_game_admin(self):
        title = 'Start game?'
        text = 'Are you sure you want to start the game?'
        yesNoDialog = YesNoDialog(self, title, text)
        result = yesNoDialog.exec_()
        if result == QtW.QDialog.Accepted:
            # Close lobby
            self.Refs('open').set(False)
    
    def start_game(self):
        if self.test == 1:
            self.chat_display.append(f'--> {self.username}: Start game whoooooooooooooo!!!!')
            time.sleep(1)
        self.close()
        QtW.qApp.quit()
    
    def update_start_button(self):
        # Enable start button for admin
        if self.username == self.Refs('admin').get():
            connections = self.Refs('connections').get()
            if len(connections) == 1:
                # only one connection
                self.start_button.setEnabled(False)
                self.start_button.setToolTip('Need at least one more player to start.')
            else:
                # multiple connections
                for player in connections:
                    colour = self.Refs(f'players/{player}/colour').get()
                    if colour == self.colours[0]:
                        # not everybody chose a colour yet
                        self.start_button.setEnabled(False)
                        self.start_button.setToolTip('Not all players have chosen a colour yet.')
                        break
                else:
                    # everyone chose a colour
                    self.start_button.setEnabled(True)
        else:
            # for non-admins
            self.start_button.setEnabled(False)
            self.start_button.setToolTip('Only the lobby leader can start the game.')
    
    def update_player_list(self, player_list):
        for i in reversed(range(self.player_list.count())):
            self.player_list.itemAt(i).widget().setParent(None)
        
        admin = self.Refs('admin').get()
        
        # Enable start button for admin
        self.update_start_button()
        
        # Add player colour indicators
        self.draw_player_colours(player_list)
        
        # Add player labels
        for idx, player in enumerate(player_list):
            # allow admin to choose new admin
            if player == admin:
                label = QtW.QLabel('(leader)')
                label.setFont(QtG.QFont(self.font, 12))
                self.player_list.addWidget(label, idx, 0, alignment = QtC.Qt.AlignCenter)
            
            if self.username == admin and player != admin:
                label = QtE.ClickableLabel(self)
                label.clicked.connect(self.make_admin(player))
                label.setToolTip("Click to make lobby leader.")
            else:
                label = QtW.QLabel(player)
            label.setText(f'{player}')
            label.setFont(QtG.QFont(self.font, 12))
            self.player_list.addWidget(label, idx, 2, alignment=QtC.Qt.AlignLeft)
        self.player_list.setColumnMinimumWidth(0, 60)
        self.player_list.setColumnMinimumWidth(1, 40)
        self.player_list.setColumnStretch(2, 1000)            
    
    def update_player_colours(self, player_list):
        # Update colour indicators of player list
        for i in reversed(range(self.player_list.count())):
            widget = self.player_list.itemAt(i).widget()
            if type(widget) == type(QtW.QPushButton()):
                widget.setParent(None)
        
        # Get current player list
        players = self.Refs('connections').get()
        if players != None:
            player_list = []
            for player in players:
                if player is not None:
                    player_list.append(player)
        
        self.draw_player_colours(player_list)
        
        # Update colour picker buttons
        for i in reversed(range(self.colour_picker.count())):
            widget = self.colour_picker.itemAt(i).widget()
            widget.setParent(None)
        self.draw_colourPicker()
        
        # Enable start button for admin
        self.update_start_button()
        
    def update_expansions_list(self):
        admin = self.Refs('admin').get()
        expansions_info = self.Refs('expansions').get()
        for expansion in self.expansions_switches.keys():
            # Check or uncheck
            button = self.expansions_switches[expansion]
            button.setChecked(expansions_info[expansion])
            # Enable or disable
            if admin == self.username:
                button.setEnabled(True)
                button.setToolTip('')
            else:
                button.setEnabled(False)
                button.setToolTip('Only the lobby leader can select expansions.')
    
    def make_admin(self, player):
        def make_new_admin():
            title = 'Change lobby leader?'
            text = f"Make '{player}' the lobby leader?"
            admin_dialog = YesNoDialog(self, title, text)
            result = admin_dialog.exec_()
            if result == QtW.QDialog.Accepted:
                self.Refs('admin').set(player)
        return make_new_admin

    # @QtC.pyqtSlot(dict)
    def update_chat_display(self, event):
        if event.data is not None:
            # Initial startup:
            if event.path == '/':
                # Extract all previous message
                paths = list(self.Refs('chat').get().keys())
                for idx, path in enumerate(paths):
                    message = db.reference(f'lobbies/{self.lobby_key}/chat/{path}').get()
                    messageNew = self.Refs(f'chat/{path}').get()
                    if message == messageNew:
                        print('Message reference is good')
                    else: print('Message reference is bad, check it.')
                    data = {}
                    for item in message.items():
                        data[item[0]] = item[1]
                    chat_text = f"{data['username']}: {data['message']}"
                    self.chat_display.append(chat_text)
            # New message
            else:
                messages = event.data
                data = {}
                for item in messages.items():
                    data[item[0]] = item[1]
                chat_text = f"{data['username']}: {data['message']}"
                self.chat_display.append(chat_text)
                if data['message'] == 'conns':
                    conns = self.Refs('connections').get()
                    self.chat_display.append(f'--> {conns}')
    
    def send_chat_message(self):
        message = self.chat_input.text().strip()
        if len(message)>0:
            chat_message = {
                'username': self.username,
                'message': message
            }
            if self.Refs('chat').push(chat_message):
                self.chat_input.clear()

    def closeEvent(self, event):
        self.menu_screen.remove_connection(self.username)
        event.accept()

#%% Updaters
class PlayerListUpdater(QtC.QThread):
    updateSignal = QtC.pyqtSignal(list)

    def __init__(self, refs):
        super().__init__()
        self.Refs = refs

    def run(self):
        # Get current admin and connections
        admin = self.Refs('admin').get()
        players = self.Refs('connections').get()
        
        # Make sure that the admin hasn't changed before continuing
        if players != None:
            while admin not in players:
                time.sleep(0.1)
                admin = self.Refs('admin').get()
            
            # Get a new player list
            player_list = []
            for player in players:
                if player is not None:
                    player_list.append(player)
            self.updateSignal.emit(player_list)
    
    def listen_for_updates(self):
        # when these references update, they trigger a function
        self.Refs('connections').listen(self.on_player_list_update)
        self.Refs('admin').listen(self.on_player_list_update)
    
    def on_player_list_update(self, event):
        # if event.data is not None:
        self.run()
            
class PlayerColoursUpdater(QtC.QThread):
    updateSignal = QtC.pyqtSignal(list)

    def __init__(self, refs):
        super().__init__()
        self.Refs = refs

    def run(self):
        # Get current connections
        players = self.Refs('connections').get()
        
        # Get a new player list
        if players != None:
            player_list = []
            for player in players:
                if player is not None:
                    player_list.append(player)
            self.updateSignal.emit(player_list)
    
    def listen_for_updates(self):
        # when these references update, they trigger a function
        self.Refs('colours').listen(self.on_player_colours_update)
    
    def on_player_colours_update(self, event):
        # if event.data is not None:
        self.run()
        
class ExpansionsUpdater(QtC.QThread):
    updateSignal = QtC.pyqtSignal()

    def __init__(self, refs):
        super().__init__()
        self.Refs = refs

    def run(self):
        # Get current connections
        players = self.Refs('connections').get()
        
        if players != None:
            self.updateSignal.emit()
    
    def listen_for_updates(self):
        # when these references update, they trigger a function
        self.Refs('expansions').listen(self.on_expansions_update)
        self.Refs('admin').listen(self.on_expansions_update)
    
    def on_expansions_update(self, event):
        # if event.data is not None:
        self.run()

class StartGameUpdater(QtC.QThread):
    updateSignal = QtC.pyqtSignal()
    
    def __init__(self, refs):
        super().__init__()
        self.Refs = refs
    
    def run(self):
        if self.Refs('open').get() == False:
            self.updateSignal.emit()
        
    def listen_for_updates(self):
        self.Refs('open').listen(self.on_update)
    
    def on_update(self, event):
        self.run()