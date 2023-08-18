# 2.4.2 Formats

This section defines common standardized specification formats
to be used for variations of the [extension points](../extensionpoints/README.md)
of the [Open Component Model](../../../README.md). There might be any number
of incarnations of such extension points.

## Repository Specifications

Any [repository](../elements/README.md#repositories) that can be used to store
content according to the [Open Component Model](../../../README.md) MUST be
describable by a formal repository specification.

Such a specification is usable by a language binding supporting
this kind of specification to gain access to this repository.
In a concrete environment, all repositories are usable, for which an
implementation of the [abstract model operations](../operations/README.md#repository-operations)
exist.

Therefore, a repository specification has a type, the [*Repository Type*](types.md#repository-types).
used to identify the required [mapping](../mapping/README.md) and the
used specification scheme for an instance of this type holding
the information required to identify a concrete repository instance.

The specification MUST contain at least the field

- **`type`** (required) *string*

  The type of the repository. It determines the possible and required
  additional fields of the access specification (for example a URL of the
  repository instance).

Defined repository types and the definition of their specification attributes
can be found in [appendix A](../../appendix/A/README.md)


## Access Specifications

Access specifications are used to describe the technical access path
of the content of [artifacts](../elements/README.md#artifacts) described by a
[component version](../elements/README.md#component-versions).
Every access specification has a formal type and type specific attributes.
The type uniquely specifies the technical procedure how to use the
attributes and the [repository context](../elements/README.md#repository-contexts) of
the component descriptor containing the access specification
to retrieve the content of the artifact.

There are basically two ways an artifact blob can be stored:
- `external` access methods allow referring to artifacts in any other
  technical repository as long as the access type is supported by the
  used tool set.
- `internal` access methods ([`localBlob`](../../appendix/B/localBlob.md)).
  are used to store an artifact together with the component descriptor in an
  OCM repository. These methods must be supported by all OCM repository
  implementations.

The specification MUST contain at least the field

- **`type`** (required) *string*

  The type of the access method. It determines the possible and required
  additional fields of the access specification.


## Label Specifications

There are several elements in the component descriptor, which
can be annotated by labels:

- The [component version](../elements/README.md#component-versions) itself
- The [provider](../elements/README.md#provider-information) of the component version
- [resource](../elements/README.md#resources) specifications
- [source](../elements/README.md#sources) specifications
- component version [references](../elements/README.md#component-version-reference)

In addition to the element type (for resources and sources), labels
are intended to express additional semantics for an element.
To do so the meaning of labels must be clearly defied. Therefore,
a label and its bound semantic must be uniquely identified by its name.

The usage of labels is left to the creator of a component version, therefore
the set of labels must be extensible and the label name must follow
a dedicated [naming scheme](types.md#label-names)

A label entry in the [component descriptor](../elements/README.md#component-descriptor)
consists of a dedicated set of
meta attributes with a predefined meaning. While arbitrary values are allowed for the
label `value`, additional (vendor/user specific) attributes are not
allowed at the label entry level.

- `name` (required) *string*

  The label name according to the specification above.

- `value` (required) *any*

  The label value may be an arbitrary JSON compatible YAML value.

- `version` (optional) *string*

  The specification version for the label content. If no version is
  specified, implicitly the version `v1` is assumed.

- `signing` (optional) *bool*:  (default: `false`)

  If this attribute is set to `true`, the label with its value will be incorporated
  into the signatures of the component version.

  By default, labels are not part of the signature.

- `merge` (optional) *merge spec*

  non-signature relevant labels (the default) can be modified without breaking a potential signature. They can be changed in any repository the component version has been transferred to. This is supported to attach evolving information to a component version. But it also implies, that a component version must be updatable (re-transferable) in a certain target repository. This may lead to conflicting changes which might need to be resolved in a non-trivial way. 

  The merge behaviour can be specified together with the label definition using the `merge` attribute. It has the following fields:

  - `algorithm` (optional) *string*

    The name of the algorithm used to merge the label during a transport step. (see [appendix H](../../appendix/H/README.md) for available algorithms)
  - `config` (optional) *any*

    A configuration specific for the chosen algorithm.
  
Centrally defined labels with their specification versions
can be found in [appendix F](../../appendix/F/README.md).

## Extensions

Detailed format specifications according to dedicated variations for
the [model extension points](../extensionpoints/README.md)
can be found in the [appendix](../../appendix/README.md).