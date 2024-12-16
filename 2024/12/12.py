from collections import defaultdict

INPUT_FILE = "12.in"

def in_bounds(i, j, bounds):
  return i >= 0 and j >= 0 and i < bounds[0] and j < bounds[1]

def neighbor_indexes(i, j, bounds):
  all_neighbors = [(i + 1, j), (i - 1, j), (i, j + 1), (i, j - 1)]
  return [(x, y) for x, y in all_neighbors if in_bounds(x, y, bounds)]

def get_regions(lines):
  bounds = (len(lines), len(lines[0]))

  visited = set()
  to_visit = set()
  for i in range(bounds[0]):
    for j in range(bounds[1]):
      to_visit.add((i, j))

  regions = []
  while len(to_visit) > 0:
    v = to_visit.pop()
    to_visit.add(v) # meh
    q = [v]

    region = []
    while len(q) > 0:
      curr = q.pop(0)
      i, j = curr
      region.append(curr)
      visited.add(curr)
      to_visit.remove(curr)

      for ni, nj in neighbor_indexes(i, j, bounds):
        if lines[i][j] == lines[ni][nj] and (ni, nj) not in visited and (ni, nj) not in q:
          q.append((ni, nj))

    regions.append(region)

  return regions

def get_area(region):
  return len(region)

def get_perimeter(region):
  added = set()
  perimeter = 4 * len(region)

  for i, j in region:
    all_neighbors = [(i + 1, j), (i - 1, j), (i, j + 1), (i, j - 1)]
    shared_edges = sum(1 for x, y in all_neighbors if (x, y) in added)
    perimeter -= 2 * shared_edges
    added.add((i, j))

  return perimeter



def price_region(region):
  return get_area(region) * get_perimeter(region)


def price_regions(regions):
  return sum(price_region(region) for region in regions)


def a():
  with open(INPUT_FILE) as f:
    lines = f.read().split("\n")
    regions = get_regions(lines)
    print(price_regions(regions))

def get_sides(region):
  # let's say region (i, j) has four edges:
  # (i, j) -> (i + 1, j)          vertical
  # (i, j) -> (i, j + 1)          horizontal
  # (i + 1, j) -> (i + 1, j + 1)  horizontal
  # (i, j + 1) -> (i + 1, j + 1)  vertical
  
  horizontal_edges = set()
  vertical_edges = set()
  for i, j in region:
    h = [((i, j), (i, j + 1)), ((i + 1, j), (i + 1, j + 1))]
    v = [((i, j), (i + 1, j)), ((i, j + 1), (i + 1, j + 1))]

    # we only care about exterior edges
    # these are the ones contained exactly once in the total set of edges
    for e in h:
      if e in horizontal_edges:
        horizontal_edges.remove(e)
      else:
        horizontal_edges.add(e)

    for e in v:
      if e in vertical_edges:
        vertical_edges.remove(e)
      else:
        vertical_edges.add(e)

  h_groups = defaultdict(list)
  for e in horizontal_edges:
    h_groups[e[0][0]].append(e)

  v_groups = defaultdict(list)
  for e in vertical_edges:
    v_groups[e[0][1]].append(e)


  num_sides = 0
  for group in h_groups.values():
    group = sorted(group, key=lambda e: e[0][1])
    group = [e[0][1] for e in group]
    ds = [n - m for m, n in zip(group, group[1:])]
    num_sides += 1 + sum(1 for d in ds if d != 1)


  for group in v_groups.values():
    group = sorted(group, key=lambda e: e[0][0])
    group = [e[0][0] for e in group]
    ds = [n - m for m, n in zip(group, group[1:])]
    num_sides += 1 + sum(1 for d in ds if d != 1)

  # awful hack to patch this example
  # AAAAAA
  # AAABBA
  # AAABBA
  # ABBAAA
  # ABBAAA
  # AAAAAA
  for x in range(min(r[0] for r in region), max(r[0] for r in region) + 1):
    for y in range(min(r[1] for r in region), max(r[1] for r in region) + 1):
      if ((x, y), (x, y + 1)) in horizontal_edges and ((x, y - 1), (x, y)) in horizontal_edges and ((x, y), (x + 1, y)) in vertical_edges and ((x - 1, y), (x, y)) in vertical_edges:
        num_sides += 2

  return num_sides


def price_region_b(region):
  return get_area(region) * get_sides(region)

def price_regions_b(regions):
  return sum(price_region_b(region) for region in regions)


def b():
  with open(INPUT_FILE) as f:
    lines = f.read().split("\n")
    regions = get_regions(lines)
    print(price_regions_b(regions))


if __name__ == '__main__':
  a()
  b()