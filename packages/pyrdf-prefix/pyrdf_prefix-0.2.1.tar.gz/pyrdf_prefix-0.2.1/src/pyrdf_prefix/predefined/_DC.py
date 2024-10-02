from pyoxigraph import NamedNode

from pyrdf_prefix.namespace import PredefinedNamespace


class DC(PredefinedNamespace):
    """Dublin Core DCMI Metadata Terms"""

    # Conversion-Date: 2024-09-30T10:48+00:00
    # Source: https://www.dublincore.org/specifications/dublin-core/dcmi-terms/dublin_core_terms.nt

    _nsBaseIri = "http://purl.org/dc/terms/"
    _issueWarning = True
    _withContainerMembershipProperty = False
    _nonPyIdentifiers = ("ISO639-2", "ISO639-3")

    Agent: NamedNode
    """A resource that acts or has the power to act."""
    AgentClass: NamedNode
    """A group of agents."""
    BibliographicResource: NamedNode
    """A book, article, or other documentary resource."""
    Box: NamedNode
    """The set of regions in space defined by their geographic coordinates according to the DCMI Box Encoding Scheme."""
    DCMIType: NamedNode
    """The set of classes specified by the DCMI Type Vocabulary, used to categorize the nature or genre of the resource."""
    DDC: NamedNode
    """The set of conceptual resources specified by the Dewey Decimal Classification."""
    FileFormat: NamedNode
    """A digital resource format."""
    Frequency: NamedNode
    """A rate at which something recurs."""
    IMT: NamedNode
    """The set of media types specified by the Internet Assigned Numbers Authority."""
    ISO3166: NamedNode
    """The set of codes listed in ISO 3166-1 for the representation of names of countries."""
    Jurisdiction: NamedNode
    """The extent or range of judicial, law enforcement, or other authority."""
    LCC: NamedNode
    """The set of conceptual resources specified by the Library of Congress Classification."""
    LCSH: NamedNode
    """The set of labeled concepts specified by the Library of Congress Subject Headings."""
    LicenseDocument: NamedNode
    """A legal document giving official permission to do something with a resource."""
    LinguisticSystem: NamedNode
    """A system of signs, symbols, sounds, gestures, or rules used in communication."""
    Location: NamedNode
    """A spatial region or named place."""
    LocationPeriodOrJurisdiction: NamedNode
    """A location, period of time, or jurisdiction."""
    MESH: NamedNode
    """The set of labeled concepts specified by the Medical Subject Headings."""
    MediaType: NamedNode
    """A file format or physical medium."""
    MediaTypeOrExtent: NamedNode
    """A media type or extent."""
    MethodOfAccrual: NamedNode
    """A method by which resources are added to a collection."""
    MethodOfInstruction: NamedNode
    """A process that is used to engender knowledge, attitudes, and skills."""
    NLM: NamedNode
    """The set of conceptual resources specified by the National Library of Medicine Classification."""
    Period: NamedNode
    """The set of time intervals defined by their limits according to the DCMI Period Encoding Scheme."""
    PeriodOfTime: NamedNode
    """An interval of time that is named or defined by its start and end dates."""
    PhysicalMedium: NamedNode
    """A physical material or carrier."""
    PhysicalResource: NamedNode
    """A material thing."""
    Point: NamedNode
    """The set of points in space defined by their geographic coordinates according to the DCMI Point Encoding Scheme."""
    Policy: NamedNode
    """A plan or course of action by an authority, intended to influence and determine decisions, actions, and other matters."""
    ProvenanceStatement: NamedNode
    """Any changes in ownership and custody of a resource since its creation that are significant for its authenticity, integrity, and interpretation."""
    RFC1766: NamedNode
    """The set of tags, constructed according to RFC 1766, for the identification of languages."""
    RFC3066: NamedNode
    """The set of tags constructed according to RFC 3066 for the identification of languages."""
    RFC4646: NamedNode
    """The set of tags constructed according to RFC 4646 for the identification of languages."""
    RFC5646: NamedNode
    """The set of tags constructed according to RFC 5646 for the identification of languages."""
    RightsStatement: NamedNode
    """A statement about the intellectual property rights (IPR) held in or over a resource, a legal document giving official permission to do something with a resource, or a statement about access rights."""
    SizeOrDuration: NamedNode
    """A dimension or extent, or a time taken to play or execute."""
    Standard: NamedNode
    """A reference point against which other things can be evaluated or compared."""
    TGN: NamedNode
    """The set of places specified by the Getty Thesaurus of Geographic Names."""
    UDC: NamedNode
    """The set of conceptual resources specified by the Universal Decimal Classification."""
    URI: NamedNode
    """The set of identifiers constructed according to the generic syntax for Uniform Resource Identifiers as specified by the Internet Engineering Task Force."""
    W3CDTF: NamedNode
    """The set of dates and times constructed according to the W3C Date and Time Formats Specification."""
    abstract: NamedNode
    """A summary of the resource."""
    accessRights: NamedNode
    """Information about who access the resource or an indication of its security status."""
    accrualMethod: NamedNode
    """The method by which items are added to a collection."""
    accrualPeriodicity: NamedNode
    """The frequency with which items are added to a collection."""
    accrualPolicy: NamedNode
    """The policy governing the addition of items to a collection."""
    alternative: NamedNode
    """An alternative name for the resource."""
    audience: NamedNode
    """A class of agents for whom the resource is intended or useful."""
    available: NamedNode
    """Date that the resource became or will become available."""
    bibliographicCitation: NamedNode
    """A bibliographic reference for the resource."""
    conformsTo: NamedNode
    """An established standard to which the described resource conforms."""
    contributor: NamedNode
    """An entity responsible for making contributions to the resource."""
    coverage: NamedNode
    """The spatial or temporal topic of the resource, spatial applicability of the resource, or jurisdiction under which the resource is relevant."""
    created: NamedNode
    """Date of creation of the resource."""
    creator: NamedNode
    """An entity responsible for making the resource."""
    date: NamedNode
    """A point or period of time associated with an event in the lifecycle of the resource."""
    dateAccepted: NamedNode
    """Date of acceptance of the resource."""
    dateCopyrighted: NamedNode
    """Date of copyright of the resource."""
    dateSubmitted: NamedNode
    """Date of submission of the resource."""
    description: NamedNode
    """An account of the resource."""
    educationLevel: NamedNode
    """A class of agents, defined in terms of progression through an educational or training context, for which the described resource is intended."""
    extent: NamedNode
    """The size or duration of the resource."""
    format: NamedNode
    """The file format, physical medium, or dimensions of the resource."""
    hasFormat: NamedNode
    """A related resource that is substantially the same as the pre-existing described resource, but in another format."""
    hasPart: NamedNode
    """A related resource that is included either physically or logically in the described resource."""
    hasVersion: NamedNode
    """A related resource that is a version, edition, or adaptation of the described resource."""
    identifier: NamedNode
    """An unambiguous reference to the resource within a given context."""
    instructionalMethod: NamedNode
    """A process, used to engender knowledge, attitudes and skills, that the described resource is designed to support."""
    isFormatOf: NamedNode
    """A pre-existing related resource that is substantially the same as the described resource, but in another format."""
    isPartOf: NamedNode
    """A related resource in which the described resource is physically or logically included."""
    isReferencedBy: NamedNode
    """A related resource that references, cites, or otherwise points to the described resource."""
    isReplacedBy: NamedNode
    """A related resource that supplants, displaces, or supersedes the described resource."""
    isRequiredBy: NamedNode
    """A related resource that requires the described resource to support its function, delivery, or coherence."""
    isVersionOf: NamedNode
    """A related resource of which the described resource is a version, edition, or adaptation."""
    issued: NamedNode
    """Date of formal issuance of the resource."""
    language: NamedNode
    """A language of the resource."""
    license: NamedNode
    """A legal document giving official permission to do something with the resource."""
    mediator: NamedNode
    """An entity that mediates access to the resource."""
    medium: NamedNode
    """The material or physical carrier of the resource."""
    modified: NamedNode
    """Date on which the resource was changed."""
    provenance: NamedNode
    """A statement of any changes in ownership and custody of the resource since its creation that are significant for its authenticity, integrity, and interpretation."""
    publisher: NamedNode
    """An entity responsible for making the resource available."""
    references: NamedNode
    """A related resource that is referenced, cited, or otherwise pointed to by the described resource."""
    relation: NamedNode
    """A related resource."""
    replaces: NamedNode
    """A related resource that is supplanted, displaced, or superseded by the described resource."""
    requires: NamedNode
    """A related resource that is required by the described resource to support its function, delivery, or coherence."""
    rights: NamedNode
    """Information about rights held in and over the resource."""
    rightsHolder: NamedNode
    """A person or organization owning or managing rights over the resource."""
    source: NamedNode
    """A related resource from which the described resource is derived."""
    spatial: NamedNode
    """Spatial characteristics of the resource."""
    subject: NamedNode
    """A topic of the resource."""
    tableOfContents: NamedNode
    """A list of subunits of the resource."""
    temporal: NamedNode
    """Temporal characteristics of the resource."""
    title: NamedNode
    """A name given to the resource."""
    type: NamedNode
    """The nature or genre of the resource."""
    valid: NamedNode
    """Date (often a range) of validity of a resource."""
