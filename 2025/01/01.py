INPUT_FILE = "01.in"

def parse_input(f):
  lines = f.read().split("\n")
  return [(-1 if line[0] == 'L' else 1) * int(line[1:]) for line in lines]

def a():
  with open(INPUT_FILE) as f:
    deltas = parse_input(f)
    
    curr = 50
    count = 0

    for delta in deltas:
      curr += delta
      curr %= 100
      if curr == 0:
        count += 1

    print(count)


# Number of clicks at zero, including the click at after but omitting the click at before
def num_zero(before, after):
  assert before >= 0 and before <= 99
  assert before != after

  if after > before:
    return abs(after // 100 - before // 100)

  if before > after:
    return abs((after - 1) // 100 - (before - 1) // 100)


def test_b():
  assert num_zero(99, 100) == 1
  assert num_zero(0, 99) == 0
  assert num_zero(1, 100) == 1
  assert num_zero(0, 1) == 0
  assert num_zero(0, -1) == 0
  assert num_zero(0, -2) == 0
  assert num_zero(0, -99) == 0
  assert num_zero(0, -100) == 1
  assert num_zero(1, -1) == 1
  assert num_zero(1, 0) == 1


def b():
  with open(INPUT_FILE) as f:
    deltas = parse_input(f)

    curr = 50
    count = 0

    for delta in deltas:
      count += num_zero(curr, curr + delta)
      curr += delta
      curr %= 100

    print(count)


if __name__ == '__main__':
  a()
  b()