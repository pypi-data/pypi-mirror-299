from pyoxigraph import NamedNode

from pyrdf_prefix.namespace import PredefinedNamespace


class CSVW(PredefinedNamespace):
    """CSV on the Web"""

    # Conversion-Date: 2024-09-30T10:48+00:00
    # Source: https://www.w3.org/ns/csvw.ttl

    _nsBaseIri = "http://www.w3.org/ns/csvw#"
    _issueWarning = True
    _withContainerMembershipProperty = False
    _nonPyIdentifiers = ()

    Cell: NamedNode
    """A Cell represents a cell at the intersection of a Row and a Column within a Table."""
    Column: NamedNode
    """A Column represents a vertical arrangement of Cells within a Table."""
    Datatype: NamedNode
    """Describes facets of a datatype."""
    Dialect: NamedNode
    """A Dialect Description provides hints to parsers about how to parse a linked file."""
    Direction: NamedNode
    """The class of table/text directions."""
    ForeignKey: NamedNode
    """Describes relationships between Columns in one or more Tables."""
    JSON: NamedNode
    """A literal containing JSON."""
    NumericFormat: NamedNode
    """If the datatype is a numeric type, the format property indicates the expected format for that number. Its value must be either a single string or an object with one or more properties."""
    Row: NamedNode
    """A Row represents a horizontal arrangement of cells within a Table."""
    Schema: NamedNode
    """A Schema is a definition of a tabular format that may be common to multiple tables."""
    Table: NamedNode
    """An annotated table is a table that is annotated with additional metadata."""
    TableGroup: NamedNode
    """A Group of Tables comprises a set of Annotated Tables and a set of annotations that relate to those Tables."""
    TableReference: NamedNode
    """An object property that identifies a referenced table and a set of referenced columns within that table."""
    Transformation: NamedNode
    """A Transformation Definition is a definition of how tabular data can be transformed into another format."""
    aboutUrl: NamedNode
    """A URI template property that MAY be used to indicate what a cell contains information about."""
    auto: NamedNode
    """Indicates whether the tables in the group should be displayed based on the first character in the table that has a specific direction."""
    base: NamedNode
    """An atomic property that contains a single string: a term defined in the default context representing a built-in datatype URL, as listed above."""
    column: NamedNode
    """An array property of column descriptions as described in section 5.6 Columns."""
    columnReference: NamedNode
    """A column reference property that holds either a single reference to a column description object within this schema, or an array of references. These form the referencing columns for the foreign key definition."""
    commentPrefix: NamedNode
    """An atomic property that sets the comment prefix flag to the single provided value, which MUST be a string."""
    csvEncodedTabularData: NamedNode
    """Describes the role of a CSV file in the tabular data mapping."""
    datatype: NamedNode
    """An object property that contains either a single string that is the main datatype of the values of the cell or a datatype description object. If the value of this property is a string, it MUST be one of the built-in datatypes defined in section 5.11.1 Built-in Datatypes or an absolute URL; if it is an object then it describes a more specialised datatype."""
    decimalChar: NamedNode
    """A string whose value is used to represent a decimal point within the number."""
    default: NamedNode
    """An atomic property holding a single string that is used to create a default value for the cell in cases where the original string value is an empty string."""
    delimiter: NamedNode
    """An atomic property that sets the delimiter flag to the single provided value, which MUST be a string."""
    describes: NamedNode
    """From IANA describes: The relationship A 'describes' B asserts that resource A provides a description of resource B. There are no constraints on the format or representation of either A or B, neither are there any further constraints on either resource."""
    dialect: NamedNode
    """An object property that provides a single dialect description. If provided, dialect provides hints to processors about how to parse the referenced files to create tabular data models for the tables in the group."""
    doubleQuote: NamedNode
    """A boolean atomic property that, if `true`, sets the escape character flag to `"`."""
    encoding: NamedNode
    """An atomic property that sets the encoding flag to the single provided string value, which MUST be a defined in [[encoding]]. The default is "utf-8"."""
    foreignKey: NamedNode
    """For a Table: a list of foreign keys on the table.

For a Schema: an array property of foreign key definitions that define how the values from specified columns within this table link to rows within this table or other tables."""
    format: NamedNode
    """An atomic property that contains either a single string or an object that defines the format of a value of this type, used when parsing a string value as described in Parsing Cells in [[tabular-data-model]]."""
    groupChar: NamedNode
    """A string whose value is used to group digits within the number."""
    header: NamedNode
    """A boolean atomic property that, if `true`, sets the header row count flag to `1`, and if `false` to `0`, unless headerRowCount is provided, in which case the value provided for the header property is ignored."""
    headerRowCount: NamedNode
    """An numeric atomic property that sets the header row count flag to the single provided value, which must be a non-negative integer."""
    inherit: NamedNode
    """For `textDirection`, indicates that the direction is inherited from the `tableDirection` annotation of the `table`."""
    lang: NamedNode
    """An atomic property giving a single string language code as defined by [[BCP47]]."""
    length: NamedNode
    """The exact length of the value of the cell."""
    lineTerminators: NamedNode
    """An atomic property that sets the line terminators flag to either an array containing the single provided string value, or the provided array."""
    ltr: NamedNode
    """Indicates whether the tables in the group should be displayed with the first column on the right."""
    maxExclusive: NamedNode
    """An atomic property that contains a single number that is the maximum valid value (exclusive)."""
    maxInclusive: NamedNode
    """An atomic property that contains a single number that is the maximum valid value (inclusive)."""
    maxLength: NamedNode
    """A numeric atomic property that contains a single integer that is the maximum length of the value."""
    minExclusive: NamedNode
    """An atomic property that contains a single number that is the minimum valid value (exclusive)."""
    minInclusive: NamedNode
    """An atomic property that contains a single number that is the minimum valid value (inclusive)."""
    minLength: NamedNode
    """An atomic property that contains a single integer that is the minimum length of the value."""
    name: NamedNode
    """An atomic property that gives a single canonical name for the column. The value of this property becomes the name annotation for the described column."""
    note: NamedNode
    """An array property that provides an array of objects representing arbitrary annotations on the annotated tabular data model."""
    null: NamedNode
    """An atomic property giving the string or strings used for null values within the data. If the string value of the cell is equal to any one of these values, the cell value is `null`."""
    ordered: NamedNode
    """A boolean atomic property taking a single value which indicates whether a list that is the value of the cell is ordered (if `true`) or unordered (if `false`)."""
    pattern: NamedNode
    """A regular expression string, in the syntax and interpreted as defined by [[ECMASCRIPT]]."""
    primaryKey: NamedNode
    """For Schema: A column reference property that holds either a single reference to a column description object or an array of references.

For Row: a possibly empty list of cells whose values together provide a unique identifier for this row. This is similar to the name of a column."""
    propertyUrl: NamedNode
    """An URI template property that MAY be used to create a URI for a property if the table is mapped to another format. """
    quoteChar: NamedNode
    """An atomic property that sets the quote character flag to the single provided value, which must be a string or `null`."""
    reference: NamedNode
    """An object property that identifies a **referenced table** and a set of **referenced columns** within that table."""
    referencedRow: NamedNode
    """A possibly empty list of pairs of a foreign key and a row in a table within the same group of tables."""
    required: NamedNode
    """A boolean atomic property taking a single value which indicates whether the cell must have a non-null value. The default is `false`. """
    resource: NamedNode
    """A link property holding a URL that is the identifier for a specific table that is being referenced."""
    row: NamedNode
    """Relates a Table to each Row output."""
    rowTitle: NamedNode
    """A column reference property that holds either a single reference to a column description object or an array of references."""
    rownum: NamedNode
    """The position of the row amongst the rows of the Annotated Tabl, starting from 1"""
    rtl: NamedNode
    """Indicates whether the tables in the group should be displayed with the first column on the left."""
    schemaReference: NamedNode
    """A link property holding a URL that is the identifier for a schema that is being referenced."""
    scriptFormat: NamedNode
    """A link property giving the single URL for the format that is used by the script or template."""
    separator: NamedNode
    """An atomic property that MUST have a single string value that is the character used to separate items in the string value of the cell."""
    skipBlankRows: NamedNode
    """An boolean atomic property that sets the `skip blank rows` flag to the single provided boolean value."""
    skipColumns: NamedNode
    """An numeric atomic property that sets the `skip columns` flag to the single provided numeric value, which MUST be a non-negative integer."""
    skipInitialSpace: NamedNode
    """A boolean atomic property that, if `true`, sets the trim flag to "start". If `false`, to `false`."""
    skipRows: NamedNode
    """An numeric atomic property that sets the `skip rows` flag to the single provided numeric value, which MUST be a non-negative integer."""
    source: NamedNode
    """A single string atomic property that provides, if specified, the format to which the tabular data should be transformed prior to the transformation using the script or template."""
    suppressOutput: NamedNode
    """A boolean atomic property. If `true`, suppresses any output that would be generated when converting a table or cells within a column."""
    table: NamedNode
    """Relates an Table group to annotated tables."""
    tableDirection: NamedNode
    """One of `rtl`, `ltr` or `auto`. Indicates whether the tables in the group should be displayed with the first column on the right, on the left, or based on the first character in the table that has a specific direction."""
    tableSchema: NamedNode
    """An object property that provides a single schema description as described in section 5.5 Schemas, used as the default for all the tables in the group"""
    tabularMetadata: NamedNode
    """Describes the role of a Metadata file in the tabular data mapping."""
    targetFormat: NamedNode
    """A link property giving the single URL for the format that will be created through the transformation."""
    textDirection: NamedNode
    """An atomic property that must have a single value that is one of `rtl` or `ltr` (the default)."""
    title: NamedNode
    """For a Transformation A natural language property that describes the format that will be generated from the transformation.

For a Column: A natural language property that provides possible alternative names for the column."""
    transformations: NamedNode
    """An array property of transformation definitions that provide mechanisms to transform the tabular data into other formats."""
    trim: NamedNode
    """An atomic property that, if the boolean `true`, sets the trim flag to `true` and if the boolean `false` to `false`. If the value provided is a string, sets the trim flag to the provided value, which must be one of "true", "false", "start" or "end"."""
    uriTemplate: NamedNode
    """"""
    url: NamedNode
    """For a Table: This link property gives the single URL of the CSV file that the table is held in, relative to the location of the metadata document.

For a Transformation: A link property giving the single URL of the file that the script or template is held in, relative to the location of the metadata document."""
    valueUrl: NamedNode
    """An URI template property that is used to map the values of cells into URLs."""
    virtual: NamedNode
    """A boolean atomic property taking a single value which indicates whether the column is a virtual column not present in the original source"""
