tiles = dict()

#%% 1 base game
tiles[1] = dict()
tiles[1]['A'] = {'grass': [[1, 1, 1, 1, 1, 1, 1],
                        [1, 1, 1, 1, 1, 1, 1],
                        [1, 1, 1, 1, 1, 1, 1],
                        [0, 0, 0, 0, 0, 0, 0],
                        [2, 2, 2, 2, 2, 2, 2],
                        [2, 2, 2, 2, 2, 2, 2],
                        [2, 2, 2, 2, 2, 2, 2]],
              
              'road':  [[0, 0, 0, 0, 0, 0, 0],
                        [0, 0, 0, 0, 0, 0, 0],
                        [0, 0, 0, 0, 0, 0, 0],
                        [1, 1, 1, 1, 1, 1, 1],
                        [0, 0, 0, 0, 0, 0, 0],
                        [0, 0, 0, 0, 0, 0, 0],
                        [0, 0, 0, 0, 0, 0, 0]],
             }
tiles[1]['B'] = {'grass': [[1, 1, 1, 1, 1, 1, 1],
                        [1, 1, 1, 1, 1, 1, 1],
                        [1, 1, 1, 1, 1, 1, 1],
                        [0, 0, 0, 1, 1, 1, 1],
                        [2, 2, 0, 0, 1, 1, 1],
                        [2, 2, 2, 0, 1, 1, 1],
                        [2, 2, 2, 0, 1, 1, 1]],
              
              'road':  [[0, 0, 0, 0, 0, 0, 0],
                        [0, 0, 0, 0, 0, 0, 0],
                        [0, 0, 0, 0, 0, 0, 0],
                        [1, 1, 1, 0, 0, 0, 0],
                        [0, 0, 1, 1, 0, 0, 0],
                        [0, 0, 0, 1, 0, 0, 0],
                        [0, 0, 0, 1, 0, 0, 0]],
             }
tiles[1]['C'] = {'grass': [[1, 1, 1, 1, 1, 1, 1],
                        [1, 1, 1, 1, 1, 1, 1],
                        [1, 1, 1, 1, 1, 1, 1],
                        [0, 0, 0, 0, 0, 0, 0],
                        [2, 2, 2, 0, 3, 3, 3],
                        [2, 2, 2, 0, 3, 3, 3],
                        [2, 2, 2, 0, 3, 3, 3]],
              
              'road':  [[0, 0, 0, 0, 0, 0, 0],
                        [0, 0, 0, 0, 0, 0, 0],
                        [0, 0, 0, 0, 0, 0, 0],
                        [1, 1, 1, 0, 2, 2, 2],
                        [0, 0, 0, 3, 0, 0, 0],
                        [0, 0, 0, 3, 0, 0, 0],
                        [0, 0, 0, 3, 0, 0, 0]],
             }
tiles[1]['D'] = {'grass': [[1, 1, 1, 0, 4, 4, 4],
                        [1, 1, 1, 0, 4, 4, 4],
                        [1, 1, 1, 0, 4, 4, 4],
                        [0, 0, 0, 0, 0, 0, 0],
                        [2, 2, 2, 0, 3, 3, 3],
                        [2, 2, 2, 0, 3, 3, 3],
                        [2, 2, 2, 0, 3, 3, 3]],
              
              'road':  [[0, 0, 0, 4, 0, 0, 0],
                        [0, 0, 0, 4, 0, 0, 0],
                        [0, 0, 0, 4, 0, 0, 0],
                        [1, 1, 1, 0, 2, 2, 2],
                        [0, 0, 0, 3, 0, 0, 0],
                        [0, 0, 0, 3, 0, 0, 0],
                        [0, 0, 0, 3, 0, 0, 0]],
             }
