import PyQt6.QtGui     as QtG
import PyQt6.QtWidgets as QtW
import PyQt6.QtCore    as QtC
import PyQt6_Extra     as QtE
from firebase_admin import db

import time
import sys
import prop_s

if r"..\Dialogs" not in sys.path:
    sys.path.append(r"..\Dialogs")
from Dialogs.YesNo import YesNoDialog

if r"..\Screens" not in sys.path:
    sys.path.append(r"..\Screens")
from Screens.Game import GameScreen

#%% Colour picker
class ColourPicker(QtW.QWidget):
    def _ColourPicker_init(self):
        self.current_colour = self.lobby.Refs(f'players/{self.lobby.username}/colour')
        self.colour_picker_buttons = {x:None for x in prop_s.colours}
        
        # Listener
        self.player_colours_updater = PlayerColoursUpdater(self.lobby.Refs)
        self.player_colours_updater.updateSignal.connect(self.draw_colours)
        self.player_colours_updater.listen_for_updates()
        self.player_colours_updater.start()
        
    def _ColourPicker_header(self):
        self.header = QtW.QLabel('Pick your colour')
        # self.header.setFont(QtG.QFont(prop_s.font, prop_s.font_sizes[2+self.lobby.font_size], QtG.QFont.Bold))
        font = QtG.QFont(prop_s.font, prop_s.font_sizes[2+self.lobby.font_size])
        font.setBold(True)
        self.header.setFont(font)
    
    def _ColourPicker_list(self):
        self.list = QtW.QHBoxLayout()
        for colour in prop_s.colours:
            self.draw_colours(colour)
        
    def __init__(self, lobby):
        super().__init__()
        self.lobby = lobby
        
        self._ColourPicker_init()
        self._ColourPicker_header()
        self._ColourPicker_list()
        
        layout = QtW.QVBoxLayout()
        layout.addWidget(self.header)
        layout.addLayout(self.list)
        self.setLayout(layout)
    
    def colour_stylesheet(self, colour):
        return f'''QPushButton {{
                                    background-color: rgba{tuple(int(colour[i:i+2], 16) for i in (0, 2, 4, 6))};
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
                                    background-color: rgb{tuple(int(colour[i:i+2], 16)/1.1 for i in (0, 2, 4))};
                                    border-width: 4px;
                                }}
                                QPushButton:disabled {{
                                    background-color: rgb{tuple(int(colour[i:i+2], 16)/1.5 for i in (0, 2, 4))};
                                }}'''
    
    def update_colours(self):
        # Update colour picker buttons
        for i in reversed(range(self.list.count())):
            widget = self.list.itemAt(i).widget()
            widget.setParent(None)
        self.draw_colours(prop_s.colours)
    
    def draw_colours(self, colours):
        if type(colours) is not type(list()):
            colours = [colours]
        else:
            colours = prop_s.colours
        
        for colour in colours:
            if self.colour_picker_buttons[colour] == None:
                button = self.colour_picker_buttons[colour] = QtW.QPushButton(minimumHeight=100)
                button.clicked.connect(self.Select_colour(colour))
                button.setStyleSheet(self.colour_stylesheet(colour))
                self.list.addWidget(button)
                if colour == prop_s.colours[0]: # initiate with checkmark in transparent
                    button.setIcon(QtG.QIcon(r'.\Images\checkmark_icon.png'))
                    button.setIconSize(QtC.QSize(50,50))
            else:
                button = self.colour_picker_buttons[colour]
            
            # print(self.current_colour.get(), tuple(int(colour[i:i+2], 16) for i in (0, 2, 4)))
            if self.lobby.Refs(f'colours/{colour}').get() == 1 and colour != self.current_colour.get(): # don't disable current colour
                # selected by someone else
                button.setEnabled(False)
            else:
                # allowed to be clicked
                button.setEnabled(True)
                button.setCursor(QtG.QCursor(QtC.Qt.CursorShape.PointingHandCursor))
    
    def Select_colour(self, button_colour):
        """Function for all colour buttons. When a button is clicked, its colour is assigned to the player that selected it."""
        def select_new_colour():
            current_colour = self.current_colour.get()
            
            # If new colour selected and it's still free or it's blank
            if button_colour != current_colour and\
               (self.lobby.Refs(f'colours/{button_colour}').get() == 0 or button_colour == prop_s.colours[0]):
                # Remove checkmark from old selected colour
                self.colour_picker_buttons[current_colour].setIcon(QtG.QIcon())
                
                # Add checkmark to new selected colour
                self.colour_picker_buttons[button_colour].setIcon(QtG.QIcon(r'.\Images\checkmark_icon.png'))
                self.colour_picker_buttons[button_colour].setIconSize(QtC.QSize(50,50))
                
                # If current colour not blank, set old colour to be free and occupy new colour
                colours_update = {}
                if current_colour != prop_s.colours[0]:
                    colours_update[current_colour] = 0
                if button_colour != prop_s.colours[0]:
                    colours_update[button_colour] = 1
                self.lobby.Refs('colours').update(colours_update) # update to only cause 1 event change
                self.lobby.Refs(f'players/{self.lobby.username}/colour').set(button_colour)
                
                # Redraw the two buttons
                # Doesn't visualise until whole update is finished...
                # for colour_update in list(colours_update.keys()):
                #     self.draw_colours(colour_update)
                
                # Set local selected colour
                self.current_colour.set(button_colour)
        return select_new_colour

