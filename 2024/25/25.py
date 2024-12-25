from itertools import product

INPUT_FILE = "25.in"


def parse_lock_heights(lines):
  heights = [-1, -1, -1, -1, -1]
  for line in lines:
    for i, c in enumerate(line):
      if c == '#':
        heights[i] += 1
  return heights


def parse_key_heights(lines):
  return parse_lock_heights(lines)


def parse_object(object_str):
  lines = object_str.split("\n")
  
  object_type = None
  heights = None
  if lines[0] == '#####':
    object_type = "LOCK"
    heights = parse_lock_heights(lines)
  else:
    assert lines[-1] == '#####'
    object_type = "KEY"
    heights = parse_key_heights(lines)

  return (object_type, heights)


def parse_input(input_str):
  objects = input_str.split("\n\n")

  keys = []
  locks = []
  for o in objects:
    t, heights = parse_object(o)
    if t == "KEY":
      keys.append(heights)
    else:
      locks.append(heights)

  return (locks, keys)


def does_fit(lock, key):
  for i in range(5):
    if lock[i] + key[i] > 5:
      return False
  return True


def solve_a(locks, keys):
  valid = 0
  for lock, key in product(locks, keys):
    if does_fit(lock, key):
      valid += 1
  return valid


def a():
  with open(INPUT_FILE) as f:
    locks, keys = parse_input(f.read())
    print(solve_a(locks, keys))


if __name__ == '__main__':
  a()