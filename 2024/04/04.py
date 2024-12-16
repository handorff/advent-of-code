INPUT_FILE = "04.in"

PATTERNS = [
  ((1, 0), (2, 0), (3, 0)),
  ((-1, 0), (-2, 0), (-3, 0)),
  ((0, 1), (0, 2), (0, 3)),
  ((0, -1), (0, -2), (0, -3)),
  ((1, 1), (2, 2), (3, 3)),
  ((1, -1), (2, -2), (3, -3)),
  ((-1, 1), (-2, 2), (-3, 3)),
  ((-1, -1), (-2, -2), (-3, -3))
]

def get(lines, i, j):
  if i < 0 or i >= len(lines):
    return ' '

  line = lines[i]
  if j < 0 or j >= len(line):
    return ' '

  return line[j]


def xmas_test(lines, i, j, pattern):
  (x1, y1), (x2, y2), (x3, y3) = pattern
  return get(lines, i + x1, j + y1) == "M" and get(lines, i + x2, j + y2) == "A" and get(lines, i + x3, j + y3) == "S"


# number of occurrences of XMAS starting at i, j
def xmas_count_at(lines, i, j, c):
  if c != "X":
    return 0

  count = 0
  for pattern in PATTERNS:
    if xmas_test(lines, i, j, pattern):
      count += 1
  return count


# in each pattern, each group must be one M and one S in some order
PATTERNS_B = [
  # (((1, 0), (-1, 0)), ((0, 1), (0, -1))) # oops can't be horizontal/vertical
  (((1, 1), (-1, -1)), ((1, -1), (-1, 1)))
]

def x_mas_test_pattern(lines, i, j, pattern):
  for group in pattern:
    (x1, y1), (x2, y2) = group
    group_chars = [get(lines, i + x1, j + y1), get(lines, i + x2, j + y2)]
    if set(group_chars) != {"M", "S"}:
      return False
  return True


# returns true if there is an X-MAS centered at i, j
def x_mas_test(lines, i, j, c):
  if c != "A":
    return False

  for pattern in PATTERNS_B:
    if x_mas_test_pattern(lines, i, j, pattern):
      return True
  return False


def a():
  with open(INPUT_FILE) as f:
    lines = f.read().split("\n")

    total = 0
    for i, line in enumerate(lines):
      for j, c in enumerate(line):
        total += xmas_count_at(lines, i, j, c)
    print(total)

def b():
  with open(INPUT_FILE) as f:
    lines = f.read().split("\n")

    count = 0
    for i, line in enumerate(lines):
      for j, c in enumerate(line):
        if x_mas_test(lines, i, j, c):
          count += 1
    print(count)

if __name__ == '__main__':
  a()
  b()