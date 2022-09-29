# 2.1 Common Transport Format (CTF)

# Introduction

The purpose of the transport format is to transfer
components between locations optionally including all their
references. Based on a file-system it can be used to transport
content without direct internet access. A tar file of this file
structure will be called the transport archive of the OCI artifacts.
If offline access is not required the CTF can also be stored
in an OCI registry as an additional repository view. You can transport between any kind of repository
view as source and sink:

```
    CTF -> OCI
    OCI -> CTF
    CTF -> CTF
    OCI -> OCI
    <any supported type> -> <any supported type>
```


There are three different technical flavors:

- `directory`: the content is stored directly as a directory tree
- `tar`: the directory tree is stored in a tar archive
- `tgz`: the directory tree is stored in a zipped tar archive

All those technical representations use the same file formats and directory structure. The containing directory is not part of the tar file

# Format

The common transport format is described in detail in the [Appendix Common Transport Format](../../appendix/common/formatspec.md)

(../appendix/common/formatspec.md)

## Component Descriptor of a Transport Archive
When a transport between a source and a destination repository happens the component descriptor gets
converted. A transport can happen in multiple variants:

* plain
* including closure (will include all references attached as local resources)
* with values (will include all resources that point to external location, e.g. OCI images)

The options with closure and with values can be combined. Only with this combination it is ensured
that the target system has included all resources for offline scenarios.

## Transport Format for Other Resource Types

Whenever a new resource type is supported, a corresponding transport format must be defined.

# Example

## Example with Closure and by Values

Here is an example of a transport archive containing two artifacts and a reference. See the component-descriptor below for details. The transport archive was created locally in the file system, then transferred to an OCI registry containg the closure (including all resources and references)
and copying the references by value. Then it was signed and transferred backto the local file system.

File System Structure:

```shell
.
├── artefact-index.json
└── blobs
    ├── sha256.059604bdee64629c3fa1a59b9df2f652055d9e466572b16ac85f57fd431c084f # config echo-server
    ├── sha256.45d6ac13fac76c36758497b6e1ca146a85789c21ff83e7d2f3aa15bba32751ae # component descriptor echo-server
    ├── sha256.604a9c317c832a4fd903192ca12a519dcb932e58ce167c8763ea36250eac9404 # image manifest echo-server
    ├── sha256.635f6c518783a6f1003cf26eee0b3fc89807478cbc7bc850ee1f5df7e99968db # container image echo-server
    ├── sha256.946ffdc3d823f76d07b5f9fa7e0d4b3be6617316cad4e88a17aa229c5ade1640 # helm chart echo-server as tar archive
    ├── sha256.a58194a0a291ad66fe415d3591198d0f3fe33280b7fd3c62d23101190c956007 # config referenced component nginx-controller
    ├── sha256.9dcab5b0ef34267199941e9632952fd5d35b3d392d1c6a84ad8327adb3d76f7e # component descriptor referenced component nginx-controller
    ├── sha256.93e5c216753c6343eafef81d34f0a49fac4b4884728ad472d4b1739a26d81ddf # image manifest referenced component nginx-controller
    ├── sha256.0efef9e1a323b925fe98ef1c0c03df99b7df597a7fe40981569cb34fd73e1289 # container image referenced component nginx-controller
    └── sha256.26f5894c0082232959daf2bea30af474b02ae385be28ed219b52987819a9b1e4 # helm-chart referenced component nginx-controller
```

`artefact-index.json`:

```json
{
  "schemaVersion": 1,
  "artefacts": [
    {
      "repository": "component-descriptors/github.com/jensh007/ocmechoserver",
      "tag": "0.1.0-dev",
      "digest": "sha256:604a9c317c832a4fd903192ca12a519dcb932e58ce167c8763ea36250eac9404"
    },
    {
      "repository": "component-descriptors/github.com/jensh007/ocmnginx-ingress-controller",
      "tag": "0.1.0-dev",
      "digest": "sha256:93e5c216753c6343eafef81d34f0a49fac4b4884728ad472d4b1739a26d81ddf"
    }
  ]
}
```

