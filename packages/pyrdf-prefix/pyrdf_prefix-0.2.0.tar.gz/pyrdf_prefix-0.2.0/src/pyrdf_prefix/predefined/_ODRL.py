from pyoxigraph import NamedNode

from pyrdf_prefix.namespace import PredefinedNamespace


class ODRL(PredefinedNamespace):
    """Open Digital Rights Language 2.0"""

    # Conversion-Date: 2024-09-30T10:48+00:00
    # Source: https://www.w3.org/ns/odrl/2/ODRL22.ttl

    _nsBaseIri = "http://www.w3.org/ns/odrl/2/"
    _issueWarning = True
    _withContainerMembershipProperty = False
    _nonPyIdentifiers = ("and", "or")

    Action: NamedNode
    """An operation on an Asset."""
    Agreement: NamedNode
    """A Policy that grants the assignee a Rule over an Asset from an assigner."""
    All: NamedNode
    """Specifies that the scope of the relationship is all of the collective individuals within a context."""
    All2ndConnections: NamedNode
    """Specifies that the scope of the relationship is all of the second-level connections to the Party."""
    AllConnections: NamedNode
    """Specifies that the scope of the relationship is all of the first-level connections of the Party."""
    AllGroups: NamedNode
    """Specifies that the scope of the relationship is all of the group connections of the Party."""
    Assertion: NamedNode
    """A Policy that asserts a Rule over an Asset from parties."""
    Asset: NamedNode
    """A resource or a collection of resources that are the subject of a Rule."""
    AssetCollection: NamedNode
    """An Asset that is collection of individual resources"""
    AssetScope: NamedNode
    """Scopes for Asset Scope expressions."""
    ConflictTerm: NamedNode
    """Used to establish strategies to resolve conflicts that arise from the merging of Policies or conflicts between Permissions and Prohibitions in the same Policy."""
    Constraint: NamedNode
    """A boolean expression that refines the semantics of an Action and Party/Asset Collection or declare the conditions applicable to a Rule."""
    Duty: NamedNode
    """The obligation to perform an Action"""
    Group: NamedNode
    """Specifies that the scope of the relationship is the defined group with multiple individual members."""
    Individual: NamedNode
    """Specifies that the scope of the relationship is the single Party individual."""
    LeftOperand: NamedNode
    """Left operand for a constraint expression."""
    LogicalConstraint: NamedNode
    """A logical expression that refines the semantics of an Action and Party/Asset Collection or declare the conditions applicable to a Rule."""
    Offer: NamedNode
    """A Policy that proposes a Rule over an Asset from an assigner."""
    Operator: NamedNode
    """Operator for constraint expression."""
    Party: NamedNode
    """An entity or a collection of entities that undertake Roles in a Rule."""
    PartyCollection: NamedNode
    """A Party that is a group of individual entities"""
    PartyScope: NamedNode
    """Scopes for Party Scope expressions."""
    Permission: NamedNode
    """The ability to perform an Action over an Asset."""
    Policy: NamedNode
    """A non-empty group of Permissions and/or Prohibitions."""
    Privacy: NamedNode
    """A Policy that expresses a Rule over an Asset containing personal information."""
    Prohibition: NamedNode
    """The inability to perform an Action over an Asset."""
    Request: NamedNode
    """A Policy that proposes a Rule over an Asset from an assignee."""
    RightOperand: NamedNode
    """Right operand for constraint expression."""
    Rule: NamedNode
    """An abstract concept that represents the common characteristics of Permissions, Prohibitions, and Duties."""
    Set: NamedNode
    """A Policy that expresses a Rule over an Asset."""
    Ticket: NamedNode
    """A Policy that grants the holder a Rule over an Asset from an assigner."""
    UndefinedTerm: NamedNode
    """Is used to indicate how to support Actions that are not part of any vocabulary or profile in the policy expression system."""
    absolutePosition: NamedNode
    """A point in space or time defined with absolute coordinates for the positioning of the target Asset."""
    absoluteSize: NamedNode
    """Measure(s) of one or two axes for 2D-objects or measure(s) of one to tree axes for 3D-objects of the target Asset."""
    absoluteSpatialPosition: NamedNode
    """The absolute spatial positions of four corners of a rectangle on a 2D-canvas or the eight corners of a cuboid in a 3D-space for the target Asset to fit."""
    absoluteTemporalPosition: NamedNode
    """The absolute temporal positions in a media stream the target Asset has to fit."""
    acceptTracking: NamedNode
    """To accept that the use of the Asset may be tracked."""
    action: NamedNode
    """The operation relating to the Asset for which the Rule is being subjected."""
    adHocShare: NamedNode
    """The act of sharing the asset to parties in close proximity to the owner."""
    aggregate: NamedNode
    """To use the Asset or parts of it as part of a composite collection."""
    andSequence: NamedNode
    """The relation is satisfied when each of the Constraints are satisfied in the order specified."""
    annotate: NamedNode
    """To add explanatory notations/commentaries to the Asset without modifying the Asset in any other way."""
    anonymize: NamedNode
    """To anonymize all or parts of the Asset."""
    append: NamedNode
    """The act of adding to the end of an asset."""
    appendTo: NamedNode
    """The act of appending data to the Asset without modifying the Asset in any other way."""
    archive: NamedNode
    """To store the Asset (in a non-transient form)."""
    assignee: NamedNode
    """The Party is the recipient of the Rule."""
    assigneeOf: NamedNode
    """Identifies an ODRL Policy for which the identified Party undertakes the assignee functional role."""
    assigner: NamedNode
    """The Party is the issuer of the Rule."""
    assignerOf: NamedNode
    """Identifies an ODRL Policy for which the identified Party undertakes the assigner functional role."""
    attachPolicy: NamedNode
    """The act of keeping the policy notice with the asset."""
    attachSource: NamedNode
    """The act of attaching the source of the asset and its derivatives."""
    attribute: NamedNode
    """To attribute the use of the Asset."""
    attributedParty: NamedNode
    """The Party to be attributed."""
    attributingParty: NamedNode
    """The Party who undertakes the attribution."""
    commercialize: NamedNode
    """The act of using the asset in a business environment."""
    compensate: NamedNode
    """To compensate by transfer of some amount of value, if defined, for using or selling the Asset."""
    compensatedParty: NamedNode
    """The Party is the recipient of the compensation."""
    compensatingParty: NamedNode
    """The Party that is the provider of the compensation."""
    concurrentUse: NamedNode
    """To create multiple copies of the Asset that are being concurrently used."""
    conflict: NamedNode
    """The conflict-resolution strategy for a Policy."""
    consentedParty: NamedNode
    """The Party who obtains the consent."""
    consentingParty: NamedNode
    """The Party to obtain consent from."""
    consequence: NamedNode
    """Relates a Duty to another Duty, the latter being a consequence of not fulfilling the former."""
    constraint: NamedNode
    """Constraint applied to a Rule"""
    contractedParty: NamedNode
    """The Party who is being contracted."""
    contractingParty: NamedNode
    """The Party who is offering the contract."""
    copy: NamedNode
    """The act of making an exact reproduction of the asset."""
    core: NamedNode
    """Identifier for the ODRL Core Profile"""
    count: NamedNode
    """Numeric count of executions of the action of the Rule."""
    dataType: NamedNode
    """The datatype of the value of the rightOperand or rightOperandReference of a Constraint."""
    dateTime: NamedNode
    """The date (and optional time and timezone) of exercising the action of the Rule. Right operand value MUST be an xsd:date or xsd:dateTime as defined by [[xmlschema11-2]]."""
    delayPeriod: NamedNode
    """A time delay period prior to exercising the action of the Rule. The point in time triggering this period MAY be defined by another temporal Constraint combined by a Logical Constraint (utilising the odrl:andSequence operand). Right operand value MUST be an xsd:duration as defined by [[xmlschema11-2]]."""
    delete: NamedNode
    """To permanently remove all copies of the Asset after it has been used."""
    deliveryChannel: NamedNode
    """The delivery channel used for exercising the action of the Rule."""
    derive: NamedNode
    """To create a new derivative Asset from this Asset and to edit or modify the derivative."""
    device: NamedNode
    """An identified device used for exercising the action of the Rule."""
    digitize: NamedNode
    """To produce a digital copy of (or otherwise digitize) the Asset from its analogue form."""
    display: NamedNode
    """To create a static and transient rendition of an Asset."""
    distribute: NamedNode
    """To supply the Asset to third-parties."""
    duty: NamedNode
    """Relates an individual Duty to a Permission."""
    elapsedTime: NamedNode
    """A continuous elapsed time period which may be used for exercising of the action of the Rule. Right operand value MUST be an xsd:duration as defined by [[xmlschema11-2]]."""
    ensureExclusivity: NamedNode
    """To ensure that the Rule on the Asset is exclusive."""
    eq: NamedNode
    """Indicating that a given value equals the right operand of the Constraint."""
    event: NamedNode
    """An identified event setting a context for exercising the action of the Rule."""
    execute: NamedNode
    """To run the computer program Asset."""
    export: NamedNode
    """The act of transforming the asset into a new form."""
    extract: NamedNode
    """To extract parts of the Asset and to use it as a new Asset."""
    extractChar: NamedNode
    """The act of extracting (replicating) unchanged characters from the asset."""
    extractPage: NamedNode
    """The act of extracting (replicating) unchanged pages from the asset."""
    extractWord: NamedNode
    """The act of extracting (replicating) unchanged words from the asset."""
    failure: NamedNode
    """Failure is an abstract property that defines the violation (or unmet) relationship between Rules."""
    fileFormat: NamedNode
    """A transformed file format of the target Asset."""
    function: NamedNode
    """Function is an abstract property whose sub-properties define the functional roles which may be fulfilled by a party in relation to a Rule."""
    give: NamedNode
    """To transfer the ownership of the Asset to a third party without compensation and while deleting the original asset."""
    grantUse: NamedNode
    """To grant the use of the Asset to third parties."""
    gt: NamedNode
    """Indicating that a given value is greater than the right operand of the Constraint."""
    gteq: NamedNode
    """Indicating that a given value is greater than or equal to the right operand of the Constraint."""
    hasPart: NamedNode
    """A set-based operator indicating that a given value contains the right operand of the Constraint."""
    hasPolicy: NamedNode
    """Identifies an ODRL Policy for which the identified Asset is the target Asset to all the Rules."""
    ignore: NamedNode
    """The Action is to be ignored and is not part of the policy – and the policy remains valid."""
    implies: NamedNode
    """An Action asserts that another Action is not prohibited to enable its operational semantics."""
    include: NamedNode
    """To include other related assets in the Asset."""
    includedIn: NamedNode
    """An Action transitively asserts that another Action that encompasses its operational semantics."""
    index: NamedNode
    """To record the Asset in an index."""
    industry: NamedNode
    """A defined industry sector setting a context for exercising the action of the Rule."""
    inform: NamedNode
    """To inform that an action has been performed on or in relation to the Asset."""
    informedParty: NamedNode
    """The Party to be informed of all uses."""
    informingParty: NamedNode
    """The Party who provides the inform use data."""
    inheritAllowed: NamedNode
    """Indicates if the Policy entity can be inherited."""
    inheritFrom: NamedNode
    """Relates a (child) policy to another (parent) policy from which terms are inherited."""
    inheritRelation: NamedNode
    """Indentifies the type of inheritance."""
    install: NamedNode
    """To load the computer program Asset onto a storage device which allows operating or running the Asset."""
    invalid: NamedNode
    """The policy is void."""
    isA: NamedNode
    """A set-based operator indicating that a given value is an instance of the right operand of the Constraint."""
    isAllOf: NamedNode
    """A set-based operator indicating that a given value is all of the right operand of the Constraint."""
    isAnyOf: NamedNode
    """A set-based operator indicating that a given value is any of the right operand of the Constraint."""
    isNoneOf: NamedNode
    """A set-based operator indicating that a given value is none of the right operand of the Constraint."""
    isPartOf: NamedNode
    """A set-based operator indicating that a given value is contained by the right operand of the Constraint."""
    language: NamedNode
    """A natural language used by the target Asset."""
    lease: NamedNode
    """The act of making available the asset to a third-party for a fixed period of time with exchange of value."""
    leftOperand: NamedNode
    """The left operand in a constraint expression."""
    lend: NamedNode
    """The act of making available the asset to a third-party for a fixed period of time without exchange of value."""
    license: NamedNode
    """The act of granting the right to use the asset to a third-party."""
    lt: NamedNode
    """Indicating that a given value is less than the right operand of the Constraint."""
    lteq: NamedNode
    """Indicating that a given value is less than or equal to the right operand of the Constraint."""
    media: NamedNode
    """Category of a media asset setting a context for exercising the action of the Rule."""
    meteredTime: NamedNode
    """An accumulated amount of one to many metered time periods which were used for exercising the action of the Rule. Right operand value MUST be an xsd:duration as defined by [[xmlschema11-2]]."""
    modify: NamedNode
    """To change existing content of the Asset. A new asset is not created by this action."""
    move: NamedNode
    """To move the Asset from one digital location to another including deleting the original copy."""
    neq: NamedNode
    """Indicating that a given value is not equal to the right operand of the Constraint."""
    nextPolicy: NamedNode
    """To grant the specified Policy to a third party for their use of the Asset."""
    obligation: NamedNode
    """Relates an individual Duty to a Policy."""
    obtainConsent: NamedNode
    """To obtain verifiable consent to perform the requested action in relation to the Asset."""
    operand: NamedNode
    """Operand is an abstract property for a logical relationship."""
    operator: NamedNode
    """The operator function applied to operands of a Constraint"""
    output: NamedNode
    """The output property specifies the Asset which is created from the output of the Action."""
    partOf: NamedNode
    """Identifies an Asset/PartyCollection that the Asset/Party is a member of."""
    pay: NamedNode
    """The act of paying a financial amount to a party for use of the asset."""
    payAmount: NamedNode
    """The amount of a financial payment. Right operand value MUST be an xsd:decimal. """
    payeeParty: NamedNode
    """The Party is the recipient of the payment."""
    percentage: NamedNode
    """A percentage amount of the target Asset relevant for exercising the action of the Rule. Right operand value MUST be an xsd:decimal from 0 to 100."""
    perm: NamedNode
    """Permissions take preference over prohibitions."""
    permission: NamedNode
    """Relates an individual Permission to a Policy."""
    play: NamedNode
    """To create a sequential and transient rendition of an Asset."""
    policyUsage: NamedNode
    """Indicates the actual datetime the action of the Rule was exercised."""
    present: NamedNode
    """To publicly perform the Asset."""
    preview: NamedNode
    """The act of providing a short preview of the asset."""
    print: NamedNode
    """To create a tangible and permanent rendition of an Asset."""
    product: NamedNode
    """Category of product or service setting a context for exercising the action of the Rule."""
    profile: NamedNode
    """The identifier(s) of an ODRL Profile that the Policy conforms to."""
    prohibit: NamedNode
    """Prohibitions take preference over permissions."""
    prohibition: NamedNode
    """Relates an individual Prohibition to a Policy."""
    proximity: NamedNode
    """An value indicating the closeness or nearness."""
    purpose: NamedNode
    """A defined purpose for exercising the action of the Rule."""
    read: NamedNode
    """To obtain data from the Asset."""
    recipient: NamedNode
    """The party receiving the result/outcome of exercising the action of the Rule."""
    refinement: NamedNode
    """Constraint used to refine the semantics of an Action, or Party/Asset Collection"""
    relation: NamedNode
    """Relation is an abstract property which creates an explicit link between an Action and an Asset."""
    relativePosition: NamedNode
    """A point in space or time defined with coordinates relative to full measures the positioning of the target Asset."""
    relativeSize: NamedNode
    """Measure(s) of one or two axes for 2D-objects or measure(s) of one to tree axes for 3D-objects - expressed as percentages of full values - of the target Asset."""
    relativeSpatialPosition: NamedNode
    """The relative spatial positions - expressed as percentages of full values - of four corners of a rectangle on a 2D-canvas or the eight corners of a cuboid in a 3D-space of the target Asset."""
    relativeTemporalPosition: NamedNode
    """A point in space or time defined with coordinates relative to full measures the positioning of the target Asset."""
    remedy: NamedNode
    """Relates an individual remedy Duty to a Prohibition."""
    reproduce: NamedNode
    """To make duplicate copies the Asset in any material form."""
    resolution: NamedNode
    """Resolution of the rendition of the target Asset."""
    reviewPolicy: NamedNode
    """To review the Policy applicable to the Asset."""
    rightOperand: NamedNode
    """The value of the right operand in a constraint expression."""
    rightOperandReference: NamedNode
    """A reference to a web resource providing the value for the right operand of a Constraint."""
    scope: NamedNode
    """The identifier of a scope that provides context to the extent of the entity."""
    secondaryUse: NamedNode
    """The act of using the asset for a purpose other than the purpose it was intended for."""
    sell: NamedNode
    """To transfer the ownership of the Asset to a third party with compensation and while deleting the original asset."""
    share: NamedNode
    """The act of the non-commercial reproduction and distribution of the asset to third-parties."""
    shareAlike: NamedNode
    """The act of distributing any derivative asset under the same terms as the original asset."""
    source: NamedNode
    """Reference to a Asset/PartyCollection"""
    spatial: NamedNode
    """A named and identified geospatial area with defined borders which is used for exercising the action of the Rule. An IRI MUST be used to represent this value."""
    spatialCoordinates: NamedNode
    """A set of coordinates setting the borders of a geospatial area used for exercising the action of the Rule. The coordinates MUST include longitude and latitude, they MAY include altitude and the geodetic datum."""
    status: NamedNode
    """the value generated from the leftOperand action or a value related to the leftOperand set as the reference for the comparison."""
    stream: NamedNode
    """To deliver the Asset in real-time."""
    support: NamedNode
    """The Action is to be supported as part of the policy – and the policy remains valid."""
    synchronize: NamedNode
    """To use the Asset in timed relations with media (audio/visual) elements of another Asset."""
    system: NamedNode
    """An identified computing system used for exercising the action of the Rule."""
    systemDevice: NamedNode
    """An identified computing system or computing device used for exercising the action of the Rule."""
    target: NamedNode
    """The target property indicates the Asset that is the primary subject to which the Rule action directly applies."""
    textToSpeech: NamedNode
    """To have a text Asset read out loud."""
    timeInterval: NamedNode
    """A recurring period of time before the next execution of the action of the Rule. Right operand value MUST be an xsd:duration as defined by [[xmlschema11-2]]."""
    timedCount: NamedNode
    """The number of seconds after which timed metering use of the asset begins."""
    trackedParty: NamedNode
    """The Party whose usage is being tracked."""
    trackingParty: NamedNode
    """The Party who is tracking usage."""
    transfer: NamedNode
    """To transfer the ownership of the Asset in perpetuity."""
    transform: NamedNode
    """To convert the Asset into a different format."""
    translate: NamedNode
    """To translate the original natural language of an Asset into another natural language."""
    uid: NamedNode
    """An unambiguous identifier"""
    undefined: NamedNode
    """Relates the strategy used for handling undefined actions to a Policy."""
    uninstall: NamedNode
    """To unload and delete the computer program Asset from a storage device and disable its readiness for operation."""
    unit: NamedNode
    """The unit of measurement of the value of the rightOperand or rightOperandReference of a Constraint."""
    unitOfCount: NamedNode
    """The unit of measure used for counting the executions of the action of the Rule."""
    use: NamedNode
    """To use the Asset"""
    version: NamedNode
    """The version of the target Asset."""
    virtualLocation: NamedNode
    """An identified location of the IT communication space which is relevant for exercising the action of the Rule."""
    watermark: NamedNode
    """To apply a watermark to the Asset."""
    write: NamedNode
    """The act of writing to the Asset."""
    writeTo: NamedNode
    """The act of adding data to the Asset."""
    xone: NamedNode
    """The relation is satisfied when only one, and not more, of the Constaints is satisfied"""
