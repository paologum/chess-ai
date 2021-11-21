
from tkinter import image_types
from typing import List
import chess
import chess.polyglot
import chess.pgn
from random import randint
import PySimpleGUI as sg

#added a COMMENT
sg.theme('DarkAmber')   # Add a touch of color
image_file_path = 'IMAGES/'
image_name = 'blank'
image_file_type = '.png'
move_list = []
difficulties = ['Easy', 'Medium', 'Hard']
total_moves_simulated = 0
depth_options = [1, 2, 3, 4, 5, 6]
thisdict = {
    "B": "wB",
    "K": "wK",
    "N": "wN",
    "Q": "wQ",
    "R": "wR",
    "P": "wP",
    "p": "bp",
    "b": "bB",
    "n": "bN",
    "k": "bK",
    "r": "bR",
    "q": "bQ" }
pawntable = [
    0, 0, 0, 0, 0, 0, 0, 0,
    5, 10, 10, -20, -20, 10, 10, 5,
    5, -5, -10, 0, 0, -10, -5, 5,
    0, 0, 0, 20, 20, 0, 0, 0,
    5, 5, 10, 25, 25, 10, 5, 5,
    10, 10, 20, 30, 30, 20, 10, 10,
    50, 50, 50, 50, 50, 50, 50, 50,
    0, 0, 0, 0, 0, 0, 0, 0]
knightstable = [
    -50, -40, -30, -30, -30, -30, -40, -50,
    -40, -20, 0, 5, 5, 0, -20, -40,
    -30, 5, 10, 15, 15, 10, 5, -30,
    -30, 0, 15, 20, 20, 15, 0, -30,
    -30, 5, 15, 20, 20, 15, 5, -30,
    -30, 0, 10, 15, 15, 10, 0, -30,
    -40, -20, 0, 0, 0, 0, -20, -40,
    -50, -40, -30, -30, -30, -30, -40, -50]
bishopstable = [
    -20, -10, -10, -10, -10, -10, -10, -20,
    -10, 5, 0, 0, 0, 0, 5, -10,
    -10, 10, 10, 10, 10, 10, 10, -10,
    -10, 0, 10, 10, 10, 10, 0, -10,
    -10, 5, 5, 10, 10, 5, 5, -10,
    -10, 0, 5, 10, 10, 5, 0, -10,
    -10, 0, 0, 0, 0, 0, 0, -10,
    -20, -10, -10, -10, -10, -10, -10, -20]
rookstable = [
    0, 0, 0, 5, 5, 0, 0, 0,
    -5, 0, 0, 0, 0, 0, 0, -5,
    -5, 0, 0, 0, 0, 0, 0, -5,
    -5, 0, 0, 0, 0, 0, 0, -5,
    -5, 0, 0, 0, 0, 0, 0, -5,
    -5, 0, 0, 0, 0, 0, 0, -5,
    5, 10, 10, 10, 10, 10, 10, 5,
    0, 0, 0, 0, 0, 0, 0, 0]
queenstable = [
    -20, -10, -10, -5, -5, -10, -10, -20,
    -10, 0, 0, 0, 0, 0, 0, -10,
    -10, 5, 5, 5, 5, 5, 0, -10,
    0, 0, 5, 5, 5, 5, 0, -5,
    -5, 0, 5, 5, 5, 5, 0, -5,
    -10, 0, 5, 5, 5, 5, 0, -10,
    -10, 0, 0, 0, 0, 0, 0, -10,
    -20, -10, -10, -5, -5, -10, -10, -20]
kingstable = [
    20, 30, 10, 0, 0, 10, 30, 20,
    20, 20, 0, 0, 0, 0, 20, 20,
    -10, -20, -20, -20, -20, -20, -20, -10,
    -20, -30, -30, -40, -40, -30, -30, -20,
    -30, -40, -40, -50, -50, -40, -40, -30,
    -30, -40, -40, -50, -50, -40, -40, -30,
    -30, -40, -40, -50, -50, -40, -40, -30,
    -30, -40, -40, -50, -50, -40, -40, -30]


# Function to print move list
def printmovelist():
    global move_list
    if move_list == [] :
        return 'No moves played'
    count = int(1)
    move_list_string = ""
    for m in move_list :
        if count % 2 == 1:
            move_list_string += str(int(count / 2) + 1) + ". "
        move_list_string += m + " "
        if count % 20 == 0 :
            move_list_string += "\n"
        count += 1
    return move_list_string
