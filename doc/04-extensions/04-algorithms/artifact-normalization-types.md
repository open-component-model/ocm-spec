# Artifact Normalization Types

The following algorithms are defined:

- `EXCLUDE-FROM-SIGNATURE`: Blob content is ignored for the signing process.

  This is a possibility for referencing volatile artifact content.

- `genericBlobDigest/v1` (*default*): Blob byte stream digest

  This is the default algorithm. It just uses the blob content
  provided by the access method of an OCM artifact to calculate the digest.
  It is always used, if no special digester is available for an artifact type.

- `ociArtifactDigest/v1`: OCI manifest digest

  This algorithm is used for artifact blobs with the media type of an OCI artifact.
  It just uses the manifest digest of the OCI artifact.
  