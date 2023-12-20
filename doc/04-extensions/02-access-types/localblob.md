# localBlob — Blob Hosted in OCM Repository

## Synopsis
```
type: localBlob/[VERSION]
[ATTRIBUTES]
```

## Description

Access to a resource blob stored along with the component descriptor.

It's implementation of an OCM repository type how to read the component descriptor. Every repository implementation may decide how and where local blobs are stored, but it MUST provide an implementation for this access method.

The concrete implementation MUST be provided by the storage backend used to store the component version. All storage backends MUST use the same attribute set. The field `localReference` MAY have a storage backend specific representation for the location information in the backend. It MUST contain the information required by the backend
to access the blob. For example, for an OCI registry backend the `localReference` contains the SHA of the blob used to store the blob as layer in the same OCI artifact
as the component descriptor.

## Supported Media Types

The provided media type is taken from the specification attribute `mediaType`.

## Specification Version

The following versions are supported

### v1

Attributes:

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


