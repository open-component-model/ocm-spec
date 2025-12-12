# Mappings for OCM Persistence

This chapter describes how OCM model elements are mapped to elements of a persistence layer.

OCM model elements are stored using various backend technologies. The interoperability layer for a client tool is typically the API of the chosen storage backend, avoiding the need for a dedicated OCM server.

An implementation of this layer **MUST** support the [mandatory abstract model operations](./01-operations.md#mandatory-operations).  
It **SHOULD** support the [optional operations](./01-operations.md#optional-operations).

## Storage Backend Mappings for the Open Component Model

The OCM specification provides an interpretation layer on top of storage technologies used to persist component versions.

For every supported technology, a mapping **MUST** be defined to ensure consistent interoperability across implementations.  
These mappings describe:

- the repository specification type and format for identifying a repository instance, and
- how OCM model elements are mapped to the artifacts or structures provided by that backend.

These mappings are defined as part of the [extensions](../04-extensions/03-storage-backends/README.md).

## Note on OCI Storage Backends

The OCI storage backend mapping now supports **both manifest-based and index-based representations** of component versions.  
The detailed rules and normative behavior of the index-based format are defined in the corresponding OCI backend extension.
