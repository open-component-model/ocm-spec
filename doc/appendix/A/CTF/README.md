# Common Transport Format (CTF)

Storing [component versions](../../../specification/elements/README.md#component-versions)
in a file format.

There is no dedicated format for OCM content. Instead,
the OCI registry mapping is reused to represent OCI content in a filesystem
structure. This way the Common Transport Format is defined for general
OCI content and can be used to transport OCI as well as OCM content.

## Specification Format

To describe a [repository context](../../../specification/elements/README.md#repository-contexts)
for an OCM repository conforming to this specification the following
repository specification format MUST be used.

### Synopsis

```
type: CommonTransportFormat/v1
```

### Description

An OCM repository view will be mapped to a
filesystem-based representation according to the [Common Transport Format specification](../../common/formatspec.md#common-transport-format).

Supported specification version is `v1`.

### Specification Versions

#### Version `v1`

The type specific specification fields are:

- **`filePath`** *string*

  The path in the filesystem used to store the content

- **`fileFormat`** *string*

  The file format to use:
    - `directory`: stored as file hierarchy in a directory
    - `tar`: stored as file hierarchy in a TAR file
    - `tgz`: stored as file hierarchy in a GNU-zipped TAR file (tgz)

- **`accessMode`** (optional) *byte*

  Access mode used to access the content:
    - 0: write access
    - 1: read-only
    - 2: create id not existent, yet


## Element Mapping

This format used the [`OCIRegistry`](../OCIRegistry/README.md#element-mapping)
element mapping to map OCM elements to OCI elements.
Those elements will then be stored according to the [OCI mapping to filesystem content](../../common/formatspec.md#common-transport-format)

## Blob Mappings

This format supports no dedicated blob mappings.
Local blobs are always stored as blobs.