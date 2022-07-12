from rdflib import Graph, Namespace, Literal, RDF

base = "http://test.com/ns#"
foobar = Namespace("http://test.com/ns")
g = Graph(base = base)
g.bind('foobar', foobar)

g.add((foobar.something, RDF.type, Literal('Blah')))
g.add((foobar.something, foobar.contains, Literal('a property')))

g.add((foobar.anotherthing, RDF.type, Literal('Blubb')))
g.add((foobar.anotherthing, foobar.contains, Literal('another property')))

print(g.serialize(format='turtle'))

dev
# just to test the merge feature

main
