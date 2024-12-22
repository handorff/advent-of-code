import itertools
from collections import defaultdict

INPUT_FILE = "21.in"


def move_numeric_robot(direction, square):
  d = {
    '^4': '7',
    '^5': '8',
    '^6': '9',
    '^1': '4',
    '^2': '5',
    '^3': '6',
    '^0': '2',
    '^A': '3',
    'v7': '4',
    'v8': '5',
    'v9': '6',
    'v4': '1',
    'v5': '2',
    'v6': '3',
    'v2': '0',
    'v3': 'A',
    '>7': '8',
    '>4': '5',
    '>1': '2',
    '>8': '9',
    '>5': '6',
    '>2': '3',
    '>0': 'A',
    '<8': '7',
    '<5': '4',
    '<2': '1',
    '<9': '8',
    '<6': '5',
    '<3': '2',
    '<A': '0'
  }
  if (direction + square) in d:
    return d[direction + square]
  return None


def move_direction_robot(direction, square):
  # robot is on square and moves in direction
  d = {
    '^v': '^',
    '^>': 'A',
    'v^': 'v',
    'vA': '>',
    '>^': 'A',
    '>v': '>',
    '><': 'v',
    '<v': '<',
    '<>': 'v',
    '<A': '^'
  }
  if (direction + square) in d:
    return d[direction + square]
  return None


def press_button(button, state):
  # get new state if I press button from state
  (r3, r2, r1) = state
  if button == 'A':
    if r3 == 'A':
      if r2 == 'A':
        # emit r1
        return (state, r1)

      else:
        new_r1 = move_numeric_robot(r2, r1)
        if new_r1 is None:
          return None
        new_state = (r3, r2, new_r1)
        return (new_state, None)

    else:
      new_r2 = move_direction_robot(r3, r2)
      if new_r2 is None:
        return None
      new_state = (r3, new_r2, r1)
      return (new_state, None)

  else:
    new_r3 = move_direction_robot(button, r3)
    if new_r3 is None:
      return None
    new_state = (new_r3, r2, r1)
    return (new_state, None)


def test_press_button(button_sequence, expected):
  state = ('A', 'A', 'A')
  emitted = ''

  for button in button_sequence:
    result = press_button(button, state)
    assert result is not None
    (state, emit) = result
    if emit is not None:
      emitted += emit

  return emitted == expected


def shortest_sequence_length(code):
  q = [(0, ('A', 'A', 'A'), '')]

  visited = set()

  while len(q) > 0:
    n, state, emitted = q.pop(0)

    visited.add((state, emitted))

    if emitted == code:
      return n

    for b in '^v><A':
      result = press_button(b, state)
      if result is not None:
        new_state, emit = result
        if emit is None:
          if (new_state, emitted) not in visited:
            q.append((n + 1, new_state, emitted))
        else:
          new_emitted = emitted + emit
          if code.startswith(new_emitted):
            q = [(n + 1, new_state, new_emitted)]


def test_button_sequences():
  assert test_press_button('<vA<AA>>^AvAA<^A>A<v<A>>^AvA^A<vA>^A<v<A>^A>AAvA^A<v<A>A>^AAAvA<^A>A', '029A')
  assert test_press_button('<v<A>>^AAAvA^A<vA<AA>>^AvAA<^A>A<v<A>A>^AAAvA<^A>A<vA>^A<A>A', '980A')
  assert test_press_button('<v<A>>^A<vA<A>>^AAvAA<^A>A<v<A>>^AAvA^A<vA>^AA<A>A<v<A>A>^AAAvA<^A>A', '179A')
  assert test_press_button('<v<A>>^AA<vA<A>>^AAvAA<^A>A<vA>^A<A>A<vA>^A<A>A<v<A>A>^AAvA<^A>A', '456A')
  assert test_press_button('<v<A>>^AvA^A<vA<AA>>^AAvA<^A>AAvA^A<vA>^AA<A>A<v<A>A>^AAAvA<^A>A', '379A')


def numeric_part(code):
  return int(''.join(c for c in code if c.isdigit()))

def a():
  with open(INPUT_FILE) as f:
    codes = f.read().split("\n")
    # test_button_sequences()

    print(sum(shortest_sequence_length(code) * numeric_part(code) for code in codes))


###


def get_numeric_sequence(from_button, to_button):
  q = [('', from_button)]
  visited = set()

  while len(q) > 0:
    seq, square = q.pop(0)

    if square == to_button:
      return seq

    for b in '^v><':
      result = move_numeric_robot(b, square)
      if result is not None and result not in visited:
        q.append((seq + b, result))


