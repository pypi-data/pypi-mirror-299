from pyoxigraph import NamedNode

from pyrdf_prefix.namespace import PredefinedNamespace


class MA(PredefinedNamespace):
    """Ontology for Media Resources 1.0"""

    # Conversion-Date: 2024-09-30T10:48+00:00
    # Source: https://www.w3.org/ns/ma-ont.ttl

    _nsBaseIri = "http://www.w3.org/ns/ma-ont#"
    _issueWarning = True
    _withContainerMembershipProperty = False
    _nonPyIdentifiers = ()

    Agent: NamedNode
    """A person or organisation contributing to the media resource."""
    AudioTrack: NamedNode
    """A specialisation of Track for Audio to provide a link to specific data properties such as sampleRate, etc. Specialisation is defined through object properties."""
    Collection: NamedNode
    """Any group of media resource e.g. a series."""
    DataTrack: NamedNode
    """Ancillary data track e.g. captioning  in addition to video and audio tracks. Specialisation is made through the use of appropriate object properties."""
    Image: NamedNode
    """A still image / thumbnail / key frame related to the media resource or being the media resource itself."""
    Location: NamedNode
    """A location related to the media resource, e.g. depicted in the resource (possibly fictional) or where the resource was created (shooting location), etc."""
    MediaFragment: NamedNode
    """A media fragment (spatial, temporal, track...) composing a media resource. In other ontologies fragment is sometimes referred to as a 'part' or 'segment'."""
    MediaResource: NamedNode
    """An image or an audiovisual media resource, which can be composed of one or more fragment / track."""
    Organisation: NamedNode
    """An organisation or moral agent."""
    Person: NamedNode
    """A physical person."""
    Rating: NamedNode
    """Information about the rating given to a media resource."""
    TargetAudience: NamedNode
    """Information about The target audience (target region, target audience category but also parental guidance recommendation) for which a media resource is intended."""
    Track: NamedNode
    """A specialisation of MediaFragment for audiovisual content."""
    VideoTrack: NamedNode
    """A specialisation of Track for Video to provide a link to specific data properties such as frameRate, etc. Signing is another possible example of video track. Specialisation is defined through object properties."""
    alternativeTitle: NamedNode
    """Corresponds to 'title.title' in the Ontology for Media Resources with a 'title.type' meaning "alternative"."""
    averageBitRate: NamedNode
    """Corresponds to 'averageBitRate' in the Ontology for Media Resources, expressed in kilobits/second."""
    collectionName: NamedNode
    """The name by which a collection (e.g. series) is known."""
    copyright: NamedNode
    """Corresponds to 'copyright.copyright' in the Ontology for Media Resources."""
    createdIn: NamedNode
    """A subproperty of 'hasRelatedLocation" used to specify where material shooting took place."""
    creationDate: NamedNode
    """Corresponds to 'date.date' in the Ontology for Media Resources with a 'date.type' meaning "creationDate"."""
    date: NamedNode
    """Corresponds to date.date in the ontology for Media Resources. Subproperties can be used to distinguish different values of 'date.type'. The recommended range is 'xsd:dateTime' (for compliance with OWL2-QL and OWL2-RL) but other time-related datatypes may be used (e.g. 'xsd:gYear', 'xsd:date'...)."""
    depictsFictionalLocation: NamedNode
    """A subproperty of 'hasRelatedLocation' used to specify where the action depicted in the media is supposed to take place, as opposed to the location where shooting actually took place (see 'createdIn')."""
    description: NamedNode
    """Corresponds to 'description' in the Ontology for Media Resources. This can be specialised by using sub-properties e.g. 'summary' or 'script'."""
    duration: NamedNode
    """Corresponds to 'duration' in the Ontology for Media Resources."""
    editDate: NamedNode
    """Corresponds to 'date.date' in the Ontology for Media Resources with a 'date.type' meaning "editDate"."""
    features: NamedNode
    """Corresponds to 'contributor.contributor' in the Ontology for Media Resources with a 'contributor.role' meaning "actor"."""
    fragmentName: NamedNode
    """Corresponds to 'namedFragment.label' in the Ontology for Media Resources."""
    frameHeight: NamedNode
    """Corresponds to 'frameSize.height' in the Ontology for Media Resources, measured in frameSizeUnit."""
    frameRate: NamedNode
    """Corresponds to 'frameRate' in the Ontology for Media Resources, in frame per second."""
    frameSizeUnit: NamedNode
    """Corresponds to 'frameSize.unit' in the Ontology for Media Resources."""
    frameWidth: NamedNode
    """Corresponds to 'frameSize.width' in the Ontology for Media Resources measured in frameSizeUnit."""
    hasAccessConditions: NamedNode
    """Corresponds to 'policy' in the Ontology for Media Resources with a 'policy.type' "access conditions"."""
    hasAudioDescription: NamedNode
    """Corresponds to 'fragment' in the Ontology for Media Resources with a 'fragment.role' meaning "audio-description"."""
    hasCaptioning: NamedNode
    """Corresponds to 'fragment' in the Ontology for Media Resources with a 'fragment.role' meaning "captioning". This property can for example point to a spatial fragment, a VideoTrack or a DataTrack. The language of the captioning track can be expressed by attaching a 'hasLanguage' property to the specific track."""
    hasChapter: NamedNode
    """Corresponds to 'fragment' in the Ontology for Media Resources with a 'fragment.role' meaning "chapter"."""
    hasClassification: NamedNode
    """Corresponds to 'targetAudience.classification' in the Ontology for Media Resources. This property is used to provide a value characterising the target audience."""
    hasClassificationSystem: NamedNode
    """Corresponds to 'targetAudience.identifier' in the Ontology for Media Resources. This is used to identify the reference sheme against which the target audience has been characterised."""
    hasCompression: NamedNode
    """Corresponds to 'compression' in the Ontology for Media Resources."""
    hasContributor: NamedNode
    """Corresponds to 'contributor.contributor' in the Ontology for Media Resources. Subproperties can be used to distinguish different values of 'contributor.role'."""
    hasCreator: NamedNode
    """Corresponds to 'creator.creator' in the Ontology for Media Resources. Subproperties can be used to distinguish different values of 'creator.role'. Note that this property is semantically a subproperty of 'hasContributor'."""
    hasFormat: NamedNode
    """Corresponds to 'format' in the Ontology for Media Resources."""
    hasFragment: NamedNode
    """Corresponds to 'fragment' in the Ontology for Media Resources. Subproperties can be used to distinguish different values of 'fragment.role'."""
    hasGenre: NamedNode
    """Corresponds to 'genre' in the Ontology for Media Resources."""
    hasKeyword: NamedNode
    """Corresponds to 'keyword' in the Ontology for Media Resources."""
    hasLanguage: NamedNode
    """Corresponds to 'language' in the Ontology for Media Resources. The language used in the resource. A controlled vocabulary such as defined in BCP 47 SHOULD be used. This property can also be used to identify the presence of sign language (RFC 5646). By inheritance, the hasLanguage property applies indifferently at the media resource / fragment / track levels.  Best practice recommends to use to best possible level of granularity fo describe the usage of language within a media resource including at fragment and track levels."""
    hasLocationCoordinateSystem: NamedNode
    """Corresponds to 'location.coordinateSystem' in the Ontology for Media Resources."""
    hasNamedFragment: NamedNode
    """Corresponds to 'namedFragment' in the Ontology for Media Resources."""
    hasPermissions: NamedNode
    """Corresponds to 'policy' in the Ontology for Media Resources with a  'policy.type' meaning "permissions"."""
    hasPolicy: NamedNode
    """Corresponds to 'policy' in the Ontology for Media Resources. Subproperties can be used to distinguish different values of 'policy.type'."""
    hasPublisher: NamedNode
    """Corresponds to 'publisher' in the Ontology for Media Resources."""
    hasRating: NamedNode
    """Corresponds to 'rating' in the Ontology for Media Resources."""
    hasRatingSystem: NamedNode
    """Corresponds to 'rating.type' in the Ontology for Media Resources."""
    hasRelatedImage: NamedNode
    """Corresponds to 'relation' and in the Ontology for Media Resources with a 'relation.type' meaning "related image"."""
    hasRelatedLocation: NamedNode
    """Corresponds to 'location' in the Ontology for Media Resources. Subproperties are provided to specify, when possible, the relation between the media resource and the location."""
    hasRelatedResource: NamedNode
    """Corresponds to 'relation' and in the Ontology for Media Resources. Subproperties can be used to distinguish different values of 'relation.type'."""
    hasSigning: NamedNode
    """Corresponds to 'fragment' in the Ontology for Media Resources with a 'fragment.role' meaning "signing". This property can for example point to a spatial fragment or a VideoTrack. The sign language of the captioning track can be expressed by attaching a 'hasLanguage' property to the specific track."""
    hasSource: NamedNode
    """Corresponds to 'relation' and in the Ontology for Media Resources with a 'relation.type' meaning "source"."""
    hasSubtitling: NamedNode
    """Corresponds to 'fragment' in the Ontology for Media Resources with a 'fragment.role' meaning "subtitling"."""
    hasTargetAudience: NamedNode
    """Corresponds to 'targetAudience' in the Ontology for Media Resources."""
    hasTrack: NamedNode
    """Corresponds to 'fragment' in the Ontology for Media Resources with a 'fragment.role' meaning "track"."""
    isCopyrightedBy: NamedNode
    """Corresponds to 'copyright.identifier' in the Ontology for Media Resources."""
    isMemberOf: NamedNode
    """Corresponds to 'collection' in the Ontology for Media Resources."""
    isProvidedBy: NamedNode
    """Corresponds to 'rating.identifier' in the Ontology for Media Resources."""
    locationAltitude: NamedNode
    """Corresponds to 'location.altitude' in the Ontology for Media Resources."""
    locationLatitude: NamedNode
    """Corresponds to 'location.latitude' in the Ontology for Media Resources."""
    locationLongitude: NamedNode
    """Corresponds to 'location.longitude' in the Ontology for Media Resources."""
    locationName: NamedNode
    """Corresponds to 'location.name' in the Ontology for Media Resources."""
    locator: NamedNode
    """Corresponds to 'locator' in the Ontology for Media Resources."""
    mainOriginalTitle: NamedNode
    """Corresponds to 'title.title' in the Ontology for Media Resources with a 'title.type' meaning "original"."""
    numberOfTracks: NamedNode
    """Corresponds to 'numTracks.number' in the Ontology for Media Resources. Subproperties can be used to distinguish different values of 'numTracks.type'."""
    ratingScaleMax: NamedNode
    """Corresponds to 'rating.max' in the Ontology for Media Resources."""
    ratingScaleMin: NamedNode
    """Corresponds to 'rating.min' in the Ontology for Media Resources."""
    ratingValue: NamedNode
    """Corresponds to 'rating.value' in the Ontology for Media Resources."""
    recordDate: NamedNode
    """Corresponds to 'date.date' in the Ontology for Media Resources with a 'date.type' meaning "recordDate"."""
    releaseDate: NamedNode
    """Corresponds to 'date.date' in the Ontology for Media Resources with a 'date.type' meaning "releaseDate"."""
    samplingRate: NamedNode
    """Corresponds to 'samplingRate' in the Ontology for Media Resources, in samples per second."""
    title: NamedNode
    """Corresponds to 'title.title' in the Ontology for Media Resources. Subproperties can be used to distinguish different values of 'title.type'."""
    trackName: NamedNode
    """Corresponds to 'fragment.name' in the Ontology for Media Resources, for Track fragments."""
