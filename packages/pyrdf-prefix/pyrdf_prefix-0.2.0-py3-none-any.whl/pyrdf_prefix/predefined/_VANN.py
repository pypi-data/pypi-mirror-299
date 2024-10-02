from pyoxigraph import NamedNode

from pyrdf_prefix.namespace import PredefinedNamespace


class VANN(PredefinedNamespace):
    """VANN: A vocabulary for annotating vocabulary descriptions"""

    # Conversion-Date: 2024-09-30T10:48+00:00
    # Source: https://vocab.org/vann/vann-vocab-20100607.rdf

    _nsBaseIri = "http://purl.org/vocab/vann/"
    _issueWarning = True
    _withContainerMembershipProperty = False
    _nonPyIdentifiers = ()

    changes: NamedNode
    """A reference to a resource that describes changes between this version of a vocabulary and the previous."""
    example: NamedNode
    """A reference to a resource that provides an example of how this resource can be used."""
    preferredNamespacePrefix: NamedNode
    """The preferred namespace prefix to use when using terms from this vocabulary in an XML document."""
    preferredNamespaceUri: NamedNode
    """The preferred namespace URI to use when using terms from this vocabulary in an XML document."""
    termGroup: NamedNode
    """A group of related terms in a vocabulary."""
    usageNote: NamedNode
    """A reference to a resource that provides information on how this resource is to be used."""
