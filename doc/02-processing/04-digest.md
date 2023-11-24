# Signing Process

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

```
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

```
[a-z][a-zA-Z0-9]*/v[0-9]+([a-z][a-z0-9]*)
```

For example: `ociArtifactDigest/v1` or `jsonNormalisationV2`

The normalization algorithms are listed in the [extensible parts](../04-extensions/01-extensions.md#normalization-algorithms) of the specification

## Serialization Format

A digest for a component version is stored along with a signature in a
component descriptor. A component descriptor can have multiple signatures and with this
multiple digests.

Example:

```
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
# Examples for Signing of Component Versions

## Simple Component Version

The component descriptor to be signed is:

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

The normalized form of the component descriptor in `jsonNormalisation/v2` is the string:

```
[{"component":[{"componentReferences":[]},{"name":"ocm.software/simpleapp"},{"provider":[{"name":"ocm.software"}]},{"resources":[[{"digest":[{"hashAlgorithm":"SHA-256"},{"normalisationAlgorithm":"ociArtifactDigest/v1"},{"value":"5e28862f7ad5b71f3f5c5dc7a4ccc8c3d3cb87f5e5774458d895d831d3765548"}]},{"name":"chart"},{"relation":"local"},{"type":"helmChart"},{"version":"0.1.0"}],[{"digest":[{"hashAlgorithm":"SHA-256"},{"normalisationAlgorithm":"ociArtifactDigest/v1"},{"value":"cb5c1bddd1b5665e1867a7fa1b5fa843a47ee433bbb75d4293888b71def53229"}]},{"name":"image"},{"relation":"external"},{"type":"ociImage"},{"version":"1.0"}]]},{"sources":[[{"name":"source"},{"type":"filesytem"},{"version":"0.1.0"}]]},{"version":"0.1.0"}]}]
```

The `SHA-256` digest of this string is: `01c211f5c9cfd7c40e5b84d66a2fb7d19cb0d65174b06c57b403c2ad9fdf8ed2`

Adding the signature and digests for all artifacts leads to this signed component descriptor:

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

## Component Version with Reference

