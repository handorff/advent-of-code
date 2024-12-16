import heapq
from collections import defaultdict
INPUT_FILE = "16.in"

def parse_input(input_str):
  lines = input_str.split("\n")
  bounds = (len(lines), len(lines[0]))
  walls = set()
  start = None
  end = None

  for i, line in enumerate(lines):
    for j, c in enumerate(line):
      if c == "#":
        walls.add((i, j))

      if c == "S":
        assert start is None
        start = (i, j)

      if c == "E":
        assert end is None
        end = (i, j)

  return walls, bounds, start, end


def print_map(walls, bounds, start, end, tiles=[]):
  for i in range(bounds[0]):
    line = ''
    for j in range(bounds[1]):
      if (i, j) in walls:
        line += "#"
      elif (i, j) == start:
        line += "S"
      elif (i, j) == end:
        line += "E"
      elif (i, j) in tiles:
        line += "O"
      else:
        line += "."
    print(line)


def rotate_cw(direction):
  return {
    (0, 1):  (1, 0),
    (1, 0): (0, -1),
    (0, -1): (-1, 0),
    (-1, 0): (0, 1)
  }[direction]


def rotate_ccw(direction):
  return {
    (1, 0): (0, 1),
    (0, 1): (-1, 0),
    (-1, 0): (0, -1),
    (0, -1): (1, 0)
  }[direction]


def find_min_path(walls, bounds, start, end):
  q = [(0, start, (0, 1))]
  visited = set()

  while len(q) > 0:
    cost, pos, direction = heapq.heappop(q)

    if (pos, direction) in visited:
      continue

    visited.add((pos, direction))

    i, j = pos
    di, dj = direction

    if pos == end:
      return cost

    # step
    new_pos = (i + di, j + dj)
    if new_pos not in walls and (new_pos, direction) not in visited:
      new_cost = 1 + cost
      heapq.heappush(q, (new_cost, new_pos, direction))

    # rotate
    heapq.heappush(q, (cost + 1000, pos, rotate_cw(direction)))
    heapq.heappush(q, (cost + 1000, pos, rotate_ccw(direction)))


def a():
  with open(INPUT_FILE) as f:
    walls, bounds, start, end = parse_input(f.read())
    # print_map(walls, bounds, start, end)
    print(find_min_path(walls, bounds, start, end))


def get_path_tiles(parents, start, end):
  tiles = set()
  q = [elt for elt in parents.keys() if elt[0] == end]

  while len(q) > 0:
    p = q.pop(0)
    tiles.add(p[0])

    for node in parents[p]:
      if node not in q:
        q.append(node)

  return tiles


def update_parents(parents, parent_costs, original, new):
  cost, pos, direction = original
  new_cost, new_pos, new_direction = new

  if (new_pos, new_direction) in parent_costs:
    if parent_costs[(new_pos, new_direction)] == new_cost:
      parents[(new_pos, new_direction)].append((pos, direction))
    elif parent_costs[(new_pos, new_direction)] > new_cost:
      parents[(new_pos, new_direction)] = [(pos, direction)]
      parent_costs[(new_pos, new_direction)] = new_cost
  else:
    parent_costs[(new_pos, new_direction)] = new_cost
    parents[(new_pos, new_direction)].append((pos, direction))

  return parents, parent_costs


def find_min_path_tiles(walls, bounds, start, end):
  q = [(0, start, (0, 1))]
  visited = set()
  parents = defaultdict(list)
  parents[(start, (0, 1))] = []
  parent_costs = {(start, (0, 1)): 0}

  while len(q) > 0:
    original = heapq.heappop(q)
    cost, pos, direction = original

    if (pos, direction) in visited:
      continue

    visited.add((pos, direction))

    i, j = pos
    di, dj = direction

    if pos == end:
      q = [elt for elt in parents.keys() if elt[0] == end]
      return get_path_tiles(parents, start, end)

    # step
    new_pos = (i + di, j + dj)
    if new_pos not in walls:
      new = (cost + 1, new_pos, direction)
      parents, parent_costs = update_parents(parents, parent_costs, original, new)
      heapq.heappush(q, new)

    # rotate cw
    new = (cost + 1000, pos, rotate_cw(direction))
    parents, parent_costs = update_parents(parents, parent_costs, original, new)
    heapq.heappush(q, new)

    # rotate cw
    new = (cost + 1000, pos, rotate_ccw(direction))
    parents, parent_costs = update_parents(parents, parent_costs, original, new)
    heapq.heappush(q, new)


def b():
  with open(INPUT_FILE) as f:
    walls, bounds, start, end = parse_input(f.read())
    tiles = find_min_path_tiles(walls, bounds, start, end)
    print(len(tiles))
    # print_map(walls, bounds, start, end, tiles)
    

if __name__ == '__main__':
  a()
  b()