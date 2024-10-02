from pyoxigraph import NamedNode

from pyrdf_prefix.namespace import PredefinedNamespace


class AS(PredefinedNamespace):
    """Activity Streams"""

    # Conversion-Date: 2024-09-30T10:48+00:00
    # Source: https://www.w3.org/ns/activitystreams-owl

    _nsBaseIri = "http://www.w3.org/ns/activitystreams#"
    _issueWarning = True
    _withContainerMembershipProperty = False
    _nonPyIdentifiers = ()

    Accept: NamedNode
    """Actor accepts the Object"""
    Activity: NamedNode
    """An Object representing some form of Action that has been taken"""
    Add: NamedNode
    """To Add an Object or Link to Something"""
    Announce: NamedNode
    """Actor announces the object to the target"""
    Application: NamedNode
    """Represents a software application of any sort"""
    Arrive: NamedNode
    """To Arrive Somewhere (can be used, for instance, to indicate that a particular entity is currently located somewhere, e.g. a "check-in")"""
    Article: NamedNode
    """A written work. Typically several paragraphs long. For example, a blog post or a news article."""
    Audio: NamedNode
    """An audio file"""
    Collection: NamedNode
    """An ordered or unordered collection of Objects or Links"""
    CollectionPage: NamedNode
    """A subset of items from a Collection"""
    Create: NamedNode
    """To Create Something"""
    Delete: NamedNode
    """To Delete Something"""
    Dislike: NamedNode
    """The actor dislikes the object"""
    Document: NamedNode
    """Represents a digital document/file of any sort"""
    Event: NamedNode
    """An Event of any kind"""
    Flag: NamedNode
    """To flag something (e.g. flag as inappropriate, flag as spam, etc)"""
    Follow: NamedNode
    """To Express Interest in Something"""
    Group: NamedNode
    """A Group of any kind."""
    Ignore: NamedNode
    """Actor is ignoring the Object"""
    Image: NamedNode
    """An Image file"""
    IntransitiveActivity: NamedNode
    """An Activity that has no direct object"""
    Invite: NamedNode
    """To invite someone or something to something"""
    Join: NamedNode
    """To Join Something"""
    Leave: NamedNode
    """To Leave Something"""
    Like: NamedNode
    """To Like Something"""
    Link: NamedNode
    """Represents a qualified reference to another resource. Patterned after the RFC5988 Web Linking Model"""
    Listen: NamedNode
    """The actor listened to the object"""
    Mention: NamedNode
    """A specialized Link that represents an @mention"""
    Move: NamedNode
    """The actor is moving the object. The target specifies where the object is moving to. The origin specifies where the object is moving from."""
    Note: NamedNode
    """A Short note, typically less than a single paragraph. A "tweet" is an example, or a "status update"""
    Offer: NamedNode
    """To Offer something to someone or something"""
    OrderedCollection: NamedNode
    """A variation of Collection in which items are strictly ordered"""
    OrderedCollectionPage: NamedNode
    """An ordered subset of items from an OrderedCollection"""
    OrderedItems: NamedNode
    """A rdf:List variant for Objects and Links"""
    Organization: NamedNode
    """An Organization"""
    Page: NamedNode
    """A Web Page"""
    Person: NamedNode
    """A Person"""
    Place: NamedNode
    """A physical or logical location"""
    Profile: NamedNode
    """A Profile Document"""
    Question: NamedNode
    """A question of any sort."""
    Read: NamedNode
    """The actor read the object"""
    Reject: NamedNode
    """Actor rejects the Object"""
    Relationship: NamedNode
    """Represents a Social Graph relationship between two Individuals (indicated by the 'a' and 'b' properties)"""
    Remove: NamedNode
    """To Remove Something"""
    Service: NamedNode
    """A service provided by some entity"""
    TentativeAccept: NamedNode
    """Actor tentatively accepts the Object"""
    TentativeReject: NamedNode
    """Actor tentatively rejects the object"""
    Tombstone: NamedNode
    """A placeholder for a deleted object"""
    Travel: NamedNode
    """The actor is traveling to the target. The origin specifies where the actor is traveling from."""
    Undo: NamedNode
    """To Undo Something. This would typically be used to indicate that a previous Activity has been undone."""
    Update: NamedNode
    """To Update/Modify Something"""
    Video: NamedNode
    """A Video document of any kind."""
    View: NamedNode
    """The actor viewed the object"""
    accuracy: NamedNode
    """Specifies the accuracy around the point established by the longitude and latitude"""
    actor: NamedNode
    """Subproperty of as:attributedTo that identifies the primary actor"""
    altitude: NamedNode
    """The altitude of a place"""
    anyOf: NamedNode
    """Describes a possible inclusive answer or option for a question."""
    attributedTo: NamedNode
    """Identifies an entity to which an object is attributed"""
    author: NamedNode
    """Identifies the author of an object. Deprecated. Use as:attributedTo instead"""
    content: NamedNode
    """The content of the object."""
    context: NamedNode
    """Specifies the context within which an object exists or an activity was performed"""
    deleted: NamedNode
    """Specifies the date and time the object was deleted"""
    describes: NamedNode
    """On a Profile object, describes the object described by the profile"""
    duration: NamedNode
    """The duration of the object"""
    endTime: NamedNode
    """The ending time of the object"""
    formerType: NamedNode
    """On a Tombstone object, describes the former type of the deleted object"""
    height: NamedNode
    """The display height expressed as device independent pixels"""
    href: NamedNode
    """The target URI of the Link"""
    hreflang: NamedNode
    """A hint about the language of the referenced resource"""
    instrument: NamedNode
    """Indentifies an object used (or to be used) to complete an activity"""
    latitude: NamedNode
    """The latitude"""
    longitude: NamedNode
    """The longitude"""
    mediaType: NamedNode
    """The MIME Media Type"""
    oneOf: NamedNode
    """Describes a possible exclusive answer or option for a question."""
    origin: NamedNode
    """For certain activities, specifies the entity from which the action is directed."""
    published: NamedNode
    """Specifies the date and time the object was published"""
    radius: NamedNode
    """Specifies a radius around the point established by the longitude and latitude"""
    rating: NamedNode
    """A numeric rating (>= 0.0, <= 5.0) for the object"""
    rel: NamedNode
    """The RFC 5988 or HTML5 Link Relation associated with the Link"""
    relationship: NamedNode
    """On a Relationship object, describes the type of relationship"""
    startIndex: NamedNode
    """In a strictly ordered logical collection, specifies the index position of the first item in the items list"""
    startTime: NamedNode
    """The starting time of the object"""
    subject: NamedNode
    """On a Relationship object, identifies the subject. e.g. when saying "John is connected to Sally", 'subject' refers to 'John'"""
    summary: NamedNode
    """A short summary of the object"""
    totalItems: NamedNode
    """The total number of items in a logical collection"""
    units: NamedNode
    """Identifies the unit of measurement used by the radius, altitude and accuracy properties. The value can be expressed either as one of a set of predefined units or as a well-known common URI that identifies units."""
    updated: NamedNode
    """Specifies when the object was last updated"""
    url: NamedNode
    """Specifies a link to a specific representation of the Object"""
    width: NamedNode
    """Specifies the preferred display width of the content, expressed in terms of device independent pixels."""