def get_numeric_sequences():
  buttons = '1234567890A'
  sequences = {}

  for p in itertools.product(buttons, repeat=2):
    from_button, to_button = p
    seq = get_numeric_sequence(from_button, to_button)
    sequences[(from_button, to_button)] = ''.join(sorted(seq))

  return sequences


def get_direction_sequence(from_button, to_button):
  q = [('', from_button)]
  visited = set()

  while len(q) > 0:
    seq, square = q.pop(0)

    if square == to_button:
      return seq

    for b in '^v><':
      result = move_direction_robot(b, square)
      if result is not None and result not in visited:
        q.append((seq + b, result))


def get_direction_sequences():
  buttons = '^v><A'
  sequences = {}

  for p in itertools.product(buttons, repeat=2):
    from_button, to_button = p
    seq = get_direction_sequence(from_button, to_button)
    sequences[(from_button, to_button)] = ''.join(sorted(seq))

  return sequences


def is_valid_permutation(start, button_sequence):
  square = start
  for b in button_sequence:
    square = move_direction_robot(b, square)
    if square is None:
      return False
  return True


def get_orderings(pair, buttons):
  perms = itertools.permutations(buttons)
  perms = list(set(perms))
  perms = [''.join(p) for p in perms]
  return [p for p in perms if is_valid_permutation(pair[0], p)]


def get_direction_sequences2():
  sequences = get_direction_sequences()
  return {
    k: get_orderings(k, v) for k, v in sequences.items()
  }


def is_reasonable_num_permutation(start, button_sequence):
  square = start
  for b in button_sequence:
    square = move_numeric_robot(b, square)
    if square is None:
      return False
  
  # assumption: should always have consecutive button presses in a row
  index_dict = defaultdict(list)
  for i, b in enumerate(button_sequence):
    index_dict[b].append(i)
  assert len(index_dict) < 3
  if len(index_dict) == 2:
    [i1, i2] = index_dict.values()
    return max(i1) < min(i2) or max(i2) < min(i1)

  else:
    return True


def get_num_orderings(pair, buttons):
  perms = itertools.permutations(buttons)
  perms = list(set(perms))
  perms = [''.join(p) for p in perms]
  return [p for p in perms if is_reasonable_num_permutation(pair[0], p)]


def get_numeric_sequences2():
  sequences = get_numeric_sequences()
  return {
    k: get_num_orderings(k, v) for k, v in sequences.items()
  }


def direction_sequence_to_counts(seq):
  buttons = '^v><A'
  d = {p: 0 for p in itertools.product(buttons, repeat=2)}
  for (from_button, to_button) in zip(seq, seq[1:]):
    d[(from_button, to_button)] += 1
  return d

def expand_table(d, table):
  buttons = '^v><A'
  new_table = {p: 0 for p in itertools.product(buttons, repeat=2)}

  for p, count in table.items():
    seq = 'A' + d[p] + 'A'
    for pair in zip(seq, seq[1:]):
      new_table[pair] += count

  return new_table


def shortest_sequence_length_b(d, seq):
  table = direction_sequence_to_counts(seq)

  for i in range(25):
    table = expand_table(d, table)
    # print (i + 1, sum(table.values()))
  return sum(table.values())


def get_all_rules(d):
  items = d.items()
  keys = [k for k, v in items]
  values = [v for k, v in items]
  return [dict(list(zip(keys, p))) for p in itertools.product(*values)]


def select_rules(nums, codes):
  d = get_direction_sequences2()
  rules = get_all_rules(d)
  seq = expand_num_sequence(nums, codes[0])[0]

  min_r = None
  min_r_length = 10 ** 15

  for r in rules:
    l = shortest_sequence_length_b(r, seq)
    if l < min_r_length:
      min_r = r
      min_r_length = l

  return min_r


def expand_num_sequence(d, sequence):
  sequence = 'A' + sequence
  arr = [d[pair] for pair in zip(sequence, sequence[1:])]
  return ['A' + 'A'.join(p) + 'A' for p in itertools.product(*arr)]


def b():
  with open(INPUT_FILE) as f:
    codes = f.read().split("\n")
    d = get_numeric_sequences2()
    min_r = select_rules(d, codes)
    num_sequences = {code: expand_num_sequence(d, code) for code in codes}

    total = 0
    for k, seqs in num_sequences.items():
      total += numeric_part(k) * min(shortest_sequence_length_b(min_r, seq) for seq in seqs)
    print(total)

if __name__ == '__main__':
  a()
  b()