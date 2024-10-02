from pyoxigraph import NamedNode

from pyrdf_prefix.namespace import PredefinedNamespace


class RDFS(PredefinedNamespace):
    """The RDF Schema vocabulary (RDFS)"""

    # Conversion-Date: 2024-09-30T10:48+00:00
    # Source: http://www.w3.org/2000/01/rdf-schema#

    _nsBaseIri = "http://www.w3.org/2000/01/rdf-schema#"
    _issueWarning = True
    _withContainerMembershipProperty = False
    _nonPyIdentifiers = ()

    Class: NamedNode
    """The class of classes."""
    Container: NamedNode
    """The class of RDF containers."""
    ContainerMembershipProperty: NamedNode
    """The class of container membership properties, rdf:_1, rdf:_2, ...,
                    all of which are sub-properties of 'member'."""
    Datatype: NamedNode
    """The class of RDF datatypes."""
    Literal: NamedNode
    """The class of literal values, eg. textual strings and integers."""
    Resource: NamedNode
    """The class resource, everything."""
    comment: NamedNode
    """A description of the subject resource."""
    domain: NamedNode
    """A domain of the subject property."""
    isDefinedBy: NamedNode
    """The defininition of the subject resource."""
    label: NamedNode
    """A human-readable name for the subject."""
    member: NamedNode
    """A member of the subject resource."""
    range: NamedNode
    """A range of the subject property."""
    seeAlso: NamedNode
    """Further information about the subject resource."""
    subClassOf: NamedNode
    """The subject is a subclass of a class."""
    subPropertyOf: NamedNode
    """The subject is a subproperty of a property."""
