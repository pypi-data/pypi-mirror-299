from pyoxigraph import NamedNode

from pyrdf_prefix.namespace import PredefinedNamespace


class SSN(PredefinedNamespace):
    """Semantic Sensor Network Ontology"""

    # Conversion-Date: 2024-09-30T10:48+00:00
    # Source: http://www.w3.org/ns/ssn/

    _nsBaseIri = "http://www.w3.org/ns/ssn/"
    _issueWarning = True
    _withContainerMembershipProperty = False
    _nonPyIdentifiers = ()

    Deployment: NamedNode
    """Describes the Deployment of one or more Systems for a particular purpose. Deployment may be done on a Platform."""
    Input: NamedNode
    """Any information that is provided to a Procedure for its use."""
    Output: NamedNode
    """Any information that is reported from a Procedure."""
    Property: NamedNode
    """A quality of an entity. An aspect of an entity that is intrinsic to and cannot exist without the entity."""
    Stimulus: NamedNode
    """An event in the real world that 'triggers' the Sensor. The properties associated to the Stimulus may be different to the eventual observed ObservableProperty. It is the event, not the object, that triggers the Sensor."""
    System: NamedNode
    """System is a unit of abstraction for pieces of infrastructure that implement Procedures. A System may have components, its subsystems, which are other systems."""
    deployedOnPlatform: NamedNode
    """Relation between a Deployment and the Platform on which the Systems are deployed."""
    deployedSystem: NamedNode
    """Relation between a Deployment and a deployed System."""
    detects: NamedNode
    """A relation from a Sensor to the Stimulus that the Sensor detects. The Stimulus itself will be serving as a proxy for some ObservableProperty."""
    forProperty: NamedNode
    """A relation between some aspect of an entity and a Property."""
    hasDeployment: NamedNode
    """Relation between a System and a Deployment, recording that the System is deployed in that Deployment."""
    hasInput: NamedNode
    """Relation between a Procedure and an Input to it."""
    hasOutput: NamedNode
    """Relation between a Procedure and an Output of it."""
    hasProperty: NamedNode
    """Relation between an entity and a Property of that entity."""
    hasSubSystem: NamedNode
    """Relation between a System and its component parts."""
    implementedBy: NamedNode
    """Relation between a Procedure (an algorithm, procedure or method) and an entity that implements that Procedure in some executable way."""
    implements: NamedNode
    """Relation between an entity that implements a Procedure in some executable way and the Procedure (an algorithm, procedure or method)."""
    inDeployment: NamedNode
    """Relation between a Platform and a Deployment, meaning that the deployedSystems of the Deployment are hosted on the Platform."""
    isPropertyOf: NamedNode
    """Relation between a Property and the entity it belongs to."""
    isProxyFor: NamedNode
    """A relation from a Stimulus to the Property that the Stimulus is serving as a proxy for."""
    wasOriginatedBy: NamedNode
    """Relation between an Observation and the Stimulus that originated it."""
