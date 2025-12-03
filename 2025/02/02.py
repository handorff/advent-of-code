INPUT_FILE = "02.in"

def parse_input(f):
  ranges = f.read().split(",")
  return [tuple(map(int, r.split("-"))) for r in ranges]


def get_invalid(start, end):
  # handle differing numbers of digits
  if len(str(start)) != len(str(end)):
    start_digits = len(str(start))
    end_digits = len(str(end))

    invalid_ids = []
    for d in range(start_digits, end_digits + 1):
      if d == start_digits:
        invalid_ids += get_invalid(start, 10 ** d - 1)
      elif d == end_digits:
        invalid_ids += get_invalid(10 ** (d - 1), end)
      else:
        invalid_ids += get_invalid(10 ** (d - 1), 10 ** d - 1)
    return invalid_ids

  num_digits = len(str(start))

  # can't have repeat if odd
  if num_digits % 2 == 1:
    return []

  l = num_digits // 2
  divisor = 10 ** l + 1
  s = start // divisor
  e = end // divisor
  invalid_ids = list(range(s + 1, e + 1))

  if start % divisor == 0:
    invalid_ids = [s] + invalid_ids

  return [i * divisor for i in invalid_ids]


def a():
  with open(INPUT_FILE) as f:
    ranges = parse_input(f)

    total = 0
    for (start, end) in ranges:
      total += sum(get_invalid(start, end))
    print(total)


def get_invalid_for_digit_divisor(start, end, d):
  num_digits = len(str(start))
  if num_digits % d != 0:
    return []

  l = num_digits // d
  divisor = sum(10 ** (l * i) for i in range(d))
  s = start // divisor
  e = end // divisor
  invalid_ids = list(range(s + 1, e + 1))

  if start % divisor == 0:
    invalid_ids = [s] + invalid_ids

  return [i * divisor for i in invalid_ids]


def get_invalid_helper(start, end):
  num_digits = len(str(start))
  
  invalid_ids = []
  for d in range(2, num_digits + 1):
    invalid_ids += get_invalid_for_digit_divisor(start, end, d)

  return list(set(invalid_ids))


def get_invalid_b(start, end):
  # handle differing numbers of digits
  if len(str(start)) != len(str(end)):
    start_digits = len(str(start))
    end_digits = len(str(end))

    invalid_ids = []
    for d in range(start_digits, end_digits + 1):
      if d == start_digits:
        invalid_ids += get_invalid_helper(start, 10 ** d - 1)
      elif d == end_digits:
        invalid_ids += get_invalid_helper(10 ** (d - 1), end)
      else:
        invalid_ids += get_invalid_helper(10 ** (d - 1), 10 ** d - 1)
    return invalid_ids

  return get_invalid_helper(start, end)


def b():
  with open(INPUT_FILE) as f:
    ranges = parse_input(f)

    total = 0
    for (start, end) in ranges:
      total += sum(get_invalid_b(start, end))
    print(total)


if __name__ == '__main__':
  a()
  b()