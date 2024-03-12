# Artifact Types

The formal type of an artifact uniquely specifies the logical interpretation of an artifact, independent of its concrete technical representation.
Artifacts appear in two flavors in the OCM model, as resources and as sources. They have three main characteristics:

- content (byte sequence or blob)
- technical format of the blobs (media type)
- semantical meaning

An artifact type describes the semantic meaning of an artifact, e.g. a Helm chart. The content of a Helm chart might exist in different blob formats, either a directory
tree or an OCI artifact blob, as described by a mime type. The access method always provides the content of an artifact as a blob plus a mime type.

The definition of an artifact type MUST contain a unique name, the meaning of the content and possible blob formats in form of mime types.

The following table contains all artifact types defined in the core specification.

| TYPE NAME                                     | DESCRIPTION                                                                                                                                |
|-----------------------------------------------|--------------------------------------------------------------------------------------------------------------------------------------------|
| [`blob`](blob.md)                               | Any anonymous untyped blob data                                       |
| [`directoryTree`<br>`fileSystem`](file-system.md) | Files from a file system (typically provided by a *tar* or *tgz* archive). The mime type of the blob e format |
| [`gitOpsTemplate`](gitops.md)                   | Filesystem content (tar, tgz) used as GitOps Template, e.g. to set up a git repo used for continuous e using FluxCD  |
| [`helmChart`](helmchart.md)                     | A Helm Chart stored as OCI artifact or as tar blob (`mediaType` tar) |
| [`npmPackage`](npm.md)                          | A Node Package Manager [npm](https://www.npmjs.com) archive |
| [`ociArtifact`](oci-artifact.md)                | A generic OCI artifact following the [open containers image specification](https://github.com/opencontainers/image-spec/blob/main/spec.md) |
| [`ociImage`](oci-image.md)                     | An OCI image or image list  |
| [`executable`](executable.md)                   | A blob describing an executable program |
| [`sbom`](sbom.md)                               | A list of ingredients that make up software components (<https://www.cisa.gov/sbom>) |

Some additional types are defined, but not part of the core specification. Support is optional, but the list of names is reserved.

| TYPE NAME          |DESCRIPTION                          |
|--------------------|-------------------------------------|
| [`blueprint`](blueprint.md)                   | An installation description for the [landscaper](https://github.com/gardener/landscaper) installation               |
| [`toiExecutor`](toiExecutor.md)               | A toolset for simple installation in the [OCM CLI](https://github.com/open-component-model/ocm/blob/cm_toi.md) installation environment.    |
| [`toiPackage`](toiPackackage.md)              | A YAML resource describing the installation for the [OCM CLI](https://github.com/open-component-model/ocm/blob/main/docs/reference/ocm_toi.md) TOI installation. |
