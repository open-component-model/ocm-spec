# A. Storage Backend Mappings for the Open Component Model

The OCM specification describes an interpretation layer on-top of
well-known storage backend technologies used to store
[OCM component versions](../../specification/elements/README.md#component-versions).

Therefore, for every storage technology a dedicated mapping 
must be defined to ensure interoperability of different
OCM implementations.

These mappings describe:
- the repository specification [type](../../specification/formats/types.md#repository-types)
  and format used to specify a dedicated repository instance
- the mapping of the [OCM elements](../../specification/elements/README.md) 
  to the elements provided by the storage technology.

Mappings for the following technologies are defined:

- [OCIRegistry](OCIRegistry/README.md) OCM content in OCI registries
- [FileSystem (CTF)](CTF/README.md) OCM content as filesystem structure
- [AWS S3](S3/README.md)OCM content in AWS S3 buckets

## Transport of Artefact Content

A [transport](../../introduction/transports.md) of a [component version](../../specification/elements/README.md#component-versions)
from one [component repository](../../introduction/component_repository.md) into 
another one can be done in several ways:

- directly from an OCM repository to another one: To support transport by value
  requires the availability of a blob state in the target environment.
- indirectly using an intermedite file based format: This format must be capable
  to store blobs that have to be transported side-by-side with the component
  descriptors. In this format the component descriptor must be capable to
  describe the access to those locally stored blobs.

To simplify and unify the handling of those two scenarios, and generally the
handling of blobs in various environments, a component repository must also
include support for storing blobs under the identity of the component
descriptor. A repository implementation may forward this task to a predefinied
other blob store or handle this part of the API in its own way.

This enables:

- a simple usage of a component repository to store any content without the need
  of always requiring other externals stores for (possibly specific types of)
  resources. (for example for storing sinmple configuration data along with the
  component descriptor)
- providing a respository implementation for filesystem formats that can
  transparently be used by component tools.
- the usage of a minimal repository environment on the target side of a
  transport by just using a dedicated component repository.

Therefore, *Component Repositories* MUST provide the possibility to store
technical artefacts together with the component descriptors in the component
repository itself as so-called *local blobs*. Therefore, a dedicated general
access type [`localBlob`](../B/localBlob.md)is used that MUST be implemented by all 
repository implementations. This also allows to pack all component versions with their
technical artefacts in a *Component Repository* as a completely self-contained
package, a typical requirement if you need to deliver your product into a fenced
landscape.

As a short example, assume some component needs additional configuration data
stored in some YAML file. If in some landscape of your transport chain there is
only an OCI registry available to store content, then you need to define a
format how to store such a YAML file in the OCI registry. With *local blobs* you
could just upload the file into the *Component Repository*.

