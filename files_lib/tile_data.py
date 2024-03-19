# Tiles currently modelled as 32x32 pixels, upscaled x10
# NOTE TO SELF
# FIXME: the corners of CITIES are now filled in instead of left blank.
# FIXME: if problems occur with possession merging or tile placement, check this.

# grass     = list
# road      = list
# city      = list
# monastery = list
# water     = list # The River
# cathedral = list # Inns & Cathedrals
# inns      = list # Inns & Cathedrals
# garden    = list # The Abbot

tiles = dict()
data_steps = 7

#%% Basic shapes
def make_row(pairs, num_rows:int=1):
    '''
    pairs : tuple (mat_idx, reps)
        Contains the mat_idx and number of repetitions to make a material data row.
    
    num_rows : int (default = 1)
        How many times should this row be repeated?'''
        
    # Check
    if type(pairs) == tuple:
        pairs = [pairs]
    elif type(pairs) != list:
        raise Exception('pairs must be of type list or tuple.')
    
    # Make row
    row = list()
    for mat_idx, reps in pairs:
        row += [mat_idx for x in range(reps)]
    
    # Return
    if num_rows == 1:
        return row
    else:
        return [row for x in range(num_rows)]
    
def add_moon(pos, mat_idx, data=None):
    data_new = [[0 for col in range(data_steps)] for row in range(data_steps)]
    moon = [mat_idx for x in range(data_steps)]
    if pos == 'N':
        data_new[0] = moon
    elif pos == 'E':
        for row in range(data_steps):
            data_new[row][-1] = mat_idx
    elif pos == 'S':
        data_new[-1] = moon
    elif pos == 'W':
        for row in range(data_steps):
            data_new[row][0] = mat_idx
    
    if data == None:
        return data_new
    else:
        # Combine data
        for row_idx in range(len(data)):
            data[row_idx] = [data[row_idx][x]+data_new[row_idx][x] for x in range(len(data))]
        return data

def add_triangle(pos, mat_idx, data=None):
    data_new = [[0 for col in range(data_steps)] for row in range(data_steps)]
    if pos == 'NE':
        data_new[0] = make_row([(mat_idx, 7)])
        data_new[1] = make_row([(0, 3), (mat_idx, 4)])
        data_new[2:4] = make_row([(0, 5), (mat_idx, 2)], 2)
        data_new[4:] = make_row([(0, 6), (mat_idx, 1)], 3)
    elif pos == 'SE':
        data_new[:3] = make_row([(0, 6), (mat_idx, 1)], 3)
        data_new[3:5] = make_row([(0, 5), (mat_idx, 2)], 2)
        data_new[5] = make_row([(0, 3), (mat_idx, 4)])
        data_new[6] = make_row([(mat_idx, 7)])
    elif pos == 'SW':
        data_new[:3] = make_row([(mat_idx, 1), (0, 6)], 3)
        data_new[3:5] = make_row([(mat_idx, 2), (0, 5)], 2)
        data_new[5] = make_row([(mat_idx, 4), (0, 3)])
        data_new[6] = make_row([(mat_idx, 7)])
    elif pos == 'NW':
        data_new[0] = make_row([(mat_idx, 7)])
        data_new[1] = make_row([(mat_idx, 4), (0, 3)])
        data_new[2:4] = make_row([(mat_idx, 2), (0, 5)], 2)
        data_new[4:] = make_row([(mat_idx, 1), (0, 6)], 3)
    
    if data == None:
        return data_new
    else:
        # Combine data
        for row_idx in range(len(data)):
            data[row_idx] = [data[row_idx][x]+data_new[row_idx][x] for x in range(len(data))]
        return data

