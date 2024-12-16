INPUT_FILE = "03.in"
import re

def a():
  with open(INPUT_FILE) as f:
    input_string = f.read()
    matches = re.findall("mul\((\d*),(\d*)\)", input_string)
    print(sum(int(a) * int(b) for a, b, in matches))

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
  b()