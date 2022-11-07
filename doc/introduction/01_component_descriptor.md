# Component Descriptor Specification

Usually, complex software products are divided into logical units, which are called **components** in this specification. For example, a software product might consist of three components, a frontend, a backend and some monitoring stack. Of course, the software product itself could be seen as a component comprising the other three components.

As a result of the development phase, **component versions** are created, e.g. when you make a new release of a component.

A component version consists of a set of technical artifacts, e.g. docker images, helm charts, binaries, configuration data etc. Such artifacts are called **resources** in this specification.

Resources are usually build from something, e.g. code in a git repo, named **sources** in this specification.

The OCM introduces a so called **Component Descriptor** for every component version, to describe the resources, sources and other component versions belonging to a particular component version and how these could be accessed.

For the three components in our example software product, one *Component Descriptor* exists for every component version, e.g. three *Component Descriptor* for the three versions of the frontend, six for the six versions of the backend etc.

Not all component version combinations of frontend, backend and monitoring are compatible and build a valid product version. In order to define reasonable version combinations for our software product, we could use another feature of the *Component Descriptor*, which allows the aggregation of component versions.

For our example we could introduce a component for the overall product. A particular version of this product component is again described by a *Component Descriptor*, which contains references to particular *Component Descriptors* for the frontend, backend and monitoring.

This is only an example how to describe a particular product version with OCM as a component with one *Component Descriptor* with references to other *Component Descriptors*, which itself could have such references and so on. You are not restricted to this approach, i.e. you could still just maintain a list of component version combinations which build a valid product release. But OCM provides you a simple approach to specify what belongs to a product version. Starting with the *Component Descriptor* for a product version and following the component references, you could collect all artifacts, belonging to this product version.

*Component Descriptors* are the central concept of OCM. A *Component Descriptor* describes what belongs to a particularversion of a software component and how to access it. This includes:

- resources, i.e. technical artifacts like binaries, docker images, ...
- sources like code in github
- references to other software component versions


### Component Name and Version

Every *Component Descriptor* has a name and version, also called component name and component version. Name and version are the identifier for a *Component Descriptor* and the component version described by it.

```
meta:
  - schemaVersion: "v2"
component:
  name: ...
  version: ...
```

Examples are:

- *github.com*
- *github.com/pathToYourRepo*

A component name SHOULD reference a location where the component’s resources (typically source code, and/or documentation) are hosted. An example and recommended practise is using GitHub repository names for components on GitHub like *github.com/path-of-your-repo*.

*Component versions* refer to specific snapshots of a component. A common scenario being the release of a component.

### Sources and Resources

Components versions are typically built from sources, maintained in source code management systems, and transformed into resources (for example by a build), which are used at installation or runtime of the product.

Each *Component Descriptor* contains a field for references to the used sources and a field for references to the built resources.

Example for resource references:

```
...
component:
  resources:
    - name: external-monitoring
      version: v0.8.3
      relation: external
      type: ociImage
      access:
        imageReference: example.com/monitoring:v0.8.3
        type: ociRegistry
...

```
Example for a source reference:

```
...
component:
  sources:
  - name: example-sources-1
    version: v1.19.4
    type: git
    access:
      commit: e01326928b6f9825dba9fa530b8d4917f93194b0
      ref: refs/tags/v1.19.4
      repoUrl: github.com/my.org/example-sources-1
      type: github
      ...
```

## References

A component version might have also references to other component versions. The semantic of component references is, that the referencing component version comprises the referenced component versions, i.e. it is an aggregation or composition semantic.

A *Component Descriptor* has a field to specify references to other *Component Descriptors* and thereby to the component versions described by them.

Example for component references:

```
component:
  componentReferences:
  - name: name-1
    componentName: github.com/.../component-name-1
    version: v1.38.3
  - name: name-2
    componentName: .../component-name-2
    version: v0.11.4
```

The lookup of references is always done by their name and version.

### Identifier for Sources, Resources and Component References

Every *source*, *resource* or *componentReference* needs a unique identifier in a *Component Descriptor*.

In particular situations the name and version are not sufficient, e.g. if docker images for different platforms are included. Therefore, every entry has an additional optional field *extraIdentity* to resolve this problem. An *extraIdentity* is a map, of key value pairs.

Example for two resource entries with the same name and version but different extra identities and therefore different identifier:

```
component:
  resources:
  - name: name-1
    version: 1.0.0
    extraIdentity:
      platform: "arm64"
    ...
  - name: name-1
    version: 1.0.0
    extraIdentity:
      platform: "x86_64"
    ...
```

## Labels

To express application specific extensions, every entry in the *sources*, *resources* and *componentReferences* fields, and the component itself may declare optional labels.

Labels are a map, of key value pairs.

Example:

```
component:
  labels:
    maintainer: "maintainer@my-component.net"
    tags: "monitoring,logging,internal"
  ...
```

## Repository Contexts

Every *Component Descriptor* has a field *repositoryContexts* containing an array of access information of *Component Descriptor Repositories*, i.e. stores for *Component Descriptors* which are specified later.

