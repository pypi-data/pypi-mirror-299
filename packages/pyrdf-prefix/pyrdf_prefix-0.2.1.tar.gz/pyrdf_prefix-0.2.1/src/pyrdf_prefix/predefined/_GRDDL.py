from pyoxigraph import NamedNode

from pyrdf_prefix.namespace import PredefinedNamespace


class GRDDL(PredefinedNamespace):
    """Gleaning resource descriptions from dialects of languages (defunct?)"""

    # Conversion-Date: 2024-09-30T10:48+00:00
    # Source: https://www.w3.org/2003/g/data-view.rdf

    _nsBaseIri = "http://www.w3.org/2003/g/data-view#"
    _issueWarning = True
    _withContainerMembershipProperty = False
    _nonPyIdentifiers = ()

    InformationResource: NamedNode
    """A resource which has the property that all of its essential characteristics can be conveyed in a message"""
    RDFGraph: NamedNode
    """a
    set of RDF triples"""
    RootNode: NamedNode
    """the root of the tree in the XPath data
    model"""
    Transformation: NamedNode
    """an InformationResource that specifies
    a transformation from a set of XML documents to RDF graphs"""
    TransformationProperty: NamedNode
    """a FunctionalProperty that relates
    XML document root nodes to
    RDF graphs"""
    namespaceTransformation: NamedNode
    """relates a namespace to a transformation for
    all documents in that namespace"""
    profileTransformation: NamedNode
    """relates a profile document to a
    transformation for all documents bearing that profile"""
    result: NamedNode
    """an
    RDF graph obtained from an information resource by directly
    parsing a representation in the standard RDF/XML syntax or
    indirectly by parsing some other dialect using a transformation
    nominated by the document"""
    transformation: NamedNode
    """relates a source document to a
    transformation, usually represented in XSLT, that relates the source document syntax
    to the RDF graph syntax"""
    transformationProperty: NamedNode
    """relates a transformation to the algorithm
    specified by the property that computes an RDF graph from an XML
    document node"""
