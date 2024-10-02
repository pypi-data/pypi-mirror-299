from pyoxigraph import NamedNode

from pyrdf_prefix.namespace import PredefinedNamespace


class LDP(PredefinedNamespace):
    """The W3C Linked Data Platform (LDP) Vocabulary"""

    # Conversion-Date: 2024-09-30T10:48+00:00
    # Source: https://www.w3.org/ns/ldp.ttl

    _nsBaseIri = "http://www.w3.org/ns/ldp#"
    _issueWarning = True
    _withContainerMembershipProperty = False
    _nonPyIdentifiers = ()

    Ascending: NamedNode
    """Ascending order."""
    BasicContainer: NamedNode
    """An LDPC that uses a predefined predicate to simply link to its contained resources."""
    Container: NamedNode
    """A Linked Data Platform RDF Source (LDP-RS) that also conforms to additional patterns and conventions for managing membership. Readers should refer to the specification defining this ontology for the list of behaviors associated with it."""
    Descending: NamedNode
    """Descending order."""
    DirectContainer: NamedNode
    """An LDPC that is similar to a LDP-DC but it allows an indirection with the ability to list as member a resource, such as a URI representing a real-world object, that is different from the resource that is created."""
    IndirectContainer: NamedNode
    """An LDPC that has the flexibility of choosing what form the membership triples take."""
    MemberSubject: NamedNode
    """Used to indicate default and typical behavior for ldp:insertedContentRelation, where the member-URI value in the membership triple added when a creation request is successful is the URI assigned to the newly created resource."""
    NonRDFSource: NamedNode
    """A Linked Data Platform Resource (LDPR) whose state is NOT represented as RDF."""
    Page: NamedNode
    """URI signifying that the resource is an in-sequence page resource, as defined by LDP Paging.  Typically used on Link rel='type' response headers."""
    PageSortCriterion: NamedNode
    """Element in the list of sorting criteria used by the server to assign container members to pages."""
    PreferContainment: NamedNode
    """URI identifying a LDPC's containment triples, for example to allow clients to express interest in receiving them."""
    PreferEmptyContainer: NamedNode
    """Archaic alias for ldp:PreferMinimalContainer"""
    PreferMembership: NamedNode
    """URI identifying a LDPC's membership triples, for example to allow clients to express interest in receiving them."""
    PreferMinimalContainer: NamedNode
    """URI identifying the subset of a LDPC's triples present in an empty LDPC, for example to allow clients to express interest in receiving them.  Currently this excludes containment and membership triples, but in the future other exclusions might be added.  This definition is written to automatically exclude those new classes of triples."""
    RDFSource: NamedNode
    """A Linked Data Platform Resource (LDPR) whose state is represented as RDF."""
    Resource: NamedNode
    """A HTTP-addressable resource whose lifecycle is managed by a LDP server."""
    constrainedBy: NamedNode
    """Links a resource with constraints that the server requires requests like creation and update to conform to."""
    contains: NamedNode
    """Links a container with resources created through the container."""
    hasMemberRelation: NamedNode
    """Indicates which predicate is used in membership triples, and that the membership triple pattern is < membership-constant-URI , object-of-hasMemberRelation, member-URI >."""
    inbox: NamedNode
    """Links a resource to a container where notifications for the resource can be created and discovered."""
    insertedContentRelation: NamedNode
    """Indicates which triple in a creation request should be used as the member-URI value in the membership triple added when the creation request is successful."""
    isMemberOfRelation: NamedNode
    """Indicates which predicate is used in membership triples, and that the membership triple pattern is < member-URI , object-of-isMemberOfRelation, membership-constant-URI >."""
    member: NamedNode
    """LDP servers should use this predicate as the membership predicate if there is no obvious predicate from an application vocabulary to use."""
    membershipResource: NamedNode
    """Indicates the membership-constant-URI in a membership triple.  Depending upon the membership triple pattern a container uses, as indicated by the presence of ldp:hasMemberRelation or ldp:isMemberOfRelation, the membership-constant-URI might occupy either the subject or object position in membership triples."""
    pageSequence: NamedNode
    """Link to a page sequence resource, as defined by LDP Paging.  Typically used to communicate the sorting criteria used to allocate LDPC members to pages."""
    pageSortCollation: NamedNode
    """The collation used to order the members across pages in a page sequence when comparing strings."""
    pageSortCriteria: NamedNode
    """Link to the list of sorting criteria used by the server in a representation.  Typically used on Link response headers as an extension link relation URI in the rel= parameter."""
    pageSortOrder: NamedNode
    """The ascending/descending/etc order used to order the members across pages in a page sequence."""
    pageSortPredicate: NamedNode
    """Predicate used to specify the order of the members across a page sequence's in-sequence page resources; it asserts nothing about the order of members in the representation of a single page."""
