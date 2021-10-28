import chess
import chess.polyglot
import chess.pgn
from random import randint

# Initializes all the variables
board = chess.Board()
total_moves = []
pick_color = False
resign = False
pick_difficulty = False
total_moves_simulated = int(0)
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
    count = int(1)
    move_list = ""
    for m in total_moves :
        if count % 2 == 1:
            move_list += str(int(count / 2) + 1) + ". "
        move_list += m + " "
        if count % 20 == 0 :
            move_list += "\n"
        count += 1
    return move_list + "\n\n========================\n"


# Evaluation function implemented from https://medium.com/dscvitpune/lets-create-a-chess-ai-8542a12afef
def evaluate():
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
def minimax(depth):
    if depth == 0 :
        return evaluate()
    if board.turn :
        max_evaluation = -1000000000
        for some_move in board.legal_moves :
            board.push(some_move)
            evaluation = minimax(depth - 1)
            board.pop()
            max_evaluation = max(max_evaluation, evaluation)
        return max_evaluation
    else :
        min_evaluation = 100000000000
        for some_move in board.legal_moves :
            board.push(some_move)
            evaluation = minimax(depth - 1)
            board.pop()
            min_evaluation = min(evaluation, min_evaluation)
        return min_evaluation

#Get a move from the minimax alogrithim
def getmove(depth):
    best_move = chess.Move.null()
    if board.turn :
        best_evaluation = -999999999
    else :
        best_evaluation = 999999999
    for some_move in board.legal_moves:
        board.push(some_move)
        evaluation = minimax(depth - 1)
        board.pop()
        if board.turn and evaluation > best_evaluation:
            best_evaluation = evaluation
            best_move = some_move
        elif not board.turn and evaluation < best_evaluation :
            best_evaluation = evaluation
            best_move = some_move
    return best_move

#Applies minimax with an alpha beta pruning
def alphabeta(depth, alpha, beta) :
    if depth == 0 :
        return evaluate()
    if board.turn :
        max_evaluation = -1000000000
        for some_move in board.legal_moves :
            board.push(some_move)
            evaluation = alphabeta(depth - 1, alpha, beta)
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
            evaluation = alphabeta(depth - 1, alpha, beta)
            beta = min(evaluation, beta)
            board.pop()
            min_evaluation = min(evaluation, min_evaluation)
            if beta <= alpha :
                break
        return min_evaluation

#Get a move from the minimax alogrithim with alpha beta pruning
def getmove_alphabeta(depth, alpha, beta):
    best_move = chess.Move.null()
    if board.turn :
        best_evaluation = -999999999
    else :
        best_evaluation = 999999999
    for some_move in board.legal_moves:
        board.push(some_move)
        evaluation = alphabeta(depth - 1, alpha, beta)
        board.pop()
        if board.turn and evaluation > best_evaluation:
            best_evaluation = evaluation
            best_move = some_move
        elif not board.turn and evaluation < best_evaluation :
            best_evaluation = evaluation
            best_move = some_move
    return best_move


print("Welcome to chess!")
while True:
    try :
        menu_option = int(input("\nPick one of the three options.\n1. Play a game against an AI\n2. Play a game against an AI starting from a PGN file.\n"))
        if (menu_option > 0 and menu_option < 3) :
            break
        else :
            print("\nInvalid Value, Try Again")
    except ValueError:
        print("\nInvalid Value, Try Again")
        menu_option = 0
