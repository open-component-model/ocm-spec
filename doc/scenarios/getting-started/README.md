# Getting Started

This chapter walks you through some basic steps, in order to get you started with OCM, the concepts and the OCM CLI:

- [Getting Started](#getting-started)
  - [Prerequisites](#prerequisites)
  - [Creating a component version](#creating-a-component-version)
    - [Creating a component archive](#creating-a-component-archive)
    - [Adding a local resource](#adding-a-local-resource)
    - [Adding an image reference](#adding-an-image-reference)
    - [Using a resources file](#using-a-resources-file)
    - [Uploading component versions](#uploading-component-versions)
    - [Bundling of composed components](#bundling-of-composed-components)
  - [Displaying and Examining component versions](#displaying-and-examining-component-versions)
    - [Listing component versions](#listing-component-versions)
    - [Listing resources of a component version](#listing-resources-of-a-component-version)
    - [Downloading resources of a component version](#downloading-resources-of-a-component-version)
  - [Transporting OCM component versions](#transporting-ocm-component-versions)
  - [Signing component versions](#signing-component-versions)

## Prerequisites

To follow the steps described in this section, you need

- The OCM Command Line Interface (CLI) to interact with component versions and registries. You can download it from [https://github.com/open-component-model/ocm/releases](https://github.com/open-component-model/ocm/releases).
  ```shell
  $ curl -L https://github.com/open-component-model/ocm/releases/download/v0.1.0-alpha.1/ocm-linux-amd64.tgz -o - | tar -xz; mv ocm* ocm
  ```
- Access to an OCM repository. You can use any existing OCI registry for which you have write permission (e.g. Github Packages). An OCM repository based on an OCI registry is identified by a leading OCI repository prefix. For example: `ghcr.io/<YOUR-ORG>/ocm`.
- Credentials for the CLI to access the registry. The easiest way to do this is to reuse the docker configuration:

  You can create a file named `.ocmconfig` in your home directory with the following content:

  <a href='.ocmconfig'>

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
  </a>

## Creating a component version

The first step when creating a new component versions is to create a component archive. You can use the `ocm` CLI tool for this. Such a component archive contains references, resources and sources.

For convenience, we define the following SHELL variables:
```bash
PROVIDER="acme.org"
ORG="acme"
COMPONENT="github.com/${ORG}/helloworld"
VERSION="1.0.0"
CA_ARCHIVE="ca-hello-world"
```

If you specify values applicable for your setup, you can directly use the command lines shown below.

Let's asssume that we create a component based on a GitHub source repository.

### Creating a component archive

First, we will create an empty component archive using the following command:

<a href="https://github.com/open-component-model/ocm/blob/main/docs/reference/ocm_create_componentarchive.md">

```shell
$ ocm create componentarchive ${COMPONENT} ${VERSION}  --provider ${PROVIDER} --file $CA_ARCHIVE
```
</a>

<details><summary>What happened?</summary>

This command will create the following file structure:
```bash
$ tree ca-hello-world
ca-hello-world
├── blobs
└── component-descriptor.yaml
```

The resulting component descriptor is already configured:

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

The [component descriptor](../../specification/elements/README.md#component-descriptor)
is stored as a yaml file named `component-descriptor.yaml`. It describes the content of a component version.

By default, a directory structure is created. Using the option `--type` you can select other target formats (tar, tgz).

</details>

### Adding a local resource

The next step is to add resources. First, we want to add a helm chart stored in a local folder named `helmchart`.

<a href="https://github.com/open-component-model/ocm/blob/main/docs/reference/ocm_add_resources.md">

```shell
$ ocm add resource $CA_ARCHIVE --type helmChart --name deploy --version ${VERSION} --inputType helm --inputPath ./helmchart

processing resource (by options)...
  processing document 1...
    processing index 1
found 1 resources
adding resource helmChart: "name"="deploy","version"="1.0.0"...
```
</a>
<details><summary>What happened?</summary>

The generated file structure then is:

```shell
$ tree ca-hello-world
ca-hello-world
├── blobs
│   └── sha256.60bfd05083f81f2841657e24410d3ba25e4bcc3e3c927da7e1811e775116a74d
└── component-descriptor.yaml
```

The added blob contains the packaged helm chart and the blob is referenced in the component descriptor:

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
    name: deploy
    relation: local
    type: helmChart
    version: 1.0.0
  sources: []
  componentReferences: []
```
Because we use content from the local environment, it is directly packaged into component archive using the [access method](../../specification/elements/README.md#artifact-access) [`local`](../../appendix/B/localBlob.md).
</details>

### Adding an image reference

As a next step, we add an image, which is already stored in an image registry (e.g. by a previous Docker build/push).

```shell
$ ocm add resource $CA_ARCHIVE --type ociImage --name image --version ${VERSION} --accessType ociArtefact --reference gcr.io/google_containers/echoserver:1.10

processing resource (by options)...
  processing document 1...
    processing index 1
found 1 resources
adding resource ociImage: "name"="image","version"="1.0.0"...
```

<details><summary>What happened?</summary>
The component descriptor now has the content:

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
    name: deploy
    relation: local
    type: helmChart
    version: 1.0.0
  - access:
      imageReference: gcr.io/google_containers/echoserver:1.10
      type: ociArtefact
    name: image
    relation: external
    type: ociImage
    version: 1.0.0
  sources: []
  componentReferences: []
  repositoryContexts: []
```
</details>

### Using a resources file

You could simplify the previous two steps (adding helm chart and image as resources) by using a text file as input. For that, you could create a file `resources.yaml`, which should look like this:

```yaml
---
name: chart
type: helmChart
input:
  type: helm
  path: ./helmchart
---
name: image
type: ociImage
version: "1.0.0"
access:
  type: ociArtefact
  imageReference: gcr.io/google_containers/echoserver:1.10
```

Then add the resources using the following command:

```shell
$ ocm add resources $CA_ARCHIVE resources.yaml
processing resources.yaml...
  processing document 1...
    processing index 1
  processing document 2...
    processing index 1
found 2 resources
adding resource helmChart: "name"="chart","version"="<componentversion>"...
adding resource ociImage: "name"="image","version"="1.0.0"...
```

### Uploading component versions
To upload the component version to an OCI registry, you can transfer the component archive using the command:

<a href="https://github.com/open-component-model/ocm/blob/main/docs/reference/ocm_transfer_componentarchive.md">

```shell
OCMREPO=ghcr.io/acme
$ ocm transfer componentarchive ./ca-hello-world ${OCMREPO}

transferring version "github.com/acme/helloworld:1.0.0"...
...resource 0(github.com/acme/helloworld/echoserver:0.1.0)...
...adding component version...
```
</a>

### Bundling of composed components

If you have created multiple components according to the instructions above, you can bundle
them into a single archive entity. This requires creating a transport archive. You can add
any number of component versions. You can also push a transport archive to an OCM
repository. Note that a transport achive is also an OCM repository and can be used as source or target
for transport operations.

```shell
$ CTF_ARCHIVE=ctf-hello-world
$ ocm transfer componentversion ${CA_ARCHIVE} ${CTF_ARCHIVE}

transferring version "github.com/acme/helloworld:1.0.0"...
...resource 0(github.com/acme/helloworld/echoserver:0.1.0)...
...adding component version...
1 versions transferred
```
<details><summary>What happened?</summary>

The resulting transport archive contains an index file `artifact-index.json` and a `blobs`
directory. The index file contains the list of component version artifacts in this archive.
The component artifacts are stored in OCI format. The component descriptor is
now stored as a blob. It can be identified by its content type `application/vnd.ocm.software.component-descriptor.v2+yaml+tar`.

**TODO**: The above text and the stuff below needs to be explained better. It's kinda hard to relate both. Suggestion: Explain each of the trees / JSONs below with a specific short paragraph.

```shell
$ tree ${CTF_ARCHIVE}
ctf-hello-world
├── artefact-index.json
└── blobs
    ├── sha256.378a171e7a1bcecc19b7fd4a330161a9d91550486dad668c78d08e590ef245e7
    ├── sha256.4f2080d8d41d2b52182f325f4f42d91e2581e3f2299f4f8631196801773ba869
    ├── sha256.63dc40246a604ef503f0361e14216ab7e002912697d09da49f50bba7091549f7
    └── sha256.b9bf66cb07b129d12956392dff6110874c37a1b06ed8dde88881f6de971ff293

$ jq . ${CTF_ARCHIVE}/artefact-index.json
{
  "schemaVersion": 1,
  "artefacts": [
    {
      "repository": "component-descriptors/github.com/acme/helloworld",
      "tag": "1.0.0",
      "digest": "sha256:63dc40246a604ef503f0361e14216ab7e002912697d09da49f50bba7091549f7"
    }
  ]
}

$ jq . ${CTF_ARCHIVE}/blobs/sha256.63dc40246a604ef503f0361e14216ab7e002912697d09da49f50bba7091549f7
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

```shell
$ tar xvf ctf-hello-world/blobs/sha256.4f2080d8d41d2b52182f325f4f42d91e2581e3f2299f4f8631196801773ba869 -O - component-descriptor.yaml

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
    name: chart
    relation: local
    type: helmChart
    version: 1.0.0
  - access:
      imageReference: gcr.io/google_containers/echoserver:1.10
      type: ociArtefact
    name: image
    relation: external
    type: ociImage
    version: 1.0.0
  sources: []
  version: 1.0.0
meta:
  schemaVersion: v2
```

</details>

## Displaying and Examining component versions

### Listing component versions

To show the component stored in a component archive (without looking the file system structure), the `get componentversion` command can be used.

<a href="https://github.com/open-component-model/ocm/blob/main/docs/reference/ocm_get_componentversions.md">

```shell
$ ocm get componentversion ${CA_ARCHIVE}
COMPONENT                  VERSION PROVIDER
github.com/acme/helloworld 1.0.0   acme.org
```
</a>

If you want to see the component descriptor of the displayed component version, you can use the output format option `-o yaml`

```shell
$ ocm get componentversion ${CA_ARCHIVE} -o yaml
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

You also can display component versions in any OCM repository with this command:

```shell
$ ocm get cv ghcr.io/mandelsoft/cnudie//github.com/mandelsoft/ocmhelmdemo
COMPONENT                         VERSION   PROVIDER
github.com/mandelsoft/ocmhelmdemo 0.1.0-dev mandelsoft
```

If you refer to content of a component repository, the component name can be appended to the repository specification separated by `//`:
In the example above, `ghcr.io/mandelsoft/cnudie` is the OCM repository, whereas `github.com/mandelsoft/ocmhelmdemo` is the component stored in this component repository. Optionally, a dedicated version can be appended, separated by a colon (`:`). If no version is specified, all component versions will be displayed.

With the option `--recursive`, it is possible to show the complete component version closure including the referenced component versions.

```shell
$ ocm get cv ghcr.io/mandelsoft/cnudie//github.com/mandelsoft/ocmhelmdemo --recursive
REFERENCEPATH                               COMPONENT                              VERSION   PROVIDER   IDENTITY
                                            github.com/mandelsoft/ocmhelmdemo      0.1.0-dev mandelsoft
github.com/mandelsoft/ocmhelmdemo:0.1.0-dev github.com/mandelsoft/ocmhelminstaller 0.1.0-dev mandelsoft "name"="installer"
```

To get a tree view, you can add the option `-o tree`.

```shell
$ ocm get componentversion ghcr.io/mandelsoft/cnudie//github.com/mandelsoft/ocmhelmdemo --recursive -o tree
NESTING    COMPONENT                              VERSION   PROVIDER   IDENTITY
└─ ⊗       github.com/mandelsoft/ocmhelmdemo      0.1.0-dev mandelsoft
   └─      github.com/mandelsoft/ocmhelminstaller 0.1.0-dev mandelsoft "name"="installer"
```

### Listing resources of a component version

To list the resources found in a component version tree, the command `ocm get resources` can be used:

<a href="https://github.com/open-component-model/ocm/blob/main/docs/reference/ocm_get_resources.md">

```shell
$ ocm get resources ghcr.io/mandelsoft/cnudie//github.com/mandelsoft/ocmhelmdemo:0.1.0-dev --recursive -o tree
COMPONENTVERSION                                           NAME        VERSION   IDENTITY TYPE        RELATION
└─ github.com/mandelsoft/ocmhelmdemo:0.1.0-dev
   ├─                                                      chart       0.1.0-dev          helmChart   local
   ├─                                                      image       1.0                ociImage    external
   ├─                                                      package     0.1.0-dev          toiPackage  local
   └─ github.com/mandelsoft/ocmhelminstaller:0.1.0-dev
      ├─                                                   toiexecutor 0.1.0-dev          toiExecutor local
      └─                                                   toiimage    0.1.0-dev          ociImage    local
```
</a>

### Downloading resources of a component version

You can download entire component versions, individual resources or
artifacts using the `ocm download` command:

<a href="https://github.com/open-component-model/ocm/blob/main/docs/reference/ocm_download_resources.md">

```shell
$ ocm download resource ghcr.io/jensh007//github.com/acme/helloworld:1.0.0 chart -O helmchart.tgz
helmchart.tgz: 4747 byte(s) written
```
</a>

Because it is stored as OCI artifact in an OCI registry the filesystem format is the
blob format used for OCI artifacts.

<details><summary>What happened?</summary>
The file helmchart.tgz was downloaded.

```shell
$ tar xvf helmchart.tgz
x index.json
x oci-layout
x blobs
x blobs/sha256.1c1af427d477202d102c141f27d3be0f5b6595e2948a82ec58987560c1915fea
x blobs/sha256.47eacca4cbed4b63c17e044d3c87a33d9bd1f88a9e76fa0ab051e48b0a3cd7ec
x blobs/sha256.ea8e5b44cd1aff1f3d9377d169ad795be20fbfcd58475a62341ed8fb74d4788c

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

If you want to use a format more suitable for the content technology, you could enable the usage
of download handlers. If a download handler is available for the combination of artifact type and
blob media type used to store the blob in the OCM repository it will convert the native blob format
into a format suitable to the content technology:

```shell
$ ocm download resource -d ghcr.io/jensh007//github.com/acme/helloworld:1.0.0 chart -O helmchart.tgz
helmchart.tgz: 4747 byte(s) written
```

For images the native  format is better suited.

```shell
$ ocm download resource ghcr.io/jensh007//github.com/acme/helloworld:1.0.0 image -O echoserver.tgz
echoserver.tgz: 46148828 byte(s) written
```

<details><summary>What happened?</summary>
The file echoserver.tgz was downloaded.

```shell
$ tar xvf echoserver.tgz
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

You can download entire component versions using the `ocm download componentversion` command
```shell
ocm download componentversions ghcr.io/jensh007//github.com/acme/helloworld:1.0.0 -O helloworld

TODO!!
Error: all mode not supported
```

<details><summary>What happened?</summary>
The component version  was downloaded.

```shell
$ tree helloworld
```
</details>

### Download of OCI Artifacts

You can download OCI artifacts from an OCI registry, e.g. OCI images using `ocm download artifacts` command:

<a href="https://github.com/open-component-model/ocm/blob/main/docs/reference/ocm_download_artifacts.md">

```shell
$ ocm download artefact ghcr.io/jensh007/github.com/acme/helloworld/echoserver:0.1.0 -O echoserver
echoserver: downloaded
```
</a>

<details><summary>What happened?</summary>
The OCI image echoserver was downloaded.

```shell
$ tree echoserver
echoserver
├── blobs
│   ├── sha256.1c1af427d477202d102c141f27d3be0f5b6595e2948a82ec58987560c1915fea
│   ├── sha256.47eacca4cbed4b63c17e044d3c87a33d9bd1f88a9e76fa0ab051e48b0a3cd7ec
│   └── sha256.ea8e5b44cd1aff1f3d9377d169ad795be20fbfcd58475a62341ed8fb74d4788c
├── index.json
└── oci-layout
```
</details>


## Transporting OCM component versions

We saw already how to bundle multiple component version into a transport
archive. The transport archive is the entity you can transfer between
component repositories. This is used to transfer entire deployments between
locations. During transfer you can decide if component references should be
included as local blobs and if references should be followed (by value transport) so that the transitive closure in included (recursive transport).
Examples how the transport archive looks like can be found in [appendix A](../../appendix/A/CTF/README.md).

Example to transfer from one OCI registry to another (including resources and references):

```shell
$ ocm transfer componentversion --recursive --copy-resources ${OCM_REPO}//${COMPONENT}:${VERSION} eu.gcr.io/acme/
transferring version "github.com/acme/helloworld:1.0.0"...
...resource 0(github.com/acme/helloworld/echoserver:0.1.0)...
...adding component version...
1 versions transferred
```

You can transfer component versions, component archives, transport archives or artifacts. See `ocm transfer -h` for more information.

## Signing component versions

You can sign component versions to ensure integrity along a transport chain.
Signing requires a key pair, a signature algorithm and a name for the signature.
A component version can have multiple signatures with different names. For signing
a normalization of the component version is used. See [appendix X](../../appendix/C/README.md) for details.

Yoy can create a key pair using the OCM client:
```shell
$ ocm create rsakeypair acme.priv acme.pub
```

This will create two files named `acme.priv` for the private key and `acme.pub` for
the public key.

For signing a component version use the command:

```shell
ocm sign componentversion --signature acme-sig --private-key=acme.priv ${OCM_REPO}//${COMPONENT}:${VERSION}
````

You can also sign a common transport archive before uploading to component
repository:

```shell
$ ocm sign componentversion --signature acme-sig --private-key=acme.priv ctf-hello-world
applying to version "github.com/acme/helloworld:1.0.0"...
successfully signed github.com/acme/helloworld:1.0.0 (digest sha256:46615253117b7217903302d172a45de7a92f2966f6a41efdcc948023ada318bc)

```

<details><summary>What happened?</summary>
The component was signed and signature and digests are stored in the component
descriptor

```shell
$ jq . ${CTF_ARCHIVE}/artifact-index.json
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

$ jq . ${CTF_ARCHIVE}/blobs/sha256.8c6b8c5a63a09d96d2a60b50adbd47f06b31be6e9d3e8618177c60fb47ec4bb2
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

$ tar xvf ${CTF_ARCHIVE}/blobs/sha256.1f8c7801b2b35768b0eb9c919683ffcd0af24d8135beaccb7146af56cb2981d9 -O - component-descriptor.yaml

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

You can verify a signature with `ocm verify`

```shell
$ ocm verify componentversions --signature acme-sig --public-key=acme.pub ctf-hello-world
applying to version "github.com/acme/helloworld:1.0.0"...
successfully verified github.com/acme/helloworld:1.0.0 (digest sha256:46615253117b7217903302d172a45de7a92f2966f6a41efdcc948023ada318bc)
```

