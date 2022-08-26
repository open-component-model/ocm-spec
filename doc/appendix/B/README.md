# B.  Access Method Types

[Access methods](../../specification/elements/README.md#artifact-access)
are used to access the content of artefacts described
by a [component version](../../specification/elements/README.md#component-versions).
The [type](../../specification/formats/types.md#access-method-types)
of the methods defines the access procedure and the
[access specification](../../specification/formats/formats.md#access-specifications)
format used to provide the appropriate attributes
required to identity the blob and its location.

The following access method types are centrally defined:

- [localBlob](localBlob.md) an artefact stored along with the component version
- [ociArtefact](ociArtefact.md) an artefact in a repository of an OCI registry
- [ociBlob](ociBlob.md) a blob in a repository of an OCI registry
- [gitHub](gitHub.md) a GitHub commit
- [s3](s3.md) a blob stored in an AWS S3 bucket
