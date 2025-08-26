from queue import PriorityQueue
import tkinter as tk
from tkinter import messagebox
import random

class PuzzleGame:
    def __init__(self, root):
        self.root = root
        self.root.title("8-Puzzle Game")
        self.default_board = self.generate_random_board()
        self.board = []
        self.buttons = []
        self.create_ui()

    def generate_random_board(self):
        board = list(range(9))
        random.shuffle(board)
        return board

    def create_ui(self):
        self.input_label = tk.Label(self.root, text="Nhập dãy số (0-8, cách nhau bằng dấu phẩy, để trống để dùng mặc định):", font=("Arial", 12))
        self.input_label.grid(row=0, column=0, columnspan=3)

        self.input_entry = tk.Entry(self.root, width=40)
        self.input_entry.grid(row=1, column=0, columnspan=3)

        self.start_button = tk.Button(self.root, text="Bắt đầu trò chơi", command=self.start_game)
        self.start_button.grid(row=2, column=0, columnspan=1)

        self.solve_button = tk.Button(self.root, text="Tự giải", command=self.solve_puzzle)
        self.solve_button.grid(row=2, column=1, columnspan=1)

        self.grid_frame = tk.Frame(self.root)
        self.grid_frame.grid(row=3, column=0, columnspan=3)

        self.status_label = tk.Label(self.root, text="", font=("Arial", 14), fg="blue")
        self.status_label.grid(row=4, column=0, columnspan=3)

    def start_game(self):
        user_input = self.input_entry.get()
        self.board = self.parse_input(user_input)
        if not self.board:
            return
        self.create_grid()

    def parse_input(self, input_str):
        if not input_str.strip():
            return [self.default_board[i:i + 3] for i in range(0, 9, 3)]

        try:
            numbers = list(map(int, input_str.split(',')))
            if len(numbers) != 9 or sorted(numbers) != list(range(9)):
                raise ValueError("Dãy số không hợp lệ!")
            return [numbers[i:i + 3] for i in range(0, 9, 3)]
        except ValueError:
            messagebox.showerror("Lỗi", "Vui lòng nhập đúng dãy số từ 0 đến 8, không trùng lặp!")
            return None

    def create_grid(self):
        for widget in self.grid_frame.winfo_children():
            widget.destroy()

        self.buttons = []
        for i in range(3):
            row_buttons = []
            for j in range(3):
                button = tk.Button(self.grid_frame, text=str(self.board[i][j]) if self.board[i][j] != 0 else "",
                                   font=("Arial", 20), width=4, height=2,
                                   command=lambda x=i, y=j: self.move_tile(x, y))
                button.grid(row=i, column=j)
                row_buttons.append(button)
            self.buttons.append(row_buttons)

        self.status_label.config(text="Hãy sắp xếp các ô số!")

    def move_tile(self, x, y):
        blank_x, blank_y = self.find_blank()
        if abs(blank_x - x) + abs(blank_y - y) == 1:
            self.board[blank_x][blank_y], self.board[x][y] = self.board[x][y], self.board[blank_x][blank_y]
            self.update_ui()
            if self.check_win():
                self.status_label.config(text="Chúc mừng! Bạn đã thắng!", fg="green")

    def find_blank(self):
        for i in range(3):
            for j in range(3):
                if self.board[i][j] == 0:
                    return i, j

    def update_ui(self):
        for i in range(3):
            for j in range(3):
                self.buttons[i][j].config(text=str(self.board[i][j]) if self.board[i][j] != 0 else "")

    def check_win(self):
        target = list(range(1, 9)) + [0]
        flat_board = [self.board[i][j] for i in range(3) for j in range(3)]
        return flat_board == target

    def solve_puzzle(self):
        solution = self.a_star(self.board)
        if solution:
            self.animate_solution(solution)
        else:
            messagebox.showerror("Lỗi", "Không thể giải được trạng thái hiện tại!")

    def a_star(self, start):
        def heuristic(state):
            goal = list(range(1, 9)) + [0]
            flat_state = [state[i][j] for i in range(3) for j in range(3)]
            return sum(abs(flat_state.index(i) // 3 - goal.index(i) // 3) +
                       abs(flat_state.index(i) % 3 - goal.index(i) % 3) for i in range(1, 9))

        def neighbors(state):
            blank_x, blank_y = [(i, j) for i in range(3) for j in range(3) if state[i][j] == 0][0]
            directions = [(-1, 0), (1, 0), (0, -1), (0, 1)]
            for dx, dy in directions:
                new_x, new_y = blank_x + dx, blank_y + dy
                if 0 <= new_x < 3 and 0 <= new_y < 3:
                    new_state = [row[:] for row in state]
                    new_state[blank_x][blank_y], new_state[new_x][new_y] = new_state[new_x][new_y], new_state[blank_x][blank_y]
                    yield new_state

        start_flat = [start[i][j] for i in range(3) for j in range(3)]
        goal_flat = list(range(1, 9)) + [0]
        if start_flat == goal_flat:
            return []

        open_set = PriorityQueue()
        open_set.put((0, start, []))
        visited = set()

        while not open_set.empty():
            _, current, path = open_set.get()
            if [current[i][j] for i in range(3) for j in range(3)] == goal_flat:
                return path
            visited.add(tuple(tuple(row) for row in current))

            for neighbor in neighbors(current):
                if tuple(tuple(row) for row in neighbor) not in visited:
                    new_path = path + [neighbor]
                    priority = len(new_path) + heuristic(neighbor)
                    open_set.put((priority, neighbor, new_path))

        return None

    def animate_solution(self, solution):
        for step in solution:
            self.board = step
            self.update_ui()
            self.root.update()
            self.root.after(1000)

# Tạo cửa sổ ứng dụng
root = tk.Tk()
game = PuzzleGame(root)
root.mainloop()
