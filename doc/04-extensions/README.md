# Extensions

The core specification does not rely on a fixed set of certain fields.
However, the specification defines a set of known values for certain types
listed in the following sections. These sets can be extended by new specification versions,
addendums or for customer-specific environments.

## Table of Content

* 1 [Artifact Types](01-artifact-types/README.md)
  * 1.1 [blob](01-artifact-types/blob.md)
  * 1.2 [directoryTree, fileSystem](01-artifact-types/file-system.md)
  * 1.3 [gitOpsTemplate](01-artifact-types/gitops.md)
  * 1.4 [helmChart](01-artifact-types/helmchart.md)
  * 1.5 [npmPackage](01-artifact-types/npm.md)
  * 1.6 [ociArtifact](01-artifact-types/oci-artifact.md)
  * 1.7 [ociImage](01-artifact-types/oci-image.md)
  * 1.8 [executable](01-artifact-types/executable.md)
  * 1.9 [sbom](01-artifact-types/sbom.md)
* 2 [Access Method Types](02-access-types/README.md)
  * 2.1 [localBlob](02-access-types/localblob.md)
  * 2.2 [ociArtifact](02-access-types/ociartifact.md)
  * 2.3 [ociBlob](02-access-types/ociblob.md)
  * 2.4 [helm](02-access-types/elm.md)
  * 2.5 [gitHub](02-access-types/github.md)
  * 2.6 [s3](02-access-types/s3.md)
  * 2.7 [npm](02-access-types/npm.md)
* 3 [Storage Backend Mappings](03-storage-backends/README.md)
  * 3.1 [OCIRegistry](03-storage-backends/oci.md)
  * 3.2 [FileSystem (CTF)](03-storage-backends/ctf.md)
  * 3.3 [FileSystem (Component Archive)](03-storage-backends/component-archive.md)
  * 3.4 [AWS S3](03-storage-backends/s3.md)
* 4 [Algorithms](04-algorithms/README.md)
  * 4.1 [Artifact Normalization](04-algorithms/artifact-normalization-types.md)
  * 4.2 [Digest Algorithms](04-algorithms/label-merge-algorithms.md)
  * 4.3 [Label Merge Algorithm](04-algorithms/digest-algorithms.md)
  * 4.4 [Component Descriptor Normalization Algorithms](04-algorithms/component-descriptor-normalization-algorithms.md)
  * 4.5 [Signing Algorithms](04-algorithms/signing-algorithms.md)
