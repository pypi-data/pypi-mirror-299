from pyoxigraph import NamedNode

from pyrdf_prefix.namespace import PredefinedNamespace


class RR(PredefinedNamespace):
    """R2RML: RDB to RDF Mapping Language Schema"""

    # Conversion-Date: 2024-09-30T10:48+00:00
    # Source: https://www.w3.org/ns/r2rml.ttl

    _nsBaseIri = "http://www.w3.org/ns/r2rml#"
    _issueWarning = True
    _withContainerMembershipProperty = False
    _nonPyIdentifiers = ("class",)

    BlankNode: NamedNode
    """Denotes a blank node, used with termType"""
    GraphMap: NamedNode
    """Represents a graph map."""
    IRI: NamedNode
    """Denotes an IRI, used with termpType."""
    Join: NamedNode
    """Represents a join condition."""
    Literal: NamedNode
    """Denotes a Literal, used with termType."""
    LogicalTable: NamedNode
    """Represents a logical table."""
    ObjectMap: NamedNode
    """Represents an object map."""
    PredicateMap: NamedNode
    """Represents a predicate map."""
    PredicateObjectMap: NamedNode
    """Represents a predicate-object map."""
    RefObjectMap: NamedNode
    """Denotes a reference to an object map."""
    SQL2008: NamedNode
    """Core SQL 2008"""
    SubjectMap: NamedNode
    """Represents a subject map."""
    TermMap: NamedNode
    """A function that generates an RDF term from a logical table row."""
    TriplesMap: NamedNode
    """Represents a triples map."""
    child: NamedNode
    """Names a column in the child table of a join."""
    column: NamedNode
    """Name of a column in the logical table. When generating RDF triples from a logical table row, value from the specified column is used as the subject, predicate, or object (based upon the specific domain)."""
    datatype: NamedNode
    """Specifies the datatype of the object component for the generated triple from a logical table row."""
    defaultGraph: NamedNode
    """Denotes a default graph"""
    graph: NamedNode
    """An IRI reference for use as the graph name of all triples generated with the GraphMap."""
    graphMap: NamedNode
    """Specifies a GraphMap. When used with a SubjectMap element, all the RDF triples generated from a logical row will be stored in the specified named graph. Otherwise, the RDF triple generated using the (predicate, object) pair will be stored in the specified named graph."""
    inverseExpression: NamedNode
    """An expression that allows, at query processing time, use of index-based access to the the (underlying) relational tables, instead of simply retrieving the table rows first and then applying a filter. This property is useful for retrieval based on conditions involving subject, predicate, or object generated from logical table column(s) and involves some transformation."""
    joinCondition: NamedNode
    """Specifies the join condition for joining the child logical table with the parent logical table of the foreign key constraint."""
    language: NamedNode
    """Specified the language for the object component for the generated triple from a logical table row."""
    logicalTable: NamedNode
    """Definition of logical table to be mapped."""
    object: NamedNode
    """Specifies the object for the generated triple from the logical table row."""
    objectMap: NamedNode
    """An ObjectMap element to generate the object component of the (predicate, object) pair from a logical table row."""
    parent: NamedNode
    """Names a column in the parent table of a join."""
    parentTriplesMap: NamedNode
    """Specifies the TriplesMap element corresponding to the parent logical table of the foreign key constraint."""
    predicate: NamedNode
    """Specifies the predicate for the generated triple from the logical table row."""
    predicateMap: NamedNode
    """A PredicateMap element to generate the predicate component of the (predicate, object) pair from a logical table row."""
    predicateObjectMap: NamedNode
    """A PredicateObjectMap element to generate (predicate, object) pair from a logical table row."""
    sqlQuery: NamedNode
    """A valid SQL query."""
    sqlVersion: NamedNode
    """An identifier for a SQL version."""
    subject: NamedNode
    """An IRI reference for use as subject for all the RDF triples generated from a logical table row."""
    subjectMap: NamedNode
    """A SubjectMap element to generate a subject from a logical table row."""
    tableName: NamedNode
    """Schema-qualified name of a table or view."""
    template: NamedNode
    """A template (format string) to specify how to generate a value for a subject, predicate, or object, using one or more columns from a logical table row."""
    termType: NamedNode
    """A string indicating whether subject or object generated using the value from column name specified for rr:column should be an IRI reference, blank node, or a literal."""
