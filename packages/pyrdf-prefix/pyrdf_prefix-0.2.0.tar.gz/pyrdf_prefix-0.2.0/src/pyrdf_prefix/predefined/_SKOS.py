from pyoxigraph import NamedNode

from pyrdf_prefix.namespace import PredefinedNamespace


class SKOS(PredefinedNamespace):
    """SKOS Simple Knowledge Organization System"""

    # Conversion-Date: 2024-09-30T10:48+00:00
    # Source: http://www.w3.org/TR/skos-reference/skos.rdf

    _nsBaseIri = "http://www.w3.org/2004/02/skos/core#"
    _issueWarning = True
    _withContainerMembershipProperty = False
    _nonPyIdentifiers = ()

    Collection: NamedNode
    """A meaningful collection of concepts."""
    Concept: NamedNode
    """An idea or notion; a unit of thought."""
    ConceptScheme: NamedNode
    """A set of concepts, optionally including statements about semantic relationships between those concepts."""
    OrderedCollection: NamedNode
    """An ordered collection of concepts, where both the grouping and the ordering are meaningful."""
    altLabel: NamedNode
    """An alternative lexical label for a resource."""
    broadMatch: NamedNode
    """skos:broadMatch is used to state a hierarchical mapping link between two conceptual resources in different concept schemes."""
    broader: NamedNode
    """Relates a concept to a concept that is more general in meaning."""
    broaderTransitive: NamedNode
    """skos:broaderTransitive is a transitive superproperty of skos:broader."""
    changeNote: NamedNode
    """A note about a modification to a concept."""
    closeMatch: NamedNode
    """skos:closeMatch is used to link two concepts that are sufficiently similar that they can be used interchangeably in some information retrieval applications. In order to avoid the possibility of "compound errors" when combining mappings across more than two concept schemes, skos:closeMatch is not declared to be a transitive property."""
    definition: NamedNode
    """A statement or formal explanation of the meaning of a concept."""
    editorialNote: NamedNode
    """A note for an editor, translator or maintainer of the vocabulary."""
    exactMatch: NamedNode
    """skos:exactMatch is used to link two concepts, indicating a high degree of confidence that the concepts can be used interchangeably across a wide range of information retrieval applications. skos:exactMatch is a transitive property, and is a sub-property of skos:closeMatch."""
    example: NamedNode
    """An example of the use of a concept."""
    hasTopConcept: NamedNode
    """Relates, by convention, a concept scheme to a concept which is topmost in the broader/narrower concept hierarchies for that scheme, providing an entry point to these hierarchies."""
    hiddenLabel: NamedNode
    """A lexical label for a resource that should be hidden when generating visual displays of the resource, but should still be accessible to free text search operations."""
    historyNote: NamedNode
    """A note about the past state/use/meaning of a concept."""
    inScheme: NamedNode
    """Relates a resource (for example a concept) to a concept scheme in which it is included."""
    mappingRelation: NamedNode
    """Relates two concepts coming, by convention, from different schemes, and that have comparable meanings"""
    member: NamedNode
    """Relates a collection to one of its members."""
    memberList: NamedNode
    """Relates an ordered collection to the RDF list containing its members."""
    narrowMatch: NamedNode
    """skos:narrowMatch is used to state a hierarchical mapping link between two conceptual resources in different concept schemes."""
    narrower: NamedNode
    """Relates a concept to a concept that is more specific in meaning."""
    narrowerTransitive: NamedNode
    """skos:narrowerTransitive is a transitive superproperty of skos:narrower."""
    notation: NamedNode
    """A notation, also known as classification code, is a string of characters such as "T58.5" or "303.4833" used to uniquely identify a concept within the scope of a given concept scheme."""
    note: NamedNode
    """A general note, for any purpose."""
    prefLabel: NamedNode
    """The preferred lexical label for a resource, in a given language."""
    related: NamedNode
    """Relates a concept to a concept with which there is an associative semantic relationship."""
    relatedMatch: NamedNode
    """skos:relatedMatch is used to state an associative mapping link between two conceptual resources in different concept schemes."""
    scopeNote: NamedNode
    """A note that helps to clarify the meaning and/or the use of a concept."""
    semanticRelation: NamedNode
    """Links a concept to a concept related by meaning."""
    topConceptOf: NamedNode
    """Relates a concept to the concept scheme that it is a top level concept of."""
