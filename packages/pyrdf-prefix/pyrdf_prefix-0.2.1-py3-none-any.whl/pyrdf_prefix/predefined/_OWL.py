from pyoxigraph import NamedNode

from pyrdf_prefix.namespace import PredefinedNamespace


class OWL(PredefinedNamespace):
    """The OWL 2 Schema vocabulary (OWL 2)"""

    # Conversion-Date: 2024-09-30T10:48+00:00
    # Source: http://www.w3.org/2002/07/owl#

    _nsBaseIri = "http://www.w3.org/2002/07/owl#"
    _issueWarning = True
    _withContainerMembershipProperty = False
    _nonPyIdentifiers = ()

    AllDifferent: NamedNode
    """The class of collections of pairwise different individuals."""
    AllDisjointClasses: NamedNode
    """The class of collections of pairwise disjoint classes."""
    AllDisjointProperties: NamedNode
    """The class of collections of pairwise disjoint properties."""
    Annotation: NamedNode
    """The class of annotated annotations for which the RDF serialization consists of an annotated subject, predicate and object."""
    AnnotationProperty: NamedNode
    """The class of annotation properties."""
    AsymmetricProperty: NamedNode
    """The class of asymmetric properties."""
    Axiom: NamedNode
    """The class of annotated axioms for which the RDF serialization consists of an annotated subject, predicate and object."""
    Class: NamedNode
    """The class of OWL classes."""
    DataRange: NamedNode
    """The class of OWL data ranges, which are special kinds of datatypes. Note: The use of the IRI owl:DataRange has been deprecated as of OWL 2. The IRI rdfs:Datatype SHOULD be used instead."""
    DatatypeProperty: NamedNode
    """The class of data properties."""
    DeprecatedClass: NamedNode
    """The class of deprecated classes."""
    DeprecatedProperty: NamedNode
    """The class of deprecated properties."""
    FunctionalProperty: NamedNode
    """The class of functional properties."""
    InverseFunctionalProperty: NamedNode
    """The class of inverse-functional properties."""
    IrreflexiveProperty: NamedNode
    """The class of irreflexive properties."""
    NamedIndividual: NamedNode
    """The class of named individuals."""
    NegativePropertyAssertion: NamedNode
    """The class of negative property assertions."""
    Nothing: NamedNode
    """This is the empty class."""
    ObjectProperty: NamedNode
    """The class of object properties."""
    Ontology: NamedNode
    """The class of ontologies."""
    OntologyProperty: NamedNode
    """The class of ontology properties."""
    ReflexiveProperty: NamedNode
    """The class of reflexive properties."""
    Restriction: NamedNode
    """The class of property restrictions."""
    SymmetricProperty: NamedNode
    """The class of symmetric properties."""
    Thing: NamedNode
    """The class of OWL individuals."""
    TransitiveProperty: NamedNode
    """The class of transitive properties."""
    allValuesFrom: NamedNode
    """The property that determines the class that a universal property restriction refers to."""
    annotatedProperty: NamedNode
    """The property that determines the predicate of an annotated axiom or annotated annotation."""
    annotatedSource: NamedNode
    """The property that determines the subject of an annotated axiom or annotated annotation."""
    annotatedTarget: NamedNode
    """The property that determines the object of an annotated axiom or annotated annotation."""
    assertionProperty: NamedNode
    """The property that determines the predicate of a negative property assertion."""
    backwardCompatibleWith: NamedNode
    """The annotation property that indicates that a given ontology is backward compatible with another ontology."""
    bottomDataProperty: NamedNode
    """The data property that does not relate any individual to any data value."""
    bottomObjectProperty: NamedNode
    """The object property that does not relate any two individuals."""
    cardinality: NamedNode
    """The property that determines the cardinality of an exact cardinality restriction."""
    complementOf: NamedNode
    """The property that determines that a given class is the complement of another class."""
    datatypeComplementOf: NamedNode
    """The property that determines that a given data range is the complement of another data range with respect to the data domain."""
    deprecated: NamedNode
    """The annotation property that indicates that a given entity has been deprecated."""
    differentFrom: NamedNode
    """The property that determines that two given individuals are different."""
    disjointUnionOf: NamedNode
    """The property that determines that a given class is equivalent to the disjoint union of a collection of other classes."""
    disjointWith: NamedNode
    """The property that determines that two given classes are disjoint."""
    distinctMembers: NamedNode
    """The property that determines the collection of pairwise different individuals in a owl:AllDifferent axiom."""
    equivalentClass: NamedNode
    """The property that determines that two given classes are equivalent, and that is used to specify datatype definitions."""
    equivalentProperty: NamedNode
    """The property that determines that two given properties are equivalent."""
    hasKey: NamedNode
    """The property that determines the collection of properties that jointly build a key."""
    hasSelf: NamedNode
    """The property that determines the property that a self restriction refers to."""
    hasValue: NamedNode
    """The property that determines the individual that a has-value restriction refers to."""
    imports: NamedNode
    """The property that is used for importing other ontologies into a given ontology."""
    incompatibleWith: NamedNode
    """The annotation property that indicates that a given ontology is incompatible with another ontology."""
    intersectionOf: NamedNode
    """The property that determines the collection of classes or data ranges that build an intersection."""
    inverseOf: NamedNode
    """The property that determines that two given properties are inverse."""
    maxCardinality: NamedNode
    """The property that determines the cardinality of a maximum cardinality restriction."""
    maxQualifiedCardinality: NamedNode
    """The property that determines the cardinality of a maximum qualified cardinality restriction."""
    members: NamedNode
    """The property that determines the collection of members in either a owl:AllDifferent, owl:AllDisjointClasses or owl:AllDisjointProperties axiom."""
    minCardinality: NamedNode
    """The property that determines the cardinality of a minimum cardinality restriction."""
    minQualifiedCardinality: NamedNode
    """The property that determines the cardinality of a minimum qualified cardinality restriction."""
    onClass: NamedNode
    """The property that determines the class that a qualified object cardinality restriction refers to."""
    onDataRange: NamedNode
    """The property that determines the data range that a qualified data cardinality restriction refers to."""
    onDatatype: NamedNode
    """The property that determines the datatype that a datatype restriction refers to."""
    onProperties: NamedNode
    """The property that determines the n-tuple of properties that a property restriction on an n-ary data range refers to."""
    onProperty: NamedNode
    """The property that determines the property that a property restriction refers to."""
    oneOf: NamedNode
    """The property that determines the collection of individuals or data values that build an enumeration."""
    priorVersion: NamedNode
    """The annotation property that indicates the predecessor ontology of a given ontology."""
    propertyChainAxiom: NamedNode
    """The property that determines the n-tuple of properties that build a sub property chain of a given property."""
    propertyDisjointWith: NamedNode
    """The property that determines that two given properties are disjoint."""
    qualifiedCardinality: NamedNode
    """The property that determines the cardinality of an exact qualified cardinality restriction."""
    sameAs: NamedNode
    """The property that determines that two given individuals are equal."""
    someValuesFrom: NamedNode
    """The property that determines the class that an existential property restriction refers to."""
    sourceIndividual: NamedNode
    """The property that determines the subject of a negative property assertion."""
    targetIndividual: NamedNode
    """The property that determines the object of a negative object property assertion."""
    targetValue: NamedNode
    """The property that determines the value of a negative data property assertion."""
    topDataProperty: NamedNode
    """The data property that relates every individual to every data value."""
    topObjectProperty: NamedNode
    """The object property that relates every two individuals."""
    unionOf: NamedNode
    """The property that determines the collection of classes or data ranges that build a union."""
    versionIRI: NamedNode
    """The property that identifies the version IRI of an ontology."""
    versionInfo: NamedNode
    """The annotation property that provides version information for an ontology or another OWL construct."""
    withRestrictions: NamedNode
    """The property that determines the collection of facet-value pairs that define a datatype restriction."""
