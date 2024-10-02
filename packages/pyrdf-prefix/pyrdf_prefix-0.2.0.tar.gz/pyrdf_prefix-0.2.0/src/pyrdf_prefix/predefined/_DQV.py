from pyoxigraph import NamedNode

from pyrdf_prefix.namespace import PredefinedNamespace


class DQV(PredefinedNamespace):
    """Data Quality Vocabulary"""

    # Conversion-Date: 2024-09-30T10:48+00:00
    # Source: https://www.w3.org/ns/dqv.ttl

    _nsBaseIri = "http://www.w3.org/ns/dqv#"
    _issueWarning = True
    _withContainerMembershipProperty = False
    _nonPyIdentifiers = ()

    Category: NamedNode
    """Represents a group of quality dimensions in which a common type of information is used as quality indicator."""
    Dimension: NamedNode
    """Represents criteria relevant for assessing quality. Each quality dimension must have one or more metric to measure it. A dimension is linked with a category using the dqv:inCategory property."""
    Metric: NamedNode
    """Represents a standard to measure a quality dimension. An observation (instance of dqv:QualityMeasurement) assigns a value in a given unit to a Metric."""
    QualityAnnotation: NamedNode
    """Represents quality annotations, including ratings, quality certificates or feedback that can be associated to datasets or distributions. Quality annotations must have one oa:motivatedBy statement with an instance of oa:Motivation (and skos:Concept) that reflects a quality assessment purpose. We define this instance as dqv:qualityAssessment."""
    QualityCertificate: NamedNode
    """An annotation that associates a resource (especially, a dataset or a distribution) to another resource (for example, a document) that certifies the resource's quality according to a set of quality assessment rules."""
    QualityMeasurement: NamedNode
    """Represents the evaluation of a given dataset (or dataset distribution) against a specific quality metric."""
    QualityMeasurementDataset: NamedNode
    """Represents a dataset of quality measurements, evaluations of one or more datasets (or dataset distributions) against specific quality metrics."""
    QualityMetadata: NamedNode
    """Represents quality metadata, it is defined to group quality certificates, policies, measurements and annotations under a named graph."""
    QualityPolicy: NamedNode
    """Represents a policy or agreement that is chiefly governed by data quality concerns."""
    UserQualityFeedback: NamedNode
    """Represents feedback that users have on the quality of datasets or distributions. Besides dqv:qualityAssessment, which is the motivation required by all quality annotations, one of the predefined instances of oa:Motivation should be indicated as motivation to distinguish among the different kinds of feedback, e.g., classifications, questions."""
    computedOn: NamedNode
    """Refers to the resource (e.g., a dataset, a linkset, a graph, a set of triples) on which the quality measurement is performed. In the DQV context, this property is generally expected to be used in statements in which objects are instances of dcat:Dataset or dcat:Distribution."""
    expectedDataType: NamedNode
    """Represents the expected data type for metric's observed value (e.g. xsd:boolean, xsd:double etc...)"""
    hasQualityAnnotation: NamedNode
    """Refers to a quality annotation. Quality annotation can be applied to any kind of resource, e.g., a dataset, a linkset, a graph, a set of triples. However, in the DQV context, this property is generally expected to be used in statements in which subjects are instances of dcat:Dataset or dcat:Distribution."""
    hasQualityMeasurement: NamedNode
    """Refers to the performed quality measurements. Quality measurements can be performed to any kind of resource (e.g., a dataset, a linkset, a graph, a set of triples). However, in the DQV context, this property is generally expected to be used in statements in which subjects are instances of dcat:Dataset or dcat:Distribution."""
    hasQualityMetadata: NamedNode
    """Refers to a grouping of quality information such as certificates, policies, measurements and annotations as a named graph. Quality information represented in such a grouping can pertain to any kind of resource (e.g., a dataset, a linkset, a graph, a set of triples). However, in the DQV context, this property is generally expected to be used in statements in which subjects are instances of dcat:Dataset or dcat:Distribution."""
    inCategory: NamedNode
    """Represents the category a dimension is grouped in."""
    inDimension: NamedNode
    """Represents the dimensions a quality metric, certificate and annotation allow a measurement of."""
    isMeasurementOf: NamedNode
    """Indicates the metric being observed."""
    precision: NamedNode
    """Precision is a quality dimension, which refers to the recorded level of details. It represents the exactness of a measurement or description. It is equivalent the notion of Precision from ISO 25012."""
    qualityAssessment: NamedNode
    """Motivation that must be specified for quality annotations."""
    value: NamedNode
    """Refers to values computed by metric."""
