INPUT_FILE = "10.in"

def parse_line(line):
  return list(map(int, list(line)))

def in_bounds(i, j, bounds):
  return i >= 0 and j >= 0 and i < bounds[0] and j < bounds[1]

def neighbor_indexes(i, j, bounds):
  all_neighbors = [(i + 1, j), (i - 1, j), (i, j + 1), (i, j - 1)]
  return [(x, y) for x, y in all_neighbors if in_bounds(x, y, bounds)]

def get_score(parsed, i, j):
  assert parsed[i][j] == 0

  bounds = (len(parsed), len(parsed[0]))

  reachable_n = {(i, j)}
  for n in range(1, 10):
    next_reachable_n = set()

    for x, y in reachable_n:
      for r, c in neighbor_indexes(x, y, bounds):
        if parsed[r][c] == n:
          next_reachable_n.add((r, c))
    reachable_n = next_reachable_n

  return len(reachable_n)

def get_score_b(parsed, i, j):
  assert parsed[i][j] == 0

  bounds = (len(parsed), len(parsed[0]))

  reachable_n = [(i, j)]
  for n in range(1, 10):
    next_reachable_n = []

    for x, y in reachable_n:
      for r, c in neighbor_indexes(x, y, bounds):
        if parsed[r][c] == n:
          next_reachable_n.append((r, c))
    reachable_n = next_reachable_n

  return len(reachable_n)


def b():
  with open(INPUT_FILE) as f:
    lines = f.read().split("\n")
    parsed = [parse_line(line) for line in lines]

    total = 0
    for i, line in enumerate(parsed):
      for j, n in enumerate(line):
        if n == 0:
          total += get_score_b(parsed, i, j)

    print(total) 

def a():
  with open(INPUT_FILE) as f:
    lines = f.read().split("\n")
    parsed = [parse_line(line) for line in lines]

    total = 0
    for i, line in enumerate(parsed):
      for j, n in enumerate(line):
        if n == 0:
          total += get_score(parsed, i, j)

    print(total)


if __name__ == '__main__':
  a()
  b()