# A. Storage Backend Mappings for the Open Component Model

The OCM specification describes an interpretation layer on-top of
well-known storage backend technologies used to store
[OCM component versions](../../specification/elements/README.md#component-versions).

Therefore, for every storage technology a dedicated mapping 
must be defined to ensure interoperability of different
OCM implementations.

These mappings describe:
- the repository specification [type](../../specification/formats/types.md#repository-types)
  and format used to specify a dedicated repository instance
- the mapping of the [OCM elements](../../specification/elements/README.md) 
  to the elements provided by the storage technology.

Mappings for the following technologies are defined:

- [OCIRegistry](OCIRegistry/README.md) OCM content in OCI registries
- [FileSystem (CTF)](CTF/README.md) OCM content as filesystem structure
- [AWS S3](S3/README.md)OCM content in AWS S3 buckets


