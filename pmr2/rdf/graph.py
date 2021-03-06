from cStringIO import StringIO
from lxml import etree

import rdflib

from rdflib.graph import ConjunctiveGraph, Graph
PMR2Graph = ConjunctiveGraph
namespaces = {
    'rdf': 'http://www.w3.org/1999/02/22-rdf-syntax-ns#',
}

def parseXML(source, publicID=None, context=None, **args):

    if not hasattr(source, 'read'):
        source = StringIO(source)

    if context is None:
        context = Graph()

    rdfnodes = []
    xpath_expr = [
        './/rdf:RDF',
        '/rdf:RDF',
    ]
    dom = etree.parse(source)
    for expr in xpath_expr:
        rdfnodes.extend(dom.xpath(expr, namespaces=namespaces))
    for node in rdfnodes:
        s = StringIO(etree.tostring(node))
        s.seek(0)
        context.parse(s, publicID=publicID, format='xml', **args)
    return context
