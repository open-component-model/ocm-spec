# E. Artifact Types

The following [artifact types](../../specification/formats/types.md#artifact-types) are centrally defined:

| TYPE          | VALUE                           | DESCRIPTION                   |
| ------------- | ------------------------------- | ----------------------------- |
| OCI Artifact  | [`ociArtefact`](ociArtefact.md) | A generic OCI artefact following the [open containers image specification](https://github.com/opencontainers/image-spec/blob/main/spec.md) |
| OCI Image     | [`ociImage`](ociImage.md)       | An OCI image or image list |
| Helm Chart    | [`helmChart`](helmChart.md)     | A Helm Chart stored as OCI artifact or as tar blob (`mediaType` tar) |
| Blob          | [`blob`](blob.md)               | Any anonymous untyped blob data |
| Filesystem   | [`fileSystem`](fileSystem.md)    | Some filesystem content (tar, tgz) |
| GitOps        | [`gitOpsTemplate`](gitOpsTemplate.md) | Filesystem content (tar, tgz) used as GitOps Template, e.g. to set up a git repo used for continuous deployment (for example flux) |

For centrally defined artifact types, there might be special support in the
standard OCM library and tool set. For example, there is a dedicated downloader
for helm charts providing the filesystem helm chart format regardless of
the storage method and supported media type.
