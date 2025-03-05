import homework3

board = homework3.create_tile_puzzle(3, 3)
print(board.get_board())
board2 = board.copy()
print(board2.get_board())
board.perform_move('up')
print(board.get_board())
print(board2.get_board())