Here is a component descriptor containing a reference to the component in the previous [example](#simple-component-version).

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

The normalized form of the component descriptor in `jsonNormalisation/v2` is the string:

```
[{"component":[{"componentReferences":[[{"componentName":"ocm.software/simpleapp"},{"digest":[{"hashAlgorithm":"SHA-256"},{"normalisationAlgorithm":"jsonNormalisation/v2"},{"value":"01c211f5c9cfd7c40e5b84d66a2fb7d19cb0d65174b06c57b403c2ad9fdf8ed2"}]},{"name":"myhelperapp"},{"version":"0.1.0"}]]},{"name":"ocm.software/complexapp"},{"provider":[{"name":"ocm.software"}]},{"resources":[[{"digest":[{"hashAlgorithm":"SHA-256"},{"normalisationAlgorithm":"ociArtifactDigest/v1"},{"value":"927d98197ec1141a368550822d18fa1c60bdae27b78b0c004f705f548c07814f"}]},{"name":"image"},{"relation":"external"},{"type":"ociImage"},{"version":"1.0"}]]},{"sources":[]},{"version":"0.1.0"}]}]
```

The `SHA-256` digest of this string is: `01801dfb56ba7b4033b8177e53e689644f1447c8270004b2c05c5fe45aa1063f`

Adding the signature and digests for all artifacts leads to this signed component descriptor:

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

Note that the `references` section in `spec` now contains a `digest` for the referenced component `ocm.software/simpleapp`. The value of the digest therefore is the same as in the previous example.

# Component Descriptor Normalization

The component descriptor contains several kinds of information:
- volatile label settings, which might be changeable.
- artifact access information, which might be changed during transport steps.
- static information describing the features and artifacts of a component version.

The digest of a component descriptor is calculated on a normalized form of the
elements of the component descriptor. The normalized form contains only the signature
relevant information, everything else gets removed during the normalization process. 
The resulting string is the source for calculating the digest. This digest is then finally signed (and verified).

A normalized component descriptor is a subset of its elements containing only the properties relevant for signing:

- based on JSON
- map serializes as alphanumerically ordered list of fields (to define unique order)
- field is map with two keys 'name', 'value'

Like for signature algorithms, the model offers the possibility to work with
different normalization algorithms and formats.

The algorithms used for normalization are listed in the [extensible parts](../04-extensions/01-extensions.md#normalization-algorithms) of the specification.


## Signing-relevant Information in Component Descriptors

A component descriptor contains static information and
information, which may change over time, e.g. access method
specifications might be changed during transport steps. A digest should be
stable even after a transport and therefore should only hash static
information. Therefore, a component descriptor is transformed into a format
that only contains immutable fields, finally relevant for the signing
process and assuring data integrity.

Relevant fields and their mapping to the normalized data structure for `JsonNormalisationV2` are:

- Component Name: mapped to `component.name`
- Component Version: mapped to `component.version`
- Component Labels: mapped to `component.labels` (see [Labels](#labels)])
- Component Provider: mapped to `component.provider`
- Resources: mapped to `component.resources`, always empty list enforced, without the source references (see [Labels](#labels)] and [Access Methods](#access-methods)])
- Sources: mapped to `component.sources`, always empty list enforced, (see [Labels](#labels)] and [Access Methods](#access-methods)])
- References: mapped to `component.references`, always empty list enforced, (see [Labels](#labels)])

### Access Methods

Access method specifications are completely ignored.
A resource or source is ignored, if the access method type is `none`.

## Labels

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

and are all normalized to:

```json
[]
```

# Artifact Normalization

To be able to sign a component version a digest for the artifact **content** must be determined.

By default, this digest is calculated based on the blob provided by the access specification.
There might be technology specific ways to uniquely identify the content for dedicated artifact types.
Therefore an artifact normalization algorithm is kept in the component descriptor.

## Blob Representation Format for Resource Types

The central task of a component version is to provide information about versioned sets of resources.
For the component model such content of resources are just simple typed blobs.
The evaluation of an access specification always results in a simple blob, representing the content of the described resource.
This way blobs can be stored in any supported external blob store.

An access method MUST always be able to return a blob representation for the accessed artifact.
If there are native storage technologies for dedicated artifact types they must also deliver such a blob.

Whenever a new resource type is supported, corresponding blob formats MUST be defined for this type.
Type-agnostic access method types, like `localBlob` or `ociBlob` never need to know anything about their internal format.
But specific access methods, e.g. the `ociArtifact` method, MAY provide dedicated blob formats.

These blob formats may depend on the combination of artifact type and access method type.
Therefore, a blob always has a *media type* specifying the technical format.
For every artifact type the possible media types with their technical format specifications MUST be defined.

When using the component repository to transport content from one repository to
another the access information may change. But all variants MUST describe the same
content.

If multiple media types are possible for blobs, the digest of the artifact content
MUST be immutable to avoid invalidating signatures. In such a case a
dedicated artifact normalization algorithm MUST be provided for such media types.

Available artifact normalization types can be found [above](#normalization-types).

## Interaction of Local Blobs, Access Methods, Uploaders and Media Types

The Open Component Model is desiged to support transports of artifacts.
To assure the integrity of digests and signatures some rules must be obeyed by the involved model extensions.

### Access Methods

A remote access method MUST return the artifact content as blob.

By default, this blob is used to calculate the content digest for an artifact.
Therefore, the byte-stream of this blob must be deterministic.
Multiple calls for the same content must return the identical blob.
If this cannot be guaranteed, a blob digest handler for the media type of this blob format MUST be defined.

For example, the `ociArtifact` access method provides content as artifact set blob,
with a format based on the OCI artifact structure, which is defined by a dedicated media type.
For this media type a digest handler is defined, which replaces the default blob digest by the manifest digest of the artifact.
This way the digest is independent from the creation of the archive blob containing the artifact.

Once the artifact content has been converted to a blob and stored as local blob,
this blob is by default kept for further transport steps.
This way, the digest calculation always provides the same result.

### Blob Uploaders

Blob Uploaders can be used as part of the transport process, to automatically
provide transported artifacts in technology specific local storage systems, e.g. OCI registries.
The Open Component Model allows to change access locations
of artifact content during transport. Therefore an automatic upload
with modification of the access method is principally allowed.
In such scenarios, it's essential to adhere to specific rules to ensure the integrity of digests and signatures.

If a blob uploader is used to upload the artifact to a remote repository after a transfer again,
the access method can potentially be changed. But this MUST guarantee the same digest calculation.
The new access method must again provide a blob with a media type and digest handler combination, providing the same digest.

For example, storing an OCI artifact delivered as local blob in an OCI repository again, the manifest digest will be the same.
This is guaranteed because it is the identity of the artifact according to the OCI specification.
As a result, a new transformation to a blob representation in combination with the digest handler
will always provide the same artifact digest. The access method can be switched again,
from `localBlob` to `ociArtifact` regardless of the artifact type.

If this can not be guaranteed, once a blob representation is chosen, it must be kept as it is.
In such a case a blob uploader must preserve the local access method,
even if it uploads the content to an external storage system.

This can be described in the component version by adding the new remote access specification
as part of the existing local one, using the `globalAccess` attribute.

The artifact digest is always calculated based on the local access,
but tools may use the information provided by the global access to use technology native ways to access the artifact.
