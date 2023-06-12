# `ociArtifact` &#8212; General OCI Artifact or Artifact Index

## Format Variants

When provided as a blob, the [Artifact Set Format](../common/formatspec.md#artifact-set-archive-format)
MUST be used to represent the content of the OCI artifact.
THis format can be used to store multiple versions of on OCI repository
in a filesystem-compatible manner. In this scenario only the 
single version of interest is stored.

Provided blobs use the following media type:

- `application/vnd.oci.image.manifest.v1+tar+gzip`: OCI image manifests
- `application/vnd.oci.image.index.v1+tar.gzip`: OCI index manifests

## Special Support

There is a dedicated uploader available for local blobs.
It converts a blob with the media type shown above into 
a regular OCI artifact in an OCI repository.

It uses the reference hint attribute of the
[`localBlob` access method](../B/localBlob.md) to determine
an appropriate OCI repository. If the import target
of the OCM component version is an OCI registry, by default,
the used OCI repository will be the base repository of the
[OCM mapping](../A/OCIRegistry/README.md) with the appended
reference hint.