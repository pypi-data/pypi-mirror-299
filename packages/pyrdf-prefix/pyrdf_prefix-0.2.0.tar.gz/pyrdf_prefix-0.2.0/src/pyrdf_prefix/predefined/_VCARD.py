from pyoxigraph import NamedNode

from pyrdf_prefix.namespace import PredefinedNamespace


class VCARD(PredefinedNamespace):
    """Ontology for vCard based on RFC6350"""

    # Conversion-Date: 2024-09-30T10:48+00:00
    # Source: http://www.w3.org/2006/vcard/ns#

    _nsBaseIri = "http://www.w3.org/2006/vcard/ns#"
    _issueWarning = True
    _withContainerMembershipProperty = False
    _nonPyIdentifiers = (
        "additional-name",
        "class",
        "country-name",
        "extended-address",
        "family-name",
        "given-name",
        "honorific-prefix",
        "honorific-suffix",
        "organization-name",
        "organization-unit",
        "post-office-box",
        "postal-code",
        "sort-string",
        "street-address",
    )

    Address: NamedNode
    """To specify the components of the delivery address for the  object"""
    BBS: NamedNode
    """This class is deprecated"""
    Car: NamedNode
    """This class is deprecated"""
    Cell: NamedNode
    """Also called mobile telephone"""
    Dom: NamedNode
    """This class is deprecated"""
    Email: NamedNode
    """To specify the electronic mail address for communication with the object the vCard represents. Use the hasEmail object property."""
    Gender: NamedNode
    """Used for gender codes. The URI of the gender code must be used as the value for Gender."""
    Group: NamedNode
    """Object representing a group of persons or entities.  A group object will usually contain hasMember properties to specify the members of the group."""
    Home: NamedNode
    """This implies that the property is related to an individual's personal life"""
    ISDN: NamedNode
    """This class is deprecated"""
    Individual: NamedNode
    """An object representing a single person or entity"""
    Internet: NamedNode
    """This class is deprecated"""
    Intl: NamedNode
    """This class is deprecated"""
    Kind: NamedNode
    """The parent class for all objects"""
    Label: NamedNode
    """This class is deprecated"""
    Location: NamedNode
    """An object representing a named geographical place"""
    Modem: NamedNode
    """This class is deprecated"""
    Msg: NamedNode
    """This class is deprecated"""
    Name: NamedNode
    """To specify the components of the name of the object"""
    Organization: NamedNode
    """An object representing an organization.  An organization is a single entity, and might represent a business or government, a department or division within a business or government, a club, an association, or the like.
"""
    PCS: NamedNode
    """This class is deprecated"""
    Parcel: NamedNode
    """This class is deprecated"""
    Postal: NamedNode
    """This class is deprecated"""
    Pref: NamedNode
    """This class is deprecated"""
    RelatedType: NamedNode
    """Used for relation type codes. The URI of the relation type code must be used as the value for the Relation Type."""
    Tel: NamedNode
    """This class is deprecated. Use the hasTelephone object property."""
    TelephoneType: NamedNode
    """Used for telephone type codes. The URI of the telephone type code must be used as the value for the Telephone Type."""
    Text: NamedNode
    """Also called sms telephone"""
    Type: NamedNode
    """Used for type codes. The URI of the type code must be used as the value for Type."""
    VCard: NamedNode
    """The vCard class is  equivalent to the new Kind class, which is the parent for the four explicit types of vCards (Individual, Organization, Location, Group)"""
    Work: NamedNode
    """This implies that the property is related to an individual's work place"""
    X400: NamedNode
    """This class is deprecated"""
    adr: NamedNode
    """This object property has been mapped"""
    agent: NamedNode
    """This object property has been deprecated"""
    anniversary: NamedNode
    """The date of marriage, or equivalent, of the object"""
    bday: NamedNode
    """To specify the birth date of the object"""
    category: NamedNode
    """The category information about the object, also known as tags"""
    email: NamedNode
    """This object property has been mapped"""
    fn: NamedNode
    """The formatted text corresponding to the name of the object"""
    geo: NamedNode
    """This object property has been mapped"""
    hasAdditionalName: NamedNode
    """Used to support property parameters for the additional name data property"""
    hasAddress: NamedNode
    """To specify the components of the delivery address for the object"""
    hasCalendarBusy: NamedNode
    """To specify the busy time associated with the object. (Was called FBURL in RFC6350)"""
    hasCalendarLink: NamedNode
    """To specify the calendar associated with the object. (Was called CALURI in RFC6350)"""
    hasCalendarRequest: NamedNode
    """To specify the calendar user address to which a scheduling request be sent for the object. (Was called CALADRURI in RFC6350)"""
    hasCategory: NamedNode
    """Used to support property parameters for the category data property"""
    hasCountryName: NamedNode
    """Used to support property parameters for the country name data property"""
    hasEmail: NamedNode
    """To specify the electronic mail address for communication with the object"""
    hasFN: NamedNode
    """Used to support property parameters for the formatted name data property"""
    hasFamilyName: NamedNode
    """Used to support property parameters for the family name data property"""
    hasGender: NamedNode
    """To specify  the sex or gender identity of the object. URIs are recommended to enable interoperable sex and gender codes to be used."""
    hasGeo: NamedNode
    """To specify information related to the global positioning of the object. May also be used as a property parameter."""
    hasGivenName: NamedNode
    """Used to support property parameters for the given name data property"""
    hasHonorificPrefix: NamedNode
    """Used to support property parameters for the honorific prefix data property"""
    hasHonorificSuffix: NamedNode
    """Used to support property parameters for the honorific suffix data property"""
    hasInstantMessage: NamedNode
    """To specify the instant messaging and presence protocol communications with the object. (Was called IMPP in RFC6350)"""
    hasKey: NamedNode
    """To specify a public key or authentication certificate associated with the object"""
    hasLanguage: NamedNode
    """Used to support property parameters for the language data property"""
    hasLocality: NamedNode
    """Used to support property parameters for the locality data property"""
    hasLogo: NamedNode
    """To specify a graphic image of a logo associated with the object """
    hasMember: NamedNode
    """To include a member in the group this object represents. (This property can only be used by Group individuals)"""
    hasName: NamedNode
    """To specify the components of the name of the object"""
    hasNickname: NamedNode
    """Used to support property parameters for the nickname data property"""
    hasNote: NamedNode
    """Used to support property parameters for the note data property"""
    hasOrganizationName: NamedNode
    """Used to support property parameters for the organization name data property"""
    hasOrganizationUnit: NamedNode
    """Used to support property parameters for the organization unit name data property"""
    hasPhoto: NamedNode
    """To specify an image or photograph information that annotates some aspect of the object"""
    hasPostalCode: NamedNode
    """Used to support property parameters for the postal code data property"""
    hasRegion: NamedNode
    """Used to support property parameters for the region data property"""
    hasRelated: NamedNode
    """To specify a relationship between another entity and the entity represented by this object"""
    hasRole: NamedNode
    """Used to support property parameters for the role data property"""
    hasSound: NamedNode
    """To specify a digital sound content information that annotates some aspect of the object"""
    hasSource: NamedNode
    """To identify the source of directory information of the object"""
    hasStreetAddress: NamedNode
    """Used to support property parameters for the street address data property"""
    hasTelephone: NamedNode
    """To specify the telephone number for telephony communication with the object"""
    hasTitle: NamedNode
    """Used to support property parameters for the title data property"""
    hasUID: NamedNode
    """To specify a value that represents a globally unique identifier corresponding to the object"""
    hasURL: NamedNode
    """To specify a uniform resource locator associated with the object"""
    hasValue: NamedNode
    """Used to indicate the resource value of an object property that requires property parameters"""
    key: NamedNode
    """This object property has been mapped"""
    label: NamedNode
    """This data property has been deprecated"""
    language: NamedNode
    """To specify the language that may be used for contacting the object. May also be used as a property parameter."""
    latitude: NamedNode
    """This data property has been deprecated. See hasGeo"""
    locality: NamedNode
    """The locality (e.g. city or town) associated with the address of the object"""
    logo: NamedNode
    """This object property has been mapped"""
    longitude: NamedNode
    """This data property has been deprecated. See hasGeo"""
    mailer: NamedNode
    """This data property has been deprecated"""
    n: NamedNode
    """This object property has been mapped"""
    nickname: NamedNode
    """The nick name associated with the object"""
    note: NamedNode
    """A note associated with the object"""
    org: NamedNode
    """This object property has been mapped. Use the organization-name data property."""
    photo: NamedNode
    """This object property has been mapped"""
    prodid: NamedNode
    """To specify the identifier for the product that created the object"""
    region: NamedNode
    """The region (e.g. state or province) associated with the address of the object"""
    rev: NamedNode
    """To specify revision information about the object"""
    role: NamedNode
    """To specify the function or part played in a particular situation by the object"""
    sound: NamedNode
    """This object property has been mapped"""
    tel: NamedNode
    """This object property has been mapped"""
    title: NamedNode
    """To specify the position or job of the object"""
    tz: NamedNode
    """To indicate time zone information that is specific to the object. May also be used as a property parameter."""
    url: NamedNode
    """This object property has been mapped"""
    value: NamedNode
    """Used to indicate the literal value of a data property that requires property parameters"""
