from pyoxigraph import NamedNode

from pyrdf_prefix.namespace import PredefinedNamespace


class WDRS(PredefinedNamespace):
    """Protocol for Web Description Resources (POWDER)"""

    # Conversion-Date: 2024-09-30T10:48+00:00
    # Source: https://www.w3.org/2007/05/powder-s.rdf

    _nsBaseIri = "http://www.w3.org/2007/05/powder-s#"
    _issueWarning = True
    _withContainerMembershipProperty = False
    _nonPyIdentifiers = ()

    Document: NamedNode
    """A POWDER document."""
    Processor: NamedNode
    """A software agent able to process POWDER documents."""
    authenticate: NamedNode
    """A pointer to a document that describes how Description Resources created by a FOAF Agent or a DC Terms Agent may be authenticated"""
    certified: NamedNode
    """A property that takes a Boolean value to declare whether the author of the data certifies the described resource."""
    certifiedby: NamedNode
    """A property that links a resource to a POWDER document that certifies it."""
    data_error: NamedNode
    """A property denoting a description of the specific error found in a given POWDER document."""
    describedby: NamedNode
    """An RDF property to exactly match the describedby relationship type introduced in http://www.w3.org/TR/powder-dr/#assoc-linking and formally defined in appendix D of the same document, i.e. the relationship A 'describedby' B asserts that resource B provides a description of resource A. There are no constraints on the format or representation of either A or B, neither are there any further constraints on either resource."""
    error_code: NamedNode
    """A property denoting the code of any error encountered by the POWDER processor."""
    hasIRI: NamedNode
    """This property is meant to be used in OWL2 instead of wdrs:matchesregex. It denotes the string data range corresponding to a set of IRIs."""
    issuedby: NamedNode
    """This property denotes the author of a POWDER document."""
    logo: NamedNode
    """Points to a graphic summary for the resources in a given class. Typically, it is a logo denoting conformance of a given (set of) resource(s) to a given set of criteria."""
    matchesregex: NamedNode
    """This is the key 'include' property for IRI set definitions in POWDER-S. It is necessary to take account of the POWDER Semantic Extension to process this fully. The value is a regular expression that is matched against an IRI."""
    notknownto: NamedNode
    """Property used in results returned from a POWDER Processor that has no data about the candidate resource. The value is the IRI of the processor."""
    notmatchesregex: NamedNode
    """This is the key 'exclude' property for IRI set definitions in POWDER-S. It is necessary to take account of the POWDER Semantic Extension to process this fully. The value is a regular expression that is matched against an IRI."""
    proc_error: NamedNode
    """A property denoting a description of the specific software error."""
    sha1sum: NamedNode
    """Links to a Base64-encoded binary SHA-1 hash of the described resource. May be used by POWDER Processors when assessing trustworthiness of a DR."""
    supportedby: NamedNode
    """A property that links a POWDER document to some other data source that supports the descriptions provided."""
    tag: NamedNode
    """Property linking to a free-text tag which may include spaces."""
    text: NamedNode
    """This property provides a summary of the descriptorset that it annotates, suitable for display to end users."""
    validfrom: NamedNode
    """Provides a timestamp that a POWDER Processor may use when assessing trustworthiness of a POWDER document. Informally, a POWDER Processor should normally ignore data in the document before the given date."""
    validuntil: NamedNode
    """Provides a timestamp that a POWDER Processor may use when assessing trustworthiness of a POWDER document. Informally, a POWDER Processor should normally ignore data in the document after the given date."""


DESCRIBEDBY = WDRS.describedby
