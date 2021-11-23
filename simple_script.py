from life import LifeBoard, SparseSetRules, SparseSetState

nx = 4
ny = 4

initial_state = {(1, 1)}

rules = SparseSetRules()
state = SparseSetState(initial_state)

print(state.to_dense(nx, ny))
