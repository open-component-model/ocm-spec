# 2.4.2 Formats

## Repository Specifications

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

The specification must contain at least the field

- **`type`** (required) *string*

  The type of the access method. It determines the possible and required
  additional fields of the access specification.


## Extensions

More format specifications according to dedicated variations for
model extension points
can be found in the [appendix](../../appendix/README.md).