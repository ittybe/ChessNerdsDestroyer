from ahk import AHK
import time
import pyscreenshot as ImageGrab
from image_slicer import slice
import os
from PIL import Image
import json
import tempfile
from pathlib import Path
import chess
import logging
# TODO Test get_rivals_move
# TODO write update board method
# TODO check click method with black player 
class BoardAPI:
    """
    def __init__(self, point_top_right, point_top_left, point_bottom_right, point_bottom_left):
        # point format (x, y) tuple type
        top = point_top_right[1]
        bottom = point_bottom_right[1]
        left = point_top_left[0]
        right = point_top_right[0]

        self.point_top_right = point_top_right

        if (point_top_left[1] != top):
            point_top_left = (left, top)
        self.point_top_left = point_top_left

        if (point_bottom_right[0] != right ):
            point_bottom_right = (right, bottom)
        self.point_bottom_right = point_bottom_right

        if (point_bottom_left[0] != left or point_bottom_left[1] != bottom):
            point_bottom_left = (left, bottom)

        self.point_bottom_left = point_bottom_left
    """
    def __init__(self, point_top_right, length, playing_color):
        self.point_top_right = point_top_right;
        self.point_top_left = (point_top_right[0] + length,  point_top_right[1])
        self.point_bottom_right = (point_top_right[0],  point_top_right[1] + length)
        self.point_bottom_left = (point_top_right[0] + length,  point_top_right[1] + length)
        self.board = chess.Board()
        # to detect rival move 
        self.previous_board_state = {'a8': ('black', 'R'), 'b8': ('black', 'N'), 'c8': ('black', 'B'), 'd8': ('black', 'Q'), 'e8': ('black', 'K'), 'f8': ('black', 'B'), 'g8': ('black', 'N'), 'h8': ('black', 'R'), 'a7': ('black', 'P'), 'b7': ('black', 'P'), 'c7': ('black', 'P'), 'd7': ('black', 'P'), 'e7': ('black', 'P'), 'f7': ('black', 'P'), 'g7': ('black', 'P'), 'h7': ('black', 'P'), 'a6': None, 'b6': None, 'c6': None, 'd6': None, 'e6': None, 'f6': None, 'g6': None, 'h6': None, 'a5': None, 'b5': None, 'c5': None, 'd5': None, 'e5': None, 'f5': None, 'g5': None, 'h5': None, 'a4': None, 'b4': None, 'c4': None, 'd4': None, 'e4': None, 'f4': None, 'g4': None, 'h4': None, 'a3': None, 'b3': None, 'c3': None, 'd3': None, 'e3': None, 'f3': None, 'g3': None, 'h3': None, 'a2': ('white', 'P'), 'b2': ('white', 'P'), 'c2': ('white', 'P'), 'd2': ('white', 'P'), 'e2': ('white', 'P'), 'f2': ('white', 'P'), 'g2': ('white', 'P'), 'h2': ('white', 'P'), 'a1': ('white', 'R'), 'b1': ('white', 'N'), 'c1': ('white', 'B'), 'd1': ('white', 'Q'), 'e1': ('white', 'K'), 'f1': ('white', 'B'), 'g1': ('white', 'N'), 'h1': ('white', 'R')}

        self.playing_color = playing_color
        self.ahk = AHK()
    
    def init(self):
        self.previous_board_state = self.get_figures_pos()

    def get_rival_color(self):
        map_color = {
            "white" : "black", 
            "black" : "white"
        }
        return map_color[self.playing_color]

    def get_A(self):
        return abs(self.point_bottom_right[1]) - abs(self.point_top_right[1]);
    
    def get_B(self):
        return abs(self.point_top_left[0]) - abs(self.point_top_right[0]);

    def get_C(self):
        return abs(self.point_bottom_left[1]) - abs(self.point_top_left[1]);

    def get_D(self):
        return abs(self.point_bottom_left[0]) - abs(self.point_bottom_right[0]);


    def save_image_of_board(self, filepath):
        # part of the screen
        im = ImageGrab.grab(bbox=(
            self.point_top_right[0], self.point_top_right[1], 
            self.point_bottom_left[0], self.point_bottom_left[1]))  # X1,Y1,X2,Y2

        # save image file
        im.save(filepath)

    def _slice_images(self, filepath, dirpath):
        # white case
        
        board_coord_map_col = {
            1: "8",
            2: "7",
            3: "6",
            4: "5",
            5: "4",
            6: "3",
            7: "2",
            8: "1"
        }

        board_coord_map_row = {
            1: "a",
            2: "b",
            3: "c",
            4: "d",
            5: "e",
            6: "f",
            7: "g",
            8: "h"
        }
        
        # black case
        if (self.playing_color == "black"):
            board_coord_map_col = {
                1: "1",
                2: "2",
                3: "3",
                4: "4",
                5: "5",
                6: "6",
                7: "7",
                8: "8"
            }
            board_coord_map_row = {
                1: "h",
                2: "g",
                3: "f",
                4: "e",
                5: "d",
                6: "c",
                7: "b",
                8: "a"
            }


        tiles = slice(filepath, 64, 8, 8, False)
        result = []
        for tile in tiles:
            filepath = dirpath
            filename = f"{board_coord_map_row[tile.row]}{board_coord_map_col[tile.column]}.png"
            fullpath = os.path.join(filepath, filename)
            tile.save(fullpath)
            result.append(fullpath)
        return result


    def get_figures_pos(self, debug=False):
        """[summary]
            returns dict with figures and possitions
            possitions as keys and figures as value
        """
        result = {}
        with tempfile.TemporaryDirectory() as tmpdirname:
            filepath = os.path.join(tmpdirname, "board.png")
            self.save_image_of_board(filepath)
            tiles_pathes = self._slice_images(filepath, tmpdirname)
            for tile in tiles_pathes:
                figure = self.recognize_figure(tile)
                tile_location = Path(tile).stem
                result[tile_location] = figure
            if (debug):
                print(tmpdirname)
                input(f"press any button {__name__}")

        return result


    def _get_figures_pos(self, debug=True):
        result = {}
        tmpdirname = tempfile.mkdtemp()
        if True:
            filepath = os.path.join(tmpdirname, "board.png")
            self.save_image_of_board(filepath)
            tiles_pathes = self._slice_images(filepath, tmpdirname)
            for tile in tiles_pathes:
                figure = self.recognize_figure(tile)
                tile_location = Path(tile).stem
                result[tile_location] = figure
            if (debug):
                print(tmpdirname)
                input(f"press any button {__name__}")

        return result

    def get_board_state_fen(self, debug=False):
        return self.board.fen()

    def recognize_figure(self, filepath):
        # output format (1 or 2, "letter")
        result = None
        which_color = { 
            "(248, 248, 248)" : "white", # whie color
            "(86, 83, 82)" : "black"  # black color
        }
        approx_pixel_count_map = {
            "K" : 2171,
            "Q" : 1865,
            "R" : 1507,
            "B" : 1365,
            "N" : 1677,
            "P" : 978
        }

        coef_map  = {
            "K" : 4.15707,
            "Q" : 4.91825,
            "R" : 5.98871,
            "B" : 6.61172,
            "N" : 5.18163,
            "P" : 9.22801
        }

        im = Image.open(filepath)

        pixels = list(im.getdata())
        width, height = im.size
        pixels = [pixels[i] for i in range(height * width)]
        
        unique_pixels = list(set(pixels))
        pixel_count = {}
        for pixel in unique_pixels:
            if (pixels.count(pixel) > 20):
                pixel_count[str(pixel)] = pixels.count(pixel)
        # create difference dict
        difference_dict = {}
        # find main color
        figure_color = None
        main_color_pixel = None
        for pixel in pixel_count:
            if pixel in which_color:
                figure_color = which_color[pixel]
                main_color_pixel = pixel
        
        if figure_color is not None:
            # get subtraction of main color
            for figure_letter in approx_pixel_count_map:
                # write into difference dict as differ as key and letter as value
                # amount_of_pixels = width * height
                # coefficient = amount_of_pixels / pixel_count[main_color_pixel]
                # difference = abs(coefficient - coef_map[figure_letter])
                # difference_dict[difference] = figure_letter
                # working
                difference =abs(pixel_count[main_color_pixel] - approx_pixel_count_map[figure_letter]) 
                difference_dict[difference] = figure_letter
            
            diff_list = list(difference_dict.keys())
            diff_list.sort()
            print(f"recognize_figure: filepath = {filepath} diffrenece dict = ")
            print(difference_dict)
            print(f"sorted values: {diff_list}")
            print()
            figure_letter = difference_dict[diff_list[0]]
            result = (figure_color, figure_letter)

        return result 
    
    def _click_on_tile(self, tile_location :str):
        # white case
        letter_map = {
            "a" : 0,
            "b" : 1,
            "c" : 2,
            "d" : 3,
            "e" : 4,
            "f" : 5,
            "g" : 6,
            "h" : 7
        }
        number_map = {
            "8" : 0,
            "7" : 1,
            "6" : 2,
            "5" : 3,
            "4" : 4,
            "3" : 5,
            "2" : 6,
            "1" : 7
        }
        # black case
        if (self.playing_color == "black"):
            letter_map = {
                "a" : 7,
                "b" : 6,
                "c" : 5,
                "d" : 4,
                "e" : 3,
                "f" : 2,
                "g" : 1,
                "h" : 0
            }
            number_map = {
                "8" : 7,
                "7" : 6,
                "6" : 5,
                "5" : 4,
                "4" : 3,
                "3" : 2,
                "2" : 1,
                "1" : 0
            }   
        
        length = self.get_A()

        length_of_tile = length/8
        # init X Y values which will be added to point top right
        # set X to letter_sequence * width + (width/8/2)
        X = letter_map[tile_location[0]] * length_of_tile + (length_of_tile/2)
        
        # set Y to number * height + (height/8/2)
        Y = number_map[tile_location[1]] * length_of_tile + (length_of_tile/2)
        
        # add to point top rigth X and Y
        coords = (self.point_top_right[0] + X, self.point_top_right[1] + Y)
        print(X)
        print(Y)
        print(coords)
        # click with this coords on screen

        self.ahk.click(coords[0], coords[1])

        # get rid of cursor
        self.ahk.mouse_move(0, 0)

    def move_figure_from_to(self, coords :str):
        """[summary]

        Args:
            coords (str): e5e1 this is an example of coords 
        """
        print(f" move_figure_from_to coords is {coords}")
        print(f"before:\n{self.board}")

        self._click_on_tile(coords[:2])
        self._click_on_tile(coords[2:])
        
        self.board.push_uci(coords)
        # TODO optimize this shit, if it s needed due to optimazation problem with this method 
        self.previous_board_state = self.get_figures_pos()

        print(f"after:\n{self.board}")


    def update_board_after_rival_move(self):
        print("update_board_after_rival_move")
        print(f"before:\n{self.board}")
        moveuci = self.get_rivals_move()
        self.board.push_uci(moveuci)
        self.previous_board_state = self.get_figures_pos()
        print(f"after:\n{self.board}")

    def is_my_turn(self):
        turn_dict = {
            chess.BLACK : "black" ,
            chess.WHITE : "white"
        }

        return turn_dict[self.board.turn] == self.playing_color 

    def get_rivals_move(self):
        # get new board state
        new_board_state = self.get_figures_pos()
        
        # check if it s catstling 
        castling_tiles_map = {
            "white" : {
                'K' : ['e1', 'g1'],
                'Q' : ['c1', 'd1']
            },
            "black" : {
                'K' : ['e8','g8'],
                'Q' : ['c8','d8']
            }
        }
        
        # check castling rivals tiles from King side
        print("get_rival_move: check for castling k side")

        k_side_castle = castling_tiles_map[self.get_rival_color()]['K']
        if new_board_state[k_side_castle[1]] != None and self.previous_board_state[k_side_castle[0]] != None:
            first_check = new_board_state[k_side_castle[1]][1] == 'K' and new_board_state[k_side_castle[0]] == None
            second_check = self.previous_board_state[k_side_castle[1]] == None and self.previous_board_state[k_side_castle[0]][1] == 'K'
            if first_check and second_check:
                return ''.join(k_side_castle)
        print("nope this is not the case")
        # check castling rivals tiles from Queen side
        print("get_rival_move: check for castling q side")
        q_side_castle = castling_tiles_map[self.get_rival_color()]['Q']
        if new_board_state[q_side_castle[0]] != None and new_board_state[q_side_castle[1]] != None:
            first_check = new_board_state[q_side_castle[0]][1] == 'K' and new_board_state[q_side_castle[1]][1] == 'R'
            second_check = self.previous_board_state[q_side_castle[0]] == None and self.previous_board_state[q_side_castle[1]] 
            if first_check and second_check:
                return ''.join(q_side_castle)
        print("this is also not the case")

        # else go ahead    
        
        # check for en passant
        # get en passant fen str from board
        en_passant = self.board.fen().split(" ")[3]
        if en_passant != '-':
            # if on that tile is a pawn, then check where is was
            positions = list(new_board_state.keys())
            prev_pos = None
            # get position, comparing new and old states, of empty tile 
            for position in positions:
                # where no figure there is coords for first part
                existing_check =  new_board_state[position] == None
                generic_check = new_board_state[position] != self.previous_board_state[position] 
                if generic_check and existing_check and en_passant[0] not in position:
                    prev_pos = position
                    logging.debug(f"Comparing En passant new board state[pos] = {new_board_state[position]} prev pos = {self.previous_board_state[position]}, pos appended = {position} ")
            return position + prev_pos
        # concate en passant str with pawn prev pos 
        # return this 
        # else go ahead 
        

        # compare every single position on board with new board state
        positions = list(new_board_state.keys())
        changed_pos = []

        # get position, comparing new and old states, of empty tile 
        for position in positions:
            # where no figure there is coords for first part
            existing_check =  new_board_state[position] == None
            generic_check = new_board_state[position] != self.previous_board_state[position] 
            if generic_check and existing_check:
                changed_pos.append(position)
                logging.debug(f"Comparing None new board state[pos] = {new_board_state[position]} prev pos = {self.previous_board_state[position]}, pos appended = {position} ")
        # get figure that moved and new pos of this figure 
        for position in positions:
            # where figure appeared there is coords for second part 
            if (new_board_state[position] != None):
                color_check =  new_board_state[position][0] == self.get_rival_color() 
                generic_check = new_board_state[position] != self.previous_board_state[position] 
                if generic_check and color_check:
                    changed_pos.append(position)  
                    logging.debug(f"Comparing figure new board state[pos] = {new_board_state[position]} prev pos = {self.previous_board_state[position]}, pos appended = {position} ")

        # get two difference positions of rivals figures
        move = ''.join(changed_pos)
        if (move == ''):
            move = None
        # promotion in chess, if pawn manage to get to the other side of a board
        # TODO there some bug where Knight recognized as Queen in some cases
        # have no idea how to fix that so I jsut bodge this 
        if self.previous_board_state[changed_pos[0]][1] != new_board_state[changed_pos[1]][1] and self.previous_board_state[changed_pos[0]][1] == 'P' :  
            print(f"promotion check: prev on '{changed_pos[0]}' = {self.previous_board_state[changed_pos[0]]}, new on '{changed_pos[1]}' = {new_board_state[changed_pos[1]]}")
            print(self.previous_board_state)
            print(new_board_state)
            move += new_board_state[changed_pos[1]][1].lower()
        return move
        

