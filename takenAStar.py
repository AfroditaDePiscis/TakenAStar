from queue import PriorityQueue
import numpy as np
import random


def shuffle(matriz):
    for _ in range(40):
        i, j = np.argwhere(matriz == 0)[0]
        moves = []
        if i > 0:
            moves.append((-1, 0))  
        if i < 3:
            moves.append((1, 0))  
        if j > 0:
            moves.append((0, -1))  
        if j < 3:
            moves.append((0, 1)) 
        di, dj = random.choice(moves)
        new_i, new_j = i+di, j+dj
        matriz[i][j], matriz[new_i][new_j] = matriz[new_i][new_j], matriz[i][j]
    return matriz

matriz = np.array([[1, 2, 3, 4], [5, 6, 7, 8], [9, 10, 11, 12], [13, 14, 15, 0]])
boardStart = shuffle(matriz)


print(boardStart)


class Puzzle:
    def __init__(self, board):
        self.board = board
        self.cost = 0
    
    def __lt__(self, other):
        return self.cost < other.cost
    
    def __eq__(self, other):
        return np.array_equal(self.board, other.board)
    
    def __hash__(self):
        return hash(str(self.board))
    
    def get_blank_pos(self):
        for i in range(4):
            for j in range(4):
                if self.board[i][j] == 0:
                    return i, j
    
    def get_neighbors(self):
        i, j = self.get_blank_pos()
        neighbors = []
        if i > 0:
            new_board = np.copy(self.board)
            new_board[i][j], new_board[i-1][j] = new_board[i-1][j], new_board[i][j]
            neighbors.append(Puzzle(new_board))
        if i < 3:
            new_board = np.copy(self.board)
            new_board[i][j], new_board[i+1][j] = new_board[i+1][j], new_board[i][j]
            neighbors.append(Puzzle(new_board))
        if j > 0:
            new_board = np.copy(self.board)
            new_board[i][j], new_board[i][j-1] = new_board[i][j-1], new_board[i][j]
            neighbors.append(Puzzle(new_board))
        if j < 3:
            new_board = np.copy(self.board)
            new_board[i][j], new_board[i][j+1] = new_board[i][j+1], new_board[i][j]
            neighbors.append(Puzzle(new_board))
        return neighbors
    
    def manhattan_distance(self):
        distance = 0
        for i in range(4):
            for j in range(4):
                if self.board[i][j] != 0:
                    x, y = divmod(self.board[i][j]-1, 4)
                    distance += abs(x-i) + abs(y-j)
        return distance
    
def solve(board):
    start_state = Puzzle(board)
    goal_state = Puzzle(np.array([[1, 2, 3, 4], [5, 6, 7, 8], [9, 10, 11, 12], [13, 14, 15, 0]]))
    open_set = PriorityQueue()
    open_set.put(start_state)
    closed_set = set()
    max_steps = 10000 # número máximo de pasos permitidos
    steps = 0 # contador de pasos
    while not open_set.empty() and steps < max_steps:
        current_state = open_set.get()
        if current_state == goal_state:
            return current_state.cost
        closed_set.add(current_state)
        for neighbor in current_state.get_neighbors():
            if neighbor in closed_set:
                continue
            neighbor.cost = current_state.cost + 1 + neighbor.manhattan_distance()
            open_set.put(neighbor)
        steps += 1 # incrementa el contador de pasos
    print("No se encontró solución después de", max_steps, "pasos.")
    return None
    
board = boardStart
steps = solve(board)
print("Numero de paso: " + str(steps))