Image-Manifest of echoserver in `blobs/sha256.604a9c317c832a4fd903192ca12a519dcb932e58ce167c8763ea36250eac9404`:

```json
{
  "schemaVersion": 2,
  "mediaType": "application/vnd.oci.image.manifest.v1+json",
  "config": {
    "mediaType": "application/vnd.gardener.cloud.cnudie.component.config.v1+json",
    "digest": "sha256:059604bdee64629c3fa1a59b9df2f652055d9e466572b16ac85f57fd431c084f",
    "size": 210
  },
  "layers": [
    {
      "mediaType": "application/vnd.gardener.cloud.cnudie.component-descriptor.v2+yaml+tar",
      "digest": "sha256:45d6ac13fac76c36758497b6e1ca146a85789c21ff83e7d2f3aa15bba32751ae",
      "size": 4096
    },
    {
      "mediaType": "application/vnd.oci.image.manifest.v1+tar+gzip",
      "digest": "sha256:946ffdc3d823f76d07b5f9fa7e0d4b3be6617316cad4e88a17aa229c5ade1640",
      "size": 4647
    },
    {
      "mediaType": "application/vnd.docker.distribution.manifest.v2+tar+gzip",
      "digest": "sha256:635f6c518783a6f1003cf26eee0b3fc89807478cbc7bc850ee1f5df7e99968db",
      "size": 46146624
    }
  ]
}
```

Image-Manifest of referenced component nginx-controller in `blobs/sha256.93e5c216753c6343eafef81d34f0a49fac4b4884728ad472d4b1739a26d81ddf`:

```json
{
  "schemaVersion": 2,
  "mediaType": "application/vnd.oci.image.manifest.v1+json",
  "config": {
    "mediaType": "application/vnd.gardener.cloud.cnudie.component.config.v1+json",
    "digest": "sha256:a58194a0a291ad66fe415d3591198d0f3fe33280b7fd3c62d23101190c956007",
    "size": 210
  },
  "layers": [
    {
      "mediaType": "application/vnd.gardener.cloud.cnudie.component-descriptor.v2+yaml+tar",
      "digest": "sha256:9dcab5b0ef34267199941e9632952fd5d35b3d392d1c6a84ad8327adb3d76f7e",
      "size": 4096
    },
    {
      "mediaType": "application/vnd.oci.image.manifest.v1+tar+gzip",
      "digest": "sha256:26f5894c0082232959daf2bea30af474b02ae385be28ed219b52987819a9b1e4",
      "size": 28527
    },
    {
      "mediaType": "application/vnd.docker.distribution.manifest.v2+tar+gzip",
      "digest": "sha256:0efef9e1a323b925fe98ef1c0c03df99b7df597a7fe40981569cb34fd73e1289",
      "size": 41792324
    }
  ]
}
```

Component-Descriptor (untared with `tar -xOf blobs/sha256.45d6ac13fac76c36758497b6e1ca146a85789c21ff83e7d2f3aa15bba32751ae`):

