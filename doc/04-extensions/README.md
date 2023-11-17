# Extensions (extensible part)

This chapter contains elements being part of the OCM specification that can be extended by users or in specific environments. The elements mentioned here are standardized but can be extended independent of the core parts.

# Model Elements
- [ Extensible Parts of the OCM model](01-extensions.md)

# Storage Mappings
for the following technologies are defined:

- [OCIRegistry](03-oci.md) OCM content in OCI registries
- [FileSystem (CTF)](04-files.md) OCM content as filesystem structure
- [FileSystem (Component Archive)](04-files.md) Single component version as content as filesystem structure
- [AWS S3](05-s3.md) OCM content in AWS S3 buckets

# Extensions

* 1 [Extensible Field Values](01-extensions.md#extensible-field-values)
  * 1.1 [Resource Types](01-extensions.md#resource-types)
  * 1.2 [Source Types](01-extensions.md#source-types)
  * 1.3 [Access Method Types](01-extensions.md#access-types)
* 2 [Normalization Algorithms](01-extensions.md#normalization-algorithms)
  * 2.1 [jsonNormalisationV1](01-extensions.md#jsonnormalisationv1)
* 3 [Digest Algorithms](01-extensions.md#digest-algorithms)
  * 3.1 [Digesting Content](01-extensions.md#digesting-content)
* 4 [Signature Algorithms](01-extensions.md#signature-algorithms)
  * 4.1 [RSA](01-extensions.md#rsa)
* 5  [Storage Backend Mappings](01-storage-backends)
  * 5.1 [OCI Registries](oci.md)
  * 5.2 [File System: Common Transport Format (CTF)](ctf.md)
  * 5.3 [File System: Component Archive](component-archive.md)
  * 5.4 [AWS S3](s3.md)
