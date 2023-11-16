#ociArtifact

##Synopsis

```
type: ociArtifact[/VERSION]
[ATTRIBUTES]
```

## Description
Access of an OCI artifact stored in an OCI registry.

## Supported Media Types

- `application/vnd.oci.image.manifest.v1+tar+gzip`: OCI image manifests
- `application/vnd.oci.image.index.v1+tar.gzip`: OCI index manifests

Depending on the repository appropriate docker legacy types might be used.

## Specification Version

The following versions are supported

### v1

Attributes:

- **`imageReference`** *string*

  OCI image/artifact reference following the possible docker schemes:
    - `<repo>/<artifact>:<digest>@<tag>`
    - `<host>[<port>]/repo path>/<artifact>:<version>@<tag>`

