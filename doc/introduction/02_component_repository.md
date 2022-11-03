# Component Repository Specification

*Component Descriptors* are stored in *Component Repositories*. Defining a storage layer allows referencing between component descriptors and provides a standardized remote access.

This specification does not define an OCM storage technology or access protocol but instead uses existing storage technologies and defines a [mapping](../appendix/A/README.md) from OCM elements to storage elements, e.g. an OCI registry.

## Local Blobs

The central task of a component repository is to provide information about versioned sets of resources. Therefore, a component descriptor as technical representation of a component version describes such a set of resources. This explicitly includes access information, a formal description to describe a technical access path. For the component model those resources are just seen as simple typed blobs. This enables to formally reference blobs in external environments, as long as the described method is known to the consuming environment. The evaluation of an access specification always results in a simple blob representing the content of the described resource. This way basically all required blobs can be stored in any supported external blob store.

When using the component repository to transport content from one repository the another one (possibly behind a firewall without access to external blob repositories), the described content of a component version must be transportable by value together with the component descriptor. Therefore the access information stored along with the described resoures may change over time or from environment to environment. But all
variants must describe the same technical content.

Such a tranport can be done in several ways:

- directly from an OCM repository to another one: To support transport by value requires the availability of a blob state in the target environment.
- indirectly using an intermedite file based format: This format must be capable to store blobs that have to be transported side-by-side with the component descriptors. In this format the component descriptor must be capable to describe the access to those locally stored blobs.

To simplify and unify the handling of those two scenarios, and generally the handling of blobs in various environments, a component repository must also include support for storing blobs under the identity of the component descriptor. A repository implementation may forward this task to a predefinied other blob store or handle this part of the API in its own way.

This enables:

- a simple usage of a component repository to store any content without the need of always requiring other externals stores for (possibly specific types of) resources. (for example for storing sinmple configuration data along with the component descriptor)
- providing a respository implementation for filesystem formats that can transparently be used by component tools.
- the usage of a minimal repository environment on the target side of a transport by just using a dedicated component repository.

Therefore, *Component Repositories* MUST provide the possibility to store technical artifacts together with the *Component Descriptors* in the *Component Repository* itself as so-called *local blobs*. Therefore a dedicated general access type `localBlob` is used that MUST be implemented by all repository implementations. This also allows to pack all component versions with their technical artifacts in a *Component Repository* as a completely self-contained package, a typical requirement if you need to deliver your product into a fenced landscape.

As a short example, assume some component needs additional configuration data stored in some YAML file. If in some landscape of your transport chain there is only an OCI registry available to store content, then you need to define a format how to store such a YAML file in the OCI registry. With *local blobs* you could just upload the file into the *Component Repository*.

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
      annotations:
        name: test/monitoring
      localAccess: "digest: sha256:b5733194756a0a4a99a4b71c4328f1ccf01f866b5c3efcb4a025f02201ccf623"
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
      digest: <identifier/digest of the local blob>
      type: localBlob
```