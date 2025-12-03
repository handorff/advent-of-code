INPUT_FILE = "03.in"

def get_joltage(line):
  m = max(line[:-1])
  i = line.find(m)
  n = max(line[i+1:])
  return 10 * int(m) + int(n)

def a():
  with open(INPUT_FILE) as f:
    lines = f.read().split("\n")
    print(sum(get_joltage(line) for line in lines))


def get_joltage_helper(line, n):
  if n == 0:
    return []

  if n == 1:
    return [max(line)]

  m = max(line[:-(n-1)])
  i = line.find(m)
  return [m] + get_joltage_helper(line[i+1:], n - 1)


def get_joltage_b(line):
  return int(''.join(get_joltage_helper(line, 12)))

def b():
  with open(INPUT_FILE) as f:
    lines = f.read().split("\n")
    print(sum(get_joltage_b(line) for line in lines))



if __name__ == '__main__':
  a()
  b()