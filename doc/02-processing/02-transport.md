# Transport

In some scenarios it is required to transfer artifacts to a different location. For example:

* deployments have to be performed in isolated environments without Internet access
* replication between locations in different regions or environments, sometimes far away.

It is required to transfer delivered artifacts consistently.

The description model provided by OCM can be used to provide a transport tool being able to transfer the complete closure of a component version from one environment to another.

To support this, a component version includes the access information for the described artifacts. If no applicable storage system for an artifact type according to its access method is available it can be stored as local blob along with the component descriptor.

The descriptor stored in the target repository has to be adapted accordingly  to reflect the new ocal location. In this way OCM allows to provide modifiable access information for artifacts.

The transport target might even be an archive or filesystem. This enables the transport of OCM content into fenced environments via data storage media (e.g USB stick).

A transport might be done with various options:

- *recursive or non-recursive*

  If a component version should be transferred into a local environment all referenced component versions have to be transferred too. This is called a recursive transport.

- *by-value or by-reference*

  It is possible to transfer component version as they are. This means, only the
  component version meta information including the component descriptor and the local blobs are transferred, but externally referenced artifacts are kept at their current location (by reference).

  If a transport is done by-value the content of the external artifacts is transferred too.
  By default, the content is transformed to a blob representation which is stored as local blob along with the component descriptor in the target repository. Optional artifacts can be imported into its native repository format. So by default, OCI artifacts SHOULD be transferred to regular OCI artifacts if the target OCM repository is an OCI registry. In this way external tools can reference them as before (e.g. an image reference).

## Kinds of Transports

A transport of a component version from one component repository into another one can be done in several ways:

- directly from an OCM repository to another one: To support transport by value requires the availability of a blob state in the target environment.
- indirectly using an intermediate file based format: This format must be capable to store blobs that have to be transported side-by-side with the component descriptors. In this format the component descriptor must be capable to describe the access to those locally stored blobs.

To simplify and unify the handling of those two scenarios, and generally the handling of blobs in various environments, a component repository must also include support for storing blobs under the identity of the component descriptor. A repository implementation may forward this task to a predefinied other blob store or handle this part of the API in its own way.

This enables:

- a simple usage of a component repository to store any content without the need of always requiring other externals stores for (possibly specific types of) resources. (for example for storing sinmple configuration data along with the component descriptor)
- providing a respository implementation for filesystem formats that can transparently be used by component tools.
- the usage of a minimal repository environment on the target side of a transport by just using a dedicated component repository.

Therefore, *Component Repositories* MUST provide the possibility to store technical artifacts together with the component descriptors in the component repository itself as so-called *local blobs*. Therefore, a dedicated general access type `localBlob` is used that MUST be implemented by all repository implementations. This allows packing all component versions with their technical artifacts in a *Component Repository* as a completely self-contained package.

As a short example, assume some component needs additional configuration data stored in some YAML file. If in some landscape of your transport chain there is only an OCI registry available to store content, then you need to define a format how to store such a YAML file in the OCI registry. With *local blobs* you could just upload the file into the *Component Repository*.

