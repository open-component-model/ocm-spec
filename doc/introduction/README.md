
# 1 Introduction

Goal of the Open Component Model (OCM) is to provides a standard for a well-defined description of software-artifacts, their types and the access to their physical content in machine-readable manner.

## Scope

## Overview

The _Open Component Model (OCM)_ is an open standard to describe software-bill-of-deliveries (SBOD). OCM is a technology-agnostic and machine-readable format focused on the software artifacts that must be delivered for software products.

By providing a globally unique identity scheme, OCM can be employed throughout the entire software lifecycle management process, from build to compliance, to deployment.

It can be used as a common basis and lingua franca for the exchange, access and
transport of delivery artifacts between different tools, processes and environments.

To support fenced or otherwise restricted environments, OCM provides a mechanism to transparently adapt access information for artifacts during transport. This means that applications accessing the component information in a particular environment always receive location specific access information that is valid for their own environment.

OCM is a technology-agnostic model to describe artifacts and the specific means by which to access their content. In this context we understand technology-agnostic to mean the following:

- the model can describe any artifact regardless of its technology
- artifacts can be stored using any storage backend technology or repository
- the model information can be stored using any storage backend technology or repository

This can be used for:

- compliance checks
- security scanning
- code signing
- transport
- deployment or
- other lifecycle-management aspects

In that sense, the OCM provides the basis to

- exchange information about software by defining a location- and technology-agnostic reference
- enable access to local technical artifacts via these IDs
- verify the authenticity of the artifact content

OCM consists of:

* a schema describing a software component (component descriptor)
* operations to store and retrieve components and their descriptors from a registry
* methods for proofing authentity

OCM is not:

* a communication protocol (like http)
* a persistence layer (like a database)
* a tool set

## Comparison with Software-Bill-of-Materials

OCM is (explicitly) not meant to describe the complete bill of materials of a software product,
in relation to the packages those delivery artifacts are composed of. This makes OCM a simpler model in comparison with standards such as [CycloneDX](https://cyclonedx.org/). OCM provides detailed and unambiguous specifications with respect to delivery and deployment related aspects such as transport and signing of software artifacts. Further information about artifacts (like typical SBOMs) can be added using labels, additional resources or even
component versions.

## Specification
This specification is divided into three parts:

- Part 1: The [model elements](../model/README.md) defined by the Open Component Model
- Part 2: The [model operations](../operations/README.md) , which must be provided to
  interact with those model elements stored in any OCM persistence
- Part 3: The [persistence layer](../persistence‚/README.md) describing
  how the model elements are mapped to elements of an underlying persistence layer
  (for example and OCI registry)

## Notational Conventions

The keywords "MUST", "MUST NOT", "REQUIRED", "SHALL", "SHALL NOT", "SHOULD", "SHOULD NOT", "RECOMMENDED", "MAY", and "OPTIONAL" in this document are to be interpreted as described in [RFC 2119](https://www.rfc-editor.org/info/rfc2119).

## Implementation

Accompanying this specification a [reference implementation](https://github.com/open-component-model/ocm) is provided for objects in the Kubernetes ecosystem.

It consists of:

* a (Go) library provides a framework for adding further implementations
* a [command line tool](https://github.com/open-component-model/ocm/blob/main/docs/reference/ocm.md) supporting general operations, like composing, viewing, transporting and signing.
