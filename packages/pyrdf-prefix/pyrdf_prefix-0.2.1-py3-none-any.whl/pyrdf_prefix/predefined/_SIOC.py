from pyoxigraph import NamedNode

from pyrdf_prefix.namespace import PredefinedNamespace


class SIOC(PredefinedNamespace):
    """Semantically-Interlinked Online Communities"""

    # Conversion-Date: 2024-09-30T10:48+00:00
    # Source: http://rdfs.org/sioc/ns#

    _nsBaseIri = "http://rdfs.org/sioc/ns#"
    _issueWarning = True
    _withContainerMembershipProperty = False
    _nonPyIdentifiers = ()

    Community: NamedNode
    """Community is a high-level concept that defines an online community and what it consists of."""
    Container: NamedNode
    """An area in which content Items are contained."""
    Forum: NamedNode
    """A discussion area on which Posts or entries are made."""
    Item: NamedNode
    """An Item is something which can be in a Container."""
    Post: NamedNode
    """An article or message that can be posted to a Forum."""
    Role: NamedNode
    """A Role is a function of a UserAccount within a scope of a particular Forum, Site, etc."""
    Site: NamedNode
    """A Site can be the location of an online community or set of communities, with UserAccounts and Usergroups creating Items in a set of Containers. It can be thought of as a web-accessible data Space."""
    Space: NamedNode
    """A Space is a place where data resides, e.g. on a website, desktop, fileshare, etc."""
    Thread: NamedNode
    """A container for a series of threaded discussion Posts or Items."""
    User: NamedNode
    """UserAccount is now preferred. This is a deprecated class for a User in an online community site."""
    UserAccount: NamedNode
    """A user account in an online community site."""
    Usergroup: NamedNode
    """A set of UserAccounts whose owners have a common purpose or interest. Can be used for access control purposes."""
    about: NamedNode
    """Specifies that this Item is about a particular resource, e.g. a Post describing a book, hotel, etc."""
    account_of: NamedNode
    """Refers to the foaf:Agent or foaf:Person who owns this sioc:UserAccount."""
    addressed_to: NamedNode
    """Refers to who (e.g. a UserAccount, e-mail address, etc.) a particular Item is addressed to."""
    administrator_of: NamedNode
    """A Site that the UserAccount is an administrator of."""
    attachment: NamedNode
    """The URI of a file attached to an Item."""
    avatar: NamedNode
    """An image or depiction used to represent this UserAccount."""
    container_of: NamedNode
    """An Item that this Container contains."""
    content: NamedNode
    """The content of the Item in plain text format."""
    content_encoded: NamedNode
    """The encoded content of the Post, contained in CDATA areas."""
    created_at: NamedNode
    """When this was created, in ISO 8601 format."""
    creator_of: NamedNode
    """A resource that the UserAccount is a creator of."""
    delivered_at: NamedNode
    """When this was delivered, in ISO 8601 format."""
    description: NamedNode
    """The content of the Post."""
    discussion_of: NamedNode
    """The Item that this discussion is about."""
    earlier_version: NamedNode
    """Links to a previous (older) revision of this Item or Post."""
    email: NamedNode
    """An electronic mail address of the UserAccount."""
    email_sha1: NamedNode
    """An electronic mail address of the UserAccount, encoded using SHA1."""
    embeds_knowledge: NamedNode
    """This links Items to embedded statements, facts and structured content."""
    feed: NamedNode
    """A feed (e.g. RSS, Atom, etc.) pertaining to this resource (e.g. for a Forum, Site, UserAccount, etc.)."""
    first_name: NamedNode
    """First (real) name of this User. Synonyms include given name or christian name."""
    follows: NamedNode
    """Indicates that one UserAccount follows another UserAccount (e.g. for microblog posts or other content item updates)."""
    function_of: NamedNode
    """A UserAccount that has this Role."""
    generator: NamedNode
    """A URI for the application used to generate this Item."""
    has_administrator: NamedNode
    """A UserAccount that is an administrator of this Site."""
    has_container: NamedNode
    """The Container to which this Item belongs."""
    has_creator: NamedNode
    """This is the UserAccount that made this resource."""
    has_discussion: NamedNode
    """A discussion that is related to this Item. The discussion can be anything, for example, a sioc:Forum or sioc:Thread, a sioct:WikiArticle or simply a foaf:Document."""
    has_function: NamedNode
    """A Role that this UserAccount has."""
    has_host: NamedNode
    """The Site that hosts this Container."""
    has_member: NamedNode
    """A UserAccount that is a member of this Usergroup."""
    has_moderator: NamedNode
    """A UserAccount that is a moderator of this Forum."""
    has_modifier: NamedNode
    """A UserAccount that modified this resource (e.g. Item, Container, Space)."""
    has_owner: NamedNode
    """A UserAccount that this resource is owned by."""
    has_parent: NamedNode
    """A Container or Forum that this Container or Forum is a child of."""
    has_part: NamedNode
    """An resource that is a part of this subject."""
    has_reply: NamedNode
    """Points to an Item or Post that is a reply or response to this Item or Post."""
    has_scope: NamedNode
    """A resource that this Role applies to."""
    has_space: NamedNode
    """A data Space which this resource is a part of."""
    has_subscriber: NamedNode
    """A UserAccount that is subscribed to this Container."""
    has_usergroup: NamedNode
    """Points to a Usergroup that has certain access to this Space."""
    host_of: NamedNode
    """A Container that is hosted on this Site."""
    id: NamedNode
    """An identifier of a SIOC concept instance. For example, a user ID. Must be unique for instances of each type of SIOC concept within the same site."""
    ip_address: NamedNode
    """The IP address used when creating this Item, UserAccount, etc. This can be associated with a creator. Some wiki articles list the IP addresses for the creator or modifiers when the usernames are absent."""
    last_activity_date: NamedNode
    """The date and time of the last activity associated with a SIOC concept instance, and expressed in ISO 8601 format. This could be due to a reply Post or Comment, a modification to an Item, etc."""
    last_item_date: NamedNode
    """The date and time of the last Post (or Item) in a Forum (or a Container), in ISO 8601 format."""
    last_name: NamedNode
    """Last (real) name of this user. Synonyms include surname or family name."""
    last_reply_date: NamedNode
    """The date and time of the last reply Post or Comment, which could be associated with a starter Item or Post or with a Thread, and expressed in ISO 8601 format."""
    later_version: NamedNode
    """Links to a later (newer) revision of this Item or Post."""
    latest_version: NamedNode
    """Links to the latest revision of this Item or Post."""
    likes: NamedNode
    """Used to indicate some form of endorsement by a UserAccount or Agent of an Item, Container, Space, UserAccount, etc."""
    link: NamedNode
    """A URI of a document which contains this SIOC object."""
    links_to: NamedNode
    """Links extracted from hyperlinks within a SIOC concept, e.g. Post or Site."""
    member_of: NamedNode
    """A Usergroup that this UserAccount is a member of."""
    mentions: NamedNode
    """Refers to a UserAccount that a particular Item mentions."""
    moderator_of: NamedNode
    """A Forum that a UserAccount is a moderator of."""
    modified_at: NamedNode
    """When this was modified, in ISO 8601 format."""
    modifier_of: NamedNode
    """A resource that this UserAccount has modified."""
    name: NamedNode
    """The name of a SIOC concept instance, e.g. a username for a UserAccount, group name for a Usergroup, etc."""
    next_by_date: NamedNode
    """Next Item or Post in a given Container sorted by date."""
    next_version: NamedNode
    """Links to the next revision of this Item or Post."""
    note: NamedNode
    """A note associated with this resource, for example, if it has been edited by a UserAccount."""
    num_authors: NamedNode
    """The number of unique authors (UserAccounts and unregistered posters) who have contributed to this Item, Thread, Post, etc."""
    num_items: NamedNode
    """The number of Posts (or Items) in a Forum (or a Container)."""
    num_replies: NamedNode
    """The number of replies that this Item, Thread, Post, etc. has. Useful for when the reply structure is absent."""
    num_threads: NamedNode
    """The number of Threads (AKA discussion topics) in a Forum."""
    num_views: NamedNode
    """The number of times this Item, Thread, UserAccount profile, etc. has been viewed."""
    owner_of: NamedNode
    """A resource owned by a particular UserAccount, for example, a weblog or image gallery."""
    parent_of: NamedNode
    """A child Container or Forum that this Container or Forum is a parent of."""
    part_of: NamedNode
    """A resource that the subject is a part of."""
    previous_by_date: NamedNode
    """Previous Item or Post in a given Container sorted by date."""
    previous_version: NamedNode
    """Links to the previous revision of this Item or Post."""
    read_at: NamedNode
    """When this was read, in ISO 8601 format."""
    reference: NamedNode
    """Links either created explicitly or extracted implicitly on the HTML level from the Post."""
    related_to: NamedNode
    """Related resources for this resource, e.g. for Posts, perhaps determined implicitly from topics or references."""
    reply_of: NamedNode
    """Links to an Item or Post which this Item or Post is a reply to."""
    respond_to: NamedNode
    """For the reply-to address set in email messages, IMs, etc. The property name was chosen to avoid confusion with has_reply/reply_of (the reply graph)."""
    scope_of: NamedNode
    """A Role that has a scope of this resource."""
    shared_by: NamedNode
    """For shared Items where there is a certain creator_of and an intermediary who shares or forwards it (e.g. as a sibling Item)."""
    sibling: NamedNode
    """An Item may have a sibling or a twin that exists in a different Container, but the siblings may differ in some small way (for example, language, category, etc.). The sibling of this Item should be self-describing (that is, it should contain all available information)."""
    space_of: NamedNode
    """A resource which belongs to this data Space."""
    subject: NamedNode
    """Keyword(s) describing subject of the Post."""
    subscriber_of: NamedNode
    """A Container that a UserAccount is subscribed to."""
    title: NamedNode
    """This is the title (subject line) of the Post. Note that for a Post within a threaded discussion that has no parents, it would detail the topic thread."""
    topic: NamedNode
    """A topic of interest, linking to the appropriate URI, e.g. in the Open Directory Project or of a SKOS category."""
    usergroup_of: NamedNode
    """A Space that the Usergroup has access to."""
