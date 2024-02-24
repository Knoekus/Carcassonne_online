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
        self.main_layout.addLayout(self.player_list_grid,       7, 0)
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
    
    def _Player_list_init(self):
        self._Player_list_vars()
        
        # Header
        self.player_list_header = QtW.QLabel('Player list')
        font = self.Carcassonne.Properties.Font(size=2, bold=True)
        self.player_list_header.setFont(font)
        
        # Player list grid
        self.player_list_grid = QtW.QGridLayout()
        # self.player_list_grid.setColumnMinimumWidth(0, 60) # leader yes/no
        # self.player_list_grid.setColumnMinimumWidth(1, 40) # colour indicator
        # self.player_list_grid.setColumnStretch(2, 1000)    # username
        
        # Add all current connections to player list
        for player in self.player_list_usernames:
            self._Player_list_add_player(player)
    
    def _Player_list_add_player(self, player, feed=False):
        # Admin indicator
        admin = self.player_list_admins[player] = QtW.QLabel()
        admin.setText('(leader)')
        font = self.Carcassonne.Properties.Font(size=0, bold=False)
        admin.setFont(font)
        if player != self.Carcassonne.Refs('admin').get():
            admin.setVisible(False)
        
        # Colour indicator
        indicator = self.player_list_colour_indicators[player] = QtW.QPushButton()
        indicator.setEnabled(False)
        indicator_colour = self.Carcassonne.Refs(f'players/{player}/colour').get()
        indicator.setStyleSheet(self._Colour_picker_stylesheet(indicator_colour, 2))
        
        # Username
        username = self.player_list_usernames[player] = QtW.QLabel()
        username.setText(player)
        font = self.Carcassonne.Properties.Font(size=0, bold=False)
        username.setFont(font)
        
        # Add to layout
        row_idx = self.player_list_grid.rowCount()
        print('  Row index before:', row_idx)
        print(f'  {player} - {indicator_colour}')
        self.player_list_grid.addWidget(admin,     row_idx, 0, alignment=QtC.Qt.AlignmentFlag.AlignCenter)
        self.player_list_grid.addWidget(indicator, row_idx, 1, alignment=QtC.Qt.AlignmentFlag.AlignCenter)
        self.player_list_grid.addWidget(username,  row_idx, 2, alignment=QtC.Qt.AlignmentFlag.AlignLeft)
        print('  Row index after: ', self.player_list_grid.rowCount())
        
        # Disable colour in picker, if applicable
        if player != self.Carcassonne.username and indicator_colour != self.all_colours[0]:
            self.colour_picker_buttons[indicator_colour].setEnabled(False)

    def _Player_list_vars(self):
        self.connections_ref = self.Carcassonne.Refs('connections')
        
        self.player_list_admins            = {x:None for x in self.connections_ref.get()}
        self.player_list_colour_indicators = {x:None for x in self.connections_ref.get()}
        self.player_list_usernames         = {x:None for x in self.connections_ref.get()}
    
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
        # TODO: functionality: admin = self.lobby.Refs('admin').get()
        
        # Draw switches
        for idx, expansion in enumerate(self.Carcassonne.Properties.expansions):
            # Add switch
            switch = self.expansions_switches[expansion] = QtW.QCheckBox(expansion)
            font = self.Carcassonne.Properties.Font(size=0, bold=False)
            switch.setFont(font)
            
            checked = self.Carcassonne.Refs(f'expansions/{expansion}').get()
            switch.setChecked(checked)
            # button.setStyleSheet(f"""QCheckBox::indicator{{
            #                           width:  {prop_s.font_sizes[1+self.lobby.font_size]}px;
            #                           height: {prop_s.font_sizes[0+self.lobby.font_size]}px;
            #                           }}""") # make a little wider
            
            self.expansions_list_grid.addWidget(switch, idx, 1)
            # TODO: functionality: switch.clicked.connect(self.Expansions_clicked(button))
            
            # TODO: functionality
            # if admin != self.Carcassonne.username:
            #     switch.setEnabled(False)
            #     switch.setToolTip('Only the lobby leader can select expansions.')
    
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
    
    #%% Feed handling
    def _Feed_receive_player_joined(self, data):
        # Import data
        player = data['user']
        
        # Function
        if player == self.Carcassonne.username:
        # If player who joined receives their own join event
            return
        
        print('\nAdding player...')
        self._Player_list_add_player(player, feed=True)
        # FIXME: this is executing, but not showing in the player list.
        print('Player added.')
        
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
        indicator = self.player_list_colour_indicators[player_clicked]
        indicator.setStyleSheet(self._Colour_picker_stylesheet(new_colour, 2))