INPUT_FILE = "02.in"

def is_safe(line):
  diffs = [b - a for a, b in zip(line, line[1:])]
  direction = all(d > 0 for d in diffs) or all(d < 0 for d in diffs)
  magnitude = all(abs(d) >= 1 and abs(d) <= 3 for d in diffs)
  return direction and magnitude

def is_almost_safe(line):
  if is_safe(line):
    return True

  for i in range(len(line)):
    if is_safe(line[:i] + line[i+1:]):
      return True

  return False



def a():
  with open(INPUT_FILE) as f:
    lines = [list(map(int, line.split(" "))) for line in f.read().split("\n")]
    print(sum(1 if is_safe(line) else 0 for line in lines))

def b():
  with open(INPUT_FILE) as f:
    lines = [list(map(int, line.split(" "))) for line in f.read().split("\n")]
    print(sum(1 if is_almost_safe(line) else 0 for line in lines))


if __name__ == '__main__':
  a()
  b()