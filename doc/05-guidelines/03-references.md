# References

## Relative Artifact References

A composite, consisting of an artifact identity and a sequence of reference identities is called relative *Source Reference* or *Resource Reference*. It can be used in artifacts described by a component version to refer to other artifacts described by the same component version.

*Example:*

Component Version: `A:1.0.0`:

```
- resources:
  - name: DEPLOYER
  - type: mySpecialDeploymentDescription
- references:
  - name: content
    component: B:1.0.0
```

Component Version: `B:1.0.0`

```yaml
- resources:
  - name: IMAGE
    type: ociImage
```

The deployment description contained in CompVers `A:1.0.0` may have the following content

```yaml
...
deploymentImages:
  - resource:
      name: IMAGE
      referencePath:
      - name: content
```

This description contains a resource reference indicating to use the resource `IMAGE` of a component version named `content`. As the description is part of component version `A:1.0.0` `content` refers to component `B:1.0.0` when evaluated. Finally it refers to resource `IMAGE` in `B:1.0.0`.

This kind of relative access description is location-agnostic, meaning, independent of the repository context. The stored description only includes identities provided by the model. They can then be evaluated to finally obtain the artifact content (or location) in the current environment.

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