tiles[1]['E'] = {'grass': [[0, 0, 0, 0, 0, 0, 0],
                        [1, 1, 0, 0, 0, 1, 1],
                        [1, 1, 1, 1, 1, 1, 1],
                        [0, 0, 0, 0, 0, 0, 0],
                        [2, 2, 2, 0, 3, 3, 3],
                        [2, 2, 2, 0, 3, 3, 3],
                        [2, 2, 2, 0, 3, 3, 3]],
              
              'road':  [[0, 0, 0, 0, 0, 0, 0],
                        [0, 0, 0, 0, 0, 0, 0],
                        [0, 0, 0, 0, 0, 0, 0],
                        [1, 1, 1, 0, 2, 2, 2],
                        [0, 0, 0, 3, 0, 0, 0],
                        [0, 0, 0, 3, 0, 0, 0],
                        [0, 0, 0, 3, 0, 0, 0]],
              
              'city':  [[0, 1, 1, 1, 1, 1, 0],
                        [0, 0, 1, 1, 1, 0, 0],
                        [0, 0, 0, 0, 0, 0, 0],
                        [0, 0, 0, 0, 0, 0, 0],
                        [0, 0, 0, 0, 0, 0, 0],
                        [0, 0, 0, 0, 0, 0, 0],
                        [0, 0, 0, 0, 0, 0, 0]],
             }
tiles[1]['F'] = {'grass': [[0, 0, 0, 0, 0, 0, 0],
                        [1, 1, 0, 0, 0, 1, 1],
                        [1, 1, 1, 1, 1, 1, 1],
                        [1, 1, 1, 1, 0, 0, 0],
                        [1, 1, 1, 0, 0, 2, 2],
                        [1, 1, 1, 0, 2, 2, 2],
                        [1, 1, 1, 0, 2, 2, 2]],
              
              'road':  [[0, 0, 0, 0, 0, 0, 0],
                        [0, 0, 0, 0, 0, 0, 0],
                        [0, 0, 0, 0, 0, 0, 0],
                        [0, 0, 0, 0, 1, 1, 1],
                        [0, 0, 0, 1, 1, 0, 0],
                        [0, 0, 0, 1, 0, 0, 0],
                        [0, 0, 0, 1, 0, 0, 0]],
              
              'city':  [[0, 1, 1, 1, 1, 1, 0],
                        [0, 0, 1, 1, 1, 0, 0],
                        [0, 0, 0, 0, 0, 0, 0],
                        [0, 0, 0, 0, 0, 0, 0],
                        [0, 0, 0, 0, 0, 0, 0],
                        [0, 0, 0, 0, 0, 0, 0],
                        [0, 0, 0, 0, 0, 0, 0]],
             }
tiles[1]['G'] = {'grass': [[0, 0, 0, 0, 0, 0, 0],
                        [1, 1, 0, 0, 0, 1, 1],
                        [1, 1, 1, 1, 1, 1, 1],
                        [0, 0, 0, 1, 1, 1, 1],
                        [2, 2, 0, 0, 1, 1, 1],
                        [2, 2, 2, 0, 1, 1, 1],
                        [2, 2, 2, 0, 1, 1, 1]],
              
              'road':  [[0, 0, 0, 0, 0, 0, 0],
                        [0, 0, 0, 0, 0, 0, 0],
                        [0, 0, 0, 0, 0, 0, 0],
                        [1, 1, 1, 0, 0, 0, 0],
                        [0, 0, 1, 1, 0, 0, 0],
                        [0, 0, 0, 1, 0, 0, 0],
                        [0, 0, 0, 1, 0, 0, 0]],
              
              'city':  [[0, 1, 1, 1, 1, 1, 0],
                        [0, 0, 1, 1, 1, 0, 0],
                        [0, 0, 0, 0, 0, 0, 0],
                        [0, 0, 0, 0, 0, 0, 0],
                        [0, 0, 0, 0, 0, 0, 0],
                        [0, 0, 0, 0, 0, 0, 0],
                        [0, 0, 0, 0, 0, 0, 0]],
             }
