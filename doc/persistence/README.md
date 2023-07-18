# OCM Persistence

This chapter describes how OCM model elements are mapped to elements of a persistence layer.

OCM model elements are mapped to various storage technologies. The interoperability layer for a client tool is typically the API of the storage backend. This avoids the need for a dedicated OCM server infrastructure.

An implementation of this layer for a dedicated storage technology MUST
implement this mapping by supporting the mandatory abstract model operations. It SHOULD implement the optional operations, also.