# OCM Model

This chapter describes the elements and data formats the Open Component Model deals with. All implementations MUST provide a binding for those kinds of elements.

## Introduction

The Open Compoment Model consists of a core model plus extensions. The core model describes the key elements *Component*, *Component Version* being stored in *Component Registries*. *Component Versions* have a type and an identity, and consist of *sources*, *resources* and *references*. *Component Registries* are containers persisting component versions and may exist in various types for different storage technologies. Many parts of the Open-Component-Model can be extended to provide flexibility and adaption to different environments. Some of these extension are defined in this specification. Others may be defined customer-specific or for dedicated environments.

The following chapters will provide more details about these concepts.

## Components and Component Versions

Usually, complex software products are divided into logical units (called components in this specification). A component is typically maintained in a version control system. It has a build procedure generating binary artifacts from source code and a release process to make it available for consumers. Usually, releases are repeated from time to time, making new versions available. A component is a logical unit within a software product. It is a semantic bracket around software pieces belonging together because they fulfill a specific purpose. E.g. like, "This is the Frontend Component," "This is the Database component," and "This is the Kubernetes vertical autoscale component."

In the Open Component Model, a *Component Version* is described by a *Component Descriptor*. It describes the resources, sources, and aggregated other Component Versions belonging to a particular Component Version. A Component Descriptor is stored in a yaml file following this [schema](https://github.com/open-component-model/ocm/blob/main/resources/component-descriptor-ocm-v3-schema.yaml).

A component itself is described by a globally unique identity. Each component version is described by the identity of the component plus a version number following the [semantic versioning](https://semver.org) specification.

Example:

```yaml
...
component:
  name: github.com/open-component-model/echoserver  # name of this component
  version: 0.1.0                                    # version of this component
  provider:                                         # provider of this component
    name: open-component-model
```

A component version contains all artifacts required for using it, plus additional metadata. Such artifacts in OCM are called resources. Resources are usually built or packaged from something, e.g., code in a git repo. The artifacts needed for creating a component version are named *sources* in OCM.

```yaml
...
component:
  name: ...
  ...
  resources:                # -> resources making this component
  - name: image             # -> name of this resource
    version: "1.0"          # -> version of this resource
    type: ociImage          # -> type of the resource (here indicating a container image)
    relation: external      # -> resource is provided by a different entity than the component
  sources:                  # -> information about the origin (source code) of this component
  - name: echoserver_source # -> name of the source
    version: 0.1.0          # -> version of this source
    type: git               # -> type of the source (here Git repository)
```

A component version does not consist only of identities but also carries access information for the technical content behind an artifact. Therefore, given the access to a component descriptor also provides access to the content of the described artifacts (e.g. how to find an OCI image built from a Dockerfile).

```yaml
...
component:
  name: ...
  ...
  resources:
  - name: ...
    ...
    access:                # -> access information how to locate this resource
      imageReference: gcr.io/google_containers/echoserver:1.10
      type: ociArtifact
  sources:
  - name: ...
    ...
    access:                # -> access information how to locate this resource
      commit: 9b2cf6ced322c7b938533caa22d5a5f48105b3ab
      ref: refs/heads/main
      repoUrl: github.com/open-component-model/ocm
      type: github
```

A *Component Version* can also reference other *Component Versions* using their identity. In this way aggregations of components are possible. OCM does not make any assumption of the meaning of the reference. Often you will see component versions containing only references and no sources or resources. They can be used for example to describe deployments or delivery packages of software.

Example:

```yaml
...
component:
  name: ...
  ...
  componentReferences:  # -> components referenced by this component
  - name: installer     # -> name of reference in this component descriptor
    componentName: github.com/mandelsoft/ocmhelminstaller # -> name of referenced component
    version: 0.1.0      # -> version of referenced component
```

## Component Repositories

The definition of a component descriptor is not enough to provide standardized remote access for component versions and allow referencing between component versions. Therefore a *Component Repository* is the second important entity in the Open Component Model.

The component repository acts as the access point to the elements of the component model. The OCM specification does not define an access protocol but instead uses existing storage technologies and their protocol and defines a mapping from OCM elements to storage elements. The most prominent example is an [OCI registry](https://github.com/opencontainers/distribution-spec/blob/main/spec.md). Other technologies are object stores like Amazon S3 or file systems. File systems do not provide remote access but are helpful for offline scenarios and transporting component versions between locations.

A component descriptor contains references to all other elements belonging to a component version. Those elements may be stored in the same repository or in other storages. Blob content may be stored along with the component descriptor as a special case. Those blobs are called local blobs.

All repositories that can be used to store content according to the Open Component Model, need to be described by a specification.

Such a specification is usable by a language binding to gain access to this repository.
In a concrete environment all those repositories are usable, for which an
implementation of the [abstract model operations](../03-persistence/01-operations.md) exists.

A repository specification has a type, the *Repository Type*
used to identify the required [mapping](../03-persistence/02-mappings.md)
and the information required to identity a concrete repository instance.

## Summary

Component Versions are the central concept of OCM. A Component Version describes what belongs to a particular version of a software component and how to access it. This includes:

* resources, i.e. technical artifacts like binaries, docker images, ...
* sources like code in github
* references to other software component versions

Component Repositories are the persistent store for component versions. Their artifacts can be stored along their component descriptor or in other external repositories.
