# Core Elements of a Component Version

The following section describes how a component (version) is specified in more detail.
Please note that this section intends to give an overview and explain the principal
elements and their structure. It is not a complete specification.
See the [schemas](https://github.com/open-component-model/ocm/tree/main/resources)
for a full definition.

A component version describes artifacts, using several core elements.

- Artifacts represent technical content. They appear in two different flavors:
  - *Sources* describe the sources a component version has been composed/generated from.
  - *Resources* describe the delivery artifacts contained in a component version.
- References describe the aggregation of other component versions.

All those described elements share a common set of metadata.

## Component Identity

A *Component* is technically defined by a globally unique identifier.

The component identity uses the following naming scheme:

<div>

*&lt;DNS domain>* `/` *&lt;name component> {* `/` *&lt;name component> }*

</div>

Hereby the DNS domain plus optionally any number of leading name components MUST
be owned by the provider of a component. For example, `github.com`, as DNS domain
is shared by lots of organizations. Therefore, all component identities provided
based on this DNS name, must include the owner prefix of the providing
organization, e.g. `github.com/my-org`.

The component acts as a namespace to host multiple *Component Versions*.

A component version has a unique identity composed of the component identity
and a version name following the [semantic versioning](https://semver.org)
specification (e.g. `github.com/gardener/external-dns-management:0.15.1`).

## Artifacts (Resources and Sources)

The Open Component Model distinguishes two kinds of artifacts:
- *Sources* are optional artifacts that contain the sources, which
  were used to generate the deployment-relevant *Resources*.
- *Resources* are artifacts that finally make up the deployment-relevant set of artifacts.

An *Artifact* is a blob containing some data in a technical format.
Every artifact described by the component version has

- an *Identity* in the context of the component version
- a type representing the kind of content and how it can be used
- a set of labels
- an Access Specification to technically access the content (blob) of the artifact
- an optional digest of the artifact

Those attributes are described by formal fields in the component descriptor:

- The [element identity](./03-elements-sub.md#element-identity)
  fields are directly embedded

- **`type`** (required) *string*

  The type of an artifact  specifies the logical interpretation of an artifact
  and is independent of its concrete technical representation.

- **`labels`** (optional) *[]Label*

- **`access`** (required) *Access Specification*

  The access specification for the actual artifact (see below)


### Artifact Types

The formal type of an artifact uniquely specifies the logical interpretation of an artifact and its kind,
independent of its concrete technical representation.

If there are different possible technical representations,
the access specification determines the concrete format given by a media type used for the returned blob.

For example, a helm chart (type `helmChart`) can be represented as OCI artifact
or helm chart archive. Nevertheless, the technical meaning is the same.
In both cases the artifact (resource)`type` will be `helmChart`.
The acess specification however will be different. In the first case it will refer to the helm-chart archive.
In the second case the access method type will be `ociArtifact`.

```yaml
...
  resources:
  - name: mariadb-chart
    version: 12.2.7
    type: helmChart
    relation: external
    access:
      type: helm
      helmChart: mariadb:12.2.7
      helmRepository: https://charts.bitnami.com/bitnami
```

```yaml
...
  resources:
  - name: mariadb-chart
    version: 12.2.7
    type: helmChart
    relation: external
    access:
      type: ociArtifact
      imageReference: ghcr.io/open-component-model/helmexample/charts/mariadb:12.2.7
```

The access method type `ociArtifact` however is also used for container images:

```yaml
...
resources:
  - name: mariadb-image
    version: 10.11.2
    relation: external
    type: ociImage
    access:
      type: ociArtifact
      imageReference: bitnami/mariadb:10.11.2
```

The resource type `ociImage` now describes an object that can be used as a container image.
So, the technical representation in both cases will be an OCI image manifest.
The semantics how these objects can be used are completely different.
This is expressed by the `type` of the artifact.

An artifact's kind and logical interpretation is encoded into a simple string.
The artifact type must be globally unique. OCM defines a naming scheme to guarantee this uniqueness.

There are two kinds of types:

- Centrally defined type names managed by the OCM organization

  These types use flat names following a camel case scheme with the first character
  in lower case, for example `ociArtifact`.

  Their format is described by the following regular expression:

  ```regex
  [a-z][a-zA-Z0-9]*
  ```

- Vendor specific types

  Any organization may define dedicated types on their own.
  Nevertheless, the meaning of those types must be defined.
  There may be multiple such types provided by different organizations with the same meaning.
  Organizations should share and reuse such types instead of introducing new type names.

  To support a unique namespace for those type names vendor specific types
  MUST follow a hierarchical naming scheme based on DNS domain names.
  Every type name has to be preceded by a DNS domain owned by the providing organization,
  like `landscaper.gardener.cloud/blueprint`. The local type must follow the above rules
  for centrally defined type names and is appended, separated by a slash (`/`).

  So, the complete pattern looks as follows:

  ```
  <DNS domain name>/[a-z][a-zA-Z0-9]*
  ```

  [Artifact Types](../01-model/07-extensions.md#artifact-types) are an extension point within the OCM model.
  All existing artifact types are listed [here](../04-extensions/01-artifact-types/README.md).

## Sources

A *Source* is an artifact which describes the sources that were used to generate one or more of the resources. Source elements do not have specific additional formal attributes.

Example:

```yaml
  ...
  sources:
  - name: ocm_source
    version: 0.1.0
    type: git
    access:
      commit: 9b2cf6ced322c7b938533caa22d5a5f48105b3ab
      ref: refs/heads/main
      repoUrl: github.com/open-component-model/ocm
      type: github
```

Currently there is only one source type defined: `github`.

## Resources

A *Resource* is a delivery artifact,
intended for deployment into a runtime environment, or describing additional
content, relevant for a deployment mechanism. For example, installation procedures
or meta-model descriptions controlling orchestration and/or deployment mechanisms.

The Open Component Model makes no assumptions about how content described
by the model is finally deployed or used. This is left to external tools. Tool
specific deployment information is formally represented by other artifacts with
an appropriate type.

In addition to the common artifact information, a resource may optionally describe a reference to the source by specifying its artifact identity.

A resource uses the following additional formal fields:

- **`relation`** (required) *string['local', 'external']*
  Indicates whether the entity providing a component is also the provider of the resource ('local') or whether the 
  resource is provided by a separate entity ('external'). This may be useful to determine whether the entity responsible 
  for the component is also responsible for the resource.  
  This property is purely informational and completely unrelated to the access method type.

- **`digest`** (optional) *Digest Info*

  If the component descriptor is signed (directly or indirectly by one of its
  referencing component versions), a digest of a resource is stored along with
  the resource description. This is required because there might be different
  digest and resource normalization algorithms.

- **`srcRefs`** (optional) *list of structs*

  This field is used to describe the sources used to generate the resource.
  The selection is done by the following two fields:

    - **`identitySelector`** *map[string]string*

      Identity attributes determining an appropriate source
      element.

    - **`labels`** (optional) *[]Label*

      A list of arbitrary labels

Example:

```yaml
...
  resources:
  - name: image
    relation: external
    type: ociImage
    version: 1.0.0
    access:
      imageReference: gcr.io/google_containers/echoserver:1.10
      type: ociArtefact
```

The full list of resource types is [here](../04-extensions/01-artifact-types/README.md).

## References

A component version may refer to other component versions by adding a *reference* to the component version.

A *reference* does not have a blob, but it has:

- an *Identity* in the context of the component version
- a set of labels
- an optional digest

A `references` element has the following fields:

- **`name`** (required) *string*

  The identity of the reference in this component version

- **`componentName`** (required) *string*

  The identity of the referenced component.

- **`version`** (required) *string*

  The version of the referenced component.

- **`extraIdentity`** (optional) *map[string]string*

  The extra identity of the referenced component.

- **`labels`** (optional) see below  *[]Label*

  The extra identity of the referenced component.

- **`digest`** (optional) see below *Digest Info*

  The extra identity of the referenced component.

Example:
```yaml
...
  references:
  - name: installer
    version: 0.1.0
    componentName: github.com/open-component-model/ocmhelminstaller
```

## Summary

The OCM model describes component versions. A component version is stored in a component repository and consists of sources, resources and references. The component version itself as well as each resource, source and reference has an identity. Only sources and resources have content and therefore an access specification and an optional digest. All elements can have labels.
