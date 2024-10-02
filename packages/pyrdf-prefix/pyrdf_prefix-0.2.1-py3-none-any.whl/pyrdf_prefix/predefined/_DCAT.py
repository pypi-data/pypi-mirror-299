from pyoxigraph import NamedNode

from pyrdf_prefix.namespace import PredefinedNamespace


class DCAT(PredefinedNamespace):
    """Data catalog vocabulary"""

    # Conversion-Date: 2024-09-30T10:48+00:00
    # Source: https://www.w3.org/ns/dcat2.ttl

    _nsBaseIri = "http://www.w3.org/ns/dcat#"
    _issueWarning = True
    _withContainerMembershipProperty = False
    _nonPyIdentifiers = ()

    Catalog: NamedNode
    """A curated collection of metadata about resources (e.g., datasets and data services in the context of a data catalog)."""
    CatalogRecord: NamedNode
    """A record in a data catalog, describing the registration of a single dataset or data service."""
    DataService: NamedNode
    """A site or end-point providing operations related to the discovery of, access to, or processing functions on, data or related resources."""
    Dataset: NamedNode
    """A collection of data, published or curated by a single source, and available for access or download in one or more represenations."""
    Distribution: NamedNode
    """A specific representation of a dataset. A dataset might be available in multiple serializations that may differ in various ways, including natural language, media-type or format, schematic organization, temporal and spatial resolution, level of detail or profiles (which might specify any or all of the above)."""
    Relationship: NamedNode
    """An association class for attaching additional information to a relationship between DCAT Resources."""
    Resource: NamedNode
    """Resource published or curated by a single agent."""
    Role: NamedNode
    """A role is the function of a resource or agent with respect to another resource, in the context of resource attribution or resource relationships."""
    accessService: NamedNode
    """A site or end-point that gives access to the distribution of the dataset."""
    accessURL: NamedNode
    """A URL of a resource that gives access to a distribution of the dataset. E.g. landing page, feed, SPARQL endpoint. Use for all cases except a simple download link, in which case downloadURL is preferred."""
    bbox: NamedNode
    """The geographic bounding box of a resource."""
    byteSize: NamedNode
    """The size of a distribution in bytes."""
    catalog: NamedNode
    """A catalog whose contents are of interest in the context of this catalog."""
    centroid: NamedNode
    """The geographic center (centroid) of a resource."""
    compressFormat: NamedNode
    """The compression format of the distribution in which the data is contained in a compressed form, e.g. to reduce the size of the downloadable file."""
    contactPoint: NamedNode
    """Relevant contact information for the catalogued resource. Use of vCard is recommended."""
    dataset: NamedNode
    """A collection of data that is listed in the catalog."""
    distribution: NamedNode
    """An available distribution of the dataset."""
    downloadURL: NamedNode
    """The URL of the downloadable file in a given format. E.g. CSV file or RDF file. The format is indicated by the distribution's dct:format and/or dcat:mediaType."""
    endDate: NamedNode
    """The end of the period."""
    endpointDescription: NamedNode
    """A description of the service end-point, including its operations, parameters etc."""
    endpointURL: NamedNode
    """The root location or primary endpoint of the service (a web-resolvable IRI)."""
    hadRole: NamedNode
    """The function of an entity or agent with respect to another entity or resource."""
    keyword: NamedNode
    """A keyword or tag describing a resource."""
    landingPage: NamedNode
    """A Web page that can be navigated to in a Web browser to gain access to the catalog, a dataset, its distributions and/or additional information."""
    mediaType: NamedNode
    """The media type of the distribution as defined by IANA."""
    packageFormat: NamedNode
    """The package format of the distribution in which one or more data files are grouped together, e.g. to enable a set of related files to be downloaded together."""
    qualifiedRelation: NamedNode
    """Link to a description of a relationship with another resource."""
    record: NamedNode
    """A record describing the registration of a single dataset or data service that is part of the catalog."""
    servesDataset: NamedNode
    """A collection of data that this DataService can distribute."""
    service: NamedNode
    """A site or endpoint that is listed in the catalog."""
    spatialResolutionInMeters: NamedNode
    """minimum spatial separation resolvable in a dataset, measured in meters."""
    startDate: NamedNode
    """The start of the period"""
    temporalResolution: NamedNode
    """minimum time period resolvable in a dataset."""
    theme: NamedNode
    """A main category of the resource. A resource can have multiple themes."""
    themeTaxonomy: NamedNode
    """The knowledge organization system (KOS) used to classify catalog's datasets."""