```yaml
meta:
  schemaVersion: v2
component:
  name: github.com/jensh007/ocmechoserver
  provider: jensh007
  repositoryContexts:
  - baseUrl: ghcr.io
    componentNameMapping: urlPath
    subPath: jensh007/ocm
    type: OCIRegistry
  componentReferences:
  - componentName: github.com/jensh007/ocmnginx-ingress-controller
    digest:
      hashAlgorithm: sha256
      normalisationAlgorithm: jsonNormalisation/v1
      value: e9440ed669e5a832ce927ab0ea25dab8f02b2bdd7da14872f2750a3392d7208a
    name: nginx-ingress-controller
    version: 0.1.0-dev
  resources:
  - access:
      localReference: sha256:946ffdc3d823f76d07b5f9fa7e0d4b3be6617316cad4e88a17aa229c5ade1640
      mediaType: application/vnd.oci.image.manifest.v1+tar+gzip
      referenceName: github.com/jensh007/ocmechoserver/echoserver:0.1.0
      type: localBlob
    digest:
      hashAlgorithm: sha256
      normalisationAlgorithm: ociArtifactDigest/v1
      value: aa86f3b3547ccb075ab3dcebce7177115017771876df685b0f487d97f37d816f
    name: chart
    relation: local
    type: helmChart
    version: 0.1.0-dev
  - access:
      localReference: sha256:635f6c518783a6f1003cf26eee0b3fc89807478cbc7bc850ee1f5df7e99968db
      mediaType: application/vnd.docker.distribution.manifest.v2+tar+gzip
      referenceName: google_containers/echoserver:1.10
      type: localBlob
    digest:
      hashAlgorithm: sha256
      normalisationAlgorithm: ociArtifactDigest/v1
      value: cb5c1bddd1b5665e1867a7fa1b5fa843a47ee433bbb75d4293888b71def53229
    name: image
    relation: external
    type: ociImage
    version: "1.0"
  sources: []
  version: 0.1.0-dev
signatures:
- digest:
    hashAlgorithm: sha256
    normalisationAlgorithm: jsonNormalisation/v1
    value: 78798e15be6f56e08bc3d519b1dcc0df875bde0014848a362fb68187d146c98e
  name: mysig
  signature:
    algorithm: RSASSA-PKCS1-V1_5
    mediaType: application/vnd.ocm.signature.rsa
    value: 6ba56c64d7e576f663131eaab35f3001decf1ca71998de9c097b26c8ccd72f1203cc4c8725b6a7e20c0e225b434f3a26acf5ed817c8f4075600d902b05d88ad62e302394f79e1f25eec830458f632e842d2895cb5cfa3337d62a8f6adf9226ddbdb26905b6f26cd108d3e2b474c07764ac56f38cabcf263d91ed55e6b3855bb1b073b4b9a91483dc0cb7799ed6ff7cc51af3a2b83c8ffdb80091284968d2b061f26261b82eb8ddd29a8f45dd079f0a414741d07a05f062cd5866860d4c502c37495f1059ea973f5fd342f40d6603cf41df2c31153e00d5e0ea804a7366b5c7e4ff28ad721ce23b57d27d584234871949c22fcce4ba5b2146eb44895f7d104b67
```

## Example without Closure and Values

```
.
├── artefact-index.json
└── blobs
    ├── sha256.0073ee2eefae1e8ba4e428b7a34e7beb5969ad47bb0056ad7b4a9897c0596387
    ├── sha256.7478db0eed5181f5cd93583be77a9d368627a91b7698c4594a1485aae425161c
    └── sha256.c92b4ca340fcc7d7750968dd465b8ab94d9e536a3ad073fe944d815ec0d9c85a
```

`blobs/sha256.0073ee2eefae1e8ba4e428b7a34e7beb5969ad47bb0056ad7b4a9897c0596387`:

```
{
  "schemaVersion": 2,
  "mediaType": "application/vnd.oci.image.manifest.v1+json",
  "config": {
    "mediaType": "application/vnd.gardener.cloud.cnudie.component.config.v1+json",
    "digest": "sha256:7478db0eed5181f5cd93583be77a9d368627a91b7698c4594a1485aae425161c",
    "size": 210
  },
  "layers": [
    {
      "mediaType": "application/vnd.gardener.cloud.cnudie.component-descriptor.v2+yaml+tar",
      "digest": "sha256:c92b4ca340fcc7d7750968dd465b8ab94d9e536a3ad073fe944d815ec0d9c85a",
      "size": 2560
    }
  ]
}
```

untared `blobs/sha256.c92b4ca340fcc7d7750968dd465b8ab94d9e536a3ad073fe944d815ec0d9c85a`:

