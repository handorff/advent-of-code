import math
from collections import defaultdict

INPUT_FILE = "11.in"

def blink_one(stone):
  if stone == 0:
    return [1]

  l = math.ceil(math.log10(stone + 1))
  if l % 2 == 0:
    n = 10 ** (l // 2)
    left = stone // n
    right = stone % n
    return [left, right]

  return [stone * 2024]


def blink_all(stones):
  new_stones = []
  for stone in stones:
    new_stones += blink_one(stone)
  return new_stones


def a():
  with open(INPUT_FILE) as f:
    stones = [int(s) for s in f.read().split(" ")]
    for _ in range(25):
      stones = blink_all(stones)
    print(len(stones))


def blink_all_b(stones_dict):
  new_stones_dict = defaultdict(int)

  for value, count in stones_dict.items():
    for new_value in blink_one(value):
      new_stones_dict[new_value] += count

  return new_stones_dict


def b():
  with open(INPUT_FILE) as f:
    stones = [int(s) for s in f.read().split(" ")]
    stones_dict = { stone: 1 for stone in stones }

    for i in range(75):
      stones_dict = blink_all_b(stones_dict)
    print(sum(stones_dict.values()))



if __name__ == '__main__':
  a()
  b()