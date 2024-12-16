from collections import defaultdict

INPUT_FILE = "08.in"


def get_antennas(lines):
  antennas = defaultdict(set)

  for i, line in enumerate(lines):
    for j, c in enumerate(line):
      if c != ".":
        antennas[c].add((i, j))

  return antennas

def get_frequency_antinodes(antennas):
  antinodes = set()
  for x1, y1 in antennas:
    for x2, y2 in antennas:
      if not (x1 == x2 and y1 == y2):
        dx = x1 - x2
        dy = y1 - y2
        antinode = (x1 + dx, y1 + dy)
        antinodes.add(antinode)
  return antinodes

def in_bounds(p, bounds):
  x, y = p
  if x < 0 or y < 0:
    return False
  if x >= bounds[0] or y >= bounds[1]:
    return False
  return True


def a():
  with open(INPUT_FILE) as f:
    lines = f.read().split("\n")
    antennas = get_antennas(lines)
    bounds = (len(lines), len(lines[0]))

    antinodes = set()
    for c in antennas:
      antinodes |= get_frequency_antinodes(antennas[c])

    antinodes = [p for p in antinodes if in_bounds(p, bounds)]
    print(len(antinodes))


def get_frequency_antinodes_b(antennas, bounds):
  antinodes = set()
  for x1, y1 in antennas:
    for x2, y2 in antennas:
      if not (x1 == x2 and y1 == y2):
        dx = x1 - x2
        dy = y1 - y2
        x = x1
        y = y1
        while in_bounds((x, y), bounds):
          antinodes.add((x, y))
          x += dx
          y += dy

  return antinodes

def b():
  with open(INPUT_FILE) as f:
    lines = f.read().split("\n")
    antennas = get_antennas(lines)
    bounds = (len(lines), len(lines[0]))

    antinodes = set()
    for c in antennas:
      antinodes |= get_frequency_antinodes_b(antennas[c], bounds)

    print(len(antinodes))

if __name__ == '__main__':
  a()
  b()