from pyoxigraph import NamedNode

from pyrdf_prefix.namespace import PredefinedNamespace


class DOAP(PredefinedNamespace):
    """Description of a Project (DOAP) vocabulary"""

    # Conversion-Date: 2024-09-30T10:48+00:00
    # Source: http://usefulinc.com/ns/doap#

    _nsBaseIri = "http://usefulinc.com/ns/doap#"
    _issueWarning = True
    _withContainerMembershipProperty = False
    _nonPyIdentifiers = (
        "anon-root",
        "bug-database",
        "developer-forum",
        "download-mirror",
        "download-page",
        "file-release",
        "mailing-list",
        "old-homepage",
        "programming-language",
        "security-contact",
        "security-policy",
        "service-endpoint",
        "support-forum",
    )

    ArchRepository: NamedNode
    """GNU Arch source code repository."""
    BKRepository: NamedNode
    """BitKeeper source code repository."""
    BazaarBranch: NamedNode
    """Bazaar source code branch."""
    CVSRepository: NamedNode
    """CVS source code repository."""
    DarcsRepository: NamedNode
    """darcs source code repository."""
    GitBranch: NamedNode
    """Git source code branch."""
    GitRepository: NamedNode
    """Git source code repository."""
    HgRepository: NamedNode
    """Mercurial source code repository."""
    Project: NamedNode
    """A project."""
    Repository: NamedNode
    """Source code repository."""
    SVNRepository: NamedNode
    """Subversion source code repository."""
    Specification: NamedNode
    """A specification of a system's aspects, technical or otherwise."""
    Version: NamedNode
    """Version information of a project release."""
    audience: NamedNode
    """Description of target user base"""
    blog: NamedNode
    """URI of a blog related to a project"""
    browse: NamedNode
    """Web browser interface to repository."""
    category: NamedNode
    """A category of project."""
    created: NamedNode
    """Date when something was created, in YYYY-MM-DD form. e.g. 2004-04-05"""
    description: NamedNode
    """Plain text description of a project, of 2-4 sentences in length."""
    developer: NamedNode
    """Developer of software for the project."""
    documentation: NamedNode
    """Documentation of the project."""
    documenter: NamedNode
    """Contributor of documentation to the project."""
    helper: NamedNode
    """Project contributor."""
    homepage: NamedNode
    """URL of a project's homepage,
		associated with exactly one project."""
    implements: NamedNode
    """A specification that a project implements. Could be a standard, API or legally defined level of conformance."""
    language: NamedNode
    """BCP47 language code a project has been translated into"""
    license: NamedNode
    """The URI of an RDF description of the license the software is distributed under. E.g. a SPDX reference"""
    location: NamedNode
    """Location of a repository."""
    maintainer: NamedNode
    """Maintainer of a project, a project leader."""
    module: NamedNode
    """Module name of a Subversion, CVS, BitKeeper or Arch repository."""
    name: NamedNode
    """A name of something."""
    os: NamedNode
    """Operating system that a project is limited to.  Omit this property if the project is not OS-specific."""
    platform: NamedNode
    """Indicator of software platform (non-OS specific), e.g. Java, Firefox, ECMA CLR"""
    release: NamedNode
    """A project release."""
    repository: NamedNode
    """Source code repository."""
    repositoryOf: NamedNode
    """The project that uses a repository."""
    revision: NamedNode
    """Revision identifier of a software release."""
    screenshots: NamedNode
    """Web page with screenshots of project."""
    shortdesc: NamedNode
    """Short (8 or 9 words) plain text description of a project."""
    tester: NamedNode
    """A tester or other quality control contributor."""
    translator: NamedNode
    """Contributor of translations to the project."""
    vendor: NamedNode
    """Vendor organization: commercial, free or otherwise"""
    wiki: NamedNode
    """URL of Wiki for collaborative discussion of project."""
