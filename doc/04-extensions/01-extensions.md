# Extensible Field Values

The core specification does not rely on a fixed set of certain field. However the specification defines a set of known values listed in the following sections. These sets can be extended by new specification versions, addendums or for customer-specific environments.


## Resource Types

| TYPE               | VALUE                                         | DESCRIPTION                                                                                                                                |
|--------------------|-----------------------------------------------|--------------------------------------------------------------------------------------------------------------------------------------------|
| Blob               | [`blob`](#blobd)                             | Any anonymous untyped blob data                                                                                                            |
| Filesystem Content | [`filesystem` `directoryTree`](#file-system) | Files from a file system (typically provided by a *tar* or *tgz* archive). The mime type of the blob specifies the concrete format.              |
| GitOps             | [`gitOpsTemplate`](#file-system)         | Filesystem content (tar, tgz) used as GitOps Template, e.g. to set up a git repo used for continuous deployment (for example flux)         |
| Helm Chart         | [`helmChart`](#helm-chart)                   | A Helm Chart stored as OCI artifact or as tar blob (`mediaType` tar)                                                                       |
| Node Package Manager | [`npm`](npm.md)                             | A Node Package Manager [npm](https://www.npmjs.com) archive |
| OCI Artifact       | [`ociArtifact`](#oci-artifact)               | A generic OCI artifact following the [open containers image specification](https://github.com/opencontainers/image-spec/blob/main/spec.md) |
| OCI Image          | [`ociImage`](#oci-image)                     | An OCI image or image list                                                                                                                 |

The following additional types are defined but not part of the core specification. Support is optional, but the list of names is reserved.

| TYPE               | VALUE                                         | DESCRIPTION                                                                                                                                |
|--------------------|-----------------------------------------------|--------------------------------------------------------------------------------------------------------------------------------------------|
| Blueprint          | [`blueprint`](blueprint.md)                   | An installation description for the [landscaper](https://github.com/gardener/landscaper) installation environment.                         |
| TOI Executor       | [`toiExecutor`](toiExecutor.md)               | A toolset for simple installation in the [OCM CLI](https://github.com/open-component-model/ocm/blob/main/docs/reference/ocm_toi.md) installation environment.    |
| TOI Package        | [`toiPackage`](toiPackackage.md)              | A YAML resource describing the installation for the [OCM CLI](https://github.com/open-component-model/ocm/blob/main/docs/reference/ocm_toi.md) TOI installation. |

#### Blob

- **`blob`**

A blob represents any data without a dedicated logical type.

The media type is used to define the logical and/or technical format of the byte-stream represented by the blob

#### File System

- **`filesystem`**
- **`directoryTree`**

Filesystem content represented in tar format.

The media type SHOULD be application/x-tar or for content compressed with GNU Zip application/gzip, application/x-gzip, application/x-gtar, and application/x-tgz or application/x-tar+gzip.

#### GitOps

- **`gitOpsTemplate`**

A filesystem content intended to be used as Git Opts Template. Such an artifact should be used in a sequence of successive versions that can be used by a 3-way merge to be merged with an instance specific Git Ops Repository content (for example via GitHub Pull Requests).

#### Helm Chart

- **`helmChart`**

A Kubernetes installation resource representing a Helm chart, either stored as OCI artifact or as tar blob.

Format Variants:

- *OCI Artifact*

  If stored as OCI artifact, the access type MUST either be
  `ociArtifact` or the [OCI artifact blob format](ociArtifact.md#format-variants) must be
  used with an appropriate media type.

- *Helm Tar Archive*

  If stored in the Helm tar format (for the filesystem),
  the tar media type MUST be used.

Special Support

There is a dedicated downloader available, that always converts the helm chart blob into the appropriate filesystem representation required by Helm when downloading the artifact using the command line interface.

#### npm

- **`npm`**

A Node Package Manager ([npm](https://www.npmjs.com)) archive that is located in an npm registry. By default npm packages use the npm public registry at https://registry.npmjs.org.

#### OCI Artifact

- **`helmChart`**

Format Variants:

When provided as a blob, the [Artifact Set Format](../common/formatspec.md#artifact-set-archive-format)
MUST be used to represent the content of the OCI artifact.
THis format can be used to store multiple versions of on OCI repository
in a filesystem-compatible manner. In this scenario only the
single version of interest is stored.

Provided blobs use the following media type:

- `application/vnd.oci.image.manifest.v1+tar+gzip`: OCI image manifests
- `application/vnd.oci.image.index.v1+tar.gzip`: OCI index manifests

Special Support:

There is a dedicated uploader available for local blobs. It converts a blob with the media type shown above into a regular OCI artifact in an OCI repository.

It uses the reference hint attribute of the [`localBlob` access method](#localblob) to determine an appropriate OCI repository. If the import target of the OCM component version is an OCI registry, by default, the used OCI repository will be the base repository of the [OCM mapping](../04-persistence/01-mappings.md#mappings-for-ocm-persistence) with the appended reference hint.

#### OCI Image

- **`helmChart`**

This type describes an OCI artifact containing an OCI container image.

A general [ociArtifact](#oci-artifact) describes any kind of content, depending on the media type of its config blob.

`ociImage` is a dedicated variant for the container image media types.

Format Variants:

As special case for a general `ociArtifact` is uses the `ociArtifact` blob format.

Special Support:

As special case for a general `ociArtifact` it uses the `ociArtifact` special support.

#### Reserved Types

The following artifact types are reserved:

- **`blueprint`**
- **`toiExecutor`**
- **`toiPackage`**

## Source Types

The following list of artifact types is defined as part of the OCM specification. This list can be extended by user-defined custom types or by later versions of the OCM specification.

| TYPE               | VALUE        | DESCRIPTION                           |
|--------------------|--------------|---------------------------------------|
| Github sources     | `github`     | Sources in Git or Github repositories |

## Access Types

The following access types are defined in the core model. This list can be extended by custom access methods or by later extensions of the specification:

---
#### gitHub

Access to a commit in a Git repository.

*Synopsis:*
```
type: gitHub/v1
```

*Media type for blobs*

`application/x-tgz`

The artifact content is provided as g-zipped tar archive

*Specification Versions*

Supported specification version is `v1`

*Attributes*


- **`repoUrl`**  *string*

  Repository URL with or without scheme.

- **`ref`** (optional) *string*

  Original ref used to get the commit from

- **`commit`** *string*

  The sha/id of the git commit

---
#### helm

Access to a Helm chart in a Helm repository.

*Synopsis:*
```
type: helm/v1
```
*Specification Versions*

Supported specification version is `v1`

*Attributes*

- **`helmRepository`** *string*

  Helm repository URL.

- **`helmChart`** *string*

  The name of the Helm chart and its version separated by a colon.

- **`caCert`** *string*

  An optional TLS root certificate.

- **`keyring`** *string*

  An optional keyring used to verify the chart.

---
#### localBlob

Access to a resource blob stored along with the component descriptor.

It's implementation of an OCM repository type how to read the component descriptor. Every repository implementation may decide how and where local blobs are stored, but it MUST provide an implementation for this access method.

*Synopsis:*

```
type: localBlob/v1
```

*Attributes*

- **`localReference`** *string*

  Repository type specific location information as string. The value
  may encode any deep structure, but typically an access path is sufficient.

- **`mediaType`** *string*

  The media type of the blob used to store the resource. It may add
  format information like `+tar` or `+gzip`.

- **`referenceName`** (optional) *string*

  This optional attribute may contain identity information used by other repositories to restore some global access with an identity related to the original source.

  For example, an OCI artifact originally referenced using the access method `ociArtifact` is stored during a transport as local artifact. The reference name can then be set to its original repository name. An import step into an OCI repository may then decide to makethis artifact available again as regular OCI artifact using this attribute.

- **`globalAccess`** (optional) *access method specification*

  If a resource blob is stored locally, the repository implementation may decide to provide an external access information (usable by non OCM-aware tools). For example, an OCI artifact stored as local blob can be additionally stored as regular OCI artifact in an OCI registry.

  This additional external access information can be added using a second external access method specification.

---
#### npm

Access to an NodeJS package in an NPM registry.

*Synopsis:*
```
type: npm/v1
```
*Specification Versions*

Supported specification version is `v1`

*Attributes*

- **`registry`** *string*

  Base URL of the NPM registry.

- **`package`** *string*

  Name of the NPM package.

- **`version`** *string*

  Version name of the NPM package.

---
#### ociArtifact

Access of an OCI artifact stored in an OCI registry.

*Synopsis:*

```
type: ociArtifact/v1
```

*Media type for blobs*

- `application/vnd.oci.image.manifest.v1+tar+gzip`: OCI image manifests
- `application/vnd.oci.image.index.v1+tar.gzip`: OCI index manifests

Depending on the repository appropriate docker legacy types might be used.

*Attributes*

- **`imageReference`** *string*

  OCI image/artifact reference following the possible docker schemes:
    - `<repo>/<artifact>:<digest>@<tag>`
    - `<host>[<port>]/repo path>/<artifact>:<version>@<tag>`


---

#### ociBlob

Access of an OCI blob stored in an OCI repository.

*Synopsis:*
```
type: ociBlob/v1
```
*Specification Versions*

Supported specification version is `v1`

*Attributes*

- **`imageReference`** *string*

  OCI repository reference (this artifact name used to store the blob).

- **`mediaType`** *string*

  The media type of the blob

- **`digest`** *string*

  The digest of the blob used to access the blob in the OCI repository.

- **`size`** *integer*

  The size of the blob

---
#### s3

Access to a blob stored in an S3 API compatible bucket.

*Synopsis:*
```
type: s3/v1
```
*Specification Versions*

Supported specification version is `v1`

*Attributes*

- **`region`** (optional) *string*

  region identifier of the used store

- **`bucket`** *string*

  The name of the S3 bucket containing the blob

- **`key`** *string*

  The key of the desired blob

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

# Storage Backends
