from pyoxigraph import NamedNode

from pyrdf_prefix.namespace import PredefinedNamespace


class DUV(PredefinedNamespace):
    """Dataset Usage Vocabulary"""

    # Conversion-Date: 2024-09-30T10:48+00:00
    # Source: http://www.w3.org/ns/duv#

    _nsBaseIri = "http://www.w3.org/ns/duv#"
    _issueWarning = True
    _withContainerMembershipProperty = False
    _nonPyIdentifiers = ()

    RatingFeedback: NamedNode
    """Predefined criteria used to express a user opinion about a dataset or distribution using a discrete range of values."""
    Usage: NamedNode
    """A helpful description of actions that can be performed on a given dataset or distribution."""
    UsageTool: NamedNode
    """A synopsis describing the way a tool can use a dataset or distribution."""
    UserFeedback: NamedNode
    """User feedback on the dataset. Expresses whether the dataset was useful or not, for example."""
    hasDistributor: NamedNode
    """The distributor is the organization that makes the dataset available for downloading and use."""
    hasFeedback: NamedNode
    """User feedback associated with Dataset or distribution"""
    hasRating: NamedNode
    """Rating Feedback has rating opinion"""
    hasUsage: NamedNode
    """Dataset/distribution usage guidance or instructions."""
    hasUsageTool: NamedNode
    """Describes the tool that provides the Usage """
    refersTo: NamedNode
    """Dataset associated with Usage. """
