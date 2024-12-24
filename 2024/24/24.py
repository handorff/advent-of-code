from collections import defaultdict

INPUT_FILE = "24.in"


def parse_values(val_str):
  lines = val_str.split("\n")

  d = {}
  for line in lines:
    [a, b] = line.split(": ")
    d[a] = int(b)

  return d


def parse_gate(line):
  [input_str, output] = line.split(" -> ")
  [a, op, b] = input_str.split(" ")
  [a, b] = sorted([a, b])
  return ((a, op, b), output)



def parse_gates(gate_str):
  lines = gate_str.split("\n")
  return [parse_gate(line) for line in lines]


def parse_input(input_str):
  [val_str, gate_str] = input_str.split("\n\n")
  return parse_values(val_str), parse_gates(gate_str)


def get_var_dict(values, gates):
  d = defaultdict(list)
  for g in gates:
    (a, _, b), _ = g
    d[a].append(g)
    d[b].append(g)

  return d


def compute_gate(gate, a_val, b_val):
  (_, op, _), _ = gate
  if op == "AND":
    return a_val and b_val

  if op == "OR":
    return a_val or b_val

  if op == "XOR":
    return a_val ^ b_val

  assert False


def solve_a(values, gates):
  values = find_all_values(values, gates)
  z_values = sorted((a, b) for a, b in values.items() if a[0] == 'z')
  s = ''.join(str(b) for _, b in z_values[::-1])
  return int(s, 2)


def find_all_values(values, gates):
  variables_to_gates = get_var_dict(values, gates)
  q = list(values.keys())

  while len(q) > 0:
    v = q.pop(0)

    for gate in variables_to_gates[v]:
      (a, _, b), out = gate
      if a in values.keys() and b in values.keys():
        result = compute_gate(gate, values[a], values[b])
        values[out] = result
        q.append(out)

  return values



def a():
  with open(INPUT_FILE) as f:
    values, gates = parse_input(f.read())
    print(solve_a(values, gates))




def get_var(c, i):
  if i < 10:
    return c + '0' + str(i)
  return c + str(i)


def find_gate_output(gates, a, op, b):
  [a, b] = sorted([a, b])
  for g in gates:
    g_in, g_out = g
    if g_in == (a, op, b):
      return g_out

  assert False


# mkk / z10
# qbw / z14
# wjb / cvp
# wcb / z34

def solve_b(values, gates):
  # get first wrong gate
  variables_to_gates = get_var_dict(values, gates)

  assert (('x00', 'XOR', 'y00'), 'z00') in variables_to_gates['x00']
  carry_var = find_gate_output(gates, 'x00', 'AND', 'y00')

  i = 1
  while True:
    x_var = get_var('x', i)
    y_var = get_var('y', i)
    z_var = get_var('z', i)
    xor_var = find_gate_output(gates, x_var, 'XOR', y_var)
    and_var = find_gate_output(gates, x_var, 'AND', y_var)

    output_var = find_gate_output(gates, carry_var, 'XOR', xor_var)

    if output_var != z_var:
      print(output_var, z_var)
      assert False
    assert output_var == z_var

    boop_var = find_gate_output(gates, carry_var, 'AND', xor_var)
    carry_var = find_gate_output(gates, boop_var, 'OR', and_var)

    i += 1





def b():
  with open(INPUT_FILE) as f:
    values, gates = parse_input(f.read())
    solve_b(values, gates)


if __name__ == '__main__':
  a()
  b()
