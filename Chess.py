import chess
from random import randint

# Initializes all the variables
board = chess.Board()
total_moves = []
pick_color = False
resign = False
pick_difficulty = False
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