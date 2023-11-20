# Table of Content
- [Table of Content](#table-of-content)
- [Normalization Algorithms](#normalization-algorithms)
  - [`jsonNormalisationV1`](#jsonnormalisationv1)
  - [`jsonNormalisationV2`](#jsonnormalisationv2)
- [Digest Algorithms](#digest-algorithms)
- [Digesting Content](#digesting-content)
- [Signature Algorithms](#signature-algorithms)
  - [RSA](#rsa)


# Normalization Algorithms

Currently the there are two different normalizations defined:

- `jsonNormalisationV1`: This is a legacy format, which depends on the format of the
  component descriptor
- `jsonNormalisationV2`: This is the new format. which is independent of the
  chosen representation format of the component descriptor.

The normalization process is divided into two steps:

- *extraction of the signature relevant information from the component descriptor*

  The result is basically a JSON object, which decsribed the relevant information.

- *normalization of the resulting JSON object*

  Here, the object is serialized to a unique and reproducable byte sequence, which is finally used to determine the digest.

  There are two such normalization methods:
  - `jsonNormalisationV1`
  - `jsonNormalisationV2`

## `jsonNormalisationV1`

The `JsonNormalisationV1` serialization format is based on the serialization format of the component descriptor.
It uses an appropriate JSON object containing the relevant fields as contained in the component descriptors's serialization.
The format version fields are included. Therefore, the normalized form is depending on the chosen serialization format.
Changing this format version would result in different digests.
The resulting JSON object is serialized with the [OCM specific scheme](#generic-normalization-format)

## `jsonNormalisationV2`

`JsonNormalisationV2` strictly uses only the relevant component descriptor
information according to the field specification. It is independent of the serialization format used to store the component decsriptor in some storage backend. Therefore, the calculated digest is finally independent of the serialization format chosen for storing the component descriptor in a storage backend. It uses a standard scheme according to [RFC8785 (JCS)](https://www.rfc-editor.org/rfc/rfc8785)

# Digest Algorithms

Digest algorithms describe the way digests are calculated from a byte stream.

The following digest algorithms are defined:

- `SHA-256`
- `SHA-512`

# Digesting Content
The following algorithms are defined:

- `NO-DIGEST`: Blob content is ignored for the signing process.

  This is a possibility for referencing volatile artifact content.

- `genericBlobDigest/v1` (*default*): Blob byte stream digest

  This is the default algorithm. It just uses the blob content
  provided by the access method of an OCM artifact to calculate the digest.
  It is always used, if no special digester is available for an artifact type.

- `ociArtifactDigest/v1`: OCI manifest digest

  This algorithm is used for artifact blobs with the media type of an OCI artifact.
  It just uses the manifest digest of the OCI artifact.

# Signature Algorithms

Signing a component-descriptor requires a hash of the normalized component-descriptor,
which will the be signed with the selected signing algorithm.

## RSA

*Algorith Name:* `RSASSA-PKCS1-V1_5`

After the digest for the normalised component-descriptor is calculated, it can be signed using RSASSA-PKCS1-V1_5
as signature.algorithm. The corresponding signature is stored hex encoded in `signature.value` with a `mediaType` of
`application/vnd.ocm.signature.rsa`.