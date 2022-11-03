# Open Component Model (OCM)

## Overview

The *Open Component Model (OCM)* is an open standard to describe software-bill-of-deliveries (SBOD). OCM is a technology-agnostic and machine-readable format focused on the software artifacts that must be delivered for software products.

By providing a globally unique identity scheme, OCM can be employed throughout the entire software lifecycle management process, from build to compliance, to deployment.

It can be used as a common basis and lingua franca for the exchange, access and
transport of delivery artifacts between different tools, processes and environments.

To support fenced or otherwise restricted environments, OCM provides a mechanism to transparently adapt access information for artifacts during transport. This means that applications accessing the component information in a particular environment always receive location specific access information that is valid for their own environment.

OCM is a technology-agnostic model to describe artifacts and the specific means by which to access their content. In this context we understand technology-agnostic to mean the following:

- the model can describe any artifact regardless of its technology
- artifacts can be stored using any storage backend technology or repository
- the model information can be stored using any storage backend technology or repository

## Comparison with Software-Bill-of-Materials

OCM is (explicitly) not meant to describe the complete bill of materials of a software product,
in relation to the packages those delivery artifacts are composed of. This makes OCM a simpler model in comparison with standards such as [CycloneDX](https://cyclonedx.org/). OCM provides detailed and unambiguous specifications with respect to delivery and deployment related aspects such as transport and signing of software artifacts. Further information about artifacts (like typical SBOMs) can be added using labels, additional resources or even
component versions.

## Storage Technology

The Open Component Model is an interpretation layer on top of existing storage technologies and is not itself a repository technology. Therefore, it does not define an authentication scheme but, rather, uses those defined by the underlying storage technology.

To use a backend storage technology as an OCM repository it is necessary to provide:
- an implementation for accessing artifacts in the desired backend and mapping them to a blob format
- a specification for a [mapping scheme](doc/specification/mapping/README.md)
  describing how to map the elements of the Open Component Model to the supported
  elements of the backend storage technology
- an [implementation](doc/specification/operations/README.md) of all the mapping
  schemes for the storage scenarios used in a dedicated environment

## Specification

1 [Introduction](doc/introduction/README.md)

1.1 [Component Descriptor](doc/introduction/01_component_descriptor.md)<br>
1.2 [Component Repository](doc/introduction/02_component_repository.md)<br>

2 [OCM Specification](doc/specification/README.md)

2.1 [OCM Elements](doc/specification/elements/README.md) <br>
2.2 [OCM Operations](doc/specification/operations/README.md) <br>
2.3 [Storage Backend Mappings](doc/specification/mapping/README.md) <br>
2.4 [Formats and Names](doc/specification/formats/README.md) <br>
2.5 [Denotation Schemes](doc/specification/denotations/README.md) <br>

3 [Scenarios](doc/scenarios/README.md) <br>

[Glossary](doc/glossary.md) <br>

[Appendix:](doc/appendix/README.md) <br>

[A. Storage Backend Mappings](doc/appendix/A/README.md) <br>
[B. Access Method Types](doc/appendix/B/README.md) <br>
[C. Resource Types](doc/appendix/C/README.md) <br>
[D. Labels](doc/appendix/D/README.md) <br>

## Notational Conventions

The keywords "MUST", "MUST NOT", "REQUIRED", "SHALL", "SHALL NOT", "SHOULD", "SHOULD NOT", "RECOMMENDED", "MAY",
and "OPTIONAL" in this document are to be interpreted as described in [RFC 2119](https://www.rfc-editor.org/info/rfc2119).

## Model Support

Accompanying to this specification a ready-to-go [reference implementation](https://github.com/open-component-model/ocm)
is provided, which supports the common environment and access types for objects
in the Kubernetes ecosystem. A (Go) library provides a framework for
adding further implementations of the [model extension points](doc/appendix/README.md) under the hood
of a generic OCM API, and a [command line tool](https://github.com/open-component-model/ocm/blob/main/docs/reference/ocm.md)
based on this library supports general operations, like composing, viewing,
transporting and signing of component versions.

## Contributing

Code contributions, feature requests, bug reports, and help requests are very welcome. Please refer to the [Contributing Guide in the Community repository](https://github.com/open-component-model/community/blob/main/CONTRIBUTING.md) for more information on how to contribute to OCM.

OCM follows the [CNCF Code of Conduct](https://github.com/cncf/foundation/blob/main/code-of-conduct.md).
