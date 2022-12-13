<!-- omit in toc -->
# Getting Started

This chapter walks you through some basic steps to get started with OCM concepts and the OCM CLI.

- [Prerequisites](#prerequisites)
- [Create a component version](#create-a-component-version)
  - [Create a component archive](#create-a-component-archive)
  - [Add a local resource](#add-a-local-resource)
  - [Add an image reference](#add-an-image-reference)
  - [Add an image resource](#add-an-image-resource)
  - [Using a resources file](#using-a-resources-file)
  - [Uploading component versions](#uploading-component-versions)
  - [Bundle composed components](#bundle-composed-components)
- [Display and Examine component versions](#display-and-examine-component-versions)
  - [List component versions](#list-component-versions)
  - [List the resources of a component version](#list-the-resources-of-a-component-version)
  - [Download the resources of a component version](#download-the-resources-of-a-component-version)
    - [Download with download handlers](#download-with-download-handlers)
    - [Download an image](#download-an-image)
    - [Download an executable](#download-an-executable)
    - [Download a full component version](#download-a-full-component-version)
  - [Download OCI Artifacts](#download-oci-artifacts)
- [Transport OCM component versions](#transport-ocm-component-versions)
- [Sign component versions](#sign-component-versions)
  - [Signing with certificates](#signing-with-certificates)
  - [Signature Verification](#signature-verification)

## Prerequisites

To follow the steps described in this section, you will need:

- The OCM Command Line Interface (CLI) to interact with component versions and registries. Download it from the [releases](https://github.com/open-component-model/ocm/releases) or with the following command:
  ```shell
  curl -L https://github.com/open-component-model/ocm/releases/download/v0.1.0-alpha.1/ocm-linux-amd64.tgz -o - | tar -xz; mv ocm* ocm
  ```
- Access to an OCM repository. This can be any OCI registry for which you have write permission (e.g. GitHub Packages). An OCM repository based on an OCI registry is identified by a leading OCI repository prefix. For example: `ghcr.io/<YOUR-ORG>/ocm`.
- Credentials for the CLI to access the OCM repository. The easiest way to do this is to reuse the Docker configuration.

  To do this, create a file named <a href='.ocmconfig'>`.ocmconfig`</a> in your home directory with the following:

  ```yaml
  type: generic.config.ocm.software/v1
  configurations:
  - type: credentials.config.ocm.software
    repositories:
      - repository:
          type: DockerConfig/v1
          dockerConfigFile: "~/.docker/config.json"
          propagateConsumerIdentity: true
  - type: attributes.config.ocm.software
    attributes:
      cache: ~/.ocm/cache
  ```

## Create a component version

The first step when creating a new component version is to create a component archive. A component archive contains references, resources and sources. The `ocm` CLI tool can help with this.

For convenience, we define the following environment variables:
```bash
PROVIDER="acme.org"
ORG="acme"
COMPONENT="github.com/${ORG}/helloworld"
VERSION="1.0.0"
CA_ARCHIVE="ca-hello-world"
```

If you specify values for your setup, you can directly use the commands shown in the next steps.

Let's asssume that we create a component based on a GitHub source repository.

### Create a component archive

First we create an empty component archive using the command <a href="https://github.com/open-component-model/ocm/blob/main/docs/reference/ocm_create_componentarchive.md">`ocm create componentarchive`</a>:

```shell
ocm create componentarchive ${COMPONENT} ${VERSION}  --provider ${PROVIDER} --file $CA_ARCHIVE
```

<details><summary>What happened?</summary>

This command creates the following file structure:
```bash
$ tree ca-hello-world
ca-hello-world
├── blobs
└── component-descriptor.yaml
```

The [component descriptor](../../specification/elements/README.md#component-descriptor)
is stored as a yaml file named `component-descriptor.yaml`. It describes the content of a component version.

It contains the following configuration:

```yaml
meta:
  schemaVersion: v2
component:
  name: github.com/acme/helloworld
  version: 1.0.0
  provider: acme.org
  resources: []
  sources: []
  componentReferences: []
```

By default, the command creates a directory structure. The option `--type` can be used to select other target formats, such as `tar` or `tgz`.

</details>

### Add a local resource

The next step is <a href="https://github.com/open-component-model/ocm/blob/main/docs/reference/ocm_add_resources.md">
`ocm add resources`</a>. First, we want to add a Helm Chart stored in a local folder named `helmchart`.

```shell
ocm add resource $CA_ARCHIVE --type helmChart --name mychart --version ${VERSION} --inputType helm --inputPath ./helmchart
```
```shell
processing resource (by options)...
  processing document 1...
    processing index 1
found 1 resources
adding resource helmChart: "name"="mychart","version"="1.0.0"...
```

<details><summary>What happened?</summary>

The generated file structure is:

```shell
tree ca-hello-world
```
```shell
ca-hello-world
├── blobs
│   └── sha256.60bfd05083f81f2841657e24410d3ba25e4bcc3e3c927da7e1811e775116a74d
└── component-descriptor.yaml
```

The added blob contains the packaged Helm Chart. The blob is referenced in the component descriptor
in `component.resources.access.localreference`:

```yaml
meta:
  schemaVersion: v2
component:
  name: github.com/acme/helloworld
  version: 1.0.0
  provider: acme.org
  resources:
  - access:
      localReference: sha256.60bfd05083f81f2841657e24410d3ba25e4bcc3e3c927da7e1811e775116a74d
      mediaType: application/vnd.oci.image.manifest.v1+tar+gzip
      referenceName: github.com/acme/helloworld/echoserver:0.1.0
      type: localBlob
    name: mychart
    relation: local
    type: helmChart
    version: 1.0.0
  sources: []
  componentReferences: []
```
Because we use content from the local environment, it is directly packaged into the component archive
using the [access method](../../specification/elements/README.md#artifact-access) of type
[`local`](../../appendix/B/localBlob.md).
</details>

### Add an image reference

Next, we will add an image. The image is already stored in an image registry (e.g. by a previous Docker build/push).

```shell
ocm add resource $CA_ARCHIVE --type ociImage --name image --version ${VERSION} --accessType ociArtifact --reference gcr.io/google_containers/echoserver:1.10
```
```shell
processing resource (by options)...
  processing document 1...
    processing index 1
found 1 resources
adding resource ociImage: "name"="image","version"="1.0.0"...
```

<details><summary>What happened?</summary>
The component descriptor now has the following content, with an additional `access` under
`component.resources`, where `access` is of type `external`:

```yaml
meta:
  schemaVersion: v2
component:
  name: github.com/acme/helloworld
  version: 1.0.0
  provider: acme.org
  resources:
  - access:
      localReference: sha256.60bfd05083f81f2841657e24410d3ba25e4bcc3e3c927da7e1811e775116a74d
      mediaType: application/vnd.oci.image.manifest.v1+tar+gzip
      referenceName: github.com/acme/helloworld/echoserver:0.1.0
      type: localBlob
    name: mychart
    relation: local
    type: helmChart
    version: 1.0.0
  - access:
      imageReference: gcr.io/google_containers/echoserver:1.10
      type: ociArtifact
    name: image
    relation: external
    type: ociImage
    version: 1.0.0
  sources: []
  componentReferences: []
  repositoryContexts: []
```
</details>

### Add an image resource

Alternatively you can add an image as a resource built locally using Docker before. It will be picked up from the local Docker file system and added to the component archive.

```shell
docker image ls

REPOSITORY                                              TAG                 IMAGE ID       CREATED         SIZE
echoserverimage                                         1.10.0              365ec60129c5   4 years ago     95.4MB
...
```
```shell
ocm add resource ${CA_ARCHIVE} --name image --version ${VERSION} --type ociArtifact  --inputType docker --inputPath=echoserverimage:1.10.0
```
```shell
processing resource (by options)...
  processing document 1...
    processing index 1
found 1 resources
adding resource ociArtifact: "name"="image","version"="1.0.0"...
  image echoserverimage:1.10.0
locator: echoserverimage, repo: , version 1.10.0
~/temp/ocm/hello>
```

<details><summary>What happened?</summary>
The docker image is downloaded from the docker daemon, converted to an OCI artifact,
and added as local artifact to the component version.
The component descriptor now has the content:

```yaml
component:
  componentReferences: []
  name: github.com/acme/helloworld
  provider: acme.org
  repositoryContexts: []
  resources:
  - access:
      localReference: sha256.31b7c98008a6b2d6f0b07e11b997c47c70d31edeea0986382940ccc42288741e
      mediaType: application/vnd.oci.image.manifest.v1+tar+gzip
      referenceName: github.com/acme/helloworld/echoserverimage:1.10.0
      type: localBlob
    name: image
    relation: local
    type: ociArtifact
    version: 1.0.0
  - access:
      localReference: sha256.cf0b6e95c1f05e6825d37e15744f46c6fdb37eea7be2234b8948be71b28ff6b1
      mediaType: application/vnd.oci.image.manifest.v1+tar+gzip
      referenceName: github.com/acme/helloworld/echoserver:0.1.0
      type: localBlob
    name: mychart
    relation: local
    type: helmChart
    version: 1.0.0
  sources: []
  version: 1.0.0
meta:
  schemaVersion: v2
```
The generated blob sha256.65cf... is an archive describing the image according to the
[OCI Image Layout Specification](https://github.com/opencontainers/image-spec/blob/v1.0.1/image-layout.md).

</details>

### Using a resources file

You could simplify the previous two steps (adding helm chart and image as resources) by using a text file as input. For that, you could create a file `resources.yaml`, which looks like this:

```yaml
---
name: mychart
type: helmChart
input:
  type: helm
  path: ./helmchart
---
name: image
type: ociImage
version: "1.0.0"
access:
  type: ociArtifact
  imageReference: gcr.io/google_containers/echoserver:1.10
```

Then add the resources using the following command:

```shell
$ ocm add resources $CA_ARCHIVE resources.yaml
```
```shell
processing resources.yaml...
  processing document 1...
    processing index 1
  processing document 2...
    processing index 1
found 2 resources
adding resource helmChart: "name"="mychart","version"="<componentversion>"...
adding resource ociImage: "name"="image","version"="1.0.0"...
```

For an image built with Docker use this file:
```shell
---
name: mychart
type: helmChart
input:
  type: helm
  path: ./helmchart
---
name: image
type: ociImage
version: "1.0.0"
input:
  type: docker
  repository: echoserverimage
  path: echoserverimage:1.10.0
```

### Uploading component versions
To upload the component version to an OCI registry, you can transfer the component archive using the command <a href="https://github.com/open-component-model/ocm/blob/main/docs/reference/ocm_transfer_componentarchive.md">`ocm transfer componentarchive`</a>:

```shell
OCMREPO=ghcr.io/acme
ocm transfer componentarchive ./ca-hello-world ${OCMREPO}
```
```shell
transferring version "github.com/acme/helloworld:1.0.0"...
...resource 0(github.com/acme/helloworld/echoserver:0.1.0)...
...adding component version...
```


### Bundle composed components

If you have created multiple components according to the instructions above, you can bundle
them into a single archive entity. This can be done by creating a transport archive.

The transport archive is the entity that does the transfer between
component repositories. It is used to transfer entire deployments between
locations.

A transport archive may contain any number of component versions. It may also be pushed to an OCM repository.

Note that a transport achive is also an OCM repository, so it can also be used as source or as a target
for transport operations.

```shell
CTF_ARCHIVE=ctf-hello-world
ocm transfer componentversion ${CA_ARCHIVE} ${CTF_ARCHIVE}
```
```shell
transferring version "github.com/acme/helloworld:1.0.0"...
...resource 0(github.com/acme/helloworld/echoserver:0.1.0)...
...adding component version...
1 versions transferred
```
<details><summary>What happened?</summary>

The resulting transport archive has the following file structure:

```shell
tree ${CTF_ARCHIVE}
```
```shell
ctf-hello-world
├── artifact-index.json
└── blobs
    ├── sha256.378a171e7a1bcecc19b7fd4a330161a9d91550486dad668c78d08e590ef245e7
    ├── sha256.4f2080d8d41d2b52182f325f4f42d91e2581e3f2299f4f8631196801773ba869
    ├── sha256.63dc40246a604ef503f0361e14216ab7e002912697d09da49f50bba7091549f7
    └── sha256.b9bf66cb07b129d12956392dff6110874c37a1b06ed8dde88881f6de971ff293
```

The transport archive's contents can be found in `artifact-index.json`. This file
contains the list of component version artifacts to be transported.

```shell
jq . ${CTF_ARCHIVE}/artifact-index.json
```
```shell
{
  "schemaVersion": 1,
  "artifacts": [
    {
      "repository": "component-descriptors/github.com/acme/helloworld",
      "tag": "1.0.0",
      "digest": "sha256:63dc40246a604ef503f0361e14216ab7e002912697d09da49f50bba7091549f7"
    }
  ]
}
```

The content of the transport archive is stored as OCI artifacts. Notice that the repository names of Component Version artifacts (found at `artifacts.respository`) are prefixed by `component-descriptors/`.

The component version is described as an OCI manifest:

```shell
jq . ${CTF_ARCHIVE}/blobs/sha256.63dc40246a604ef503f0361e14216ab7e002912697d09da49f50bba7091549f7
```
```shell
{
  "schemaVersion": 2,
  "mediaType": "application/vnd.oci.image.manifest.v1+json",
  "config": {
    "mediaType": "application/vnd.ocm.software.component.config.v1+json",
    "digest": "sha256:b9bf66cb07b129d12956392dff6110874c37a1b06ed8dde88881f6de971ff293",
    "size": 201
  },
  "layers": [
    {
      "mediaType": "application/vnd.ocm.software.component-descriptor.v2+yaml+tar",
      "digest": "sha256:4f2080d8d41d2b52182f325f4f42d91e2581e3f2299f4f8631196801773ba869",
      "size": 2560
    },
    {
      "mediaType": "application/vnd.oci.image.manifest.v1+tar+gzip",
      "digest": "sha256:378a171e7a1bcecc19b7fd4a330161a9d91550486dad668c78d08e590ef245e7",
      "size": 4747
    }
  ]
}
```

Notice that the output of the component version above contains the component descriptor as a `layer`. It can be identified by its content type, which is `application/vnd.ocm.software.component-descriptor.v2+yaml+tar`. In ths case, the component descriptor can be displayed with the following command:

```shell
tar xvf ctf-hello-world/blobs/sha256.4f2080d8d41d2b52182f325f4f42d91e2581e3f2299f4f8631196801773ba869 -O - component-descriptor.yaml
```
```shell
component:
  componentReferences: []
  name: github.com/acme/helloworld
  provider: acme.org
  repositoryContexts: []
  resources:
  - access:
      localReference: sha256:378a171e7a1bcecc19b7fd4a330161a9d91550486dad668c78d08e590ef245e7
      mediaType: application/vnd.oci.image.manifest.v1+tar+gzip
      referenceName: github.com/acme/helloworld/echoserver:0.1.0
      type: localBlob
    name: mychart
    relation: local
    type: helmChart
    version: 1.0.0
  - access:
      imageReference: gcr.io/google_containers/echoserver:1.10
      type: ociArtifact
    name: image
    relation: external
    type: ociImage
    version: 1.0.0
  sources: []
  version: 1.0.0
meta:
  schemaVersion: v2
```

The other elements listed as `layer`s describe the blobs for the local resources stored along with the component version. The digests can be seen in the `localReference` attributes of the component descriptor.

</details>

## Display and Examine component versions

### List component versions

To show the component stored in a component archive (without looking at the file system structure), the <a href="https://github.com/open-component-model/ocm/blob/main/docs/reference/ocm_get_componentversions.md">`ocm get componentversion`</a> command can be used:

```shell
ocm get componentversion ${CA_ARCHIVE}
```
```shell
COMPONENT                  VERSION PROVIDER
github.com/acme/helloworld 1.0.0   acme.org
```

To see the component descriptor of the displayed component version, use the output format option `-o yaml`:

```shell
ocm get componentversion ${CA_ARCHIVE} -o yaml
```
```shell
---
context: []
element:
  component:
    componentReferences: []
    name: github.com/acme/helloworld
    provider:
      name: acme.org
    repositoryContexts: []
    resources: []
    sources: []
    version: 1.0.0
  meta:
    configuredSchemaVersion: v2
```

Display the component versions of any OCM repository with this command:

```shell
ocm get cv ghcr.io/mandelsoft/cnudie//github.com/mandelsoft/ocmhelmdemo
```
```shell
COMPONENT                         VERSION   PROVIDER
github.com/mandelsoft/ocmhelmdemo 0.1.0-dev mandelsoft
```

To refer to the content of a component repository, the component name can be appended to the repository specification separated by `//`.

In the example above, `ghcr.io/mandelsoft/cnudie` is the OCM repository, whereas `github.com/mandelsoft/ocmhelmdemo` is the component stored in this component repository.

Optionally, a specific version can be appended, separated by a colon (`:`). If no version is specified, all component versions will be displayed.

With the option `--recursive`, it is possible to show the complete component version, including the component versions it references.

```shell
ocm get cv ghcr.io/mandelsoft/cnudie//github.com/mandelsoft/ocmhelmdemo --recursive
```
```shell
REFERENCEPATH                               COMPONENT                              VERSION   PROVIDER   IDENTITY
                                            github.com/mandelsoft/ocmhelmdemo      0.1.0-dev mandelsoft
github.com/mandelsoft/ocmhelmdemo:0.1.0-dev github.com/mandelsoft/ocmhelminstaller 0.1.0-dev mandelsoft "name"="installer"
```

To get a tree view, add the option `-o tree`:

```shell
ocm get componentversion ghcr.io/mandelsoft/cnudie//github.com/mandelsoft/ocmhelmdemo --recursive -o tree
```
```shell
NESTING    COMPONENT                              VERSION   PROVIDER   IDENTITY
└─ ⊗       github.com/mandelsoft/ocmhelmdemo      0.1.0-dev mandelsoft
   └─      github.com/mandelsoft/ocmhelminstaller 0.1.0-dev mandelsoft "name"="installer"
```

### List the resources of a component version

To list the resources found in a component version tree, the command <a href="https://github.com/open-component-model/ocm/blob/main/docs/reference/ocm_get_resources.md">`ocm get resources`</a> can be used:

```shell
ocm get resources ghcr.io/mandelsoft/cnudie//github.com/mandelsoft/ocmhelmdemo:0.1.0-dev --recursive -o tree
```
```shell
COMPONENTVERSION                                           NAME        VERSION   IDENTITY TYPE        RELATION
└─ github.com/mandelsoft/ocmhelmdemo:0.1.0-dev
   ├─                                                      chart       0.1.0-dev          helmChart   local
   ├─                                                      image       1.0                ociImage    external
   ├─                                                      package     0.1.0-dev          toiPackage  local
   └─ github.com/mandelsoft/ocmhelminstaller:0.1.0-dev
      ├─                                                   toiexecutor 0.1.0-dev          toiExecutor local
      └─                                                   toiimage    0.1.0-dev          ociImage    local
```

### Download the resources of a component version

Use the <a href="https://github.com/open-component-model/ocm/blob/main/docs/reference/ocm_download_resources.md">`ocm download`</a> command to download resources such as component versions, individual resources or artifacts:

```shell
ocm download resource ghcr.io/jensh007//github.com/acme/helloworld:1.0.0 chart -O helmchart.tgz
```
```shell
helmchart.tgz: 4747 byte(s) written
```

Because it is stored as OCI artifact in an OCI registry, the filesystem format used for OCI artifacts is the blob format.

<details><summary>What happened?</summary>
The file helmchart.tgz was downloaded.

```shell
tar xvf helmchart.tgz
```
```shell
x index.json
x oci-layout
x blobs
x blobs/sha256.1c1af427d477202d102c141f27d3be0f5b6595e2948a82ec58987560c1915fea
x blobs/sha256.47eacca4cbed4b63c17e044d3c87a33d9bd1f88a9e76fa0ab051e48b0a3cd7ec
x blobs/sha256.ea8e5b44cd1aff1f3d9377d169ad795be20fbfcd58475a62341ed8fb74d4788c
```
```shell
$ jq . index.json
{
  "schemaVersion": 2,
  "mediaType": "application/vnd.oci.image.index.v1+json",
  "manifests": [
    {
      "mediaType": "application/vnd.oci.image.manifest.v1+json",
      "digest": "sha256:47eacca4cbed4b63c17e044d3c87a33d9bd1f88a9e76fa0ab051e48b0a3cd7ec",
      "size": 410,
      "annotations": {
        "cloud.gardener.ocm/tags": "0.1.0",
        "org.opencontainers.image.ref.name": "0.1.0",
        "software.ocm/tags": "0.1.0"
      }
    }
  ],
  "annotations": {
    "cloud.gardener.ocm/main": "sha256:47eacca4cbed4b63c17e044d3c87a33d9bd1f88a9e76fa0ab051e48b0a3cd7ec",
    "software.ocm/main": "sha256:47eacca4cbed4b63c17e044d3c87a33d9bd1f88a9e76fa0ab051e48b0a3cd7ec"
  }
}

```
</details>


#### Download with download handlers

To use a format more suitable for the content technology, enable the usage
of download handlers.

If a download handler is available for the artifact type and the
blob media type used to store the blob in the OCM repository, it will convert the blob format
into a more suitable format:

```shell
ocm download resource -d ghcr.io/jensh007//github.com/acme/helloworld:1.0.0 chart -O helmchart.tgz
```
```shell
helmchart.tgz: 4747 byte(s) written
```

<details><summary>What happened?</summary>
The downloaded archive is now a regular Helm Chart archive:

```shell
tar tvf echoserver-0.1.0.tgz
```
```shell
-rw-r--r--  0 0      0         136 Nov 30 13:19 echoserver/Chart.yaml
-rw-r--r--  0 0      0        1842 Nov 30 13:19 echoserver/values.yaml
-rw-r--r--  0 0      0        1755 Nov 30 13:19 echoserver/templates/NOTES.txt
-rw-r--r--  0 0      0        1802 Nov 30 13:19 echoserver/templates/_helpers.tpl
-rw-r--r--  0 0      0        1848 Nov 30 13:19 echoserver/templates/deployment.yaml
-rw-r--r--  0 0      0         922 Nov 30 13:19 echoserver/templates/hpa.yaml
-rw-r--r--  0 0      0        2083 Nov 30 13:19 echoserver/templates/ingress.yaml
-rw-r--r--  0 0      0         367 Nov 30 13:19 echoserver/templates/service.yaml
-rw-r--r--  0 0      0         324 Nov 30 13:19 echoserver/templates/serviceaccount.yaml
-rw-r--r--  0 0      0         385 Nov 30 13:19 echoserver/templates/tests/test-connection.yaml
-rw-r--r--  0 0      0         349 Nov 30 13:19 echoserver/.helmignore
```
</details>


#### Download an image

For example, for OCI images, the OCI format is more suitable:

```shell
ocm download resource ghcr.io/jensh007//github.com/acme/helloworld:1.0.0 image -O echoserver.tgz
```
```shell
echoserver.tgz: 46148828 byte(s) written
```

<details><summary>What happened?</summary>
The file `echoserver.tgz` was downloaded.

```shell
tar xvf echoserver.tgz
```
```shell
x index.json
x oci-layout
x blobs
x blobs/sha256.06679f57dba70a6875e4ae5843ba2483ecab6ec48182ca8720ddc5b1863bad52
x blobs/sha256.28c6282d04f63710146ace6c7be14a40c7ee6a71a2f91316928469e4aafe0d92
x blobs/sha256.2d3e25b9e93ad26878862abee5ed02683206f6f6d57e311cdd1dedf3662b61c8
x blobs/sha256.365ec60129c5426b4cf160257c06f6ad062c709e0576c8b3d9a5dcc488f5252d
x blobs/sha256.4b12f3ef8e65aaf1fd77201670deb98728a8925236d8f1f0473afa5abe9de119
x blobs/sha256.76d46396145f805d716dcd1607832e6a1257aa17c0c2646a2a4916e47059dd54
x blobs/sha256.7fd34bf149707ca78b3bb90e4ba68fe9a013465e5d03179fb8d3a3b1cac8be27
x blobs/sha256.b0e3c31807a2330c86f07d45a6d80923d947a8a66745a2fd68eb3994be879db6
x blobs/sha256.bc391bffe5907b0eaa04e96fd638784f77d39f1feb7fbe438a1dae0af2675205
x blobs/sha256.cb5c1bddd1b5665e1867a7fa1b5fa843a47ee433bbb75d4293888b71def53229
x blobs/sha256.d5157969118932d522396fe278eb722551751c7aa7473e6d3f03e821a74ee8ec
x blobs/sha256.e0962580d8254d0b1ef35006d7e2319eb4870e63dc1f9573d2406c7c47d442d2
```
```shell

jq . index.json
{
  "schemaVersion": 2,
  "mediaType": "application/vnd.oci.image.index.v1+json",
  "manifests": [
    {
      "mediaType": "application/vnd.docker.distribution.manifest.v2+json",
      "digest": "sha256:cb5c1bddd1b5665e1867a7fa1b5fa843a47ee433bbb75d4293888b71def53229",
      "size": 2400,
      "annotations": {
        "cloud.gardener.ocm/tags": "1.10",
        "org.opencontainers.image.ref.name": "1.10",
        "software.ocm/tags": "1.10"
      }
    }
  ],
  "annotations": {
    "cloud.gardener.ocm/main": "sha256:cb5c1bddd1b5665e1867a7fa1b5fa843a47ee433bbb75d4293888b71def53229",
    "software.ocm/main": "sha256:cb5c1bddd1b5665e1867a7fa1b5fa843a47ee433bbb75d4293888b71def53229"
  }
}
```
</details>

#### Download an executable
The Open Component Model allows to publish platform-specific executables. In this case, the platform
specification is used by convention as extra identity for the artifacts that are contained in the component
version.

Example:
```shell
ocm get componentversion ghcr.io/open-component-model/ocm//ocm.software/ocmcli:0.1.0-dev -o yaml
```
```shell
...
    resources:
    - name: ocmcli
      extraIdentity:
        architecture: amd64
        os: linux
      relation: local
      type: executable
      version: 0.1.0-dev
      access:
        localReference: sha256:1a8827761f0aaa897d1d4330c845121c157e905d1ff300ba5488f8c423bc7cd9
        mediaType: application/octet-stream
        type: localBlob
    - name: ocmcli
      extraIdentity:
        architecture: arm64
        os: darwin
      relation: local
      type: executable
      version: 0.1.0-dev
      access:
        localReference: sha256:9976b18dc16ae2b2b3fc56686f18f4896d44859f1ea6221f70e83517f697e289
        mediaType: application/octet-stream
        type: localBlob
...
```
Note, the resources shown above have the same name and type `executable` but a different extra-identity. If a
component version complies to this convention, executables can directly be downloaded for the specified
platform with the use of the `-x` option. If only one executable is contained in the component version, the
resource name can be omitted. Example:

```shell
ocm download resource -x --latest ghcr.io/open-component-model/ocm//ocm.software/ocmcli
```
```shell
ocm: 52613730 byte(s) written
```

<details><summary>What happened?</summary>

```shell
ls -l
```
```shell
total 51M
-rwxr-xr-x  1 me staff  51M Nov 30 13:49 ocm
```
```shell
file ocm
```
```shell
ocm: Mach-O 64-bit executable arm64
```

With the option `--latest`, the latest mathching component version is used for download. With the
option `--constraints` version constraints can be configured. For example: `--constraints 0.1.x`
will select all patch versions of `0.1`. Together with `--latest` the latest patch version is
selected.

The option `-x` enables the executable download handler, which provides the x-bit of the downloaded
files. Additionally it filters all matching resources for executables and the correct platform.

</details>

#### Download a full component version

Download entire component versions using the <a href="https://github.com/open-component-model/ocm/blob/main/docs/reference/ocm_download_componentversions.md">`ocm download componentversion`</a> command:

```shell
ocm download componentversions ${OCM_REPO}//${COMPONENT}:${VERSION} -O helloworld
```
```shell
helloworld: downloaded
```

The result is a component archive. This can then be modified using the `ocm add ...` commands shown earlier.

<details><summary>What happened?</summary>
The component version was downloaded.

```shell
tree helloworld2
```
```shell
├── blobs
└── component-descriptor.yaml
```

The `blobs` directory is empty because, during the upload to the OCI registry, the local helmchart blob was transformed to a regular OCI artifact. The access method in the component descriptor has been modified to ociArtifact.

</details>

### Download OCI Artifacts

Download OCI artifacts from an OCI registry, such as OCI images, with the <a href="https://github.com/open-component-model/ocm/blob/main/docs/reference/ocm_download_artifacts.md">`ocm download artifacts`</a> command:

```shell
ocm download artifact ${OCM_REPO}/${COMPONENT}:${VERSION} -O echoserver
```
```shell
echoserver: downloaded
```

<details><summary>What happened?</summary>
The OCI image `echoserver` was downloaded.

```shell
tree echoserver
```
```shell
echoserver
├── blobs
│   ├── sha256.1c1af427d477202d102c141f27d3be0f5b6595e2948a82ec58987560c1915fea
│   ├── sha256.47eacca4cbed4b63c17e044d3c87a33d9bd1f88a9e76fa0ab051e48b0a3cd7ec
│   └── sha256.ea8e5b44cd1aff1f3d9377d169ad795be20fbfcd58475a62341ed8fb74d4788c
├── index.json
└── oci-layout
```
</details>


## Transport OCM component versions

The section [Bundle composed components](#bundle-composed-components) explained how to bundle multiple component version into a transport
archive.

During the transfer, it is possible to include component references as local blobs. It is also possible to include references in a recursive way.

Here is an example of a recursive transfer from one OCI registry to another, which includes resources and references:

```shell
ocm transfer componentversion --recursive --copy-resources ${OCM_REPO}//${COMPONENT}:${VERSION} eu.gcr.io/acme/
```
```shell
transferring version "github.com/acme/helloworld:1.0.0"...
...resource 0(github.com/acme/helloworld/echoserver:0.1.0)...
...adding component version...
1 versions transferred
```

The OCM CLI's `transfer` command can be used to transfer component versions, component archives, transport archives and artifacts. See `ocm transfer -h` for more information.

More examples on the transport archive can be found in [appendix A](../../appendix/A/CTF/README.md).

## Sign component versions

Sign component versions to ensure integrity along a transport chain.

Signing requires a key pair, a signature, and optionally an issuer as well as an algorithm and a
name for the signature.

A component version can have multiple signatures with different names. A normalization of the
component version is used for signing. See [appendix C](../../appendix/C/README.md) for more details.
Currently only signing according
[RSA PKCS #1 v1.5 signature algorithm](https://datatracker.ietf.org/doc/html/rfc3447) supported.

Create a key pair using the OCM CLI:
```shell
ocm create rsakeypair acme.priv
```

This will create two files. One named `acme.priv` for the private key and for convenience one named
`acme.pub` for the public key.

Use the `sign componentversion` command to sign a component version:

```shell
ocm sign componentversion --signature acme-sig --private-key=acme.priv ${OCM_REPO}//${COMPONENT}:${VERSION}
```

You can also sign a common transport archive before uploading to a component
repository:

```shell
ocm sign componentversion --signature acme-sig --private-key=acme.priv ctf-hello-world
```
```shell
applying to version "github.com/acme/helloworld:1.0.0"...
successfully signed github.com/acme/helloworld:1.0.0 (digest sha256:46615253117b7217903302d172a45de7a92f2966f6a41efdcc948023ada318bc)
```

<details><summary>What happened?</summary>

Digests will be created for all described artifacts and referenced component versions. Then for the
top-level component versions the component-version digests are signed. Signature and digests are
stored in the component descriptor(s):

```shell
jq . ${CTF_ARCHIVE}/artifact-index.json
```
```shell
{
  "schemaVersion": 1,
  "artifacts": [
    {
      "repository": "component-descriptors/github.com/acme/helloworld",
      "tag": "1.0.0",
      "digest": "sha256:8c6b8c5a63a09d96d2a60b50adbd47f06b31be6e9d3e8618177c60fb47ec4bb2"
    }
  ]
}

Beside the digests of the component descriptor layer nothing has changed:

jq . ${CTF_ARCHIVE}/blobs/sha256.8c6b8c5a63a09d96d2a60b50adbd47f06b31be6e9d3e8618177c60fb47ec4bb2
```
```shell
{
  "schemaVersion": 2,
  "mediaType": "application/vnd.oci.image.manifest.v1+json",
  "config": {
    "mediaType": "application/vnd.ocm.software.component.config.v1+json",
    "digest": "sha256:23225a4bfd2bacd575ec5317a25a0dd63702594f5859fbc3a4c4301453ac311a",
    "size": 201
  },
  "layers": [
    {
      "mediaType": "application/vnd.ocm.software.component-descriptor.v2+yaml+tar",
      "digest": "sha256:1f8c7801b2b35768b0eb9c919683ffcd0af24d8135beaccb7146af56cb2981d9",
      "size": 3584
    },
    {
      "mediaType": "application/vnd.oci.image.manifest.v1+tar+gzip",
      "digest": "sha256:2a958a5e8e9cca1b4e5b3cce510db9058f0117d09ce8c0981523230aa5d0e3d0",
      "size": 4714
    }
  ]
}
```
```shell
tar xvf ${CTF_ARCHIVE}/blobs/sha256.1f8c7801b2b35768b0eb9c919683ffcd0af24d8135beaccb7146af56cb2981d9 -O - component-descriptor.yaml
```
```shell
meta:
  schemaVersion: v2
component:
  name: github.com/acme/helloworld
  version: 1.0.0
  provider: acme.org
  resources:
  - access:
      localReference: sha256:2a958a5e8e9cca1b4e5b3cce510db9058f0117d09ce8c0981523230aa5d0e3d0
      mediaType: application/vnd.oci.image.manifest.v1+tar+gzip
      referenceName: github.com/acme/helloworld/echoserver:0.1.0
      type: localBlob
    digest:
      hashAlgorithm: sha256
      normalisationAlgorithm: ociArtifactDigest/v1
      value: 7b1614e9de1daee6334c91fce087e4365ee30f8f4da783ae81c27c6a81718b1d
    name: chart
    relation: local
    type: helmChart
    version: 1.0.0
  - access:
      imageReference: gcr.io/google_containers/echoserver:1.10
      type: ociArtifact
    digest:
      hashAlgorithm: sha256
      normalisationAlgorithm: ociArtifactDigest/v1
      value: cb5c1bddd1b5665e1867a7fa1b5fa843a47ee433bbb75d4293888b71def53229
    name: image
    relation: external
    type: ociImage
    version: 1.0.0
  componentReferences: []
  repositoryContexts: []
  sources: []
signatures:
- digest:
    hashAlgorithm: sha256
    normalisationAlgorithm: jsonNormalisation/v1
    value: 023accb95490e1cf00926ddec95aadac599528bd987f6c1f0b5440c1bc51add3
  name: acme-sig
  signature:
    algorithm: RSASSA-PKCS1-V1_5
    mediaType: application/vnd.ocm.signature.rsa
    value: 6538f0f1ddb436008c4f82a84cfa92893e44cca1f2363f9da786ab632bca92f6498d912f2e4dfcdd9fa24078be83ba4f56851fa7b1235526c11cf5c9bd923676acaecb0e19f3996ac96a7334a4b4dcbf0b33479e90dd9500ea4fd5e914e17edb41c49ead6b92b313d1b79c612309b743399a2284f19a3e98c383122aa0045766394de700b8db96f4e69c6df2238c149660e5e4f8beaec45737a7ec2ddf36aa0c2042fce298c5ef2f823612229f013c147a19afe23fe81afe31200a3c2ad77485f8e9f8f01d5faba64c484b673e42a49082e1d20fb5c75616896007432e7f1b60da1591c756f4c6fab98f4125d13d7790adb41dd46717c67e92f2de6fb7c8a6c3
```
</details>

### Signing with certificates

The public key from the last example cannot be validated. This can be changed by using a certificate
instead of a pure public key. The certificate is signed by a CA. This ensures the authenticity of the
described public key. Additionally the common name of the certificate is validated against the issuer
attribute of the signature stored in the component descriptor.

To create a certificate use the command:

```shell
ocm create rsakeypair --cacert ca.cert --cakey ca.priv CN=acme.org acme.priv
```

You can use additional attributes of the certificate like `O`, `OU` or `C`. See usage for details.
The certificate can be requested by any offical certificate authority instead. It requires the usage types x509.KeyUsageDigitalSignature and x509.ExtKeyUsageCodeSigning.

For signing the component version you need to provide the issuer then:

```shell
ocm sign componentversion --signature acme-sig --private-key=acme.priv --issuer acme.org ${OCM_REPO}//${COMPONENT}:${VERSION}
```

Now the issuer will be stored along the signature and will be checked when verifying with the certificate
instead of the public key.



### Signature Verification
You can verify a signed component version. Therefore a public or a certificate provided by the
signer is required. If a certificate is provided it is validated according its certificate chain.
If not an official CA is used you need the certificate of the used root CA.

To verify the signature of a component version use

```shell
ocm verify componentversions --signature acme-sig --public-key=acme.pub ctf-hello-world
```
```shell
applying to version "github.com/acme/helloworld:1.0.0"...
successfully verified github.com/acme/helloworld:1.0.0 (digest sha256:46615253117b7217903302d172a45de7a92f2966f6a41efdcc948023ada318bc)
```
