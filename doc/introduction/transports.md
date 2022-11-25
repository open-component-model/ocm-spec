# Transport of Component Versions

In some scenarios ist is required to transfer artifacts required to install a software product in different locations. For example:

* deployments have to be performed in isolated environments without Internet access
* replication between locations in different regions or environments, sometimes far away.

For such scenarios it is required to transfer delivered artifacts consistently.
You need a reliable list of delivery artifacts required at the target side to install
the software product.

What a coincidence, this is exactly what is describes by the Open Component Model.
Following the transitive component version references of a root [component version](component_versions.md) describing your software product, a complete list of the required artifacts cabe be determined.

Therefore, the description model provided by OCM can easily be used to provide
a transport tool, able to transport the complete closure of a component version from
one environment to another. To support this, a component version includes the
access information for the described artifacts. This can be used by the transport 
tool to access the content and to provide it in the target environment.
If no applicable storage system for the dedicated artifact type according to its
access method, it can be stored as local blob along with the component descriptor 
directly in the [component repository](component_repository.md).
The descriptor version store din the target repository has to be adapted accordingly 
to reflect the new environment-local locations of the described artifacts.
This is a special feature of the OCM, to provide modifiable access information for 
the described artifacts.

The transport target might even be an [archive or filesystem directory](../appendix/A/CTF/README.md).
This enables the transport of OCM content into fenced environments via a portable
data storage medium (e.g USB stick).

A transport might be done in several ways

- recusive or non-recursive.

  If a component version should be transferred into a local environment all
  referenced versions have to be transferred, also. Therefore, a recursive transport
  is required.

- artifacts by-value or by-reference.

  It is possible to transfer component version as they are. This means, only the 
  component version meta information including the component descriptor and the already existing local blobs are transferred, but referenced artifacts are kept in their locations.
  If the transport is done by-value the content of the referenced artifacts is transferred, also.
  By default, the content is transformed to a blob representation which is stored as [local blob](component_repository.md#local-blobs) along with the component descriptor in the target repository.

  Via upload handlers, it is possible to propagate imported content into its native
  repository technologies. By default, OCI artifacts will be transferred to regular OCI artifacts, again, if the target OCM repository is based on an OCI registry.