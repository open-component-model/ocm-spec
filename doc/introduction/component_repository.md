# Component Repositories

*Component Versions* are stored in *Component Repositories*. Using a component
repository does not necessarily mean to run and operate a new technical storage
system. This specification does not define an own OCM storage technology or access
protocol but instead uses existing storage technologies and defines a [mapping](../appendix/A/README.md)
from OCM elements to storage elements, e.g. an OCI registry.

Defining such a layer allows referencing between component versions and provides
standardized remote access for component versions and the described content.

## Content stored in a Component Repository

The compont repository acts as initial access point to elements of the component
model. The root element of a component version is its description. This
description has a formalized technical representation,
the [component descriptor](../specification/elements/README.md#component-descriptor).
It describes references to all other elements belonging to a component version.
Those elements may be stored in other storage environments. As a special
case blob content may be stored along with the component descriptor. Those blobs
are called *local* blobs and are stored in the storage backend used for the
component
repository.

## Component Descriptors

A component descriptor is a technical representation of a component version. It
describes all the elements and attributes belonging to a component version in
formalized textual representation. For this representation the YAML format has
been chosen.

## Local Blobs

The central task of a component repository is to provide information about
versioned sets of resources. Therefore, a component descriptor as technical
representation of a component version describes such a set of resources. 

The description model allows referencing content stored in other rpositories,
e.g. OCI registries or S3 blob stores.

Additionally, blob content can be stored along with the component descriptor
in the storage backend used for the component repository.

This feature is especially required to support the transport of component versions
between repositories.  To provide a closed representation of the described
referenced content it must be storable as blobs together with the component
descriptor. This especially allows to represent complete component versions as
filesystem content.

## Examples

OCI Image as Local Blob:

```yaml
...
resources:
  - name: example-image
    type: oci-image
    access:
      type: localBlob
      mediaType: application/vnd.oci.image.manifest.v1+json
      localReference: "digest: sha256:b5733194756a0a4a99a4b71c4328f1ccf01f866b5c3efcb4a025f02201ccf623"
      globalAccess:
        imageReference: somePrefix/test/monitoring@sha:...
        type: ociRegistry
...
```

Helm Chart as Local Blob:

```yaml
resources:
  - name: example-name
    relation: local
    type: helm.io/chart
    version: v0.1.0
    access:
      localReference: <identifier/digest of the local blob>
      type: localBlob
```