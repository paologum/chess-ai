import chess
from random import randint

# Initializes all the variables
board = chess.Board()
total_moves = []
pick_color = False
resign = False
pick_difficulty = False
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

print("Welcome to chess!")

# Function to print move list
def print_move_list():
    count = int(1)
    move_list = ""
    for m in total_moves :
        if count % 2 == 1:
            move_list += str(int(count / 2) + 1) + ". "
        move_list += m + " "
        count += 1
    return move_list + "\n\n========================"


# Evaluation function implemented from https://medium.com/dscvitpune/lets-create-a-chess-ai-8542a12afef
def evaluate():
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
    if board.turn:
        return eval
    else:
        return -eval

# Pick AI difficulty
while not pick_difficulty:
    try:
        ai_difficulty = int(input("Which difficulty would you like to play against?\n1. Easy\n2. Medium\n3. Hard\n"))
        pick_difficulty = True
    except ValueError:
        print("\nUnfortunately, that is not an option, please pick again.")
        pick_difficulty = False

# Picks color of user
while not pick_color:
    try:
        user_color = int(input("\nWhich color would you like to play?\n1. White\n2. Black\n"))
        pick_color = True
    except ValueError:
        print("\nUnfortunately, that is not an option, please pick again.")
        pick_color = False

# Prints initial board
print("\n========================")
print("\nWhite to move\n")
print(board)
print("\n========================\n")

# Game info, AI moves, and user input for moves are selected here until game is over
while not resign:
    move = chess.Move.null()
    if ((board.turn == chess.WHITE and user_color == 1) or (board.turn == chess.BLACK and user_color == 2)) :
        while not move in board.legal_moves:
            move = input("Please specify your move in SAN: ")
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
        #TODO legal moves that work with pins, checks, etc
        random = randint(0, board.legal_moves.count() - 1)
        count = 0
        for legal_move in board.legal_moves :
            if random == count :
                move = legal_move
                break
            else :
                count += 1

    #TODO AI moves for medium difficulty (minimax and alpha beta pruning)
    elif ai_difficulty == 2:
        print("difficulty medium")

# Pushes whatever move and continues the game. Also prints the board along with turn descriptions
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
    print(color + " turn to move " + ai_or_user + "\n")
    print(board)
    print()
    print(print_move_list())
    if (((board.turn == chess.BLACK and user_color == 2) or (board.turn == chess.WHITE and user_color == 1) and input("Resign? Type Yes or No: ").lower() == "yes")) :
        print()
        resign = True
    else :
        print()

# Handles the outcome of the game description
if resign :
    winner = "The computer won..."
elif (board.outcome().winner and user_color == 1)or (not board.outcome().winner and user_color == 2):
    winner = "You won!"
else :
    winner = "The computer won..."
print(winner)
print(board.outcome().result())