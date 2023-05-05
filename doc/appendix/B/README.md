# B.  Access Method Types

[Access methods](../../specification/elements/README.md#artifact-access)
are used to access the content of artifacts described
by a [component version](../../specification/elements/README.md#component-versions).
The [type](../../specification/formats/types.md#access-method-types)
of the methods defines the access procedure and the
[access specification](../../specification/formats/formats.md#access-specifications)
format used to provide the appropriate attributes
required to identity the blob and its location.

The following access method types are centrally defined:

- [localBlob](localBlob.md) an artifact stored along with the component version
- [ociArtifact](ociArtifact.md) an artifact in a repository of an OCI registry
- [ociBlob](ociBlob.md) a blob in a repository of an OCI registry
- [helm](helm.md) a Helm chart stored in a Helm Repository
- [gitHub](gitHub.md) a commit in a GitHub-based Git repository
- [s3](s3.md) a blob stored in an AWS S3 bucket
