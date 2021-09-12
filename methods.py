# converts letter number notation to usable index
def ln_to_index(ln):
    # spliting string
    letter = ln[:len(ln)-1]
    number = int(ln[1:])
    # getting row
    row = 8 - number
    # getting column
    columns = {'a' : 0,
               'b' : 1,
               'c' : 2,
               'd' : 3,
               'e' : 4,
               'f' : 5,
               'g' : 6,
               'h' : 7}
    col = columns[letter]
    index = row * 8 + col
    return index

# Converts fen string to list
def fen_to_list(fen):
    arr = []
    board = fen.split(' ')[0].split('/')
    #print(fen)
    for row in range(len(board)):
        line = board[row]
        for char in line:
            if char.isdigit():
                for i in range(int(char)):
                    arr.append(' ')
            else:
                arr.append(char)
    return arr

# Converts array to fen string
def list_to_fen(board_info, update = True):

    board = board_info['board']
    color = board_info['color']
    castle = board_info['castle']
    en_passant = board_info['en_passant']
    half_move_counter = board_info['half_move_counter']
    full_move_counter = board_info['full_move_counter']
    
    fen_list = ['', '', '', '', '', '']
    count = 0
    layer_count = 0
    # converting board to fen
    for i in range(64):
        if board[i] == ' ':
            count += 1
            layer_count += 1
        else:
            if count != 0:
                fen_list[0] = fen_list[0] + str(count)
                count = 0
            fen_list[0] = fen_list[0] + board[i]
            layer_count += 1
        if layer_count == 8:
            layer_count = 0
            if count != 0:
                fen_list[0] = fen_list[0] + str(count)
                count = 0
            fen_list[0] = fen_list[0] + '/'
    fen_list[0] = fen_list[0][:len(fen_list[0])-1]

    # color
    fen_list[1] = color
    if update:
        new_color = {
            'w': 'b',
            'b': 'w'
        }
        fen_list[1] = new_color[color]
    # castling
    fen_list[2] = castle
    # en passant
    fen_list[3] = en_passant
    # half move
    fen_list[4] = str(half_move_counter)
    # full move
    fen_list[5] = str(full_move_counter)

    # converting to fen string
    fen = ''
    for i in range(6):
        fen = fen + fen_list[i] + ' '

    fen = fen[:len(fen) - 1]
    return fen
    
def print_pieces(arr):
    count = 0
    for i in range(len(arr)):
        print(arr[i], end = ',')
        if count < 7:
            count += 1
        else:
            count = 0
            print()
    print()

def get_distances():
    distances = {}
    for i in range(64):
        string = ''
        row = int(i / 8)
        col = int(i % 8)
        left_distance = col
        right_distance = 7 - col
        top_distance = row
        bottom_distance = 7 - row
        string = (str(left_distance) + ';' 
                  + str(right_distance) + ';' 
                  + str(top_distance) + ';' 
                  + str(bottom_distance))
        distances[i] = string
    return distances

def display_moves(board, moves):
    for move in moves:
        board[move] = '*'
    return board

global distances
distances = get_distances()
 
def get_color(board, loc):
    if board[loc].isupper():
        return 'w'
    elif board[loc].islower():
        return 'b'
        
def check_teammate(color, board, new_index):
    new_color = ''
    if board[new_index] == ' ':
        return False
    elif board[new_index].isupper():
        new_color = 'white'
    elif board[new_index].islower():
        new_color = 'black'
    if color == new_color:
        return True
    return False


def distances_at_i(loc, distances = distances):
    distances = distances[loc].split(';')
    return int(distances[0]), int(distances[1]), int(distances[2]), int(distances[3])

################################
#       MOVE GENERATORS        #
################################

# TODO All move methods could be optimized by changing
# what info is passed through as arguments. such as splitting
# the fen string before being passed through

