# Component Descriptor Normalization

The [component descriptor](../formats/compdesc/README.md) is used to describe
a [component version](model.md#component-versions). It contains several kinds
of information:
- volatile label settings, which might be changeable.
- artifact access information, which might be changed during transport steps.
- static information describing the features and artifacts of a component
  version.

For signing a digest of the component descriptor needs to be generated.
Therefore, a standardized normalized form is needed, which contains only the signature relevant
information. This is the source to calculate a digest, which is finally signed (and verified).

Like for signature algorithms, the model offers the possibility to work with
different normalization algorithms/formats.

To support legacy versions of the component model, there are two different
normalizations.
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
  - `jsonNormalisationV1` uses an [OCM specific representation](#generic-normalization-format) of the JSON object.
  - `jsonNormalisationV2` uses a standard scheme according to [RFC8785 (JCS)](https://www.rfc-editor.org/rfc/rfc8785).


## `jsonNormalisationV1` vs `jsonNormalisationV2`

The `JsonNormalisationV1` serialization format is based on the serialization
format of the component descriptor. It uses an appropriate JSON object containing the relevant fields as contained in the component descriptors's serialization. The format version fields are included. Therefore, the normalized form is depending on the chosen serialization format. Changing this format version would result in different digests. The resulting JSON object is serialized with the [OCM specific scheme](#generic-normalization-format)

`JsonNormalisationV2` strictly uses only the relevant component descriptor
information according to the field specification shown below. It is independent of the serialization format used to store the component decsriptor in some storage backend. Therefore, the calculated digest is finally independent of the serialization format chosen for storing the component descriptor in a storage backend.

Additionally, it uses the JCS scheme for uniquely serializing the resulting
JSON object.

## Relevant information in Component Descriptors

A component descriptor contains static information and
information, which may change over time (for example, the access methods
specifications might be changed during a transport step). A digest should be
stable even after a transport and therefore should only hash static
information. Therefore, a component descriptor is transformed to format
containing only immutable fields, which are finally relevant for the signing
process to assure the data integrity.

Relevant fields and their mapping to the normalized data structure for `JsonNormalisationV2`:
- Component Name: mapped to `component.name`
- Component Version: mapped to `component.version`
- Component Labels: mapped to `component.labels` (see [Labels](#labels)])
- Component Provider: mapped to `component.provider`
- Resources: mapped to `component.resources`, always empty list enforced, without the source references (see [Labels](#labels)] and [Access Methods](#access-methods)])
- Sources: mapped to `component.sources`, always empty list enforced, (see [Labels](#labels)] and [Access Methods](#access-methods)])
- References: mapped to `component.references`, always empty list enforced, (see [Labels](#labels)])

### Access Methods

Access method specifications are completely ignored.
A resource/source is ignored, if the access method type is `none`.

## Labels

Labels are removed before signing but can be marked with a special boolean
property `signing`. This property indicates that the label should be
signing-relevant and therefore part of the digest. As a consequence such
labels cannot be changed anymore during the lifecycle of a component version
any may only describe static information.
The structure of signing-relevant labels is preserved from the component
descriptor version `v2`.

Example:

```yaml
labels:
- name: label1
  value: foo
- name: label2
  value: bar
  signing: true
```

`label1` will be excluded from the digest, `label2` will be included.
The label value is taken as it is, preserving a potentially deeply nested structure.

## Exclude Resources from Normalization/Signing

If a resource should not be part of the normalization and later signing, the resource needs a special digest in the following format:

```yaml
digest:
  hashAlgorithm: NO-DIGEST
  normalisationAlgorithm: EXCLUDE-FROM-SIGNATURE
  value: NO-DIGEST
```

## Generic Normalization Format

The generic format is based on a data structure consisting of dictionaries, lists and
simple values (like strings and integers).

The signing relevant information described by a component descriptor is mapped
to such a data structure according to the format specifications described below.

This data structure is then mapped to a formal JSON representation, which
only contains clearly ordered elements. It is marshalled without white-spaces contained
in the representation. Therefor, the resulting byte stream is directly defined
by the inbound data structure and independent of the order of marshalling
dictionaries/objects.
Its digest can be used as basis to calculate a signature.

To map lists and dictionaries into such clearly ordered elements the rules described
below are used. The inbound data structures in the examples below are shown in
YAML notation.

### Simple Values

Simple values are kept as they are.

Example:
```yaml
  "bob"
```
will result in :

```json
  "bob"
```
### Dictionary

All dictionaries are converted to a list where each element is a single-entry
dictionary containing the key/value pair of the original entry. This list is
ordered by lexicographical order of the keys.

Example:
```yaml
  bob: 26
  alice: 25
```
will result in :

```json
  [{"alice":25},{"bob":26}]
```

The values are converted according to the same rules, recursively.

Example:
```yaml
  people:
    bob: 26
    alice: 25
```
will result in :

```json
  [{"people":[{"alice":25},{"bob":26}]}]
```

### Lists

Lists are converted to JSON arrays and preserve the order of the elements

Example:
```yaml
- bob
- alice
```

normalized to:
```json
["bob","alice"]
```

The values are converted according to the same rules, recursively.

Example:
```yaml
   - bob: 26
   - alice: 25
```

will result in :

```json
  [[{"bob":26}],[{"alice":25}]]
```

### Combined example

The following snippet is taken from a real component descriptor.

```yaml
resources:
- access:
    localReference: blob
    mediaType: text/plain
    referenceName: ref
    type: localBlob
  extraIdentity:
    additional: value
    other: othervalue
  name: elem1
  relation: local
  type: elemtype
  version: 1
```

normalized to

```json
[{"resources":[[{"access":[{"localReference":"blob"},{"mediaType":"text/plain"},{"referenceName":"ref"},{"type":"localBlob"}]},{"extraIdentity":[{"additional":"value"},{"other":"othervalue"}]},{"name":"elem1"},{"relation":"local"},{"type":"elemtype"},{"version":1}]]}]
```

formatted with white spaces for better readability it looks like:

```json
[
  {
    "resources": [
      [
        {
          "access": [
            {
              "localReference": "blob"
            },
            {
              "mediaType": "text/plain"
            },
            {
              "referenceName": "ref"
            },
            {
              "type": "localBlob"
            }
          ]
        },
        {
          "extraIdentity": [
            {
              "additional": "value"
            },
            {
              "other": "othervalue"
            }
          ]
        },
        {
          "name": "elem1"
        },
        {
          "relation": "local"
        },
        {
          "type": "elemtype"
        },
        {
          "version": 1
        }
      ]
    ]
  }
]
```

### Empty values:

Empty lists are normalized as empty lists

```yaml
myList: []
```

```json
[{"myList":[]}]
```

Null values are skipped during initialization

```yaml
myList: ~
```

```yaml
myList: null
```

```yaml
myList:
```
are all normalized to:

```json
[]
```