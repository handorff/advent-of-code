import time
from collections import defaultdict
from itertools import permutations
INPUT_FILE = "20.in"

def parse_input(input_str):
  lines = input_str.split("\n")

  bounds = (len(lines), len(lines[0]))

  walls = set()
  start = None
  end = None
  for i, line in enumerate(lines):
    for j, c in enumerate(line):
      if c == '#':
        walls.add((i, j))
      if c == 'S':
        start = (i, j)
      if c == 'E':
        end = (i, j)

  return walls, start, end, bounds



def in_bounds(i, j, bounds):
  return i >= 0 and j >= 0 and i < bounds[0] and j < bounds[1]

def neighbor_indexes(p, bounds):
  i, j = p
  all_neighbors = [(i + 1, j), (i - 1, j), (i, j + 1), (i, j - 1)]
  return [(x, y) for x, y in all_neighbors if in_bounds(x, y, bounds)]


def no_cheat_time(walls, start, end, bounds):
  q = [(0, start)]
  visited = set()

  while len(q) > 0:
    time, p = q.pop(0)

    if p in visited:
      continue
    visited.add(p)

    if p == end:
      return time

    for n in neighbor_indexes(p, bounds):
      if n == end:
        return time + 1

      if n not in walls and n not in visited:
        q.append((time + 1, n))

  assert False


def get_all_times(walls, node, bounds):
  q = [(0, node)]
  visited = {}

  while len(q) > 0:
    time, p = q.pop(0)

    if p in visited:
      continue
    visited[p] = time

    for n in neighbor_indexes(p, bounds):
      if n not in walls and n not in visited:
        q.append((time + 1, n))

  return visited


def get_all_possible_cheats(walls, bounds):
  cheats = []
  for w in walls:
    empty_neighbors = [n for n in neighbor_indexes(w, bounds) if n not in walls]
    for before, after in permutations(empty_neighbors, 2):
      cheats.append((before, after))

  return cheats


def cheat_time(cheat, starts, ends):
  cheat_before, cheat_end = cheat
  return 2 + starts[cheat_before] + ends[cheat_end]


def solve_a(walls, start, end, bounds):
  t = no_cheat_time(walls, start, end, bounds)
  cheats = get_all_possible_cheats(walls, bounds)

  starts = get_all_times(walls, start, bounds)
  ends = get_all_times(walls, end, bounds)

  saved = defaultdict(int)

  for i, cheat in enumerate(cheats):
    t2 = cheat_time(cheat, starts, ends)
    if t2 is not None and t2 + 100 <= t:
      saved[t - t2] += 1

  return sum(saved.values())


def a():
  with open(INPUT_FILE) as f:
    walls, start, end, bounds = parse_input(f.read())
    print(solve_a(walls, start, end, bounds))


def get_all_possible_cheats_b(bounds):
  cheats = []
  for i in range(bounds[0]):
    for j in range(bounds[1]):
      cheat_before = (i, j)
      for d in range(1, 21):
        for di in range(d + 1):
          dj = d - di
          for i2, j2 in [(i + di, j + dj), (i + di, j - dj), (i - di, j + dj), (i - di, j - dj)]:
            if in_bounds(i2, j2, bounds):
              cheat_after = (i2, j2)
              yield((cheat_before, cheat_after))


def dist(cheat):
  (i1, j1), (i2, j2) = cheat
  return abs(i1 - i2) + abs(j1 - j2)


def cheat_time_b(cheat, starts, ends):
  cheat_before, cheat_end = cheat
  if cheat_before not in starts or cheat_end not in ends:
    return None
  return starts[cheat_before] + dist(cheat) + ends[cheat_end]


def solve_b(walls, start, end, bounds):
  t = no_cheat_time(walls, start, end, bounds)
  cheats = get_all_possible_cheats_b(bounds)
  starts = get_all_times(walls, start, bounds)
  ends = get_all_times(walls, end, bounds)

  saved = defaultdict(set)
  for i, cheat in enumerate(cheats):
    t2 = cheat_time_b(cheat, starts, ends)
    if t2 is not None and t2 + 100 <= t:
      saved[t - t2].add(cheat)

  # return sorted((t, len(s)) for t, s in saved.items())
  return sum(len(s) for s in saved.values())


def b():
  with open(INPUT_FILE) as f:
    walls, start, end, bounds = parse_input(f.read())
    print(solve_b(walls, start, end, bounds))

if __name__ == '__main__':
  a()
  b()