class PlayerColoursUpdater(QtC.QThread):
    updateSignal = QtC.pyqtSignal(list)

    def __init__(self, refs):
        super().__init__()
        self.Refs = refs

    def run(self):
        # Get list of colours
        # --> could try doing something smart with only updating necessary colours
        colours = self.Refs('colours').get()
        self.updateSignal.emit(list(colours.keys()))
    
    def listen_for_updates(self):
        # when these references update, they trigger a function
        self.Refs('colours').listen(self.on_player_colours_update)
    
    def on_player_colours_update(self, event):
        if event.data is not None:
            self.run()

#%% Player list
class PlayerList(QtW.QWidget):
    def _PlayerList_init(self):
        self.player_colours = dict()
        
        # Listener
        self.list_updater = PlayerListUpdater(self.lobby.Refs)
        self.list_updater.updateSignal.connect(self.update_list)
        self.list_updater.listen_for_updates()
        self.list_updater.start()
        
        self.colours_updater = PlayerListColoursUpdater(self.lobby.Refs)
        self.colours_updater.updateSignal.connect(self.update_colours)
        self.colours_updater.listen_for_updates()
        self.colours_updater.start()
    
    def _PlayerList_header(self):
        self.header = QtW.QLabel('Player list')
        # self.header.setFont(QtG.QFont(prop_s.font, prop_s.font_sizes[2+self.lobby.font_size], QtG.QFont.Bold))
        font = QtG.QFont(prop_s.font, prop_s.font_sizes[2+self.lobby.font_size])
        font.setBold(True)
        self.header.setFont(font)
    
    def _PlayerList_list(self):
        self.list = QtW.QGridLayout()
        
        #===== Initializing like this crashes new connections =====#
        # # Get current connections
        # players = self.lobby.Refs('connections').get()
        
        # if players != None:
        #     # Get a new player list
        #     player_list = []
        #     for player in players:
        #         if player is not None:
        #             player_list.append(player)
        # self.update_list(player_list)
        #==========================================================#
    
    def __init__(self, lobby):
        super().__init__()
        self.lobby = lobby
        
        self._PlayerList_init()
        self._PlayerList_header()
        self._PlayerList_list()
        
        # layout = QtW.QGridLayout()
        # layout.addWidget(self.header, 0, 0, 1, 1)
        # layout.addLayout(self.list,   1, 0, 1, 1)
        
        layout = QtW.QVBoxLayout()
        layout.addWidget(self.header)
        layout.addLayout(self.list)
        self.setLayout(layout)
    
    def indicator_stylesheet(self, colour):
        return f'''QPushButton:disabled {{
                                    background-color: rgba{tuple(int(colour[i:i+2], 16) for i in (0, 2, 4, 6))};
                                    min-width:  20px;
                                    max-width:  20px;
                                    min-height: 20px;
                                    max-height: 20px;
                                    border-radius: 14px;
                                    border-style: solid;
                                    border-width: 2px;
                                    border-color: rgb(50,50,50);
                                    padding: 2px;
                                }}'''
    
    def update_list(self, player_list):
        # FIXME ===== Here it removes all widgets, this can be more efficient by reusing existing widgets that don't change =====#
        for i in reversed(range(self.list.count())):
            self.list.itemAt(i).widget().setParent(None)
        #========================================================================================================================#
        
        # Enable start button for admin
        admin = self.lobby.Refs('admin').get()
        self.update_start_button()
        
        # Add player labels
        for idx, player in enumerate(player_list):
            # allow admin to choose new admin
            if player == admin:
                admin_label = QtW.QLabel('(leader)')
                admin_label.setFont(QtG.QFont(prop_s.font, prop_s.font_sizes[0+self.lobby.font_size]))
                # self.list.addWidget(admin_label, idx, 0, alignment = QtC.Qt.AlignCenter)
                self.list.addWidget(admin_label, idx, 0, alignment=QtC.Qt.AlignmentFlag.AlignCenter)
            
            # colour indicator
            colour = self.lobby.Refs(f'players/{player}/colour').get()
            indicator = self.player_colours[player] = QtW.QPushButton()
            indicator.setEnabled(False)
            indicator.setStyleSheet(self.indicator_stylesheet(colour))
            
            # username
            if self.lobby.username == admin and player != admin:
                username = QtE.ClickableLabel(self.lobby)
                username.clicked.connect(self.make_admin(player))
                username.setToolTip("Click to make lobby leader.")
            else:
                username = QtW.QLabel(player)
            username.setText(f'{player}')
            username.setFont(QtG.QFont(prop_s.font, prop_s.font_sizes[0+self.lobby.font_size]))
            
            # Put indicator and username in layout
            # self.list.addWidget(indicator, idx, 1, alignment = QtC.Qt.AlignCenter)
            self.list.addWidget(indicator, idx, 1, alignment=QtC.Qt.AlignmentFlag.AlignCenter)
            # self.list.addWidget(username,  idx, 2, alignment = QtC.Qt.AlignLeft)
            self.list.addWidget(username,  idx, 2, alignment=QtC.Qt.AlignmentFlag.AlignLeft)
            
        self.list.setColumnMinimumWidth(0, 60) # leader yes/no
        self.list.setColumnMinimumWidth(1, 40) # colour indicator
        self.list.setColumnStretch(2, 1000)    # username
    
    def update_colours(self):
        # Update colour picker buttons
        for i in reversed(range(self.list.count())):
            try:
                button = self.list.itemAt(i).widget()
                if type(button) == type(QtW.QPushButton()):
                    player = self.list.itemAt(i+1).widget().text() # +1 because order in list: leader, colour, username
                
                    # Change colour indicator
                    colour = self.lobby.Refs(f'players/{player}/colour').get()
                    button.setStyleSheet(self.indicator_stylesheet(colour))
            except:
                # this can happen when a player leaves the lobby: the reference to the colour doesnt exist anymore.
                None
        self.update_start_button()
    
    def update_start_button(self):
        # Enable start button for admin
        if self.lobby.username == self.lobby.Refs('admin').get():
            connections = self.lobby.Refs('connections').get()
            if len(connections) == 1:
                # only one connection
                self.lobby.start_button.setEnabled(False)
                self.lobby.start_button.setToolTip('Need at least one more player to start.')
            else:
                # multiple connections
                for player in connections:
                    colour = self.lobby.Refs(f'players/{player}/colour').get()
                    if colour == prop_s.colours[0]:
                        # not everybody chose a colour yet
                        self.lobby.start_button.setEnabled(False)
                        self.lobby.start_button.setToolTip('Not all players have chosen a colour yet.')
                        break
                else:
                    # everyone chose a colour
                    self.lobby.start_button.setEnabled(True)
                    self.lobby.start_button.setToolTip('Start game.')
        else:
            # for non-admins
            self.lobby.start_button.setEnabled(False)
            self.lobby.start_button.setToolTip('Only the lobby leader can start the game.')
    
    def make_admin(self, player):
        def make_new_admin():
            title = 'Change lobby leader?'
            text = f"Make '{player}' the lobby leader?"
            admin_dialog = YesNoDialog(self.lobby, title, text)
            admin_dialog.setMinWidth(300)
            result = admin_dialog.exec_()
            if result == QtW.QDialog.Accepted:
                self.lobby.Refs('admin').set(player)
        return make_new_admin

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

