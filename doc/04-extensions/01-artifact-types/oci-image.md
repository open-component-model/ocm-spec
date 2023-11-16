# OCI Image

## Type Name
**`ociImage`**

## Description
This type describes an OCI artifact containing an OCI container image. `ociImage` is a dedicated variant using the container image MIME types
used by OCI registries.

A general [ociArtifact](oci-artifact.md) describes any kind of content, depending on the MIME type of its config blob.

## Format Variants

The blob uses the [Artifact Set Archive Format](../common/formatspec.md#artifact-set-archive-format).

MIME types:
-  `application/vnd.oci.image.manifest.v1+tar`
-  `application/vnd.oci.image.manifest.v1+tar+gzip`

## Special Support:

There is a dedicated uploader available for local blobs. It converts a blob with the media type shown above into a regular OCI artifact in an OCI repository.

It uses the reference hint attribute of the [`localBlob` access method](../02-access-types/localblob.md) to determine an appropriate OCI repository. If the import target of the OCM component version is an OCI registry, by default, the used OCI repository will be the base repository of the [OCM mapping](../../03-persistence/02-mappings.md#mappings-for-ocm-persistence) with the appended reference hint.

