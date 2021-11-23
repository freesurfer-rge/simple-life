from life import LifeBoard, SparseSetRules, SparseSetState

nx = 8
ny = 6

glider = {(2, 3), (3, 3), (4, 3), (4, 4), (3, 5)}


rules = SparseSetRules()
state = SparseSetState(glider)
board = LifeBoard(state, rules, nx, ny)

print(board.state.to_dense(nx, ny))

for _ in range(16):
    print("\n--\n")
    board.update()
    print(board.state.to_dense(nx, ny))
