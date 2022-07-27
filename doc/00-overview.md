# Open Component Model Specification

The *Open Component Model (OCM)* is an open standard to describe the software artefacts which have to be delivered  
for a software products. It is explicitly not meant to describe the complete bill of material of a software product.
Compared with other standards like [CyclonDX](https://cyclonedx.org/), this makes OCM a simpler model with more detailed 
and unambiguous specifications with respect to delivery and deployment related aspects like signing. 

OCM could be used in the whole software lifecycle management, from build to compliance, to deployment
as a common basis to exchange this information between different tools and processes.

1. [Introduction](./01-introduction.md)
2. [Component Descriptor Specification](./02-component-descriptor.md)
3. [Component Repository Specification](./03-component-repository.md)
4. [Local Blobs](./04-local-blobs.md)
5. [Appendix 1: External Accessible Reference Definitions](./app01-external-references.md)

## Notational Conventions
The keywords "MUST", "MUST NOT", "REQUIRED", "SHALL", "SHALL NOT", "SHOULD", "SHOULD NOT", "RECOMMENDED", "MAY", 
and "OPTIONAL" in this document are to be interpreted as described in [RFC 2119](https://www.rfc-editor.org/info/rfc2119).
