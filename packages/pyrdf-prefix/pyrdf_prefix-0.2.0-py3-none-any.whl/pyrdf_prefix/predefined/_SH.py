from pyoxigraph import NamedNode

from pyrdf_prefix.namespace import PredefinedNamespace


class SH(PredefinedNamespace):
    """Shapes Constraint Language (SHACL)"""

    # Conversion-Date: 2024-09-30T10:48+00:00
    # Source: https://www.w3.org/ns/shacl.ttl

    _nsBaseIri = "http://www.w3.org/ns/shacl#"
    _issueWarning = True
    _withContainerMembershipProperty = False
    _nonPyIdentifiers = ("and", "class", "in", "not", "or")

    AbstractResult: NamedNode
    """The base class of validation results, typically not instantiated directly."""
    AndConstraintComponent: NamedNode
    """A constraint component that can be used to test whether a value node conforms to all members of a provided list of shapes."""
    BlankNode: NamedNode
    """The node kind of all blank nodes."""
    BlankNodeOrIRI: NamedNode
    """The node kind of all blank nodes or IRIs."""
    BlankNodeOrLiteral: NamedNode
    """The node kind of all blank nodes or literals."""
    ClassConstraintComponent: NamedNode
    """A constraint component that can be used to verify that each value node is an instance of a given type."""
    ClosedConstraintComponent: NamedNode
    """A constraint component that can be used to indicate that focus nodes must only have values for those properties that have been explicitly enumerated via sh:property/sh:path."""
    ConstraintComponent: NamedNode
    """The class of constraint components."""
    DatatypeConstraintComponent: NamedNode
    """A constraint component that can be used to restrict the datatype of all value nodes."""
    DisjointConstraintComponent: NamedNode
    """A constraint component that can be used to verify that the set of value nodes is disjoint with the the set of nodes that have the focus node as subject and the value of a given property as predicate."""
    EqualsConstraintComponent: NamedNode
    """A constraint component that can be used to verify that the set of value nodes is equal to the set of nodes that have the focus node as subject and the value of a given property as predicate."""
    ExpressionConstraintComponent: NamedNode
    """A constraint component that can be used to verify that a given node expression produces true for all value nodes."""
    Function: NamedNode
    """The class of SHACL functions."""
    HasValueConstraintComponent: NamedNode
    """A constraint component that can be used to verify that one of the value nodes is a given RDF node."""
    IRI: NamedNode
    """The node kind of all IRIs."""
    IRIOrLiteral: NamedNode
    """The node kind of all IRIs or literals."""
    InConstraintComponent: NamedNode
    """A constraint component that can be used to exclusively enumerate the permitted value nodes."""
    Info: NamedNode
    """The severity for an informational validation result."""
    JSConstraint: NamedNode
    """The class of constraints backed by a JavaScript function."""
    JSConstraintComponent: NamedNode
    """A constraint component with the parameter sh:js linking to a sh:JSConstraint containing a sh:script."""
    JSExecutable: NamedNode
    """Abstract base class of resources that declare an executable JavaScript."""
    JSFunction: NamedNode
    """The class of SHACL functions that execute a JavaScript function when called."""
    JSLibrary: NamedNode
    """Represents a JavaScript library, typically identified by one or more URLs of files to include."""
    JSRule: NamedNode
    """The class of SHACL rules expressed using JavaScript."""
    JSTarget: NamedNode
    """The class of targets that are based on JavaScript functions."""
    JSTargetType: NamedNode
    """The (meta) class for parameterizable targets that are based on JavaScript functions."""
    JSValidator: NamedNode
    """A SHACL validator based on JavaScript. This can be used to declare SHACL constraint components that perform JavaScript-based validation when used."""
    LanguageInConstraintComponent: NamedNode
    """A constraint component that can be used to enumerate language tags that all value nodes must have."""
    LessThanConstraintComponent: NamedNode
    """A constraint component that can be used to verify that each value node is smaller than all the nodes that have the focus node as subject and the value of a given property as predicate."""
    LessThanOrEqualsConstraintComponent: NamedNode
    """A constraint component that can be used to verify that every value node is smaller than all the nodes that have the focus node as subject and the value of a given property as predicate."""
    Literal: NamedNode
    """The node kind of all literals."""
    MaxCountConstraintComponent: NamedNode
    """A constraint component that can be used to restrict the maximum number of value nodes."""
    MaxExclusiveConstraintComponent: NamedNode
    """A constraint component that can be used to restrict the range of value nodes with a maximum exclusive value."""
    MaxInclusiveConstraintComponent: NamedNode
    """A constraint component that can be used to restrict the range of value nodes with a maximum inclusive value."""
    MaxLengthConstraintComponent: NamedNode
    """A constraint component that can be used to restrict the maximum string length of value nodes."""
    MinCountConstraintComponent: NamedNode
    """A constraint component that can be used to restrict the minimum number of value nodes."""
    MinExclusiveConstraintComponent: NamedNode
    """A constraint component that can be used to restrict the range of value nodes with a minimum exclusive value."""
    MinInclusiveConstraintComponent: NamedNode
    """A constraint component that can be used to restrict the range of value nodes with a minimum inclusive value."""
    MinLengthConstraintComponent: NamedNode
    """A constraint component that can be used to restrict the minimum string length of value nodes."""
    NodeConstraintComponent: NamedNode
    """A constraint component that can be used to verify that all value nodes conform to the given node shape."""
    NodeKind: NamedNode
    """The class of all node kinds, including sh:BlankNode, sh:IRI, sh:Literal or the combinations of these: sh:BlankNodeOrIRI, sh:BlankNodeOrLiteral, sh:IRIOrLiteral."""
    NodeKindConstraintComponent: NamedNode
    """A constraint component that can be used to restrict the RDF node kind of each value node."""
    NodeShape: NamedNode
    """A node shape is a shape that specifies constraint that need to be met with respect to focus nodes."""
    NotConstraintComponent: NamedNode
    """A constraint component that can be used to verify that value nodes do not conform to a given shape."""
    OrConstraintComponent: NamedNode
    """A constraint component that can be used to restrict the value nodes so that they conform to at least one out of several provided shapes."""
    Parameter: NamedNode
    """The class of parameter declarations, consisting of a path predicate and (possibly) information about allowed value type, cardinality and other characteristics."""
    Parameterizable: NamedNode
    """Superclass of components that can take parameters, especially functions and constraint components."""
    PatternConstraintComponent: NamedNode
    """A constraint component that can be used to verify that every value node matches a given regular expression."""
    PrefixDeclaration: NamedNode
    """The class of prefix declarations, consisting of pairs of a prefix with a namespace."""
    PropertyConstraintComponent: NamedNode
    """A constraint component that can be used to verify that all value nodes conform to the given property shape."""
    PropertyGroup: NamedNode
    """Instances of this class represent groups of property shapes that belong together."""
    PropertyShape: NamedNode
    """A property shape is a shape that specifies constraints on the values of a focus node for a given property or path."""
    QualifiedMaxCountConstraintComponent: NamedNode
    """A constraint component that can be used to verify that a specified maximum number of value nodes conforms to a given shape."""
    QualifiedMinCountConstraintComponent: NamedNode
    """A constraint component that can be used to verify that a specified minimum number of value nodes conforms to a given shape."""
    ResultAnnotation: NamedNode
    """A class of result annotations, which define the rules to derive the values of a given annotation property as extra values for a validation result."""
    Rule: NamedNode
    """The class of SHACL rules. Never instantiated directly."""
    SPARQLAskExecutable: NamedNode
    """The class of SPARQL executables that are based on an ASK query."""
    SPARQLAskValidator: NamedNode
    """The class of validators based on SPARQL ASK queries. The queries are evaluated for each value node and are supposed to return true if the given node conforms."""
    SPARQLConstraint: NamedNode
    """The class of constraints based on SPARQL SELECT queries."""
    SPARQLConstraintComponent: NamedNode
    """A constraint component that can be used to define constraints based on SPARQL queries."""
    SPARQLConstructExecutable: NamedNode
    """The class of SPARQL executables that are based on a CONSTRUCT query."""
    SPARQLExecutable: NamedNode
    """The class of resources that encapsulate a SPARQL query."""
    SPARQLFunction: NamedNode
    """A function backed by a SPARQL query - either ASK or SELECT."""
    SPARQLRule: NamedNode
    """The class of SHACL rules based on SPARQL CONSTRUCT queries."""
    SPARQLSelectExecutable: NamedNode
    """The class of SPARQL executables based on a SELECT query."""
    SPARQLSelectValidator: NamedNode
    """The class of validators based on SPARQL SELECT queries. The queries are evaluated for each focus node and are supposed to produce bindings for all focus nodes that do not conform."""
    SPARQLTarget: NamedNode
    """The class of targets that are based on SPARQL queries."""
    SPARQLTargetType: NamedNode
    """The (meta) class for parameterizable targets that are based on SPARQL queries."""
    SPARQLUpdateExecutable: NamedNode
    """The class of SPARQL executables based on a SPARQL UPDATE."""
    Severity: NamedNode
    """The class of validation result severity levels, including violation and warning levels."""
    Shape: NamedNode
    """A shape is a collection of constraints that may be targeted for certain nodes."""
    Target: NamedNode
    """The base class of targets such as those based on SPARQL queries."""
    TargetType: NamedNode
    """The (meta) class for parameterizable targets.	Instances of this are instantiated as values of the sh:target property."""
    UniqueLangConstraintComponent: NamedNode
    """A constraint component that can be used to specify that no pair of value nodes may use the same language tag."""
    ValidationReport: NamedNode
    """The class of SHACL validation reports."""
    ValidationResult: NamedNode
    """The class of validation results."""
    Validator: NamedNode
    """The class of validators, which provide instructions on how to process a constraint definition. This class serves as base class for the SPARQL-based validators and other possible implementations."""
    Violation: NamedNode
    """The severity for a violation validation result."""
    Warning: NamedNode
    """The severity for a warning validation result."""
    XoneConstraintComponent: NamedNode
    """A constraint component that can be used to restrict the value nodes so that they conform to exactly one out of several provided shapes."""
    alternativePath: NamedNode
    """The (single) value of this property must be a list of path elements, representing the elements of alternative paths."""
    annotationProperty: NamedNode
    """The annotation property that shall be set."""
    annotationValue: NamedNode
    """The (default) values of the annotation property."""
    annotationVarName: NamedNode
    """The name of the SPARQL variable from the SELECT clause that shall be used for the values."""
    ask: NamedNode
    """The SPARQL ASK query to execute."""
    closed: NamedNode
    """If set to true then the shape is closed."""
    condition: NamedNode
    """The shapes that the focus nodes need to conform to before a rule is executed on them."""
    conforms: NamedNode
    """True if the validation did not produce any validation results, and false otherwise."""
    construct: NamedNode
    """The SPARQL CONSTRUCT query to execute."""
    datatype: NamedNode
    """Specifies an RDF datatype that all value nodes must have."""
    deactivated: NamedNode
    """If set to true then all nodes conform to this."""
    declare: NamedNode
    """Links a resource with its namespace prefix declarations."""
    defaultValue: NamedNode
    """A default value for a property, for example for user interface tools to pre-populate input fields."""
    description: NamedNode
    """Human-readable descriptions for the property in the context of the surrounding shape."""
    detail: NamedNode
    """Links a result with other results that provide more details, for example to describe violations against nested shapes."""
    disjoint: NamedNode
    """Specifies a property where the set of values must be disjoint with the value nodes."""
    entailment: NamedNode
    """An entailment regime that indicates what kind of inferencing is required by a shapes graph."""
    equals: NamedNode
    """Specifies a property that must have the same values as the value nodes."""
    expression: NamedNode
    """The node expression that must return true for the value nodes."""
    filterShape: NamedNode
    """The shape that all input nodes of the expression need to conform to."""
    flags: NamedNode
    """An optional flag to be used with regular expression pattern matching."""
    focusNode: NamedNode
    """The focus node that was validated when the result was produced."""
    group: NamedNode
    """Can be used to link to a property group to indicate that a property shape belongs to a group of related property shapes."""
    hasValue: NamedNode
    """Specifies a value that must be among the value nodes."""
    ignoredProperties: NamedNode
    """An optional RDF list of properties that are also permitted in addition to those explicitly enumerated via sh:property/sh:path."""
    intersection: NamedNode
    """A list of node expressions that shall be intersected."""
    inversePath: NamedNode
    """The (single) value of this property represents an inverse path (object to subject)."""
    js: NamedNode
    """Constraints expressed in JavaScript."""
    jsFunctionName: NamedNode
    """The name of the JavaScript function to execute."""
    jsLibrary: NamedNode
    """Declares which JavaScript libraries are needed to execute this."""
    jsLibraryURL: NamedNode
    """Declares the URLs of a JavaScript library. This should be the absolute URL of a JavaScript file. Implementations may redirect those to local files."""
    labelTemplate: NamedNode
    """Outlines how human-readable labels of instances of the associated Parameterizable shall be produced. The values can contain {?paramName} as placeholders for the actual values of the given parameter."""
    languageIn: NamedNode
    """Specifies a list of language tags that all value nodes must have."""
    lessThan: NamedNode
    """Specifies a property that must have smaller values than the value nodes."""
    lessThanOrEquals: NamedNode
    """Specifies a property that must have smaller or equal values than the value nodes."""
    maxCount: NamedNode
    """Specifies the maximum number of values in the set of value nodes."""
    maxExclusive: NamedNode
    """Specifies the maximum exclusive value of each value node."""
    maxInclusive: NamedNode
    """Specifies the maximum inclusive value of each value node."""
    maxLength: NamedNode
    """Specifies the maximum string length of each value node."""
    message: NamedNode
    """A human-readable message (possibly with placeholders for variables) explaining the cause of the result."""
    minCount: NamedNode
    """Specifies the minimum number of values in the set of value nodes."""
    minExclusive: NamedNode
    """Specifies the minimum exclusive value of each value node."""
    minInclusive: NamedNode
    """Specifies the minimum inclusive value of each value node."""
    minLength: NamedNode
    """Specifies the minimum string length of each value node."""
    name: NamedNode
    """Human-readable labels for the property in the context of the surrounding shape."""
    namespace: NamedNode
    """The namespace associated with a prefix in a prefix declaration."""
    node: NamedNode
    """Specifies the node shape that all value nodes must conform to."""
    nodeKind: NamedNode
    """Specifies the node kind (e.g. IRI or literal) each value node."""
    nodeValidator: NamedNode
    """The validator(s) used to evaluate a constraint in the context of a node shape."""
    nodes: NamedNode
    """The node expression producing the input nodes of a filter shape expression."""
    object: NamedNode
    """An expression producing the nodes that shall be inferred as objects."""
    oneOrMorePath: NamedNode
    """The (single) value of this property represents a path that is matched one or more times."""
    optional: NamedNode
    """Indicates whether a parameter is optional."""
    order: NamedNode
    """Specifies the relative order of this compared to its siblings. For example use 0 for the first, 1 for the second."""
    parameter: NamedNode
    """The parameters of a function or constraint component."""
    path: NamedNode
    """Specifies the property path of a property shape."""
    pattern: NamedNode
    """Specifies a regular expression pattern that the string representations of the value nodes must match."""
    predicate: NamedNode
    """An expression producing the properties that shall be inferred as predicates."""
    prefix: NamedNode
    """The prefix of a prefix declaration."""
    prefixes: NamedNode
    """The prefixes that shall be applied before parsing the associated SPARQL query."""
    property: NamedNode
    """Links a shape to its property shapes."""
    propertyValidator: NamedNode
    """The validator(s) used to evaluate a constraint in the context of a property shape."""
    qualifiedMaxCount: NamedNode
    """The maximum number of value nodes that can conform to the shape."""
    qualifiedMinCount: NamedNode
    """The minimum number of value nodes that must conform to the shape."""
    qualifiedValueShape: NamedNode
    """The shape that a specified number of values must conform to."""
    qualifiedValueShapesDisjoint: NamedNode
    """Can be used to mark the qualified value shape to be disjoint with its sibling shapes."""
    result: NamedNode
    """The validation results contained in a validation report."""
    resultAnnotation: NamedNode
    """Links a SPARQL validator with zero or more sh:ResultAnnotation instances, defining how to derive additional result properties based on the variables of the SELECT query."""
    resultMessage: NamedNode
    """Human-readable messages explaining the cause of the result."""
    resultPath: NamedNode
    """The path of a validation result, based on the path of the validated property shape."""
    resultSeverity: NamedNode
    """The severity of the result, e.g. warning."""
    returnType: NamedNode
    """The expected type of values returned by the associated function."""
    rule: NamedNode
    """The rules linked to a shape."""
    select: NamedNode
    """The SPARQL SELECT query to execute."""
    severity: NamedNode
    """Defines the severity that validation results produced by a shape must have. Defaults to sh:Violation."""
    shapesGraph: NamedNode
    """Shapes graphs that should be used when validating this data graph."""
    shapesGraphWellFormed: NamedNode
    """If true then the validation engine was certain that the shapes graph has passed all SHACL syntax requirements during the validation process."""
    sourceConstraint: NamedNode
    """The constraint that was validated when the result was produced."""
    sourceConstraintComponent: NamedNode
    """The constraint component that is the source of the result."""
    sourceShape: NamedNode
    """The shape that is was validated when the result was produced."""
    sparql: NamedNode
    """Links a shape with SPARQL constraints."""
    subject: NamedNode
    """An expression producing the resources that shall be inferred as subjects."""
    suggestedShapesGraph: NamedNode
    """Suggested shapes graphs for this ontology. The values of this property may be used in the absence of specific sh:shapesGraph statements."""
    target: NamedNode
    """Links a shape to a target specified by an extension language, for example instances of sh:SPARQLTarget."""
    targetClass: NamedNode
    """Links a shape to a class, indicating that all instances of the class must conform to the shape."""
    targetNode: NamedNode
    """Links a shape to individual nodes, indicating that these nodes must conform to the shape."""
    targetObjectsOf: NamedNode
    """Links a shape to a property, indicating that all all objects of triples that have the given property as their predicate must conform to the shape."""
    targetSubjectsOf: NamedNode
    """Links a shape to a property, indicating that all subjects of triples that have the given property as their predicate must conform to the shape."""
    this: NamedNode
    """A node expression that represents the current focus node."""
    union: NamedNode
    """A list of node expressions that shall be used together."""
    uniqueLang: NamedNode
    """Specifies whether all node values must have a unique (or no) language tag."""
    update: NamedNode
    """The SPARQL UPDATE to execute."""
    validator: NamedNode
    """The validator(s) used to evaluate constraints of either node or property shapes."""
    value: NamedNode
    """An RDF node that has caused the result."""
    xone: NamedNode
    """Specifies a list of shapes so that the value nodes must conform to exactly one of the shapes."""
    zeroOrMorePath: NamedNode
    """The (single) value of this property represents a path that is matched zero or more times."""
    zeroOrOnePath: NamedNode
    """The (single) value of this property represents a path that is matched zero or one times."""
