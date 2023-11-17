# Access Method Types

Access methods are used to access the content of artifacts described by a component version. Every access method has an access method type.
All access method types are used for **resource** as well as **source** elements.  

The type of the access methods defines the access procedure and the access specification format used to provide the appropriate attributes
required to identify the blob and its location.

The following access method types are centrally defined:

| TYPE NAME | DESCRIPTION |
|-----------|-------------|
| [`localBlob`](localblob.md)     | an artifact stored along with the component version |
| [`ociArtifact`](ociartifact.md) | an artifact in a repository of an OCI registry      |
| [`ociBlob`](ociblob.md)         | a blob in a repository of an OCI registry           |
| [`helm`](helm.md)               | a Helm chart stored in a Helm Repository            |
| [`gitHub`](github.md)           | a commit in a GitHub-based Git repository           |
| [`s3`](s3.md)                   | a blob stored in an AWS S3 bucket                   |
| [`npm`](npm.md)                 | a NodeJS package stored in an NPM repository        |            