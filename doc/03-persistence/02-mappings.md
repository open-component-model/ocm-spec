# Mappings for OCM Persistence

This chapter describes how OCM model elements are mapped to elements of a persistence layer.

OCM model elements are mapped to various storage technologies. The interoperability layer for a client tool is typically the API of the storage backend. This avoids the need for providing an OCM server infrastructure.

An implementation of this layer MUST implement this mapping by supporting the [mandatory abstract model operations](../03-operations/README.md#mandatory-operations). It SHOULD implement the [optional operations](../03-operations/README.md#optional-operations) too.

## Storage Backend Mappings for the Open Component Model

The OCM specification describes an interpretation layer on-top of well-known storage backend technologies used to store OCM component versions.

Therefore, for every storage technology a mapping must be defined to ensure interoperability between different OCM implementations.

These mappings describe:
- the repository specification type and format used to specify a dedicated repository instance
- the mapping of the OCM elements to the elements provided by the storage technology.

Mappings for the following technologies are defined:

- [OCIRegistry](04-oci.md) OCM content in OCI registries
- [FileSystem (CTF)](03-files.md) OCM content as filesystem structure
- [FileSystem (Component Archive)](03-files.md) Single component version as content as filesystem structure
- [AWS S3](05-s3.md) OCM content in AWS S3 buckets