import sys
import pygame
import numpy as np
import methods as m

pygame.init()

arr = np.array([1, 2, 3])

screen = pygame.display.set_mode((640, 640))
   
global TILE_SIZE
TILE_SIZE = 80

class Board():
    def __init__(self):  
        # Defining colors of board
        color1 = (146,77,35)
        color2 = (191,147,76)

        # Creating surfaces
        self.surfaces = self.create_surfaces(color1, color2)

    def create_surfaces(self, color1, color2):
        surfaces = [] 
        for i in range(64):
            surfaces.append(pygame.Surface((TILE_SIZE, TILE_SIZE)))
        surfaces = self.color_surfaces(surfaces, color1, color2)
        return surfaces

    def color_surfaces(self, surfaces, color1, color2):
        offset = 0
        count = 0
        for i in range(len(surfaces)):
            if (i + offset) % 2 == 0:
                surfaces[i].fill(color1)
            else:
                surfaces[i].fill(color2)
            if count < 7: 
                count += 1
            else:
                count = 0
                offset += 1

        return surfaces

    def o_draw(self, blit_surface):
        x = 0
        y = 0
        for i in range(len(self.surfaces)):
            blit_surface.blit(self.surfaces[i], (x * TILE_SIZE, y * TILE_SIZE)) 
            if x < 7:
                x += 1
            else:
                x = 0
                y += 1
                
class Pieces():
    def __init__(self, fen):
        self.fen = fen
        self.positions = self.get_positions(fen, (0,0), -1, 'w')
        self.color = fen.split(' ')[1]
        self.board = m.fen_to_list(self.fen)
        self.moves = {}
        self.image_path = {
            # KINGS
            'k': 'images/b_k.png',
            'K': 'images/w_k.png',
            # ROOKS
            'r': 'images/b_r.png',
            'R': 'images/w_r.png',
            # BISHOPS
            'b': 'images/b_b.png',
            'B': 'images/w_b.png',
            # KNIGHTS
            'n': 'images/b_n.png',
            'N': 'images/w_n.png',
            # PAWNS
            'p': 'images/b_p.png',
            'P': 'images/w_p.png',
            # QUEENS
            'q': 'images/b_q.png',
            'Q': 'images/w_q.png'
        }
        
    def get_positions(self, fen, cursor_pos, click_i, color):
        x = 0
        y = 0
        positions = {}
        board = m.fen_to_list(fen)
        for i in range(64):
            if i == click_i and board[i] != ' ' and m.get_color(board, click_i) == color:
                positions[i] = '2;' + str(int(cursor_pos[0] - TILE_SIZE/2)) + ';' + str(int(cursor_pos[1] - TILE_SIZE/2))
            elif board[i] != ' ':
                positions[i] = '1;' + str(x * TILE_SIZE) + ';' + str(y * TILE_SIZE)
            if x < 7:
                x += 1
            else:
                x = 0
                y += 1
        return positions

    def o_update(self, info):
        cursor_pos = info['cursor_pos']
        full_move = info['full_move']
        click_i = info['click_i']
        self.color = self.fen.split(' ')[1]
        self.board = m.fen_to_list(self.fen)
        if full_move != '':
            full_move = full_move.split(';')
            start = int(full_move[0])
            end = int(full_move[1])
            check = m.valid_move_check(self.fen, start, end)
            # below is logic for move
            if check != False:
                self.fen = check
                print('################')
                print()
                print(self.fen)
                print()
                m.print_pieces(m.fen_to_list(self.fen))
            info['full_move'] = ''
        elif full_move == '': 
            self.positions = self.get_positions(self.fen, cursor_pos, click_i, self.color)
   
    def o_draw(self, blit_surface):
        blit_order = {}
        for key in self.positions.keys():
            value = self.positions[key].split(';')
            order = int(value[0])
            old_str = blit_order.get(order, '')
            blit_order[order] = old_str + str(key) + ';'
        for key in blit_order:
            blit_order[key] = blit_order[key][:len(blit_order[key]) - 1]
            string_list = blit_order[key].split(';')
            for index in string_list:
                pos_string = self.positions[int(index)].split(';')
                pos = (int(pos_string[1]), int(pos_string[2]))
                blit_surface.blit(pygame.transform.scale(pygame.image.load(
                    self.image_path[self.board[int(index)]]), (TILE_SIZE, TILE_SIZE)), pos)
                

            
def get_mouse_i(cursor_pos):
    x = int(cursor_pos[0]/TILE_SIZE)
    y = int(cursor_pos[1]/TILE_SIZE)
    return y * 8 + x

def update(info, *objs):
    for obj in objs:
        obj.o_update(info)

def draw(*objs):
    for obj in objs:
        obj.o_draw(screen)
    pygame.display.flip()

def update_info(info):
    info['cursor_pos'] = (int(pygame.mouse.get_pos()[0]), int(pygame.mouse.get_pos()[1]))
    
def event_loop(info):
    info['drop_pos'] = -1
    for event in pygame.event.get():
        if event.type == pygame.QUIT: sys.exit(0)
        elif event.type == pygame.MOUSEBUTTONDOWN:
            if pygame.mouse.get_pressed()[0] and not pygame.mouse.get_pressed()[1] and not pygame.mouse.get_pressed()[2]:
                info['click_i'] = get_mouse_i(info['cursor_pos'])
        elif event.type == pygame.MOUSEBUTTONUP and not pygame.mouse.get_pressed()[0]:
            info['full_move'] = str(info['click_i']) + ';' + str(get_mouse_i(info['cursor_pos']))
            info['click_i'] = -1
                
fen = 'rnbqkbnr/pppppppp/8/8/8/8/PPPPPPPP/RNBQKBNR w KQkq - 0 1'
board = Board()
pieces = Pieces(fen)
info = {'click_i': -1,
        'cursor_pos': -1,
        'full_move': '',
        'board': m.fen_to_list(fen)}

while True:
    update_info(info)
    event_loop(info)
    update(info, pieces)
    draw(board, pieces)
