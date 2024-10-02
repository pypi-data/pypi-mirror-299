from pyoxigraph import NamedNode

from pyrdf_prefix.namespace import PredefinedNamespace


class OG(PredefinedNamespace):
    """The Open Graph protocol"""

    # Conversion-Date: 2024-09-30T10:48+00:00
    # Source: https://ogp.me/ns/ogp.me.ttl

    _nsBaseIri = "http://ogp.me/ns#"
    _issueWarning = True
    _withContainerMembershipProperty = False
    _nonPyIdentifiers = (
        "audio:album",
        "audio:artist",
        "audio:secure_url",
        "audio:title",
        "audio:type",
        "country-name",
        "image:height",
        "image:secure_url",
        "image:type",
        "image:width",
        "postal-code",
        "street-address",
        "video:height",
        "video:secure_url",
        "video:type",
        "video:width",
    )

    audio: NamedNode
    """A relevant audio URL for your object."""
    description: NamedNode
    """A one to two sentence description of your object."""
    determiner: NamedNode
    """The word to precede the object's title in a sentence (e.g., "the" in "the statue of liberty").  Valid values are "a", "an", "the", "", and "auto"."""
    email: NamedNode
    """[DEPRECATED] Email of the contact for your object."""
    fax_number: NamedNode
    """[DEPRECATED] Fax number of the contact for your object."""
    image: NamedNode
    """An image URL which should represent your object within the graph."""
    isbn: NamedNode
    """[DEPRECATED] International Standard Book Number for you object."""
    latitude: NamedNode
    """[DEPRECATED] The latitude of the resource e.g., the latitude of a company."""
    locale: NamedNode
    """A Unix locale in which this markup is rendered."""
    locality: NamedNode
    """[DEPRECATED] The locality of the resource e.g, "Palo Alto"""
    longitude: NamedNode
    """[DEPRECATED] The longitude of the resource e.g., the longitude of a company."""
    phone_number: NamedNode
    """[DEPRECATED] Phone number of the contact for your object."""
    region: NamedNode
    """[DEPRECATED] The region of the resource e.g., "CA"""
    site_name: NamedNode
    """If your object is part of a larger web site, the name which should be displayed for the overall site. e.g., "IMDb"."""
    title: NamedNode
    """The title of the object as it should appear within the graph, e.g.,  "The Rock"."""
    type: NamedNode
    """The type of your object, e.g., "movie".  Depending on the type you specify, other properties may also be required."""
    upc: NamedNode
    """[DEPRECATED] Universal Product Code for your object."""
    url: NamedNode
    """The canonical URL of your object that will be used as its permanent ID in the graph, e.g., "http://www.imdb.com/title/tt0117500/"."""
    video: NamedNode
    """A relevant video URL for your object."""
