import pytest
from pyoxigraph import NamedNode

from pyrdf_prefix import PredefinedNamespace, Prefix
from pyrdf_prefix.predefined import DCTERMS, RDF


def test_expansion():
    ex = Prefix("http://example.org/ns#")

    assert ex.Foo == NamedNode(value="http://example.org/ns#Foo")
    assert ex["Bar-Baz"] == NamedNode(value="http://example.org/ns#Bar-Baz")


def test_cant_init():
    class MyTestingClass(PredefinedNamespace): ...

    with pytest.raises(TypeError):
        MyTestingClass()


def test_dunder_raise():
    py = Prefix("http://example.org/python/")

    with pytest.raises(AttributeError):
        py.__bool__

    py["__bool__"]


def test_warnings():
    with pytest.warns():
        RDF["hello,world"]

    assert RDF.type == NamedNode("http://www.w3.org/1999/02/22-rdf-syntax-ns#type")


def test_nonpyids():
    # doesn't warn
    DCTERMS["ISO639-3"]

    with pytest.warns():
        DCTERMS["ISO639-3_"]
