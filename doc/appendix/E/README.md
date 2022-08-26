# E. Artifact Types

The following [artefact types](../../specification/formats/types.md#artifact-types) are centrally defined:

- [`ociArtefact`](ociArtefact.md) a generic OCI artefact following the
  [open containers image specification](https://github.com/opencontainers/image-spec/blob/main/spec.md)
- [`ociImage`](ociImage.md) an OCI image or image list
- [`helmChart`](helmChart.md)  a helm chart, either stored as OCI artefact or as tar blob (tar media type)
- [`blob`]: any anonymous untyped blob data
- [`fileSystem`](fileSystem.md)  some filesystem content (tar, tgz)
- [`gitOpsTemplate`](gitOpsTemplate.md) a filesystem content (tar, tgz) used as Git Ops Template to set up a git repo used for continuous deployment (for example flux)

For centrally defined artifact types, there might be special support in the
standard OCM library and tool set. For example, there is a dedicated downloader
for helm charts providing the filesystem helm chart format regardless of
the storage method and supported media type.

Besides those types, there are some vendor types that are typically used:

- [`landscaper.gardener.cloud/blueprint`](blueprint.md) an installation description for the landscaper tool
- [`toiPackage`](toiPackage.md) a package for the Tiny OCM Installation Framework.
- [`toiExecutor`](toiExecutor.md) an executor for the Tiny OCM Installation Framework


