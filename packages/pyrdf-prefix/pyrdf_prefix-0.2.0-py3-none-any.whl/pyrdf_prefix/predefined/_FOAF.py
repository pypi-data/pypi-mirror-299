from pyoxigraph import NamedNode

from pyrdf_prefix.namespace import PredefinedNamespace


class FOAF(PredefinedNamespace):
    """Friend of a Friend: linking people and information using the Web"""

    # Conversion-Date: 2024-09-30T10:48+00:00
    # Source: http://xmlns.com/foaf/spec/index.rdf

    _nsBaseIri = "http://xmlns.com/foaf/0.1/"
    _issueWarning = True
    _withContainerMembershipProperty = False
    _nonPyIdentifiers = ()

    Agent: NamedNode
    """An agent (eg. person, group, software or physical artifact)."""
    Document: NamedNode
    """A document."""
    Group: NamedNode
    """A class of Agents."""
    Image: NamedNode
    """An image."""
    LabelProperty: NamedNode
    """A foaf:LabelProperty is any RDF property with texual values that serve as labels."""
    OnlineAccount: NamedNode
    """An online account."""
    OnlineChatAccount: NamedNode
    """An online chat account."""
    OnlineEcommerceAccount: NamedNode
    """An online e-commerce account."""
    OnlineGamingAccount: NamedNode
    """An online gaming account."""
    Organization: NamedNode
    """An organization."""
    Person: NamedNode
    """A person."""
    PersonalProfileDocument: NamedNode
    """A personal profile RDF document."""
    Project: NamedNode
    """A project (a collective endeavour of some kind)."""
    account: NamedNode
    """Indicates an account held by this agent."""
    accountName: NamedNode
    """Indicates the name (identifier) associated with this online account."""
    accountServiceHomepage: NamedNode
    """Indicates a homepage of the service provide for this online account."""
    age: NamedNode
    """The age in years of some agent."""
    aimChatID: NamedNode
    """An AIM chat ID"""
    based_near: NamedNode
    """A location that something is based near, for some broadly human notion of near."""
    birthday: NamedNode
    """The birthday of this Agent, represented in mm-dd string form, eg. '12-31'."""
    currentProject: NamedNode
    """A current project this person works on."""
    depiction: NamedNode
    """A depiction of some thing."""
    depicts: NamedNode
    """A thing depicted in this representation."""
    dnaChecksum: NamedNode
    """A checksum for the DNA of some thing. Joke."""
    familyName: NamedNode
    """The family name of some person."""
    family_name: NamedNode
    """The family name of some person."""
    firstName: NamedNode
    """The first name of a person."""
    focus: NamedNode
    """The underlying or 'focal' entity associated with some SKOS-described concept."""
    fundedBy: NamedNode
    """An organization funding a project or person."""
    geekcode: NamedNode
    """A textual geekcode for this person, see http://www.geekcode.com/geek.html"""
    gender: NamedNode
    """The gender of this Agent (typically but not necessarily 'male' or 'female')."""
    givenName: NamedNode
    """The given name of some person."""
    givenname: NamedNode
    """The given name of some person."""
    holdsAccount: NamedNode
    """Indicates an account held by this agent."""
    homepage: NamedNode
    """A homepage for some thing."""
    icqChatID: NamedNode
    """An ICQ chat ID"""
    img: NamedNode
    """An image that can be used to represent some thing (ie. those depictions which are particularly representative of something, eg. one's photo on a homepage)."""
    interest: NamedNode
    """A page about a topic of interest to this person."""
    isPrimaryTopicOf: NamedNode
    """A document that this thing is the primary topic of."""
    jabberID: NamedNode
    """A jabber ID for something."""
    knows: NamedNode
    """A person known by this person (indicating some level of reciprocated interaction between the parties)."""
    lastName: NamedNode
    """The last name of a person."""
    logo: NamedNode
    """A logo representing some thing."""
    made: NamedNode
    """Something that was made by this agent."""
    maker: NamedNode
    """An agent that 
made this thing."""
    mbox: NamedNode
    """A 
personal mailbox, ie. an Internet mailbox associated with exactly one owner, the first owner of this mailbox. This is a 'static inverse functional property', in that  there is (across time and change) at most one individual that ever has any particular value for foaf:mbox."""
    mbox_sha1sum: NamedNode
    """The sha1sum of the URI of an Internet mailbox associated with exactly one owner, the  first owner of the mailbox."""
    member: NamedNode
    """Indicates a member of a Group"""
    membershipClass: NamedNode
    """Indicates the class of individuals that are a member of a Group"""
    msnChatID: NamedNode
    """An MSN chat ID"""
    myersBriggs: NamedNode
    """A Myers Briggs (MBTI) personality classification."""
    name: NamedNode
    """A name for some thing."""
    nick: NamedNode
    """A short informal nickname characterising an agent (includes login identifiers, IRC and other chat nicknames)."""
    openid: NamedNode
    """An OpenID for an Agent."""
    page: NamedNode
    """A page or document about this thing."""
    pastProject: NamedNode
    """A project this person has previously worked on."""
    phone: NamedNode
    """A phone,  specified using fully qualified tel: URI scheme (refs: http://www.w3.org/Addressing/schemes.html#tel)."""
    plan: NamedNode
    """A .plan comment, in the tradition of finger and '.plan' files."""
    primaryTopic: NamedNode
    """The primary topic of some page or document."""
    publications: NamedNode
    """A link to the publications of this person."""
    schoolHomepage: NamedNode
    """A homepage of a school attended by the person."""
    sha1: NamedNode
    """A sha1sum hash, in hex."""
    skypeID: NamedNode
    """A Skype ID"""
    status: NamedNode
    """A string expressing what the user is happy for the general public (normally) to know about their current activity."""
    surname: NamedNode
    """The surname of some person."""
    theme: NamedNode
    """A theme."""
    thumbnail: NamedNode
    """A derived thumbnail image."""
    tipjar: NamedNode
    """A tipjar document for this agent, describing means for payment and reward."""
    title: NamedNode
    """Title (Mr, Mrs, Ms, Dr. etc)"""
    topic: NamedNode
    """A topic of some page or document."""
    topic_interest: NamedNode
    """A thing of interest to this person."""
    weblog: NamedNode
    """A weblog of some thing (whether person, group, company etc.)."""
    workInfoHomepage: NamedNode
    """A work info homepage of some person; a page about their work for some organization."""
    workplaceHomepage: NamedNode
    """A workplace homepage of some person; the homepage of an organization they work for."""
    yahooChatID: NamedNode
    """A Yahoo chat ID"""