def add_straight(pos, mat_idx, data=None):
    data_new = [[0 for col in range(data_steps)] for row in range(data_steps)]
    # Single positions
    if pos == 'N':
        data_new[:4] = make_row([(0, 3), (mat_idx, 1), (0, 3)], 3)
    elif pos == 'E':
        data_new[4] = make_row([(0, 4), (mat_idx, 3)])
    elif pos == 'S':
        data_new[5:] = make_row([(0, 3), (mat_idx, 1), (0, 3)], 3)
    elif pos == 'W':
        data_new[4] = make_row([(mat_idx, 3), (0, 4)])
    
    # Straights
    elif pos == 'WE' or pos == 'EW':
        data_new[4] = make_row([(mat_idx, 7)])
    elif pos == 'NS' or pos == 'SN':
        data_new = make_row([(0, 3), (mat_idx, 1), (0, 3)], 7)
    
    if data == None:
        return data_new
    else:
        # Combine data
        for row_idx in range(len(data)):
            data[row_idx] = [data[row_idx][x]+data_new[row_idx][x] for x in range(len(data))]
        return data

def add_corner(pos, mat_idx, data=None):
    data_new = [[0 for col in range(data_steps)] for row in range(data_steps)]
    if pos == 'NE':
        data_new[:2] = make_row([(0, 3), (mat_idx, 1), (0, 3)], 2)
        data_new[2] = make_row([(0, 3), (mat_idx, 2), (0, 2)])
        data_new[3] = make_row([(0, 3), (mat_idx, 4)])
    elif pos == 'SE':
        data_new[3] = make_row([(0, 3), (mat_idx, 4)])
        data_new[4] = make_row([(0, 3), (mat_idx, 2), (0, 2)])
        data_new[5:] = make_row([(0, 3), (mat_idx, 1), (0, 3)], 2)
    elif pos == 'SW':
        data_new[3] = make_row([(mat_idx, 4), (0, 3)])
        data_new[4] = make_row([(0, 2), (mat_idx, 2), (0, 3)])
        data_new[5:] = make_row([(0, 3), (mat_idx, 1), (0, 3)], 2)
    elif pos == 'NW':
        data_new[:2] = make_row([(0, 3), (mat_idx, 1), (0, 3)], 2)
        data_new[2] = make_row([(0, 2), (mat_idx, 2), (0, 3)])
        data_new[3] = make_row([(mat_idx, 4), (0, 3)])
    
    if data == None:
        return data_new
    else:
        # Combine data
        for row_idx in range(len(data)):
            data[row_idx] = [data[row_idx][x]+data_new[row_idx][x] for x in range(len(data))]
        return data

def add_grass_corner(pos, mat_idx, data=None):
    data_new = [[0 for col in range(data_steps)] for row in range(data_steps)]
    if pos == 'NE':
        data_new[:2] = make_row([(0, 4), (mat_idx, 3)], 2)
        data_new[2] = make_row([(0, 5), (mat_idx, 2)])
    elif pos == 'SE':
        data_new[4] = make_row([(0, 5), (mat_idx, 2)])
        data_new[5:] = make_row([(0, 4), (mat_idx, 3)], 2)
    elif pos == 'SW':
        data_new[4] = make_row([(mat_idx, 2), (0, 5)])
        data_new[5:] = make_row([(mat_idx, 3), (0, 4)], 2)
    elif pos == 'NW':
        data_new[:2] = make_row([(mat_idx, 3), (0, 4)], 2)
        data_new[2] = make_row([(mat_idx, 2), (0, 5)])
    
    if data == None:
        return data_new
    else:
        # Combine data
        for row_idx in range(len(data)):
            data[row_idx] = [data[row_idx][x]+data_new[row_idx][x] for x in range(len(data))]
        return data

def add_grass_straight(pos, mat_idx, data=None):
    data_new = [[0 for col in range(data_steps)] for row in range(data_steps)]
    if pos == 'N':
        data_new[:3] = make_row([(mat_idx, 7)], 3)
    elif pos == 'E':
        data_new = make_row([(0, 4), (mat_idx, 3)], 7)
    elif pos == 'S':
        data_new[4:] = make_row([(mat_idx, 7)], 3)
    elif pos == 'W':
        data_new = make_row([(mat_idx, 3), (0, 4)], 7)
    
    if data == None:
        return data_new
    else:
        # Combine data
        for row_idx in range(len(data)):
            data[row_idx] = [data[row_idx][x]+data_new[row_idx][x] for x in range(len(data))]
        return data
    
