# Component Archive Format

Storing a single [component version](../../../specification/elements/README.md#component-versions)
in a file format.

This is  a special kind of OCM repository storage format
capable to host exactly one component version. It is intended
to be used during a build process to compose a dedicated
component version before it is transported into a regular
OCM repository.

## Specification Format

To describe a [repository context](../../../specification/elements/README.md#repository-contexts)
for an OCM repository conforming to this specification the following
repository specification format MUST be used.

### Synopsis

```
type: ComponentArchive/v1
```

### Description

The content of a single OCM Component Version will be stored as Filesystem content.
This is a special version of an OCM Repository, which can be used to
compose a component version during the build time of a component.

An OCM repository view will be mapped to a
filesystem-based representation according to the [Component Archive Format specification](../../common/formatspec.md#component-archive-format).

### Specification Versions

#### Version `v1`

The type specific specification fields are:

- **`filePath`** *string*

  Path in filesystem used to host the repository.

- **`fileFormat`** (optional) *string*

  The format to use to store content:
  - `directory`: stored as directory structure
  - `tar`: stored as directory structure in a tar file
  - `tgz`: stored as directory structure in a tar file compressed by GNU Zip


## Element Mapping

The [component-descriptor](../../../specification/elements#component-descriptor) is stored as top-level file and local blobs in the `blobs`folder.

## Blob Mappings

This format supports no dedicated blob mappings.
Local blobs are always stored as blobs.

## Examples

```text
component-archive
├── component-descriptor.yaml
└── blobs
    ├── sha.456... (local blob)
    └── sha.567... (local blob)
```