# PAWN
#  NOTE: seems to work properly
def pawn_move(board_info, distances = distances):

    board = board_info['board']
    loc = board_info['start']
    en_passant = board_info['en_passant']
    color = ''
    moves = []
    info = []
    # getting board distances
    distances = distances[loc].split(';')
    l_distance = int(distances[0])
    r_distance = int(distances[1])
    t_distance = int(distances[2])
    b_distance = int(distances[3])
    
    # getting color
    if board[loc] == 'P':
        color = 'white'
    elif board[loc] == 'p':
        color = 'black'
    
    # generating pseudo moves
    if color == 'black':
        ### black pawn ###
        
        # -- BASIC FORWARD MOVE -- +8
        # check if space is empty
        if b_distance > 0 and board[loc + 8] == ' ':
            moves.append(loc + 8)
            if loc + 8 > 55:
                info.append('pawn_promo;' + str(loc + 8))
        
        # -- PAWN JUMP MOVE -- +16
        # checks if pawn on beginning row
        # checks if space in front is empty
        # and checks if two spaces in front is empty
        if (loc < 16 and board[loc + 8] == ' ' and
            board[loc + 16] == ' '):
            moves.append(loc + 16)
            info.append('pawn_jump;' + str(loc + 16))

        # -- LEFT ATTACK -- +7
        # checks if left attack is on board
        # and checks if space is not empty
        # and checks if left attack square is upper
        if ( b_distance > 0 and l_distance > 0 and board[loc + 7] != ' ' and
            board[loc + 7].isupper()):
            moves.append(loc + 7)
            if loc + 7 > 55:
                info.append('pawn_promo;' + str(loc + 7))


        # -- RIGHT ATTACK -- +9
        # checks if right attack is on board
        # and checks if space is not empty
        # and checks if right attack square is upper
        if (b_distance > 0 and r_distance > 0 and board[loc + 9] != ' ' and
            board[loc + 9].isupper()):
            moves.append(loc + 9)
            if loc + 9 > 55:
                info.append('pawn_promo;' + str(loc + 9))


        # -- EN PASSANT ATTACK -- -8
        # checks if en passant is possible
        # and checks target square color is not same
        # and checks if in valid position for en passant
        if en_passant != '-':
            ep_index = ln_to_index(en_passant)
            if (board[ep_index - 8].isupper() and
                ((ep_index == loc + 9 and r_distance > 0) or
                 (ep_index == loc + 7 and l_distance > 0))):
                moves.append(ep_index)
                info.append('en_passant;' + str(ep_index))

    elif color == 'white':
        ### white pawn ###

        # -- BASIC FORWARD MOVE -- -8
        # check if space is empty
        if t_distance > 0 and board[loc - 8] == ' ':
            moves.append(loc - 8)
            if loc - 8 < 8:
                info.append('pawn_promo;' + str(loc - 8))
         
        # -- PAWN JUMP MOVE -- -16
        # checks if pawn is on beginning row
        # checks if space in front is empty
        # and checks if two spaces in front is empty
        if (loc > 46 and board[loc - 8] == ' ' and 
            board[loc - 16] == ' '):
            moves.append(loc - 16)
            info.append('pawn_jump;' + str(loc - 16))

        # -- LEFT ATTACK -- -9
        # checks if left attack is on board
        # and checks if left attack square is upper
        if (t_distance > 0 and l_distance > 0 and board[loc - 9] != ' ' and 
            board[loc - 9].islower()):
            moves.append(loc - 9)
            if loc - 9 < 8:
                info.append('pawn_promo' + str(loc - 9))

        # -- RIGHT ATTACK -- -7
        # checks if right attack is on board
        # and checks if right attack square is upper
        if (t_distance > 0 and r_distance > 0 and board[loc - 7] != ' ' and
            board[loc - 7].islower()):
            moves.append(loc - 7)
            if loc - 7 < 8:
                info.append('pawn_promo' + str(loc - 7))


        # -- EN PASSANT ATTACK -- +8
        # checks if en passant is possible
        # and checks target square color is not same
        # and checks if in valid position for en passant
        if en_passant != '-':
            print(board_info['en_passant'])
            ep_index = ln_to_index(en_passant)
            if (board[ep_index + 8].islower() and
                ((ep_index == loc - 9 and l_distance > 0) or 
                 (ep_index == loc - 7 and r_distance > 0))):
                moves.append(ep_index)
                info.append('en_passant;' + str(ep_index))
    return moves, info


