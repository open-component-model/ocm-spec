# C. Digest Calculation

The signing of a component version is based on content of the 
[component descriptor](../../specification/elements/README.md#component-descriptor)
describing a [component version](../../specification/elements/README.md#component-versions),
the content of the described [artifacts](../../specification/elements/README.md#artifacts) and the
[referenced component versions](../../specification/elements/README.md#aggregation).

A signature of a component version is based on digests of the involved elements.
Therefore, the there must be a defined way, how to calculate digests for
artifact content and component descriptors, which be used in a recursive way
to handle aggregations.

## Artifact Digest

Because the content of every artifact is provided in dedicated blob formats by the
various [access methods](../../specification/elements/README.md#artifact-access), such
a digest can be calculated based on this blob. This is the default behaviour.
Nevertheless, there might be technology specific ways to provide an immutable
digest for a dedicated type of artifact, independent of the blob format generation
(typically an archive). For example, an OCI artifact
is always uniquely identified by its manifest digest. This can be exploited
for the calculation of OCM artifact digests.

Together with the digest and its algorithm, for example SHA-256, a
normalization type is kept for an artifact. This algorithm specifies the way
the digest is determined. For example, for OCI artifacts, the algorithm
`ociArtifactDigest/v1` is used by default. This behaviour can be controlled by
appropriate digest handlers. Supported algorithms can be found
[here](../../specification/formats/artifact_normalization.md).

If the digest algorithm `NO-DIGEST` is specified for an artifact,
this artifact content is not included into the component version digest.
This is typically configured for source artifacts, which are not deliverable.

## Component Descriptor Digest

The digest of a component descriptor is calculated on a normalized form of the
elements of a [component descriptor](../../specification/elements/README.md#component-descriptor).


### Normalization of the component-descriptor

The normalization of the [component-descriptor](../../specification/elements/README.md#component-descriptor)
describes the process of generating a normalized form a
component-descriptor. A normalized
component-descriptor is a subset of the component-descriptor elements containing
signing-relevant properties, only. 

- based on JSON
- map serializes as alphanumerically ordered list of fields (to define unique order)
- field is map with two keys 'name', 'value'

The process and the format is described [here](../../specification/formats/componentdescriptor_normalization.md).

## Artefact Digests

As described, resources have a digest field to store the content hash. Different resource types will use a different normalisationAlgorithm:

 - `ociArtefactDigest/v1`: uses the hash of the manifest of an oci artifact
 - `genericBlobDigest/v1`: uses the hash of the blob


## Digest Algorithms

Digest algorithms describe the way digests are calculated from a byte stream.

The following digest algorithms are defined:

- `SHA-256`
- `SHA-512`