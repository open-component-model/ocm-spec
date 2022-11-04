# C. Digest Calculation

## Artifact Digest
TODO
## Component descriptor Digest

## Normalisation of the component-descriptor

The normalisation of the component-descriptor describes the process of generating a normalised component-descriptor. A normalised component-descriptor is a subset of the component-descriptor containing signing-relevant properties only.igest before the normalisation, the process must be aborted if the digest mismatches the calculated digest for the entry. Such preexisting digest entries can NOT be trusted and they have to be calculated in the process.

- based on JSON
- map serializes as alphanumerically ordered list of fields (to define unique order)
- field is map with two keys 'name', 'value'
-
### Exclude Resource from Normalisation/Signing

If a resource should not be part of the normalisation and later signing, the resource needs a special digest in the following format:

```
digest:
  hashAlgorithm: NO-DIGEST
  normalisationAlgorithm: EXCLUDE-FROM-SIGNATURE
  value: NO-DIGEST
```

### Properties for normalisation

The following properties are part of the normalised component-descriptor:

```
meta
    schemaVersion

component
    name
    version
    provider

    componentReferences
        name
        componentName
        version
        extraIdentity
        digest:
            hashAlgorithm
            normalisationAlgorithm
            value
    resources
        name
        version
        extraIdentity
        type
        relation
        digest:
            hashAlgorithm
            normalisationAlgorithm
            value
```

Exceptions:

1. If resource.Access is empty or resource.access.type is `None`, no digest field is required. Then, only name, version, extraIdentity, type and relation is used for the normalisation.

### Properties **NOT** part of normalisation:

```
component
    repositoryContexts
    labels
    sources
    componentReference:
        labels
    resource:
        labels
        access
signatures
```

### Representation

In order to hash a normalised component-descriptor, it has to be transformed into a hash-able representation.

Attributes *MUST* be transformed into list of single attributes (key-value pairs) and ordered alphabetically. This list *MUST* be JSON encoded with disabled HTML Escaping and disabled pretty printing. It *MUST NOT* end with a newline character. A hash algorithm of choice can then be applied on the string

Example (pretty printed for readability): *TODO*: update

```
[
  {
    "component": [
      {
        "componentReferences": [
          [
            {
              "componentName": "compRefNameComponentName"
            },
            {
              "digest": [
                {
                  "hashAlgorithm": "sha256"
                },
                {
                  "normalisationAlgorithm": "jsonNormalisation/V1"
                },
                {
                  "value": "00000000000000"
                }
              ]
            },
            {
              "extraIdentity": [
                {
                  "refKey": "refName"
                }
              ]
            },
            {
              "name": "compRefName"
            },
            {
              "version": "v0.0.2compRef"
            }
          ]
        ]
      },
      {
        "name": "CD-Name"
      },
      {
        "resources": [
          [
            {
              "digest": [
                {
                  "hashAlgorithm": "sha256"
                },
                {
                  "normalisationAlgorithm": "manifestDigest/V1"
                },
                {
                  "value": "00000000000000"
                }
              ]
            },
            {
              "extraIdentity": [
                {
                  "key": "value"
                }
              ]
            },
            {
              "name": "Resource1"
            },
            {
              "version": "v0.0.3resource"
            }
          ]
        ]
      },
      {
        "version": "v0.0.1"
      }
    ]
  },
  {
    "meta": [
      {
        "schemaVersion": "v2"
      }
    ]
  }
]

```

### Digester

As described, resources have a digest field to store the content hash. Different resource types will use a different normalisationAlgorithm:

 - `ociArtefactDigest/v1`: uses the hash of the manifest of an oci artifact
 - `genericBlobDigest/v1`: uses the hash of the blob
