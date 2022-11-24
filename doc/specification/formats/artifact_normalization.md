# Artifact Normalization

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
format. But specific access methods, e.g. the [`ociArtecat`](../B/ociArtifact.md)
method may provide dedicated blob formats.

These blob formats may depend on the combination of artifact type and access type.
Therefore, a blob always has a *media type* specifying the technical format.

For every artifact type the possible media types with their technical format
specifications must be defined.

When using the component repository to transport content from one repository the
another one (possibly behind a firewall without access to external blob
repositories), the described content of a component version must be
transportable by value together with the component descriptor. Therefore, the
access information stored along with the described resources may change over time
or from environment to environment. But all variants must describe the same
technical content.

If multiple media types are possible for blobs, the digest of the artifact content 
must be immutable to avoid invalidating signatures. Therefore, in such a case, a
dedicated artifact normalization algorithm has to be provided for such media types.

Available artifact normalization types can be found in [appendix C](../../appendix/C/README.md#normalization-types).

## Interaction of Local Blobs, Access Methods, Uploaders and Media Types

The Open component model is desiged to support [transports](../../introduction/transports.md)
of described content from one environment into another one.
There are several mechanisms to support this:
- the [access method](../elements/README.md#artifact-access) of an artifact
  may change over time and from OCM repository to OCM repository used to store
  a component version.
- the access method must define a procedure to provide a blob representation for
  an artifact content.
- the model defines a [way to store content](../operations/README.md#mandatory-operations)
  along with the [component descriptor](../elements/README.md#component-descriptor) describing
  a [component version](../elements/README.md#component-versions).
  in a [component repository](../../introduction/component_repository.md) ([local blobs](../../appendix/B/localBlob.md).

To assure the integrity of digests and signatures some rules must be obeyed by the
involved model extensions.

### Access Methods

A remote [access method](../elements/README.md#artifact-access) (access to an artifact
storage outside the OCM repository) must return the artifact content as blob. 

By default, this blob is used to calculate the content digest for the artifact, 
therefore, this blob byte-stream must be deterministic. Multiple calls for the
same content must return the identical blob.

If this cannot be guaranteed, a blob digest handler for the media type of this
blob format must be defined.

For example. the [`ociArtifact`](../../appendix/B/ociArtifact.md) access method
provides the content as artifact set
blob, with a format based on the OCI artifact structure, which is defined by a dedicated
media type. For this media type a digest handler is defined, which replaces the default
blob digest by the manifest digest of the artifact. This way the digest is independent
of the creatio of the archive blob containing the artifact.

Once the artifact content has been converted to a blob and stored as local blob
in the component version (for example during a [transport](../../introduction/transports.md)
step), this blob is by  default kept for further transport steps. This way,
the digest calculation always provides the same result.

### Blob Uploaders

An *Uploader* can be used as part of a transport process to automatically
provide transported artifacts in technology specific local storage systems, again
(e.g. OCI registries). The Open Component Model allows to change access locations
of artifact content during a transport step, therefore such an automatic uploadeing
with the modification of the access method is principally allows. But, in such
scenarios dedicated rules must be obeyed to assure the integrity of digests and signatures.

If a blob uploader is used to upload the artifact to a remote repository again, 
at the target side of a transport, the access method can potentially be changed
to this new remote access accoding to the OCM specification.
But this MUST guarantee the same digest calculation. The new access method must
provide a blob again with a media type and digest handler combination, which
provides the same digest.

For example, storing an OCI artifact, delivered as local blob, in an OCI repository,
again, the manifest digest will be the same, because this is the identity of
artifact according to the OCI specification. As a result, a new transformation
to a blob representation in combination with the digest handler will always
provide the same artifact digest.
Therefore, the access method can be switched again, from `localBlob` to `ociArtifact`
regardless of the artifact type.

If this is not possible, once a blob representation is chosen, it must be kept as
it is. In such a case a blob uploader must preserve the local access method, even
if it uploads the content to an external storage system, which would be accessible
via another remote access method.

This can be described in the component version, by adding this new remote access
specification as part of the specification of the existing local one using
the [`globalAccess` attribute](../../appendix/B/localBlob.md).

The artifact digest is always calculated based on the local access, but tools 
may use the information provided by the global access for their purposes to
use technology native ways to access the artifact.