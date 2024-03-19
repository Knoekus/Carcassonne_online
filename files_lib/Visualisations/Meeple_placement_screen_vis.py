#%% Imports
# PyQt6
import PyQt6.QtGui     as QtG
import PyQt6.QtWidgets as QtW
import PyQt6.QtCore    as QtC
import PyQt6_Extra     as QtE

# Custom classes
import tile_data

# Other packages
import numpy as np

#%% Meeple placement screen visualisation
class Meeple_placement_screen_vis(QtW.QDialog):
    def __init__(self, Carcassonne, tile, meeple):
        super().__init__()
        self.Carcassonne = Carcassonne
        
        self.Window_properties()
        self.Parameters(tile, meeple)
        self.Layout()
        
        # Wrap it up
        self.show()
        self.setFixedSize(self.width(), self.height())
    
    def Window_properties(self):
        self.setWindowTitle('Place your meeple')
    
    def Parameters(self, tile, meeple):
        # self.animation_groups = [Animations.AnimationGroup_parallel(), Animations.AnimationGroup_parallel()]
        self.original_tile = tile
        self.meeple = meeple
        self.sub_tile_selected = None
        self.patches = {material:dict() for material in self.Carcassonne.materials}
    
    def Layout(self):
        def _Make_sub_tile_old(pixmap, row, col):
            # Find out if material patch is occupied
            for material in self.main_tile.material_data.keys():
                mat_idx = self.main_tile.material_data[material][row][col]
                if mat_idx > 0:
                # Material patch found
                    # Add subtile to patch
                    try:
                        self.patches[material][mat_idx] += [(row, col)]
                    except:
                        self.patches[material][mat_idx] = [(row, col)]
                    
                    # Get strength information
                    pos_idx = self.original_tile.possessions[material][mat_idx]
                    pos = self.Carcassonne.possessions[material][pos_idx]
                    player_strength = pos['player_strength']
                    total_strengths = [sum(player_strength[meeple].values()) for meeple in player_strength.keys()]
                    if sum(total_strengths) == 0:
                    # Possession has not yet been claimed
                        sub_tile = QtE.ClickableImage(pixmap, self.sub_length, self.sub_length)
                        sub_tile.clicked.connect(self._Position_selected(sub_tile, material, mat_idx, pos_idx))
                        sub_tile.enable()
                        self.tile_layout.addWidget(sub_tile, row, col)
                    else:
                    # Possession has been claimed, so blur out
                        sub_tile = QtE.QImage(pixmap, self.sub_length, self.sub_length)
                        self.tile_layout.addWidget(sub_tile, row, col)
                        
                        # Blur layer
                        overlay_layer = QtG.QImage(self.sub_length, self.sub_length, QtG.QImage.Format.Format_RGBA64)
                        colour = QtG.QColor(0, 0, 0, 150)
                        overlay_layer.fill(colour)
                        overlay_widget = QtE.QImage(overlay_layer, self.sub_length, self.sub_length)
                        self.tile_layout.addWidget(overlay_widget, row, col)
                        
                    self.sub_tiles[(row, col)] = sub_tile
        
        def _Make_sub_tile(pixmap, row, col):
            # Find out if material patch is occupied
            for material in self.main_tile.material_data.keys():
                mat_idx = self.main_tile.material_data[material][row][col]
                if mat_idx > 0:
                # Material patch found
                    # Add subtile to patch
                    try:
                        self.patches[material][mat_idx] += [(row, col)]
                    except:
                        self.patches[material][mat_idx] = [(row, col)]
                    
                    # Get strength information
                    try:
                        pos_idx = self.original_tile.possessions[material][mat_idx]
                    except:
                        print(self.original_tile.possessions)
                    pos = self.Carcassonne.possessions[material][pos_idx]
                    player_strength = pos['player_strength']
                    total_strengths = [sum(player_strength[meeple].values()) for meeple in player_strength.keys()]
                    if sum(total_strengths) == 0:
                    # Possession has not yet been claimed
                        sub_tile = QtE.ClickableImage(pixmap, self.sub_length, self.sub_length)
                        sub_tile.clicked.connect(self._Position_selected(sub_tile, material, mat_idx, pos_idx))
                        sub_tile.enable()
                        self.tile_layout.addWidget(sub_tile, row, col)
                        break
            else:
            # Possession cannot be claimed, so blur out
                sub_tile = QtE.QImage(pixmap, self.sub_length, self.sub_length)
                self.tile_layout.addWidget(sub_tile, row, col)
                
                # Blur layer
                overlay_layer = QtG.QImage(self.sub_length, self.sub_length, QtG.QImage.Format.Format_RGBA64)
                colour = QtG.QColor(0, 0, 0, 150)
                overlay_layer.fill(colour)
                overlay_widget = QtE.QImage(overlay_layer, self.sub_length, self.sub_length)
                self.tile_layout.addWidget(overlay_widget, row, col)
            
            # Finalise
            self.sub_tiles[(row, col)] = sub_tile
        
        def _Recreate_tile(tile, all_materials):
            # Properties
            file = tile.file
            letter = tile.letter
            index = tile.index
            rotation = tile.rotation
            
            # Making tile
            new_tile = QtE.Tile(None, 160, self.Carcassonne)
            new_tile.set_tile(file, index, letter)
            
            # Rotating
            rotations = int(np.floor(rotation/90))
            if rotations < 0:
                for idx in range(-rotations):
                    new_tile.rotate(-90)
            elif rotations > 0:
                for idx in range(rotations):
                    new_tile.rotate(90)
            
            self.pixmap = new_tile.pixmap.transformed(QtG.QTransform().rotate(rotation), QtC.Qt.TransformationMode.FastTransformation)
            self.pixmap_og = self.pixmap.copy()
            self.material_data = new_tile.material_data
                
            return new_tile
                    
        def _Split_layout():
            main_layout = QtW.QHBoxLayout()
            main_layout.addStretch()
            
            # Tile layout
            self.tile_layout = QtW.QGridLayout()
            self.tile_layout.setSpacing(0)
            self.sub_tiles = dict()
            
            pixmap_size = self.pixmap.width()
            pixels = len(tile_data.tiles[1]['A']['grass'])
            self.sub_length = round(pixmap_size/pixels)
            for row in range(pixels):
                row_b = row*self.sub_length
                for col in range(pixels):
                    col_b = col*self.sub_length
                    
                    sub_pixmap = self.pixmap.copy(col_b, row_b, self.sub_length, self.sub_length)
                    _Make_sub_tile(sub_pixmap, row, col)
            
            # Final stretch column
            main_layout.addLayout(self.tile_layout)
            main_layout.addStretch()
            
            return main_layout
        
        # Tile layout
        self.main_tile = _Recreate_tile(self.original_tile, self.Carcassonne.materials)
        
        # Buttons
        self.y_button = QtW.QPushButton('Confirm')
        font = self.Carcassonne.Properties.Font(size=-2, bold=False)
        self.y_button.setFont(font)
        self.y_button.setEnabled(False)
        
        self.n_button = QtW.QPushButton('Cancel')
        font = self.Carcassonne.Properties.Font(size=-2, bold=False)
        self.n_button.setFont(font)
        
        # Final layout
        layout = QtW.QGridLayout()
        layout.addLayout(_Split_layout(),   0, 0, 1, 2)
        layout.addWidget(self.n_button, 1, 0)
        layout.addWidget(self.y_button, 1, 1)
        self.setLayout(layout)
        
    def _Meeple_placed(self):
        self.meeple.make_unavailable()
    
    def _Position_selected(self, sub_tile, material, mat_idx, pos_idx):
        # sub_tile callback function
        def clicked():
            # Material patch selected update
            self.sub_tile_selected = (material, mat_idx, pos_idx)
            
            # # Visualise
            # # ...
            # # OR Paint meeple on corresponding material patch
            # # OR Make material patch blink
            # if self.animation_groups[0].repeat == True:
            # # Animation 1 is running, so let it finish while using 2
            #     self.animation_groups[0].stop_animation()
            #     animation_group = self.animation_groups[1]
            # else:
            # # Animation 1 can be used
            #     self.animation_groups[1].stop_animation()
            #     animation_group = self.animation_groups[0]
            # animation_group.clear()
            
            # patch_tiles = self.patches[material][mat_idx]
            # for coords in patch_tiles:
            #     sub_tile = self.sub_tiles[coords]
            #     animation = Animations.Animation(sub_tile)
            #     animation.add_blinking(1, 0.6, 2000, 0)
            #     animation_group.add(animation)
            # animation_group.start_animation()
            
            # Enable and default the confirm button
            self.y_button.setEnabled(True)
            self.y_button.setDefault(True)
        return clicked