user_turn = True
# Evaluation function implemented from https://medium.com/dscvitpune/lets-create-a-chess-ai-8542a12afef
def evaluate(board):
    global total_moves_simulated
    total_moves_simulated += 1
    # Checks game over rules and returns integers accordingly
    if board.is_checkmate():
        if board.turn:
            return -9999
        else:
            return 9999
    if board.is_stalemate():
            return 0
    if board.is_insufficient_material():
            return 0
    # Instantiates variables with the amount of each piece
    wp = len(board.pieces(chess.PAWN, chess.WHITE))
    bp = len(board.pieces(chess.PAWN, chess.BLACK))
    wn = len(board.pieces(chess.KNIGHT, chess.WHITE))
    bn = len(board.pieces(chess.KNIGHT, chess.BLACK))
    wb = len(board.pieces(chess.BISHOP, chess.WHITE))
    bb = len(board.pieces(chess.BISHOP, chess.BLACK))
    wr = len(board.pieces(chess.ROOK, chess.WHITE))
    br = len(board.pieces(chess.ROOK, chess.BLACK))
    wq = len(board.pieces(chess.QUEEN, chess.WHITE))
    bq = len(board.pieces(chess.QUEEN, chess.BLACK))

    # Uses the amounts to calculate a score or evaluation of the position (negative means black is winning and
    # positive means white is winning)
    material = 100 * (wp - bp) + 320 * (wn - bn) + 330 * (wb - bb) + 500 * (wr - br) + 900 * (wq - bq)

    #Calculates and evaluates the position of the pieces themselves rather than the pieces
    pawnsq = sum([pawntable[i] for i in board.pieces(chess.PAWN, chess.WHITE)])
    pawnsq = pawnsq + sum([-pawntable[chess.square_mirror(i)]
                        for i in board.pieces(chess.PAWN, chess.BLACK)])
    knightsq = sum([knightstable[i] for i in board.pieces(chess.KNIGHT, chess.WHITE)])
    knightsq = knightsq + sum([-knightstable[chess.square_mirror(i)]
                            for i in board.pieces(chess.KNIGHT, chess.BLACK)])
    bishopsq = sum([bishopstable[i] for i in board.pieces(chess.BISHOP, chess.WHITE)])
    bishopsq = bishopsq + sum([-bishopstable[chess.square_mirror(i)]
                            for i in board.pieces(chess.BISHOP, chess.BLACK)])
    rooksq = sum([rookstable[i] for i in board.pieces(chess.ROOK, chess.WHITE)])
    rooksq = rooksq + sum([-rookstable[chess.square_mirror(i)]
                        for i in board.pieces(chess.ROOK, chess.BLACK)])
    queensq = sum([queenstable[i] for i in board.pieces(chess.QUEEN, chess.WHITE)])
    queensq = queensq + sum([-queenstable[chess.square_mirror(i)]
                            for i in board.pieces(chess.QUEEN, chess.BLACK)])
    kingsq = sum([kingstable[i] for i in board.pieces(chess.KING, chess.WHITE)])
    kingsq = kingsq + sum([-kingstable[chess.square_mirror(i)]
                        for i in board.pieces(chess.KING, chess.BLACK)])
    eval = material + pawnsq + knightsq + bishopsq + rooksq + queensq + kingsq

    #returns the evaluation in favor of whoever's turn it is
    return eval

# MiniMax function
def minimax(depth, board):
    if depth == 0 :
        return evaluate(board)
    if board.turn :
        max_evaluation = -1000000000
        for some_move in board.legal_moves :
            board.push(some_move)
            evaluation = minimax(depth - 1, board)
            board.pop()
            max_evaluation = max(max_evaluation, evaluation)
        return max_evaluation
    else :
        min_evaluation = 100000000000
        for some_move in board.legal_moves :
            board.push(some_move)
            evaluation = minimax(depth - 1, board)
            board.pop()
            min_evaluation = min(evaluation, min_evaluation)
        return min_evaluation

