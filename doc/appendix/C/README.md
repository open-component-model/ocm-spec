# C. Digest Calculation

The signing of a component version is based on content of the 
[component descriptor](../../specification/elements/README.md#component-descriptor)
describing a [component version](../../specification/elements/README.md#component-versions),
the content of the described [artefacts](../../specification/elements/README.md#artefacts) and the
[referenced component versions](../../specification/elements/README.md#aggregation).

A signature of a component version is based on digests of the involved elements.
Therefore, the there must be a defined way, how to calculate digests for
artefact content and component descriptors, which be used in a recursive way
to handle aggregations.

## Artefact Digest

Because the content of every artefact is provided in dedicated blob formats by the
various [access methods](../../specification/elements/README.md#artefact-access), such
a digest can be calculated based on this blob. This is the default behaviour.
Nevertheless, there might be technology specific ways to provide an immutable
digest for a dedicated type of artefact, independent of the blob format generation
(typically an archive). For example, an OCI artefact
is always uniquely identified by its manifest digest. This can be exploited
for the calculation of OCM artefact digests.

Together with the digest and its algorithm, for example SHA-256, a
normalization type is kept for an artefact. This algorithm specifies the way
the digest is determined. For example, for OCI artefacts, the algorithm
`ociArtefactDigest/v1` is used by default. This behaviour can be controlled by
appropriate digest handlers. Supported algorithms can be found
[here](../../specification/formats/artefact_normalization.md).

If the digest algorithm `NO-DIGEST` is specified for an artefact,
this artefact content is not included into the component version digest.
This is typically configured for source artefacts, which are not deliverable.

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

 - `ociArtefactDigest/v1`: uses the hash of the manifest of an oci artefact
 - `genericBlobDigest/v1`: uses the hash of the blob


## Digest Algorithms

Digest algorithms describe the way digests are calculated from a byte stream.

The following digest algorithms are defined:

- `SHA-256`
- `SHA-512`

## Normalization Types

The following algorithms are centrally defined and available in the OCM toolset:

- `NO-DIGEST`: Blob content is ignored for the signing process.

  This is a possibility for referencing volatile artefact content.
- 
- `genericBlobDigest/v1` (*default*): Blob byte stream digest

  This is the default normalization algorithm. It just uses the blob content
  provided by the access method of an OCM artefact to calculate the digest.
  It is always used, if no special digester is available for an artefact type.

- `ociArtefactDigest/v1`: OCI manifest digest

  This algorithm is used for artefact blobs with the media type of an OCI artefact.
  It just uses the manifest digest of the OCI artefact.


