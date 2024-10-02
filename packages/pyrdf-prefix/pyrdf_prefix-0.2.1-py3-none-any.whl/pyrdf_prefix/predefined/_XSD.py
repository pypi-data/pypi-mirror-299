from pyoxigraph import NamedNode

from pyrdf_prefix.namespace import PredefinedNamespace


class XSD(PredefinedNamespace):
    """W3C XML Schema Definition Language (XSD) 1.1 Part 2: Datatypes"""

    _nsBaseIri = "http://www.w3.org/2001/XMLSchema#"
    _issueWarning = False

    # This module was written by hand

    anyURI: NamedNode
    base64Binary: NamedNode
    boolean: NamedNode
    byte: NamedNode
    date: NamedNode
    dateTime: NamedNode
    dateTimeStamp: NamedNode
    dayTimeDuration: NamedNode
    decimal: NamedNode
    double: NamedNode
    duration: NamedNode
    ENTITIES: NamedNode
    ENTITY: NamedNode
    float: NamedNode
    gDay: NamedNode
    gMonth: NamedNode
    gMonthDay: NamedNode
    gYear: NamedNode
    gYearMonth: NamedNode
    hexBinary: NamedNode
    ID: NamedNode
    IDREF: NamedNode
    IDREFS: NamedNode
    int: NamedNode
    integer: NamedNode
    language: NamedNode
    long: NamedNode
    Name: NamedNode
    NCName: NamedNode
    negativeInteger: NamedNode
    NMTOKEN: NamedNode
    NMTOKENS: NamedNode
    nonNegativeInteger: NamedNode
    nonPositiveInteger: NamedNode
    normalizedString: NamedNode
    NOTATION: NamedNode
    positiveInteger: NamedNode
    QName: NamedNode
    short: NamedNode
    string: NamedNode
    time: NamedNode
    token: NamedNode
    unsignedByte: NamedNode
    unsignedInt: NamedNode
    unsignedLong: NamedNode
    unsignedShort: NamedNode
    yearMonthDuration: NamedNode
