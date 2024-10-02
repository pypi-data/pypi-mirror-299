from pyoxigraph import NamedNode

from pyrdf_prefix.namespace import PredefinedNamespace


class XML(PredefinedNamespace):
    """XML Namespace"""

    _nsBaseIri = "http://www.w3.org/XML/1998/namespace"
    _issueWarning = True

    # Handwritten

    lang: NamedNode
    """Designed for identifying the human language used in the scope of the element to which it's attached."""
    space: NamedNode
    """Designed to express whether or not the document's creator wishes white space to be considered as significant in the scope of the element to which it's attached."""
    base: NamedNode
    """The XML Base specification (Second edition) describes a facility, similar to that of HTML BASE, for defining base URIs for parts of XML documents. It defines a single attribute, xml:base, and describes in detail the procedure for its use in processing relative URI refeferences. """
    id: NamedNode
    """The xml:id specification defines a single attribute, xml:id, known to be of type ID independently of any DTD or schema."""
