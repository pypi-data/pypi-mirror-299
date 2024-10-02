from pyoxigraph import NamedNode

from pyrdf_prefix.namespace import PredefinedNamespace


class QB(PredefinedNamespace):
    """The data cube vocabulary"""

    # Conversion-Date: 2024-09-30T10:48+00:00
    # Source: http://purl.org/linked-data/cube#

    _nsBaseIri = "http://purl.org/linked-data/cube#"
    _issueWarning = True
    _withContainerMembershipProperty = False
    _nonPyIdentifiers = ()

    Attachable: NamedNode
    """Abstract superclass for everything that can have attributes and dimensions"""
    AttributeProperty: NamedNode
    """The class of components which represent attributes of observations in the cube, e.g. unit of measurement"""
    CodedProperty: NamedNode
    """Superclass of all coded ComponentProperties"""
    ComponentProperty: NamedNode
    """Abstract super-property of all properties representing dimensions, attributes or measures"""
    ComponentSet: NamedNode
    """Abstract class of things which reference one or more ComponentProperties"""
    ComponentSpecification: NamedNode
    """Used to define properties of a component (attribute, dimension etc) which are specific to its usage in a DSD."""
    DataSet: NamedNode
    """Represents a collection of observations, possibly organized into various slices, conforming to some common dimensional structure."""
    DataStructureDefinition: NamedNode
    """Defines the structure of a DataSet or slice"""
    DimensionProperty: NamedNode
    """The class of components which represent the dimensions of the cube"""
    HierarchicalCodeList: NamedNode
    """Represents a generalized hierarchy of concepts which can be used for coding. The hierarchy is defined by one or more roots together with a property which relates concepts in the hierarchy to thier child concept .  The same concepts may be members of multiple hierarchies provided that different qb:parentChildProperty values are used for each hierarchy."""
    MeasureProperty: NamedNode
    """The class of components which represent the measured value of the phenomenon being observed"""
    Observation: NamedNode
    """A single observation in the cube, may have one or more associated measured values"""
    ObservationGroup: NamedNode
    """A, possibly arbitrary, group of observations."""
    Slice: NamedNode
    """Denotes a subset of a DataSet defined by fixing a subset of the dimensional values, component properties on the Slice"""
    SliceKey: NamedNode
    """Denotes a subset of the component properties of a DataSet which are fixed in the corresponding slices"""
    attribute: NamedNode
    """An alternative to qb:componentProperty which makes explicit that the component is a attribute"""
    codeList: NamedNode
    """gives the code list associated with a CodedProperty"""
    component: NamedNode
    """indicates a component specification which is included in the structure of the dataset"""
    componentAttachment: NamedNode
    """Indicates the level at which the component property should be attached, this might an qb:DataSet, qb:Slice or qb:Observation, or a qb:MeasureProperty."""
    componentProperty: NamedNode
    """indicates a ComponentProperty (i.e. attribute/dimension) expected on a DataSet, or a dimension fixed in a SliceKey"""
    componentRequired: NamedNode
    """Indicates whether a component property is required (true) or optional (false) in the context of a DSD. Only applicable
    to components correspond to an attribute. Defaults to false (optional)."""
    concept: NamedNode
    """gives the concept which is being measured or indicated by a ComponentProperty"""
    dataSet: NamedNode
    """indicates the data set of which this observation is a part"""
    dimension: NamedNode
    """An alternative to qb:componentProperty which makes explicit that the component is a dimension"""
    hierarchyRoot: NamedNode
    """Specifies a root of the hierarchy. A hierarchy may have multiple roots but must have at least one."""
    measure: NamedNode
    """An alternative to qb:componentProperty which makes explicit that the component is a measure"""
    measureDimension: NamedNode
    """An alternative to qb:componentProperty which makes explicit that the component is a measure dimension"""
    measureType: NamedNode
    """Generic measure dimension, the value of this dimension indicates which measure (from the set of measures in the DSD) is being given by the obsValue (or other primary measure)"""
    observation: NamedNode
    """indicates a observation contained within this slice of the data set"""
    observationGroup: NamedNode
    """Indicates a group of observations. The domain of this property is left open so that a group may be attached to different resources and need not be restricted to a single DataSet"""
    order: NamedNode
    """indicates a priority order for the components of sets with this structure, used to guide presentations - lower order numbers come before higher numbers, un-numbered components come last"""
    parentChildProperty: NamedNode
    """Specifies a property which relates a parent concept in the hierarchy to a child concept."""
    slice: NamedNode
    """Indicates a subset of a DataSet defined by fixing a subset of the dimensional values"""
    sliceKey: NamedNode
    """indicates a slice key which is used for slices in this dataset"""
    sliceStructure: NamedNode
    """indicates the sub-key corresponding to this slice"""
    structure: NamedNode
    """indicates the structure to which this data set conforms"""
