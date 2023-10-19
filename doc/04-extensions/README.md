# Extensions <extensible part>

This chapter contains elements being part of the OCM specification that can be extended by users or in specific environments. The elements mentioned here are standardized but can be extended independent of the core parts.

# Model Elements
- [ Extensible Parts of the OCM model](01-extensions.md)

# Storage Mappings
for the following technologies are defined:

- [OCIRegistry](03-oci.md) OCM content in OCI registries
- [FileSystem (CTF)](04-files.md) OCM content as filesystem structure
- [FileSystem (Component Archive)](04-files.md) Single component version as content as filesystem structure
- [AWS S3](05-s3.md) OCM content in AWS S3 buckets

# Table Of Content

* 1.[Extensible Field Values](01-extensions.md#extensible-field-values)
  * 1.1.[Resource Types](01-extensions.md#resource-types)
  * 1.2.[Source Types](01-extensions.md#source-types)
  * 1.3.[Access Types](01-extensions.md#access-types)
* 2.[Normalization Algorithms](01-extensions.md#normalization-algorithms)
  * 2.1.[jsonNormalisationV1](01-extensions.md#jsonnormalisationv1)
* 3.[Digest Algorithms](01-extensions.md#digest-algorithms)
  * 3.1.[Digesting Content](01-extensions.md#digesting-content)
* 4.[Signature Algorithms](01-extensions.md#signature-algorithms)
  * 4.1.[RSA](01-extensions.md#rsa)
* 5.[Storage Backends](01-extensions.md#storage-backends)
* 6.[OCI Registries](03-oci.md#oci-registries)
  * 6.1.[Specification Format](03-oci.md#specification-format)
    * 6.1.1.[Synopsis](03-oci.md#synopsis)
    * 6.1.2.[Description](03-oci.md#description)
    * 6.1.3.[Specification Versions](03-oci.md#specification-versions)
  * 6.2.[Element Mapping](03-oci.md#element-mapping)
  * 6.3.[Version Mapping](03-oci.md#version-mapping)
  * 6.4.[Blob Mappings](03-oci.md#blob-mappings)
  * 6.5.[Example](03-oci.md#example)
* 7.[Common Transport Format (CTF)](04-files.md#common-transport-format-ctf)
  * 7.1.[Specification Format](04-files.md#specification-format)
    * 7.1.1.[Synopsis](04-files.md#synopsis)
    * 7.1.2.[Description](04-files.md#description)
    * 7.1.3.[Specification Versions](04-files.md#specification-versions)
  * 7.2.[Element Mapping](04-files.md#element-mapping)
  * 7.3.[Blob Mappings](04-files.md#blob-mappings)
  * 7.4.[Examples](04-files.md#examples)
    * 7.4.1.[Example of a transport archive containing two artifacts](04-files.md#example-of-a-transport-archive-containing-two-artifacts)
* 8.[Component Archive Format](04-files.md#component-archive-format)
  * 8.1.[Specification Format](04-files.md#specification-format)
    * 8.1.1.[Synopsis](04-files.md#synopsis)
    * 8.1.2.[Description](04-files.md#description)
    * 8.1.3.[Specification Versions](04-files.md#specification-versions)
  * 8.2.[Element Mapping](04-files.md#element-mapping)
  * 8.3.[Blob Mappings](04-files.md#blob-mappings)
  * 8.4.[Examples](04-files.md#examples)
* 9.[AWS S3](05-s3.md#aws-s3)
  * 9.1.[Specification Format](05-s3.md#specification-format)
    * 9.1.1.[Synopsis](05-s3.md#synopsis)
    * 9.1.2.[Description](05-s3.md#description)
    * 9.1.3.[Specification Versions](05-s3.md#specification-versions)
  * 9.2.[Element Mapping](05-s3.md#element-mapping)
  * 9.3.[Blob Mapping](05-s3.md#blob-mapping)