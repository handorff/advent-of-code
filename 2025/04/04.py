INPUT_FILE = "04.in"

NEIGHBORS = [
  (-1, -1),
  (-1, 0),
  (-1, 1),
  (0, -1),
  (0, 1),
  (1, -1),
  (1, 0),
  (1, 1),
]

def get_neighbor_indexes(r, c, num_rows, num_cols):
  result = []
  for (dr, dc) in NEIGHBORS:
    if r + dr >= 0 and r + dr < num_rows and c + dc >= 0 and c + dc < num_cols:
      result.append((r + dr, c + dc))

  return result

def get_neighbors(r, c, grid):
  return [grid[nr][nc] for nr, nc in get_neighbor_indexes(r, c, len(grid), len(grid[0]))]
    


def a():
  with open(INPUT_FILE) as f:
    grid = f.read().split("\n")
    
    count = 0
    for r, row in enumerate(grid):
      for c, char in enumerate(row):
        if char == '@':
          if get_neighbors(r, c, grid).count('@') < 4:
            count += 1

    print(count)


def get_neighboring_roll_count(r, c, num_rows, num_cols, paper_locations):
  return sum(1 if n in paper_locations else 0 for n in get_neighbor_indexes(r, c, num_rows, num_cols))


def b():
  with open(INPUT_FILE) as f:
    grid = f.read().split("\n")
    num_rows = len(grid)
    num_cols = len(grid[0])

    paper_locations = set()
    for r, row in enumerate(grid):
      for c, char in enumerate(row):
        if char == '@':
          paper_locations.add((r, c))

    count = 0


    while True:
      accessible_rolls = set()
      for r in range(num_rows):
        for c in range(num_cols):
          if (r, c) in paper_locations:
            if get_neighboring_roll_count(r, c, num_rows, num_cols, paper_locations) < 4:
              accessible_rolls.add((r, c))

      if len(accessible_rolls) == 0:
        break

      count += len(accessible_rolls)
      paper_locations -= accessible_rolls

    print(count)


if __name__ == '__main__':
  a()
  b()