# KNIGHT
def knight_move(board_info, distances = distances):
    
    #  NOTE:
    # knights can potentially move to 8 indicies
    # +6, +10, +15, +17, -6, -10, -15, -17
    
    board = board_info['board']
    loc = board_info['start']
    color = ''
    moves = []
    info = []

    # distances
    distances = distances[loc].split(';')
    l_distance = int(distances[0])
    r_distance = int(distances[1])
    t_distance = int(distances[2])
    b_distance = int(distances[3])

    # getting color of piece
    if board[loc] == 'N':
        color = 'white'
    elif board[loc] == 'n':
        color = 'black'

    # checking if left side +1 is clear
    if l_distance > 0:
        # clear for +15 index and -17 index
        if b_distance > 1 and not check_teammate(color, board, loc + 15):
            moves.append(loc + 15)
        if t_distance > 1 and not check_teammate(color, board, loc - 17):
            moves.append(loc - 17)
        # checking if left side +2 is clear
        if l_distance > 1:
            # clear for +6 index and `-10 indexC:`
            if b_distance > 0 and not check_teammate(color, board, loc + 6):
                moves.append(loc + 6)
            if t_distance > 0 and not check_teammate(color, board, loc - 10):
                moves.append(loc - 10)

    # checking if right side +1 is clear
    if r_distance > 0:
        # clear for +17 index and -15 index
        if b_distance > 1 and not check_teammate(color, board, loc + 17):
            moves.append(loc + 17)
        if t_distance > 1 and not check_teammate(color, board, loc - 15):
            moves.append(loc - 15)
        if r_distance > 1:
            if b_distance > 0 and not check_teammate(color, board, loc + 10):
                moves.append(loc + 10)
            if t_distance > 0 and not check_teammate(color, board, loc - 6):
                moves.append(loc - 6)

    return moves, info

def rook_move(board_info, distances = distances):

    # NOTE
    # FOR UP MOVE
    # Check index-8 index and see if index is
    # empty. If empty move to next index.
    # If square is occupied by teammate then
    # stop loop. If square is occupied by enemy
    # add enemy square then stop loop
    # FOR DOWN MOVE
    # same thing but index+8
    # FOR LEFT MOVE
    # -1
    # FOR RIGHT MOVE
    # +1

    board = board_info['board']
    loc = board_info['start']
    color = ''
    moves = []
    info = []

    if board[loc].isupper():
        color = 'white'
    elif board[loc].islower():
        color = 'black'

    # getting distances from sides
    l_distance, r_distance, t_distance, b_distance = distances_at_i(loc)

    # left line move
    # subtract i
    for i in range(1, l_distance + 1):
        tar = loc - i
        if board[tar] == ' ':
            moves.append(tar)
        elif check_teammate(color, board, tar):
            break
        else:
            moves.append(tar)
            break

    # right line move
    # add i
    for i in range(1, r_distance + 1):
        tar = loc + i
        if board[tar] == ' ':
            moves.append(tar)
        elif check_teammate(color, board, tar):
            break
        else:
            moves.append(tar)
            break

    # down line move
    # add i * 8
    for i in range(1, b_distance + 1):
        tar = loc - (i * 8)
        if board[tar] == ' ':
            moves.append(tar)
        elif check_teammate(color, board, tar):
            break
        else:
            moves.append(tar)
            break

    # up line move
    # subtract i * 8
    for i in range(1, t_distance + 1):
        tar = loc - (i * 8)
        if board[tar] == ' ':
            moves.append(tar)
        elif check_teammate(color, board, tar):
            break
        else:
            moves.append(tar)
            break

    return moves, info

