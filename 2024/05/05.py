INPUT_FILE = "05.in"
# from functools import cmp_to_key

def parse_rule(line):
  [before, after] = line.split("|")
  return (int(before), int(after))

def parse_update(line):
  return list(map(int, line.split(",")))

### This approach doesn't work because it's not guaranteed to be transitive, apparently
# def all_page_numbers(rules):
#   return list(set([rule[0] for rule in rules] + [rule[1] for rule in rules]))
  
# def sort(rules, pages):
#   return sorted(pages, key=cmp_to_key(lambda p1, p2: -1 if (p1, p2) in rules else 1))

# def ranks(pages):
#   return {p: i for i, p in enumerate(pages)}

# def is_correct(page_ranks, update):
#   for a, b in zip(update, update[1:]):
#     if page_ranks[a] > page_ranks[b]:
#       return False
#   return True

# def correct_update(page_ranks, update):
#   return sorted(update, key=lambda u: page_ranks[u])

def is_correct(rules, update):
  for i, entry in enumerate(update):
    before = update[:i]
    after = update[i+1:]

    for b in before:
      if (entry, b) in rules:
        return False
    for a in after:
      if (a, entry) in rules:
        return False
  return True

def middle(update):
  return update[(len(update) - 1) // 2]

def a():
  with open(INPUT_FILE) as f:
    [rules_str, updates_str] = f.read().split("\n\n")
    rules = [parse_rule(line) for line in rules_str.split("\n")]
    updates = [parse_update(line) for line in updates_str.split("\n")]
    ordered = [update for update in updates if is_correct(rules, update)]
    print(sum(middle(update) for update in ordered))

def correct_update(rules, pages):
  if len(pages) <= 1:
    return pages

  p = pages[0]
  before_p = [r[0] for r in rules if r[1] == p and r[0] in pages]
  after_p = [r[1] for r in rules if r[0] == p and r[1] in pages]
  return correct_update(rules, before_p) + [p] + correct_update(rules, after_p)

def b():
  with open(INPUT_FILE) as f:
    [rules_str, updates_str] = f.read().split("\n\n")
    rules = [parse_rule(line) for line in rules_str.split("\n")]
    updates = [parse_update(line) for line in updates_str.split("\n")]
    incorrect = [update for update in updates if not is_correct(rules, update)]
    corrected = [correct_update(rules, update) for update in incorrect]
    print(sum(middle(update) for update in corrected))

if __name__ == '__main__':
  a()
  b()