tiles[1]['H'] = {'grass': [[0, 0, 0, 0, 0, 0, 0],
                        [1, 1, 0, 0, 0, 1, 1],
                        [1, 1, 1, 1, 1, 1, 1],
                        [0, 0, 0, 0, 0, 0, 0],
                        [2, 2, 2, 2, 2, 2, 2],
                        [2, 2, 2, 2, 2, 2, 2],
                        [2, 2, 2, 2, 2, 2, 2]],
              
              'road':  [[0, 0, 0, 0, 0, 0, 0],
                        [0, 0, 0, 0, 0, 0, 0],
                        [0, 0, 0, 0, 0, 0, 0],
                        [1, 1, 1, 1, 1, 1, 1],
                        [0, 0, 0, 0, 0, 0, 0],
                        [0, 0, 0, 0, 0, 0, 0],
                        [0, 0, 0, 0, 0, 0, 0]],
              
              'city':  [[0, 1, 1, 1, 1, 1, 0],
                        [0, 0, 1, 1, 1, 0, 0],
                        [0, 0, 0, 0, 0, 0, 0],
                        [0, 0, 0, 0, 0, 0, 0],
                        [0, 0, 0, 0, 0, 0, 0],
                        [0, 0, 0, 0, 0, 0, 0],
                        [0, 0, 0, 0, 0, 0, 0]],
             }
tiles[1]['I'] = {'grass': [[0, 0, 0, 0, 0, 0, 0],
                        [1, 1, 0, 0, 0, 1, 1],
                        [1, 1, 1, 1, 1, 1, 1],
                        [1, 1, 1, 1, 1, 1, 1],
                        [1, 1, 1, 1, 1, 1, 1],
                        [1, 1, 1, 1, 1, 1, 1],
                        [1, 1, 1, 1, 1, 1, 1]],
              
              'city':  [[0, 1, 1, 1, 1, 1, 0],
                        [0, 0, 1, 1, 1, 0, 0],
                        [0, 0, 0, 0, 0, 0, 0],
                        [0, 0, 0, 0, 0, 0, 0],
                        [0, 0, 0, 0, 0, 0, 0],
                        [0, 0, 0, 0, 0, 0, 0],
                        [0, 0, 0, 0, 0, 0, 0]],
             }
tiles[1]['J'] = {'grass': [[1, 1, 1, 1, 1, 1, 1],
                        [1, 1, 1, 1, 1, 1, 1],
                        [1, 1, 1, 1, 1, 1, 1],
                        [1, 1, 1, 0, 1, 1, 1],
                        [1, 1, 1, 1, 1, 1, 1],
                        [1, 1, 1, 1, 1, 1, 1],
                        [1, 1, 1, 1, 1, 1, 1]],
              
              'monastery': [[0, 0, 0, 0, 0, 0, 0],
                            [0, 0, 0, 0, 0, 0, 0],
                            [0, 0, 0, 0, 0, 0, 0],
                            [0, 0, 0, 1, 0, 0, 0],
                            [0, 0, 0, 0, 0, 0, 0],
                            [0, 0, 0, 0, 0, 0, 0],
                            [0, 0, 0, 0, 0, 0, 0]],
             }
tiles[1]['K'] = {'grass': [[1, 1, 1, 1, 1, 1, 1],
                        [1, 1, 1, 1, 1, 1, 1],
                        [1, 1, 1, 1, 1, 1, 1],
                        [1, 1, 1, 0, 1, 1, 1],
                        [1, 1, 1, 0, 1, 1, 1],
                        [1, 1, 1, 0, 1, 1, 1],
                        [1, 1, 1, 0, 1, 1, 1]],
              
              'road':  [[0, 0, 0, 0, 0, 0, 0],
                        [0, 0, 0, 0, 0, 0, 0],
                        [0, 0, 0, 0, 0, 0, 0],
                        [0, 0, 0, 0, 0, 0, 0],
                        [0, 0, 0, 1, 0, 0, 0],
                        [0, 0, 0, 1, 0, 0, 0],
                        [0, 0, 0, 1, 0, 0, 0]],
              
              'monastery': [[0, 0, 0, 0, 0, 0, 0],
                            [0, 0, 0, 0, 0, 0, 0],
                            [0, 0, 0, 0, 0, 0, 0],
                            [0, 0, 0, 1, 0, 0, 0],
                            [0, 0, 0, 0, 0, 0, 0],
                            [0, 0, 0, 0, 0, 0, 0],
                            [0, 0, 0, 0, 0, 0, 0]],
             }
