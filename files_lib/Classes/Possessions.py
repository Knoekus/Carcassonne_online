import PyQt6.QtGui     as QtG
import PyQt6.QtWidgets as QtW
import PyQt6.QtCore    as QtC
import PyQt6_Extra     as QtE

import Classes.Animations as Animations

class Possessions():
    def __init__(self, game):
        self.game = game
        
    def Update_possessions(self, tile_data, row, col):
        def get_neighbours(material, data, idx):
            # Get neighbouring tiles and number of edges the material patch covers
            edges = 0
            neighbours = []
            if idx in data[0][1:-1]: # north
                edges += 1
                tile = self.game.board_tiles[row-1][col]
                if len(tile.material_data) > 0: # tile is not empty
                    col_idx = data[0][1:-1].index(idx)+1
                    mat_idx_n = tile.material_data[material][-1][col_idx]
                    neighbours += [(tile, mat_idx_n)]
            if idx in [data[x][-1] for x in range(len(data))][1:-1]: # east
                edges += 1
                tile = self.game.board_tiles[row][col+1]
                if len(tile.material_data) > 0: # tile is not empty
                    row_idx = [data[x][-1] for x in range(len(data))][1:-1].index(idx)+1
                    mat_idx_n = tile.material_data[material][row_idx][0]
                    neighbours += [(tile, mat_idx_n)]
            if idx in data[-1][1:-1]: # south
                edges += 1
                tile = self.game.board_tiles[row+1][col]
                if len(tile.material_data) > 0: # tile is not empty
                    col_idx = data[-1][1:-1].index(idx)+1
                    mat_idx_n = tile.material_data[material][0][col_idx]
                    neighbours += [(tile, mat_idx_n)]
            if idx in [data[x][0] for x in range(len(data))][1:-1]: # west
                edges += 1
                tile = self.game.board_tiles[row][col-1]
                if len(tile.material_data) > 0: # tile is not empty
                    row_idx = [data[x][0] for x in range(len(data))][1:-1].index(idx)+1
                    mat_idx_n = tile.material_data[material][row_idx][-1]
                    neighbours += [(tile, mat_idx_n)]
            return neighbours, edges
        
        # Update directly connected possessions
        for material in tile_data.keys():
        # For all material of the placed tile
            mat_data = tile_data[material]
            for mat_idx in range(1, max(max(mat_data))+1):
            # Check each patch of material in the tile
                neighbours, edges = get_neighbours(material, mat_data, mat_idx)
                if len(neighbours) == 0:
                # The material patch does not touch any neighbours
                    self._New_possession(edges, material, mat_idx, row, col)
                    
                elif len(neighbours) == 1:
                # There is a neighbouring tile, don't create new possession but append to existing one
                    tile_n, mat_idx_n = neighbours[0]
                    possessions = self.game.possessions
                    pos_idx = tile_n.possessions[material][mat_idx_n]
                    self.game.board_tiles[row][col].update_possessions(material, mat_idx, pos_idx) # update tile reference
                    pos_n = possessions[material][pos_idx]
                    self._Append_possession(pos_n, edges, material, mat_idx, row, col)
                    
                elif len(neighbours) > 1:
                # There are multiple neighbouring tiles, join them together
                    self._Join_possessions(neighbours, edges, material, mat_idx, row, col)
        
        # Update indirectly connected possessions
        for row_n, col_n in [(-1, -1), (-1, 0), (-1, 1), (0, -1), (0, 1), (1, -1), (1, 0), (1, 1)]:
            tile_n = self.game.board_tiles[row + row_n][col + col_n]
            if len(tile_n.material_data) > 0:
                if 'monastery' in tile_n.material_data.keys():
                    pos_idx = tile_n.possessions['monastery'][1]
                    pos_n = self.game.possessions['monastery'][pos_idx]
                    self._Append_possession(pos_n, edges, material, mat_idx, row, col)
                
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
                                              'tile': # tile and material index of monastery
                                                  (tile, mat_idx),
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
                    possessions[material][pos_idx]['surrounding_tiles'] += 1
    
    def _Join_possessions(self, neighbours, edges, material, mat_idx, row, col):
        # Join two possessions together into one big possession
        possessions = self.game.possessions
        tile = self.game.board_tiles[row][col]
        
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
                    
            elif attribute in ['open_edges', 'finished_cities', 'shield_tiles']:
            # integer
                pos_merged[attribute] = 0
                for pos_n in pos_neighs.values():
                    pos_merged[attribute] += pos_n[attribute]
                    if attribute == 'open_edges':
                        pos_merged[attribute] -= 2 # tiles touch so each touch is -2 open edges
                    
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
        
        # Append tile to possession
        if 'tiles' in pos_n.keys():
            pos_n['tiles'] += [(tile, mat_idx)]
        
        # Update open edges
        if 'open_edges' in pos_n.keys():
            pos_n['open_edges'] += edges-2
            # Close possession if open_edges == 0
            if pos_n['open_edges'] == 0:
                self.Possession_finished(pos_n, material)
        
        # Update special tiles
        if 'shield_tiles' in pos_n.keys():
            shield_count = self.Shields_on_tile(tile)
            pos_n['shield_tiles'] += shield_count
        if 'inn' in pos_n.keys() and r'Inns && Cathedrals' in self.game.expansions:
            inn_bool = self.Inn_on_tile(tile)
            pos_n['inn'] = pos_n['inn'] or inn_bool
        if 'cathedral' in pos_n.keys() and r'Inns && Cathedrals' in self.game.expansions:
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
        pos_n['open'] = False
        
        # Decide on winner
        winner = (None, 0)
        for player in self.game.connections:
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
                winner = (player, strength)
        
        # Calculate points
        if material == 'grass':
            # Can only happen at the end of the game
            pass
        elif material == 'road':
            points = len(pos_n['tiles'])
            if 'inn' in pos_n.keys() and r'Inns && Cathedrals' in self.game.expansions:
                if pos_n['open_edges'] == 0:
                    points *= 2
                else:
                    points = 0
                    
        elif material == 'city':
            points = 2*len(pos_n['tiles'])
            points += 2*pos_n['shield_tiles']
            if 'cathedral' in pos_n.keys() and r'Inns && Cathedrals' in self.game.expansions:
                if pos_n['open_edges'] == 0:
                    points *= 1.5
                else:
                    points = 0
                    
        elif material == 'monastery':
            points = pos_n['surrounding_tiles']
            
        else:
            raise Exception(f'Unknown possession with material {material}.')
            
        # Intermediate state of points
        points_label = self.game.players_points[winner[0]]
        points_before = int(points_label.text())
        points_label.setText(f'{points_before} + {int(points)}')
        
        # Animate finishing possession and giving points
        def anim_finished():
            points_after = int(points_before + points)
            points_label.setText(points_after)
            self.Refs(f'players/{winner[0]}/points').set(points_after)
        
        # FIXME: ====================
        # FIXME: animation won't play
        # FIXME: ====================
        animation_group = Animations.AnimationGroup_parallel()
        for tile in pos_n['tiles']:
            animation = Animations.Animation(tile[0])
            animation.add_blinking(1, 0.6, 1000, 0)
            animation_group.add(animation)
        animation_group.finished.connect(anim_finished)
        animation_group.start()
        print('ANIMATION STARTED')
        
        # Giving back meeples
        # ...