# Model Contract

The plain Open Component Model itself offers a solid foundation, and its true potential shines when complemented by various tools that interact with the model, enhancing its overall value.

A first example of such a tool is a transport tool. It uses the access information of resources contained in a component version to copy software artifacts from one environment into another. Resource locations will be potentially adapted for the component versions in the target environment.

Another example could be a deployment tool using component versions to determine the artifacts to be deployed into a target environments.

Such tools are out-of-scope for the OCM specification. Nevertheless, they must interact with the content described by the Open Component Model. There must be a contract between the model and the way tools interact with the model.

This contract consists of two parts:

- All content required to deploy and install software described by a component version must be included as resources in this component version.
- All resource locations (e.g. image locations) used in a runtime environment must be taken from the access information provided by the used component versions.

This has various consequences especially for deployment environments, but basically for all tools working with the component model and even the component model itself:

- Deployment descriptions MUST be part of a component version. They have to be stored as additional resources with an appropriate (tool/technology specific) artifact type. There are too many deployment technologies to define them centrally. Deploment descriptions therefore use extensions.
- Those descriptions MUST use descriptive elements of the component model to locate and access artifacts. It is not allowed to use explicit, absolute or global direct artifact locations.
- A component version MUST include all resources, either directly contained in the component version or by referring to other component versions using references. References can contain other references resulting in a graph. To avoid the need of describing always complete closed sets of artifacts in a single component version the model offers the [component reference/aggregation feature](../02-processing/01-references.md).
- The artifacts must be resolvable in the context of the component version containing this description as artifact. See also [relative artifact references](../02-processing/01-references.md#relative-artifact-references)

## Example: Helm deployment

As an example of a deployment technology, we use the [helm deployment system](https://helm.sh/) for Kubernetes.

A helm chart describes Kubernetes resources, which are templated using values provided when deploying a chart.

Typically, a helm chart contains container image references (often provided as a default value for a template variable). Using such a default value violates the above contract: the location of resources must be taken from the component version describing the deployment (the helm chart). This step is also called *image localization*: All images in a chart must be templated to be able to specify the concrete values by a deployment configuration. An OCM conformant deployment tool must provide the values from the resources of a component version.

A tool used to deploy a component version with helm therefore requires several resources:
- all the images required for the helm chart
- the helm chart
- a helm specific description containig a mapping of value names to image locations of the component version.

The OCM-compliant deploy tool (ocm-helm-adapter) must:
- take the helm chart as a resource from the component version
- know the format of the mapping description and generate the values for helm.

The deploy tool can then call the native helm command using the helm chart location from the component version and the generated helm values.

<div align="center">
<img src="ocm-helm-simple.png" alt="OCM and Helm Deployments" width="800"/>
</div>

### Example: Indirect Deployments

A deployed image may contain code to deploy pods to a Kubernetes cluster (for example, a Kubernetes operator managing some service instances). These image locations must also be taken from the component version requiring an additional indirection. For an OCM-compliant deployment, the executable of the image must accept some argument or configuration to pass these locations at runtime. The necessary mapping from resources of a component version to the configuration of the deployer executable must again be described in the description resource and processed by the adapter to generate the target configuration.

<div align="center">
<img src="ocm-helm-indirect.png" alt="OCM and Helm Deployments with indirect Deployments" width="800"/>
</div>