class PlayerListColoursUpdater(QtC.QThread):
    updateSignal = QtC.pyqtSignal()

    def __init__(self, refs):
        super().__init__()
        self.Refs = refs

    def run(self):
        # Get current connections
        players = self.Refs('connections').get()
        
        if players != None:
            # Get a new player list
            player_list = []
            for player in players:
                if player is not None:
                    player_list.append(player)
            self.updateSignal.emit()
    
    def listen_for_updates(self):
        # when these references update, they trigger a function
        self.Refs('colours').listen(self.on_player_list_update)
    
    def on_player_list_update(self, event):
        # if event.data is not None:
        self.run()

#%% Expansions list
class ExpansionsList(QtW.QWidget):
    def _ExpansionsList_init(self):
        self.expansions_switches = dict()
        
        # Listener
        self.expansions_updater = ExpansionsUpdater(self.lobby.Refs)
        self.expansions_updater.updateSignal.connect(self.update_expansions_list)
        self.expansions_updater.listen_for_updates()
        self.expansions_updater.start()
    
    def _ExpansionsList_header(self):
        self.header = QtW.QLabel('Expansions')
        # self.header.setFont(QtG.QFont(prop_s.font, prop_s.font_sizes[2+self.lobby.font_size], QtG.QFont.Bold))
        font = QtG.QFont(prop_s.font, prop_s.font_sizes[2+self.lobby.font_size])
        font.setBold(True)
        self.header.setFont(font)
    
    def _ExpansionsList_list(self):
        self.list = QtW.QGridLayout()
        self.list.setColumnMinimumWidth(0, 10) # extra 10px padding
        self.draw_expansions_list()
    
    def __init__(self, lobby):
        super().__init__()
        self.lobby = lobby
        
        self._ExpansionsList_init()
        self._ExpansionsList_header()
        self._ExpansionsList_list()
        
        layout = QtW.QGridLayout()
        layout.addWidget(self.header, 0, 0, 1, 1)
        layout.addLayout(self.list,   1, 0, 1, 1)
        self.setLayout(layout)
    
    def draw_expansions_list(self):
        # Get data
        admin = self.lobby.Refs('admin').get()
        expansions = prop_s.expansions
        
        # Draw switches
        for idx, expansion in enumerate(expansions):
            # Add switch
            button = self.expansions_switches[expansion] = QtW.QCheckBox(expansion)
            button.setFont(QtG.QFont(prop_s.font, prop_s.font_sizes[0+self.lobby.font_size]))
            button.setChecked(self.lobby.Refs(f'expansions/{expansion}').get())
            button.setStyleSheet(f"""QCheckBox::indicator{{
                                      width:  {prop_s.font_sizes[1+self.lobby.font_size]}px;
                                      height: {prop_s.font_sizes[0+self.lobby.font_size]}px;
                                      }}""") # make a little wider
            
            self.list.addWidget(button, idx, 1)
            button.clicked.connect(self.Expansions_clicked(button))
            
            if admin != self.lobby.username:
                button.setEnabled(False)
                button.setToolTip('Only the lobby leader can select expansions.')
    
    def Expansions_clicked(self, button):
        def clicked():
            state = button.checkState()
            expansion = button.text()
            if state == 0: # unchecked
                self.lobby.Refs(f'expansions/{expansion}').set(0)
            elif state == 2: # checked
                self.lobby.Refs(f'expansions/{expansion}').set(1)
        return clicked

    def update_expansions_list(self):
        # Get data
        admin = self.lobby.Refs('admin').get()
        expansions_info = self.lobby.Refs('expansions').get()
        
        # Edit switches
        for expansion in self.expansions_switches.keys():
            # Check or uncheck
            button = self.expansions_switches[expansion]
            button.setChecked(expansions_info[expansion])
            
            # Enable or disable
            if admin == self.lobby.username:
                button.setEnabled(True)
                button.setToolTip('')
            else:
                button.setEnabled(False)
                button.setToolTip('Only the lobby leader can select expansions.')
    
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