if (menu_option == 1 or menu_option == 2) :
    if (menu_option == 2) :
        need_new_board = False
        while (not need_new_board) :
            try : 
                file_name = (input("\nWhat is the file name of the PGN? (Do not input the added file extension and make sure the file is in the PGN folder): "))
                pgn = open("PGN/" + file_name + ".pgn")
                parsed_game = chess.pgn.read_game(pgn)
                for some_move in parsed_game.mainline_moves():
                    total_moves.append(board.san(some_move))
                    board.push(some_move)
                need_new_board = True
            except (FileNotFoundError, OSError):
                print("\nInvalid PGN, try again")
                need_new_board = False
    while not pick_difficulty:
        try:
            ai_difficulty = int(input("Which difficulty would you like to play against?\n1. Easy\n2. Medium\n3. Hard\n"))
            if ai_difficulty < 1 or ai_difficulty > 3 :
                print("\nUnfortunately, that is not an option, please pick again.\n")
                pick_difficulty = False
            else :
                pick_difficulty = True
        except ValueError as e:
            print("\nUnfortunately, that is not an option, please pick again.\n")
            pick_difficulty = False
        

    # Picks color of user
    while not pick_color:
        try:
            user_color = int(input("\nWhich color would you like to play?\n1. White\n2. Black\n"))
            if (user_color != 1 and user_color != 2) :
                print("\nUnfortunately, that is not an option, please pick again.")
                pick_color = False
            else :
                pick_color = True
        except ValueError:
            print("\nUnfortunately, that is not an option, please pick again.")
            pick_color = False

    # Picks depth
    if ai_difficulty == 2 or ai_difficulty == 3:
        while True:
            try:
                input_depth = int(input("\nTo which depth would you like the computer to think to?\n"))
                if (input_depth > 0) :
                    break
                else:
                    print("\nUnfortunately, that is not an integer, please pick again.")
            except ValueError:
                print("\nUnfortunately, that is not an integer, please pick again.")

    if (board.turn) :
        start_turn = "White"
    else :
        start_turn ="Black"
    # Prints initial board
    print("\n========================")
    print("\n" + start_turn + " to move\n")
    print(board)
    print("\n========================\n")

    # Game info, AI moves, and user input for moves are selected here until game is over
    while not resign:
        move = chess.Move.null()
        if ((board.turn == chess.WHITE and user_color == 1) or (board.turn == chess.BLACK and user_color == 2)) :
            while not move in board.legal_moves:
                move = input("Please specify your move in SAN (Type resign to resign.): ")
                try :
                    if (move.lower() == "resign") :
                        resign = True
                        break
                    print()
                except ValueError :
                    print()
                try : 
                    move = board.parse_san(move)
                except ValueError:
                    move = chess.Move.null()
                    print("Invalid Input\n")
                if not move == chess.Move.null() and not move in board.legal_moves :
                    print("Invalid Input\n")

        # AI moves for easy mode
        elif ai_difficulty == 1:
            random = randint(0, board.legal_moves.count() - 1)
            count = 0
            for legal_move in board.legal_moves :
                if random == count :
                    move = legal_move
                    break
                else :
                    count += 1

        #AI moves for medium difficulty (minimax only) VERY SLOW
        elif ai_difficulty == 2:
            print("Computer thinking....\n")
            total_moves_simulated = 0
            move = getmove(input_depth)
            print("Computer simulated " + str(total_moves_simulated) + " moves. Computer played " + board.san(move) + "\n")
        #AI moves for hard difficulty (minimax alpha beta pruning) and library for openings of grandmasters
        elif ai_difficulty == 3:
            print("Computer thinking....\n")
            total_moves_simulated = 0
            try:
                move = chess.polyglot.MemoryMappedReader("human.bin").weighted_choice(board).move
            except :
                move = getmove_alphabeta(input_depth, -1000000000, 1000000000)
            print("Computer simulated " + str(total_moves_simulated) + " moves. Computer played " + board.san(move) + "\n")

        # Pushes whatever move and continues the game. Also prints the board along with turn descriptions
        if resign :
            break
        total_moves.append(board.san(move))
        board.push(move)

        # Checks if game is over
        if (board.is_checkmate() or board.is_stalemate() or board.is_insufficient_material() or board.is_fivefold_repetition() or board.is_seventyfive_moves()) :
            break
        if (board.turn == chess.BLACK):
            color = "Black's"
        else :
            color = "White's"
        if ((board.turn == chess.BLACK and user_color == 2) or (board.turn == chess.WHITE and user_color == 1)):
            ai_or_user = "(Your turn)"
        else :
            ai_or_user = "(Computer's turn)"
        print(color + " turn to move " + ai_or_user + ".\n")
        print(board)
        print()
        print(printmovelist())
        

    # Handles the outcome of the game description
    if resign :
        winner = "The computer won..."
    elif (board.outcome().winner and user_color == 1)or (not board.outcome().winner and user_color == 2):
        winner = "You won!\n"
        print(board)
        print()
    else :
        winner = "The computer won...\n"
        print(board)
        print()
    print(winner)
    if not resign :
        print(board.outcome().result())