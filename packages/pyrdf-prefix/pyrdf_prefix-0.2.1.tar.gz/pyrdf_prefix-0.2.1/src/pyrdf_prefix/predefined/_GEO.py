from pyoxigraph import NamedNode

from pyrdf_prefix.namespace import PredefinedNamespace


class GEO(PredefinedNamespace):
    """GeoSPARQL Ontology"""

    # Conversion-Date: 2024-09-30T10:48+00:00
    # Source: http://www.opengis.net/ont/geosparql#

    _nsBaseIri = "http://www.opengis.net/ont/geosparql#"
    _issueWarning = True
    _withContainerMembershipProperty = False
    _nonPyIdentifiers = ()

    Feature: NamedNode
    """A discrete spatial phenomenon in a universe of discourse."""
    FeatureCollection: NamedNode
    """A collection of individual Features."""
    Geometry: NamedNode
    """A coherent set of direct positions in space. The positions are held within a Spatial Reference System (SRS)."""
    GeometryCollection: NamedNode
    """A collection of individual Geometries."""
    SpatialObject: NamedNode
    """Anything spatial (being or having a shape, position or an extent)."""
    SpatialObjectCollection: NamedNode
    """A collection of individual Spatial Objects."""
    asDGGS: NamedNode
    """The Discrete Global Grid System (DGGS) serialization of a Geometry"""
    asGML: NamedNode
    """The GML serialization of a Geometry"""
    asGeoJSON: NamedNode
    """The GeoJSON serialization of a Geometry"""
    asKML: NamedNode
    """The KML serialization of a Geometry"""
    asWKT: NamedNode
    """The WKT serialization of a Geometry"""
    coordinateDimension: NamedNode
    """The number of measurements or axes needed to describe the position of this Geometry in a coordinate system."""
    defaultGeometry: NamedNode
    """The default Geometry to be used in spatial calculations. It is usually the most detailed Geometry."""
    dggsLiteral: NamedNode
    """A textual serialization of a Discrete Global Grid (DGGS) Geometry object."""
    dimension: NamedNode
    """The topological dimension of this geometric object, which must be less than or equal to the coordinate dimension. In non-homogeneous collections, this will return the largest topological dimension of the contained objects."""
    ehContains: NamedNode
    """States that the subject SpatialObject spatially contains the object SpatialObject. DE-9IM: T*TFF*FF*"""
    ehCoveredBy: NamedNode
    """States that the subject SpatialObject is spatially covered by the object SpatialObject. DE-9IM: TFF*TFT**"""
    ehCovers: NamedNode
    """States that the subject SpatialObject spatially covers the object SpatialObject. DE-9IM: T*TFT*FF*"""
    ehDisjoint: NamedNode
    """States that the subject SpatialObject is spatially disjoint from the object SpatialObject. DE-9IM: FF*FF****"""
    ehEquals: NamedNode
    """States that the subject SpatialObject spatially equals the object SpatialObject. DE-9IM: TFFFTFFFT"""
    ehInside: NamedNode
    """States that the subject SpatialObject is spatially inside the object SpatialObject. DE-9IM: TFF*FFT**"""
    ehMeet: NamedNode
    """States that the subject SpatialObject spatially meets the object SpatialObject. DE-9IM: FT******* ^ F**T***** ^ F***T****"""
    ehOverlap: NamedNode
    """States that the subject SpatialObject spatially overlaps the object SpatialObject. DE-9IM: T*T***T**"""
    geoJSONLiteral: NamedNode
    """A GeoJSON serialization of a Geometry object."""
    gmlLiteral: NamedNode
    """A GML serialization of a Geometry object."""
    hasArea: NamedNode
    """The area of a Spatial Object."""
    hasBoundingBox: NamedNode
    """The minimum or smallest bounding or enclosing box of a given Feature."""
    hasCentroid: NamedNode
    """The arithmetic mean position of all the Geometry points of a given Feature."""
    hasDefaultGeometry: NamedNode
    """The default Geometry to be used in spatial calculations. It is usually the most detailed Geometry."""
    hasGeometry: NamedNode
    """A spatial representation for a given Feature."""
    hasLength: NamedNode
    """The length of a Spatial Object."""
    hasMetricArea: NamedNode
    """The area of a Spatial Object in square meters."""
    hasMetricLength: NamedNode
    """The length of a Spatial Object in meters."""
    hasMetricPerimeterLength: NamedNode
    """The length of the perimeter of a Spatial Object in meters."""
    hasMetricSize: NamedNode
    """Subproperties of this property are used to indicate the size of a Spatial Object, as a measurement or estimate of one or more dimensions of the Spatial Object's spatial presence. Units are always metric (meter, square meter or cubic meter)."""
    hasMetricSpatialAccuracy: NamedNode
    """The positional accuracy of the coordinates of a Geometry in meters."""
    hasMetricSpatialResolution: NamedNode
    """The spatial resolution of a Geometry in meters."""
    hasMetricVolume: NamedNode
    """The volume of a Spatial Object in cubic meters."""
    hasPerimeterLength: NamedNode
    """The length of the perimeter of a Spatial Object."""
    hasSerialization: NamedNode
    """Connects a Geometry object with its text-based serialization."""
    hasSize: NamedNode
    """Subproperties of this property are used to indicate the size of a Spatial Object as a measurement or estimate of one or more dimensions of the Spatial Object's spatial presence."""
    hasSpatialAccuracy: NamedNode
    """The positional accuracy of the coordinates of a Geometry."""
    hasSpatialResolution: NamedNode
    """The spatial resolution of a Geometry."""
    hasVolume: NamedNode
    """The volume of a three-dimensional Spatial Object."""
    isEmpty: NamedNode
    """(true) if this geometric object is the empty Geometry. If true, then this geometric object represents the empty point set for the coordinate space."""
    isSimple: NamedNode
    """(true) if this geometric object has no anomalous geometric points, such as self intersection or self tangency."""
    kmlLiteral: NamedNode
    """A KML serialization of a Geometry object."""
    rcc8dc: NamedNode
    """States that the subject SpatialObject is spatially disjoint from the object SpatialObject. DE-9IM: FFTFFTTTT"""
    rcc8ec: NamedNode
    """States that the subject SpatialObject spatially meets the object SpatialObject. DE-9IM: FFTFTTTTT"""
    rcc8eq: NamedNode
    """States that the subject SpatialObject spatially equals the object SpatialObject. DE-9IM: TFFFTFFFT"""
    rcc8ntpp: NamedNode
    """States that the subject SpatialObject is spatially inside the object SpatialObject. DE-9IM: TFFTFFTTT"""
    rcc8ntppi: NamedNode
    """States that the subject SpatialObject spatially contains the object SpatialObject. DE-9IM: TTTFFTFFT"""
    rcc8po: NamedNode
    """States that the subject SpatialObject spatially overlaps the object SpatialObject. DE-9IM: TTTTTTTTT"""
    rcc8tpp: NamedNode
    """States that the subject SpatialObject is spatially covered by the object SpatialObject. DE-9IM: TFFTTFTTT"""
    rcc8tppi: NamedNode
    """States that the subject SpatialObject spatially covers the object SpatialObject. DE-9IM: TTTFTTFFT"""
    sfContains: NamedNode
    """States that the subject SpatialObject spatially contains the object SpatialObject. DE-9IM: T*****FF*"""
    sfCrosses: NamedNode
    """States that the subject SpatialObject spatially crosses the object SpatialObject. DE-9IM: T*T******"""
    sfDisjoint: NamedNode
    """States that the subject SpatialObject is spatially disjoint from the object SpatialObject. DE-9IM: FF*FF****"""
    sfEquals: NamedNode
    """States that the subject SpatialObject spatially equals the object SpatialObject. DE-9IM: TFFFTFFFT"""
    sfIntersects: NamedNode
    """States that the subject SpatialObject is not spatially disjoint from the object SpatialObject. DE-9IM: T******** ^ *T******* ^ ***T***** ^ ****T****"""
    sfOverlaps: NamedNode
    """States that the subject SpatialObject spatially overlaps the object SpatialObject. DE-9IM: T*T***T**"""
    sfTouches: NamedNode
    """States that the subject SpatialObject spatially touches the object SpatialObject. DE-9IM: FT******* ^ F**T***** ^ F***T****"""
    sfWithin: NamedNode
    """States that the subject SpatialObject is spatially within the object SpatialObject. DE-9IM: T*F**F***"""
    spatialDimension: NamedNode
    """The number of measurements or axes needed to describe the spatial position of this Geometry in a coordinate system."""
    wktLiteral: NamedNode
    """A Well-known Text serialization of a Geometry object."""
