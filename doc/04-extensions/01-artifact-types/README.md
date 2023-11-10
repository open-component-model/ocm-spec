# Artifact Types

The formal type of an artifact uniquely specifies the logical interpretation of an artifact and its kind, independent of its concrete technical representation.
Artifacts appear in two flavors in the OCM model, as resources and as sources. They have three main characteristics:

- content (byte sequence or blob)
- technical format of the blob (mime type)
- semantical meaning

An artifact type describes the semantic meaning of an artifact, e.g. a Helm chart. The content of a Helm chart might exist in different blob formats, either a directory
tree or an OCI artifact blob, as described by a mime type. The access method always provides the content of an artifact as a blob plus a mime type.

The definition of an artifact type MUST contain a unique name, the meaning of the content and possible blob formats in form of mime types.

The following table contains all artifact types defined in the core specification. 

| ARTIFACT TYPE      | VALUE                                         | DESCRIPTION                                                                                                                                |
|--------------------|-----------------------------------------------|--------------------------------------------------------------------------------------------------------------------------------------------|
| Blob               | [`blob`](#blobd)                             | Any anonymous untyped blob data                                       |
| Filesystem Content | [`filesystem` `directoryTree`](#file-system) | Files from a file system (typically provided by a *tar* or *tgz* archive). The mime type of the blob specifies the concrete format |
| GitOps             | [`gitOpsTemplate`](#file-system)         | Filesystem content (tar, tgz) used as GitOps Template, e.g. to set up a git repo used for continuous deployment for example using FluxCD  |
| Helm Chart         | [`helmChart`](#helm-chart)                   | A Helm Chart stored as OCI artifact or as tar blob (`mediaType` tar) |
| Node Package Manager | [`npm`](npm.md)                             | A Node Package Manager [npm](https://www.npmjs.com) archive |
| OCI Artifact       | [`ociArtifact`](#oci-artifact)               | A generic OCI artifact following the [open containers image specification](https://github.com/opencontainers/image-spec/blob/main/spec.md) |
| OCI Image          | [`ociImage`](#oci-image)                     | An OCI image or image list  |

Some additional types are defined, but not part of the core specification. Support is optional, but the list of names is reserved.

| TYPE               | VALUE                                         | DESCRIPTION                                                                                                                                |
|--------------------|-----------------------------------------------|--------------------------------------------------------------------------------------------------------------------------------------------|
| Blueprint          | [`blueprint`](blueprint.md)                   | An installation description for the [landscaper](https://github.com/gardener/landscaper) installation environment                        |
| TOI Executor       | [`toiExecutor`](toiExecutor.md)               | A toolset for simple installation in the [OCM CLI](https://github.com/open-component-model/ocm/blob/main/docs/reference/ocm_toi.md) installation environment.    |
| TOI Package        | [`toiPackage`](toiPackackage.md)              | A YAML resource describing the installation for the [OCM CLI](https://github.com/open-component-model/ocm/blob/main/docs/reference/ocm_toi.md) TOI installation. |

