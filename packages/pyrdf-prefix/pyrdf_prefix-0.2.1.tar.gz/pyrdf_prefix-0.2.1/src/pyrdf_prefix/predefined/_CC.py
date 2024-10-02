from pyoxigraph import NamedNode

from pyrdf_prefix.namespace import PredefinedNamespace


class CC(PredefinedNamespace):
    """Creative Commons"""

    # Conversion-Date: 2024-09-30T10:48+00:00
    # Source: https://creativecommons.org/schema.rdf

    _nsBaseIri = "http://creativecommons.org/ns#"
    _issueWarning = True
    _withContainerMembershipProperty = False
    _nonPyIdentifiers = ()

    Attribution: NamedNode
    """credit be given to copyright holder and/or author"""
    CommercialUse: NamedNode
    """exercising rights for commercial purposes"""
    Copyleft: NamedNode
    """derivative and combined works must be licensed under specified terms, similar to those on the original work"""
    DerivativeWorks: NamedNode
    """distribution of derivative works"""
    Distribution: NamedNode
    """distribution, public display, and publicly performance"""
    HighIncomeNationUse: NamedNode
    """use in a non-developing country"""
    Jurisdiction: NamedNode
    """the legal jurisdiction of a license"""
    LesserCopyleft: NamedNode
    """derivative works must be licensed under specified terms, with at least the same conditions as the original work; combinations with the work may be licensed under different terms"""
    License: NamedNode
    """a set of requests/permissions to users of a Work, e.g. a copyright license, the public domain, information for distributors"""
    Notice: NamedNode
    """copyright and license notices be kept intact"""
    Permission: NamedNode
    """an action that may or may not be allowed or desired"""
    Prohibition: NamedNode
    """something you may be asked not to do"""
    Reproduction: NamedNode
    """making multiple copies"""
    Requirement: NamedNode
    """an action that may or may not be requested of you"""
    ShareAlike: NamedNode
    """derivative works be licensed under the same terms or compatible terms as the original work"""
    Sharing: NamedNode
    """permits commercial derivatives, but only non-commercial distribution"""
    SourceCode: NamedNode
    """source code (the preferred form for making modifications) must be provided when exercising some rights granted by the license."""
    Work: NamedNode
    """a potentially copyrightable work"""
