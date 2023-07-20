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

- *recusive or non-recursive*

  If a component version should be transferred into a local environment all referenced component versions have to be transferred too. This is called a recursive transport.

- *by-value or by-reference*

  It is possible to transfer component version as they are. This means, only the
  component version meta information including the component descriptor and the local blobs are transferred, but external artifacts are kept at their current location (by reference).

  If a transport is done by-value the content of the external artifacts is transferred too.
  By default, the content is transformed to a blob representation which is stored as local blob along with the component descriptor in the target repository. Optional artifacts can be imported into its native repository format. So by default, OCI artifacts SHOULD be transferred to regular OCI artifacts if the target OCM repository is an OCI registry. In this way external tools can reference them as before (e.g. an image reference).