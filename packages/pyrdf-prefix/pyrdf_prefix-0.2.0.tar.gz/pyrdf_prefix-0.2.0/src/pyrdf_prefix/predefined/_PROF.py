from pyoxigraph import NamedNode

from pyrdf_prefix.namespace import PredefinedNamespace


class PROF(PredefinedNamespace):
    """Profiles Vocabulary"""

    # Conversion-Date: 2024-09-30T10:48+00:00
    # Source: https://www.w3.org/TR/dx-prof/rdf/prof.ttl

    _nsBaseIri = "http://www.w3.org/ns/dx/prof/"
    _issueWarning = True
    _withContainerMembershipProperty = False
    _nonPyIdentifiers = ()

    Profile: NamedNode
    """A specification that constrains, extends, combines, or provides guidance or explanation about the usage of other specifications.

This definition includes what are often called "application profiles", "metadata application profiles", or "metadata profiles"."""
    ResourceDescriptor: NamedNode
    """A description of a resource that defines an aspect - a particular part, feature or role - of a Profile"""
    ResourceRole: NamedNode
    """A role that an profile resource, described by a Resource Descriptor, plays"""
    hasArtifact: NamedNode
    """The URL of a downloadable file with particulars such as its format and role indicated by the Resource Descriptor"""
    hasResource: NamedNode
    """A resource which describes the nature of an artifact and the role it plays in relation to the Profile"""
    hasRole: NamedNode
    """The function of an artifact described by a Resource Descriptor, such as specification, guidance etc."""
    hasToken: NamedNode
    """The preferred identifier for the Profile, for use in circumstances where its URI cannot be used"""
    isInheritedFrom: NamedNode
    """A base specification, a Resource Descriptor from which is to be considered a Resource Descriptor for this Profile also"""
    isProfileOf: NamedNode
    """A specification for which this Profile defines constraints, extensions, or which it uses in combination with other specifications, or provides guidance or explanation about its usage"""
    isTransitiveProfileOf: NamedNode
    """The transitive closure of the prof:isProfileOf property. Relates a profile to another specification that it is a profile of, possibly via a chain of intermediate profiles that are in prof:isProfileOf relationships"""
