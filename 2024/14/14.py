from time import sleep
from collections import Counter

# INPUT_FILE = "14test.in"
# WIDTH, HEIGHT = 11, 7

INPUT_FILE = "14.in"
WIDTH, HEIGHT = 101, 103

def parse_line(line):
  [p_str, v_str] = line.split(" ")

  [px, py] = p_str[2:].split(",")
  px, py = int(px), int(py)
  p = (px, py)

  [vx, vy] = v_str[2:].split(",")
  vx, vy = int(vx), int(vy)
  v = (vx, vy)

  return (p, v)

def get_position(robot, t):
  (px, py), (vx, vy) = robot
  x = (px + t * vx) % WIDTH
  y = (py + t * vy) % HEIGHT
  return (x, y)

def get_quadrant(p):
  x, y = p
  if x < WIDTH // 2 and y < HEIGHT // 2:
    return 1

  if x > WIDTH // 2 and y < HEIGHT // 2:
    return 2

  if x < WIDTH // 2 and y > HEIGHT // 2:
    return 3

  if x > WIDTH // 2 and y > HEIGHT // 2:
    return 4

  return 0


def a():
  with open(INPUT_FILE) as f:
    lines = f.read().split("\n")
    robots = [parse_line(line) for line in lines]
    future = [get_position(r, 100) for r in robots]
    c = Counter(get_quadrant(f) for f in future)
    print(c[1] * c[2] * c[3] * c[4])

def print_robots(future):
  robots = set(future)

  for i in range(HEIGHT):
    line = []
    for j in range(WIDTH):
      if (j, i) in robots:
        line += "*"
      else:
        line += "."
    print(''.join(line))

# vertical: 81, 182, 283, 384, 485, ...
# horizontal: 30, 133, 236, 339, ...

def b():
  with open(INPUT_FILE) as f:
    lines = f.read().split("\n")
    robots = [parse_line(line) for line in lines]

    i = 7858
    future = [get_position(r, i) for r in robots]
    print_robots(future)

if __name__ == '__main__':
  a()
  b()