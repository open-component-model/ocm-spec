# Normalization

The signing of a component version is based on content of the component descriptor describing a component version, the content of the described artifacts and the referenced component versions.

A signature of a component version is based on digests of the involved elements.
Therefore, there must be a defined way, how to calculate digests for
artifact content and component descriptors, which can be used in a recursive way
to handle aggregations.

## Artifact Digest

The content of every artifact is provided in a dedicated blob format by the
various access methods. A digest can be calculated based on this blob. This is the default behaviour.
Nevertheless, there might be technology specific ways to provide an immutable
digest for a dedicated type of artifact, independent of the blob format generation
(typically an archive). For example, an OCI artifact is always uniquely identified by its manifest
digest. This can be used for the calculation of OCM artifact digests.

Together with the digest and its digesting algorithm (e.g. SHA-256) a
normalization type is kept for an artifact. This normalization algorithm specifies the way
the digest is determined. For example, for OCI artifacts, the algorithm
`ociArtifactDigest/v1` is used by default. This behaviour can be controlled by
appropriate digest handlers. Supported algorithms can be found
here.

If the digest algorithm `NO-DIGEST` is specified for an artifact,
this artifact content is not included into the component version digest.
This is typically configured for source artifacts, which are not deliverable.

## Component Descriptor Digest

The digest of a component descriptor is calculated on a normalized form of the
elements of a component descriptor.


### Normalization of the component-descriptor

The normalization of the component-descriptor describes the process of generating a normalized form a component-descriptor. A normalized component-descriptor is a subset of the component-descriptor elements containing signing-relevant properties, only.

- based on JSON
- map serializes as alphanumerically ordered list of fields (to define unique order)
- field is map with two keys 'name', 'value'

The process and the format is described here.

## Artifact Digests

As described, resources have a digest field to store the content hash. Different resource types will use a different normalisationAlgorithm:

 - `ociArtifactDigest/v1`: uses the hash of the manifest of an oci artifact
 - `genericBlobDigest/v1`: uses the hash of the blob


## Digest Algorithms

Digest algorithms describe the way digests are calculated from a byte stream.

The following digest algorithms are defined:

- `SHA-256`
- `SHA-512`

## Normalization Types

The following algorithms are centrally defined and available in the OCM toolset:

- `NO-DIGEST`: Blob content is ignored for the signing process.

  This is a possibility for referencing volatile artifact content.
-
- `genericBlobDigest/v1` (*default*): Blob byte stream digest

  This is the default normalization algorithm. It just uses the blob content
  provided by the access method of an OCM artifact to calculate the digest.
  It is always used, if no special digester is available for an artifact type.

- `ociArtifactDigest/v1`: OCI manifest digest

  This algorithm is used for artifact blobs with the media type of an OCI artifact.
  It just uses the manifest digest of the OCI artifact.

## Serialization Format

A digest for a component version is stored along with a signature in a
component-descriptor. A component-descriptor can have multiple signatures and with this
multiple digests. A digest consists of the elements `hashAlgorithm`, `normalisationAlgorithm`,
and `value`.

Example:

```
digest:
    hashAlgorithm: SHA-256
    normalisationAlgorithm: jsonNormalisation/v2
    value: 01c211f5c9cfd7c40e5b84d66a2fb7d19cb0d65174b06c57b403c2ad9fdf8ed2
```

## Recursive Digest Calculation

A digest for a component version can be calculated recursively including all referenced component
versions. For each referenced component the component-descriptor will get a `digest` section for each
`reference` contained in `spec`.

## Example

### Simple Component-Version

The component-descriptor to be signed is:

```
apiVersion: ocm.software/v3alpha1
kind: ComponentVersion
metadata:
  name: ocm.software/simpleapp
  provider:
    name: ocm.software
  version: 0.1.0
repositoryContexts: []
spec:
  resources:
  - access:
      localReference: sha256:dea5de3e6f20fc58bfa8c2a25043f628c730960d46100b83540a30ed0a4e7910
      mediaType: application/vnd.oci.image.manifest.v1+tar+gzip
      referenceName: ocm.software/simpleapp/echoserver:0.1.0
      type: localBlob
    name: chart
    relation: local
    type: helmChart
    version: 0.1.0
  - access:
      imageReference: gcr.io/google_containers/echoserver:1.10
      type: ociArtifact
    name: image
    relation: external
    type: ociImage
    version: "1.0"
  sources:
  - access:
      commit: e39625d6e919d33267da4778a1842670ce2bbf77
      repoUrl: github.com/open-component-model/ocm
      type: github
    name: source
    type: filesytem
    version: 0.1.0
```

