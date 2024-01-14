import PyQt6.QtGui     as QtG
import PyQt6.QtWidgets as QtW
import PyQt6.QtCore    as QtC
import PyQt6_Extra     as QtE

import Classes.Meeples as Meeples
import prop_s
import tile_data

import string
import os
import random as rnd
import copy
import numpy

class Tiles():
    def __init__(self, game):
        self.game = game
        self.lobby_key = game.lobby.lobby_key
        self.game.tiles = dict()
        self.game.last_placed_tile = None
    
    def Add_tiles(self, prefix, numbers):
        self.game.tiles[prefix] = dict()
        for idx, number in enumerate(numbers):
            letter = string.ascii_uppercase[idx]
            self.game.tiles[prefix][letter] = number
    
    #%% New tile placement
    def Update_tiles_left_label(self):
        self.game.tiles_left = sum([sum(expansion.values()) for expansion in self.game.tiles.values()])
        self.game.tiles_left_label.setText(f'{self.game.tiles_left} tiles left.')
    
    def New_tile(self, tile_idx_in=None, tile_letter_in=None):
        # Disable end turn button and meeples: the tile must be placed first
        self.game.button_end_turn.setEnabled(0)
        Meeples.En_dis_able_meeples(self.game, enable=False)
        self.game.new_tile.rotation = 0 # start a new tile with 0 rotation
        
        # Get a new tile
        while True:
            tile_idx, tile_letter, file = self.Choose_tile(tile_idx_in, tile_letter_in)
            # Give new tile the material data            
            for material in self.game.materials:
                try:
                    self.game.new_tile.material_data[material] = tile_data.tiles[tile_idx][tile_letter][material]
                except: None # ignore material if it's not in the game (shouldn't be able to happen)
            
            # Allow tile if there are options to place it
            options = set()
            for idx in range(4): # try each orientation
                options |= self.Tile_options(tile_idx, tile_letter)
                if len(options) > 0: 
                    # if options are found before trying all rotations, don't try the rest and rotate back
                    for idx2 in range(idx):
                        self.game.new_tile.rotate(-90)
                    break
                else:
                    # self.game.new_tile.clicked_l.emit()
                    self.game.new_tile.rotate(90)
            if len(options) > 0:
                # self.game.new_tile.rotation = 0 # reset rotation
                break
            elif True:
                print(f'\n{tile_idx}{tile_letter} is infeasible\n')
        
        # Push to event log
        self.game.lobby.send_feed_message(event          = 'new_tile',
                                          tile_idx       = tile_idx,
                                          tile_letter    = tile_letter)
        
        # Update tiles left
        self.game.new_tile_anim.swap_image(file, tile_idx, tile_letter, 500) # replaces set_tile, maybe relocate to QtE
        # self.game.new_tile.enable()
        if self.game.tiles[tile_idx][tile_letter] > 1:
            self.game.tiles[tile_idx][tile_letter] -= 1 # decrease number of tiles by 1
        else:
            if len(self.game.tiles[tile_idx].keys()) > 1:
                self.game.tiles[tile_idx].pop(tile_letter) # delete tile if none left
            else:
                self.game.tiles.pop(tile_idx) # delete expansion if no tiles left
        
        # Update tiles left label
        self.Update_tiles_left_label()
        
        # Show placement options
        self.Show_options()
    
    def Choose_tile(self, tile_idx=None, tile_letter=None):
        # Choose new tile
        if tile_idx == None and tile_letter == None:
            # New idx and letter
            tile_idx    = rnd.choice(list(self.game.tiles.keys()))
            tile_letter = rnd.choice(list(self.game.tiles[tile_idx].keys()))
        elif tile_idx != None and tile_letter == None: # if only expansion is given (e.g. for river building)
            # Only new letter
            tile_letter = rnd.choice(list(self.game.tiles[tile_idx].keys()))
            
        # Get expansion title
        tile_title  = prop_s.tile_titles[tile_idx-1]
        
        # Get tile folder
        if self.lobby_key == 'test2':
            path = f'..\\Images\\{tile_title}\\{tile_idx}{tile_letter}'
        else: # call from lobby
            path = f'.\\Images\\{tile_title}\\{tile_idx}{tile_letter}'
        
        # Choose a random design
        number_of_pngs = len([name for name in os.listdir(path) if os.path.isfile(os.path.join(path, name))])-1
        number = rnd.choice(range(number_of_pngs))
        
        # Get file
        file = path+f'\\{number}.png'
        
        return tile_idx, tile_letter, file
    
    def Option_clicked(self, row, col):
        def clicked():
            new_tile = self.game.new_tile
            
            # Get image and information
            file        = copy.deepcopy(new_tile.file)
            tile_idx    = copy.deepcopy(new_tile.index)
            tile_letter = copy.deepcopy(new_tile.letter)
            rotation    = copy.deepcopy(new_tile.rotation)
            
            # Place tile
            self.Place_tile(file, tile_idx, tile_letter, row, col, rotation)
            self.game.options.remove((row, col))
            
            # Reset new tile
            if self.lobby_key == 'test2':
                file = r'..\Images\tile_logo.png'
            else: # call from lobby
                file = r'.\Images\tile_logo.png'
            # new_tile.reset(file)
            new_tile.draw_image(file)
            new_tile.disable()
            # new_tile.rotation = 0
            
            # Clear old options
            for option in self.game.options:
                opt_row, opt_col = option
                tile = self.game.board_tiles[opt_row][opt_col]
                tile.disable()
                tile.set_tile(None, None, None, self.game.materials)
            
            # Enable/disable 'end turn' button and meeples
            if self.game.username == self.game.current_player:
                self.game.button_end_turn.setEnabled(1)
            else:
                self.game.button_end_turn.setEnabled(0)
            Meeples.En_dis_able_meeples(self.game, enable=True)
            
            # Test purposes
            # self.New_tile(1)
        return clicked
    
    def Place_tile(self, file, tile_idx, tile_letter, row, col, rotation=0):
        # Add new row if necessary
        if row < self.game.board_rows[0]:
            self._Board_new_row_above()
        elif row > self.game.board_rows[1]:
            self._Board_new_row_below()
        
        # Add new col if necessary
        if col < self.game.board_cols[0]:
            self._Board_new_col_left()
        elif col > self.game.board_cols[1]:
            self._Board_new_col_right()
            
        # Place tile
        board_tile = self.game.board_tiles[row][col]
        board_tile.set_tile(file, tile_idx, tile_letter, self.game.materials)
        board_tile.disable()
        self.game.last_placed_tile = board_tile
        
        # Rotating
        # board_tile.rotating = True
        rotations = int(numpy.floor(rotation%360/90))
        if rotations < 0:
            for idx in range(-rotations):
                board_tile.rotate(-90)
        elif rotations > 0:
            for idx in range(rotations):
                board_tile.rotate(90)
        board_tile.rotating = False
        
        # Update possessions
        self.Update_possessions(board_tile.material_data, row, col)
            
        # Push message to event log
        self.game.lobby.send_feed_message(event          = 'placed_tile',
                                          tile_idx       = tile_idx,
                                          tile_letter    = tile_letter,
                                          rotation       = rotation,
                                          row = row, col = col)
    
    #%% Possessions
    def Update_possessions(self, tile_data, row, col):
        def get_neighbours(data, idx):
            # Get neighbouring tiles and number of edges the material patch covers
            edges = 0
            neighbours = []
            if idx in data[0][1:-1]: # north
                edges += 1
                tile = self.game.board_tiles[row-1][col]
                if len(tile.material_data) > 0: # tile is not empty
                    neighbours += [tile]
            if idx in [data[x][-1] for x in range(len(data))][1:-1]: # east
                edges += 1
                tile = self.game.board_tiles[row][col+1]
                if len(tile.material_data) > 0: # tile is not empty
                    neighbours += [tile]
            if idx in data[-1][1:-1]: # south
                edges += 1
                tile = self.game.board_tiles[row+1][col]
                if len(tile.material_data) > 0: # tile is not empty
                    neighbours += [tile]
            if idx in [data[x][0] for x in range(len(data))][1:-1]: # west
                edges += 1
                tile = self.game.board_tiles[row][col-1]
                if len(tile.material_data) > 0: # tile is not empty
                    neighbours += [tile]
            return neighbours, edges
        
        for material in tile_data.keys():
        # For all material of the placed tile
            mat_data = tile_data[material]
            for mat_idx in range(1, max(max(mat_data))+1):
            # Check each patch of material in the tile
                neighbours, edges = get_neighbours(mat_data, mat_idx)
                if len(neighbours) == 0:
                # The material patch does not touch any neighbours
                    self._New_possession(edges, material, mat_idx, row, col)
                    
                elif len(neighbours) == 1:
                # There is a neighbouring tile, don't create new possession but append to existing one
                    possessions = self.game.possessions
                    pos_idx = neighbours[0].possessions[material][mat_idx]
                    self.game.board_tiles[row][col].update_possessions(material, mat_idx, pos_idx) # update tile reference
                    pos_n = possessions[material][pos_idx]
                    self._Append_possession(pos_n, edges, material, mat_idx, row, col)
                    
                elif len(neighbours) > 1:
                # There are multiple neighbouring tiles, join them together
                    self._Join_possessions(neighbours, edges, material, mat_idx, row, col)
                
    def _New_possession(self, edges, material, mat_idx, row, col):
        possessions = self.game.possessions
        pos_idx = len(possessions[material])
        
        # Make reference to possession inside the tile data
        tile = self.game.board_tiles[row][col]
        tile.update_possessions(material, mat_idx, pos_idx) # update tile reference
        
        # Create possession
        if material == 'grass':
            possessions[material][pos_idx] = {'open': # can this still be used to append/merge?
                                                  True,
                                              'tiles': # all tiles and their material index that belong to this possession
                                                  [(tile, mat_idx)],
                                              'player_strength': # meeple strength per player
                                                  {player: 
                                                   {meeple_type:0 for meeple_type in self.game.meeple_types}
                                                   for player in self.game.connections},
                                              'finished_cities': # number of finished cities in field
                                                  0
                                              }
        elif material == 'road':
            possessions[material][pos_idx] = {'open': # can this still be used to append/merge?
                                                  True,
                                              'tiles': # all tiles and their material index that belong to this possession
                                                  [(tile, mat_idx)],
                                              'player_strength': # meeple strength per player
                                                  {player: 
                                                   {meeple_type:0 for meeple_type in self.game.meeple_types}
                                                   for player in self.game.connections},
                                              'open_edges': # number of open edges of this possession
                                                  edges
                                              }
            # Add inn support if that expansion is active
            if r'Inns && Cathedrals' in self.game.expansions:
                possessions[material][pos_idx]['inn'] = False
        elif material == 'city':
            possessions[material][pos_idx] = {'open': # can this still be used to append/merge?
                                                  True,
                                              'tiles': # all tiles and their material index that belong to this possession
                                                  [(tile, mat_idx)],
                                              'player_strength': # meeple strength per player
                                                  {player: 
                                                   {meeple_type:0 for meeple_type in self.game.meeple_types}
                                                   for player in self.game.connections},
                                              'open_edges': # number of open edges of this possession
                                                  edges,
                                              'shield_tiles': # number of shields in city
                                                  0
                                              }
            # Add shield count
            shield_count = self.Shields_on_tile(tile)
            possessions[material][pos_idx]['shield_tiles'] = shield_count
            
            # Add cathedral support if that expansion is active
            if r'Inns && Cathedrals' in self.game.expansions:
                possessions[material][pos_idx]['cathedral'] = False
        elif material == 'monastery':
            possessions[material][pos_idx] = {'open': # can this still be used to append/merge?
                                                  True,
                                              'tiles': # tile and material index of monastery
                                                  [(tile, mat_idx)],
                                              'player_strength': # meeple strength per player
                                                  {player: 
                                                   {meeple_type:0 for meeple_type in self.game.meeple_types}
                                                   for player in self.game.connections},
                                              'surrounding_tiles': # number of surrounding tiles
                                                  1 # tile itself makes it 1 instead of 0
                                              }
            # Calculate surrounding tiles
            for row_n, col_n in [(-1, -1), (-1, 0), (-1, 1), (0, -1), (0, 1), (1, -1), (1, 0), (1, 1)]:
                neighbour_tile = self.game.board_tiles[row + row_n][col + col_n]
                if len(neighbour_tile.material_data) > 0:
                    possessions[material][pos_idx] += 1
    
    def _Join_possessions(self, neighbours, edges, material, mat_idx, row, col):
        # Join two possessions together into one big possession
        possessions = self.game.possessions
        tile = self.game.board_tiles[row][col]
        
        pos_neighs = dict()
        for idx, neighbour in enumerate(neighbours):
            # Get neighbour possession
            pos_idx = neighbour.possessions[material][mat_idx]
            pos_neighs[idx] = possessions[material][pos_idx]
            
            # Close neighbour possession
            pos_neighs[idx]['open'] = False
        
        # Make merged possession
        pos_idx = len(possessions[material])
        tile.update_possessions(material, mat_idx, pos_idx) # update tile reference
        pos_merged = possessions[material][pos_idx] = {'open': True}
        for attribute in pos_neighs[0].keys():
            if attribute == 'open':
                pass # ignore open attribute
            elif attribute == 'player_strength':
            # player strength
                pos_merged['player_strength'] = {player: 
                                         {meeple_type:0 for meeple_type in self.game.meeple_types}
                                         for player in self.game.connections}
                for pos_n in pos_neighs.values():
                    for player in self.game.connections:
                        for meeple_type in self.game.meeple_types:
                            pos_merged['player_strength'][player][meeple_type] += pos_n['player_strength'][player][meeple_type]
            elif attribute in ['tiles']:
            # list
                pos_merged[attribute] = list()
                for pos_n in pos_neighs.values():
                    pos_merged[attribute] += [pos_n[attribute]]
            elif attribute in ['finished_cities', 'shield_tiles']:
            # integer
                pos_merged[attribute] = 0
                for pos_n in pos_neighs.values():
                    pos_merged[attribute] += pos_n[attribute]
            elif attribute in ['inn', 'cathedral']:
            # boolean
                pos_merged[attribute] = False
                for pos_n in pos_neighs.values():
                    pos_merged[attribute] = pos_merged[attribute] or pos_n[attribute]
        
        # Append placed tile to merged possession
        self._Append_possession(pos_merged, edges, material, mat_idx, row, col)
    
    def _Append_possession(self, pos_n, edges, material, mat_idx, row, col):
        # Append tile to an existing possession
        tile = self.game.board_tiles[row][col]
        
        # Append possession
        if 'tiles' in pos_n.keys():
            pos_n['tiles'] += [(tile, mat_idx)]
            
        if 'open_edges' in pos_n.keys():
            pos_n['open_edges'] += edges-1
            # Close possession if open_edges == 0
            if pos_n['open_edges'] == 0:
                pos_n['open'] = False
                self.Possession_finished(pos_n)
            
        if 'shield_tiles' in pos_n.keys():
            shield_count = self.Shields_on_tile(tile)
            pos_n['shield_tiles'] += shield_count
        
        if 'inn' in pos_n.keys() and r'Inns && Cathedrals' in self.game.expansions:
            inn_bool = self.Inn_on_tile(tile)
            pos_n['inn'] = pos_n['inn'] or inn_bool
        
        if 'cathedral' in pos_n.keys() and r'Inns && Cathedrals' in self.game.expansions:
            cathedral_bool = self.Cathedral_on_tile(tile)
            pos_n['cathedral'] = pos_n['cathedral'] or cathedral_bool
            
    def Shields_on_tile(self, tile):
        if tile.index == 1:
        # Base game
            if tile.letter in ['M', 'O', 'Q', 'U', 'W', 'X']:
                return 1
            else:
                return 0
        elif tile.index == 2:
        # River 1
            return 0
        elif tile.index == 3:
        # Inns & Cathedrals
            if tile.letter in ['L', 'P', 'Q']:
                return 1
            else:
                return 0
        elif tile.index == 4:
        # Abbot
            if tile.letter == 'D':
                return 1
            else:
                return 0
        else:
            raise Exception(f'Tile index {tile.index} unknown or not implemented.')
    
    def Inn_on_tile(self, tile):
        if tile.index == 3:
        # Inns & Cathedrals
            if tile.letter in ['A', 'B', 'C', 'L', 'M', 'N']:
                return True
        elif tile.index > 4:
            raise Exception(f'Tile index {tile.index} unknown or not implemented.')
        
        return False
    
    def Cathedral_on_tile(self, tile):
        if tile.index == 3:
        # Inns & Cathedrals
            if tile.letter == 'K':
                return True
        elif tile.index > 4:
            raise Exception(f'Tile index {tile.index} unknown or not implemented.')
        
        return False
        
    def Possession_finished(self, possession):
        pass
    
    #%% Options
    def Show_options(self):
        tile_idx, tile_letter = self.game.new_tile.index, self.game.new_tile.letter
        
        # Clear old options
        for option in self.game.options:
            row, col = option
            tile = self.game.board_tiles[row][col]
            tile.disable()
            tile.set_tile(None, None, None, self.game.materials)
        
        # Get new options
        self.game.options = self.Tile_options(tile_idx, tile_letter)
        
        # Get image
        if self.lobby_key == 'test2':
            file = '..\\Images\\tile_available'
        else: # call from lobby
            file = '.\\Images\\tile_available'
        
        # Set options' images
        for option in self.game.options:
            row, col = option
            tile = self.game.board_tiles[row][col]
            tile.enable()
            tile.set_tile(file, None, None, self.game.materials)
            try: tile.clicked.disconnect()
            except: None
            tile.clicked.connect(self.Option_clicked(row, col))

    def Tile_options(self, tile_idx, tile_letter):
        """Find all empty neighbour tiles where the new tile can be placed."""
        def get_edge(data, pos:str):
            if pos == 'N': # north
                edge = data[0][1:-1]
            elif pos == 'E': # east
                edge = [data[x][-1] for x in range(len(data))][1:-1]
            elif pos == 'S': # south
                edge = data[-1][1:-1]
            elif pos == 'W': # west
                edge = [data[x][0] for x in range(len(data))][1:-1]
            elif pos == 'all': # all edges
                edge = get_edge(data, 'N') + get_edge(data, 'E') + get_edge(data, 'S') + get_edge(data, 'W')
            else:
                raise Exception("Unknown position of tile.")
            # convert to booleans to only consider yes/no material, not number of material patch
            return [bool(x) for x in edge]
        
        options = set()
        options_deleted = set()
        # Find all tiles in the board
        for row in range(self.game.board_rows[0], self.game.board_rows[1]+1):
            for col in range(self.game.board_cols[0], self.game.board_cols[1]+1):
                tile = self.game.board_tiles[row][col]
                
                # Find all empty neighbours
                if len(tile.material_data) > 0: # if tile not empty
                    neighbours = [(row-1, col), (row, col+1), (row+1, col), (row, col-1)]
                    for pos, coords in enumerate(neighbours):
                        neighbour_tile = self.game.board_tiles[coords[0]][coords[1]]
                        
                        # Check empty neighbour for feasibility
                        if len(neighbour_tile.material_data) == 0 and coords not in options_deleted: # if tile empty
                            data_n_all = self.game.new_tile.material_data
                            data_t_all = tile.material_data
                            
                            options.add(coords)
                            # Check all materials
                            for material in self.game.materials:
                                # Ignore material if it's not in either tile
                                if material not in data_n_all.keys() and material not in data_t_all.keys():
                                    continue
                                
                                # Material is in both tiles
                                elif material in data_n_all.keys() and material in data_t_all.keys():
                                    data_n = data_n_all[material]
                                    data_t = data_t_all[material]
                                    if pos == 0: # north
                                        # south of neighbour should match north of tile
                                        edge_n = get_edge(data_n, 'S')
                                        edge_t = get_edge(data_t, 'N')
                                    elif pos == 1: # east
                                        # west of neighbour should match east of tile
                                        edge_n = get_edge(data_n, 'W')
                                        edge_t = get_edge(data_t, 'E')
                                    elif pos == 2: # south
                                        # north of neighbour should match south of tile
                                        edge_n = get_edge(data_n, 'N')
                                        edge_t = get_edge(data_t, 'S')
                                    elif pos == 3: # west
                                        # east of neighbour should match west of tile
                                        edge_n = get_edge(data_n, 'E')
                                        edge_t = get_edge(data_t, 'W')
                                    else:
                                        raise Exception("Unknown position of tile.")
                                    if edge_n != edge_t:
                                        # print(f'   {material} does not match {coords}: \n     {[int(x) for x in edge_n]}\n     {[int(x) for x in edge_t]}')
                                        options.remove(coords)
                                        options_deleted.add(coords)
                                        break # stop trying materials
                                
                                # Material is only in new tile
                                elif material in data_n_all.keys():
                                    data_n = data_n_all[material]
                                    if pos == 0: # north
                                        # south of neighbour should match north of tile
                                        edge_n = get_edge(data_n, 'S')
                                    elif pos == 1: # east
                                        # west of neighbour should match east of tile
                                        edge_n = get_edge(data_n, 'W')
                                    elif pos == 2: # south
                                        # north of neighbour should match south of tile
                                        edge_n = get_edge(data_n, 'N')
                                    elif pos == 3: # west
                                        # east of neighbour should match west of tile
                                        edge_n = get_edge(data_n, 'E')
                                    else:
                                        raise Exception("Unknown position of tile.")
                                        
                                    if sum(edge_n) > 0:
                                        # Remove option if unique material is on edge of importance
                                        # print(f'   {material} is unique in NEW and does not match {coords}')
                                        options.remove(coords)
                                        options_deleted.add(coords)
                                        break # stop trying materials
                                
                                # Material is only in old tile
                                elif material in data_t_all.keys():
                                    data_t = data_t_all[material]
                                    if pos == 0: # north
                                        # south of neighbour should match north of tile
                                        edge_t = get_edge(data_t, 'N')
                                    elif pos == 1: # east
                                        # west of neighbour should match east of tile
                                        edge_t = get_edge(data_t, 'E')
                                    elif pos == 2: # south
                                        # north of neighbour should match south of tile
                                        edge_t = get_edge(data_t, 'S')
                                    elif pos == 3: # west
                                        # east of neighbour should match west of tile
                                        edge_t = get_edge(data_t, 'W')
                                    else:
                                        raise Exception("Unknown position of tile.")
                                        
                                    if sum(edge_t) > 0:
                                        # Remove option if unique material is on edge of importance
                                        # print(f'   {material} is unique in TILE and does not match {coords}')
                                        options.remove(coords)
                                        options_deleted.add(coords)
                                        break # stop trying materials
        return options
    
    #%% Board
    def Board_init(self):
        '''
        board_base  : the core QVBoxLayout
        board       : all QHBoxLayouts
        board_tiles : all references to tile widgets
        '''
        self.game.board = dict()
        self.game.board_tiles = dict()
        self.game.board_rows = [0,0]
        self.game.board_cols = [0,0]
        
        # Initial layout
        self.game.board_base.addStretch(1)
        self.game.board_tiles[-1] = dict()
        self.__Board_new_row(-1, -1)
        self.game.board_tiles[ 0] = dict()
        self.__Board_new_row( 0, -1)
        self.game.board_tiles[ 1] = dict()
        self.__Board_new_row( 1, -1)
        self.game.board_base.addStretch(1)
        
        # Set board to ScrollArea widget
        self.game.board_widget.setLayout(self.game.board_base)
    
    def _Board_new_row_above(self):
        self.game.board_rows[0] -= 1
        new_row_idx = self.game.board_rows[0]-1
        insert_idx = 1
        self.__Board_new_row(new_row_idx, insert_idx)
    
    def _Board_new_row_below(self):
        self.game.board_rows[1] += 1
        new_row_idx = self.game.board_rows[1]+1
        insert_idx = len(self.game.board_base)-1
        self.__Board_new_row(new_row_idx, insert_idx)
    
    def __Board_new_row(self, new_row_idx, insert_idx):
        # Make new row index available
        self.game.board_tiles[new_row_idx] = dict()
        
        # Empty row
        new_row = self.game.board[new_row_idx] = QtW.QHBoxLayout()
        new_row.setSpacing(prop_s.tile_spacing)
        new_row.setSizeConstraint(QtW.QLayout.SizeConstraint.SetFixedSize)
        
        # Fill row with necessary empty tiles
        new_row.addStretch(0)
        for col_idx in range(self.game.board_cols[0]-1, self.game.board_cols[1]+2):
            new_row.addWidget(self._New_tile(new_row_idx, col_idx))
        new_row.addStretch(0)
        
        # Add row to vertical base
        self.game.board_base.insertLayout(insert_idx, new_row)
        # print(f'Added row {new_row_idx} at {insert_idx}')
    
    def _Board_new_col_left(self):
        # self.__Board_new_col(1)
        self.game.board_cols[0] -= 1
        new_col_idx = self.game.board_cols[0]-1
        insert_idx = 1
        self.__Board_new_col(new_col_idx, insert_idx)
    
    def _Board_new_col_right(self):
        # self.__Board_new_col(-2)
        self.game.board_cols[1] += 1
        new_col_idx = self.game.board_cols[1]+1
        insert_idx = len(self.game.board[0])-1
        self.__Board_new_col(new_col_idx, insert_idx)
        
    def __Board_new_col(self, new_col_idx, insert_idx):
        # In each row add a column
        for row_idx in range(self.game.board_rows[0]-1, self.game.board_rows[1]+2):
            row = self.game.board[row_idx]
            row.insertWidget(insert_idx, self._New_tile(row_idx, new_col_idx))
        # print(f'Added col {new_col_idx} at {insert_idx}')
    
    def _New_tile(self, row, col):
        # if self.lobby_key == 'test2':
        #     file = '..\\Images\\Coin_icon.png'
        # else: # call from lobby
        #     file = '.\\Images\\Coin_icon.png'
        file = None
        
        empty_tile = QtE.Tile(file, prop_s.tile_size, self.game)
        self.game.board_tiles[row][col] = empty_tile
        return empty_tile