if __name__ == "__main__":
    logging.basicConfig(level=logging.INFO)
    ahk = AHK()
    b = BoardAPI(
        (270,171),
        760, 
        "black"
    )
    time.sleep(2)
    print(b._get_figures_pos())
    exit()
    print(b.get_rivals_move())
    print(b.update_board_after_rival_move())
    print(b.move_figure_from_to("e7e5"))
    #print(b.get_figures_pos(True))
    exit()
    b.save_image_of_board("images/board.png")

    b.move_figure_from_to("e2e4")
    figures = b.get_figures_pos()
    exit()
    print(figures)
    with open("test.json", "w") as f:
        json.dump(figures , f)
    exit()
    b.save_image_of_board("images/board.png")
    print("BOOM")

    b._slice_images("images/board.png", "images")
    exit()
    p_c = b.recognize_figure(r"C:\Users\Superuser\Pictures\Saved Pictures\chess\f1.png")
    print(p_c)
    exit()
    with open("test.json", "w") as f:
        json.dump(p_c, f)
    exit()
    time.sleep(2)
    filepath = r"C:\Users\Superuser\Pictures\Saved Pictures\chess\board.png"
    dirpath = r"C:\Users\Superuser\Pictures\Saved Pictures\chess"
    #b.save_image_of_board(filepath)
    b._slice_images(filepath, dirpath)
    exit()
    print(b.point_top_right)
    print(b.point_top_left)
    print(b.point_bottom_right)
    print(b.point_bottom_left)
    time.sleep(2)
    
    ahk.mouse_move(
        x=b.point_top_left[0], 
        y=b.point_top_left[1], 
        speed=10, blocking=True
        )

    ahk.mouse_move(
        x=b.point_bottom_left[0], 
        y=b.point_bottom_left[1], 
        speed=10, blocking=True
        )     

    ahk.mouse_move(
        x=b.point_top_right[0], 
        y=b.point_top_right[1], 
        speed=10, blocking=True
        )    
    
    ahk.mouse_move(
        x=b.point_bottom_right[0], 
        y=b.point_bottom_right[1], 
        speed=10, blocking=True
        )

    print("ultimate testing")
    ahk.mouse_move(
        x=b.point_top_right[0], 
        y=b.point_top_right[1], 
        speed=10, blocking=True
        )
    
    ahk.mouse_move(
        x=b.point_top_right[0] + b.get_B(), 
        y=b.point_top_right[1], 
        speed=10, blocking=True
        )

    ahk.mouse_move(
        x=b.point_top_right[0] + b.get_B(), 
        y=b.point_top_right[1] + b.get_C(), 
        speed=10, blocking=True
        )

    ahk.mouse_move(
        x=b.point_top_right[0] + b.get_B(), 
        y=b.point_top_right[1] + b.get_C(), 
        speed=10, blocking=True
        )
    
    print(b.get_A())

    b.save_image_of_board("some.png")