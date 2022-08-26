# `ociArtefact` &#8212; OCI Artefact Access


### Synopsis

```
type: ociArtefact/v1
```

Provided blobs use the following media type:

- `application/vnd.oci.image.manifest.v1+tar+gzip`: OCI image manifests
- `application/vnd.oci.image.index.v1+tar.gzip`: OCI index manifests

Depending on the repository appropriate docker legacy types might be used.

The artefact content is provided in the [Artefact Set Format](../common/formatspec.md#artefact-set-archive-format).
The tag is provided as annotation.

### Description

This method implements the access of an OCI artefact stored in an OCI registry.

### Specification Versions

Supported specification version is `v1`

#### Version `v1`

The type specific specification fields are:

- **`imageReference`** *string*

  OCI image/artefact reference following the possible docker schemes:
    - `<repo>/<artefact>:<digest>@<tag>`
    - `<host>[<port>]/repo path>/<artefact>:<version>@<tag>`
