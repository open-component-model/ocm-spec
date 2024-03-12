# Component Descriptor Normalization

The component descriptor contains several kinds of information:

* volatile label settings, which might be changeable.
* artifact access information, which might be changed during transport steps.
* static information describing the features and artifacts of a component version.

The digest of a component descriptor is calculated on a normalized form of the
elements of the component descriptor. The normalized form contains only the signature
relevant information, everything else gets removed during the normalization process.
The resulting string is the source for calculating the digest. This digest is then finally signed (and verified).

A normalized component descriptor is a subset of its elements containing only the properties relevant for signing:

* based on JSON
* map serializes as alphanumerically ordered list of fields (to define unique order)
* field is map with two keys 'name', 'value'

Like for signature algorithms, the model offers the possibility to work with
different normalization algorithms and formats.

The algorithms used for normalization are listed in the [extensible parts](../04-extensions/04-algorithms/component-descriptor-normalization-algorithms.md) of the specification.

## Signing-relevant Information in Component Descriptors

A component descriptor contains static information and
information, which may change over time, e.g. access method
specifications might be changed during transport steps. A digest should be
stable even after a transport and therefore should only hash static
information. Therefore, a component descriptor is transformed into a format
that only contains immutable fields, finally relevant for the signing
process and assuring data integrity.

Relevant fields and their mapping to the normalized data structure for `JsonNormalisationV2` are:

* Component Name: mapped to `component.name`
* Component Version: mapped to `component.version`
* Component Labels: mapped to `component.labels` (see [Labels](#labels)])
* Component Provider: mapped to `component.provider`
* Resources: mapped to `component.resources`, always empty list enforced, without the source references (see [Labels](#labels)] and [Access Methods](#access-methods)])
* Sources: mapped to `component.sources`, always empty list enforced, (see [Labels](#labels)] and [Access Methods](#access-methods)])
* References: mapped to `component.references`, always empty list enforced, (see [Labels](#labels)])

### Access Methods

Access method specifications are completely ignored.
A resource or source is ignored, if the access method type is `none`.

### Labels

Labels by default are removed before signing, but can be marked with a special boolean
property `signing`. This property indicates that the label is
signing-relevant and therefore becomes part of the digest. As a consequence such
labels cannot be changed during the lifecycle of a component version anymore
and should only describe static information.
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

`label1` will be excluded from the digest, whereas `label2` will be included.
The value of any label is taken as is, preserving a potentially deeply nested structure.

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
simple values, like strings and integers.

The signing relevant information described by a component descriptor is mapped
to such a data structure according to the format specifications described below.

This data structure is mapped to a formal JSON representation, which
only contains clearly ordered elements. It is marshalled without whitespaces contained
in the representation. The resulting byte stream is directly defined
by the inbound data structure and independent of the order of marshalling
dictionaries/objects.
Its digest can be used as basis for calculating a signature.

To map lists and dictionaries into such clearly ordered elements the rules
below are used. The inbound data structures in the examples are shown in
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

All dictionaries are converted into lists where each element is a single-entry
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

Lists are converted into JSON arrays and preserve the order of the elements.

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

This will be normalized to

```json
[{"resources":[[{"access":[{"localReference":"blob"},{"mediaType":"text/plain"},{"referenceName":"ref"},{"type":"localBlob"}]},{"extraIdentity":[{"additional":"value"},{"other":"othervalue"}]},{"name":"elem1"},{"relation":"local"},{"type":"elemtype"},{"version":1}]]}]
```

Formatted with whitespaces for better readability it looks like:

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

### Empty values

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

and are all normalized to:

```json
[]
```
