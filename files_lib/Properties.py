#%% Imports
import PyQt6.QtGui     as QtG

#%% Class
class Properties():
    def __init__(self, default_font_size):
        # Static properties
        self.font       = 'Microsoft Sans Serif'
        self.colours    = ['ffffff00', 'ff1414ff', 'ff7d00ff', 'ffff00ff', '14ff14ff', '3232ffff', 'cc32ffff']
        self.expansions = ['The River', r'Inns && Cathedrals', 'The Abbot']
        self.font_sizes = [8, 9, 10, 11, 12, 14, 16, 18, 20, 24, 28, 32, 36, 42, 48, 56, 62, 70, 78, 86, 94]
        self.default_font_size = default_font_size
        
        self.tile_size  = 150 / 320 # /320 because that is the original pixel size of a tile
        self.tile_spacing = 1
        self.tile_titles = [r'Tiles_1base', r'Tiles_2river1', r'Tiles_3InnsAndC', r'Tiles_4abbot']

    # def Font(self, size, bold:bool):
    def Font(self, **kwargs):
        '''
        kwargs include:
            size : int
                font size
            bold : bool (default = False)
                bold boolean
        '''
        keys = kwargs.keys()
        # Size
        if 'size' in keys:
            size = kwargs['size']
        else:
            raise Exception('Must specify font size.')
        # Bold
        if 'bold' in keys:
            bold = kwargs['bold']
        else:
            bold = False
        
        label_font = QtG.QFont(self.font, self.font_sizes[size + self.default_font_size])
        label_font.setBold(bold)
        return label_font