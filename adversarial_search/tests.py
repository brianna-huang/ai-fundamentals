import homework4

g = homework4.create_dominoes_game(3, 3)
for m, new_g in g.successors(True):
    print(m, new_g.get_board())