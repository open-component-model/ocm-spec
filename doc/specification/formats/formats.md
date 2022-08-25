# 2.4.2 Formats

This section defines common standardized specification formats
to be used for variations of the [extension points](../extensionpoints/README.md)
of the [Open Component Model](../../../README.md). There might be any number
of incarnations of such extension points.

## Repository Specifications

Any [repository](../layer1/README.md#repositories) that can be used to store
content according to the [Open Component Model](../../../README.md) MUST be
describable by a formal repository specification.

Such a specification is usable by a language binding supporting
this kind of specification to gain access to this repository.
In a concrete environment, all repositories are usable, for which an
implementation of the [abstract model operations](../layer2/README.md#repository-operations)
exist.

Therefore, a repository specification has a type, the [*Repository Type*](types.md#repository-types).
used to identify the required [mapping](../layer3/README.md) and the
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
of the content of [artefacts](../layer1/README.md#artefacts) described by a
[component version](../layer1/README.md#component-versions).
Every access specification has a formal type and type specific attributes.
The type uniquely specifies the technical procedure how to use the
attributes and the [repository context](../layer1/README.md#repository-contexts) of
the component descriptor containing the access specification
to retrieve the content of the artefact.

There are basically two ways an artefact blob can be stored:
- `external` access methods allow referring to artefacts in any other
  technical repository as long as the access type is supported by the
  used tool set.
- `internal` access methods ([`localBlob`](../../appendix/B/localBlob.md)).
  are used to store an artefact together with the component descriptor in an
  OCM repository. These methods must be supported by all OCM repository
  implementations.

The specification MUST contain at least the field

- **`type`** (required) *string*

  The type of the access method. It determines the possible and required
  additional fields of the access specification.


## Label Specifications

There are several elements in the component descriptor, which
can be annotated by labels:

- The component version itself
- resource specifications
- source specifications
- component version references

In addition to the element type (for resources and sources), labels
are intended to express additional semantics for an element.
To do so the meaning of labels must be clearly defied. Therefore,
a label and its bound semantic must be uniquely identified by its name.

The usage of labels is left to the creator of a component version, therefore
the set of labels must be extensible and the label name must follow
a dedicated [naming scheme](types.md#label-names)

A label entry in the [component descriptor](../layer1/README.md#component-descriptor)
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

Centrally defined labels with their specification versions
can be found in [appendix F](../../appendix/F/README.md).

## Extensions

Detailed format specifications according to dedicated variations for
the [model extension points](../extensionpoints/README.md)
can be found in the [appendix](../../appendix/README.md).