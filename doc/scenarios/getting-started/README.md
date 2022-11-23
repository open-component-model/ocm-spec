# Getting Started

This chapter describes a walkthrough:
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

For the following sections you will need the OCM Command Line Interface (CLI) to interact with component versions and registries. Download a binary from [here](https://github.com/open-component-model/ocm/releases).

The link follows this pattern: https://github.com/open-component-model/ocm/releases/download/<VERSION>/ocm-<PLATFORM>.tgz

You will need access to an OCM repository. You can use any existing OCI registry for which you have write permission (e.g. Github Packages).

An OCM repository based on an OCI registry is identified by a leading OCI repository prefix. For example: `ghcr.io/<YOUR-ORG>/ocm`.

You will have to configure credentials for the CLI to access the registry. The easiest way to do this is to reuse the docker configuration:

You can create a file named `.ocmconfig` in your home directory with the following content:

<a href='.ocmconfig'>
<pre>
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
</pre>
</a>

## Creating a component version

Composition of component versions consists of creating a component archive. You can use the `ocm` CLI tool to create this. A component archive contains references, resources and sources.

For convenience we define the following SHELL variables
```bash
PROVIDER="acme.org"
ORG="acme"
COMPONENT="github.com/${ORG}/helloworld"
VERSION="1.0.0"
CA_ARCHIVE="ca-hello-world"
```

Let's asssume that we create a component based on a github source
repository.

### Creating a component archive

First we create an empty component archive.

<a href="https://github.com/open-component-model/ocm/blob/main/docs/reference/ocm_create_componentarchive.md">
<pre>
$ ocm create componentarchive ${COMPONENT} ${VERSION}  --provider ${PROVIDER} --file $CA_ARCHIVE
</pre>
</a>

<details><summary>What happened?</summary>

This command will create the following file structure:
```bash
$ tree ca-hello-world
ca-hello-world
├── blobs
└── component-descriptor.yaml
```

The generated component descriptor is already configured:

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

By default a directory structure is created. Using the option `--type` you can select other target formats (tar, tgz).

</details>

### Adding a local resource

The next step is to add resources. First we want to add a helm chart located in a local folder named `helmchart`.

```
$ ocm add resource $CA_ARCHIVE --type helmChart --name deploy --version ${VERSION} --inputType helm --inputPath ./helmchart

processing resource (by options)...
  processing document 1...
    processing index 1
found 1 resources
adding resource helmChart: "name"="deploy","version"="1.0.0"...
```
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
Because we use content from the local environment it is directly packaged in the component archive using the [access method](../../specification/elements/README.md#artifact-access) [`local`](../../appendix/B/localBlob.md).
</details>

### Adding an image reference

As a next step we add the image already stored in an image registry (e.g. by a Docker build).

```
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

You can simplify the procedure by using a text file as input. Create a file `resources.yaml`:

```
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

Then add the resources using the command:

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
To upload the component version to an OCI registry you can transfer the created component archive using the command:

```shell
OCMREPO=ghcr.io/acme
$ ocm transfer componentarchive ./ca-hello-world ${OCMREPO}

transferring version "github.com/acme/helloworld:1.0.0"...
...resource 0(github.com/acme/helloworld/echoserver:0.1.0)...
...adding component version...
```
### Bundling of composed components

If you have created multiple components according to the instructions above you can bundle
them into a single archive entity. This requires creating a transport archive. You can add
arbitrary numbers of component versions. You can also push a transport archive to an OCM
repository (a transport achive is also an OCM repository and can be used as source or target
for transport operations).

```shell
$ CTF_ARCHIVE=ctf-hello-world
$ ocm transfer componentversion ${CA_ARCHIVE} ${CTF_ARCHIVE}

transferring version "github.com/acme/helloworld:1.0.0"...
...resource 0(github.com/acme/helloworld/echoserver:0.1.0)...
...adding component version...
1 versions transferred
```

<details><summary>What happened?</summary>
The created transport archive contains an index file `artifact-index.json` and a `blobs`
directory. The index file contains the list of component version artifacts in this
archive. The component artifacts are stored in OCI format. The component descriptor is
now stored as a blob. It can be identified by its content type `application/vnd.ocm.software.component-descriptor.v2+yaml+tar`.

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
To show the component stored in a component archive (without looking the file syetem structure) the `get componentversion` command can be used.
```shell
$ ocm get componentversion ${CA_ARCHIVE} 
COMPONENT                  VERSION PROVIDER
github.com/acme/helloworld 1.0.0   acme.org
```

If you want to show the component descriptor of the shown component versions you can use the output format option `-o yaml`
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

You also can display component versions in any OCM repository with this command. 
```shell
$ ocm get cv ghcr.io/mandelsoft/cnudie//github.com/mandelsoft/ocmhelmdemo
COMPONENT                         VERSION   PROVIDER
github.com/mandelsoft/ocmhelmdemo 0.1.0-dev mandelsoft
```
If you refer to content of a component repository the component name can be appended to the repository specification separated by `//`:  
In the example above `ghcr.io/mandelsoft/cnudie` is the OCM repository, wheras `github.com/mandelsoft/ocmhelmdemo` is the component stored in this component repository. Optionally a dedicated version can be appended, separated by a colon (`:`). If no version is specified all, component versions will be displayed. 

With the option `--recursive` it i possible to show the complete component version closure including the referenced component versions.
```shell
$ ocm get cv ghcr.io/mandelsoft/cnudie//github.com/mandelsoft/ocmhelmdemo --recursive
REFERENCEPATH                               COMPONENT                              VERSION   PROVIDER   IDENTITY
                                            github.com/mandelsoft/ocmhelmdemo      0.1.0-dev mandelsoft
github.com/mandelsoft/ocmhelmdemo:0.1.0-dev github.com/mandelsoft/ocmhelminstaller 0.1.0-dev mandelsoft "name"="installer"
```

To get a tree view you can add the option `-o tree`.

```shell
$ ocm get componentversion ghcr.io/mandelsoft/cnudie//github.com/mandelsoft/ocmhelmdemo --recursive -o tree
NESTING    COMPONENT                              VERSION   PROVIDER   IDENTITY
└─ ⊗       github.com/mandelsoft/ocmhelmdemo      0.1.0-dev mandelsoft
   └─      github.com/mandelsoft/ocmhelminstaller 0.1.0-dev mandelsoft "name"="installer"
```

### Listing resources of a component version

To list the resources found in a compopnent version tree the command `ocm get resources` can be used.

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


### Downloading resources of a component version


## Transporting OCM component versions

## Signing component versions