#Get a move from the minimax alogrithim
def getmove(depth, board):
    best_move = chess.Move.null()
    if board.turn :
        best_evaluation = -999999999
    else :
        best_evaluation = 999999999
    for some_move in board.legal_moves:
        board.push(some_move)
        evaluation = minimax(depth - 1, board)
        board.pop()
        if board.turn and evaluation > best_evaluation:
            best_evaluation = evaluation
            best_move = some_move
        elif not board.turn and evaluation < best_evaluation :
            best_evaluation = evaluation
            best_move = some_move
    return best_move

#Applies minimax with an alpha beta pruning
def alphabeta(depth, alpha, beta, board) :
    if depth == 0 :
        return evaluate(board)
    if board.turn :
        max_evaluation = -1000000000
        for some_move in board.legal_moves :
            board.push(some_move)
            evaluation = alphabeta(depth - 1, alpha, beta, board)
            board.pop()
            max_evaluation = max(max_evaluation, evaluation)
            alpha = max(alpha, evaluation)
            if beta <= alpha :
                break
        return max_evaluation
    else :
        min_evaluation = 100000000000
        for some_move in board.legal_moves :
            board.push(some_move)
            evaluation = alphabeta(depth - 1, alpha, beta, board)
            beta = min(evaluation, beta)
            board.pop()
            min_evaluation = min(evaluation, min_evaluation)
            if beta <= alpha :
                break
        return min_evaluation

#Get a move from the minimax alogrithim with alpha beta pruning
def getmove_alphabeta(depth, alpha, beta, board):
    best_move = chess.Move.null()
    if board.turn :
        best_evaluation = -999999999
    else :
        best_evaluation = 999999999
    for some_move in board.legal_moves:
        board.push(some_move)
        evaluation = alphabeta(depth - 1, alpha, beta, board)
        board.pop()
        if board.turn and evaluation > best_evaluation:
            best_evaluation = evaluation
            best_move = some_move
        elif not board.turn and evaluation < best_evaluation :
            best_evaluation = evaluation
            best_move = some_move
    return best_move
def update_board(board):
    global user_turn
    rank_strings = board.fen().split('/')
    print(rank_strings)
    eight_rank = rank_strings[7].split(' ')
    rank_strings[7] = eight_rank[0]
    rank_num = 8
    for rank in rank_strings:
        column_num = 1
        for file in rank:
            if rank_num % 2 == 1 and column_num % 2 == 1:
                    this_color = 'L'
            elif rank_num % 2 == 0 and column_num % 2 == 0:
                this_color = 'L'
            else:
                this_color = 'W'
            try :
                count = int(file)
                while count > 0 :
                    window['tile' + this_color + (chr(column_num + 64) + str(rank_num))].update(image_filename=(image_file_path + 'blank' + image_file_type))
                    count -= 1
                    column_num += 1
                    if this_color == 'L':
                        this_color = 'W'
                    else :
                        this_color = 'L'
                continue
            except ValueError:
                window['tile' + this_color + (chr(column_num + 64) + str(rank_num))].update(image_filename=(image_file_path + thisdict.get(file) + image_file_type))
                column_num += 1
        rank_num = rank_num - 1
        if rank_num == 0:
            break

def ai_play(game, ai_diff):
    global total_moves_simulated
    total_moves_simulated = 0
    #get a rando move
    if (ai_diff == 'Easy') :
        random = randint(0, game.legal_moves.count() - 1)
        count = 0
        for legal_move in game.legal_moves :
            if random == count :
                move = legal_move
                break
            else :
                count += 1
    elif(ai_diff == 'Medium') :
        move = getmove(depth, game)
    elif(ai_diff == 'Hard') :
        try:
            move = (chess.polyglot.MemoryMappedReader("human.bin").weighted_choice(game).move)
        except Exception:
            move = (getmove_alphabeta(depth, -1000000000, 1000000000, game))
            
    move_list.append(game.san(move))
    game.push(move)
    if (game.is_checkmate() or game.is_stalemate() or game.is_insufficient_material() or game.is_fivefold_repetition() or game.is_seventyfive_moves()) :
            return 
    #Update total moves
    window['-TOTAL_MOVES-'].update('Total moves simulated: ' + str(total_moves_simulated))
    return game