The array of access information describes the transport chain of a *Component Descriptor* through different *Component Descriptor Repositories*, whereby the last entry describes the current *Component Descriptor Repository*, in which the *Component Descriptor* is stored.

The *repositoryContexts* are usually not specified manually in the *Component Descriptor*, but are rather set automatically when a component version is uploaded to a *Component Repository*.

# Signing

Signing the component-descriptor allows to ensure that a part of the descriptor and referenced resources are identical to the authors component-descriptor. I.a., this does not include the sources field.

In order to add a signature to a component-descriptor, a digest is required at every resource and component reference as described in the next sections. With the digest information, a normalised component-descriptor can be calculated as a subset of relevant properties. The normalised component-descriptor has to be represented in a reproducable form to be hashed and signed.

## Digests

Digests are used for `componentReferences` and `resources` to indicate a hash for their content.

## Signatures

The component descriptor may have a list of signatures on root level. A signature can be identified by its name. It follows this schema:

```
signatures:
  - name: name of the signature. Used to identify the signature when verifying.
    digest: as defined, contains the digest of the normalised component-descriptor (the signing-relevant subset of the component-descriptor)
    signature:
        algorithm: signature algorithm used
        value: the signature in the format as defined in mediaType
        mediaType: defines the format of the signature.value field
```

## Normalisation of the component-descriptor

The normalisation of the component-descriptor describes the process of generating a normalised component-descriptor. A normalised component-descriptor is a subset of the component-descriptor containing signing-relevant properties only. Excluding properties from signing allows operations like transport where certain properties (e.g. image references) will change but still ensure integrity.

# Transport
In some scenarios ist is required to transfer artifacts between different locations. For example:

* deployments have to be performed in isolated environments without Internet access
* replication between locations in different regions or environments, sometimes far away.

For such scenarios it is useful to transfer delivered artifacts consistently.

## Transport Format of OCI Artifacts

Such transports are supported by definig a file system structure that represents one or more OCI artifacts.
A tar file of this file structure will be called the transport archive of the OCI artifacts.

> Clarify that the containing directory is not part of the tar file.

The file system structure consists of a directory containing:

- an `artifact-descriptor.json` file
- and a `blobs` directory.

The `blobs` directory contains the manifest, config and the layer files of all OCI artifacts under consideration
in one flat file list. In case of multi arch artifacts, the `blobs` directory can also contain index manifest files.
Every file has a filename according to its
[digest](https://github.com/opencontainers/image-spec/blob/main/descriptor.md#digests),
where the algorithm separator character is replaced by a dot (".").

The `artifact-descriptor.json` contains a list of all manifests with their tags.

The `artifact-descriptor.json`: is the entry point of the transport archive. From here the complete
network of artifacts can be resolved.

### By Value Transport
For resources referenced in non-local locations it can be chosen whether to include them ("by value")
or to keep them as references.

In a first step, all references to external resources are converted to resources of type `localBlob`.
This means two things: firstly, the resource in the component descriptor must be adjusted,
and secondly, a local blob must be added. We use the transport archive of the resource as local blob.

### Recursive Transport
A transport archive can be created for a component descriptor with keeping references as references or
including all references and the references of their references and so on (transitive closure).

For deploying a full solution in an isolated environment a transport always has to be done recursively
and by value.

Note that the transformation of external resources increases the number of layers. Hence, the
manifest of the original component (in its OCI representation) and the manifest in the transport
format are different.

```text
artifact-archive
├── artifact-descriptor.json
└── blobs
    ├── sha.123... (manifest.json)
    ├── sha.234... (config.json)
    ├── sha.345... (component descriptor)
    ├── sha.456... (local blob / transport archive of a previously external resource)
    └── sha.567... (local blob / transport archive of a previously external resource)
```

The component version appears in the archive-descriptor.json as a tag associated to the digest of the component
descriptor:

```json
{
  "manifests": [
    { "digest": "sha:345...", "tags": ["COMPONENT_VERSION"] }
  ]
}
```

#### Example of a transport archive containing two artifacts

```text
transport-archive
├── artifact-descriptor.json
└── blobs
    ├── sha256.111... (manifest.json of artifact 1)
    ├── sha256.222... (config.json   of artifact 1)
    ├── sha256.333... (layer         of artifact 1)
    ├── sha256.444... (layer         of artifact 1)
    ├── sha256.555... (manifest.json of artifact 2)
    ├── sha256.666... (config.json   of artifact 2)
    ├── sha256.777... (layer         of artifact 2)
    └── sha256.888... (layer         of artifact 2)
```

The manifest list in the `artifact-descriptor.json` contains the tags for the two manifests:

```json
{
  "manifests": [
    { "digest": "sha:111...", "tags": ["v1.25.0"] },
    { "digest": "sha:555...", "tags": ["v1.12.0"] }
  ]
}
```


## Transport Format for Other Resource Types

Whenever a new resource type is supported, a corresponding transport format must be defined.



