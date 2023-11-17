# Extensible Field Values

The core specification does not rely on a fixed set of certain fields. However the specification defines a set of known values for certain types listed in the following sections. These sets can be extended by new specification versions, addendums or for customer-specific environments.

## Artifact Types

The formal type of an artifact uniquely specifies the logical interpretation of an artifact, independent of its concrete technical representation.
Artifacts appear in two flavors in the OCM model, as resources and as sources. An artifact type describes the semantic meaning of an artifact, e.g. a Helm chart.

Below you can find a table with all current artifact types of the core model. More detailed information, including the attribute specification can be found [here](../04-extensions/01-artifact-types/README.md) and behind the links in the table.

| TYPE NAME                                     | DESCRIPTION                                                                                                                                |
|-----------------------------------------------|--------------------------------------------------------------------------------------------------------------------------------------------|
| [`blob`](../04-extensions/01-artifact-types/blob.md)                               | A blob represents any data without a dedicated logical type                             |
| [`directoryTree`, `fileSystem`](../04-extensions/01-artifact-types/file-system.md) | Files from a file system (e.g. *tar* or *tgz* archive)    |
| [`gitOpsTemplate`](../04-extensions/01-artifact-types/gitops.md)                   | Filesystem content (tar, tgz) used as GitOps Template, e.g. to set up GitOps using FluxCD |
| [`helmChart`](../04-extensions/01-artifact-types/helmchart.md)                     | A Helm Chart stored as OCI artifact or as tar blob (`mediaType` tar) |
| [`npmPackage`](../04-extensions/01-artifact-types/npm.md)                          | A Node Package Manager [npm](https://www.npmjs.com) archive |
| [`ociArtifact`](../04-extensions/01-artifact-types/oci-artifact.md)                | A generic OCI artifact following the [open containers image specification](https://github.com/spec/blob/main/spec.md) |
| [`ociImage`](../04-extensions/01-artifact-types/oci-image.md)                      | An OCI image or image list  |
| [`executable`](../04-extensions/01-artifact-types/executable.md)                   | A blob describing an executable program |
| [`sbom`](../04-extensions/01-artifact-types/sbom.md)                               | A list of ingredients that make up software components (https://www.cisa.gov/sbom) |

Some additional types are defined, but not part of the core specification. Support is optional, but the list of names is reserved.

| TYPE NAME          |DESCRIPTION                          |
|--------------------|-------------------------------------|
| [`blueprint`](../04-extensions/01-artifact-types/blueprint.md)                   | An installation description for the [landscaper](https://github.com/gardener/landscaper)           |
| [`toiExecutor`](../04-extensions/01-artifact-types/toiexecutor.md)               | A toolset for simple installation in the [OCM CLI](https://github.com/open-component-model/ocm/blob/cm_toi.md) installation environment.    |
| [`toiPackage`](../04-extensions/01-artifact-types/toipackackage.md)              | A YAML resource describing the installation for the [OCM CLI](https://github.com/open-component-model/ocm/blob/main/docs/reference/ocm_toi.md) TOI installation. |


## Access Method Types

Access methods are used to access the content of artifacts described by a component version. Every access method has an access method type.
All access method types are used for **resource** as well as **source** elements.  

The type of the access methods defines the access procedure and the access specification format used to provide the appropriate attributes
required to identify the blob and its location.

The following access method types are centrally defined. This list can be extended by custom types or by later extensions of the specification.
More detailed information, including the attribute specification can be found [here](../04-extensions/02-access-types/README.md)
and behind the links in the table.

| TYPE NAME | DESCRIPTION |
|---------------------------------|-----------------------------------------------------|
| [`localBlob`](localblob.md)     | An artifact stored along with the component version |
| [`ociArtifact`](ociartifact.md) | An artifact in a repository of an OCI registry      |
| [`ociBlob`](ociblob.md)         | A blob in a repository of an OCI registry           |
| [`helm`](helm.md)               | A Helm chart stored in a Helm Repository            |
| [`gitHub`](github.md)           | A commit in a GitHub-based Git repository           |
| [`s3`](s3.md)                   | A blob stored in an AWS S3 bucket                   |
| [`npm`](npm.md)                 | A NodeJS package stored in an NPM repository        |         


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

## `jsonNormalisationV1` vs `jsonNormalisationV2`

The `JsonNormalisationV1` serialization format is based on the serialization format of the component descriptor. It uses an appropriate JSON object containing the relevant fields as contained in the component descriptors's serialization. The format version fields are included. Therefore, the normalized form is depending on the chosen serialization format. Changing this format version would result in different digests. The resulting JSON object is serialized with the [OCM specific scheme](#generic-normalization-format)

`JsonNormalisationV2` strictly uses only the relevant component descriptor
information according to the field specification. It is independent of the serialization format used to store the component decsriptor in some storage backend. Therefore, the calculated digest is finally independent of the serialization format chosen for storing the component descriptor in a storage backend. It uses a standard scheme according to [RFC8785 (JCS)](https://www.rfc-editor.org/rfc/rfc8785)


# Digest Algorithms

Digest algorithms describe the way digests are calculated from a byte stream.

The following digest algorithms are defined:

- `SHA-256`
- `SHA-512`

## Digesting Content
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

After the digest for the normalised component-descriptor is calculated, it can be

signed using RSASSA-PKCS1-V1_5 as signature.algorithm. The corresponding signature is stored hex encoded in `signature.value` with a `mediaType` of
`application/vnd.ocm.signature.rsa`.
