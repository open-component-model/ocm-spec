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

### Specification Versions

Supported specification version is `v1`.

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

## Examples

```text
artifact-archive
├── artifact-index.json
└── blobs
    ├── sha.123... (manifest.json)
    ├── sha.234... (config.json)
    ├── sha.345... (layer 0: component descriptor)
    ├── sha.456... (local blob / transport archive of a previously external resource)
    └── sha.567... (local blob / transport archive of a previously external resource)
```

The component version appears in the archive-descriptor.json as a tag associated to the digest of the component
descriptor:

```json
{
  "schemaVersion": 1,
  "artifacts": [
    {
      "repository": "component-descriptors/<component name>>",
      "tag": "0.1.0",
      "digest": "sha256:123..."
    }
  ]
}

```

### Example of a transport archive containing two artifacts

```text
transport-archive
├── artifact-descriptor.json
└── blobs
    ├── sha256.111... (manifest.json of artifact 1)
    ├── sha256.222... (config.json   of artifact 1)
    ├── sha256.333... (layer         of artifact 1)
    ├── sha256.444... (layer         of artifact 1)
    ├── sha256.555... (manifest.json of artifact 2)
    ├── sha256.666... (config.json   of artifact 2)
    ├── sha256.777... (layer         of artifact 2)
    └── sha256.888... (layer         of artifact 2)
```

The manifest list in the `artifact-descriptor.json` contains the tags for the two manifests:

```json
{
  "schemaVersion": 1,
  "artifacts": [
    {
      "repository": "component-descriptors/<name of first component>",
      "tag": "0.1.0",
      "digest": "sha256:111..."
    },
    {
      "repository": "component-descriptors/<name of second component>",
      "tag": "0.1.6",
      "digest": "sha256:555..."
    }
  ]
}
```
