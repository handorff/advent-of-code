INPUT_FILE = "01a.in"
from collections import Counter

def a():
  with open(INPUT_FILE) as f:
    lines = [line.split("   ") for line in f.read().split("\n")]
    left, right = zip(*lines)
    left = sorted(map(int, left))
    right = sorted(map(int, right))
    print(sum(abs(a - b) for a, b in zip(left, right)))
    
def b():
  with open(INPUT_FILE) as f:
    lines = [line.split("   ") for line in f.read().split("\n")]
    left, right = zip(*lines)
    left = map(int, left)
    right = map(int, right)
    counter = Counter(right)

    score = 0
    for l in left:
      score += l * counter[l]
    print(score)


if __name__ == '__main__':
  a()
  b()