def bishop_move(board_info, distances = distances):

    board = board_info['board']
    loc = board_info['start']
    color = ''
    moves = []
    info = []

    if board[loc].isupper():
        color = 'white'
    elif board[loc].islower():
        color = 'black'

    l_distance, r_distance, t_distance, b_distance = distances_at_i(loc)

    # NOTE
    # take the min of the 2 directions that make up the
    # diagnonal direction to get distance to edge of board
    #
    # then iterate through max adding or subtracting to
    # get diagonal target index

    # left down
    # + i * 8 - i
    m_distance = min(l_distance, b_distance)
    for i in range(1, m_distance + 1):
        tar = loc + i * 8 - i
        if board[tar] == ' ':
            moves.append(tar)
        elif check_teammate(color, board, tar):
            break
        else:
            moves.append(tar)
            break

    # right down
    # + i * 8 + i
    m_distance = min(r_distance, b_distance)
    for i in range(1, m_distance + 1):
        tar = loc + i * 8 + i
        if board[tar] == ' ':
            moves.append(tar)
        elif check_teammate(color, board, tar):
            break
        else:
            moves.append(tar)
            break

    # left top
    # - i * 8 - i
    m_distance = min(l_distance, t_distance)
    for i in range(1, m_distance + 1):
        tar = loc - i * 8 - i
        if board[tar] == ' ':
            moves.append(tar)
        elif check_teammate(color, board, tar):
            break
        else:
            moves.append(tar)
            break

    # right top
    # - i * 8 + i
    m_distance = min(r_distance, t_distance)
    for i in range(1, m_distance + 1):
        tar = loc - i * 8 + i
        if board[tar] == ' ':
            moves.append(tar)
        elif check_teammate(color, board, tar):
            break
        else:
            moves.append(tar)
            break

    return moves, info

#TODO add castling support
def queen_move(board_info, distances = distances):

    # NOTE
    # will be bishop and rook moves combined

    board = board_info['board']
    loc = board_info['start']
    color = ''
    moves = []
    info = []

    if board[loc].isupper():
        color = 'white'
    elif board[loc].islower():
        color = 'black'

    l_distance, r_distance, t_distance, b_distance = distances_at_i(loc)

    # bishop moves
    m_distance = min(l_distance, b_distance)
    for i in range(1, m_distance + 1):
        tar = loc + i * 8 - i
        if board[tar] == ' ':
            moves.append(tar)
        elif check_teammate(color, board, tar):
            break
        else:
            moves.append(tar)
            break

    # right down
    # + i * 8 + i
    m_distance = min(r_distance, b_distance)
    for i in range(1, m_distance + 1):
        tar = loc + i * 8 + i
        if board[tar] == ' ':
            moves.append(tar)
        elif check_teammate(color, board, tar):
            break
        else:
            moves.append(tar)
            break

    # left top
    # - i * 8 - i
    m_distance = min(l_distance, t_distance)
    for i in range(1, m_distance + 1):
        tar = loc - i * 8 - i
        if board[tar] == ' ':
            moves.append(tar)
        elif check_teammate(color, board, tar):
            break
        else:
            moves.append(tar)
            break

    # right top
    # - i * 8 + i
    m_distance = min(r_distance, t_distance)
    for i in range(1, m_distance + 1):
        tar = loc - i * 8 + i
        if board[tar] == ' ':
            moves.append(tar)
        elif check_teammate(color, board, tar):
            break
        else:
            moves.append(tar)
            break

    # rook moves
    for i in range(1, l_distance + 1):
        tar = loc - i
        if board[tar] == ' ':
            moves.append(tar)
        elif check_teammate(color, board, tar):
            break
        else:
            moves.append(tar)
            break

    # right line move
    # add i
    for i in range(1, r_distance + 1):
        tar = loc + i
        if board[tar] == ' ':
            moves.append(tar)
        elif check_teammate(color, board, tar):
            break
        else:
            moves.append(tar)
            break

    # down line move
    # add i * 8
    for i in range(1, b_distance + 1):
        tar = loc + (i * 8)
        if board[tar] == ' ':
            moves.append(tar)
        elif check_teammate(color, board, tar):
            break
        else:
            moves.append(tar)
            break

    # up line move
    # subtract i * 8
    for i in range(1, t_distance + 1):
        tar = loc - (i * 8)
        if board[tar] == ' ':
            moves.append(tar)
        elif check_teammate(color, board, tar):
            break
        else:
            moves.append(tar)
            break

    return moves, info


