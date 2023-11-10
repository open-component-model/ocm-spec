# OCI Artifact or Artifact Index

## Synopsis
**`ociArtifact`**

## Description
A generic OCI artifact following the [open containers image specification](https://github.com/opencontainers/image-spec/blob/main/spec.md).

## Format Variants:

When provided as a blob, the [Artifact Set Archuive Format](../common/formatspec.md#artifact-set-archive-format)
MUST be used to represent the content of the OCI artifact.
This format can be used to store multiple versions of an OCI repository
in a filesystem-compatible manner. In this scenario only the
single version of interest is stored.

Mime types:

- `application/vnd.oci.image.manifest.v1+tar+gzip`: OCI image manifests
- `application/vnd.oci.image.index.v1+tar.gzip`: OCI index manifests

Special Support:

There is a dedicated uploader available for local blobs. It converts a blob with the media type shown above into a regular OCI artifact in an OCI repository.

It uses the reference hint attribute of the [`localBlob` access method](#localblob) to determine an appropriate OCI repository. If the import target of the OCM component version is an OCI registry, by default, the used OCI repository will be the base repository of the [OCM mapping](../04-persistence/01-mappings.md#mappings-for-ocm-persistence) with the appended reference hint.

# Helm Chart



## Description
A Kubernetes installation resource representing a Helm chart, either stored as OCI artifact or as tar blob.

## Blob Formats

- **OCI Artifact**
  
  A Helm chart might be stored as OCI artifact following the [Artifact Set Format](../common/formatspec.md#artifact-set-archive-format). This format is for example provided by the access type [`ociArtifact`](../02-access-types/oci-artifact.md)

  Mime types:
  -  `application/vnd.oci.image.manifest.v1+tar`
  -  `application/vnd.oci.image.manifest.v1+tar+gzip`

- **Helm Tar Archive**

  If stored in the Helm tar format (for the filesystem), the tar media type MUST be used.

  Mime types: 
  - `application/vnd.cncf.helm.chart.content.v1.tar`
  - `application/vnd.cncf.helm.chart.content.v1.tar+gzip`

  
## Special Support

There is a dedicated downloader available, that always converts the Helm chart blob into the appropriate filesystem
representation required by Helm when downloading the artifact using the command line interface.