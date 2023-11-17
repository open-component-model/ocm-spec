# Storage Backend Mappings

The OCM specification describes an interpretation layer on-top of
well-known storage backend technologies used to store OCM component versions.

Therefore, for every storage technology a dedicated mapping 
must be defined to ensure interoperability of different
OCM implementations.

These mappings describe:
- the repository specification [type](../../01-model/01-model.md#repository-types)
  and format used to specify a dedicated repository instance
- the mapping of the [OCM elements](../../01-model/02-elements-toplevel.md) 
  to the elements provided by the storage technology.

Mappings for the following technologies are defined:

* [OCIRegistry](oci.md) OCM content in OCI registries
* [FileSystem (CTF)](ctf.md) OCM content as filesystem structure
* [FileSystem (Component Archive)](component-archive.md) Single component version as content as filesystem structure
* [AWS S3](s3.md) OCM content in AWS S3 buckets
