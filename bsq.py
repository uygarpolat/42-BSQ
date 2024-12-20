from collections import defaultdict
import sys
import re

def is_in_grid(grid, loc):
    rows = len(grid)
    cols = len(grid[0])
    row = loc[0]
    col = loc[1]

    if 0 <= row < rows and 0 <= col < cols:
        return 1
    return 0

def print_grid(grid, key, value, full):
    rows = len(grid)
    cols = len(grid[0])
    for row in range(rows):
        for col in range(cols):
            if key[0] <= row < value + key[0] and key[1] <= col < value + key[1]:
                print(full, end="")
            else:
                print(grid[row][col], end="")
        print("")

def calculate_highest(tally):
    max_keys = [key for key, value in tally.items() if value == max(tally.values())]
    sorted_data = sorted(max_keys, key=lambda x: (x[0], x[1]))
    return sorted_data[0], tally[sorted_data[0]]
    
def free_of_obstacles(grid, old_loc, obstacle, offset):
    side = offset + 1
    rows = side
    cols = side
    for row in range(rows):
        for col in range(cols):
            if grid[old_loc[0] + row][old_loc[1] + col] == obstacle:
                return 0
    return 1

def calculate_two_lengths(grid, old_loc, obstacle, offset):
    length = 0

    new_loc_hori = (old_loc[0], old_loc[1] + 1 + offset)
    new_loc_vert = (old_loc[0] + 1 + offset, old_loc[1])

    if not is_in_grid(grid, new_loc_hori) or grid[new_loc_hori[0]][new_loc_hori[1]] == obstacle:
        return 0
    if not is_in_grid(grid, new_loc_vert) or grid[new_loc_vert[0]][new_loc_vert[1]] == obstacle:
        return 0

    if free_of_obstacles(grid, old_loc, obstacle, offset):
        length += 1 + calculate_two_lengths(grid, old_loc, obstacle, offset + 1)
    return length

def parse_file(file_path):
    with open(file_path, 'r') as file:
        instructions, part2 = file.read().split('\n', 1)
        grid = [line for line in part2.split('\n')]

    pattern = r'(\d+)(\D{3})'
    match = re.match(pattern, instructions)
    if match:
        line_count = match.group(1)
        empty = match.group(2)[0]
        obstacle = match.group(2)[1]
        full = match.group(2)[2]
    else:
        print("Incorrect map description.")
    return grid, line_count, obstacle, full

def main():
    file_path = sys.argv[1] if len(sys.argv) == 2 else "9x27.txt"
    grid, line_count, obstacle, full = parse_file(file_path)

    tally = defaultdict(int)

    rows = int(line_count)
    cols = len(grid[0])
    for row in range(rows):
        for col in range(cols):
            tally[(row,col)] = calculate_two_lengths(grid, (row, col), obstacle, 0)

    top_left_corner, side_length = calculate_highest(tally)
    
    print_grid(grid, top_left_corner, side_length, full)
    print(f"Grid size: {len(grid)}x{len(grid[0])}")
    print(f"Coordinates of top left corner of the square: {top_left_corner}")
    print(f"Side length: {side_length}")

if __name__ == "__main__":
    main()