def create_window(image_file_path, image_name, image_file_type, difficulties, depth_options, user_turn, default_diff, default_color, default_depth):
    menu = sg.Column(
        [[sg.Text(text='Choose a color!', font = 12, key='-COLOR_TEXT-'), sg.Combo(['White', 'Black'], enable_events=True,
        default_value=default_color, key = '-COLOR-')],
        [sg.Text(text='Pick an AI difficulty!', font = 12, key='-DIFFICULTY_TEXT-'), sg.Combo(difficulties, 
    enable_events=True, default_value=default_diff, key = '-DROPDOWN-')],
    [ sg.Text(text = 'Pick a depth!', font = 12, key = '-DEPTH_TEXT-'), sg.Combo(depth_options, enable_events=True, default_value=default_depth, key='-DEPTH-')],
    [sg.Text(text = 'Total moves simulated by computer: N/A', font = 12, key = '-TOTAL_MOVES-')],
    [sg.Button(button_text = 'See Move list', key = '-MOVE_LIST-'), sg.Button(button_text='Play a game', key='-diff_input-'), sg.Button(button_text='Resign', key='-resign-')],
    ]
    )
    rank_letters = []
    rank_one = []
    rank_two = []
    rank_three = []
    rank_four = []
    rank_five = []
    rank_six = []
    rank_seven = []
    rank_eight = []
    letter_count = 0
    while len(rank_letters) < 9:
        if letter_count == 0:
            rank_letters.append(sg.Text(text=' ', size=(6,1)))
        if user_turn:
            rank_letters.append(sg.Text(text=chr(letter_count + 65), size=(6,1), font = 8))
        else:
            rank_letters.append(sg.Text(text=chr(72 - letter_count), size=(6,1), font = 8))
        letter_count += 1
    board_gui = [rank_one, rank_two, rank_three,rank_four,rank_five,rank_six,rank_seven,rank_eight]
    rank_count = 1
    for rank in board_gui:
        if user_turn:
            column = 1
        else :
            column = 8
        while len(rank) < 9:
            this_color = 'RED'
            if rank_count % 2 == 1 and column % 2 == 1:
                this_color = 'LIGHT GREEN'
            elif rank_count % 2 == 0 and column % 2 == 0:
                this_color = 'LIGHT GREEN'
            else:
                this_color = 'WHITE'
            if column == 1 and user_turn:
                rank.append(sg.Text(text = rank_count))
            if column == 8 and not user_turn:
                rank.append(sg.Text(text = rank_count))
            rank.append(sg.Button(size=(3,1), 
            button_color=this_color, key = 'tile' + this_color[0:1] + chr(column+64) + str(rank_count), border_width=0,
            image_filename=image_file_path + image_name + image_file_type))
            if user_turn:
                column += 1
            else :
                column -= 1
        rank_count += 1  
        if (user_turn) :

            layout =    [[rank_eight],
                        [rank_seven],
                        [rank_six],
                        [rank_five],
                        [rank_four],
                        [rank_three],
                        [rank_two],
                        [rank_one],
                        [rank_letters],
                        [menu]]
        else:
            layout =    [[rank_one],
                        [rank_two],
                        [rank_three],
                        [rank_four],
                        [rank_five],
                        [rank_six],
                        [rank_seven],
                        [rank_eight],
                        [rank_letters],
                        [menu]] 
    return sg.Window('Chess', layout, element_justification='c', size=(800,800))

