# 2.4.1 Types

Types are used to type variants for [extension points](../extensionpoints/README.md)
provided by the [Open Component Model](../../../README.md).
It is used to describe the intended dedicated logical or technical interpretation
of the described element.

- [Repository Types](#repository-types)

  [OCM repositories](../elements/README.md#repositories) can be described by a
  repository specification. The repository
  type determines the field structure of the specification and its technical
  access procedure.

- [Access Method Types](#access-method-types)

  [Access methods](../elements/README.md#artifact-access) describe dedicated
  technical ways how to access the blob
  content of an [artifact](../elements/README.md#artifacts) described by an
  [OCM component descriptor](../formats/compdesc/README.md). It is evaluated in
  the storage context used to read the component descriptor containing the
  access method description.

- [Artifact Types](#artifact-types)

  The OCM component descriptor describes a set of resources, their type and
  meaning with attached meta and access information.

- [Label Names](#label-names)

  The OCM component descriptor itself, resources, sources  and component version
  references can be enriched by labels capable to carry values with an
  arbitrary structure.

- [Normalization Types](#normalization-types)

  To calculate signatures, digests must be calculated for artifact content.
  
## Repository Types

  Any [repository](../elements/README.md#repositories) that can be used to store
  content according to the [Open Component Model](../../../README.md) must be
  describable by a formal repository specification.

Such a specification is usable by a language binding supporting
this kind of specification to gain access to this repository.
In a concrete environment, all repositories are usable, for which an
implementation of the [abstract model operations](../operations/README.md#repository-operations)
exists.

Therefore, a repository specification has a type, the *Repository Type*
used to identify the required [mapping](../mapping/README.md) and the
used [specification scheme](formats.md#repository-specifications) holding
the information required to identity a concrete repository instance.

There are two kinds of types:
- centrally defined type names managed by the OCM organization

  The format of a repository type is described by the following regexp:

  ```regex
  [A-Z][a-zA-Z0-9]*
  ```

  The defined types with their meaning and format can be
  found in [appendix A](../../appendix/A/README.md)

- vendor specific types

  any organization using the [open component model](../../../README.md) may
  define dedicated types on their own. Nevertheless, the meaning of those types
  must be defined.
  Basically, there may be multiple such types provided by different organizations
  with the same meaning. But we strongly encourage organizations to share
  such types instead of introducing new type names.

  To support a unique namespace for those type names vendor specific types
  have to follow a hierarchical naming scheme based on DNS domain names.
  Every type name has to be suffixed by a DNS domain owned by the providing
  organization (for example `myspecialrepo.acme.com`).
  The local type must follow the above rules for centrally defined type names
  and prepended, separated by a dot (`.`).

  So, the complete pattern looks as follows:

  ```
  [a-z][a-zA-Z0-9].<DNS domain name>
  ```

## Access Method Types

[Access methods](../elements/README.md#artifact-access) describe (and finally
implement) dedicated technical ways how to
access the blob content of an [artifact](../elements/README.md#artifacts)
described by an [OCM component descriptor](../elements/README.md#component-descriptor).

They are an integral part of the [Open Component Model](../../../README.md). They always
provide the link between a component version stored in some repository context,
and the technical access of the described resources applicable for this
context. Therefore, the access specification as well as the method of an artifact
may change when component versions are transported among repository contexts.

In a dedicated context all used access methods must be known by the used tool
set. Nevertheless, the set of access methods is not fixed. The actual
library/tool version provides a simple way to locally add new methods with
their implementations to support own local environments.

Because of this extensibility, the names of access methods must be globally
unique.

Like for [artifact types](#artifact-types), there are two flavors
of method names:

- centrally provided access methods

  Those methods are coming with the standard OCM library and tool set.
  It provides an implementation and component version using only such
  access methods can be used across local organizational extension.

  These types use flat names following a camel case scheme with
  the first character in lower case (for example `ociArtifact`).

  Their format is described by the following regexp:

  ```regex
  [a-z][a-zA-Z0-9]*
  ```

- vendor specific types

  any organization using the open component model may define dedicated access
  methods on their own. Nevertheless, their name must be globally unique.
  Basically there may be multiple such types provided by different organizations
  with the same meaning. But we strongly encourage organizations to share
  such types instead of introducing new type names.

  Extending the toolset by own access methods always means to locally
  provide a new tool version with the additionally registered access method
  implementations. Because the purpose of the Open Component Model is the
  exchange of software, the involved parties must agree on the used toolset.
  This might involve methods provided by several potentially non-central
  providers. Therefore, use used access method names must be globally unique
  with a globally unique meaning.

  To support a unique namespace for those type names vendor specific types
  have to follow a hierarchical naming scheme based on DNS domain names.
  Every type name has to be suffixed by a DNS domain owned by the providing
  organization.
  The local type must follow the above rules for centrally defined type names
  and suffixed by the namespace separated by a dot (`.`)

  So, the complete pattern looks as follows:

  ```
  [a-z][a-zA-Z0-9]*\.<DNS domain name>
  ```

Every access method type must define a specification of its attributes,
required to locate the content. This specification may be versioned.
Therefore, the type name used in an access specification in the component descriptor
may include a specification version appended by a slash (`/`).
Similar to the kubernetes api group versions, the version must match the
following regexp

```
v[0-9]+([a-z][a-z0-9]*)?
```

Examples:
- `ociArtifact/v1`
- `myprotocol.acme.org/v1alpha1`

If no version is specified, implicitly the version `v1` is assumed.

The access method type is part of the access specification of an artifact
in the component descriptor. The access method type may define
additional specification attributes required to finally identify the
concrete access path to the artifact blob.

For example, the access method `ociBlob` requires the OCI repository reference
and the blob digest to be able to access the blob.

Centrally defined access methods with their specification versions
can be found in [appendix B](../../appendix/B/README.md).

## Artifact Types

The [OCM component version](../elements/README.md#component-versions) describes
a set of [artifacts](../elements/README.md#artifacts), their type and
meaning with attached meta, and access information.

The formal type of an artifact uniquely specifies the
logical interpretation of an artifact, its kind, independent of its
concrete technical representation.

If there are different possible technical representation the
[access method](../elements/README.md#artifact-access)
returns the concrete format given by a media type used for the returned blob.

For example, a helm chart (type `helmChart`) can be represented as
OCI artifact or helm chart archive. Nevertheless, the technical meaning is
to be a helm chart, even if represented as OCI image. The type `ociImage`
describes an object that can be used as container image. So, although the
technical representation might in both cases be an OCI image manifest, its
semantics and use case is completely different. This is expressed
by the chosen type of the artifact, which focuses on the semantics.

The kind and logical interpretation of a technical artifact is basically
encoded into a dedicated simple string.
Because the interpretation of an artifact must be the same, independent
of the provisioning and consumption environment of a component version,
the artifact type must be globally unique.
The OCM defines a dedicated naming scheme to guarantee this uniqueness.

There are two kinds of types:
- centrally defined type names managed by the OCM organization

  These types use flat names following a camel case scheme with
  the first character in lower case (for example `ociArtifact`).

  Their format is described by the following regexp:

  ```regex
  [a-z][a-zA-Z0-9]*
  ```

- vendor specific types

  any organization using the open component model may define dedicated types on
  their own. Nevertheless, the meaning of those types must be defined.
  Basically there may be multiple such types provided by different organizations
  with the same meaning. But we strongly encourage organizations to share
  such types instead of introducing new type names.

  To support a unique namespace for those type names vendor specific types
  have to follow a hierarchical naming scheme based on DNS domain names.
  Every type name has to be preceded by a DNS domain owned by the providing
  organization (for example `landscaper.gardener.cloud/blueprint`).
  The local type must follow the above rules for centrally defined type names
  and is appended, separated by a slash (`/`).

  So, the complete pattern looks as follows:

  ```
  <DNS domain name>/[a-z][a-zA-Z0-9]*
  ```

The actually defined central types with their meaning and format can be
found in [appendix E](../../appendix/E/README.md).

## Label Names

There are several elements in the [component descriptor](../elements/README.md#component-descriptor), which
can be annotated by [labels](../elements/README.md#labels):

- The [component version](../elements/README.md#component-versions) itself
- The [provider](../elements/README.md#provider-information) of the component version
- [resource](../elements/README.md#resources) specifications
- [source](../elements/README.md#sources) specifications
- component version [references](../elements/README.md#component-version-reference)

In addition to the element type (for resources and sources), labels
are intended to express additional semantics for an element that cannot
be expressed by standard OCM features.
To do so the meaning of labels must be clearly defied. Therefore,
a label and its bound semantic must be uniquely identified by its name.

The usage of labels is left to the creator of a component version, therefore
the set of labels must be extensible.
Because of this extensibility, the names of labels must be globally
unique, also.

Like for [artifact types](#artifact-types) there are two flavors
of label names:

- labels with a predefined meaning for the component model itself.

  Those labels are used by the standard OCM library and tool set to
  control some behaviour like signing.

  Such labels use flat names following a camel case scheme with
  the first character in lower case.

  Their format is described by the following regexp:

  ```regex
  [a-z][a-zA-Z0-9]*
  ```

- vendor specific labels

  any organization using the open component model may define dedicated labels
  on their own. Nevertheless, their names must be globally unique.
  Basically there may be multiple such labels provided by different organizations
  with the same meaning. But we strongly encourage organizations to share
  such types instead of introducing new type names.

  To support a unique namespace for those label names vendor specific labels
  have to follow a hierarchical naming scheme based on DNS domain names.
  Every label name has to be preceded by a DNS domain owned by the providing
  organization (for example `landscaper.gardener.cloud/blueprint`).
  The local name must follow the above rules for centrally defined names
  and is appended, separated by a slash (`/`).

  So, the complete pattern looks as follows:

  ```
  <DNS domain name>/[a-z][a-zA-Z0-9]*
  ```

There is a [standard structure](formats.md#label-specifications) of a label
that includes label meta-data and the concrete label-specific attributes.
Every label must define a specification of its attributes,
to describe its value space. This specification may be versioned.
The version must match the following regexp

```
v[0-9]+([a-z][a-z0-9]*)?
```

Centrally defined labels with their specification versions
can be found in [appendix F](../../appendix/F/README.md).


## Normalization Types

To be able to sign a component version, the content of described artifacts
must be incorporated. Therefore, a digest for the artifact content must be
determined.

By default, this digest is calculated based on the blob provided by the
[access method](../elements/README.md#artifact-access)
of an artifact. But there might be technology specific ways to uniquely identify
the content for dedicated artifact types.

Therefore, together with the digest and its algorithm, an artifact normalization
algorithm is kept in the [component descriptor](../elements/README.md#component-descriptor).

The same problem appears for the component descriptor. It contains signature
relevant information and volatile information (e.g. the
[access specification](../elements/README.md#artifact-access)). Therefore, there
is a [normalization for component descriptors](componentdescriptor_normalization.md), also.

Normalization algorithm types may be versioned and SHOULD match the following regexp

```
[a-z][a-zA-Z0-9]*/v[0-9]+([a-z][a-z0-9]*)
```

For example: `ociArtifactDigest/v1` or `jsonNormalisationV2`

There are standardized normalization types for [artifacts](artifact_normalization.md)
and [component descriptors](componentdescriptor_normalization.md).