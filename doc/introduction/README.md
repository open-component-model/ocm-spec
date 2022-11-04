# 1 Introduction

The definition, structure and management of software in larger enterprises often builds upon tools and processes, which
largely originate from former on-premise thinking and monolithic architectures. Development teams responsible for
solutions or services have built specific, often point-2-point integrations with CI/CD systems, compliance tools,
reporting dashboards or delivery processes in the past. Larger development teams might have even built their own
toolsets specifically for their products, including those needed for compliance handling and delivery automation.
These concepts, process integrations and resulting tools are often still in use today, even though everyone knows:
They don't fit into today's cloud world.

The result is a fragmented set of homegrown specific tools across products, solutions and services, affecting an
enterprises' ability to deliver software consistently and compliant to its own or customer operated target environments.
These specific, overly complex and thus hard to understand CI/CD pipelines, and the inability to instantly
provide a holistic aggregated view of currently running technical artifacts for each and every production environment
(including both cloud and on-premise), result in the overall management of software at scale becoming tedious, error-prone
and ineffective.

## Why is this a huge problem?

Most prominently, with the general un-alignment of how software is defined and managed,
it is not possible without additional overhead (like setting up even more processes and tools on top) to manage
the complete lifecycle of all solutions, services or individual deployment artifacts running in any
given landscape. Even worse, when trying to set up new landscapes, it becomes a nightmare to successfully orchestrate,
deploy and configure the needed software components in the new environments.

As long as individual development teams within a company continue to use their own tools and processes to manage the
lifecycle of the software they are responsible for, this unsatisfying (and finally TCD and TCO affecting) situation can
not improve and will only get worse over time.

## How can this improve?
The major problem at hand here is the absence of one aligned software component model, consistently used across the
enterprise, to manage compliant software components and their technical artifacts. Such
a model would help not only with streamlined deployments to public and private cloud environments, but also in various
other areas of lifecycle management like compliance processes and reporting. This software component model must describe
all technical artifacts of a software product, and establish an ID for each component, which should then consistently be
used across all lifecycle management tasks.

Here, it is also crucial to understand that setting up local environments often requires the use of artifacts stored local to the environment.
This is especially true for restricted or private clouds, in which it is usually not possible to access artifacts from
their original source location (due to restricted internet access), leading to the fact that artifacts need to be
transported into these environments. This local deployment scenario requires that software components must clearly
separate their ID from the location of their technical artifacts, so that this technical location may change, without
changing the ID. At the same time the environment-local location of the artifacts must be retrievable using this identity.

At its heart, the model has to be technology-agnostic, so that not only modern containerized cloud software,
but also legacy software is supported, out-of-the-box. It simply has to be acknowledged that companies are not able to
just drop everything that has been used in the past and solely use new cloud native workloads. This fact makes it
crucial to establish a common component model, which is able to handle both cloud native and legacy software, for which
it needs to be fully agnostic about the technology used.

Additionally, the model needs to be easily extensible. No one is able to
predict the future, apart from the fact that things will always change, especially in the area of IT. Being able to
adapt to future trends, without constantly affecting the processes and tools responsible for the core of the lifecycle
management of software, is a must.

## Scope

Operating software installations/products, both for cloud and on-premises, covers many aspects:

- How, when and where are the technical artifacts created?
- How are technical artifacts stored and accessed?
- Which technical artifacts are to be deployed?
- How is the configuration managed?
- How and when are compliance checks, scanning etc. executed?
- When are technical artifacts deployed?
- Where and how are those artifacts deployed?
- Which other software installations are required and how are they deployed and accessed?
- etc.

The overall problem domain has a complexity that makes it challenging to be solved as a whole.
However, the problem domain can be divided into two disjoint phases:

- production of technical artifacts
- deployment and lifecycle management of technical artifacts

The produced artifacts must be stored somewhere such that they can be accessed and collected for the deployment.
The OCM defines a standard to describe which technical artifacts belong to a software installation and how to
access them which could be used at the interface between production and the deployment/lifecycle management phase.

The OCM provides a common standard for the coupling of
- compliance checks
- security scanning
- code signing
- transport
- deployment or
- other lifecycle-management aspects
based on a well-defined description of software-artifacts, their types and the access to their physical content.

In that sense, the OCM provides the basis to
- exchange information about software in a controlled manner by defining a location- and technology-agnostic reference
  framework to identify software artifacts
- enable access to local technical artifacts via these IDs
- verify the authenticity of the artifact content found in an actual environment.

If software installations are described using the OCM, e.g. a scanning tool could use this to collect all technical
artifacts it needs to check and store findings under the globally unique and location-agnostic identities provided by the model.
This information can be stored along with the component versions and exchanged with other tools without loosing its meaning.
If the technical resources of different software installations are described with different
formalisms, such tools must provide interfaces and implementations for all if them and data exchange becomes a nightmare.

This problem becomes even harder if a software installation is build of different parts/components, each described with
another formalism. OCM allows a uniform definition of such compositions such that one consistent description of
a software installation is available.

The identity scheme provided by the OCM acts as some kind of Lingua Franca, enabling
a tool ecosystem to describe, store and exchange information even across environments without
loosing its meaning in relation to the described software artifacts and groupings.

The core OCM does not make any assumptions about the

- kinds of technical artifacts (e.g. docker images, helm chart, binaries etc., git sources)
- technology how to store and access technical artifacts (e.g. as OCI artifacts in an OCI registry)

OCM is a technology-agnostic specification and allows [implementations](../specification/extensionpoints/README.md) to provide support
for exactly those technical aspects as an extension of the basic model. The description formalism is even valid and can (at least partly)
formally processed, if not all specified aspects are covered by an actual implementation.

# Example
The following example illustrates the concepts of a component descriptor. The [specification chapter](../specification/README.md) provides the details about the elements and their operations.

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
      type: ociArtefact
    digest:             # -> digest of this resource used for signing
      hashAlgorithm: sha256
      normalisationAlgorithm: ociArtifactDigest/v1
      value: cb5c1bddd1b5665e1867a7fa1b5fa843a47ee433bbb75d4293888b71def53229
  - name: chart         # -> name of this resource
    version: 0.1.0-dev  # -> version of this resource
    type: helmChart     # -> type of the resource (here indicating a helm chart)
    relation: local     # -> located in the local registry
    access:             # -> access information how to locate this resource
      imageReference: ghcr.io/jensh007/ctf/github.com/open-component-model/ocmechoserver/echoserver:0.1.0
      type: ociArtefact
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
