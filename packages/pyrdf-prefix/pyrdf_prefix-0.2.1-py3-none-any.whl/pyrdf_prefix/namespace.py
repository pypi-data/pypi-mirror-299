import typing as t
import warnings
from functools import lru_cache

from pyoxigraph import NamedNode

__WELL_KNOWN_NAMESPACE_META_ATTR__: set[str] = {
    "_nsBaseIri",
    "_issueWarning",
    "_nonPyIdentifiers",
    "_withContainerMembershipProperty",
}

__WELL_KNOWN_IGNORED_ATTR__: set[str] = {
    "_pytestfixturefunction",  # pytest
}


class PredefinedNamespaceMeta(type):
    _nsBaseIri: str  # Namespace IRI base
    _issueWarning: bool = False  # Issue warning if the accessed local name is unknown
    _nonPyIdentifiers: t.Iterable[str] = (
        tuple()
    )  # Local names that aren't valid Python identifiers
    _withContainerMembershipProperty: bool = False  # For rdf:_1, rdf:_2, ...

    @lru_cache()
    def expand_with(cls, local_name: str) -> NamedNode:
        """Return the NamedNode with concatenated iri and `local_name`."""
        # Do not expand if this is a meta-attribute
        if local_name in __WELL_KNOWN_NAMESPACE_META_ATTR__:
            raise AttributeError("Private use")

        if (
            (cls._issueWarning)
            and local_name not in cls
            and local_name not in __WELL_KNOWN_IGNORED_ATTR__
        ):
            warnings.warn(
                f"Local name '{local_name}' unknown in {cls.__name__} ({cls!r})",
                stacklevel=3,
            )

        return NamedNode(cls._nsBaseIri + local_name)

    def __getitem__(cls, name: str) -> NamedNode:
        """Return a NamedNode when called as `ns[key]`; an alternative to the `ns.key`
        syntax if `key` is not a valid Python identifier OR is a dunder name.
        """
        return cls.expand_with(name)

    def __getattr__(cls, name: str) -> NamedNode:
        """Return a NamedNode when called as`ns.key`."""
        # Only called for non-existing attributes, unlike __getattributes__
        # so not-implemented Python protocols should be skipped
        if name.startswith("__") and name.endswith("__"):
            raise AttributeError("Use the ns[...] syntax for dunder namespaced terms.")
        return cls.expand_with(name)

    def __contains__(cls, name: str) -> bool:
        """To be contained is considered for localnames in c.__annotations__ or
        the extended set in _nonPyIdentifiers.

        Enable rdf:_1, rdf:_2 with _withContainerMembershipProperty = True.
        """
        name = name.removeprefix(cls._nsBaseIri)
        return any(
            (
                name in c.__annotations__
                or name in c._nonPyIdentifiers
                or (
                    cls._withContainerMembershipProperty
                    and name[0] == "_"
                    and name[1:].isdigit()
                )
            )
            for c in cls.mro()
            if issubclass(c, PredefinedNamespace)
        )

    def __repr__(cls) -> str:
        return f"Namespace('{cls._nsBaseIri}')"


class PredefinedNamespace(metaclass=PredefinedNamespaceMeta):
    """Namespace with an optionally predefined list of known members.

    Returns a NamedNode when accessing local names either with dot-access or indexed
    access.

        >>> RDFS = Prefix("http://www.w3.org/2000/01/rdf-schema#")
        >>> RDFS.Class
        <NamedNode value=http://www.w3.org/2000/01/rdf-schema#Class>
        >>> RDFS['label']
        <NamedNode value=http://www.w3.org/2000/01/rdf-schema#label>

    Warnings may be issued if the local name is unknown:

        >>> RDFS['hello,world']
        <stdin>:1: UserWarning: Local name 'hello,world' unknown in RDF (Namespace('http://www.w3.org/2000/01/rdf-schema#'))
        <NamedNode value=http://www.w3.org/1999/02/22-rdf-syntax-ns#label>
    """

    def __init__(self):
        raise TypeError("Predefined namespaces can't be instantiated.")


def Prefix(iri: str) -> type[PredefinedNamespace]:
    """Define a namespace alias."""

    class MyNamespace(PredefinedNamespace):
        _nsBaseIri = iri

    return MyNamespace
