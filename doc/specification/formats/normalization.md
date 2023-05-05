# 2.4.4 Normalization

To be able to sign a [component version](../../specification/elements/README.md#component-versions), the metadata of a component version and the
content of described artifacts must be incorporated.

The metadata of a component version is described by a [component-descriptor](../../specification/elements/README.md#component-descriptor). It contains volatile information, also, e.g. the artifact access specification, which might change during [transports](../../introduction/transports.md).
Therefore, to calculate a digest, the component descriptor has to be transformed
to an immutable technical reprsentation containing only signature relevant information. This process is called [*component descriptor normalization*](componentdescriptor_normalization.md).

To cover the content of the artifacts described by a component version, a digest
for the artifact content has to be calculated, also, and incorporated into the
immutable information of the component descriptor.

By default, this digest is calculated based on the blob provided by the
[access method](../elements/README.md#artifact-access)
of an artifact. But there might be technology specific ways to uniquely identify
the content for dedicated artifact types, which might depend on the chosen blob media type.

Therefore, together with the digest and its algorithm, an artifact normalization
algorithm is kept in the [component descriptor](../elements/README.md#component-descriptor).
This process is called [*artifact blob normalization]*(artifact_normalization.md)

