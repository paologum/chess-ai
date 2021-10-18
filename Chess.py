import chess
from random import randint

#initializes all the variables
board = chess.Board()
pick_color = False
resign = False
pick_difficulty = False
print("Welcome to chess!")

#pick AI difficulty
while not pick_difficulty:
    try:
        ai_difficulty = int(input("Which difficulty would you like to play against?\n1. Easy\n2. Medium\n3. Hard\n"))
        pick_difficulty = True
    except ValueError:
        print("Unfortunately, that is not an option, please pick again.")
        pick_difficulty = False

#picks color of user
while not pick_color:
    try:
        user_color = int(input("Which color would you like to play?\n1. White\n2. Black\n"))
        pick_color = True
    except ValueError:
        print("Unfortunately, that is not an option, please pick again.")
        pick_color = False
print(board)

#game info, AI moves, and user input for moves are selected here until game is over
while not board.is_checkmate() or not board.is_stalemate() or not board.is_insufficient_material() or resign:
    move = chess.Move.null()
    if ((board.turn == chess.WHITE and user_color == 1) or (board.turn == chess.BLACK and user_color == 2)) :
        while not move in board.legal_moves:
            move = input("Please specify your move in SAN: ")
            try : 
                move = board.parse_san(move)
            except ValueError:
                move = chess.Move.null()
                print("Invalid Input")
            if not move == chess.Move.null() and not move in board.legal_moves :
                print("Invalid Input")
    elif ai_difficulty == 1:
        #TODO legal moves that work with pins, checks, etc
        random = randint(0, board.legal_moves.count())
        count = 0
        for legal_move in board.legal_moves :
            if random == count :
                move = legal_move
                break
            else :
                count += 1
    elif ai_difficulty == 2:
        print("difficulty medium")
        
# pushes whatever move and continues the game
    board.push(move)
    print(board)
    if (((board.turn == chess.BLACK and user_color == 1) or (board.turn == chess.WHITE and user_color == 2) and input("Resign? Type Yes or No.".lower()) == "no")) :
        resign = True