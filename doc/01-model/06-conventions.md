# Conventions

To ensure uniformity across tools that interact with content from the component model,
certain conventions should be adhered to.

These conventions are not covered by the [model-tool contract](../05-guidelines/02-contract.md#model-contract).
They are also not part of the specifications but should be obeyed
to achieve a common understanding about the meaning of content.

## Intended Environments

There are several scenarios where artifacts will be provided as content of [component versions](./02-elements-toplevel.md), which might be bound to a dedicated runtime environment. If a component version should provide several flavors of the same artifact intended for different environments they should use the same element name and version, and the environment should be reflected by one or more [extra identity properties](./03-elements-sub.md#element-identity).

### Operating System and CPU Architecture

For executables and container images the specification for [OCI image indices](https://github.com/opencontainers/image-spec/blob/main/image-index.md#image-index-property-descriptions) should be used.

The following extra identity properties are defined:

- **`os`**: the operating system the element is intended for. It SHOULD use values listed in the Go Language document for [GOOS](https://go.dev/doc/install/source#environment).
- **`architecture`**: the CPU architecture the element is intended for. It should use values listed in the Go Language document for [GOARCH](https://go.dev/doc/install/source#environment).

This convention is also used by the OCM command line command [ocm download resource -x ...](https://github.com/open-component-model/ocm/blob/main/docs/reference/ocm_download_resources.md) to download an executable for the actual runtime environment.

If platform specific images are described as separate resources instead of using a multiarch image, these extra identities should also be used.

## Selection of Usage Scenarios

Usage scenarios for sets of described artifacts are best described by a dedicated description artifact with a dedicated tool-specific artifact type. Here, there is the complete freedom to describe the conditions and environments artifacts are to be used. The artifacts are described by [relative resource references](../05-guidelines/03-references.md#relative-artifact-references) in relation to the component version containing the description artifact.

Another possibility is to use dedicated [labels](./03-elements-sub.md#labels) to describe the usage scenario for dedicated artifacts. Here, the tool working on a component versions does not read a description artifact, but has to analyse the label settings of all the provided artifacts. In both cases there is a dedicated OCM specific interpretation of content provided by the component model. But while the first solution allows to describe a closed scenario in a dedicated resource, where resources from dependent component version can be described by relative resource references and multiple scenarios can be separated by multiple flavors of this resource, the label-based approach is restricted to a local component version and a single scenario. Instead of an artifact type for the description, labels with a defined [name structure](./03-elements-sub.md#labels) are required.

## Artefact-Linking Label

This section defines a label convention for expressing cross-artefact relationships.
For example, it can be used to indicate that an SBoM resource describes a specific
OCI image resource within the same component version.

### Label Name

```
ocm.software/artefactReference
```

The label follows the [vendor-specific label naming scheme](./07-extensions.md#label-types).
The label version is expressed via the separate `version` field on the label object
(e.g. `version: v1`); consumers MUST NOT treat a label with a different version as
conforming to this convention.

### Placement

The label is placed on the **derived artefact**. The resource that is related to a
subject artefact carries the label pointing back to that subject. The subject
artefact itself requires no modification.

```
Component Descriptor
├── Resource: my-image          ← subject artefact, unchanged
└── Resource: my-image-sbom     ← derived artefact, carries the label
```

When multiple derived artefacts reference the same subject (e.g. two SBoMs produced
by different tools for the same image), they MUST be told apart from each other by
their own `extraIdentity`. The `identitySelector` in each label still points to the
same subject; it is the derived artefact's own identity that makes the two resources
unique within the component version.

### Label Value

The label value is a YAML object with the following fields:

**`identitySelector`** (required) - identifies the subject artefact within the same
component version as a flat map of identity-relevant properties:

- `name` (required) *string* — resource name of the subject artefact.
- `version` (optional) *string* — resource version. If omitted, any version matches.
- Any additional key-value pair is treated as an extra identity property.
  Every such entry MUST be present and equal in the subject's `extraIdentity`.
  Required when multiple resources share the same name (e.g. arch-specific image variants).

### Examples

An SBoM describing a single-variant image:

```yaml
resources:
  - name: my-image
    version: 1.2.3
    type: ociImage

  - name: my-image-sbom
    version: 1.2.3
    type: sbom
    labels:
      - name: ocm.software/artefactReference
        version: v1
        value:
          identitySelector:
            name: my-image
```

Two SBoMs referencing the same subject, told apart by their own `extraIdentity`:

```yaml
resources:
  - name: my-image
    version: 1.2.3
    type: ociImage
    extraIdentity:
      foo: bar

  - name: my-image-sbom
    version: 1.2.3
    type: sbom
    extraIdentity:
      architecture: amd64
    labels:
      - name: ocm.software/artefactReference
        version: v1
        value:
          identitySelector:
            name: my-image
            version: 1.2.3
            foo: bar

  - name: my-image-sbom
    version: 1.2.3
    type: sbom
    extraIdentity:
      architecture: arm64
    labels:
      - name: ocm.software/artefactReference
        version: v1
        value:
          identitySelector:
            name: my-image
            version: 1.2.3
            foo: bar
```

### Lookup Algorithm

To find all artefacts related to a given subject resource:

1. Determine the identity of the subject resource: its `name`, `version`, and `extraIdentity`.
2. Iterate over all resources in the component descriptor.
3. For each resource, check whether it carries a label named `ocm.software/artefactReference` with `version: v1`.
4. If present, apply the following matching rules against `identitySelector`:
   - `name` MUST equal the subject's `name`.
   - If `version` is set, it MUST equal the subject's `version`.
   - Every additional key-value pair MUST be present and equal in the subject's `extraIdentity`.
5. Resources that pass all checks are companions of the subject.
