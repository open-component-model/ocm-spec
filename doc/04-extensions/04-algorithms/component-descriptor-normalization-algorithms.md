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

## `jsonNormalisationV3`

> **Status:** Deprecated — transparently mapped to `jsonNormalisationV4alpha1`. Existing signatures using `jsonNormalisationV3` remain verifiable.
`jsonNormalisationV3` builds on the same signing-relevant field selection as `jsonNormalisationV2` but introduces two major changes:

1. **Standard JSON serialization via [RFC 8785 (JCS)](https://www.rfc-editor.org/rfc/rfc8785):**
   Instead of the OCM-specific [generic normalization format](../../02-processing/05-component-descriptor-normalization.md#generic-normalization-format) (dictionaries serialized as sorted single-entry lists), this algorithm uses the JSON Canonicalization Scheme defined in RFC 8785. JCS produces deterministic JSON by specifying exact rules for key ordering, number representation, and string escaping, yielding a unique byte sequence for any given JSON value.
2. **Refined field handling rules:**
   The algorithm operates on the **v2 serialization** of the component descriptor as its baseline and applies the following transformation rules.

### Extraction of Signing-Relevant Information

The following top-level sections are **completely excluded**:

| Excluded Section    | Reason                                            |
|---------------------|---------------------------------------------------|
| `meta`              | Schema version metadata, not content-relevant     |
| `signatures`        | The signature itself cannot be part of the digest  |
| `nestedDigests`     | Digests stored for referenced component versions in the parent descriptor |

Within the `component` section, the following rules apply:

#### Component-Level Fields

| Field                | Treatment |
|----------------------|-----------|
| `component.name`     | Included  |
| `component.version`  | Included  |
| `component.provider` | Included — always serialized as a JSON object `{"name": "<value>"}`, even if the original descriptor stores the provider as a plain string |
| `component.labels`   | Included, subject to [Label Rules](#label-rules-v3) |
| `component.repositoryContexts` | **Excluded** — transport-specific |
| `component.resources` | Included as a JSON array (empty `[]` if absent), subject to [Resource Rules](#resource-rules-v3) |
| `component.sources`  | Included as a JSON array (empty `[]` if absent), subject to [Source Rules](#source-rules-v3) |
| `component.references` | Included as a JSON array (empty `[]` if absent), subject to [Reference Rules](#reference-rules-v3) |

All list fields (`resources`, `sources`, `references`, `repositoryContexts`) default to an empty array `[]` when absent or `null`.

#### Resource Rules {#resource-rules-v3}

For each resource entry:

| Field      | Treatment |
|------------|-----------|
| `access`   | **Excluded** — transport-specific |
| `srcRefs`  | **Excluded** |
| `labels`   | Subject to [Label Rules](#label-rules-v3) |
| `digest`   | Included, **except** for resources whose access type is `none` (or legacy `None`), where the `digest` field is removed |
| All other fields | Included (e.g. `name`, `version`, `type`, `relation`, `extraIdentity`) |

#### Source Rules {#source-rules-v3}

For each source entry:

| Field    | Treatment |
|----------|-----------|
| `access` | **Excluded** — transport-specific |
| `labels` | Subject to [Label Rules](#label-rules-v3) |
| All other fields | Included |

#### Reference Rules {#reference-rules-v3}

For each reference entry:

| Field    | Treatment |
|----------|-----------|
| `labels` | Subject to [Label Rules](#label-rules-v3) |
| All other fields | Included |

#### Label Rules {#label-rules-v3}

Labels are treated specially across all label-bearing elements (component, resources, sources, references):

1. **Only signing-relevant labels are included.** A label is signing-relevant if and only if its `signing` field is set to `true` (boolean or the string `"true"`).Labels without `signing: true` are excluded.
2. **For included labels, only these fields are preserved:**
  - `name`
  - `version`
  - `value`
  - `signing`
3. **Other label metadata** (e.g. `mergeAlgorithm`) is excluded.
4. **If the resulting label array is empty after filtering, the entire `labels` field is omitted** (not serialized as `[]`).

### Serialization

After extracting the signing-relevant fields according to the rules above, 
the resulting JSON structure is serialized using [RFC 8785 (JCS)](https://www.rfc-editor.org/rfc/rfc8785), which defines:
- Lexicographic ordering of object keys
- Specific number formatting (no trailing zeros, no positive sign for exponents)
- Specific string escaping rules
- No whitespace between tokens
  The resulting byte sequence is the normalized form used for digest calculation.

### Example

Given this component descriptor (v2 serialization):

```yaml
meta:
  schemaVersion: v2
component:
  name: ocm.software/example
  version: 1.0.0
  provider: acme.org
  repositoryContexts:
    - baseUrl: ghcr.io
      type: OCIRegistry
  resources:
    - name: my-binary
      type: executable
      version: 1.0.0
      relation: local
      access:
        type: localBlob
        localReference: sha256:abc123...
        mediaType: application/octet-stream
      digest:
        hashAlgorithm: SHA-256
        normalisationAlgorithm: genericBlobDigest/v1
        value: abc123...
      labels:
        - name: downloadName
          value: my-binary
        - name: config-hash
          value: def456...
          signing: true
  sources: []
  references: []
signatures: []
```

The normalized form (formatted for readability) is:

```json
{
  "component": {
    "name": "ocm.software/example",
    "provider": {
      "name": "acme.org"
    },
    "references": [],
    "resources": [
      {
        "digest": {
          "hashAlgorithm": "SHA-256",
          "normalisationAlgorithm": "genericBlobDigest/v1",
          "value": "abc123..."
        },
        "labels": [
          {
            "name": "config-hash",
            "signing": true,
            "value": "def456..."
          }
        ],
        "name": "my-binary",
        "relation": "local",
        "type": "executable",
        "version": "1.0.0"
      }
    ],
    "sources": [],
    "version": "1.0.0"
  }
}
```

Note: In the actual serialized byte stream, there are no whitespaces or newlines — the formatted version above is for illustration only. The keys within each object are lexicographically ordered per RFC 8785.

Excluded from this output:

- `meta` (schema version)
- `signatures`
- `component.repositoryContexts` (transport-specific)
- `resources[].access` (transport-specific)
- `resources[].labels[0]` (`downloadName` — no `signing: true`)
- `provider` is serialized as `{"name":"acme.org"}` (not as the plain string `"acme.org"`)

## `jsonNormalisationV4alpha1`

> **Status:** Current default algorithm.
`jsonNormalisationV4alpha1` is a clean-room reimplementation of `jsonNormalisationV3`. It uses the same field selection rules, the same RFC 8785 (JCS) serialization, and produces **byte-identical output** for the same input.
The algorithm exists to provide a well-tested, independently implemented normalization that is not tied to the legacy OCM v1 codebase. Conformance between v3 and v4alpha1 is verified by test suites that compare the output of both algorithms on real-world component descriptors.

### Differences from `jsonNormalisationV3`

There are **no behavioral differences**. The field extraction rules, label handling, provider normalization, none-access resource handling,
empty-list defaults, and JCS serialization are identical. The `v4alpha1` name reflects that:

1. It is part of the next-generation OCM bindings (hence the version bump).
2. The `alpha1` suffix indicates that the algorithm name may be consolidated in a future specification version (e.g. to a final `v3` or `v4`).

### Backward Compatibility

When a signature or digest references `jsonNormalisationV3`, implementations SHOULD transparently use the `jsonNormalisationV4alpha1` algorithm for both signing and verification.
The two algorithms are interchangeable.

### Reference Implementation

The reference implementation can be found in the [Open Component Model repository](https://github.com/open-component-model/open-component-model):

- Algorithm registration and exclusion rules: `bindings/go/descriptor/normalisation/json/v4alpha1/normalisation.go`
- JCS engine (RFC 8785): `bindings/go/descriptor/normalisation/engine/jcs/`
- Legacy v3 → v4alpha1 mapping: `bindings/go/signing/digest.go`
- Conformance test data (v3 compatibility): `bindings/go/descriptor/normalisation/json/v4alpha1/testdata/conformance/legacy/jsonNormalisation/v3/`
