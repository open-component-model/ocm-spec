# ociBlob — Blob hosted in OCI Repository

## Synopsis
```
type: ociBlob[/VERSION]
[ATTRIBUTES]
```

# Description
Access of an OCI blob stored in an OCI repository.

## Supported Media Types

The provided media type is taken from the specification attribute `mediaType`.

## Specification Version

The following versions are supported

### v1

Attributes:

- **`imageReference`** *string*

  OCI repository reference (this artifact name used to store the blob).

- **`mediaType`** *string*

  The media type of the blob

- **`digest`** *string*

  The digest of the blob used to access the blob in the OCI repository.

- **`size`** *integer*

  The size of the blob