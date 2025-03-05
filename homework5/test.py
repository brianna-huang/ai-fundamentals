import homework5

# path = '/Users/briannahuang/Desktop/cis 521/homework5/homework5_sudoku/easy.txt'
# print(homework5.read_board(path))

sudoku = homework5.Sudoku(homework5.read_board("/Users/briannahuang/Desktop/cis 521/homework5/homework5_sudoku/easy.txt"))

# for col in [0, 1, 4]:
#     removed = sudoku.remove_inconsistent_values((0, 3), (0, col))
#     print(removed, sudoku.get_values((0, 3)))

to_remove = set()
xi_domain = {1,2,3}
xj_domain = {3}
for x in xi_domain:
    if not any([x != y for y in xj_domain]):
    # if x == y:
        to_remove.add(x)
xi_domain -= to_remove
print(xi_domain)