```
component:
  componentReferences:
  - componentName: github.com/jensh007/ocmnginx-ingress-controller
    name: nginx-ingress-controller
    version: 0.1.0-dev
  name: github.com/jensh007/ocmechoserver
  provider: jensh007
  repositoryContexts:
  - baseUrl: ghcr.io
    componentNameMapping: urlPath
    subPath: jensh007/ocm
    type: OCIRegistry
  resources:
  - access:
      imageReference: ghcr.io/jensh007/ocm/github.com/jensh007/ocmechoserver/echoserver:0.1.0
      type: ociArtefact
    name: chart
    relation: local
    type: helmChart
    version: 0.1.0-dev
  - access:
      imageReference: gcr.io/google_containers/echoserver:1.10
      type: ociArtefact
    name: image
    relation: external
    type: ociImage
    version: "1.0"
  sources: []
  version: 0.1.0-dev
meta:
  schemaVersion: v2
```

## Example with Closure and without Values

The tranport archive contains the referenced component but keeps the image references.

`artefact-index.json`:

```
{
  "schemaVersion": 1,
  "artefacts": [
    {
      "repository": "component-descriptors/github.com/jensh007/ocmechoserver",
      "tag": "0.1.0-dev",
      "digest": "sha256:0073ee2eefae1e8ba4e428b7a34e7beb5969ad47bb0056ad7b4a9897c0596387"
    },
    {
      "repository": "component-descriptors/github.com/jensh007/ocmnginx-ingress-controller",
      "tag": "0.1.0-dev",
      "digest": "sha256:7a6ea0040f60d7479c0d73a1854f75cecdc061dd1d6573178d2c1318e6a72d72"
    }
  ]
}
```

`blobs/sha256.0073ee2eefae1e8ba4e428b7a34e7beb5969ad47bb0056ad7b4a9897c0596387`:

```json
{
  "schemaVersion": 2,
  "mediaType": "application/vnd.oci.image.manifest.v1+json",
  "config": {
    "mediaType": "application/vnd.gardener.cloud.cnudie.component.config.v1+json",
    "digest": "sha256:7478db0eed5181f5cd93583be77a9d368627a91b7698c4594a1485aae425161c",
    "size": 210
  },
  "layers": [
    {
      "mediaType": "application/vnd.gardener.cloud.cnudie.component-descriptor.v2+yaml+tar",
      "digest": "sha256:c92b4ca340fcc7d7750968dd465b8ab94d9e536a3ad073fe944d815ec0d9c85a",
      "size": 2560
    }
  ]
}
```

untared `blobs/sha256.c92b4ca340fcc7d7750968dd465b8ab94d9e536a3ad073fe944d815ec0d9c85a`:

```yaml
component:
  componentReferences:
  - componentName: github.com/jensh007/ocmnginx-ingress-controller
    name: nginx-ingress-controller
    version: 0.1.0-dev
  name: github.com/jensh007/ocmechoserver
  provider: jensh007
  repositoryContexts:
  - baseUrl: ghcr.io
    componentNameMapping: urlPath
    subPath: jensh007/ocm
    type: OCIRegistry
  resources:
  - access:
      imageReference: ghcr.io/jensh007/ocm/github.com/jensh007/ocmechoserver/echoserver:0.1.0
      type: ociArtefact
    name: chart
    relation: local
    type: helmChart
    version: 0.1.0-dev
  - access:
      imageReference: gcr.io/google_containers/echoserver:1.10
      type: ociArtefact
    name: image
    relation: external
    type: ociImage
    version: "1.0"
  sources: []
  version: 0.1.0-dev
meta:
  schemaVersion: v2
```

## Example with values but without closure
The transport archive contains the images but not the references.

```shell
.
├── artefact-index.json
└── blobs
    ├── sha256.1a7c73d2c4b917ed15e952332da0e8539835d78367d4f5cbd333e352cd2660d9
    ├── sha256.635f6c518783a6f1003cf26eee0b3fc89807478cbc7bc850ee1f5df7e99968db
    ├── sha256.8d57a47239f3bcc5f57004cbbb7fa4adb564394a9e1ab24e149adfa8dc4a18d2
    ├── sha256.a65c18e99955206e8034806c51969673ec089ec5046bae50a6a4836b63dd6818
    └── sha256.dd478c9b80ba7d253f95bb7c68989fa44fa1a5227da6e71efc000e0e92837d8e
```

