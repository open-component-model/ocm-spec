# 2.4.4 Normalization

To be able to sign a [component version](../../specification/elements/README.md#component-versions), the metadata of a component version and the
content of described artefacts must be incorporated.

The metadata of a component version is described by a [component-descriptor](../../specification/elements/README.md#component-descriptor). It contains volatile information, also, e.g. the artefact access specification, which might change during [transports](../../introduction/transports.md).
Therefore, to calculate a digest, the component descriptor has to be transformed
to an immutable technical reprsentation containing only signature relevant information. THis process is called [*component descriptor normalization*](componentdescriptor_normalization.md).

To cover the content of the artefacts described by a component version, a digest
for the artefact content has to be calculated, also, and incorporated into the
immutable information of the component descriptor.

By default, this digest is calculated based on the blob provided by the
[access method](../elements/README.md#artefact-access)
of an artefact. But there might be technology specific ways to uniquely identify
the content for dedicated artefact types, which might depend on the chosen blob media type.

Therefore, together with the digest and its algorithm, an artefact normalization
algorithm is kept in the [component descriptor](../elements/README.md#component-descriptor).
This process is called [*artefact blob normalization]*(artefact_normalization.md)

