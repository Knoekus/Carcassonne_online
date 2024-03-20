#%% Imports
# PyQt6
import PyQt6.QtCore    as QtC
import PyQt6.QtGui     as QtG
import PyQt6.QtWidgets as QtW
import PyQt6_Extra     as QtE

# Custom classes
import Classes.Animations as Animations

# Other packages
import numpy as np
import time

#%% Possessions class
class Possessions():
    def __init__(self, Carcassonne):
        self.Carcassonne = Carcassonne
        self.game_vis = self.Carcassonne.game_vis
        self.finished_anim = Animations.AnimationGroup_parallel(3)
    
    def Setup(self):
        self.Carcassonne.possessions = {material:dict() for material in self.Carcassonne.materials}
        
    def Connections(self):
        '''Get an up-to-date player list of the current connections to the lobby.'''
        for idx in range(20):
            player_list_dict = self.Carcassonne.Refs('connections').get()
            if type(player_list_dict) == type(dict()):
                player_list = player_list_dict.keys()
                break
            else:
                time.sleep(0.1)
        else:
            raise Warning('No connections found after 2 seconds.')
        return player_list
        
    def Update_possessions(self, tile_data, row, col):
        def Get_neighbours(material, data, idx):
            # Get neighbouring tiles and number of edges the material patch covers
            edges = 0
            neighbours = []
            if idx in data[0][1:-1]: # north
                edges += 1
                tile = self.Carcassonne.board_tiles[row-1][col]
                if len(tile.material_data) > 0: # tile is not empty
                    col_idx = data[0][1:-1].index(idx)+1
                    mat_idx_n = tile.material_data[material][-1][col_idx]
                    neighbours += [(tile, mat_idx_n)]
            if idx in [data[x][-1] for x in range(len(data))][1:-1]: # east
                edges += 1
                tile = self.Carcassonne.board_tiles[row][col+1]
                if len(tile.material_data) > 0: # tile is not empty
                    row_idx = [data[x][-1] for x in range(len(data))][1:-1].index(idx)+1
                    mat_idx_n = tile.material_data[material][row_idx][0]
                    neighbours += [(tile, mat_idx_n)]
            if idx in data[-1][1:-1]: # south
                edges += 1
                tile = self.Carcassonne.board_tiles[row+1][col]
                if len(tile.material_data) > 0: # tile is not empty
                    col_idx = data[-1][1:-1].index(idx)+1
                    mat_idx_n = tile.material_data[material][0][col_idx]
                    neighbours += [(tile, mat_idx_n)]
            if idx in [data[x][0] for x in range(len(data))][1:-1]: # west
                edges += 1
                tile = self.Carcassonne.board_tiles[row][col-1]
                if len(tile.material_data) > 0: # tile is not empty
                    row_idx = [data[x][0] for x in range(len(data))][1:-1].index(idx)+1
                    mat_idx_n = tile.material_data[material][row_idx][-1]
                    neighbours += [(tile, mat_idx_n)]
            return neighbours, edges
        
        # First check if possessions are finished, if not: enable end turn button
        self.end_turn = True
        
        # Update directly connected possessions
        for material in tile_data.keys():
        # For all material of the placed tile
            mat_data = tile_data[material]
            for mat_idx in range(1, np.max(mat_data)+1):
            # Check each patch of material in the tile
                neighbours, edges = Get_neighbours(material, mat_data, mat_idx)
                
                if len(neighbours) == 0:
                # The material patch does not touch any neighbours
                    self._New_possession(edges, material, mat_idx, row, col)
                    
                elif len(neighbours) == 1:
                # There is a neighbouring tile, don't create new possession but append to existing one
                    tile_n, mat_idx_n = neighbours[0]
                    possessions = self.Carcassonne.possessions
                    pos_idx = tile_n.possessions[material][mat_idx_n]
                    self.Carcassonne.board_tiles[row][col].update_possessions(material, mat_idx, pos_idx) # update tile reference
                    pos_n = possessions[material][pos_idx]
                    self._Append_possession(pos_n, 1, edges, material, mat_idx, row, col) # 1 for only 1 neighbouring possession
                    
                elif len(neighbours) > 1:
                # There are multiple neighbouring tiles, join them together
                    self._Join_possessions(neighbours, edges, material, mat_idx, row, col)
        
        # Update indirectly connected possessions
        for row_n, col_n in [(-1, -1), (-1, 0), (-1, 1), (0, -1), (0, 1), (1, -1), (1, 0), (1, 1)]:
            tile_n = self.Carcassonne.board_tiles[row + row_n][col + col_n]
            if len(tile_n.material_data) > 0:
                if 'monastery' in tile_n.material_data.keys():
                    pos_idx = tile_n.possessions['monastery'][1]
                    pos_n = self.Carcassonne.possessions['monastery'][pos_idx]
                    material = 'monastery'
                    self._Append_possession(pos_n, 1, edges, material, mat_idx, row, col)
        
        # Enable end turn button if no possessions were finished
        if self.end_turn == True:
            self.game_vis.button_end_turn.setEnabled(True)
            self.game_vis._Meeples_enable(True)
                
    def _New_possession(self, edges, material, mat_idx, row, col):
        possessions = self.Carcassonne.possessions
        pos_idx = len(possessions[material])
        
        # Make reference to possession inside the tile data
        tile = self.Carcassonne.board_tiles[row][col]
        tile.update_possessions(material, mat_idx, pos_idx) # update tile reference
        
        # Create possession
        if material == 'grass':
            possessions[material][pos_idx] = {'open': # can this still be used to append/merge?
                                                  True,
                                              'tiles': # all tiles and their material index that belong to this possession
                                                  [(tile, mat_idx)],
                                              'player_strength': # meeple strength per player
                                                  {player: 
                                                   {meeple_type:0 for meeple_type in self.Carcassonne.meeples.keys()}
                                                   for player in self.Connections()},
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
                                                   {meeple_type:0 for meeple_type in self.Carcassonne.meeples.keys()}
                                                   for player in self.Connections()},
                                              'open_edges': # number of open edges of this possession
                                                  edges
                                              }
            # Add inn support if that expansion is active
            if r'Inns && Cathedrals' in self.Carcassonne.expansions:
                possessions[material][pos_idx]['inn'] = False
        elif material == 'city':
            possessions[material][pos_idx] = {'open': # can this still be used to append/merge?
                                                  True,
                                              'tiles': # all tiles and their material index that belong to this possession
                                                  [(tile, mat_idx)],
                                              'player_strength': # meeple strength per player
                                                  {player: 
                                                   {meeple_type:0 for meeple_type in self.Carcassonne.meeples.keys()}
                                                   for player in self.Connections()},
                                              'open_edges': # number of open edges of this possession
                                                  edges,
                                              'shield_tiles': # number of shields in city
                                                  0
                                              }
            # Add shield count
            shield_count = self.Shields_on_tile(tile)
            possessions[material][pos_idx]['shield_tiles'] = shield_count
            
            # Add cathedral support if that expansion is active
            if r'Inns && Cathedrals' in self.Carcassonne.expansions:
                possessions[material][pos_idx]['cathedral'] = False
        elif material == 'monastery':
            possessions[material][pos_idx] = {'open': # can this still be used to append/merge?
                                                  True,
                                              'tile': # tile and material index of monastery
                                                  (tile, mat_idx),
                                              'player_strength': # meeple strength per player
                                                  {player: 
                                                   {meeple_type:0 for meeple_type in self.Carcassonne.meeples.keys()}
                                                   for player in self.Connections()},
                                              'surrounding_tiles': # number of surrounding tiles
                                                  1 # tile itself makes it 1 instead of 0
                                              }
            # Calculate surrounding tiles
            for row_n, col_n in [(-1, -1), (-1, 0), (-1, 1), (0, -1), (0, 1), (1, -1), (1, 0), (1, 1)]:
                neighbour_tile = self.Carcassonne.board_tiles[row + row_n][col + col_n]
                if len(neighbour_tile.material_data) > 0:
                    possessions[material][pos_idx]['surrounding_tiles'] += 1
    
    def _Join_possessions(self, neighbours, edges, material, mat_idx, row, col):
        # Join two possessions together into one big possession
        possessions = self.Carcassonne.possessions
        tile = self.Carcassonne.board_tiles[row][col]
        
        # New reference
        pos_merged_idx = len(possessions[material])
        tile.update_possessions(material, mat_idx, pos_merged_idx) # update tile reference
        pos_merged = possessions[material][pos_merged_idx] = {'open': True}
        
        # Get info from neighbours
        pos_neighs = dict()
        for idx, neighbour in enumerate(neighbours):
            # Get neighbour possession
            tile_n, mat_idx_n = neighbour
            pos_idx = tile_n.possessions[material][mat_idx_n]
            pos_neighs[idx] = possessions[material][pos_idx]
            
            # Close neighbour possession
            pos_neighs[idx]['open'] = False
            
            # Update neighbour reference
            tile_n.update_possessions(material, mat_idx_n, pos_merged_idx)
        
        # Make merged possession
        for attribute in pos_neighs[0].keys():
            if attribute == 'open':
                pass # ignore open attribute
            
            elif attribute == 'player_strength':
            # player strength (weird dictionary)
                pos_merged['player_strength'] = {player: 
                                         {meeple_type:0 for meeple_type in self.Carcassonne.meeples.keys()}
                                         for player in self.Connections()}
                for pos_n in pos_neighs.values():
                    for player in self.Connections():
                        for meeple_type in self.Carcassonne.meeples.keys():
                            pos_merged['player_strength'][player][meeple_type] += pos_n['player_strength'][player][meeple_type]
                            
            elif attribute in ['tiles']:
            # list
                pos_merged[attribute] = set()
                for pos_n in pos_neighs.values():
                    pos_merged[attribute] |= set(pos_n[attribute])
                pos_merged[attribute] = list(pos_merged[attribute])
                
            elif attribute in ['open_edges', 'finished_cities', 'shield_tiles']:
            # integer
                pos_merged[attribute] = 0
                for pos_n in pos_neighs.values():
                    pos_merged[attribute] += pos_n[attribute]
                    # if attribute == 'open_edges':
                    #     pos_merged[attribute] -= 2 # tiles touch so each touch is -2 open edges
                    # COMMENT: this is fixed in self._Append_possession
                    
            elif attribute in ['inn', 'cathedral']:
            # boolean
                pos_merged[attribute] = False
                for pos_n in pos_neighs.values():
                    pos_merged[attribute] = pos_merged[attribute] or pos_n[attribute]
        
        # Append placed tile to merged possession
        self._Append_possession(pos_merged, len(neighbours), edges, material, mat_idx, row, col)
    
    def _Append_possession(self, pos_n, n_neighbours, edges, material, mat_idx, row, col):
        # Append tile to an existing possession
        tile = self.Carcassonne.board_tiles[row][col]
        
        # Append tile to possession
        if 'tiles' in pos_n.keys():
            pos_n['tiles'] += [(tile, mat_idx)]
        
        # Update open edges
        if 'open_edges' in pos_n.keys():
            pos_n['open_edges'] += edges-(2*n_neighbours)
            # Close possession if open_edges == 0
            if pos_n['open_edges'] == 0:
                self.Possession_finished(pos_n, material)
        
        # Update special tiles
        if 'shield_tiles' in pos_n.keys():
            shield_count = self.Shields_on_tile(tile)
            pos_n['shield_tiles'] += shield_count
        if 'inn' in pos_n.keys() and r'Inns && Cathedrals' in self.Carcassonne.expansions:
            inn_bool = self.Inn_on_tile(tile)
            pos_n['inn'] = pos_n['inn'] or inn_bool
        if 'cathedral' in pos_n.keys() and r'Inns && Cathedrals' in self.Carcassonne.expansions:
            cathedral_bool = self.Cathedral_on_tile(tile)
            pos_n['cathedral'] = pos_n['cathedral'] or cathedral_bool
        
        # Update surrounding tiles
        if 'surrounding_tiles' in pos_n.keys():
            pos_n['surrounding_tiles'] += 1
            if pos_n['surrounding_tiles'] == 9:
                self.Possession_finished(pos_n, material)
            
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
        
    def Possession_finished(self, pos_n, material):
        # Wait for animation before enabling end turn button
        self.end_turn = False
        
        # Close possession
        pos_n['open'] = False
        
        # Decide on winner
        winner = (list(), 0)
        for player in self.Connections():
            strength = 0
            meeples = pos_n['player_strength'][player]
            for meeple_type in meeples:
                if meeple_type == 'standard':
                    strength += 1*meeples[meeple_type]
                elif meeple_type == 'big':
                    strength += 2*meeples[meeple_type]
                elif meeple_type == 'abbot':
                    strength += 1*meeples[meeple_type]
                else:
                    raise Exception(f'Unknown meeple type {meeple_type}.')
            if strength > winner[1]:
                winner = ([player], strength)
            elif strength == winner[1] and strength > 0:
                winners = winner[0] + [player]
                winner = (winners, strength)
        
        if winner[0] != list(): # the possession was claimed by someone
            # Calculate points
            if material == 'grass':
                # Can only happen at the end of the game
                # FIXME: calculate the number of finished cities
                pass
            elif material == 'road':
                points = len(pos_n['tiles'])
                if 'inn' in pos_n.keys() and r'Inns && Cathedrals' in self.Carcassonne.expansions:
                    if pos_n['inn'] == True:
                        if pos_n['open_edges'] == 0:
                            points *= 2
                        else:
                            points = 0
                        
            elif material == 'city':
                # FIXME: add a function to increase finished_cities of surrounding fields
                points = 2*len(pos_n['tiles'])
                points += 2*pos_n['shield_tiles']
                if 'cathedral' in pos_n.keys() and r'Inns && Cathedrals' in self.Carcassonne.expansions:
                    if pos_n['cathedral'] == True:
                        if pos_n['open_edges'] == 0:
                            points *= 1.5
                        else:
                            points = 0
                        
            elif material == 'monastery':
                points = pos_n['surrounding_tiles']
                
            else:
                raise Exception(f'Unknown possession with material {material}.')
                
            # Play animation
            self.Possession_finished_anim(pos_n, winner[0], points, material)
        else:
            # Enable end turn button
            self.game_vis.button_end_turn.setEnabled(True)
            self.game_vis._Meeples_enable(True)
        
    def Possession_finished_anim(self, pos_n, winners, points, material):
        if True:
            # Animate finishing possession and giving points
            def anim_finished():
                # End state of points
                for winner_player in winners:
                    points_after = self.points_after[winner_player]
                    points_label.setText(f'{points_after}')
                    
                # Give back meeples
                self.Give_back_meeples(winners, pos_n, material)
                
                # Enable end turn button
                self.game_vis.button_end_turn.setEnabled(True)
                self.game_vis._Meeples_enable(True)
                    
            # Intermediate state of points
            self.points_after = dict()
            for winner_player in winners:
                # Get current points
                points_label = self.game_vis.players_points[winner_player]
                points_before = int(points_label.text())
                # Intermediate label
                points_label.setText(f'{points_before} + {int(points)}')
                # End points calculation
                points_after = self.points_after[winner_player] = int(points_before + points)
                # Database
                if winner_player == self.Carcassonne.username: # do this only once per player
                    self.Carcassonne.Refs(f'players/{winner_player}/points').set(points_after)
            
            # Make animation for blinking possession
            self.Carcassonne.game_vis.button_end_turn.setEnabled(False) # Disable end turn button
            self.finished_anim.clear()
            for tile in pos_n['tiles']:
                if type(tile[0]) == QtE.Tile:
                # single entry, so tuple
                    animation = Animations.Animation(tile[0])
                else:
                # multiple entries, so list of tuples
                    animation = Animations.Animation(tile[0][0])
                animation.add_blinking(1, 0.6, 1000, 0)
                self.finished_anim.add(animation)
            self.finished_anim.finished.disconnect()
            self.finished_anim.finished.connect(anim_finished)
            self.finished_anim.start()
        # else:
        #     # FIXME: obsolete (if everything goes well)
        #     for winner_player in winners: # FIXME: new
        #         # points_label = self.game_vis.players_points[winner]
        #         points_label = self.game_vis.players_points[winner_player]
        #         points_before = int(points_label.text())
        #         points_after = int(points_before + points)
        #         points_label.setText(f'{points_after}')
        #         # self.Carcassonne.Refs(f'players/{winner}/points').set(points_after)
        #         self.Carcassonne.Refs(f'players/{winner_player}/points').set(points_after)
                
        #     self.Give_back_meeples(winners, pos_n, material)
    
    def Give_back_meeples(self, winners, pos_n, material):
        # Find meeples that are on the possession
        # for tile, mat_idx in pos_n['tiles']:
        for tile, mat_idx in pos_n['tiles']:
        # Search each tile of the possession
            for winner in winners:
            # Consider all possible winners
                for meeple in tile.meeples[winner]:
                # Find all the winner's meeples that are on the tile
                    if meeple[:2] == (material, mat_idx):
                    # Only give back meeples of finished possession
                        tile.reset_image() # FIXME: this currently deletes all meeples from tile
                        if self.Carcassonne.username == winner:
                            meeple_type = meeple[2]
                            # Give back first unavailable meeple of winner
                            for meeple_button in self.Carcassonne.meeples[meeple_type]:
                                if meeple_button.available == False:
                                    meeple_button.make_available()
                                    break