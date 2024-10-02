from pyoxigraph import NamedNode

from pyrdf_prefix.namespace import PredefinedNamespace


class SKOSXL(PredefinedNamespace):
    """SKOS Simple Knowledge Organization System eXtension for Labels (SKOS-XL)"""

    # Conversion-Date: 2024-09-30T10:48+00:00
    # Source: http://www.w3.org/TR/skos-reference/skos-xl.rdf

    _nsBaseIri = "http://www.w3.org/2008/05/skos-xl#"
    _issueWarning = True
    _withContainerMembershipProperty = False
    _nonPyIdentifiers = ()

    Label: NamedNode
    """A special class of lexical entities."""
    altLabel: NamedNode
    """The property skosxl:altLabel is used to associate an skosxl:Label with a skos:Concept. The property is analogous to skos:altLabel."""
    hiddenLabel: NamedNode
    """The property skosxl:hiddenLabel is used to associate an skosxl:Label with a skos:Concept. The property is analogous to skos:hiddenLabel."""
    labelRelation: NamedNode
    """The property skosxl:labelRelation is used for representing binary ('direct') relations between instances of the class skosxl:Label."""
    literalForm: NamedNode
    """The property skosxl:literalForm is used to give the literal form of an skosxl:Label."""
    prefLabel: NamedNode
    """The property skosxl:prefLabel is used to associate an skosxl:Label with a skos:Concept. The property is analogous to skos:prefLabel."""
