from pyoxigraph import NamedNode

from pyrdf_prefix.namespace import PredefinedNamespace


class DCMITYPE(PredefinedNamespace):
    """Dublin Core DCMI Type Vocabulary"""

    # Conversion-Date: 2024-09-30T10:48+00:00
    # Source: https://www.dublincore.org/specifications/dublin-core/dcmi-terms/dublin_core_type.nt

    _nsBaseIri = "http://purl.org/dc/dcmitype/"
    _issueWarning = True
    _withContainerMembershipProperty = False
    _nonPyIdentifiers = ()

    Collection: NamedNode
    """An aggregation of resources."""
    Dataset: NamedNode
    """Data encoded in a defined structure."""
    Event: NamedNode
    """A non-persistent, time-based occurrence."""
    Image: NamedNode
    """A visual representation other than text."""
    InteractiveResource: NamedNode
    """A resource requiring interaction from the user to be understood, executed, or experienced."""
    MovingImage: NamedNode
    """A series of visual representations imparting an impression of motion when shown in succession."""
    PhysicalObject: NamedNode
    """An inanimate, three-dimensional object or substance."""
    Service: NamedNode
    """A system that provides one or more functions."""
    Software: NamedNode
    """A computer program in source or compiled form."""
    Sound: NamedNode
    """A resource primarily intended to be heard."""
    StillImage: NamedNode
    """A static visual representation."""
    Text: NamedNode
    """A resource consisting primarily of words for reading."""