tiles[1]['L'] = {'grass': [[0, 1, 1, 1, 1, 1, 0],
                        [0, 0, 1, 1, 1, 0, 0],
                        [0, 0, 0, 0, 0, 0, 0],
                        [0, 0, 0, 0, 0, 0, 0],
                        [0, 0, 0, 0, 0, 0, 0],
                        [0, 0, 2, 2, 2, 0, 0],
                        [0, 2, 2, 2, 2, 2, 0]],
              
              'city':  [[0, 0, 0, 0, 0, 0, 0],
                        [1, 1, 0, 0, 0, 1, 1],
                        [1, 1, 1, 1, 1, 1, 1],
                        [1, 1, 1, 1, 1, 1, 1],
                        [1, 1, 1, 1, 1, 1, 1],
                        [1, 1, 0, 0, 0, 1, 1],
                        [0, 0, 0, 0, 0, 0, 0]],
             }
tiles[1]['M'] = tiles[1]['L']
tiles[1]['N'] = {'grass': [[0, 0, 0, 0, 0, 0, 0],
                        [1, 1, 0, 0, 0, 0, 0],
                        [1, 1, 1, 1, 0, 0, 0],
                        [1, 1, 1, 1, 1, 0, 0],
                        [1, 1, 1, 1, 1, 0, 0],
                        [1, 1, 1, 1, 1, 1, 0],
                        [1, 1, 1, 1, 1, 1, 0]],
              
              'city':  [[0, 1, 1, 1, 1, 1, 0],
                        [0, 0, 1, 1, 1, 1, 1],
                        [0, 0, 0, 0, 1, 1, 1],
                        [0, 0, 0, 0, 0, 1, 1],
                        [0, 0, 0, 0, 0, 1, 1],
                        [0, 0, 0, 0, 0, 0, 1],
                        [0, 0, 0, 0, 0, 0, 0]],
             }
tiles[1]['O'] = tiles[1]['N']
tiles[1]['P'] = {'grass': [[0, 0, 0, 0, 0, 0, 0],
                        [1, 1, 0, 0, 0, 0, 0],
                        [1, 1, 1, 1, 0, 0, 0],
                        [0, 0, 0, 1, 1, 0, 0],
                        [2, 2, 0, 0, 1, 0, 0],
                        [2, 2, 2, 0, 1, 1, 0],
                        [2, 2, 2, 0, 1, 1, 0]],
              
              'road':  [[0, 0, 0, 0, 0, 0, 0],
                        [0, 0, 0, 0, 0, 0, 0],
                        [0, 0, 0, 0, 0, 0, 0],
                        [1, 1, 1, 0, 0, 0, 0],
                        [0, 0, 1, 1, 0, 0, 0],
                        [0, 0, 0, 1, 0, 0, 0],
                        [0, 0, 0, 1, 0, 0, 0]],
              
              'city':  [[0, 1, 1, 1, 1, 1, 0],
                        [0, 0, 1, 1, 1, 1, 1],
                        [0, 0, 0, 0, 1, 1, 1],
                        [0, 0, 0, 0, 0, 1, 1],
                        [0, 0, 0, 0, 0, 1, 1],
                        [0, 0, 0, 0, 0, 0, 1],
                        [0, 0, 0, 0, 0, 0, 0]],
             }
tiles[1]['Q'] = tiles[1]['P']
tiles[1]['R'] = {'grass': [[0, 0, 0, 0, 0, 0, 0],
                        [1, 1, 0, 0, 0, 1, 1],
                        [1, 1, 1, 1, 1, 1, 1],
                        [1, 1, 1, 1, 1, 1, 1],
                        [1, 1, 1, 1, 1, 1, 1],
                        [1, 1, 0, 0, 0, 1, 1],
                        [0, 0, 0, 0, 0, 0, 0]],
              
              'city':  [[0, 1, 1, 1, 1, 1, 0],
                        [0, 0, 1, 1, 1, 0, 0],
                        [0, 0, 0, 0, 0, 0, 0],
                        [0, 0, 0, 0, 0, 0, 0],
                        [0, 0, 0, 0, 0, 0, 0],
                        [0, 0, 2, 2, 2, 0, 0],
                        [0, 2, 2, 2, 2, 2, 0]],
             }