ai_diff = 'Not Picked'
depth = 1
resign = False
selected_square = ' '
game = chess.Board()
window = create_window(image_file_path, image_name, image_file_type, difficulties, depth_options, True, 'Easy', 'White', '2')
# Create the Window
# Event Loop to process "events" and get the "values" of the inputs
while True:
    event, values = window.read()
    if event == sg.WIN_CLOSED or event == 'Cancel': # if user closes window or clicks cancel
        break
    #WHEN user presses enter to start game
    elif event == '-diff_input-':
        chosen_difficulty = values['-DROPDOWN-']
        chosen_depth = values['-DEPTH-']
        #Start game!
        if ai_diff == 'Not Picked' and (chosen_difficulty == 'Easy' or chosen_difficulty == 'Medium' or chosen_difficulty == 'Hard'): 
            try :
                depth = int(chosen_depth)
                if depth < 1 or depth > 6:
                    sg.popup_notify('Invalid Depth\n', 'Please input a depth from 1 to 6',
                    icon=image_file_path + 'errorpopup' + image_file_type, display_duration_in_ms=100, 
                    fade_in_duration=200)
                    continue
            except ValueError:
                sg.popup_notify('Invalid depth\n', 'Please input a depth with an integer value!',
                icon=image_file_path + 'errorpopup' + image_file_type, display_duration_in_ms=100, 
                fade_in_duration=200)
                continue
            temp_value = values['-COLOR-']
            if temp_value.lower() == 'white':
                user_turn = True
            elif temp_value.lower() == 'black':
                user_turn = False
                window.close()
                window = create_window(image_file_path, image_name, image_file_type, difficulties, depth_options, user_turn, chosen_difficulty, 'Black', depth)
                window.finalize()
                game = ai_play(game, chosen_difficulty)
                update_board(game)
            else:
                sg.popup_notify('Please choose white or black to play!\n',
                icon=image_file_path + 'errorpopup' + image_file_type, display_duration_in_ms=100, 
                fade_in_duration=200)
                continue
            
            ai_diff = chosen_difficulty
            window['-COLOR_TEXT-'].update('You are ' + temp_value.upper())
            window['-DIFFICULTY_TEXT-'].update('AI Difficulty: ' + values['-DROPDOWN-'])
            if chosen_difficulty == 'Easy' :
                window['-DEPTH_TEXT-'].update('Depth: N/A')
            else :
                window['-DEPTH_TEXT-'].update('Depth: ' + str(depth))
            update_board(game)
        #If already started, print error when changing settings!
        elif not ai_diff == 'Not Picked'and (chosen_difficulty == 'Easy' or chosen_difficulty == 'Medium' or chosen_difficulty == 'Hard'):
            sg.popup_notify('Game has started\n', 'Cannot change settings during game!',
            icon=image_file_path + 'errorpopup' + image_file_type, display_duration_in_ms=100, 
            fade_in_duration=200)
    #When selecting a square, highlight it red!
    elif not ai_diff == 'Not Picked' and selected_square == ' ' and user_turn == game.turn and event[int(0):int(4)] == 'tile' and game.color_at(chess.parse_square(event[5:7].lower())) == user_turn:
        window[event].update(button_color = 'RED')
        selected_square = event
    #When selecting a square before game started, print error
    elif ai_diff == 'Not Picked'and event[int(0):int(4)] == 'tile':
        sg.popup_notify('Game has not started\n', 'Choose the settings.',
            icon=image_file_path + 'errorpopup' + image_file_type, display_duration_in_ms=100, 
            fade_in_duration=300)
    #if you already selected a square, see if move is legal or not then proceed accordingly
    elif not selected_square == ' ' and user_turn == game.turn and event[int(0):int(4)] == 'tile':
        try :
            promotion = ''
            #TODO finish figuring out promotion
            print(game.piece_at((chess.parse_square(selected_square[5:7].lower()))).symbol())
            if (event[6:7] == 8 and user_turn and game.piece_at((chess.parse_square(selected_square[5:7].lower()))).symbol() == 'P') :
                promotion_window = sg.Window('Promote to which piece?', size = (100, 400), layout=[
                    [sg.Button(size = (2, 4),image=(image_file_path + thisdict.get('Q') + image_file_type), key = '-WQUEEN_PROMOTION-')], 
                [sg.Button(size = (2, 4),image=(image_file_path + thisdict.get('B') + image_file_type), key = '-WBISHOP_PROMOTION-')], 
                [sg.Button(size = (2, 4), image=(image_file_path + thisdict.get('N') + image_file_type), key = '-WKNIGHT_PROMOTION-')],
                [sg.Button(size = (2, 4),image=(image_file_path + thisdict.get('R') + image_file_type), key = ['-WROOK_PROMOTION-'])]])
                event, values = promotion.read()
                if event == '-WQUEEN_PROMOTION-':
                    promotion = 'Q'
                elif event == '-WBISHOP_PROMOTION-':
                    promotion ='B'
                elif event == '-BKNIGHT_PROMOTION-':
                    promotion = 'N'
                elif event == '-BROOK_PROMOTION-':
                    promotion = 'R'
                promotion_window.close()
            elif (event[6:7] == 1 and not user_turn and game.piece_at((chess.parse_square(selected_square[5:7].lower()))).symbol() == 'p')  :
                promotion_window = sg.Window('Promote to which piece?', size = (100, 400), layout=[
                    [sg.Button(image=(image_file_path + thisdict.get('q') + image_file_type), key = '-BQUEEN_PROMOTION-')], 
                [sg.Button(image=(image_file_path + thisdict.get('b') + image_file_type), key = '-BBISHOP_PROMOTION-')], 
                [sg.Button(image=(image_file_path + thisdict.get('n') + image_file_type), key = '-BKNIGHT_PROMOTION-')],
                [sg.Button(image=(image_file_path + thisdict.get('r') + image_file_type), key = ['-BROOK_PROMOTION-'])]])
                event, values = promotion.read()
                if event == '-BQUEEN_PROMOTION-':
                    promotion = 'q'
                elif event == '-BBISHOP_PROMOTION-':
                    promotion = 'b'
                elif event == '-BKNIGHT_PROMOTION-':
                    promotion = 'n'
                elif event == '-BROOK_PROMOTION-':
                    promotion = 'r'
                promotion_window.close()
            uci_move = game.parse_uci(selected_square[5: 7].lower() + event[5: 7].lower() + promotion)
            for move in game.legal_moves:
                if uci_move == move:
                    move_list.append(game.san(uci_move))
                    game.push(uci_move)
                    #Update total moves
                    window['-TOTAL_MOVES-'].update('Total moves simulated: ' + str(total_moves_simulated))
                    update_board(game)
            if (game.is_checkmate() or game.is_stalemate() or game.is_insufficient_material() or game.is_fivefold_repetition() or game.is_seventyfive_moves()) :
                break     
            #Computer Moves
            try:
                #Play computer move
                game = ai_play(game, ai_diff)
                
                update_board(game)
            except ValueError:
                print('Value Error')
                break
        except ValueError:
            print('Illegal Move')
        if (selected_square[4:5] == 'L'):
            button_color_thing = 'LIGHT GREEN'
        else :
            button_color_thing = "WHITE"
        window[selected_square].update(button_color = button_color_thing)
        selected_square = ' '
    elif event == '-MOVE_LIST-'  :
        if (ai_diff == 'Not Picked') :
            continue
        new_layout = [
            [sg.Text(text=printmovelist(), font = 12, key ='-MOVES-')],
            [sg.Button(button_text = 'Cancel', key = '-CANCEL-')]
        ]
        popup = sg.Window('Move List', new_layout)
        while(True) :
            event_popup, values = popup.read()
            if event_popup == sg.WIN_CLOSED or event_popup == '-CANCEL-' or event_popup == 'Cancel':
                break
        popup.close()
    elif event == '-resign-' and not ai_diff == 'Not Picked':
        resign = True
        break



