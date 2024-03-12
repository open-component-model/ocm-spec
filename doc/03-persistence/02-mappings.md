# Mappings for OCM Persistence

This chapter describes how OCM model elements are mapped to elements of a persistence layer.

OCM model elements are mapped to various storage technologies. The interoperability layer for a client tool is typically the API of the storage backend. This avoids the need for providing an OCM server infrastructure.

An implementation of this layer MUST implement this mapping by supporting the [mandatory abstract model operations](./01-operations.md#mandatory-operations). It SHOULD implement the [optional operations](./01-operations.md#optional-operations) too.

## Storage Backend Mappings for the Open Component Model

The OCM specification describes an interpretation layer on-top of well-known storage backend technologies used to store OCM component versions.

Therefore, for every storage technology a mapping must be defined to ensure interoperability between different OCM implementations.

These mappings describe:

- the repository specification type and format used to specify a dedicated repository instance
- the mapping of the OCM elements to the elements provided by the storage technology.

The mappings are defined as part of the [extensions](../04-extensions/03-storage-backends/README.md)