tiles[1]['S'] = {'grass': [[0, 0, 0, 0, 0, 0, 0],
                        [1, 1, 0, 0, 0, 1, 0],
                        [1, 1, 1, 1, 1, 0, 0],
                        [1, 1, 1, 1, 1, 0, 0],
                        [1, 1, 1, 1, 1, 0, 0],
                        [1, 1, 1, 1, 1, 1, 0],
                        [1, 1, 1, 1, 1, 1, 0]],
              
              'city':  [[0, 1, 1, 1, 1, 1, 0],
                        [0, 0, 1, 1, 1, 0, 2],
                        [0, 0, 0, 0, 0, 2, 2],
                        [0, 0, 0, 0, 0, 2, 2],
                        [0, 0, 0, 0, 0, 2, 2],
                        [0, 0, 0, 0, 0, 0, 2],
                        [0, 0, 0, 0, 0, 0, 0]],
             }
tiles[1]['T'] = {'grass': [[0, 0, 0, 0, 0, 0, 0],
                        [0, 0, 0, 0, 0, 0, 0],
                        [0, 0, 0, 0, 0, 0, 0],
                        [0, 0, 0, 0, 0, 0, 0],
                        [0, 0, 0, 0, 0, 0, 0],
                        [0, 0, 1, 1, 1, 0, 0],
                        [0, 1, 1, 1, 1, 1, 0]],
              
              'city':  [[1, 1, 1, 1, 1, 1, 1],
                        [1, 1, 1, 1, 1, 1, 1],
                        [1, 1, 1, 1, 1, 1, 1],
                        [1, 1, 1, 1, 1, 1, 1],
                        [1, 1, 1, 1, 1, 1, 1],
                        [1, 1, 0, 0, 0, 1, 1],
                        [0, 0, 0, 0, 0, 0, 0]],
             }
tiles[1]['U'] = tiles[1]['T']
tiles[1]['V'] = {'grass': [[0, 0, 0, 0, 0, 0, 0],
                        [0, 0, 0, 0, 0, 0, 0],
                        [0, 0, 0, 0, 0, 0, 0],
                        [0, 0, 0, 0, 0, 0, 0],
                        [0, 0, 0, 0, 0, 0, 0],
                        [0, 0, 1, 0, 1, 0, 0],
                        [0, 1, 1, 0, 1, 1, 0]],
              
              'road':  [[0, 0, 0, 0, 0, 0, 0],
                        [0, 0, 0, 0, 0, 0, 0],
                        [0, 0, 0, 0, 0, 0, 0],
                        [0, 0, 0, 0, 0, 0, 0],
                        [0, 0, 0, 0, 0, 0, 0],
                        [0, 0, 0, 1, 0, 0, 0],
                        [0, 0, 0, 1, 0, 0, 0]],
              
              'city':  [[1, 1, 1, 1, 1, 1, 1],
                        [1, 1, 1, 1, 1, 1, 1],
                        [1, 1, 1, 1, 1, 1, 1],
                        [1, 1, 1, 1, 1, 1, 1],
                        [1, 1, 1, 1, 1, 1, 1],
                        [1, 1, 0, 0, 0, 1, 1],
                        [0, 0, 0, 0, 0, 0, 0]],
             }
tiles[1]['W'] = tiles[1]['V']
tiles[1]['X'] = {'city':  [[1, 1, 1, 1, 1, 1, 1],
                        [1, 1, 1, 1, 1, 1, 1],
                        [1, 1, 1, 1, 1, 1, 1],
                        [1, 1, 1, 1, 1, 1, 1],
                        [1, 1, 1, 1, 1, 1, 1],
                        [1, 1, 1, 1, 1, 1, 1],
                        [1, 1, 1, 1, 1, 1, 1]],
             }

# grass     = list
# road      = list
# city      = list
# monastery = list
# water     = list # The River
# cathedral = list # Inns & Cathedrals
# inns      = list # Inns & Cathedrals
# garden    = list # The Abbot