`artefact-index.json`:

```json
{
  "schemaVersion": 1,
  "artefacts": [
    {
      "repository": "component-descriptors/github.com/jensh007/ocmechoserver",
      "tag": "0.1.0-dev",
      "digest": "sha256:dd478c9b80ba7d253f95bb7c68989fa44fa1a5227da6e71efc000e0e92837d8e"
    }
  ]
}
```

`blobs/sha256.dd478c9b80ba7d253f95bb7c68989fa44fa1a5227da6e71efc000e0e92837d8e`:`

```json
{
  "schemaVersion": 2,
  "mediaType": "application/vnd.oci.image.manifest.v1+json",
  "config": {
    "mediaType": "application/vnd.gardener.cloud.cnudie.component.config.v1+json",
    "digest": "sha256:1a7c73d2c4b917ed15e952332da0e8539835d78367d4f5cbd333e352cd2660d9",
    "size": 210
  },
  "layers": [
    {
      "mediaType": "application/vnd.gardener.cloud.cnudie.component-descriptor.v2+yaml+tar",
      "digest": "sha256:8d57a47239f3bcc5f57004cbbb7fa4adb564394a9e1ab24e149adfa8dc4a18d2",
      "size": 3072
    },
    {
      "mediaType": "application/vnd.oci.image.manifest.v1+tar+gzip",
      "digest": "sha256:a65c18e99955206e8034806c51969673ec089ec5046bae50a6a4836b63dd6818",
      "size": 4639
    },
    {
      "mediaType": "application/vnd.docker.distribution.manifest.v2+tar+gzip",
      "digest": "sha256:635f6c518783a6f1003cf26eee0b3fc89807478cbc7bc850ee1f5df7e99968db",
      "size": 46146624
    }
  ]
}
```

untared `blobs/sha256.8d57a47239f3bcc5f57004cbbb7fa4adb564394a9e1ab24e149adfa8dc4a18d2`:

```yaml:
component:
  componentReferences:
  - componentName: github.com/jensh007/ocmnginx-ingress-controller
    name: nginx-ingress-controller
    version: 0.1.0-dev
  name: github.com/jensh007/ocmechoserver
  provider: jensh007
  repositoryContexts:
  - baseUrl: ghcr.io
    componentNameMapping: urlPath
    subPath: jensh007/ocm
    type: OCIRegistry
  resources:
  - access:
      localReference: sha256:a65c18e99955206e8034806c51969673ec089ec5046bae50a6a4836b63dd6818
      mediaType: application/vnd.oci.image.manifest.v1+tar+gzip
      referenceName: github.com/jensh007/ocmechoserver/echoserver:0.1.0
      type: localBlob
    name: chart
    relation: local
    type: helmChart
    version: 0.1.0-dev
  - access:
      localReference: sha256:635f6c518783a6f1003cf26eee0b3fc89807478cbc7bc850ee1f5df7e99968db
      mediaType: application/vnd.docker.distribution.manifest.v2+tar+gzip
      referenceName: google_containers/echoserver:1.10
      type: localBlob
    name: image
    relation: external
    type: ociImage
    version: "1.0"
  sources: []
  version: 0.1.0-dev
meta:
  schemaVersion: v2
```

# Specification Versions

##Version `v1`

The type specific specification fields are:

- **`filePath`** *string*

  The path in the filesystem used to store the content

- **`fileFormat`** *string*

  The file format to use:
  - `directory`: stored as file hierarchy in a directory
  - `tar`: stored as file hierarchy in a TAR file
  - `tgz`: stored as file hierarchy in a GNU-zipped TAR file (tgz)

- **`accessMode`** (optional) *byte*

  Access mode used to access the content:
  - 0: write access
  - 1: read-only
  - 2: create id not existent, yet