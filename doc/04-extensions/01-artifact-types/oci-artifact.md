# OCI Artifact or Artifact Index

## Type Name
**`ociArtifact`**

## Description
A generic OCI artifact following the [open containers image specification](https://github.com/opencontainers/image-spec/blob/main/spec.md).

## Format Variants:

When provided as a blob, the [Artifact Set Archuive Format](../common/formatspec.md#artifact-set-archive-format)
MUST be used to represent the content of the OCI artifact.
This format can be used to store multiple versions of an OCI repository
in a filesystem-compatible manner.

Media Types:

- `application/vnd.oci.image.manifest.v1+tar+gzip`: OCI image manifests
- `application/vnd.oci.image.index.v1+tar.gzip`: OCI index manifests

## Special Support:

There is a dedicated uploader available for local blobs. It converts a blob with the media type shown above into a regular OCI artifact in an OCI repository.

It uses the reference hint attribute of the [`localBlob` access method](../02-access-types/localblob.md) to determine an appropriate OCI repository. If the import target of the OCM component version is an OCI registry, by default, the used OCI repository will be the base repository of the [OCM mapping](../../03-persistence/02-mappings.md#mappings-for-ocm-persistence) with the appended reference hint.
