from pyoxigraph import NamedNode

from pyrdf_prefix.namespace import PredefinedNamespace


class DC11(PredefinedNamespace):
    """Dublin Core (the original fifteen-element)"""

    # Conversion-Date: 2024-09-30T10:48+00:00
    # Source: https://www.dublincore.org/specifications/dublin-core/dcmi-terms/dublin_core_elements.nt

    _nsBaseIri = "http://purl.org/dc/elements/1.1/"
    _issueWarning = True
    _withContainerMembershipProperty = False
    _nonPyIdentifiers = ()

    contributor: NamedNode
    """An entity responsible for making contributions to the resource."""
    coverage: NamedNode
    """The spatial or temporal topic of the resource, spatial applicability of the resource, or jurisdiction under which the resource is relevant."""
    creator: NamedNode
    """An entity primarily responsible for making the resource."""
    date: NamedNode
    """A point or period of time associated with an event in the lifecycle of the resource."""
    description: NamedNode
    """An account of the resource."""
    format: NamedNode
    """The file format, physical medium, or dimensions of the resource."""
    identifier: NamedNode
    """An unambiguous reference to the resource within a given context."""
    language: NamedNode
    """A language of the resource."""
    publisher: NamedNode
    """An entity responsible for making the resource available."""
    relation: NamedNode
    """A related resource."""
    rights: NamedNode
    """Information about rights held in and over the resource."""
    source: NamedNode
    """A related resource from which the described resource is derived."""
    subject: NamedNode
    """The topic of the resource."""
    title: NamedNode
    """A name given to the resource."""
    type: NamedNode
    """The nature or genre of the resource."""
