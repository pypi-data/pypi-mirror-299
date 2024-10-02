from pyoxigraph import NamedNode

from pyrdf_prefix.namespace import PredefinedNamespace


class VOID(PredefinedNamespace):
    """Vocabulary of Interlinked Datasets"""

    # Conversion-Date: 2024-09-30T10:48+00:00
    # Source: http://vocab.deri.ie/void.ttl

    _nsBaseIri = "http://rdfs.org/ns/void#"
    _issueWarning = True
    _withContainerMembershipProperty = False
    _nonPyIdentifiers = ("class",)

    Dataset: NamedNode
    """A set of RDF triples that are published, maintained or aggregated by a single provider."""
    DatasetDescription: NamedNode
    """A web resource whose foaf:primaryTopic or foaf:topics include void:Datasets."""
    Linkset: NamedNode
    """A collection of RDF links between two void:Datasets."""
    TechnicalFeature: NamedNode
    """A technical feature of a void:Dataset, such as a supported RDF serialization format."""
    classPartition: NamedNode
    """A subset of a void:Dataset that contains only the entities of a certain rdfs:Class."""
    classes: NamedNode
    """The total number of distinct classes in a void:Dataset. In other words, the number of distinct resources occuring as objects of rdf:type triples in the dataset."""
    dataDump: NamedNode
    """An RDF dump, partial or complete, of a void:Dataset."""
    distinctObjects: NamedNode
    """The total number of distinct objects in a void:Dataset. In other words, the number of distinct resources that occur in the object position of triples in the dataset. Literals are included in this count."""
    distinctSubjects: NamedNode
    """The total number of distinct subjects in a void:Dataset. In other words, the number of distinct resources that occur in the subject position of triples in the dataset."""
    documents: NamedNode
    """The total number of documents, for datasets that are published as a set of individual documents, such as RDF/XML documents or RDFa-annotated web pages. Non-RDF documents, such as web pages in HTML or images, are usually not included in this count. This property is intended for datasets where the total number of triples or entities is hard to determine. void:triples or void:entities should be preferred where practical."""
    entities: NamedNode
    """The total number of entities that are described in a void:Dataset."""
    inDataset: NamedNode
    """Points to the void:Dataset that a document is a part of."""
    objectsTarget: NamedNode
    """The dataset describing the objects of the triples contained in the Linkset."""
    openSearchDescription: NamedNode
    """An OpenSearch description document for a free-text search service over a void:Dataset."""
    properties: NamedNode
    """The total number of distinct properties in a void:Dataset. In other words, the number of distinct resources that occur in the predicate position of triples in the dataset."""
    property: NamedNode
    """The rdf:Property that is the predicate of all triples in a property-based partition."""
    propertyPartition: NamedNode
    """A subset of a void:Dataset that contains only the triples of a certain rdf:Property."""
    rootResource: NamedNode
    """A top concept or entry point for a void:Dataset that is structured in a tree-like fashion. All resources in a dataset can be reached by following links from its root resources in a small number of steps."""
    subjectsTarget: NamedNode
    """The dataset describing the subjects of triples contained in the Linkset."""
    target: NamedNode
    """One of the two datasets linked by the Linkset."""
    triples: NamedNode
    """The total number of triples contained in a void:Dataset."""
    uriLookupEndpoint: NamedNode
    """Defines a simple URI look-up protocol for accessing a dataset."""
    uriRegexPattern: NamedNode
    """Defines a regular expression pattern matching URIs in the dataset."""
    uriSpace: NamedNode
    """A URI that is a common string prefix of all the entity URIs in a void:Dataset."""
    vocabulary: NamedNode
    """A vocabulary that is used in the dataset."""
