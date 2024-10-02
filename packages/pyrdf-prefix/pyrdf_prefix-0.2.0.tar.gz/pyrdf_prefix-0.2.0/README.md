# pyrdf-prefix

This project provides a `Prefix` utility and many predefined prefixes for many popular RDF vocabularies, like RDFS, SHACL, SKOS and OWL.
It returns `NamedNode`s to be used with [pyoxigraph].

[pyoxigraph]: https://github.com/oxigraph/oxigraph

## Usage

```py
from pyoxigraph import NamedNode
from pyrdf_prefix import Prefix

EX = Prefix('https://example.org/ns#')
assert EX.Sponge == NamedNode('https://example.org/ns#Sponge')
assert EX['Crusty-Crab'] == NamedNode('https://example.org/ns#Crusty-Crab')
```

It also predefines many well-known prefixes, like `rdf`, `skos`, `sh`:

```py
from pyrdf_prefix import RDF, SKOS, SH
from pyoxigraph import Quad

def describe():
    return Quad(EX.MyRestaurant, RDF.type, SKOS.Concept)
```
