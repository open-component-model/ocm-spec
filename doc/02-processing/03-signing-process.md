# Signing Process and Normalization

The signing of a component version is based on three things:

* selected content of the component descriptor
* the content of the described artifacts
* the referenced component versions.

A signature of a component version is based on digests of the involved elements.
Therefore, there must be a defined way, how to calculate digests.
This has to happen in a recursive way to handle aggregations.

## Determing the Artifact Digests

The content of every artifact is provided in a dedicated blob format by the various access methods.
A digest can be calculated based on this blob. This is the default behaviour.  

Nevertheless, there might be technology specific ways to provide an immutable digest for a dedicated type of artifact,
independent of the blob format generation (typically an archive).
For example, an OCI artifact is always uniquely identified by its manifest digest.
This characteristic can be used for the calculation of OCM artifact digests.

There might be various ways to determine a digest for an artifact blob.
The algorithm to do this is called *artifact normalization type*.
Together with the digest and its digesting algorithm (e.g. SHA-256)
the normalization type is kept for an artifact.

Example for the digest of an OCI artifact:

```yaml
  digest:
    hashAlgorithm: SHA-256
    normalisationAlgorithm: ociArtifactDigest/v1
    value: 5e28862f7ad5b71f3f5c5dc7a4ccc8c3d3cb87f5e5774458d895d831d3765548
```

This normalization algorithm specifies the way the digest is determined. For example, for OCI artifacts,
the algorithm `ociArtifactDigest/v1` is used by default. This behaviour can be controlled by appropriate digest handlers.

If not explicitly requested, an appropiate digest handler is automatically determined based on the available digest handlers,
when the digest of an artifact is calculated for the first time.
This selection depends on the media type of the artifact blob and the artifact type.

Normalization algorithm types may be versioned and SHOULD match the following regexp

```text
[a-z][a-zA-Z0-9]*/v[0-9]+([a-z][a-z0-9]*)
```

For example: `ociArtifactDigest/v1` or `jsonNormalisationV2`

If the digest algorithm `NO-DIGEST` is specified for an artifact,
this artifact content is not included into the component version digest.
This is typically configured for source artifacts, which are not deliverable.

The artifact digest normalization algorithms are listed in the [extensions](../04-extensions/04-algorithms/README.md#artifact-normalization-types)
section of the specification.

## Normalization Types

To be able to sign a component version, the content of the described artifacts must be incorporated
and a digest for the artifact content needs to be calculated.

By default, this digest is calculated based on the blob provided by the access specification of an artifact. There might be technology specific ways to uniquely identify the content for specific artifact types.

Together with the digest and its algorithm, an artifact normalization algorithm is specified in the component descriptor.

It contains signature
relevant information and volatile information (e.g. the access specification). Therefore, there is a normalization for component descriptors.

Normalization algorithm types may be versioned and SHOULD match the following regexp

```text
[a-z][a-zA-Z0-9]*/v[0-9]+([a-z][a-z0-9]*)
```

For example: `ociArtifactDigest/v1` or `jsonNormalisationV2`

The normalization algorithms are listed in the [extensible parts](../04-extensions/01-extensions.md#normalization-algorithms) of the specification

## Serialization Format

A digest for a component version is stored along with a signature in a
component descriptor. A component descriptor can have multiple signatures and with this
multiple digests.

Example:

```text
digest:
    hashAlgorithm: SHA-256
    normalisationAlgorithm: jsonNormalisation/v2
    value: 01c211f5c9cfd7c40e5b84d66a2fb7d19cb0d65174b06c57b403c2ad9fdf8ed2
```

## Recursive Digest Calculation

A digest for a component version is calculated recursively including all referenced component versions. For each referenced component the component descriptor will get a `digest` section for each `reference` contained in `spec`:

```yaml
spec:
  ...
  references:
  - componentName: ocm.software/simpleapp
    digest:
      hashAlgorithm: SHA-256
      normalisationAlgorithm: jsonNormalisation/v2
      value: 01c211f5c9cfd7c40e5b84d66a2fb7d19cb0d65174b06c57b403c2ad9fdf8ed2
    name: myhelperapp
    version: 0.1.0
```
