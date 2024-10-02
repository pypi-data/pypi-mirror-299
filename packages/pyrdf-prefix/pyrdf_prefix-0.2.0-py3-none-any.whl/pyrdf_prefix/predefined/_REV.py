from pyoxigraph import NamedNode

from pyrdf_prefix.namespace import PredefinedNamespace


class REV(PredefinedNamespace):
    """RDF Review Vocabulary"""

    # Conversion-Date: 2024-09-30T10:48+00:00
    # Source: https://www.w3.org/archive/purl.org/stuff/rev.rdf

    _nsBaseIri = "http://purl.org/stuff/rev#"
    _issueWarning = True
    _withContainerMembershipProperty = False
    _nonPyIdentifiers = ()

    Comment: NamedNode
    """A comment on a review"""
    Feedback: NamedNode
    """Feedback on the review. Expresses whether the review was useful or not"""
    Review: NamedNode
    """A review of an work"""
    commenter: NamedNode
    """The commenter on the review"""
    hasComment: NamedNode
    """Used to associate a review with a comment on the review"""
    hasFeedback: NamedNode
    """Associates a review with a feedback on the review"""
    hasReview: NamedNode
    """Associates a work with a a review"""
    maxRating: NamedNode
    """A numeric value"""
    minRating: NamedNode
    """A numeric value"""
    positiveVotes: NamedNode
    """Number of positive usefulness votes (integer)"""
    rating: NamedNode
    """A numeric value"""
    reviewer: NamedNode
    """The person that has written the review"""
    text: NamedNode
    """The text of the review"""
    title: NamedNode
    """The title of the review"""
    totalVotes: NamedNode
    """Number of usefulness votes (integer)"""
    type: NamedNode
    """The type of media of a work under review"""
