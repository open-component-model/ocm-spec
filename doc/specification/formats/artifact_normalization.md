# Artifact Normalization Types

To be able to sign a component version, the content of described artifacts
must be incorporated. Therefore, a digest for the artifact content must be
determined.

By default, this digest is calculated based on the blob provided by the
[access method](../elements/README.md#artifact-access)
of an artifact. But there might be technology specific ways to uniquely identify
the content for dedicated artifact types.

Therefore, together with the digest and its algorithm, an artifact normalization
algorithm is kept in the [component descriptor](../elements/README.md#component-descriptor).

## Blob Representation Format for Resource Types

The central task of a [component version](../../introduction/component_versions.md)
is to provide information about  versioned sets of resources. Therefore, a
[component descriptor](../../specification/elements/README.md#component-descriptor)
as technical representation of a component version describes such a set of resources.
This explicitly includes access information, a formal description to describe a
technical access path, which can be used to gain access to the real technical
content. For the component model such content of resources is just seen as
simple typed blobs. This enables to formally reference blobs in external
environments, as long as the described [access method](../specification/elements/README.md#artifact-access)
is known to the consuming environment. The evaluation of an access specification
always results in a simple blob representing the content of the described resource.
This way basically all required blobs can be stored in any supported external blob store.

An [access method](../../specification/elements/README.md#artifact-access) must
always be able to return a blob representation for the accessed artifact.
If there are native storage technologies for dedicated artifact types they
must deliver such a blob, also.

This basically means, whenever a new resource type is supported,
corresponding blob formats must be defined for this type. Type-agnostic access types, like [`localBlob`](../B/localBlob.md) or [`ociBlob`](../B/ociBlob.md)
just deal with those blobs, they never need to know anything about their internal
format. But specific access methods, e.g. the [`ociArtecat`](../B/ociArtefact.md)
method may provide dedicated blob formats.

These blob formats may depend on the combination of artifact type and access type.
Therefore, a blob always has a *mimeType* specifying the technical format.

For every artifact type the possible mime types with their technical format
specifications must be defined.

When using the component repository to transport content from one repository the
another one (possibly behind a firewall without access to external blob
repositories), the described content of a component version must be
transportable by value together with the component descriptor. Therefore, the
access information stored along with the described resources may change over time
or from environment to environment. But all variants must describe the same
technical content.

If multiple mime types are possible for blobs, the digest of the artifact content 
must be immutable to avoid invalidating signatures. Therefore, in such a case, a
dedicated artifact normalization algorithm has to be provided for such mime types.

## Normalization Types

The following algorithms are centrally defined and available in the OCM toolset:

- `ociArtifactDigest/v1`: OCI manifest digest

  This algorithm is used for artifacts of type `ociArtefact`. It just uses the
  manifest digest of the OCI artifact.

- `genericBlobDigest/v1`: Blob byte stream digest

  This is the default normalization algorithm. It just uses the blob content
  provided by the access method of an OCM artifact to calculate the digest.
  It is always used, if no special digester is available for an artifact type.

- `NO-DIGEST`: Blob content is ignored for the signing process.
  
  This is a possibility for referencing volatile artifact content.