The normalized form in `jsonNormalisation/v2` is then:

```
[{"component":[{"componentReferences":[]},{"name":"ocm.software/simpleapp"},{"provider":[{"name":"ocm.software"}]},{"resources":[[{"digest":[{"hashAlgorithm":"SHA-256"},{"normalisationAlgorithm":"ociArtifactDigest/v1"},{"value":"5e28862f7ad5b71f3f5c5dc7a4ccc8c3d3cb87f5e5774458d895d831d3765548"}]},{"name":"chart"},{"relation":"local"},{"type":"helmChart"},{"version":"0.1.0"}],[{"digest":[{"hashAlgorithm":"SHA-256"},{"normalisationAlgorithm":"ociArtifactDigest/v1"},{"value":"cb5c1bddd1b5665e1867a7fa1b5fa843a47ee433bbb75d4293888b71def53229"}]},{"name":"image"},{"relation":"external"},{"type":"ociImage"},{"version":"1.0"}]]},{"sources":[[{"name":"source"},{"type":"filesytem"},{"version":"0.1.0"}]]},{"version":"0.1.0"}]}]
```

The sha-256 digest of this string is: `01c211f5c9cfd7c40e5b84d66a2fb7d19cb0d65174b06c57b403c2ad9fdf8ed2`

The signed component-descriptor is then:

```
apiVersion: ocm.software/v3alpha1
kind: ComponentVersion
metadata:
  name: ocm.software/simpleapp
  provider:
    name: ocm.software
  version: 0.1.0
repositoryContexts: []
signatures:
- digest:
    hashAlgorithm: SHA-256
    normalisationAlgorithm: jsonNormalisation/v2
    value: 01c211f5c9cfd7c40e5b84d66a2fb7d19cb0d65174b06c57b403c2ad9fdf8ed2
  name: mysig
  signature:
    algorithm: RSASSA-PKCS1-V1_5
    mediaType: application/vnd.ocm.signature.rsa
    value: ae7e7a215d970c036773221642693bded5cf6a039597113d5ec522d5ebd491a40e3f6d850689a749aaa2de3c0cc2a9e5f564c8353f514385fae7c9554e00aead4890483a0ae5cef5c3629eb63ba4ee061659b06737b4985b4c04d286d19a09735482a769e82dd4a0b396cb0dda0822817b72b7daa1dfd2a1c071dd4a7e7bea1e25ee4156594efc5a567ac092ae8518995843bef1e79c7bfd95651cf66725f3740ef8b0202485900a0445df327543963322baf61dd91d4b30356b996bd99e513e2b5a7643a8ddfc706773603dfb3f8f38d7a9fbd10c48fe813c8149b1e0be20f7fcf54bdd5efe4da37c60730fbf33f3ea26b793cf6ac531b8c6f66bea3e3d2ffc
spec:
  resources:
  - access:
      localReference: sha256:dea5de3e6f20fc58bfa8c2a25043f628c730960d46100b83540a30ed0a4e7910
      mediaType: application/vnd.oci.image.manifest.v1+tar+gzip
      referenceName: ocm.software/simpleapp/echoserver:0.1.0
      type: localBlob
    digest:
      hashAlgorithm: SHA-256
      normalisationAlgorithm: ociArtifactDigest/v1
      value: 5e28862f7ad5b71f3f5c5dc7a4ccc8c3d3cb87f5e5774458d895d831d3765548
    name: chart
    relation: local
    type: helmChart
    version: 0.1.0
  - access:
      imageReference: gcr.io/google_containers/echoserver:1.10
      type: ociArtifact
    digest:
      hashAlgorithm: SHA-256
      normalisationAlgorithm: ociArtifactDigest/v1
      value: cb5c1bddd1b5665e1867a7fa1b5fa843a47ee433bbb75d4293888b71def53229
    name: image
    relation: external
    type: ociImage
    version: "1.0"
  sources:
  - access:
      commit: e39625d6e919d33267da4778a1842670ce2bbf77
      repoUrl: github.com/open-component-model/ocm
      type: github
    name: source
    type: filesytem
    version: 0.1.0
```

