import os
from dataclasses import dataclass
from dataclasses import field
from typing import Any
from typing import List
from typing import Tuple

from graphviz import Digraph
from rdflib import Graph as RDFGraph

NTuple = Tuple[Any, ...]


@dataclass
class Graph(RDFGraph):
  triples: List[Tuple[Any, ...]] = field(default_factory=list)

  def clear(self):
    self.triples.clear()

  def append(self, nt: NTuple):
    if not nt in self.triples:
      self.triples.append(nt)

  def remove(self, nt: NTuple):
    if nt in self.triples:
      self.triples.remove(nt)

  def match(self, s=None, p=None, o=None):
    return [t for t in self.triples if
            (not s or t[0] == s)
            and (not p or t[1] == p)
            and (not o or t[2] == o)]

  def parse(self, uri, fmt='ttl'):
    g = RDFGraph().parse(uri, format=fmt)
    for s, p, o in g.triples((None, None, None)):
      self.append((s, p, o))

  def write(self, name):
    d = os.listdir(".")
    print(d)
    f = os.path.join("../coatingOntology_HAP", "%s.ttl"%name)
    out = open(f,'w')
    for t in self.triples:
        out.write(str(t))

    out.close()

  def path(self, origin, destination, link=None, visited=None):
    if link is None:
      link = [origin]
    if visited is None:
      visited = []

    visited.append(origin)
    for _, r, dest in self.match(origin, None, None):
      if not dest in visited:
        link.append(dest)
        print("forward", dest)
        if dest == destination:
          return link
        else:
          return self.path(dest, destination, link, visited)

    for dest, r, _ in self.match(None, None, origin):
      if not dest in visited:
        link.append(dest)
        print("reverse", dest)
        if dest == destination:
          return link
        else:
          return self.path(dest, destination, link, visited)
    return visited

  def plot(self, class_names=[]):
    """
    Create Digraph plot
    """
    dot = Digraph()
    # Add nodes 1 and 2
    for s, p, o in self.match():
      if s in class_names:
        dot.node(str(s),color='red', shape="rectangle")
      else:
        dot.node(str(s))

      if o in class_names:
        dot.node(str(o), color='red', shape="rectangle")
      else:
        dot.node(str(o))
      dot.edge(str(s), str(o), label=p)

    # Visualize the graph
    return dot

  def gen_cytoscape(self):
    nodes = []
    for s, p, o in self.match():
      nodes.append(str(s))
      nodes.append(str(o))

    edges = []
    for s, p, o in self.match():
      edges.append((str(s), str(p), str(o)))

    for s in set(nodes):
      print(f"{{ data: {{ id: '{s}' }} }},")

    for e in edges:
      s = e[0]
      p = e[1]
      o = e[2]
      print(f"{{ data: {{ id: '{p}_{s}_{o}', source: '{s}', target: '{o}', label: '{p}' }} }},")
