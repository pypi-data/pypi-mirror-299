from pyrdf_prefix.namespace import PredefinedNamespace


class RDFA(PredefinedNamespace):
    """RDFa Vocabulary for Term and Prefix Assignment"""

    # Conversion-Date: 2024-09-30T10:48+00:00
    # Source: https://www.w3.org/ns/rdfa.ttl

    _nsBaseIri = "http://www.w3.org/ns/rdfa#"
    _issueWarning = True
    _withContainerMembershipProperty = False
    _nonPyIdentifiers = ()
