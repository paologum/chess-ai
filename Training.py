import chess
import numpy as np
import random
from stockfish import Stockfish

piece_list = ["R", "N", "B", "Q", "P"]

stockfish = Stockfish(r"C:\Users\sunny\Downloads\stockfish_14.1_win_x64_avx2\stockfish_14.1_win_x64_avx2\stockfish_14.1_win_x64_avx2",
parameters = {
    "Write Debug Log": "false",
    "Contempt": 0,
    "Min Split Depth": 0,
    "Threads": 2,
    "Ponder": "false",
    "Hash": 16,
    "MultiPV": 1,
    "Skill Level": 25,
    "Move Overhead": 30,
    "Minimum Thinking Time": 20,
    "Slow Mover": 80,
    "UCI_Chess960": "false",
}
)
 

def create_random_board() :
	random_integer = random.randint(10,120)
	init_board = chess.Board()
	for i in range(random_integer) :
		if init_board.legal_moves.count() == 0 :
			return init_board
		random_move = random.randint(0, init_board.legal_moves.count() - 1)
		count = 0
		for move in init_board.legal_moves :
			if count == random_move:	
				init_board.push(move)
				break
			count += 1
	return init_board

piece_dict  = {
	"0" : "k",
	"1" : "p",
	"2" : "n",
	"3" : "b",
	"4" : "q",
	"5" : "r",
	"6" : "K",
	"7" : "P",
	"8" : "N",
	"9" : "B",
	"10" : "Q",
	"11" : "R"
}
training_board = []
training_answers = []
for i in range(10000):
	random_board = create_random_board()
	random_fen = random_board.fen()
	print(random_fen)
	stockfish.set_fen_position(random_fen)
	rank_strings = random_fen.split('/')
	eight_rank = rank_strings[7].split(' ')
	rank_strings[7] = eight_rank[0]
	final_array = []
	for i in range(12):
		piece_array = []
		for rank in rank_strings:
			piece_array_rank = []
			for piece in rank :
				try :
					skip = int(piece)
					for skipped_number in range(skip) :
						piece_array_rank.append(0)
				except :	
					if piece == piece_dict.get(str(i)) :
						piece_array_rank.append(1)
					else :
						piece_array_rank.append(0)
			piece_array.append(piece_array_rank)
		final_array.append(piece_array)
	numpy_array = np.array(final_array)
	type = stockfish.get_evaluation().get('type')
	value = stockfish.get_evaluation().get('value')
	training_answers.append(value)
	training_board.append(final_array)
	if (type == 'mate') :
		value *= 1000000
np.save('training_boards', training_board)
np.save('traning_board_key', training_answers)
np.set_printoptions(threshold=np.inf)
my_array = np.load('training_boards.npy', encoding='bytes')
print(my_array)






