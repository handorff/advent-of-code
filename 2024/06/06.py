import sys
import time
sys.setrecursionlimit(10000)

INPUT_FILE = "06.in"

ORIENTATIONS = [
  (0, -1),
  (1, 0),
  (0, 1),
  (-1, 0)
]

def parse_lines(lines):
  guard_position = None
  obstruction_positions = set()
  for i, line in enumerate(lines):
    for j, c in enumerate(line):
      if c == "#":
        obstruction_positions.add((j, i))

      elif c == "^":
        guard_position = (j, i)

  bounds = (len(lines), len(lines[0]))
  return (guard_position, obstruction_positions, bounds)

def outside_bounds(guard, bounds):
  guard_x, guard_y = guard
  bounds_x, bounds_y = bounds
  return guard_x < 0 or guard_x >= bounds_x or guard_y < 0 or guard_y >= bounds_y


def solve_a(guard, obstructions, bounds, orientation_index):
  if outside_bounds(guard, bounds):
    return []

  orientation = ORIENTATIONS[orientation_index]
  dx, dy = orientation
  guard_x, guard_y = guard
  next_x, next_y = guard_x + dx, guard_y + dy
  next_pos = (next_x, next_y)
  
  if next_pos in obstructions:
    # rotate
    next_orientation_index = (orientation_index + 1) % (len(ORIENTATIONS))
    return [guard] + solve_a(guard, obstructions, bounds, next_orientation_index)

  else:
    return [guard] + solve_a(next_pos, obstructions, bounds, orientation_index)


def solve_a2(guard, obstructions, bounds, orientation_index):
  visited = set()

  while True:
    if outside_bounds(guard, bounds):
      return visited

    visited.add(guard)

    orientation = ORIENTATIONS[orientation_index]
    dx, dy = orientation
    guard_x, guard_y = guard
    next_x, next_y = guard_x + dx, guard_y + dy
    next_pos = (next_x, next_y)

    if next_pos in obstructions:
      # rotate
      orientation_index = (orientation_index + 1) % (len(ORIENTATIONS))

    else:
      # step
      guard = next_pos


def a():
  with open(INPUT_FILE) as f:
    lines = f.read().split("\n")
    guard, obstructions, bounds = parse_lines(lines)
    orientation_index = 0

    before_a1 = time.time()
    print(len(set(solve_a(guard, obstructions, bounds, orientation_index))))
    after_a1 = time.time()
    print(after_a1 - before_a1)

    before_a2 = time.time()
    print(len(solve_a2(guard, obstructions, bounds, orientation_index)))
    after_a2 = time.time()
    print(after_a2 - before_a2)


def does_loop(guard, obstructions, bounds, orientation_index):
  previous_states = set()

  while True:
    if outside_bounds(guard, bounds):
      return False

    if (guard, orientation_index) in previous_states:
      return True

    previous_states.add((guard, orientation_index))

    orientation = ORIENTATIONS[orientation_index]
    dx, dy = orientation
    guard_x, guard_y = guard
    next_x, next_y = guard_x + dx, guard_y + dy
    next_pos = (next_x, next_y)

    if next_pos in obstructions:
      # rotate
      orientation_index = (orientation_index + 1) % (len(ORIENTATIONS))

    else:
      # step
      guard = next_pos



def solve_b(guard, obstructions, bounds, orientation_index):
  loop_positions = set()

  bounds_x, bounds_y = bounds
  for i in range(bounds_x):
    for j in range(bounds_y):
      add_obstruction = j, i
      if does_loop(guard, set(obstructions + [(j, i)]), bounds, orientation_index):
        loop_positions.add((j, i))

  return loop_positions


def solve_b2(guard, obstructions, bounds, orientation_index):
  loop_positions = set()
  for pos in solve_a2(guard, obstructions, bounds, orientation_index):
    if does_loop(guard, set(obstructions + [pos]), bounds, orientation_index):
      loop_positions.add(pos)
  return loop_positions

def does_loop2(guard, obstructions, bounds, orientation_index, previous_states):
  obstructions = set(obstructions)
  while True:
    if outside_bounds(guard, bounds):
      return False

    if (guard, orientation_index) in previous_states:
      return True

    previous_states.add((guard, orientation_index))

    orientation = ORIENTATIONS[orientation_index]
    dx, dy = orientation
    guard_x, guard_y = guard
    next_x, next_y = guard_x + dx, guard_y + dy
    next_pos = (next_x, next_y)

    if next_pos in obstructions:
      # rotate
      orientation_index = (orientation_index + 1) % (len(ORIENTATIONS))

    else:
      # step
      guard = next_pos

def solve_b3(guard, obstructions, bounds, orientation_index):
  previous_states = set()
  loop_positions = set()

  while True:
    if outside_bounds(guard, bounds):
      return loop_positions

    orientation = ORIENTATIONS[orientation_index]
    dx, dy = orientation
    guard_x, guard_y = guard
    next_x, next_y = guard_x + dx, guard_y + dy
    next_pos = (next_x, next_y)

    if next_pos in obstructions:
      # rotate
      previous_states.add((guard, orientation_index))
      orientation_index = (orientation_index + 1) % (len(ORIENTATIONS))

    else:
      # try adding an obstruction at nextpos and see if it would loop
      if next_pos not in (pos for pos, _ in previous_states):
        if does_loop2(guard, obstructions + [next_pos], bounds, orientation_index, previous_states.copy()):
          loop_positions.add(next_pos)

      previous_states.add((guard, orientation_index))

      # step
      guard = next_pos


def b():
  with open(INPUT_FILE) as f:
    lines = f.read().split("\n")
    guard, obstructions, bounds = parse_lines(lines)
    orientation_index = 0

    # before_b1 = time.time()
    # print(len(solve_b(guard, list(obstructions), bounds, orientation_index)))
    # after_b1 = time.time()
    # print(after_b1 - before_b1)

    # before_b2 = time.time()
    # print(len(solve_b2(guard, list(obstructions), bounds, orientation_index)))
    # after_b2 = time.time()
    # print(after_b2 - before_b2)

    before_b3 = time.time()
    print(len(solve_b3(guard, list(obstructions), bounds, orientation_index)))
    after_b3 = time.time()
    print(after_b3 - before_b3)


if __name__ == '__main__':
  a()
  b()