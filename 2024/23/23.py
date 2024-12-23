from collections import defaultdict
from itertools import combinations

INPUT_FILE = "23.in"


def get_edges(lines):
  return [line.split("-") for line in lines]


def get_edge_dict(edges):
  d = defaultdict(set)
  for (a, b) in edges:
    d[a].add(b)
    d[b].add(a)
  return d


def a():
  with open(INPUT_FILE) as f:
    lines = f.read().split("\n")
    edges = get_edges(lines)
    edge_dict = get_edge_dict(edges)

    triangles = set()
    for a, b in edges:
      for c in edge_dict[a] & edge_dict[b]:
        triangles.add(tuple(sorted([a, b, c])))

    print(sum(1 for a, b, c in triangles if a[0] == 't' or b[0] == 't' or c[0] == 't'))


def get_nodes(edges):
  nodes = set()
  for n1, n2 in edges:
    nodes.add(n1)
    nodes.add(n2)
  return nodes


def is_clique(nodes, edge_dict):
  return all(n2 in edge_dict[n1] for n1, n2 in combinations(nodes, 2))


def solve_b(nodes, edge_dict):
  for k, v in edge_dict.items():
    # observe that each node has 13 adjacent edges
    assert len(v) == 13

    # try making a clique of size 14
    if is_clique(v, edge_dict):
      return sorted(list(v) + [k])    


  for k, v in edge_dict.items():
    # since that didn't work, try making a clique of size 13
    arr = list(v)
    for i in range(len(v)):
      new_v = set(arr[:i] + arr[i + 1:])
      if is_clique(new_v, edge_dict):
        return sorted(list(new_v) + [k])

  assert False


def b():
  with open(INPUT_FILE) as f:
    lines = f.read().split("\n")
    edges = get_edges(lines)
    edge_dict = get_edge_dict(edges)
    nodes = get_nodes(edges)
    print(','.join(solve_b(nodes, edge_dict)))
    


if __name__ == '__main__':
  a()
  b()