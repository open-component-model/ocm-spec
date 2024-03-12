# Normalization Algorithms

Currently the there are two different normalizations defined:

- `jsonNormalisationV1`: This is a legacy format, which depends on the format of the
  component descriptor
- `jsonNormalisationV2`: This is the new format. which is independent of the
  chosen representation format of the component descriptor.

The normalization process is divided into two steps:

- *extraction of the signature relevant information from the component descriptor*

  The result is basically a JSON object, which decsribed the relevant information.

- *normalization of the resulting JSON object*

  Here, the object is serialized to a unique and reproducable byte sequence, which is finally used to determine the digest.

  There are two such normalization methods:
  - `jsonNormalisationV1`
  - `jsonNormalisationV2`

## `jsonNormalisationV1`

The `JsonNormalisationV1` serialization format is based on the serialization format of the component descriptor.
It uses an appropriate JSON object containing the relevant fields as contained in the component descriptors's serialization.
The format version fields are included. Therefore, the normalized form is depending on the chosen serialization format.
Changing this format version would result in different digests.
The resulting JSON object is serialized with the [OCM specific scheme](../../02-processing/05-component-descriptor-normalization.md#generic-normalization-format)

## `jsonNormalisationV2`

`JsonNormalisationV2` strictly uses only the relevant component descriptor
information according to the field specification. It is independent of the serialization format used to store the component decsriptor in some storage backend. Therefore, the calculated digest is finally independent of the serialization format chosen for storing the component descriptor in a storage backend. It uses a standard scheme according to [RFC8785 (JCS)](https://www.rfc-editor.org/rfc/rfc8785)

Relevant fields and their mapping to the normalized data structure for `JsonNormalisationV2` are:

- Component Name: mapped to `component.name`
- Component Version: mapped to `component.version`
- Component Labels: mapped to `component.labels`
- Component Provider: mapped to `component.provider`
- Resources: mapped to `component.resources`, if no resource is present, an empty list is enforced
- Sources: mapped to `component.sources`, if no source is present, an empty list is enforced
- References: mapped to `component.references`, if no reference is present, an empty list is enforced
