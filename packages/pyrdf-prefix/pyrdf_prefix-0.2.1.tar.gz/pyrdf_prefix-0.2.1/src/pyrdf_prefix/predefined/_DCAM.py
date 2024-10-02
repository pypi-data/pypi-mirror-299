from pyoxigraph import NamedNode

from pyrdf_prefix.namespace import PredefinedNamespace


class DCAM(PredefinedNamespace):
    """Dublin Core Abstract Model for vocabulary description"""

    # Conversion-Date: 2024-09-30T10:48+00:00
    # Source: https://www.dublincore.org/specifications/dublin-core/dcmi-terms/dublin_core_abstract_model.nt

    _nsBaseIri = "http://purl.org/dc/dcam/"
    _issueWarning = True
    _withContainerMembershipProperty = False
    _nonPyIdentifiers = ()

    VocabularyEncodingScheme: NamedNode
    """An enumerated set of resources."""
    domainIncludes: NamedNode
    """A suggested class for subjects of this property."""
    memberOf: NamedNode
    """A relationship between a resource and a vocabulary encoding scheme which indicates that the resource is a member of a set."""
    rangeIncludes: NamedNode
    """A suggested class for values of this property."""
