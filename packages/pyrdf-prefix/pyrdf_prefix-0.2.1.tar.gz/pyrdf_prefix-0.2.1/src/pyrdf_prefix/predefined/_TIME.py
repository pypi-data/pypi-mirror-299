from pyoxigraph import NamedNode

from pyrdf_prefix.namespace import PredefinedNamespace


class TIME(PredefinedNamespace):
    """OWL-Time"""

    # Conversion-Date: 2024-09-30T10:48+00:00
    # Source: http://www.w3.org/2006/time#

    _nsBaseIri = "http://www.w3.org/2006/time#"
    _issueWarning = True
    _withContainerMembershipProperty = False
    _nonPyIdentifiers = ()

    DateTimeDescription: NamedNode
    """Description of date and time structured with separate values for the various elements of a calendar-clock system. The temporal reference system is fixed to Gregorian Calendar, and the range of year, month, day properties restricted to corresponding XML Schema types xsd:gYear, xsd:gMonth and xsd:gDay, respectively."""
    DateTimeInterval: NamedNode
    """DateTimeInterval is a subclass of ProperInterval, defined using the multi-element DateTimeDescription."""
    DayOfWeek: NamedNode
    """The day of week"""
    Duration: NamedNode
    """Duration of a temporal extent expressed as a number scaled by a temporal unit"""
    DurationDescription: NamedNode
    """Description of temporal extent structured with separate values for the various elements of a calendar-clock system. The temporal reference system is fixed to Gregorian Calendar, and the range of each of the numeric properties is restricted to xsd:decimal"""
    GeneralDateTimeDescription: NamedNode
    """Descripción de fecha y hora estructurada con valores separados para los distintos elementos de un sistema calendario-reloj."""
    GeneralDurationDescription: NamedNode
    """Description of temporal extent structured with separate values for the various elements of a calendar-clock system."""
    Instant: NamedNode
    """A temporal entity with zero extent or duration"""
    Interval: NamedNode
    """A temporal entity with an extent or duration"""
    MonthOfYear: NamedNode
    """The month of the year"""
    ProperInterval: NamedNode
    """A temporal entity with non-zero extent or duration, i.e. for which the value of the beginning and end are different"""
    TRS: NamedNode
    """A temporal reference system, such as a temporal coordinate system (with an origin, direction, and scale), a calendar-clock combination, or a (possibly hierarchical) ordinal system. 

This is a stub class, representing the set of all temporal reference systems."""
    TemporalDuration: NamedNode
    """Time extent; duration of a time interval separate from its particular start position"""
    TemporalEntity: NamedNode
    """A temporal interval or instant."""
    TemporalPosition: NamedNode
    """A position on a time-line"""
    TemporalUnit: NamedNode
    """A standard duration, which provides a scale factor for a time extent, or the granularity or precision for a time position."""
    TimePosition: NamedNode
    """A temporal position described using either a (nominal) value from an ordinal reference system, or a (numeric) value in a temporal coordinate system. """
    TimeZone: NamedNode
    """A Time Zone specifies the amount by which the local time is offset from UTC. 
	A time zone is usually denoted geographically (e.g. Australian Eastern Daylight Time), with a constant value in a given region. 
The region where it applies and the offset from UTC are specified by a locally recognised governing authority."""
    Year: NamedNode
    """Year duration"""
    after: NamedNode
    """Gives directionality to time. If a temporal entity T1 is after another temporal entity T2, then the beginning of T1 is after the end of T2."""
    before: NamedNode
    """Gives directionality to time. If a temporal entity T1 is before another temporal entity T2, then the end of T1 is before the beginning of T2. Thus, "before" can be considered to be basic to instants and derived for intervals."""
    day: NamedNode
    """Day position in a calendar-clock system.

The range of this property is not specified, so can be replaced by any specific representation of a calendar day from any calendar. """
    dayOfWeek: NamedNode
    """The day of week, whose value is a member of the class time:DayOfWeek"""
    dayOfYear: NamedNode
    """The number of the day within the year"""
    days: NamedNode
    """length of, or element of the length of, a temporal extent expressed in days"""
    generalDay: NamedNode
    """Day of month - formulated as a text string with a pattern constraint to reproduce the same lexical form as gDay, except that values up to 99 are permitted, in order to support calendars with more than 31 days in a month. 
Note that the value-space is not defined, so a generic OWL2 processor cannot compute ordering relationships of values of this type."""
    generalMonth: NamedNode
    """Month of year - formulated as a text string with a pattern constraint to reproduce the same lexical form as gMonth, except that values up to 20 are permitted, in order to support calendars with more than 12 months in the year. 
Note that the value-space is not defined, so a generic OWL2 processor cannot compute ordering relationships of values of this type."""
    generalYear: NamedNode
    """Year number - formulated as a text string with a pattern constraint to reproduce the same lexical form as gYear, but not restricted to values from the Gregorian calendar. 
Note that the value-space is not defined, so a generic OWL2 processor cannot compute ordering relationships of values of this type."""
    hasBeginning: NamedNode
    """Beginning of a temporal entity."""
    hasDateTimeDescription: NamedNode
    """Value of DateTimeInterval expressed as a structured value. The beginning and end of the interval coincide with the limits of the shortest element in the description."""
    hasDuration: NamedNode
    """Duration of a temporal entity, event or activity, or thing, expressed as a scaled value"""
    hasDurationDescription: NamedNode
    """Duration of a temporal entity, expressed using a structured description"""
    hasEnd: NamedNode
    """End of a temporal entity."""
    hasTRS: NamedNode
    """The temporal reference system used by a temporal position or extent description. """
    hasTemporalDuration: NamedNode
    """Duration of a temporal entity."""
    hasTime: NamedNode
    """Supports the association of a temporal entity (instant or interval) to any thing"""
    hasXSDDuration: NamedNode
    """Extent of a temporal entity, expressed using xsd:duration"""
    hour: NamedNode
    """Hour position in a calendar-clock system."""
    hours: NamedNode
    """length of, or element of the length of, a temporal extent expressed in hours"""
    inDateTime: NamedNode
    """Position of an instant, expressed using a structured description"""
    inTemporalPosition: NamedNode
    """Position of a time instant"""
    inTimePosition: NamedNode
    """Position of a time instant expressed as a TimePosition"""
    inXSDDate: NamedNode
    """Position of an instant, expressed using xsd:date"""
    inXSDDateTime: NamedNode
    """Position of an instant, expressed using xsd:dateTime"""
    inXSDDateTimeStamp: NamedNode
    """Position of an instant, expressed using xsd:dateTimeStamp"""
    inXSDgYear: NamedNode
    """Position of an instant, expressed using xsd:gYear"""
    inXSDgYearMonth: NamedNode
    """Position of an instant, expressed using xsd:gYearMonth"""
    inside: NamedNode
    """An instant that falls inside the interval. It is not intended to include beginnings and ends of intervals."""
    intervalAfter: NamedNode
    """If a proper interval T1 is intervalAfter another proper interval T2, then the beginning of T1 is after the end of T2."""
    intervalBefore: NamedNode
    """If a proper interval T1 is intervalBefore another proper interval T2, then the end of T1 is before the beginning of T2."""
    intervalContains: NamedNode
    """If a proper interval T1 is intervalContains another proper interval T2, then the beginning of T1 is before the beginning of T2, and the end of T1 is after the end of T2."""
    intervalDisjoint: NamedNode
    """If a proper interval T1 is intervalDisjoint another proper interval T2, then the beginning of T1 is after the end of T2, or the end of T1 is before the beginning of T2, i.e. the intervals do not overlap in any way, but their ordering relationship is not known."""
    intervalDuring: NamedNode
    """If a proper interval T1 is intervalDuring another proper interval T2, then the beginning of T1 is after the beginning of T2, and the end of T1 is before the end of T2."""
    intervalEquals: NamedNode
    """If a proper interval T1 is intervalEquals another proper interval T2, then the beginning of T1 is coincident with the beginning of T2, and the end of T1 is coincident with the end of T2."""
    intervalFinishedBy: NamedNode
    """If a proper interval T1 is intervalFinishedBy another proper interval T2, then the beginning of T1 is before the beginning of T2, and the end of T1 is coincident with the end of T2."""
    intervalFinishes: NamedNode
    """If a proper interval T1 is intervalFinishes another proper interval T2, then the beginning of T1 is after the beginning of T2, and the end of T1 is coincident with the end of T2."""
    intervalIn: NamedNode
    """If a proper interval T1 is intervalIn another proper interval T2, then the beginning of T1 is after the beginning of T2 or is coincident with the beginning of T2, and the end of T1 is before the end of T2, or is coincident with the end of T2, except that end of T1 may not be coincident with the end of T2 if the beginning of T1 is coincident with the beginning of T2."""
    intervalMeets: NamedNode
    """If a proper interval T1 is intervalMeets another proper interval T2, then the end of T1 is coincident with the beginning of T2."""
    intervalMetBy: NamedNode
    """If a proper interval T1 is intervalMetBy another proper interval T2, then the beginning of T1 is coincident with the end of T2."""
    intervalOverlappedBy: NamedNode
    """If a proper interval T1 is intervalOverlappedBy another proper interval T2, then the beginning of T1 is after the beginning of T2, the beginning of T1 is before the end of T2, and the end of T1 is after the end of T2."""
    intervalOverlaps: NamedNode
    """If a proper interval T1 is intervalOverlaps another proper interval T2, then the beginning of T1 is before the beginning of T2, the end of T1 is after the beginning of T2, and the end of T1 is before the end of T2."""
    intervalStartedBy: NamedNode
    """If a proper interval T1 is intervalStarted another proper interval T2, then the beginning of T1 is coincident with the beginning of T2, and the end of T1 is after the end of T2."""
    intervalStarts: NamedNode
    """If a proper interval T1 is intervalStarts another proper interval T2, then the beginning of T1 is coincident with the beginning of T2, and the end of T1 is before the end of T2."""
    minute: NamedNode
    """Minute position in a calendar-clock system."""
    minutes: NamedNode
    """length, or element of, a temporal extent expressed in minutes"""
    month: NamedNode
    """Month position in a calendar-clock system.

The range of this property is not specified, so can be replaced by any specific representation of a calendar month from any calendar. """
    monthOfYear: NamedNode
    """The month of the year, whose value is a member of the class time:MonthOfYear"""
    months: NamedNode
    """length of, or element of the length of, a temporal extent expressed in months"""
    nominalPosition: NamedNode
    """The (nominal) value indicating temporal position in an ordinal reference system """
    numericDuration: NamedNode
    """Value of a temporal extent expressed as a decimal number scaled by a temporal unit"""
    numericPosition: NamedNode
    """The (numeric) value indicating position within a temporal coordinate system """
    second: NamedNode
    """Second position in a calendar-clock system."""
    seconds: NamedNode
    """length of, or element of the length of, a temporal extent expressed in seconds"""
    timeZone: NamedNode
    """The time zone for clock elements in the temporal position"""
    unitType: NamedNode
    """The temporal unit which provides the precision of a date-time value or scale of a temporal extent"""
    week: NamedNode
    """Week number within the year."""
    weeks: NamedNode
    """length of, or element of the length of, a temporal extent expressed in weeks"""
    xsdDateTime: NamedNode
    """Value of DateTimeInterval expressed as a compact value."""
    year: NamedNode
    """Year position in a calendar-clock system.

The range of this property is not specified, so can be replaced by any specific representation of a calendar year from any calendar. """
    years: NamedNode
    """length of, or element of the length of, a temporal extent expressed in years"""
