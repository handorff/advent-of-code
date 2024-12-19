INPUT_FILE = "19.in"



def parse_input(input_str):
  [pattern_str, design_str] = input_str.split("\n\n")
  patterns = pattern_str.split(", ")
  designs = design_str.split("\n")
  return patterns, designs


def is_possible(patterns, design):
  assert "u" in patterns
  assert "g" in patterns
  assert "b" in patterns
  assert "w" in patterns
  assert "r" not in patterns

  assert "ru" in patterns
  assert "rg" in patterns
  assert "rb" in patterns
  assert "rw" in patterns
  assert "rr" in patterns

  # we can trivially make anything except for things that END WITH R
  # because we can use RX every time we see an r, and U/G/B/W otherwise
  
  if design == '':
    return True

  if design[-1] != 'r':
    return True

  for p in patterns:
    if design.endswith(p) and is_possible(patterns, design[:-len(p)]):
      return True

  return False


def a():
  with open(INPUT_FILE) as f:
    patterns, designs = parse_input(f.read())
    print(sum(1 for d in designs if is_possible(patterns, d)))


CACHE = {}
def num_ways(patterns, design):
  if design == '':
    return 1

  if design in CACHE:
    return CACHE[design]

  result = 0
  for p in patterns:
    if design.endswith(p):
      result += num_ways(patterns, design[:-len(p)])
  CACHE[design] = result
  return result


def b():
  with open(INPUT_FILE) as f:
    patterns, designs = parse_input(f.read())
    print(sum(num_ways(patterns, d) for d in designs))


if __name__ == '__main__':
  a()
  b()