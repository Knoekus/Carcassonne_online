def init(Carcassonne):
    Carcassonne.tiles_dict = dict()
    Carcassonne.tile_last_placed = None

def _Add_tiles_standard(Carcassonne):
    numbers = [8, 9, 4, 1, 3, 3, 3, 4, 5, 4, 2, 1, 2, 3, 2, 3, 2, 3, 2, 3, 1, 1, 2, 1]
    