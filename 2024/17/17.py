INPUT_FILE = "17.in"

def parse_registers(s):
  lines = s.split("\n")
  [a, b, c] = [int(line.split(": ")[1]) for line in lines]
  return (a, b, c)

def parse_program(s):
  arr = [int(c) for c in s.split(": ")[1].split(",")]
  return { i: n for i, n in enumerate(arr) }

def parse_input(input_str):
  [registers_str, program_str] = input_str.split("\n\n")
  return parse_registers(registers_str), parse_program(program_str)

def get_combo_operand(operand, registers):
  if operand in [0, 1, 2, 3]:
    return operand

  a, b, c = registers
  if operand == 4:
    return a
  if operand == 5:
    return b
  if operand == 6:
    return c
  # can't be 7
  assert False

def do_instruction(program, registers, ptr):
  if ptr not in program:
    # halt
    return None

  a, b, c = registers
  output = None
  opcode = program[ptr]
  if opcode == 0:
    # adv
    operand = program[ptr + 1]
    value = get_combo_operand(operand, registers)
    a = a // (2 ** value)
    ptr = ptr + 2

  if opcode == 1:
    # bxl
    operand = program[ptr + 1]
    b = b ^ operand
    ptr = ptr + 2

  if opcode == 2:
    # bst
    operand = program[ptr + 1]
    value = get_combo_operand(operand, registers)
    b = value % 8
    ptr = ptr + 2

  if opcode == 3:
    # jnz
    if a == 0:
      ptr = ptr + 2
    else:
      operand = program[ptr + 1]
      ptr = operand

  if opcode == 4:
    # bxc
    b = b ^ c
    ptr = ptr + 2

  if opcode == 5:
    # out
    operand = program[ptr + 1]
    value = get_combo_operand(operand, registers)
    output = value % 8
    ptr = ptr + 2

  if opcode == 6:
    # bdv
    operand = program[ptr + 1]
    value = get_combo_operand(operand, registers)
    b = a // (2 ** value)
    ptr = ptr + 2

  if opcode == 7:
    # cdv
    operand = program[ptr + 1]
    value = get_combo_operand(operand, registers)
    c = a // (2 ** value)
    ptr = ptr + 2

  return (a, b, c), ptr, output


def run_program(program, registers):
  output = []
  ptr = 0

  while True:
    r = do_instruction(program, registers, ptr)
    if r is None: # halt
      return output

    registers, ptr, o = r
    if o is not None:
      output.append(o)


def a():
  with open(INPUT_FILE) as f:
    registers, program = parse_input(f.read())
    print(",".join(map(str, run_program(program, registers))))


def b():
  with open(INPUT_FILE) as f:
    _, program = parse_input(f.read())

    program_arr = [v[1] for v in sorted(program.items())]

    arr = [0]
    for i in range(1, len(program_arr) + 1):
      target = program_arr[-i:]

      next_arr = []
      for a in arr:
        for next_a in range(a * 8, (a + 1) * 8):
          if run_program(program, (next_a, 0, 0)) == target:
            next_arr.append(next_a)

      arr = next_arr

    print(min(arr))




if __name__ == '__main__':
  a()
  b()