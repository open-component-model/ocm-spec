# `helmChart` &#8212; Kubernetes Helm Chart

A Kubernetes installation resource representing a Helm chart, either stored as OCI artefact or as tar blob.

## Format Variants

So far, two technical representations are supported:

- *OCI Artefact*

  If stored as OCI artefact, the access type MUST either be
  `ociArtefact` or the [OCI artefact blob format](ociArtefact.md#format-variants) must be
  used with an appropriate media type.

- *Helm Tar Archive*

  If stored in the Helm tar format (for the filesystem),
  the tar media type MUST be used.

## Special Support

There is a dedicated downloader available, that always converts
the helm chart blob into the appropriate filesystem representation
required by Helm when downloading the artefact using the
command line interface.