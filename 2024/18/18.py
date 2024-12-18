INPUT_FILE = "18.in"
SIZE = 70
INITIAL_BYTES = 1024

def parse_line(line):
  [x, y] = line.split(",")
  return int(x), int(y)

def parse_input(input_str):
  lines = input_str.split("\n")
  return [parse_line(line) for line in lines]

def in_bounds(x, y):
  if x < 0 or y < 0:
    return False
  if x > SIZE or y > SIZE:
    return False
  return True

def neighbors(p):
  x, y = p
  all_neighbors = [
    (x + 1, y),
    (x - 1, y),
    (x, y + 1),
    (x, y - 1)
  ]
  return [(i, j) for i, j in all_neighbors if in_bounds(i, j)]

def find_path(walls, size):
  q = [(0, (0, 0))]

  visited = set()
  max_dist = 0

  while len(q) > 0:
    dist, p = q.pop(0)

    if p == (SIZE, SIZE):
      return dist

    visited.add(p)

    for neighbor in neighbors(p):
      if neighbor not in walls and neighbor not in visited and neighbor not in (elt[1] for elt in q):
        q.append((dist + 1, neighbor))


def a():
  with open(INPUT_FILE) as f:
    walls = parse_input(f.read())
    print(find_path(walls[:INITIAL_BYTES], SIZE))

def b():
  with open(INPUT_FILE) as f:
    walls = parse_input(f.read())

    good = INITIAL_BYTES
    bad = len(walls)
    while bad - good > 1:
      mid = (good + bad) // 2
      if find_path(walls[:mid], SIZE) is None: # no path
        bad = mid
      else:
        good = mid

    print(",".join(map(str, walls[bad - 1])))
    assert find_path(walls[:good], SIZE) is not None
    assert find_path(walls[:bad], SIZE) is None


if __name__ == '__main__':
  a()
  b()