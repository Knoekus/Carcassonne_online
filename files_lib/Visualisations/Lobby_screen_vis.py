#%% Imports
# PyQt6
import PyQt6.QtGui     as QtG
import PyQt6.QtWidgets as QtW
import PyQt6.QtCore    as QtC
import PyQt6_Extra     as QtE

# Custom classes
# ...

# Other packages
# ...

#%% Lobby screen visualisation
class Lobby_screen_vis(QtW.QWidget):
    def __init__(self, Carcassonne):
        super().__init__()
        self.Carcassonne = Carcassonne
    
        self.Window_properties()
        self.Parameters()
        self.Layout()
    
    def Window_properties(self):
        self.Carcassonne.setWindowTitle(f'Lobby - {self.Carcassonne.lobby_key}')
    
    def Parameters(self):
        # Presets
        # ...
        pass
    
    def Layout(self):
        # Layout
        self.main_layout = QtW.QGridLayout()
        self.setLayout(self.main_layout)
        self.main_layout.setRowStretch(0, 1) # center vertically
        self.main_layout.setRowStretch(100, 1) # center vertically
        
        self._Title()
        self._Colour_picker_init()
        self._Player_list_init()
        self._Expansions_list_init()
        self._Lobby_buttons()
        
        # Insert components
        self.main_layout.addWidget(self.title_label,            1, 0, alignment=QtC.Qt.AlignmentFlag.AlignCenter)
        self.main_layout.addWidget(self.joined_as_label,        2, 0, alignment=QtC.Qt.AlignmentFlag.AlignCenter)
        self.main_layout.addWidget(QtE.QHSeparationLine(),      3, 0)
        self.main_layout.addWidget(self.colour_picker_header,   4, 0)
        self.main_layout.addLayout(self.colour_picker_hbox,     5, 0)
        self.main_layout.addWidget(self.player_list_header,     6, 0)
        self.main_layout.addWidget(self.player_list_widget,     7, 0)
        self.main_layout.addWidget(self.expansions_list_header, 8, 0)
        self.main_layout.addLayout(self.expansions_list_grid,   9, 0)
        self.main_layout.addWidget(QtE.QHSeparationLine(),     10, 0)
        self.main_layout.addLayout(self.lobby_buttons_grid,    11, 0)
        
        # Chat
        if self.Carcassonne.test == True:
            self._Chat()
            
            self.main_layout.addWidget(QtE.QHSeparationLine(), 12, 0)
            self.main_layout.addWidget(self.chat_display,      13, 0)
            self.main_layout.addLayout(self.input_layout,      14, 0)
    
    def _Title(self):
        self.title_label = QtW.QLabel(f'Lobby: {self.Carcassonne.lobby_key}')
        font = self.Carcassonne.Properties.Font(size=5, bold=True)
        self.title_label.setFont(font)
        
        self.joined_as_label = QtW.QLabel(f'Joined as: {self.Carcassonne.username}')
        font = self.Carcassonne.Properties.Font(size=2, bold=False)
        self.joined_as_label.setFont(font)
    
    def _Colour_picker_init(self):
        self._Colour_picker_vars()
        
        # Header
        self.colour_picker_header = QtW.QLabel('Pick your colour')
        font = self.Carcassonne.Properties.Font(size=2, bold=True)
        self.colour_picker_header.setFont(font)
        
        # Colour buttons
        self.colour_picker_hbox = QtW.QHBoxLayout()
        for colour in self.all_colours:
            self._Colour_picker_button(colour)
    
    def _Colour_picker_vars(self):
        self.all_colours = self.Carcassonne.Properties.colours
        self.player_colour_ref = self.Carcassonne.Refs(f'players/{self.Carcassonne.username}/colour')
        self.colour_picker_buttons = {colour:None for colour in self.all_colours}
    
    def _Colour_picker_button(self, colour):
        if self.colour_picker_buttons[colour] == None:
        # Initialisation
            # Button itself
            button = self.colour_picker_buttons[colour] = QtW.QPushButton(minimumHeight=100)
            button.setStyleSheet(self._Colour_picker_stylesheet(colour, 1))
            button.setCursor(QtG.QCursor(QtC.Qt.CursorShape.PointingHandCursor))
            self.colour_picker_hbox.addWidget(button)
            
            # Checkmark
            if colour == self.player_colour_ref.get(): # initiate with checkmark in current colour
                button.setIcon(QtG.QIcon(r'.\Images\checkmark_icon.png'))
                button.setIconSize(QtC.QSize(50,50))
        else:
        # Button already exists, so use it
            button = self.colour_picker_buttons[colour]
    
    def _Colour_picker_stylesheet(self, colour, index):
        if index == 1:
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
        elif index == 2:
            return f'''QPushButton:disabled {{
                                        background-color: rgba{tuple(int(colour[i:i+2], 16) for i in (0, 2, 4, 6))};
                                        min-width:  18px;
                                        max-width:  18px;
                                        min-height: 18px;
                                        max-height: 18px;
                                        border-radius: 13px;
                                        border-style: solid;
                                        border-width: 2px;
                                        border-color: rgb(50,50,50);
                                        padding: 2px;
                                    }}'''
    
    def _Player_list_init(self):
        self._Player_list_vars()
        
        # Header
        self.player_list_header = QtW.QLabel('Player list')
        font = self.Carcassonne.Properties.Font(size=2, bold=True)
        self.player_list_header.setFont(font)
        
        # Player list grid
        self.player_list_widget = QtW.QWidget()
        self.player_list_grid = QtW.QGridLayout()
        self.player_list_widget.setLayout(self.player_list_grid)
        self.player_list_grid.setColumnMinimumWidth(0, 60) # leader yes/no
        self.player_list_grid.setColumnMinimumWidth(1, 40) # colour indicator
        self.player_list_grid.setColumnStretch(2, 1000)    # username
        
        # Add all widgets
        for row_idx, player in enumerate(self.all_players.keys()):
            self._Player_list_add_player(row_idx, player)
    
    def _Player_list_vars(self):
        self.connections_ref = self.Carcassonne.Refs('connections')
        
        # Fill player list
        self.all_players = self.connections_ref.get()
        while len(self.all_players) != 6: # 6 is the maximum number of colours (and therefore players) in a lobby
            player_idx = len(self.all_players)+1
            self.all_players[f'placeholder_username_{player_idx}'] = 10 # this is longer than the max character limit (20)
        
        self.player_list_admins            = {x:None for x in range(6)}
        self.player_list_colour_indicators = {x:None for x in range(6)}
        self.player_list_usernames         = {x:None for x in range(6)}
    
    def _Player_list_add_player(self, row_idx, player):
        # Admin indicator
        admin = self.player_list_admins[row_idx] = QtW.QLabel()
        font = self.Carcassonne.Properties.Font(size=0, bold=False)
        admin.setFont(font)
        
        # Colour indicator
        indicator = self.player_list_colour_indicators[row_idx] = QtW.QPushButton()
        indicator.setEnabled(False)
        if len(player) <= 20:
        # Not a placeholder
            indicator_colour = self.Carcassonne.Refs(f'players/{player}/colour').get()
        else:
        # Placeholder
            indicator_colour = self.all_colours[0]
        indicator.setStyleSheet(self._Colour_picker_stylesheet(indicator_colour, 2))
        
        # Username
        username = self.player_list_usernames[row_idx] = QtW.QLabel()
        font = self.Carcassonne.Properties.Font(size=3, bold=False)
        username.setFont(font)
        
        # Make placeholders invisible (this works!)
        if len(player) > 20:
            indicator.setVisible(False)
        else:
            if player == self.Carcassonne.Refs('admin').get():
                admin.setText('(leader)')
            else:
                admin.setText('')
            username.setText(player)
            
        # Make placeholders invisible (this does NOT work!)
        # if len(player) > 20:
        #     admin.setVisible(False)
        #     indicator.setVisible(False)
        #     username.setVisible(False)
        # else:
        #     # Admin
        #     admin.setVisible(True)
        #     if player != self.Carcassonne.Refs('admin').get():
        #         admin.setText('(leader)')
        #     else:
        #         admin.setText('')
                
        #     # Indicator
        #     indicator.setVisible(True)
            
        #     # Username
        #     username.setVisible(True)
        #     username.setText(player)
        
        # Add to layout
        row_idx = self.player_list_grid.rowCount()
        self.player_list_grid.addWidget(admin,     row_idx, 0, alignment=QtC.Qt.AlignmentFlag.AlignCenter)
        self.player_list_grid.addWidget(indicator, row_idx, 1, alignment=QtC.Qt.AlignmentFlag.AlignCenter)
        self.player_list_grid.addWidget(username,  row_idx, 2, alignment=QtC.Qt.AlignmentFlag.AlignLeft)
        
        # Disable colour in picker, if applicable
        if player != self.Carcassonne.username and indicator_colour != self.all_colours[0]:
            self.colour_picker_buttons[indicator_colour].setEnabled(False)
    
    def _Player_list_update(self):
        # Set all current players to a widget and make it visible
        for row_idx, player in enumerate(self.all_players.keys()):
            admin     = self.player_list_admins[row_idx]
            indicator = self.player_list_colour_indicators[row_idx]
            username  = self.player_list_usernames[row_idx]
            
            # Set admin
            if player == self.Carcassonne.Refs('admin').get():
                admin.setText('(leader)')
            else:
                admin.setText('')
            
            # Indicator
            indicator.setVisible(True)
            indicator_colour = self.Carcassonne.Refs(f'players/{player}/colour').get()
            indicator.setStyleSheet(self._Colour_picker_stylesheet(indicator_colour, 2))
            
            # Username
            username.setText(player)
            
            # Disable colour in picker, if applicable
            if player != self.Carcassonne.username and indicator_colour != self.all_colours[0]:
                self.colour_picker_buttons[indicator_colour].setEnabled(False)
        
        # Hide all unused placeholders
        while len(self.all_players) != 6: # 6 is the maximum number of colours (and therefore players) in a lobby
            admin     = self.player_list_admins[len(self.all_players)]
            indicator = self.player_list_colour_indicators[len(self.all_players)]
            username  = self.player_list_usernames[len(self.all_players)]
            
            admin.setText('')
            indicator.setVisible(False)
            username.setText('')
            
            player_idx = len(self.all_players)+1
            self.all_players[f'placeholder_username_{player_idx}'] = 10 # this is longer than the max character limit (20)
    
    def _Expansions_list_init(self):
        self._Expansions_list_vars()
        
        # Header
        self.expansions_list_header = QtW.QLabel('Expansions')
        font = self.Carcassonne.Properties.Font(size=2, bold=True)
        self.expansions_list_header.setFont(font)
        
        # Expansions list grid
        self.expansions_list_grid = QtW.QGridLayout()
        self.expansions_list_grid.setColumnMinimumWidth(0, 10) # extra 10px padding
        
        # Get data
        admin = self.Carcassonne.Refs('admin').get()
        
        # Draw switches
        for idx, expansion in enumerate(self.Carcassonne.Properties.expansions):
            # Add switch
            expansion_switch = self.expansions_switches[expansion] = QtW.QCheckBox(expansion)
            font = self.Carcassonne.Properties.Font(size=0, bold=False)
            expansion_switch.setFont(font)
            
            checked = self.Carcassonne.Refs(f'expansions/{expansion}').get()
            expansion_switch.setChecked(checked)
            # expansion_switch.setStyleSheet(f"""QCheckBox::indicator{{
            #                               width:  {prop_s.font_sizes[1+self.lobby.font_size]}px;
            #                               height: {prop_s.font_sizes[0+self.lobby.font_size]}px;
            #                               }}""") # make a little wider
            
            self.expansions_list_grid.addWidget(expansion_switch, idx, 1)
            # TODO: functionality: expansion_switch.clicked.connect(self.Expansions_clicked(button))
            
            if admin != self.Carcassonne.username:
                expansion_switch.setEnabled(False)
                expansion_switch.setToolTip('Only the lobby leader can select expansions.')
    
    def _Expansions_list_vars(self):
        self.expansions_switches = dict()
    
    def _Lobby_buttons(self):
        # Leave button
        self.leave_button = QtW.QPushButton('Leave')
        font = self.Carcassonne.Properties.Font(size=0, bold=False)
        self.leave_button.setFont(font)
        # TODO: functionality: self.leave_button.clicked.connect(self.leave_lobby)
        
        # Start button
        self.start_button = QtW.QPushButton('Start')
        font = self.Carcassonne.Properties.Font(size=0, bold=False)
        self.start_button.setFont(font)
        # TODO: functionality: self.start_button.clicked.connect(self.start_game_admin)
        self._Update_start_button()
        
        # Layout
        self.lobby_buttons_grid = QtW.QGridLayout()
        self.lobby_buttons_grid.addWidget(self.leave_button,  0, 0)
        self.lobby_buttons_grid.addWidget(self.start_button, 0, 4)
        for idx in range(5): # equal size for all columns
            self.lobby_buttons_grid.setColumnStretch(idx, 1)
        
        # For testing, add an 'add player' button
        if self.Carcassonne.test == True:
            self.add_player_button = QtW.QPushButton('Add user2')
            font = self.Carcassonne.Properties.Font(size=0, bold=False)
            self.add_player_button.setFont(font)
            
            self.lobby_buttons_grid.addWidget(self.add_player_button, 0, 2)
    
    def _Chat(self):
        self.chat_display = QtW.QTextEdit()
        self.chat_display.setReadOnly(True)
        font = self.Carcassonne.Properties.Font(size=0, bold=False)
        self.chat_display.setFont(font)
        
        self.chat_input = QtW.QLineEdit()
        self.chat_input.setFont(font)
        self.chat_input.setPlaceholderText('Type here...')
        
        self.send_button = QtW.QPushButton('Send')
        self.send_button.setFont(font)
        # TODO: functionality: self.send_button.clicked.connect(self.send_chat_message)
        # TODO: functionality: self.chat_input.returnPressed.connect(self.send_button.click)
        
        self.input_layout = QtW.QHBoxLayout()
        self.input_layout.addWidget(self.chat_input)
        self.input_layout.addWidget(self.send_button)
    
    def _Update_start_button(self):
        self.start_button.setEnabled(False)
        if self.Carcassonne.username != self.Carcassonne.Refs('admin').get():
        # Disable start button for non-admins
            self.start_button.setToolTip('Only the lobby leader can start the game.')
        elif len(self.Carcassonne.Refs('connections').get()) == 1:
        # You are the admin, but alone in the lobby
            self.start_button.setToolTip('At least one more player is needed to start the game.')
        else:
        # You are the admin, check if all players have selected a colour
            for player in self.player_list_usernames:
                if self.Carcassonne.Refs(f'players/{player}/colour').get() == self.all_colours[0]:
                    self.start_button.setToolTip('All players must select a colour to start the game.')
                    break
            else:
                self.start_button.setEnabled(True)
                self.start_button.setToolTip('Start the game!')
    
    #%% Feed handling, receiving
    def _Feed_receive_colour_button_clicked(self, data):
        # Import data
        old_colour = data['old_colour']
        new_colour = data['new_colour']
        player_clicked = data['user']
        
        # Function
        if self.Carcassonne.username == player_clicked:
        # This player changed the colour
            if new_colour != self.all_colours[0] and self.Carcassonne.Refs(f'colours/{new_colour}').get() == 1:
            # If selected non-blank colour is occupied, don't do anything
                return
        
            # Free up previously selected colour
            self.colour_picker_buttons[old_colour].setIcon(QtG.QIcon())
            
            # Occupy newly selected colour
            self.colour_picker_buttons[new_colour].setIcon(QtG.QIcon(r'.\Images\checkmark_icon.png'))
            self.colour_picker_buttons[new_colour].setIconSize(QtC.QSize(50,50))
        else:
        # This player did not change the colour
            # Enable the old colour button
            self.colour_picker_buttons[old_colour].setEnabled(True)
            
            # Disable the new colour button
            if new_colour != self.all_colours[0]:
                self.colour_picker_buttons[new_colour].setEnabled(False)
        
        # Update player's colour indicator
        for idx in range(6):
            if self.player_list_usernames[idx].text() == player_clicked:
                break
        indicator = self.player_list_colour_indicators[idx]
        indicator.setStyleSheet(self._Colour_picker_stylesheet(new_colour, 2))
        
        # Update start button
        self._Update_start_button()
    
    def _Feed_receive_player_joined(self, data):
        # Import data
        player = data['user']
        
        # Function
        if player == self.Carcassonne.username:
        # If player who joined receives their own join event
            return
        
        # Update all players and player list
        self.all_players = self.connections_ref.get()
        self._Player_list_update()
        self._Update_start_button()
    
    def _Feed_receive_player_left(self, data):
        # Import data
        player_left = data['user']
        
        # Function
        if player_left == self.Carcassonne.username:
        # If player who left receives their own join event
            return
        
        # Update all players and player list
        self.all_players = self.connections_ref.get()
        self.all_players.pop(player_left, None) # try to delete player from list
        self._Player_list_update()
        self._Update_start_button()
        