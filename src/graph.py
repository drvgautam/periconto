import uuid
from typing import Tuple, List, Dict, Any, Optional
from dataclasses import dataclass, field
from functools import reduce
from rdflib import Graph as RDFGraph
from graphviz import Digraph

NTuple = Tuple[Any, ...]

@dataclass
class Graph:
    triples: List[Tuple[Any, ...]] = field(default_factory=list)
    
    def clear(self):
        self.triples.clear()
        
    def append(self, nt: NTuple):
        if not nt in self.triples:
            self.triples.append(nt)

    def remove(self, nt:NTuple):
        if nt in self.triples:
            self.triples.remove(nt)
        
    def match(self, s = None, p = None, o = None):        
        return [t for t in self.triples if 
                (not s or t[0] == s) 
                and (not p or t[1] == p)
                and (not o or t[2] == o)]
    def parse(self, uri, fmt='ttl'):
        g = RDFGraph().parse(uri, format=fmt)
        for s, p, o in g.triples((None, None, None)):
            self.append((s, p, o))
            
    
    def path(self, origin, destination, link=None, visited=None):        
        if link is None:
            link = [origin]
        if visited is None:
            visited = []
            
        visited.append(origin)
        for _, r, dest in self.match(origin, None, None):            
            if not dest in visited:
                link.append(dest)
                print ("forward", dest)
                if dest == destination:                
                    return link
                else:                    
                    return self.path(dest, destination, link, visited)

        for dest, r, _ in self.match(None, None, origin):            
            if not dest in visited:
                link.append(dest)
                print ("reverse", dest)
                if dest == destination:                
                    return link
                else:                    
                    return self.path(dest, destination, link, visited)
        return visited        
        
    def plot(self):
        """
        Create Digraph plot
        """
        dot = Digraph()
        # Add nodes 1 and 2
        for s, p, o in self.match():
            dot.node(str(s))
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
            print (f"{{ data: {{ id: '{s}' }} }},")
        
        for e in edges:
            s = e[0]
            p = e[1]
            o = e[2]
            print (f"{{ data: {{ id: '{p}_{s}_{o}', source: '{s}', target: '{o}', label: '{p}' }} }},")

    #
    # def makeTree(self, origin):
    #
    #     for _, r, dest in self.match(origin, None, None):
    #
    #
    #         if not dest in visited:
    #             link.append(dest)
    #             print("forward", dest)
    #             if dest == destination:
    #                 return link
    #             else:
    #                 return self.path(dest, destination, link, visited)
    #
    #
    #
    #     pass
    def walkDepthFirstFnc(tree, id):
        """
        walk a tree depth first iteratively
        :param tree: container with node and its children specified tree[#node]["children" ]
        :param id: #node
        :return: nodes
        """
        nodes = []
        stack = [id]
        while stack:
            cur_node = stack[0]
            stack = stack[1:]
            nodes.append(cur_node)
            for child in reversed(tree[cur_node]["children"]):
                stack.insert(0, child)
        return nodes