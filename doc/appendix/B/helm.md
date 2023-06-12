
# Access Method `helm` - Helm Repository Access


### Synopsis
```
type: helm/v1
```

Provided blobs use the following media type: attribute `application/vnd.cncf.helm.chart.content.v1.tar+gzip`

### Description
This method implements the access of a Helm chart stored in a Helm chart repository.

Supported specification version is `v1`

### Specification Versions

#### Version `v1`

The type specific specification fields are:

- **`helmRepository`** *string*

  Helm repository URL.

- **`helmChart`** *string*

  The name of the Helm chart and its version separated by a colon.

- **`caCert`** *string*

  An optional TLS root certificate.

- **`keyring`** *string*

  An optional keyring used to verify the chart.

### Related

Helm charts can be stored as OCI artifacts in OCI registries, also. The access to those
helm charts is described by the access method [`ociArtifact](ociArtifact.md).