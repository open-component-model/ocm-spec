# Component Versions

Usually, complex software products are divided into logical units, which are called **components** in this specification. For example, a software product might consist of three components, a frontend, a backend and some monitoring stack. Of course, the software product itself can be seen as a component comprising the other three components.

As a result of the development phase, **component versions** are created, e.g. when you make a new release of a component.

The *component* itself just describes a globally unique identity with a dedicated 
meaning (the purpose a dedicated version of this component can be used for). The 
*component version* describes dedicated versions of a component with all the
concrete artifact required to install this version.

In this sense a component version is a software-bill-of-delivery (SBOD). It describes
delivery and installation artifacts together with metadata. It does not contain
formal descriptions of the decomposition of such artifacts, like packages or modules
used to compose/build an artifact (typically meant with the term SBOM).

A component version consists of a set of [technical artifacts](../specification/elements/README.md#artifact-access), e.g. Docker images, Helm charts, binaries, configuration data etc. Such artifacts are called [**resources**](../specification/elements/README.md#resources).
Resources are usually build or packaged from something, e.g. code in a git repository,  named [**sources**](../specification/elements/README.md#sources).

In the Open Component Model a component version is described by a [**Component Descriptor**](../specification/elements/README.md#component-descriptor). 
It describes the resources, sources and aggregated other component versions belonging to a particular component version.

It not only describes identities for contained artifacts, but the real truth, by 
additionally carrying access information for the technical content behind an artifact. Therefore, given the access to a component descriptor also provides access
to the content of the described artifacts.

The model definition provides means to handle the [transport](transports.md) of
component versions from one environment into another by adapting the artifact 
access information, accordingly, without invalidation potential signatures. Therefore, the access information given by
a component descriptor always provides environment local information, which
enables tools working (e.g. deployment tools) with it to always access described
artifacts from locations applicable for the actual environment.

For the three components in our sample software product mentioned above, one component descriptor exists for every component version, the frontend, backend and monitoring stack.

Not all component version combinations of frontend, backend and monitoring are compatible and build a valid product version. In order to define reasonable version combinations for our software product, we could use the aggregation feature of the component version, which allows referencing other component versions.

For our example we could introduce a component for the overall software product. A particular version of this product component is again described by a component descriptor, which contains references to particular component version for the frontend, backend and monitoring stack.

This is only an example how to describe a particular product version with OCM as a component with one version with references to versions of other components, which itself could have such references and so on. You are not restricted to this approach, i.e. you could still just maintain a list of component version combinations which build a valid product release. But OCM provides you a simple approach to specify what belongs to a product version. Starting with the Component Descriptor for a product version and following the component references, you could collect all artifacts, belonging to this product version.

**Summary:** \
*Component Versions* are the central concept of OCM. A *Component Version* describes what belongs to a particular version of a software component and how to access it. This includes:

- resources, i.e. technical artifacts like binaries, Docker images, ...
- sources like code in GitHub
- references to other software component versions

### Component Name and Version

Every *Component Version* has a name and version, also called component name and component version. Name and version are the identifier for a *Component Version* and therefor for the artifact set described by it.

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

# Signing

Signing a component version allows to ensure to ve able to verify the authenticity and integrity of the content described by a component version.

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

## Example for a complete Description of a Component Version

```yaml
# Example for a signed component descriptor containing three resources and one reference
meta:
  configuredSchemaVersion: v2
component:
  name: github.com/open-component-model/ocmechoserver  # name of this component
  version: 0.1.0-dev                                   # version of this component
  provider:                                            # provider of this component
    name: open-component-model
  repositoryContexts: # -> origin of this document
  - baseUrl: ghcr.io
    componentNameMapping: urlPath
    subPath: jensh007/ctf
    type: OCIRegistry
  componentReferences:  # -> components referenced by this component
  - componentName: github.com/mandelsoft/ocmhelminstaller # -> name of referenced component
    name: installer    # -> name of reference in this component descriptor
    version: 0.1.0-dev # -> version of referenced component
    digest:            # -> digest used for signing this referenced component
      hashAlgorithm: sha256
      normalisationAlgorithm: jsonNormalisation/v1
      value: d1871d98a6b9ec11b562895efccdcb8b8f87d8dcb81eabc40cad4d9b68f0ea36
  resources: # -> resources making this component
  - name: image         # -> name of this resource
    version: "1.0"      # -> version of this resource
    type: ociImage      # -> type of the resource (here indicating a container image)
    relation: external  # -> located in an external registry
    access:             # -> access information how to locate this resource
      imageReference: gcr.io/google_containers/echoserver:1.10
      type: ociArtifact
    digest:             # -> digest of this resource used for signing
      hashAlgorithm: sha256
      normalisationAlgorithm: ociArtifactDigest/v1
      value: cb5c1bddd1b5665e1867a7fa1b5fa843a47ee433bbb75d4293888b71def53229
  - name: chart         # -> name of this resource
    version: 0.1.0-dev  # -> version of this resource
    type: helmChart     # -> type of the resource (here indicating a Helm chart)
    relation: local     # -> located in the local registry
    access:             # -> access information how to locate this resource
      imageReference: ghcr.io/jensh007/ctf/github.com/open-component-model/ocmechoserver/echoserver:0.1.0
      type: ociArtifact
    digest:             # -> digest of this resource used for signing
      hashAlgorithm: sha256
      normalisationAlgorithm: ociArtifactDigest/v1
      value: 385531bf40fc2b93e1693c0270250deb8da488a8f6f8dcaa79b0ab2bf1041c0b
  - name: package      # -> name of this resource
    version: 0.1.0-dev # -> version of this resource
    type: toiPackage   # -> type of the resource (here indicating a custom tyoe)
    relation: local    # -> located in the local registry
    access:            # -> access information how to locate this resource
      globalAccess:
        digest: sha256:57563cb451bb79eb1c4bf0e71c66fdad1daf44fe55e128f12eae5f7e5496a188
        mediaType: application/vnd.toi.ocm.software.package.v1+yaml
        ref: ghcr.io/jensh007/ctf/component-descriptors/github.com/open-component-model/ocmechoserver
        size: 615
        type: ociBlob
      localReference: sha256:57563cb451bb79eb1c4bf0e71c66fdad1daf44fe55e128f12eae5f7e5496a188
      mediaType: application/vnd.toi.ocm.software.package.v1+yaml
      type: localBlob
    labels:            # -> labels on this resource as key-value pairs
    - name: commit
      value: 9b2cf6ced322c7b938533caa22d5a5f48105b3ab
    digest:            # -> digest of this resource used for signing
      hashAlgorithm: sha256
      normalisationAlgorithm: genericBlobDigest/v1
      value: 57563cb451bb79eb1c4bf0e71c66fdad1daf44fe55e128f12eae5f7e5496a188
  sources:  # -> information about the origin (source code) of this component
  - name: echoserver_source # -> name of the source
    version: 0.1.0-dev      # -> version of this source
    type: git               # -> type of the source (here Git repository)
    access:                 # -> access information how to locate this resource
      commit: 9b2cf6ced322c7b938533caa22d5a5f48105b3ab
      ref: refs/heads/main
      repoUrl: github.com/open-component-model/ocm
      type: github
signatures: # -> signing information using cryptographic signatures
- name: mysig # -> name of this signature
  digest: # -> digest of this signature including used algorithm
    hashAlgorithm: sha256
    normalisationAlgorithm: jsonNormalisation/v1
    value: cf08abae08bb874597630bc0573d941b1becc92b4916cbe3bef9aa0e89aec3f6
  signature:  # -> signature including used algorithm
    algorithm: RSASSA-PKCS1-V1_5
    mediaType: application/vnd.ocm.signature.rsa
    value: 390157b7311538bc50e31d126b413b49e2ec85a6bc16a4fe6a27fbc9f9b6f89bc9ac48091beff3d091a9eb0a62a35e0eb2b6f5ab35c3cdde6cfad3437d660894ecc9a4e42cc4664ade28e74c478d69fe791d18b81fb31ee6c5633a9ea2543e868281dd6de6d29b68200ba135fd5718b3fc0ac1cd437910d06c9a88753e00b7e5b778bf52d668a5e20e0f857702c5c03abc42933af2af00b701722c50835bc5f9d85fd523654647e49dccdede1e17f20e4a6b30037d3d151e08c58c2aabe638028dbfddbd4a63e4efb07983631e1cb98902677e7e17b9e5192d4a6c178ec694eaa260f7a7845378019ce3368082c466a4ff54d823191f44db61b7aa75ab2705d6
```