### Component-Version With Reference

Here is a component-descriptor containing a reference to the component from the previous section.

```
apiVersion: ocm.software/v3alpha1
kind: ComponentVersion
metadata:
  name: ocm.software/complexapp
  provider:
    name: ocm.software
  version: 0.1.0
repositoryContexts: []
spec:
  references:
  - componentName: ocm.software/simpleapp
    name: myhelperapp
    version: 0.1.0
  resources:
  - access:
      imageReference: gcr.io/google_containers/pause:3.2
      type: ociArtifact
    name: image
    relation: external
    type: ociImage
    version: "1.0"
```


Normalized form:

```
[{"component":[{"componentReferences":[[{"componentName":"ocm.software/simpleapp"},{"digest":[{"hashAlgorithm":"SHA-256"},{"normalisationAlgorithm":"jsonNormalisation/v2"},{"value":"01c211f5c9cfd7c40e5b84d66a2fb7d19cb0d65174b06c57b403c2ad9fdf8ed2"}]},{"name":"myhelperapp"},{"version":"0.1.0"}]]},{"name":"ocm.software/complexapp"},{"provider":[{"name":"ocm.software"}]},{"resources":[[{"digest":[{"hashAlgorithm":"SHA-256"},{"normalisationAlgorithm":"ociArtifactDigest/v1"},{"value":"927d98197ec1141a368550822d18fa1c60bdae27b78b0c004f705f548c07814f"}]},{"name":"image"},{"relation":"external"},{"type":"ociImage"},{"version":"1.0"}]]},{"sources":[]},{"version":"0.1.0"}]}]
```

The sha-256 digest of this string is: `01801dfb56ba7b4033b8177e53e689644f1447c8270004b2c05c5fe45aa1063f`

The signed component-descriptor then is:

```
apiVersion: ocm.software/v3alpha1
kind: ComponentVersion
metadata:
  name: ocm.software/complexapp
  provider:
    name: ocm.software
  version: 0.1.0
repositoryContexts: []
signatures:
- digest:
    hashAlgorithm: SHA-256
    normalisationAlgorithm: jsonNormalisation/v2
    value: 01801dfb56ba7b4033b8177e53e689644f1447c8270004b2c05c5fe45aa1063f
  name: mysig
  signature:
    algorithm: RSASSA-PKCS1-V1_5
    mediaType: application/vnd.ocm.signature.rsa
    value: 727b067cd67003338b83149220a36fdb7e16f29d4d5790474c95ee3547adcbe64d699efce3d19fa2e85424904265c0364e95f15cbf816e093b633943a632ba9f3b862e1f5adb62620cf7eb2d85b60796f329afb1df26019ca84b42c58ebc6e691094e34eca223195f96cee3a8a1552e4ac7d1821e32072213f6cc762355c5974be56f239a270a9c67056ec3455f10339eb76eb8ca1905f0201190130fac0683bc2d09fa9bc3a9cd30af414b6f29e97397621d2f6b715353a7f793813139ed9707824b648aa84f2b38cc27fd7f6e89633ba83eb1fd34ab68a3b9c098eddd659f94a06d0225a4ed607b4c7682ca8d824ee005e618a25d3dde9d6aaf626aa7e1556
spec:
  references:
  - componentName: ocm.software/simpleapp
    digest:
      hashAlgorithm: SHA-256
      normalisationAlgorithm: jsonNormalisation/v2
      value: 01c211f5c9cfd7c40e5b84d66a2fb7d19cb0d65174b06c57b403c2ad9fdf8ed2
    name: myhelperapp
    version: 0.1.0
  resources:
  - access:
      imageReference: gcr.io/google_containers/pause:3.2
      type: ociArtifact
    digest:
      hashAlgorithm: SHA-256
      normalisationAlgorithm: ociArtifactDigest/v1
      value: 927d98197ec1141a368550822d18fa1c60bdae27b78b0c004f705f548c07814f
    name: image
    relation: external
    type: ociImage
    version: "1.0"
```

Note that the `references` section in `spec` now contains a `digest` for the referenced component.
The value of the digest is the same as in the previous section.