#%% Lobby screen
# class LobbyScreen(QtW.QMainWindow):
class LobbyScreen(QtW.QWidget):
    #%% Visuals
    def _Lobby_init(self):
        # References from menu screen
        self.lobby_key = self.menu_screen.lobby_key
        self.username = self.menu_screen.username
        self.Refs = self.menu_screen.Refs
        self.test = self.menu_screen.test
        self.font_size = self.menu_screen.font_size
        self.stacked = self.menu_screen.stacked
        
        # Functions
        self.remove_connection = self.menu_screen.remove_connection
    
    def _Lobby_title(self):
        self.title_label = QtW.QLabel(f'Lobby: {self.lobby_key}')
        # self.title_label.setFont(QtG.QFont(prop_s.font, prop_s.font_sizes[5+self.font_size], QtG.QFont.Bold))
        font = QtG.QFont(prop_s.font, prop_s.font_sizes[5+self.font_size])
        font.setBold(True)
        self.title_label.setFont(font)
        
        self.joined_as_label = QtW.QLabel(f'Joined as: {self.username}')
        self.joined_as_label.setFont(QtG.QFont(prop_s.font, prop_s.font_sizes[2+self.font_size]))
    
    def _Lobby_leave_start(self):
        self.leave_button = QtW.QPushButton('Leave')
        self.leave_button.setFont(QtG.QFont(prop_s.font, prop_s.font_sizes[0+self.font_size]))
        self.leave_button.clicked.connect(self.leave_lobby)
        
        self.start_button = QtW.QPushButton('Start')
        self.start_button.setFont(QtG.QFont(prop_s.font, prop_s.font_sizes[0+self.font_size]))
        self.start_button.clicked.connect(self.start_game_admin)
        self.start_button.setEnabled(False)
        self.start_button.setToolTip('Only the lobby leader can start the game.')
        
        self.continue_layout = QtW.QGridLayout()
        self.continue_layout.addWidget(self.leave_button,  0, 0)
        self.continue_layout.addWidget(self.start_button, 0, 4)
        
        # equal size for all columns
        for idx in range(5):
            self.continue_layout.setColumnStretch(idx, 1)
        
        # Updater threads
        self.start_game_updater = StartGameUpdater(self.Refs)
        self.start_game_updater.updateSignal.connect(self.start_game)
        self.start_game_updater.listen_for_updates()
        self.start_game_updater.start()
    
    def _Lobby_chat(self):
        if self.test == 1:
            self.chat_display = QtW.QTextEdit()
            self.chat_display.setReadOnly(True)
            self.chat_display.setFont(QtG.QFont(prop_s.font, prop_s.font_sizes[0+self.font_size]))
            
            self.chat_input = QtW.QLineEdit()
            self.chat_input.setFont(QtG.QFont(prop_s.font, prop_s.font_sizes[0+self.font_size]))
            self.chat_input.setPlaceholderText('Type here...')
            
            self.send_button = QtW.QPushButton('Send')
            self.send_button.setFont(QtG.QFont(prop_s.font, prop_s.font_sizes[0+self.font_size]))
            self.send_button.clicked.connect(self.send_chat_message)
            self.chat_input.returnPressed.connect(self.send_button.click)
            
            self.input_layout = QtW.QHBoxLayout()
            self.input_layout.addWidget(self.chat_input)
            self.input_layout.addWidget(self.send_button)
        
    def __init__(self, menu_screen):
        # super().__init__(menu_screen)
        super().__init__()
        self.menu_screen = menu_screen
        
        self._Lobby_init()
        self._Lobby_title()
        self._Lobby_leave_start()
        self._Lobby_chat()

        # Create a layout and add the components
        self.main_layout = QtW.QGridLayout()
        self.main_layout.addWidget(self.title_label,            1, 0, alignment=QtC.Qt.AlignmentFlag.AlignCenter)
        self.main_layout.addWidget(self.joined_as_label,        2, 0, alignment=QtC.Qt.AlignmentFlag.AlignCenter)
        
        self.main_layout.addWidget(QtE.QHSeparationLine(),      3, 0)
        
        colour_picker = ColourPicker(self)
        self.main_layout.addWidget(colour_picker,               4, 0)
        player_list = PlayerList(self)
        self.main_layout.addWidget(player_list,                 5, 0)
        expansions_list = ExpansionsList(self)
        self.main_layout.addWidget(expansions_list,             6, 0)
        
        self.main_layout.addWidget(QtE.QHSeparationLine(),      7, 0)
        self.main_layout.addLayout(self.continue_layout,        8, 0)
        
        if self.test == 1:
            self.main_layout.addWidget(QtE.QHSeparationLine(),  9, 0)
            self.main_layout.addWidget(self.chat_display,      10, 0)
            self.main_layout.addLayout(self.input_layout,      11, 0)
        
        self.main_layout.setRowStretch(0, 1)
        self.main_layout.setRowStretch(100, 1)
        
        # self.mainWidget = QtW.QWidget()
        self.setLayout(self.main_layout)
        
        # self.stacked = QtW.QStackedWidget()
        # self.stacked = self.menu_screen.stacked
        # self.stacked.addWidget(self)
        
        # self.setCentralWidget(self.stacked)
        # self.showMaximized()
        
        if self.test == 1:
            self.Refs('chat').listen(self.update_chat_display)
    
    #%% Functionality
    def closeEvent(self, event):
        title = 'Close program?'
        text = 'Are you sure you want to close the program?'
        yesNoDialog = YesNoDialog(self, title, text)
        result = yesNoDialog.exec_()
        
        # Ignore if not accepted, else continue (close)
        if result != QtW.QDialog.Accepted:
            event.ignore()
        else:
            self.menu_screen.remove_connection(self.username)
        
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
        result = yesNoDialog.exec()
        # QtW.QDialog.Accepted
        if result == QtW.QDialog.DialogCode.Accepted:
            # Close lobby
            self.Refs('open').set(False)
    
    def start_game(self):
        self.start_game_updater.disconnect() # don't listen to updates anymore
        game_screen = GameScreen(self)
        self.stacked.addWidget(game_screen)
        self.stacked.setCurrentWidget(game_screen)
        self.menu_screen.setWindowTitle(f'Carcassonne Online - {self.username}')

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
    
    def send_feed_message(self, **kwargs):
        print('\n', kwargs)
        if len(kwargs.keys()) > 0: # call from internal game
            chat_message = {'username': self.username}
            for arg in kwargs.keys():
                chat_message[arg] = kwargs[arg]
                
            if self.Refs('feed').push(chat_message):
                print('sent')
            
        else: # call from the chat input box
            message = self.chat_input.text().strip()

            if len(message)>0:
                chat_message = {
                    'username': self.username,
                    'message': message
                }
                if self.Refs('feed').push(chat_message):
                    print('sent')

#%% Updaters
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