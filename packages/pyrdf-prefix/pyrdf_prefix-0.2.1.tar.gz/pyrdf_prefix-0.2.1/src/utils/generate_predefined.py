import csv
import datetime as dt
import keyword
import urllib.request
from dataclasses import dataclass
from string import Template
from sys import stderr

import pyoxigraph  # noqa
from pyoxigraph import Literal, NamedNode, RdfFormat, Store

type DescMapping = dict[NamedNode, Literal]


@dataclass
class PredefinedClass:
    nsIRI: str  # base namespace, conceptual source
    downloadFormat: RdfFormat | None  # format to parse downloaded file as
    issueWarnings: bool = False  # issue warnings if the local name is unknown
    sourceIRI: str | None = None  # overrides iri, if defined
    hasContainerMembershipProperties: bool = False
    title: str = ""


def load_from_url(info: PredefinedClass) -> DescMapping:
    if info.downloadFormat is None:
        raise ValueError("Cannot attempt to download file without format")

    # Download and parse the original source file
    req = urllib.request.Request(info.sourceIRI or info.nsIRI)
    req.add_header("Accept", "*/*")
    req.add_header("User-Agent", "curl/8.7.1")
    f = urllib.request.urlopen(req)
    store = Store()
    store.load(f, info.downloadFormat, base_iri=info.nsIRI)

    # Get all defined localnames, whether as subject, predicate or object.
    lnames = set()
    filter_subjects = Template("""
        SELECT ?lname WHERE {
            { ?lname ?p ?o . FILTER ( STRSTARTS(str(?lname), "$BASE" ) ) } UNION
            { ?s ?lname ?o . FILTER ( STRSTARTS(str(?lname), "$BASE" ) ) } UNION
            { ?s ?p ?lname . FILTER ( STRSTARTS(str(?lname), "$BASE" ) ) } 
        }
    """).substitute({"BASE": info.nsIRI})

    q = store.query(filter_subjects)  # type: ignore
    q = q  # type: pyoxigraph.QuerySolution
    for row in q:
        lnames.add(row["lname"])

    lname_docstring: DescMapping = dict()

    # Get docstrings of all those lnames
    for lname in lnames:
        get_docstring = Template("""
PREFIX skos: <http://www.w3.org/2004/02/skos/core#>
PREFIX rdfs: <http://www.w3.org/2000/01/rdf-schema#>

SELECT DISTINCT ?docstring WHERE {
  $this rdfs:comment|skos:definition ?ds .

  # The language has to be either EN or have no language tag
  FILTER ( LANGMATCHES(LANG(?ds), "en") || LANG(?ds) = '')

  BIND (?ds AS ?docstring)
}
limit 10

                        """).substitute({"this": lname})
        q = store.query(get_docstring)  # type: ignore
        q = q  # type: pyoxigraph.QuerySolution
        for row in q:
            lname_docstring[lname] = row["docstring"]

    return lname_docstring


def predefined_class_as_string(
    alias: str, contents: DescMapping, info: PredefinedClass
) -> str:
    lnames = ""
    nonPyIdentifiers: list[str] = list()

    for lname in sorted(contents.keys()):
        comment = contents[lname]
        attr = lname.value.removeprefix(info.nsIRI)
        if not len(attr):
            continue  # ignore the `:` subject
        if not attr.isidentifier() or keyword.iskeyword(attr):
            # we can't add this directly, sadly losing docstrings too...
            nonPyIdentifiers.append(attr)
            continue
        docstring = comment.value
        lnames += f'''
    {attr}: NamedNode
    """{docstring}"""'''

    return f'''\
from pyoxigraph import NamedNode

from pyrdf_prefix import PredefinedNamespace

class {alias}(PredefinedNamespace):
    """{info.title}"""
    # Conversion-Date: {dt.datetime.now(dt.UTC).isoformat(timespec='minutes')}
    # Source: {info.sourceIRI or info.nsIRI}

    _nsBaseIri = "{info.nsIRI}"
    _issueWarning = {info.issueWarnings}
    _withContainerMembershipProperty = {info.hasContainerMembershipProperties}
    _nonPyIdentifiers = {tuple(nonPyIdentifiers)}

    {lnames}
'''


def known_prefixes():
    results: dict[str, PredefinedClass] = dict()
    with open("docs/Predefined-Namespaces.tsv") as tsv:
        reader = csv.DictReader(
            tsv,
            (
                "Prefix",
                "NamespaceIRI",
                "SourceIRI",
                "Title",
                "SourceFormat",
                "ReasonForInclusion",
            ),
            delimiter="\t",
        )
        next(reader)
        for line in reader:
            results[line["Prefix"]] = PredefinedClass(
                line["NamespaceIRI"],
                RdfFormat.from_extension(line["SourceFormat"]),
                issueWarnings=True,
                sourceIRI=line["SourceIRI"],
                hasContainerMembershipProperties=line["Prefix"] == "RDF",
                title=line["Title"],
            )

    return results


if __name__ == "__main__":
    failed = set()
    for alias, info in known_prefixes().items():
        try:
            contents = load_from_url(info)
            result = predefined_class_as_string(alias, contents, info)
            outfn = f"src/pyrdf_prefix/predefined/_{alias}.py"
            with open(outfn, "w") as out:
                print(result, file=out)
            print(f"PredefinedNamespace for '{alias}' DONE: {outfn}")
        except Exception as err:
            print(f"PredefinedNamespace for '{alias}' FAIL:", err, file=stderr)
            failed.add(alias)
            continue

    print(f"FAILED: {', '.join(failed)}")
