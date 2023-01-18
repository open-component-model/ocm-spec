# E. Artifact Types

The following [artifact types](../../specification/formats/types.md#artifact-types) are centrally defined:

| TYPE          | VALUE                           | DESCRIPTION                   |
| ------------- | ------------------------------- | ----------------------------- |
| OCI Artifact  | [`ociArtifact`](ociArtefact.md) | A generic OCI artifact following the [open containers image specification](https://github.com/opencontainers/image-spec/blob/main/spec.md) |
| OCI Image     | [`ociImage`](ociImage.md)       | An OCI image or image list |
| Helm Chart    | [`helmChart`](helmChart.md)     | A Helm Chart stored as OCI artifact or as tar blob (`mediaType` tar) |
| Blob          | [`blob`](blob.md)               | Any anonymous untyped blob data |
| Filesystem   | [`fileSystem`](fileSystem.md)    | Some filesystem content (tar, tgz) |
| GitOps        | [`gitOpsTemplate`](gitOpsTemplate.md) | Filesystem content (tar, tgz) used as GitOps Template, e.g. to set up a git repo used for continuous deployment (for example flux) |

For centrally defined artifact types, there might be special support in the
standard OCM library and tool set. For example, there is a dedicated downloader
for helm charts providing the filesystem helm chart format regardless of
the storage method and supported media type.

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

If multiple mime types are possible for blobs, the digest of the artifact content must be immutable to avoud invalidating signatures. Therefore, in such a case, a
dedicated [blob normalization algorithms](../../specification/formats/artifact_normalization.md) 
has to be provided for such mime types.
