from pyoxigraph import NamedNode

from pyrdf_prefix.namespace import PredefinedNamespace


class RDF(PredefinedNamespace):
    """The RDF Concepts Vocabulary (RDF)"""

    # Conversion-Date: 2024-09-30T10:48+00:00
    # Source: http://www.w3.org/1999/02/22-rdf-syntax-ns#

    _nsBaseIri = "http://www.w3.org/1999/02/22-rdf-syntax-ns#"
    _issueWarning = True
    _withContainerMembershipProperty = True
    _nonPyIdentifiers = ()

    Alt: NamedNode
    """The class of containers of alternatives."""
    Bag: NamedNode
    """The class of unordered containers."""
    CompoundLiteral: NamedNode
    """A class representing a compound literal."""
    HTML: NamedNode
    """The datatype of RDF literals storing fragments of HTML content"""
    JSON: NamedNode
    """The datatype of RDF literals storing JSON content."""
    List: NamedNode
    """The class of RDF Lists."""
    PlainLiteral: NamedNode
    """The class of plain (i.e. untyped) literal values, as used in RIF and OWL 2"""
    Property: NamedNode
    """The class of RDF properties."""
    Seq: NamedNode
    """The class of ordered containers."""
    Statement: NamedNode
    """The class of RDF statements."""
    XMLLiteral: NamedNode
    """The datatype of XML literal values."""
    direction: NamedNode
    """The base direction component of a CompoundLiteral."""
    first: NamedNode
    """The first item in the subject RDF list."""
    langString: NamedNode
    """The datatype of language-tagged string values"""
    language: NamedNode
    """The language component of a CompoundLiteral."""
    nil: NamedNode
    """The empty list, with no items in it. If the rest of a list is nil then the list has no more items in it."""
    object: NamedNode
    """The object of the subject RDF statement."""
    predicate: NamedNode
    """The predicate of the subject RDF statement."""
    rest: NamedNode
    """The rest of the subject RDF list after the first item."""
    subject: NamedNode
    """The subject of the subject RDF statement."""
    type: NamedNode
    """The subject is an instance of a class."""
    value: NamedNode
    """Idiomatic property used for structured values."""