def give_fill(mat_idx):
    data_new = [[mat_idx for col in range(data_steps)] for row in range(data_steps)]
    return data_new

def fill_remainder(mat_idx, datas, data):
    data_new = [[mat_idx for col in range(data_steps)] for row in range(data_steps)]
    for sub_data in datas:
        for y, row in enumerate(sub_data):
            for x, cell in enumerate(row):
                if cell != 0:
                    data_new[y][x] = 0
    
    if data == None:
        return data_new
    else:
        # Combine data
        for row_idx in range(len(data)):
            data[row_idx] = [data[row_idx][x]+data_new[row_idx][x] for x in range(len(data))]
        return data

def replace_idx(data, before, after):
    for y, row in enumerate(data):
        for x, cell in enumerate(row):
            if cell == before:
                data[y][x] = after
    return data

example_1P = dict()
example_1P['road'] = add_corner('SW', 1)
example_1P['city'] = add_triangle('NE', 1)
example_1P['grass'] = add_grass_corner('SW', 2)
example_1P['grass'] = fill_remainder(1, [example_1P['road'], example_1P['city'], example_1P['grass']], example_1P['grass'])

#%% 1 base game
tiles[1] = dict()
tiles[1]['A_m'] = {'grass': {1: (1, 1), 2: (5, 1)},
                   'road': {1: (3, 1)}}
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
tiles[1]['B_m'] = {'grass': {1: (1, 1), 2: (5, 1)},
                   'road': {1: (3, 1)}}
tiles[1]['B'] = {'grass': [[1, 1, 1, 1, 1, 1, 1],
                        [1, 1, 1, 1, 1, 1, 1],
                        [1, 1, 1, 1, 1, 1, 1],
                        [0, 0, 0, 0, 1, 1, 1],
                        [2, 2, 0, 0, 1, 1, 1],
                        [2, 2, 2, 0, 1, 1, 1],
                        [2, 2, 2, 0, 1, 1, 1]],
              
              'road':  [[0, 0, 0, 0, 0, 0, 0],
                        [0, 0, 0, 0, 0, 0, 0],
                        [0, 0, 0, 0, 0, 0, 0],
                        [1, 1, 1, 1, 0, 0, 0],
                        [0, 0, 1, 1, 0, 0, 0],
                        [0, 0, 0, 1, 0, 0, 0],
                        [0, 0, 0, 1, 0, 0, 0]],
             }
tiles[1]['C_m'] = {'grass': {1: (1, 1), 2: (5, 1), 3:(5, 5)},
                   'road': {1: (3, 1), 2: (3, 5), 3: (5, 3)}}
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
tiles[1]['D_m'] = {'grass': {1: (1, 1), 2: (5, 1), 3:(5, 5), 4: (1, 5)},
                   'road': {1: (3, 1), 2: (3, 5), 3: (5, 3), 4: (1, 3)}}
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
tiles[1]['E_m'] = {'grass': {1: (1, 1), 2: (5, 1), 3:(5, 5)},
                   'road': {1: (3, 1), 2: (3, 5), 3: (5, 3)},
                   'city': {1: (0, 3)}}
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
              
              'city':  [[1, 1, 1, 1, 1, 1, 1],
                        [0, 0, 1, 1, 1, 0, 0],
                        [0, 0, 0, 0, 0, 0, 0],
                        [0, 0, 0, 0, 0, 0, 0],
                        [0, 0, 0, 0, 0, 0, 0],
                        [0, 0, 0, 0, 0, 0, 0],
                        [0, 0, 0, 0, 0, 0, 0]],
             }
tiles[1]['F_m'] = {'grass': {1: (5, 1), 2:(5, 5)},
                   'road': {1: (5, 3)},
                   'city': {1: (0, 3)}}
