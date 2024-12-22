from collections import defaultdict

INPUT_FILE = "22.in"


def mix(a, b):
  return a ^ b


def prune(a):
  return a % 16777216


def next_secret(n):
  n = mix(n, n * 64)
  n = prune(n)
  n = mix(n, n // 32)
  n = prune(n)
  n = mix(n, n * 2048)
  n = prune(n)
  return n


def ith_secret(n, i):
  for _ in range(i):
    n = next_secret(n)
  return n


def a():
  with open(INPUT_FILE) as f:
    lines = f.read().split("\n")
    nums = [int(line) for line in lines]

    print(sum(ith_secret(n, 2000) for n in nums))


def prices(n):
  secret_numbers = [n]
  curr = n

  for _ in range(2000):
    curr = next_secret(curr)
    secret_numbers.append(curr)

  return [s % 10 for s in secret_numbers]


def do_policy(policy, prices):
  for i in range(len(prices) - 4):
    if all(prices[i + j + 1] - prices[i + j] == policy[j] for j in range(4)):
      return prices[i + 4]
  return 0


def b():
  with open(INPUT_FILE) as f:
    lines = f.read().split("\n")
    nums = [int(line) for line in lines]

    policies_to_bananas = defaultdict(int)

    for n in nums:
      seen = set()
      p = prices(n)
      for i in range(len(p) - 4):
        policy = tuple(p[i + j + 1] - p[i + j] for j in range(4))
        bananas = p[i + 4]
        if policy not in seen:
          seen.add(policy)
          policies_to_bananas[policy]+= bananas

    print(max(policies_to_bananas.values()))


if __name__ == '__main__':
  a()
  b()