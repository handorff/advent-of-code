INPUT_FILE = "15.in"

def parse_map(map_str):
  lines = map_str.split("\n")
  walls = set()
  boxes = set()
  robot = None
  for i, line in enumerate(lines):
    for j, c in enumerate(line):
      if c == '#':
        walls.add((i, j))
      if c == 'O':
        boxes.add((i, j))
      if c == '@':
        robot = (i, j)

  bounds = len(lines), len(lines[0])
  return (robot, walls, boxes, bounds)


def parse_input(input_str):
  [map_str, moves_str] = input_str.split("\n\n")
  warehouse = parse_map(map_str)
  return (warehouse, moves_str)


def print_map(warehouse):
  robot, walls, boxes, bounds = warehouse

  for i in range(bounds[0]):
    line = ''
    for j in range(bounds[1]):
      if (i, j) in walls:
        line += '#'
      elif (i, j) in boxes:
        line += 'O'
      elif (i, j) == robot:
        line += '@'
      else:
        line += '.'
    print(line)


def move_to_d(move):
  return {
    "<": (0, -1),
    ">": (0, 1),
    "^": (-1, 0),
    "v": (1, 0)
  }[move]


def do_move(warehouse, move):
  robot, walls, boxes, bounds = warehouse
  di, dj = move_to_d(move)

  i, j = robot
  new_i, new_j = i + di, j + dj
  if (new_i, new_j) in walls:
    # can't move
    return warehouse

  if (new_i, new_j) in boxes:
    # push boxes
    box_line = []
    while True:
      box_line.append((new_i, new_j))
      new_i, new_j = new_i + di, new_j + dj

      if (new_i, new_j) in walls:
        # can't move
        return warehouse

      if (new_i, new_j) in boxes:
        continue

      # found empty space, move whole box line
      to_remove = box_line[0]
      last_box = box_line[-1]
      li, lj = last_box
      to_add = (li + di, lj + dj)

      new_boxes = boxes.copy()
      new_boxes.add(to_add)
      new_boxes.remove(to_remove)

      robot = (i + di, j + dj)
      return (robot, walls, new_boxes, bounds)

  # move to empty space
  robot = (new_i, new_j)
  return (robot, walls, boxes, bounds)
  
def gps(box):
  i, j = box
  return 100 * i + j

def a():
  with open(INPUT_FILE) as f:
    warehouse, moves = parse_input(f.read())
    for move in moves:
      if move != "\n":
        warehouse = do_move(warehouse, move)
    # print_map(warehouse)
    _, _, boxes, _ = warehouse
    print(sum(gps(box) for box in boxes))

def parse_map_b(map_str):
  lines = map_str.split("\n")
  walls = set()
  boxes = set()
  robot = None
  for i, line in enumerate(lines):
    for j, c in enumerate(line):
      if c == '#':
        walls.add((i, 2 * j))
        walls.add((i, 2 * j + 1))
      if c == 'O':
        boxes.add((i, 2 * j))
      if c == '@':
        robot = (i, 2 * j)

  bounds = len(lines), 2 * len(lines[0])
  return (robot, walls, boxes, bounds)


def parse_input_b(input_str):
  [map_str, moves_str] = input_str.split("\n\n")

  warehouse = parse_map_b(map_str)
  return (warehouse, moves_str)

def print_map_b(warehouse):
  robot, walls, boxes, bounds = warehouse

  for i in range(bounds[0]):
    line = ''
    for j in range(bounds[1]):
      if (i, j) in walls:
        line += '#'
      elif (i, j) in boxes:
        line += '['
      elif (i, j - 1) in boxes:
        line += ']'
      elif (i, j) == robot:
        line += '@'
      else:
        line += '.'
    print(line)


def do_move_b(warehouse, move):
  robot, walls, boxes, bounds = warehouse
  di, dj = move_to_d(move)

  i, j = robot
  new_i, new_j = i + di, j + dj
  if (new_i, new_j) in walls:
    # can't move
    return warehouse

  if (new_i, new_j) in boxes or (new_i, new_j - 1) in boxes:
    initial_box = (new_i, new_j) if (new_i, new_j) in boxes else (new_i, new_j - 1)

    # push boxes
    boxes_to_move = []
    
    box_queue = [initial_box]
    while len(box_queue) > 0:
      bi, bj = box_queue.pop(0)
      boxes_to_move.append((bi, bj))
      # box occupies the spaces (bi, bj) and (bi, bj + 1)
      new_bi, new_bj = bi + di, bj + dj

      # box wants to move to spaces (new_bi, new_bj) and (new_bi, new_bj + 1)
      if (new_bi, new_bj) in walls or (new_bi, new_bj + 1) in walls:
        # nothing can move
        return warehouse

      if (new_bi, new_bj) in boxes:
        box_queue.append((new_bi, new_bj))

      if (new_bi, new_bj - 1) in boxes and (new_bi, new_bj - 1) != (bi, bj): # don't add same box
        box_queue.append((new_bi, new_bj - 1))

      if (new_bi, new_bj + 1) in boxes and (new_bi, new_bj + 1) != (bi, bj): # don't add same box
        box_queue.append((new_bi, new_bj + 1))

    old_boxes_to_move = boxes_to_move[:]
    new_boxes_to_move = [(bi + di, bj + dj) for (bi, bj) in boxes_to_move]

    to_add = set(new_boxes_to_move) - set(old_boxes_to_move)
    to_remove = set(old_boxes_to_move) - set(new_boxes_to_move)

    new_boxes = boxes.copy()
    for b in to_add:
      new_boxes.add(b)
    for b in to_remove:
      new_boxes.remove(b)

    robot = (i + di, j + dj)
    return (robot, walls, new_boxes, bounds)

  # move to empty space
  robot = (new_i, new_j)
  return (robot, walls, boxes, bounds)


def b():
  with open(INPUT_FILE) as f:
    warehouse, moves = parse_input_b(f.read())
    for move in moves:
      # print_map_b(warehouse)

      if move != "\n":
        # print(move)
        warehouse = do_move_b(warehouse, move)

    # print_map_b(warehouse)
    _, _, boxes, _ = warehouse
    print(sum(gps(box) for box in boxes))
    

if __name__ == '__main__':
  a()
  b()