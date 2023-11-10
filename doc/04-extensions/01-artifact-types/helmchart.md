# Helm Chart

**`helmChart`**

## Description
A Kubernetes installation resource representing a Helm chart, either stored as OCI artifact or as tar blob.

## Format Variants

- **OCI Artifact**
  
  A Helm chart might be stored as OCI artifact following the [Artifact Set Archive Format](../common/formatspec.md#artifact-set-archive-format). This format is for example provided by the access type [`ociArtifact`](../02-access-types/oci-artifact.md)

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