tiles[1]['F'] = {'grass': [[0, 0, 0, 0, 0, 0, 0],
                        [1, 1, 0, 0, 0, 1, 1],
                        [1, 1, 1, 1, 1, 1, 1],
                        [1, 1, 1, 0, 0, 0, 0],
                        [1, 1, 1, 0, 0, 2, 2],
                        [1, 1, 1, 0, 2, 2, 2],
                        [1, 1, 1, 0, 2, 2, 2]],
              
              'road':  [[0, 0, 0, 0, 0, 0, 0],
                        [0, 0, 0, 0, 0, 0, 0],
                        [0, 0, 0, 0, 0, 0, 0],
                        [0, 0, 0, 1, 1, 1, 1],
                        [0, 0, 0, 1, 1, 0, 0],
                        [0, 0, 0, 1, 0, 0, 0],
                        [0, 0, 0, 1, 0, 0, 0]],
              
              'city':  [[1, 1, 1, 1, 1, 1, 1],
                        [0, 0, 1, 1, 1, 0, 0],
                        [0, 0, 0, 0, 0, 0, 0],
                        [0, 0, 0, 0, 0, 0, 0],
                        [0, 0, 0, 0, 0, 0, 0],
                        [0, 0, 0, 0, 0, 0, 0],
                        [0, 0, 0, 0, 0, 0, 0]],
             }
tiles[1]['G_m'] = {'grass': {1: (5, 5), 2:(5, 1)},
                   'road': {1: (5, 3)},
                   'city': {1: (0, 3)}}
tiles[1]['G'] = {'grass': [[0, 0, 0, 0, 0, 0, 0],
                        [1, 1, 0, 0, 0, 1, 1],
                        [1, 1, 1, 1, 1, 1, 1],
                        [0, 0, 0, 0, 1, 1, 1],
                        [2, 2, 0, 0, 1, 1, 1],
                        [2, 2, 2, 0, 1, 1, 1],
                        [2, 2, 2, 0, 1, 1, 1]],
              
              'road':  [[0, 0, 0, 0, 0, 0, 0],
                        [0, 0, 0, 0, 0, 0, 0],
                        [0, 0, 0, 0, 0, 0, 0],
                        [1, 1, 1, 1, 0, 0, 0],
                        [0, 0, 1, 1, 0, 0, 0],
                        [0, 0, 0, 1, 0, 0, 0],
                        [0, 0, 0, 1, 0, 0, 0]],
              
              'city':  [[1, 1, 1, 1, 1, 1, 1],
                        [0, 0, 1, 1, 1, 0, 0],
                        [0, 0, 0, 0, 0, 0, 0],
                        [0, 0, 0, 0, 0, 0, 0],
                        [0, 0, 0, 0, 0, 0, 0],
                        [0, 0, 0, 0, 0, 0, 0],
                        [0, 0, 0, 0, 0, 0, 0]],
             }
tiles[1]['H_m'] = {'grass': {1: (2, 1), 2:(2, 5)},
                   'road': {1: (3, 2)},
                   'city': {1: (0, 3)}}
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
              
              'city':  [[1, 1, 1, 1, 1, 1, 1],
                        [0, 0, 1, 1, 1, 0, 0],
                        [0, 0, 0, 0, 0, 0, 0],
                        [0, 0, 0, 0, 0, 0, 0],
                        [0, 0, 0, 0, 0, 0, 0],
                        [0, 0, 0, 0, 0, 0, 0],
                        [0, 0, 0, 0, 0, 0, 0]],
             }
tiles[1]['I_m'] = {'grass': {1: (5, 1)},
                   'city': {1: (0, 3)}}
tiles[1]['I'] = {'grass': [[0, 0, 0, 0, 0, 0, 0],
                        [1, 1, 0, 0, 0, 1, 1],
                        [1, 1, 1, 1, 1, 1, 1],
                        [1, 1, 1, 1, 1, 1, 1],
                        [1, 1, 1, 1, 1, 1, 1],
                        [1, 1, 1, 1, 1, 1, 1],
                        [1, 1, 1, 1, 1, 1, 1]],
              
              'city':  [[1, 1, 1, 1, 1, 1, 1],
                        [0, 0, 1, 1, 1, 0, 0],
                        [0, 0, 0, 0, 0, 0, 0],
                        [0, 0, 0, 0, 0, 0, 0],
                        [0, 0, 0, 0, 0, 0, 0],
                        [0, 0, 0, 0, 0, 0, 0],
                        [0, 0, 0, 0, 0, 0, 0]],
             }
