# helm — Helm Package in Helm Repository

*Synopsis:*
```
type: helm[/VERSION]
[ATTRIBUTES]
```

## Description
Access to a Helm chart in a Helm repository.

## Supported Media Types

  - `application/vnd.cncf.helm.chart.content.v1.tar+gzip`

## Specification Version

The following versions are supported

### v1

Attributes:

- **`helmRepository`** *string*

  Helm repository URL.

- **`helmChart`** *string*

  The name of the Helm chart and its version separated by a colon.

- **`caCert`** *string*

  An optional TLS root certificate.

- **`keyring`** *string*

  An optional keyring used to verify the chart.