# Artifact Normalization

To be able to sign a component version a digest for the artifact **content** must be determined.

By default, this digest is calculated based on the blob provided by the access specification.
There might be technology specific ways to uniquely identify the content for dedicated artifact types.
Therefore an artifact normalization algorithm is kept in the component descriptor.

## Blob Representation Format for Resource Types

The central task of a component version is to provide information about versioned sets of resources.
For the component model such content of resources are just simple typed blobs.
The evaluation of an access specification always results in a simple blob, representing the content of the described resource.
This way blobs can be stored in any supported external blob store.

An access method MUST always be able to return a blob representation for the accessed artifact.
If there are native storage technologies for dedicated artifact types they must also deliver such a blob.

Whenever a new resource type is supported, corresponding blob formats MUST be defined for this type.
Type-agnostic access method types, like `localBlob` or `ociBlob` never need to know anything about their internal format.
But specific access methods, e.g. the `ociArtifact` method, MAY provide dedicated blob formats.

These blob formats may depend on the combination of artifact type and access method type.
Therefore, a blob always has a *media type* specifying the technical format.
For every artifact type the possible media types with their technical format specifications MUST be defined.

When using the component repository to transport content from one repository to
another the access information may change. But all variants MUST describe the same
content.

If multiple media types are possible for blobs, the digest of the artifact content
MUST be immutable to avoid invalidating signatures. In such a case a
dedicated artifact normalization algorithm MUST be provided for such media types.

Available artifact normalization types can be found [here](./03-signing-process.md#normalization-types).

## Interaction of Local Blobs, Access Methods, Uploaders and Media Types

The Open Component Model is desiged to support transports of artifacts.
To assure the integrity of digests and signatures some rules must be obeyed by the involved model extensions.

### Access Methods

A remote access method MUST return the artifact content as blob.

By default, this blob is used to calculate the content digest for an artifact.
Therefore, the byte-stream of this blob must be deterministic.
Multiple calls for the same content must return the identical blob.
If this cannot be guaranteed, a blob digest handler for the media type of this blob format MUST be defined.

For example, the `ociArtifact` access method provides content as artifact set blob,
with a format based on the OCI artifact structure, which is defined by a dedicated media type.
For this media type a digest handler is defined, which replaces the default blob digest by the manifest digest of the artifact.
This way the digest is independent from the creation of the archive blob containing the artifact.

Once the artifact content has been converted to a blob and stored as local blob,
this blob is by default kept for further transport steps.
This way, the digest calculation always provides the same result.

### Blob Uploaders

Blob Uploaders can be used as part of the transport process, to automatically
provide transported artifacts in technology specific local storage systems, e.g. OCI registries.
The Open Component Model allows to change access locations
of artifact content during transport. Therefore an automatic upload
with modification of the access method is principally allowed.
In such scenarios, it's essential to adhere to specific rules to ensure the integrity of digests and signatures.

If a blob uploader is used to upload the artifact to a remote repository after a transfer again,
the access method can potentially be changed. But this MUST guarantee the same digest calculation.
The new access method must again provide a blob with a media type and digest handler combination, providing the same digest.

For example, storing an OCI artifact delivered as local blob in an OCI repository again, the manifest digest will be the same.
This is guaranteed because it is the identity of the artifact according to the OCI specification.
As a result, a new transformation to a blob representation in combination with the digest handler
will always provide the same artifact digest. The access method can be switched again,
from `localBlob` to `ociArtifact` regardless of the artifact type.

If this can not be guaranteed, once a blob representation is chosen, it must be kept as it is.
In such a case a blob uploader must preserve the local access method,
even if it uploads the content to an external storage system.

This can be described in the component version by adding the new remote access specification
as part of the existing local one, using the `globalAccess` attribute.

The artifact digest is always calculated based on the local access,
but tools may use the information provided by the global access to use technology native ways to access the artifact.
