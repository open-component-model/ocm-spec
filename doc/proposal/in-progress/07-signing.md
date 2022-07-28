# Signing

Signing the component-descriptor allows to ensure that a part of the descriptor and referenced resources are identical to the authors component-descriptor. I.a., this does not include the sources field.
In order to add a signature to a component-descriptor, a digest is required at every resource and component reference as described in the next sections. With the digest information, a normalised component-descriptor can be calculated as a subset of relevant properties. The normalised component-descriptor has to be represented in a reproducable form to be hashed and signed.

## Digests

Digests are used for componentReferences and resources to indicate a hash for their content.

Fields:
digest:
  - hashAlgorithm: Hash algorithm used, e.g. 'sha256'
  - normalisationAlgorithm: normalisation Algorithm, defines which subset of the data is used as normalised representation
  - value: the digest value for the normalised data as defined by normalisationAlgorithm with the hash algorithm defined by hashAlgorithm

## Signatures

The component descriptor may have a list of signatures on root level. A signature can be identified by its name. It follows this schema:
```
signatures:
  - name: name of the signature. Used to identify the signature when verifying.
    digest: as defined, contains the digest of the normalised component-descriptor (the signing-relevant subset of the component-descriptor)
    signature:
        algorithm: signature algorithm used
        value: the signature in the format as defined in mediaType
        mediaType: defines the format of the signature.value field
```

## Normalisation CD

The normalisation of the component-descriptor describes the process of generating a normalised component-descriptor. A normalised component-descriptor is a subset of the component-descriptor of signing-relevant properties. 

### Digests in Normalisation
In the process of normalisation, all component-references and resources must be filled with a digest (excpet resources with access null or access.type = 'None').
If a digest-containing entry (= component reference or resource) already contain a digest before the normalisation, the process must be aborted if the digest mismatches the calcuated digest for the entry. Such preexisting digest entries can NOT be trusted and they have to be calculated in the process.

### Exclude Resource from Normalisation/Signing
If a resource should not be part of the normalisation and later signing, the resource needs a special digest in the following format:
digest:
  hashAlgorithm: NO-DIGEST
  normalisationAlgorithm: EXCLUDE-FROM-SIGNATURE
  value: NO-DIGEST

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

1. If resource.Access is emtpy or resource.access.type is None, no digest field is required. Then, only name, version, extraIdentity, type and relation is used for the normalisation.

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

In order to hash a normalised component-descriptor, it has to be transformed into a hashable representation.

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

 - `ociArtifactDigest/v1`: uses the hash of the manifest of an oci artifact
 - `genericBlobDigest/v1`: uses the hash of the blob

## Sign Algorithm

Signing a component-descriptor requires a hash of the normalised component-descriptor, that can be signed.
The digest fields *MUST* be calculated during normalisation and already existing digest fields *CAN NOT* be trusted. Resources have to be accessed and digested. ComponentReferences has to be followed recursively, calculating the digest for the referenced componentDescriptor. If digests fields for resources or component-references exist, they have to be compared against the calculated digest and rejected if different.

### RSA

After the digest for the normalised component-descriptor is calculated, it can be signed using RSASSA-PKCS1-V1_5 as signature.algorithm. The corresponding signature is stored hex encoded in signature.value with a mediaType of application/vnd.ocm.signature.rsa.

## Verification Algorithm

Verifying a component-descriptor consits of three steps. Failing any step **MUST** fail the validation.

1. Verify the digest of all resources and component references. Recursively follow component references and create an in-memory representation of the referenced component-descriptor by accessing and digesting all resources and references. Do not trust any digest data in child component-descriptors. The digest of the normalised in-memory representation of a component-reference **MUST** match the digest in the root component-descriptor (that contains a signature we verify in the next step).
```
func digestForComponentDescriptor(cd) -> digest:
  for reference in cd.component.componentReferences:
    referencedCd = loadCdForReference(reference)
    reference.Digest = digestForComponentDescriptor(referencedCd)

  for resource in cd.component.Resource:
    resource.Digest = loadAndDigestResource(resource)

  normalisedCd = normaliseComponentDescriptor(cd)
  digest = createDigestForNormalisedCd
  return digest
```
2. verify the signature, identified by signatureName.
3. check if calcluated digest of the normalised compponent-descriptor matches the digest in signatures.digest with hashAlgorithm, NormalisationAlgorithm and Value

### Verify with RSA

Signature verification with RSASSA-PKCS1-V1_5 requires a Public Key. This is used in step 2 of the verification algorithm.

### Verify with X509
Signature verification with X509 certificates require a validation of the "signing" certificate and the signature itself. First, the validity of the "signing" certificate is checked with a root CA and a chain of intermediate certificates. Afterwards, the CD signature is verified with the public key in the "signing" certificate.