#Find the winners of the game
if resign:
    sg.popup('You resigned', 'Computer won...')
elif game.outcome().winner == user_turn:
    sg.popup('Checkmate.', 'You won!')
else :
    sg.popup('Checkmate', 'You lost')
window.close()







# while True:
#     try :
#         menu_option = int(input("\nPick one of the three options.\n1. Play a game against an AI\n2. Play a game against an AI starting from a PGN file.\n"))
#         if (menu_option > 0 and menu_option < 3) :
#             break
#         else :
#             print("\nInvalid Value, Try Again")
#     except ValueError:
#         print("\nInvalid Value, Try Again")
#         menu_option = 0
# if (menu_option == 1 or menu_option == 2) :
#     if (menu_option == 2) :
#         need_new_board = False
#         while (not need_new_board) :
#             try : 
#                 file_name = (input("\nWhat is the file name of the PGN? (Do not input the added file extension and make sure the file is in the PGN folder): "))
#                 pgn = open("PGN/" + file_name + ".pgn")
#                 parsed_game = chess.pgn.read_game(pgn)
#                 for some_move in parsed_game.mainline_moves():
#                     total_moves.append(board.san(some_move))
#                     board.push(some_move)
#                 need_new_board = True
#             except (FileNotFoundError, OSError):
#                 print("\nInvalid PGN, try again")
#                 need_new_board = False
#     while not pick_difficulty:
#         try:
#             ai_difficulty = int(input("Which difficulty would you like to play against?\n1. Easy\n2. Medium\n3. Hard\n"))
#             if ai_difficulty < 1 or ai_difficulty > 3 :
#                 print("\nUnfortunately, that is not an option, please pick again.\n")
#                 pick_difficulty = False
#             else :
#                 pick_difficulty = True
#         except ValueError as e:
#             print("\nUnfortunately, that is not an option, please pick again.\n")
#             pick_difficulty = False
        