#TODO add castling
def king_move(board_info, distances = distances):

    board = board_info['board']
    loc = board_info['start']
    color = ''
    moves = []
    info = []

    if board[loc].isupper():
        color = 'white'
    elif board[loc].islower():
        color = 'black'

    l_distance, r_distance, t_distance, b_distance = distances_at_i(loc)

    # up, up left, up right
    if t_distance > 0:
        tar = loc - 8
        if not check_teammate(color, board, tar):
            moves.append(tar)
        # up left check
        if l_distance > 0:
            tar = loc - 9
            if not check_teammate(color, board, tar):
                moves.append(tar)
        if r_distance > 0:
            tar = loc - 7
            if not check_teammate(color, board, tar):
                moves.append(tar)

    # down, down left, down right
    if b_distance > 0:
        tar = loc + 8
        if not check_teammate(color, board, tar):
            moves.append(tar)
        # up left check
        if l_distance > 0:
            tar = loc + 7
            if not check_teammate(color, board, tar):
                moves.append(tar)
        if r_distance > 0:
            tar = loc + 9
            if not check_teammate(color, board, tar):
                moves.append(tar)

    # left
    tar = loc - 1
    if l_distance > 0 and not check_teammate(color, board, tar):
        moves.append(tar)

    # right
    tar = loc + 1
    if r_distance > 0 and not check_teammate(color, board, tar):
        moves.append(tar)

    return moves, info

def generate_move(board_info):
    board = board_info['board']
    piece = board[board_info['start']]
    moves = []
    info = []
    if piece == ' ':
        return moves, info
    method_dic = {
        'k': king_move(board_info),
        'q': queen_move(board_info),
        'n': knight_move(board_info),
        'p': pawn_move(board_info),
        'b': bishop_move(board_info),
        'r': rook_move(board_info)
    }
    std_piece = piece.lower()
    moves, info = method_dic[std_piece]
    return moves, info

def valid_move_check(fen, start, end):

    en_passant = fen.split(' ')[3]
    color = fen.split(' ')[1]
    board = fen_to_list(fen.split(' ')[0])
    
    board_info = {
        'board': board,
        'color': color,
        'castle': fen[2],
        'en_passant': en_passant,
        'half_move_counter': fen[4],
        'full_move_counter': fen[5],
        'start': start,
        'end': end
    }

    print(board_info['color'])
    if get_color(board, start) != board_info['color']:
        return False

    piece = board[start]
    
    moves, move_info = generate_move(board_info)
    if end in moves:
        board[end] = piece
        board[start] = ' '
        new_fen = (board_info)
        new_fen = list_to_fen(board_info)   
        return new_fen
    return False
    
# what is this for?
def check_index(board, *indexs):
    dic = {}
    for index in indexs:
        x = board[index]
        dic[index] = x
    return dict


# FEN  = 'rPbqkbnr/pppppppp/8/3Q4/Pp6/8/PPPPPPP1/RNBQKBNR w KQkq a3 0 1'
# LOC = 3
# LOC = 27
# LOC = 62
# board = fen_to_list(FEN)
# moves, special = generate_move(FEN, LOC)
# print_pieces(display_moves(board, moves))
# print(LOC)
# print(moves)

