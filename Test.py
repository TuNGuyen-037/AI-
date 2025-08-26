import copy
from collections import deque
import time

# Kiểm tra xem trạng thái hiện tại có phải là trạng thái đích
def is_goal(state, goal):
    return state == goal

# Tìm vị trí ô trống (0) trong bảng
def find_zero(state):
    for i in range(len(state)):
        for j in range(len(state[i])):
            if state[i][j] == 0:
                return i, j

# Sinh các trạng thái con (các bước di chuyển hợp lệ)
def get_neighbors(state):
    neighbors = []
    x, y = find_zero(state)
    directions = [(-1, 0), (1, 0), (0, -1), (0, 1)]  # Lên, Xuống, Trái, Phải

    for dx, dy in directions:
        nx, ny = x + dx, y + dy
        if 0 <= nx < len(state) and 0 <= ny < len(state[0]):  # Kiểm tra biên
            new_state = copy.deepcopy(state)
            # Hoán đổi vị trí ô trống với ô kề
            new_state[x][y], new_state[nx][ny] = new_state[nx][ny], new_state[x][y]
            neighbors.append(new_state)

    return neighbors

# Thuật toán DFS
def dfs(start, goal):
    stack = [(start, [])]  # Ngăn xếp lưu (trạng thái hiện tại, đường đi)
    visited = set()  # Tập hợp để tránh lặp trạng thái

    while stack:
        current_state, path = stack.pop()
        state_tuple = tuple(tuple(row) for row in current_state)

        if state_tuple in visited:
            continue
        visited.add(state_tuple)

        if is_goal(current_state, goal):
            return path + [current_state]

        for neighbor in get_neighbors(current_state):
            stack.append((neighbor, path + [current_state]))

    return None  # Không tìm thấy lời giải

# Thuật toán BFS
def bfs(start, goal):
    queue = deque([(start, [])])  # Hàng đợi lưu (trạng thái hiện tại, đường đi)
    visited = set()

    while queue:
        current_state, path = queue.popleft()
        state_tuple = tuple(tuple(row) for row in current_state)

        if state_tuple in visited:
            continue
        visited.add(state_tuple)

        if is_goal(current_state, goal):
            return path + [current_state]

        for neighbor in get_neighbors(current_state):
            queue.append((neighbor, path + [current_state]))

    return None  # Không tìm thấy lời giải

# Hiển thị bảng
def print_board(state):
    for row in state:
        print(" ".join(map(str, row)))
    print()

# Hàm chính
def main():
    # Nhập trạng thái ban đầu và đích từ người dùng
    print("Nhập trạng thái ban đầu (9 số, cách nhau bởi khoảng trắng):")
    start = list(map(int, input().split()))
    print("Nhập trạng thái đích (9 số, cách nhau bởi khoảng trắng):")
    goal = list(map(int, input().split()))

    start = [start[:3], start[3:6], start[6:]]
    goal = [goal[:3], goal[3:6], goal[6:]]

    print("\nTrạng thái ban đầu:")
    print_board(start)

    print("Trạng thái đích:")
    print_board(goal)

    # Thực hiện DFS
    print("\nĐang giải bằng DFS...")
    start_time = time.time()
    dfs_solution = dfs(start, goal)
    dfs_time = time.time() - start_time

    if dfs_solution:
        print(f"Tìm thấy lời giải bằng DFS với {len(dfs_solution) - 1} bước:")
        for step in dfs_solution:
            print_board(step)
    else:
        print("DFS: Không tìm thấy lời giải.")
    print(f"Thời gian thực thi DFS: {dfs_time:.2f} giây\n")

    # Thực hiện BFS
    print("Đang giải bằng BFS...")
    start_time = time.time()
    bfs_solution = bfs(start, goal)
    bfs_time = time.time() - start_time

    if bfs_solution:
        print(f"Tìm thấy lời giải bằng BFS với {len(bfs_solution) - 1} bước:")
        for step in bfs_solution:
            print_board(step)
    else:
        print("BFS: Không tìm thấy lời giải.")
    print(f"Thời gian thực thi BFS: {bfs_time:.2f} giây\n")

    # So sánh hiệu quả
    print("So sánh kết quả:")
    print(f"- DFS: {len(dfs_solution) - 1 if dfs_solution else 'Không tìm thấy'} bước, {dfs_time:.2f} giây")
    print(f"- BFS: {len(bfs_solution) - 1 if bfs_solution else 'Không tìm thấy'} bước, {bfs_time:.2f} giây")

if __name__ == "__main__":
    main()
