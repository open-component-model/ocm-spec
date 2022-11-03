# D. Signature Types

## Sign Algorithm

Signing a component-descriptor requires a hash of the normalised component-descriptor, that can be signed.
The digest fields *MUST* be calculated during normalisation and already existing digest fields *CAN NOT* be trusted. Resources have to be accessed and digested. ComponentReferences has to be followed recursively, calculating the digest for the referenced componentDescriptor. If digests fields for resources or component-references exist, they have to be compared against the calculated digest and rejected if different.

### RSA

After the digest for the normalised component-descriptor is calculated, it can be signed using RSASSA-PKCS1-V1_5 as signature.algorithm. The corresponding signature is stored hex encoded in signature.value with a mediaType of application/vnd.ocm.signature.rsa.

## Verification Algorithm

Verifying a component-descriptor consist of three steps. Failing any step **MUST** fail the validation.

1. Verify the digest of all resources and component references. Recursively follow component references and create an in-memory representation of the referenced component-descriptor by accessing and digesting all resources and references. Do not trust any digest data in child component-descriptors. The digest of the normalised in-memory representation of a component-reference **MUST** match the digest in the root component-descriptor (that contains a signature we verify in the next step).

```go
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
3. check if calculated digest of the normalised component-descriptor matches the digest in signatures.digest with hashAlgorithm, NormalisationAlgorithm and Value

### Verify with RSA

Signature verification with RSASSA-PKCS1-V1_5 requires a Public Key. This is used in step 2 of the verification algorithm.

### Verify with X509

Signature verification with X509 certificates require a validation of the "signing" certificate and the signature itself. First, the validity of the "signing" certificate is checked with a root CA and a chain of intermediate certificates. Afterwards, the CD signature is verified with the public key in the "signing" certificate.