tiles[1]['J_m'] = {'grass': {1: (5, 1)},
                   'monastery': {1: (3, 3)}}
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
tiles[1]['K_m'] = {'grass': {1: (1, 1)},
                   'road': {1: (5, 3)},
                   'monastery': {1: (3, 3)}}
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
tiles[1]['L_m'] = {'grass': {1: (0, 3), 2: (6, 3)},
                   'city': {1: (3, 1)}}
tiles[1]['L'] = {'grass': [[0, 1, 1, 1, 1, 1, 0],
                        [0, 0, 1, 1, 1, 0, 0],
                        [0, 0, 0, 0, 0, 0, 0],
                        [0, 0, 0, 0, 0, 0, 0],
                        [0, 0, 0, 0, 0, 0, 0],
                        [0, 0, 2, 2, 2, 0, 0],
                        [0, 2, 2, 2, 2, 2, 0]],
              
              'city':  [[1, 0, 0, 0, 0, 0, 1],
                        [1, 1, 0, 0, 0, 1, 1],
                        [1, 1, 1, 1, 1, 1, 1],
                        [1, 1, 1, 1, 1, 1, 1],
                        [1, 1, 1, 1, 1, 1, 1],
                        [1, 1, 0, 0, 0, 1, 1],
                        [1, 0, 0, 0, 0, 0, 1]],
             }
tiles[1]['M_m'] = tiles[1]['L_m']
tiles[1]['M'] = tiles[1]['L']
tiles[1]['N_m'] = {'grass': {1: (5, 1)},
                   'city': {1: (1, 5)}}
tiles[1]['N'] = {'grass': [[0, 0, 0, 0, 0, 0, 0],
                        [1, 1, 1, 0, 0, 0, 0],
                        [1, 1, 1, 1, 1, 0, 0],
                        [1, 1, 1, 1, 1, 0, 0],
                        [1, 1, 1, 1, 1, 1, 0],
                        [1, 1, 1, 1, 1, 1, 0],
                        [1, 1, 1, 1, 1, 1, 0]],
              
              'city':  [[1, 1, 1, 1, 1, 1, 1],
                        [0, 0, 0, 1, 1, 1, 1],
                        [0, 0, 0, 0, 0, 1, 1],
                        [0, 0, 0, 0, 0, 1, 1],
                        [0, 0, 0, 0, 0, 0, 1],
                        [0, 0, 0, 0, 0, 0, 1],
                        [0, 0, 0, 0, 0, 0, 1]],
             }
tiles[1]['O_m'] = tiles[1]['N_m']
tiles[1]['O'] = tiles[1]['N']
tiles[1]['P_m'] = {'grass': {1: (1, 1), 2: (5, 1)},
                   'road': {1: (5, 3)},
                   'city': {1: (1, 5)}}
tiles[1]['P'] = {'grass': [[0, 0, 0, 0, 0, 0, 0],
                        [1, 1, 1, 0, 0, 0, 0],
                        [1, 1, 1, 1, 1, 0, 0],
                        [0, 0, 0, 0, 1, 0, 0],
                        [2, 2, 0, 0, 1, 1, 0],
                        [2, 2, 2, 0, 1, 1, 0],
                        [2, 2, 2, 0, 1, 1, 0]],
              
              'road':  [[0, 0, 0, 0, 0, 0, 0],
                        [0, 0, 0, 0, 0, 0, 0],
                        [0, 0, 0, 0, 0, 0, 0],
                        [1, 1, 1, 1, 0, 0, 0],
                        [0, 0, 1, 1, 0, 0, 0],
                        [0, 0, 0, 1, 0, 0, 0],
                        [0, 0, 0, 1, 0, 0, 0]],
              
              'city':  [[1, 1, 1, 1, 1, 1, 1],
                        [0, 0, 0, 1, 1, 1, 1],
                        [0, 0, 0, 0, 0, 1, 1],
                        [0, 0, 0, 0, 0, 1, 1],
                        [0, 0, 0, 0, 0, 0, 1],
                        [0, 0, 0, 0, 0, 0, 1],
                        [0, 0, 0, 0, 0, 0, 1]],
             }
