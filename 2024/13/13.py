INPUT_FILE = "13.in"

def parse_button(s):
  [x_str, y_str] = s.split(": ")[1].split(", ")
  x = int(x_str.split("+")[1])
  y = int(y_str.split("+")[1])
  return (x, y)

def parse_target(s):
  [x_str, y_str] = s.split(": ")[1].split(", ")
  x = int(x_str.split("=")[1])
  y = int(y_str.split("=")[1])
  return (x, y)

def parse_machine(s):
  [a_str, b_str, target_str] = s.split("\n")
  return (parse_button(a_str), parse_button(b_str), parse_target(target_str))

def parse_input(input_str):
  machine_strs = input_str.split("\n\n")
  return [parse_machine(m) for m in machine_strs]

def min_tokens(machine):
  (ax, ay), (bx, by), (target_x, target_y) = machine

  min_so_far = None

  for a_presses in range(101):
    x, y = a_presses * ax, a_presses * ay
    dx, dy = target_x - x, target_y - y
    if dx % bx == 0 and dy % by == 0 and dx // bx == dy // by:
      b_presses = dx // bx
      cost = 3 * a_presses + b_presses
      min_so_far = cost if min_so_far is None else min(min_so_far, cost)

  return 0 if min_so_far is None else min_so_far

def a():
  with open(INPUT_FILE) as f:
    machines = parse_input(f.read())
    print(sum(min_tokens(m) for m in machines))


def min_tokens_b(machine):
  (ax, ay), (bx, by), (target_x, target_y) = machine
  target_x += 10000000000000
  target_y += 10000000000000
  
  if ay * bx == by * ax:
    # only case where you can swap a presses for b presses is where the ratio is the same
    # otherwise there's at most one way
    assert False

  # ax * a + bx * b = target_x
  # ay * a + by * b = target_y

  # ax * ay * a + bx * ay * b = target_x * ay  # multiply by ay
  # ay * ax * a + by * ax * b = target_y * ax  # multiply by ax
  # target_x * ay - bx * ay * b = target_y * ax - by * ax * b
  # target_x * ay - target_y * ax = bx * ay * b - by * ax * b
  # target_x * ay - target_y * ax = (b) * (bx * ay - by * ax)
  # b = (target_x * ay - target_y * ax) // (bx * ay - by * ax)
  # a = (target_x - bx * b) // ax


  if (target_x * ay - target_y * ax) % (bx * ay - by * ax) != 0:
    # not possible
    return 0

  b = (target_x * ay - target_y * ax) // (bx * ay - by * ax)

  if (target_x - bx * b) % ax != 0:
    return 0
  assert (target_y - by * b) % ay == 0
  assert (target_x - bx * b) // ax == (target_y - by * b) // ay
  a = (target_x - bx * b) // ax

  assert a * ax + b * bx == target_x
  assert a * ay + b * by == target_y

  return 3 * a + b


def b():
  with open(INPUT_FILE) as f:
    machines = parse_input(f.read())
    print(sum(min_tokens_b(m) for m in machines))
    # min_tokens_b(machines[1])

if __name__ == '__main__':
  a()
  b()