import time

INPUT_FILE = "09.in"

def make_initial_array(input_str):
  arr = []

  block_id = 0
  for i, c in enumerate(input_str):
    n = int(c)
    if i % 2 == 0:
      for _ in range(n):
        arr.append(block_id)
      block_id += 1
    else:
      for _ in range(n):
        arr.append(None)

  return arr


def reorder_array(arr):
  i = 0 # front pointer
  j = len(arr) - 1 # back pointer

  assert arr[i] is not None
  assert arr[j] is not None

  while i < j:
    # advance i
    while arr[i] is not None:
      i += 1

    # move arr[j] to empty slot
    arr[i] = arr[j]
    arr[j] = None

    # advance j
    while arr[j] is None:
      j -= 1

  return [elt for elt in arr if elt is not None]


def a():
  with open(INPUT_FILE) as f:
    input_str = f.read()
    arr = make_initial_array(input_str)
    arr = reorder_array(arr)
    print(sum(i * d for i, d in enumerate(arr)))


def make_initial_array_b(input_str):
  arr = []

  block_id = 0
  for i, c in enumerate(input_str):
    n = int(c)
    if i % 2 == 0:
      arr.append((block_id, n))
      block_id += 1
    else:
      arr.append((None, n))

  return arr


def reorder_array_b(arr):
  from_index = len(arr) - 1

  while from_index > 0:
    from_block = arr[from_index]

    assert from_block[0] is not None

    from_block_length = from_block[1]

    # look for a place to move
    to_index = 0
    while to_index < from_index:
      while arr[to_index][0] is not None:
        to_index += 1

      maybe_to_block = arr[to_index]
      assert maybe_to_block[0] is None
      maybe_to_block_length = maybe_to_block[1]

      if maybe_to_block_length >= from_block_length:
        # do move
        # oof this is slow
        before = arr[:to_index]
        after = arr[to_index + 1:]
        new_to_block = [(from_block[0], from_block_length), (None, maybe_to_block_length - from_block_length)]
        arr = before + new_to_block + after
        from_index += 1 # because we always insert an extra block to the left
        arr[from_index] = (None, from_block_length)

        break

      to_index += 1

    # advance to next block
    from_index -= 1
    while arr[from_index][0] is None:
      from_index -= 1

  return arr

def checksum_b(arr):
  i = 0
  total = 0

  for (block_id, block_length) in arr:
    if block_id is None:
      i += block_length
    else:
      for _ in range(block_length):
        total += block_id * i
        i += 1

  return total

def solve_b(input_str):
  arr = make_initial_array_b(input_str)
  arr = reorder_array_b(arr)
  return checksum_b(arr)


def get_file_lengths(input_str):
  return { i // 2: int(c) for i, c in enumerate(input_str) if i % 2 == 0}

def get_file_indexes(input_str):
  file_indexes = {}

  current_index = 0
  for i, c in enumerate(input_str):
    n = int(c)
    if i % 2 == 0:
      file_indexes[i // 2] = current_index

    current_index += n

  return file_indexes

def get_space_indexes(input_str):
  space_indexes = []

  current_index = 0
  for i, c in enumerate(input_str):
    n = int(c)
    if i % 2 == 1 and n > 0:
      space_indexes.append((current_index, n))

    current_index += n

  return space_indexes

def reorder_array_b2(file_lengths, file_indexes, space_indexes):
  for file_id in range(max(file_lengths), 0, -1):
    # try to move file
    file_length = file_lengths[file_id]
    file_index = file_indexes[file_id]

    for i, (maybe_to_index, space_length) in enumerate(space_indexes):
      if maybe_to_index > file_index:
        break

      if space_length >= file_length:
        # do move
        file_indexes[file_id] = maybe_to_index
        space_indexes[i] = (maybe_to_index + file_length, space_length - file_length)
        break

  return file_indexes


def checksum_b2(file_indexes, file_lengths):
  total = 0

  for file_id, file_index in file_indexes.items():
    file_length  = file_lengths[file_id]

    for i in range(file_length):
      total += file_id * (file_index + i)

  return total


def solve_b2(input_str):
  file_lengths = get_file_lengths(input_str)
  file_indexes = get_file_indexes(input_str)
  space_indexes = get_space_indexes(input_str)

  ordered_file_indexes = reorder_array_b2(file_lengths, file_indexes, space_indexes)
  return checksum_b2(ordered_file_indexes, file_lengths)


def b():
  with open(INPUT_FILE) as f:
    input_str = f.read()

    before_b1 = time.time()
    print(solve_b(input_str))
    after_b1 = time.time()
    print(after_b1 - before_b1)

    before_b2 = time.time()
    print(solve_b2(input_str))
    after_b2 = time.time()
    print(after_b2 - before_b2)



if __name__ == '__main__':
  a()
  b()