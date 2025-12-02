INPUT_FILE = "03.in"
import re

def a():
  with open(INPUT_FILE) as f:
    input_string = f.read()
    matches = re.findall("mul\((\d*),(\d*)\)", input_string)
    print(sum(int(a) * int(b) for a, b, in matches))

def score(s):
  inner = s.split(")")[0]
  parts = inner.split(",")
  if len(parts) != 2:
    return 0

  [p1, p2] = parts
  if not p1.isnumeric() or not p2.isnumeric():
    return 0
  return int(p1) * int(p2)

def a2():
  with open(INPUT_FILE) as f:
    input_string = f.read()
    print(sum(score(s) for s in input_string.split("mul(")))

def b():
  with open(INPUT_FILE) as f:
    input_string = "do()" + f.read()
    disable_groups = input_string.split("don\'t()")

    total = 0
    for group in disable_groups:
      if "do()" in group:
        _, enabled = group.split("do()", 1)
        matches = re.findall("mul\((\d*),(\d*)\)", enabled)
        total += sum(int(a) * int(b) for a, b, in matches)
    print(total)


if __name__ == '__main__':
  a()
  a2()
  b()