tiles[1]['Q_m'] = tiles[1]['P_m']
tiles[1]['Q'] = tiles[1]['P']
tiles[1]['R_m'] = {'grass': {1: (3, 1)},
                   'city': {1: (0, 3), 2: (6, 3)}}
tiles[1]['R'] = {'grass': [[0, 0, 0, 0, 0, 0, 0],
                        [1, 1, 0, 0, 0, 1, 1],
                        [1, 1, 1, 1, 1, 1, 1],
                        [1, 1, 1, 1, 1, 1, 1],
                        [1, 1, 1, 1, 1, 1, 1],
                        [1, 1, 0, 0, 0, 1, 1],
                        [0, 0, 0, 0, 0, 0, 0]],
              
              'city':  [[1, 1, 1, 1, 1, 1, 1],
                        [0, 0, 1, 1, 1, 0, 0],
                        [0, 0, 0, 0, 0, 0, 0],
                        [0, 0, 0, 0, 0, 0, 0],
                        [0, 0, 0, 0, 0, 0, 0],
                        [0, 0, 2, 2, 2, 0, 0],
                        [2, 2, 2, 2, 2, 2, 2]],
             }
tiles[1]['S_m'] = {'grass': {1: (5, 2)},
                   'city': {1: (0, 3), 2: (3, 6)}}
tiles[1]['S'] = {'grass': [[0, 0, 0, 0, 0, 0, 0],
                        [1, 1, 0, 0, 0, 1, 0],
                        [1, 1, 1, 1, 1, 0, 0],
                        [1, 1, 1, 1, 1, 0, 0],
                        [1, 1, 1, 1, 1, 0, 0],
                        [1, 1, 1, 1, 1, 1, 0],
                        [1, 1, 1, 1, 1, 1, 0]],
              
              'city':  [[1, 1, 1, 1, 1, 1, 0],
                        [0, 0, 1, 1, 1, 0, 2],
                        [0, 0, 0, 0, 0, 2, 2],
                        [0, 0, 0, 0, 0, 2, 2],
                        [0, 0, 0, 0, 0, 2, 2],
                        [0, 0, 0, 0, 0, 0, 2],
                        [0, 0, 0, 0, 0, 0, 2]],
             }
tiles[1]['T_m'] = {'grass': {1: (6, 3)},
                   'city': {1: (2, 2)}}
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
                        [1, 0, 0, 0, 0, 0, 1]],
             }
tiles[1]['U_m'] = tiles[1]['T_m']
tiles[1]['U'] = tiles[1]['T']
tiles[1]['V_m'] = {'grass': {1: (6, 2), 2: (6, 4)},
                   'road': {1: (6, 3)},
                   'city': {1: (2, 2)}}
tiles[1]['V'] = {'grass': [[0, 0, 0, 0, 0, 0, 0],
                        [0, 0, 0, 0, 0, 0, 0],
                        [0, 0, 0, 0, 0, 0, 0],
                        [0, 0, 0, 0, 0, 0, 0],
                        [0, 0, 0, 0, 0, 0, 0],
                        [0, 0, 1, 0, 2, 0, 0],
                        [0, 1, 1, 0, 2, 2, 0]],
              
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
                        [1, 0, 0, 0, 0, 0, 1]],
             }
tiles[1]['W_m'] = tiles[1]['V_m']
tiles[1]['W'] = tiles[1]['V']
tiles[1]['X_m'] = {'city': {1: (3, 2)}}
tiles[1]['X'] = {'city':  [[1, 1, 1, 1, 1, 1, 1],
                        [1, 1, 1, 1, 1, 1, 1],
                        [1, 1, 1, 1, 1, 1, 1],
                        [1, 1, 1, 1, 1, 1, 1],
                        [1, 1, 1, 1, 1, 1, 1],
                        [1, 1, 1, 1, 1, 1, 1],
                        [1, 1, 1, 1, 1, 1, 1]],
             }