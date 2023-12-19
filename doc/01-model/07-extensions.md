# Extending the Open Component Model

The OCM specification is designed to be extended in several ways. The definition of such elements is restricted to a minimum set of attributes and may include functional behavior. It typically consists of a `type` attribute.

Those extension points are used to cover technology-specific aspects to be known either by dedicated implementations of the model or by applications using the model.

There are two different kinds of extensions: functional and semantic.

- Functional extensions

  Functional extensions offer the possibility to enrich an implementation of the Open Component Model with technology-specific parts to support more technology environments, like storage backends for the model or artifacts described by the model.

  The functional extension points are:

  - [Component Descriptor Serialization](#component-descriptor-serialization)
  - [Storage Backends](#storage-backends)
  - [Access Methods](#access-methods)
  - [Digest Algorithms](#digest-algorithms)
  - [Signing Algorithms](#signing-algorithms)
  - [Artifact Normalization](#artifact-normalization)
  - [Component Descriptor Normalization](#component-descriptor-normalization)
  - [Label Merge Algorithms](#label-merge-algorithms)

- Semantic extensions
  
  Semantic extensions offer the possibility to describe the semantics and structure of an element
  by arbitrary types, not defined by the Open Component Model itself.

  The semantic extension points are:

  - [Artifact Types](#artifact-types)
  - [Label Types](#label-types)


## Component Descriptor Serialization

The elements used to describe a component version can be represented in a serialized format,
typically as yaml document. This document must contain a format specification version
specifying the concrete represenation of the model elements of a component version.
The defined formats are described [here](../04-extensions/00-component-descriptor/README.md).
  
    
    
## Storage Backends

The Open Component Model specification does not describe a dedicated remotely accessible 
repository API (like for example the [OCI distribution specification](https://github.com/opencontainers/distribution-spec/blob/main/spec.md)).

The model is intended to be stored in any kind of storage sub system,
which is able to store a potentially unlimited number of blobs with an adequate addressing scheme, 
upporting arbitrary names.

For example, an OCI repository with a deep repository structure,
is suitable to host OCM components (see [OCI mapping Scheme](../04-extensions/03-storage-backends/README.md)).

On the client side, a suitable implementation or language binding must be available
to work with component information stored in such a storage backend.

Every such binding must support at least the mandatory set of abstract operations
working with elements of the component model (see below).

The Open Component Model defines abstract operations that must be available
to work with a component repository view as interpretation layer on-top
of dedicated well-known storage subsystems (like an OCI registry or an S3 blob store).
These operations build the first extension point of OCM,
which allows to map the OCM functionality onto any blobstore-like storage system.

A concrete implementation of a storage backend extension consists of two parts:

- a language-independent mapping of the OCM elements to the elements available in the storage backend
and a formal specification how the abstract model operations are mapped to operations provided by the storage backend.
- a language-specific binding of the formerly described mapping 

By defining the language-independent part used for those operations the interoperability
between different implementations is assured.

### Data Formats

The metadata of a component version is defined by the [serialization format of a component descriptor](#component-descriptor-serialization).
It is stored as single blob in the storage backend together with the format version.
It must be possible to store any supported format version.

### Mandatory Operations

The following operations are mandatory:

- **`UploadComponentDescriptor(ComponentDescriptor-YAML) error`**

  Persist a serialized form of the descriptor of a component version with its
  component identity and version name in way so that it is retrievable again using
  this identity.

- **`GetComponentDescriptor(ComponentId, VersionName) (ComponentDescriptor-YAML, error)`**

  Retrieve a formally persisted description of a component version.

- **`UploadBlob(ComponentId, VersionName, BlobAccess, MediaType, ReferenceHint) (BlobIdentity, GlobalAccessSpec, error)`**

  Store a byte stream or blob under a namespace given by the component version
  identity and return a local blob identity (as string) that can be used to retrieve
  the blob, again (together with the component version identity).

  Additionally, a dedicated media type can be used to decide how to internally
  represent the artifact content.

  Optionally, the operation may decide to store the blob in dedicated ways according to its media type.
  For example, an OCI based implementation can represent blobs containing an OCI artifact as regular,
  globally addressable object.

  A type-specific optional *ReferenceHint* can be passed to guide the operation for generating an identity,
  if it decided to make the object externally visible.

  If this is the case, an external access specification has to be returned. At least a blob identity or
  an external access specification has to be returned for not successful executions.

- **`GetBlob(ComponentId, VersionName, BlobIdentity) (Blob, error)`**

  Retrieve a formerly stored blob, again, using the blob identity provided by the store operation. Technically this should be a stream or the blob content.

- **`ListComponentVersions(ComponentId) ([]VersionName, error)`**

  List all the known versions of a component specified by its component identity.

### Optional Operations

Optional operations might be:

- **`DeleteComponentVersion(ComponentId, VersionName) error`**

  To be able to clean up old information, an operation to delete the information
  stored for a component version should be available.

- **`DeleteBlob(ComponentId, VersionName, BlobIndentity) error`**

  It might be useful to provide an explicit delete operation for blobs stored
  along with the component version. But the repository implementation
  may keep track of used blobs on its own.

- **`ListComponents(ComponentId-Prefix) ([]ComponentId, error)`**

  List all components in the given identifier namespace. (The structure of a
  component id based on hierarchical namespace).

- **`ListComponentClosure(ComponentId-Prefix) ([]ComponentId, error)`**

  List all components in the given identifier namespace, recursively.
  It should not only return component identities, that are direct children,
  but traverse the complete subtree.

## Access Methods

The task of an access method is to provide access to the physical content of an artifact described by a component version.
The content is always provided as blob with a dedicated media type, either depending on the access method itself
or the [artifact type](#artifact-types). To fulfill its task an access method gets an access specification.

The list of centrally defined access methods types can be found [here](../04-extensions/02-access-types/README.md)

### Access Specification

The technical access to the physical content of an artifact described as part of a Component Version is expressed
by an *Access Specification*. It specifies which access method to use and additionaly the type-specific attributes,
which are required by the access method to access the content. In an implementation the *Access Method Type* is mapped
to code for finally accessing the content of an artifact.

### Access Method Names

Regardless of the creator of a component version, an access method must be uniquely identifyable. 
Therefore the names of access methods must be globally unique.

There are two flavors of method names:

- Centrally provided access methods

  Those methods should be implemented by OCM compliant libraries and tools. Using only such
  access methods guarantees universal access.

  These types use flat names following a camel case scheme with the first character in lower case (for example `ociArtifact`).

  Their format is described by the following regexp:

  ```regexp
  [a-z][a-zA-Z0-9]*
  ```

- Vendor specific types

  Any organization using the open component model may define additional access methods on their own.
  Their name MUST be globally unique. There may be multiple such types provided by different organizations with the same meaning.
  Organizations should share such types and reuse existing types instead of introducing new type names.

  Using component versions with vendor specific access methods always means a restriction on using tools
  implementing these access methods. FOr exchanging such component versions involved parties must agree on the used toolset.

  To support a unique namespace for those type names vendor specific types MUST follow a hierarchical naming scheme
  based on DNS domain names. Every type name has to be suffixed by a DNS domain owned by the providing organization.
  The local type must follow the above rules for centrally defined type names and suffixed by the namespace separated by a dot (`.`)

  So, the complete pattern looks as follows:

  ```regexp
  [a-z][a-zA-Z0-9]*\.<DNS domain name>
  ```

### Access specification format

Every access method MUST define a specification of the attributes required to locate the content.
This specification MAY be versioned. The type of the access specification MUST contain the access method name
and MAY have an optional specification type to uniquely describe the method and the attribute set.
Therefore, in addition to the access method type name the access specification type name MAY include
a version appended by a slash (`/`) to completely describe the description format.

The version MUST match the following regular expression:

```regexp
v[1-9][0-9]*
```

Examples:
- `ociArtifact/v1`
- `myprotocol.acme.org/v1alpha1`


If no version is specified, implicitly the version `v1` is assumed.

The access method type is part of the access specification. The access method type may define additional specification attributes required to specify the access path to the artifact blob.

For example, the access method `ociBlob` requires the OCI repository reference and the blob digest to be able to access the blob.

```yaml
...
  access:
    type: ociArtefact
    imageReference: ghcr.io/jensh007/ctf/github.com/open-component-model/ocmechoserver/echoserver:0.1.0
```

### Access Method Operations

There must be an implementation for all supported external access methods
according to their specifications. The local access method is mapped
to the local blob access provided by the repository.

They have to support read access, only. At least a media type
and stream access for the denoted blob is required.

- **`<method>.GetMediaType(RepositoryContext, ComponentVersion, AccessSpecification) (string, error)`**

  Provide the media type of the described artifact. It might explicitly be stored as part of the access specification,
  or implicitly provided by the access method.

- **`<method>.GetStream(RepositoryContext, ComponentVersion, AccessSpecification) (Byte Stream, error)`**

  Provide access to the blob content described by a dedicated access specification.

- **`<method>.GetInexpensiveContentVersionIdentity(RepositoryContext, ComponentVersion, AccessSpecification) (string, error)`**

  This **optional** operation is used to provide a unique identifier for the version
  of the described content, without the requirement of an (expensive) access to the byte stream.
  For example, the OCI artifact access method can extract the content digest from the reference part
  of its access specification. If this operation is not supported or proveds an empty string,
  an identity will be calculated based on accessing the byte stream.


## Digest Algorithms

Digest algorithms describe the way digests are calculated from a byte stream. The defined algorithms can be found [here](../04-extensions/04-algorithms/digest-algorithms.md).


## Signing Algorithms

A signing algorithm is used to provide a signature byte sequence for a given digest.
The algorithm is denoted by a name following the syntax

```regexp
[A-Z][A-Z0-9-_]*
```

The result of a signing is a structured data set with the following fields:

- **`mediatype`** (required) *string*

  The mediatype used to represent the signature value. Possible values:

  - `application/x-pem-file` signature is stored as multi-block PEM document.
    The signature block uses the type `SIGNATURE`. This block might describe the 
    signature algorithm with the block header `Signature Algorithm`. 
    Additionally there might be blocks describing the certificate chain of the used public key.
  - `application/vnd.ocm.signature.rsa` signature is stored as HEX encoded byte stream.

- **`value`** (required) *string* 
  
  The signature byte stream according to the specified media type.

- **`algorithm`** (required) *string*
  
  The technical algorithm used to verify the signature. For example, this name might be different
  from the signing algorithm name. The signing algorithm might describe the usage of a signing server,
  which provides an RSA signature. In this case the verification algorithm would be `RSASSA-PKCS1-V1_5`.

- **`issuer`** (optional) *string*
  
  The distinguished name of the subject of the public key certificate.


## Artifact Normalization

If a component is signed this signature should cover the content provided by the component resources.
Therefore a digest is calculated for the resource content blobs.
To be able to provide a format-independent digest, the resource blob can be normalized
before a digest is calculated. For example, an OCI artifact is represented 
as blob following the [OCI Image Layout Specification](https://github.com/opencontainers/image-spec/blob/main/image-layout.md).

Unfortunately the byte stream of the resulting artifact blob is not stable,
it depends on the used archiving tool, timestamps and the archiving order of the files.
So, reccreating an OCI artifact in an OCI repository and recreating it into an archive
does not necessaryily provide the same byte sequence. Therfore the natural blob digest
is not necessarily a source of providing stable digests for signing.
Hence OCM provides a mechanism to calculate digests for resources based on the logical
content of an artifact. This mechanism is called *Artifact Normalization*.

Hereby a stable digest is provided for an artifact, independent of the physical byte representation.
The normalization is selected based on the resource type and the artifact media type. The result of
the normalization is a *digest specification* with the following fields

- **`normalizationType`** (required) *string*

  The name of the algorithm used to provide a digest for an artifact blob.
  The default digets algorithm is `genericBlobDigest/v1`, which calculates
  the byte stream digest of the blob.

- **`hashAlgorithm`** (required) *string*

  The [type of the digest](#digest-algorithms) provided.

- **`value`** (required) *string*

  The HEX encoded digest value.

The already defined digesters can be found [here](../04-extensions/04-algorithms/artifact-normalization-types.md).

Example: 

```yaml
resources:
  - name: apiserver-proxy
    version: v0.14.0
    type: ociImage
    access:
      type: ociRegistry
      imageReference: >-
        mycompany.com/myrepo/apiserver-proxy:v0.14.0-mod1
    digest:
      hashAlgorithm: SHA-256
      normalisationAlgorithm: ociArtifactDigest/v1
      value: 9dc9c7c74abe301e0ee2cb168c004051179e7365d269719db434d3582a12dcb6
    relation: local
```

## Component Descriptor Normalization

The component descriptor contains several kinds of information:
- volatile label settings, which might be changeable.
- artifact access information, which might be changed during transport steps.
- static information describing the features and artifacts of a component version.

The digest of a component descriptor is calculated on a normalized form of its
elements. The normalized form contains only the signature
relevant information, everything else gets removed during the normalization process. 
The resulting string is the source for calculating the digest.
This digest is then finally signed (and verified).

A normalized component descriptor is a subset of its elements containing only the properties relevant for signing.

Like for signature algorithms, the model offers the possibility to work with
different normalization algorithms and formats.

The algorithms used for normalization are listed in the [extensions](../04-extensions/04-algorithms/component-descriptor-normalization-algorithms.md) section.

### Signing-relevant Information in Component Descriptors

Relevant fields are:

- Component Name
- Component Version
- Labels (for component, provider, resources, sources and references) (only signature-relevant labels, see [below](#labels))
- Component Provider
- Resources without access method specification see [below](#artifacts)
- Sources without access method specification see [below](#artifacts)
- References see [below](#references)

### Artifacts

Access method specifications for sources and resources are completely ignored.
A resource or source is ignored, if the access method type is `none`
or the hash algorithm of the digest specification is `NO-DIGEST` and the 
normalization algorithm is `EXCLUDE-FROM-SIGNATURE`.

### Labels

Labels by default are removed before signing, but can be marked with a special boolean
property `signing` set to `true`. This property indicates that the label is
signing-relevant and therefore becomes part of the digest. As a consequence such
labels cannot be changed during the lifecycle of a component version anyomre
and SHOULD only describe static information.

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

### References 

If a component version contains references to other component versions,
their digests are stored along with the reference as digest descriptor.
The digest descriptor is similar to the [artifact digest](#artifact-normalization).
Hereby the component descriptor normalization algorithm is registered instead of the
artifact normalization algorithm.

Example:

```yaml
...
componentReferences:
  - name: etcd-druid
    componentName: github.com/gardener/etcd-druid
    version: v0.21.0
    digest:
      hashAlgorithm: SHA-256
      normalisationAlgorithm: jsonNormalisation/v1
      value: 7f5255bc89cdfc1eb06ce20dba7fb6e1d93a065533354ca9fccfe958c90eac73
...
```

### Applying Normalization Algorithms

The normalization algorithm provides a stable deserialization format based on the 
elements of a component descriptor, excluding the fields not relevant for signing.
Afterwards the resulting byte stream is hashed using a [digest algorithm](#digest-algorithms).
The resulting digest is the digest of the component version.

## Label Merge Algorithms

Value merge algorithms are used during a transfer of a component version into a target repository 
to merge label values, in case the transferred version is already present
and the new content does not hamper the digest of the old one.
 
This scenario is used to re-transfer updated content of non-signature relevant labels
(for example updated routing slips).
 
Hereby, potential changes in the target must be merged with the new inbound content.
This is done by executing value merge algorithms for changed label values.

If no specific algorithm is configured for a label, the algorithm used is `default`.

The merge algorithm is described by a specification descriptor optionally provided 
by the field `merge` as part of a label descriptor. It has the following fields:

- **`algorithm`** (required) *string*
  
  The name of the merge algorithm to be used.

- **`config`** (optional) *any*

  An arbitrary description of the config. The structure depends on the selected algorithm.

Example:

```yaml
labels:
  - name: mylabel
    value: ...
    merge: 
      algorithm: mapListMerge
      config:
        keyField: name
        entries:
          algorithm: ...
          config: ...
```

The configuration may recursively contain further merge specifications used
for nested parts of the label value, depending on the outer algorithm.

A model implementation MUST provide the possibility to declare merge algorithms
for dedicated label names to be able to omit merge specifications
as part of the component descriptor.

The currently specified algorithms for label merge can be found in the [extensions](../04-extensions/04-algorithms/label-merge-algorithms.md)section.

## Artifact Types 

Artifact types describe the meaning of an artifact independent of their technical representation in a blob format.
The artifact types defined by the core model (this specification) are described
in section [Artifact Types](02-elements-toplevel.md#artifact-types)

## Label Types

Dynamic attribution of model elements with additional information is possible using [*Labels*](./03-elements-sub.md#labels)].
To be interpretable by tools the meaning of a label must be uniquely derivable from its name,
regardless of the creator of a concrete label entry in a component version.
To assure that every consumer of a component version has the same understanding odf the label,
label names MUST be globally unique. 

To combine globally uniqueness and arbitrarely extensibility of label names,
they must comply with some namespaced naming scheme.

There are two flavors of labels:

- labels with a predefined meaning within the component model.

  Those labels are used by the standard OCM library and tool set to control some behaviour.
  Labels without a namespace are relevant for the component model itself.

  Such labels use flat names following a camel case scheme with the first character in lower case.

  Their format is described by the following regexp:

  ```regexp
  [a-z][a-zA-Z0-9]*
  ```

- vendor specific labels

  any organization using the open component model may define own labels.
  Nevertheless, these names must be globally unique.
  Basically there may be multiple such labels provided by different organizations
  with the same meaning. Such label names MUST use a namespace.

  To support a unique namespace vendor specific labels
  have to follow a hierarchical naming scheme based on DNS domain names.
  Every label name has to be preceded by a DNS domain owned by the providing
  organization (for example `landscaper.gardener.cloud/blueprint`).
  The local name MUST follow the above rules for centrally defined names
  and is appended, separated by a slash (`/`).

  So, the complete pattern looks as follows:

  ```regexp
  <DNS domain name>/[a-z][a-zA-Z0-9]*
  ```

### Format Versions

To be interpretable by tools, every label MUST define a specification of its attributes,
to describe its value space. This specification may be versioned.

The version must match the following regexp

```regexp
v[0-9]+([a-z][a-z0-9]*)?
```

### Predefined Labels

So far, no centrally predefined labels have been defined.
