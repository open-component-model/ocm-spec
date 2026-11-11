# Label `ocm.software/artifact-references`

This label specifies how cross-artifact relationships are expressed.
For example, it can be used to indicate that an SBoM resource describes a specific
OCI image resource within the same component version.

## Label Name

```text
ocm.software/artifact-references
```

The label is a predefined label within the Open Component Model (see [Label Types](../../01-model/07-extensions.md#label-types)).
The label version is expressed via the separate `version` field on the label object
(e.g. `version: v1alpha1`); consumers MUST NOT treat a label with a different version as
conforming to this specification.

## Placement

The label is placed on the **derived artifact**. The resource that is related to a
subject artifact carries the label pointing back to that subject. The subject
artifact itself requires no modification.

```text
Component Descriptor
├── Resource: my-image          ← subject artifact, unchanged
└── Resource: my-image-sbom     ← derived artifact, carries the label
```

When multiple derived artifacts reference the same subject (e.g. two SBoMs produced
by different tools for the same image), they MUST be told apart from each other by
their own artifact identity. The `identity` in each label still points to the
same subject; it is the derived artifact's own identity that makes the two resources
unique within the component version.

## Label Value

The label value is a list of objects. Each object has the following field:

**`identity`** (required) - a flat map of identity-relevant properties that identifies the subject artifact within the same component version:

- `name` (required) *string* — resource name of the subject artifact.
- `version` (optional) *string* — resource version. If omitted, any version matches.
- Any additional key-value pair is treated as an extra identity property.
  Every such entry MUST be present and equal in the subject's `extraIdentity`.
  Required when multiple resources share the same name (e.g. arch-specific image variants).

## Examples

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
      - name: ocm.software/artifact-references
        version: v1alpha1
        value:
          - identity:
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
      - name: ocm.software/artifact-references
        version: v1alpha1
        value:
          - identity:
              name: my-image
              version: 1.2.3
              foo: bar

  - name: my-image-sbom
    version: 1.2.3
    type: sbom
    extraIdentity:
      architecture: arm64
    labels:
      - name: ocm.software/artifact-references
        version: v1alpha1
        value:
          - identity:
              name: my-image
              version: 1.2.3
              foo: bar
```

## Lookup Algorithm

To find all artifacts related to a given subject resource:

1. Determine the identity of the subject resource: its `name`, `version`, and `extraIdentity`.
2. Iterate over all resources in the component descriptor.
3. For each resource, check whether it carries a label named `ocm.software/artifact-references` with `version: v1alpha1`.
4. If present, apply the following matching rules against each `identity` entry in the label value:
   - `name` MUST equal the subject's `name`.
   - If `version` is set, it MUST equal the subject's `version`.
   - The set of additional key-value pairs MUST exactly match the subject's `extraIdentity`:
     every key in the `identity` entry MUST be present and equal in the subject's `extraIdentity`,
     and the subject's `extraIdentity` MUST NOT contain any keys not present in the `identity` entry.
5. Resources that pass all checks are derived artifacts of the subject.
