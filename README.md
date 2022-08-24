
## Open Component Model (OCM)

The *Open Component Model (OCM)* is an open standard for a technology-agnostic
and machine-readable format to describe software-bill-of-deliveries (SBOD) with
the focus on the software artefacts which have to be delivered for
software products. 

It is explicitly
not meant to describe the complete bill of material of a software product
in relation to the packages those delivery artefacts are composed of.
Compared with other standards like [CyclonDX](https://cyclonedx.org/), this
makes OCM a simpler model with more detailed and unambiguous specifications
with respect to delivery and deployment related aspects like transport
and signing of software artefacts. Further information about artefacts (like
typical SBOMs) can be added using labels, additional resources or even
component versions.

It is a completely technology-agnostic model to describe artefacts and
the technical access to their content. Technology-agnostic means:

- it can describe any artefact regardless of its technology
- the artefacts can basically be stored using any storage backend technology or
  repository
- the model information can be stored using any storage backend technology or
  repository

The Open Component Model is just an interpretation layer on top of
existing storage technologies and not an own technical repository. Therefore, it
does not define an own authentication scheme, it just uses the ones defined
by the underlying storage technologies.

The only constraint for using backend storage technologies is, that there must be
- an implementation for accessing artefacts in the desired repository technology
  and map them to a blob format
- a specification for a [mapping scheme](doc/specification/layer3/README.md)
  describing how to map the elements of the component model to the supported
  elements of the backend technology
- an [implementation](doc/specification/layer2/README.md) of all the mapping
  schemes for the storage scenarios used in a dedicated environment.

By providing a globally unique identity scheme for component versions and
artefacts,
OCM could be used in the whole software lifecycle management, from build to
compliance, to deployment.
It can be used as a common basis and lingua franca to exchange, access and
transport delivery artefacts and their grouping in components as well as
information about these artefacts between different tools, processes and even
fenced environments.

To support fenced and/or private repository landscapes used to store the
artefact content, OCM provides a mechanism to transparently adapt access
information for artefacts during a transport step. Applications
accessing the component information in a dedicated environment always 
get the location specific access information valid for the actual environment. 


1 [Introduction](doc/introduction/README.md)

2 [OCM Specification](doc/specification/README.md)
  
2.1 [OCM Elements](doc/specification/layer1/README.md) <br>
2.2 [OCM Operations](doc/specification/layer2/README.md) <br>
2.3 [Storage Backend Mappings](doc/specification/layer3/README.md) <br>
2.4 [Formats and Names](doc/specification/formats/README.md) <br>
2.5 [Denotation Schemes](doc/specification/fdenotations/README.md) <br>

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

Accompanying to this specification a ready-to-go [reference implementation](https://github.com/gardener/ocm)
is provided, which supports the common environment and access types for objects
in the Kubernetes ecosystem. A (golang) library provides a framework for
adding further implementations of the [model extension points](doc/appendix/README.md) under the hood
of a generic OCM API, and a [command line tool](https://github.com/gardener/ocm/blob/main/docs/reference/ocm.md)
based on this library supports general operations, like composing, viewing, 
transporting and signing of component versions.