#     # Picks color of user
#     while not pick_color:
#         try:
#             user_color = int(input("\nWhich color would you like to play?\n1. White\n2. Black\n"))
#             if (user_color != 1 and user_color != 2) :
#                 print("\nUnfortunately, that is not an option, please pick again.")
#                 pick_color = False
#             else :
#                 pick_color = True
#         except ValueError:
#             print("\nUnfortunately, that is not an option, please pick again.")
#             pick_color = False

#     # Picks depth
#     if ai_difficulty == 2 or ai_difficulty == 3:
#         while True:
#             try:
#                 input_depth = int(input("\nTo which depth would you like the computer to think to?\n"))
#                 if (input_depth > 0) :
#                     break
#                 else:
#                     print("\nUnfortunately, that is not an integer, please pick again.")
#             except ValueError:
#                 print("\nUnfortunately, that is not an integer, please pick again.")

#     if (board.turn) :
#         start_turn = "White"
#     else :
#         start_turn ="Black"
#     # Prints initial board
#     print("\n========================")
#     print("\n" + start_turn + " to move\n")
#     print(board)
#     print("\n========================\n")

#     # Game info, AI moves, and user input for moves are selected here until game is over
#     while not resign:
#         move = chess.Move.null()
#         if ((board.turn == chess.WHITE and user_color == 1) or (board.turn == chess.BLACK and user_color == 2)) :
#             while not move in board.legal_moves:
#                 move = input("Please specify your move in SAN (Type resign to resign.): ")
#                 try :
#                     if (move.lower() == "resign") :
#                         resign = True
#                         break
#                     print()
#                 except ValueError :
#                     print()
#                 try : 
#                     move = board.parse_san(move)
#                 except ValueError:
#                     move = chess.Move.null()
#                     print("Invalid Input\n")
#                 if not move == chess.Move.null() and not move in board.legal_moves :
#                     print("Invalid Input\n")

#         # AI moves for easy mode
#         elif ai_difficulty == 1:
#             random = randint(0, board.legal_moves.count() - 1)
#             count = 0
#             for legal_move in board.legal_moves :
#                 if random == count :
#                     move = legal_move
#                     break
#                 else :
#                     count += 1

#         #AI moves for medium difficulty (minimax only) VERY SLOW
#         elif ai_difficulty == 2:
#             print("Computer thinking....\n")
#             total_moves_simulated = 0
#             move = getmove(input_depth)
#             print("Computer simulated " + str(total_moves_simulated) + " moves. Computer played " + board.san(move) + "\n")
#         #AI moves for hard difficulty (minimax alpha beta pruning) and library for openings of grandmasters
#         elif ai_difficulty == 3:
#             print("Computer thinking....\n")
#             total_moves_simulated = 0
#             try:
#                 move = chess.polyglot.MemoryMappedReader("human.bin").weighted_choice(board).move
#             except :
#                 move = getmove_alphabeta(input_depth, -1000000000, 1000000000)
#             print("Computer simulated " + str(total_moves_simulated) + " moves. Computer played " + board.san(move) + "\n")

#         # Pushes whatever move and continues the game. Also prints the board along with turn descriptions
#         if resign :
#             break
#         total_moves.append(board.san(move))
#         board.push(move)

#         # Checks if game is over
#         if (board.is_checkmate() or board.is_stalemate() or board.is_insufficient_material() or board.is_fivefold_repetition() or board.is_seventyfive_moves()) :
#             break
#         if (board.turn == chess.BLACK):
#             color = "Black's"
#         else :
#             color = "White's"
#         if ((board.turn == chess.BLACK and user_color == 2) or (board.turn == chess.WHITE and user_color == 1)):
#             ai_or_user = "(Your turn)"
#         else :
#             ai_or_user = "(Computer's turn)"
#         print(color + " turn to move " + ai_or_user + ".\n")
#         print(board)
#         print()
#         print(printmovelist())
        

#     # Handles the outcome of the game description
#     if resign :
#         winner = "The computer won..."
#     elif (board.outcome().winner and user_color == 1)or (not board.outcome().winner and user_color == 2):
#         winner = "You won!\n"
#         print(board)
#         print()
#     else :
#         winner = "The computer won...\n"
#         print(board)
#         print()
#     print(winner)
#     if not resign :
#         print(board.outcome().result())
