# References

## Relative Artifact References

A composite, consisting of an artifact identity and a sequence of reference identities is called relative *Source Reference* or *Resource Reference*. It can be used in artifacts described by a component version to refer to other artifacts described by the same component version.

*Example:*

Component Version: `A:1.0.0`:

```yaml
apiVersion: ocm.software/v3alpha1
kind: ComponentVersion
metadata:
  name: github.com/acme/A
  version: 1.0.0
  ...
spec:
  resources:
    name: DEPLOYER
    type: mySpecialDeploymentDescription
    ...
  - access:
      ...
  references:
  - name: ref_to_b
    componentName: github.com/acme/B
    version: 1.0.0
...
```

Here we define a component version `A` with a resource having a custom type. Furthermore it references a component `B` and names this reference `ref_to_b`.

Then we have a second component `B:1.0.0` with on OCI image resource:

```yaml
apiVersion: ocm.software/v3alpha1
kind: ComponentVersion
metadata:
  name: github.com/acme/B
  version: 1.0.0
  ...
spec:
  resources:
    name: IMAGE
    type: ociImage
    ...
  - access:
      ...
...
```

The deployment description contained in `A` has a proprierty format unnknown to OCM. It is used by  some deployment tooling interpreting this description. For example it may have the following content:

```yaml
# Deployment description in 'mySpecialDeploymentDescription' format:
...
deploymentImages:
  - resource:
      name: IMAGE
    referencePath:
    - name: ref_to_b
```

This description contains a resource reference indicating to use the resource named `IMAGE` of some component version. As the description is part of component version `A:1.0.0`, `content` is resolved by checking the named references in `A`. The reference named `ref_to_b` refers to component `B:1.0.0`. Looking up the resources of `B` a resource named `IMAGE` can be found.

This mechanism can be also used for multiple level of indirections:

```yaml
# Deployment description in 'mySpecialDeploymentDescription' format:
...
deploymentImages:
  - resource:
      name: IMAGE
    referencePath:
    - name: ref_to_b
      name: ref_to_c
      name: ref_to_d
```

In this case component `A` would have a reference `ref_to_b` as before. `B` would then contain another reference named `ref_to_c` pointing to another component, e.g. `C:1.0.0`. `C` would contain a reference named `ref_to_d` pointing, e.g. to `D:1.0.0`. `D` then would contain a resource named `IMAGE`.

This kind of relative access description is location-agnostic, meaning, independent of the repository context. The stored description only includes identities provided by the model. They can then be evaluated to finally obtain the artifact content (or location) in the current environment.

It is important that this referencing mechanism is not resolved by the OCM tooling. It is the purpose of the deploment tool to resolve this. It is pure convention to follow this pattern. As referencing resources however is a common problem occuring in many scenarios it is recommended to use a common schema.

## Absolute Artifact References

A relative reference can be extended to an location-agnostic absolute reference by extending
the pair by a third value, a component version identity.

<div align="center">

( *&lt;Component Version>* , *&lt;Reference Path> {* , *&lt;Local Artifact Identity> }* )

</div>

A reference can again be transferred into a location-specific reference by adding a repository-context.

Such a reference can then be used to finally address the content of this artifact by the
following procedure:

- gain access to the OCM repository described by the repository context.
- gain access to the component version, respectively the component descriptor, by a lookup operation
- follow the resolution procedure for the relative artifact reference.
