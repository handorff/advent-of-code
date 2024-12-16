import time
import math

INPUT_FILE = "07.in"


def test_line_helper(target, nums_left, total_so_far):
  if len(nums_left) == 0:
    return target == total_so_far

  test_add = test_line_helper(target, nums_left[1:], total_so_far + nums_left[0])
  test_mul = test_line_helper(target, nums_left[1:], total_so_far * nums_left[0])
  return test_add or test_mul


def test_line(target, nums):
  return test_line_helper(target, nums[1:], nums[0])


def parse_line(line):
  [a, b] = line.split(": ")
  target = int(a)
  nums = list(map(int, b.split(' ')))
  return (target, nums)


def a():
  with open(INPUT_FILE) as f:
    lines = f.read().split("\n")
    parsed_lines = [parse_line(line) for line in lines]
    print(sum(target for target, nums in parsed_lines if test_line(target, nums)))


def test_line_helper_b(target, nums_left, total_so_far):
  if len(nums_left) == 0:
    return target == total_so_far

  if total_so_far > target:
    return False

  test_add = test_line_helper_b(target, nums_left[1:], total_so_far + nums_left[0])
  test_mul = test_line_helper_b(target, nums_left[1:], total_so_far * nums_left[0])
  concat_result = int(str(total_so_far) + str(nums_left[0]))

  # num_digits = math.ceil(math.log10(nums_left[0] + 1))
  # concat_result = total_so_far * 10 ** num_digits + nums_left[0]

  test_concat = test_line_helper_b(target, nums_left[1:], concat_result)
  return test_add or test_mul or test_concat


def test_line_b(target, nums):
  return test_line_helper_b(target, nums[1:], nums[0])

def solve_b1(parsed_lines):
  return sum(target for target, nums in parsed_lines if test_line_b(target, nums))



def b():
  with open(INPUT_FILE) as f:
    lines = f.read().split("\n")
    parsed_lines = [parse_line(line) for line in lines]

    before_b1 = time.time()
    print(solve_b1(parsed_lines))
    after_b1 = time.time()
    print(after_b1 - before_b1)
    


if __name__ == '__main__':
  a()
  b()
