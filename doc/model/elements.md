# Model Elements

The following section describe in more detail how a component (version) is specified. Please note that this section is intended to give an overview and explain the main elements and their structure. It is not a full specification. See the [schemas](https://github.com/open-component-model/ocm/tree/main/resources) for a full definition.

## Components and Component Versions

A component version describes several kinds of elements.

- Artifacts represent technical content. The appear in two different flavors:
  - Sources describe the sources a component version  has been composed/geerated from
  - Resources describe the delivery artifacts contained in the component version
- References describe the aggregation of other component versions

All those described elements share a common set of meta data.

## Artifacts (Resources and Sources)

The Open Component Model distinguishes two kinds of artifacts:
- *Sources* are optional artifacts that contain the sources, which
  were used to generate the deployment-relevant *Resources*
- *Resources* are artifacts that finally make up the deployment
  relevant set of artifacts

An *Artifact* is a blob containing some data in a technical format.
Every artifact described by the component version has

- an Identity in the context of the component version
- a type representing the kind of content and how it can be used
- a set of labels
- an Access Specification to technically access the content of the artifact
- an optional digest of the artifact

Those attributes are described by formal fields in the component descriptor:

- the identity fields are directly embedded

- **`type`** (required) *string*

  The type of an artifact  specifies the logical interpretation of an artifact and is independent of its concrete technical representation.

- **`labels`** (optional) *[]Label*

- **`access`** (required) *Access Specification*

  The access specification for the actual artifact (see below)

## Sources

A *Source* is an artifact which describes the sources that were used to generate one or more of the resources. Source elements do not have specific additional formal attributes.

## Resources

A *Resource* is a delivery artifact,
intended for deployment into a runtime environment, or describing additional
content, relevant for a deployment mechanism. For example, installation procedures
or meta-model descriptions controlling orchestration and/or deployment mechanisms.

The Open Component Model makes no assumptions about how content described
by the model is finally deployed or used. This is left to external tools. Tool
specific deployment information is formally represented by other artifacts with
an appropriate type.

In addition to the common artifact information, a resource may optionally describe a reference to the source by specifying its artifact identity.

A resource uses the following additional formal fields:

- **`digest`** (optional) *Digest Info*

  If the component descriptor is signed (directly or indirectly by one of its
  referencing component versions), a digest of a resource is stored along with
  the resource description. This is required because there might be different
  digest and resource normalization algorithms.

- **`relation`** (required) *string['local', 'external']*
  Indicates if the resource is part of this component version ('local') or accessed by a separate identity

- **`srcRef`** (optional) *struct*

  This field is used to describe the sources used to generate the resource.
  The selection is done by the following two fields:

    - **`identitySelector`** *map[string]string*

      Identity attributes determining an appropriate source
      element.

    - **`labels`** (optional) *[]Label*

      A list of arbitrary labels

## References

A component version may refer to other component versions by adding a *reference* to the component version.s

A reference element has the following fields:

- **`name`** (required) *string*

  The identity of the reference in this component version

- **`componentName`** (required) *string*

  The identity of the referenced component.

- **`version`** (required) *string*

  The version of the referenced component.

- **`extraIdentity`** (optional) *string*

  The extra identity of the referenced component.

- **`labels`** (optional) see below  *[]Label*

  The extra identity of the referenced component.

- **`digest`** (optional) see below *Digest Info*

  The extra identity of the referenced component.

## Identifiers

A *Component* is technically defined by a globally unique identifier.

A component identifier uses the following naming scheme:

<div align="center">

*&lt;DNS domain>* `/` *&lt;name component> {* `/` *&lt;name component> }*

</div>

Hereby the DNS domain plus optionally any number of leading name components MUST
be owned by the provider of a component. For example, `github.com`, as DNS domain
is shared by lots of organizations. Therefore, all component identities provided
based on this DNS name, must include the owner prefix of the providing
organization, e.g. `github.com/my-org`.

The component acts as a namespace to host multiple *Component Versions*.

A component version has a unique identity composed of the component identity and a version name following the [semantic versioning](https://semver.org) specification (e.g. `github.com/gardener/external-dns-management:0.15.1`).

The element identity is composed by the following formal fields of an element:

- **`name`** (required) *string*

  The name of the element. In most of the cases the name should be chosen
  to be unique in the context of the list of elements.
  It basically also expresses the meaning or purpose of the element in the
  context of the component version. But it might be the
  case that multiple elements should be used for the same purpose. For example,
  a component version is used to describe multiple versions of an artifact,
  which should be selected for different environment versions for deployment.
  Then, they could share the same name, to be able to easily find all those
  elements. In such a case the name is not sufficient to uniquely identify
  a dedicated element.

- **`version`** (optional) *string*

  This optional attribute version describes the version of the element.
  If given, and the name of the element is not unique in its context, the
  version is added to the identity attribute set.

- **`extraIdentity`** (optional) *map[string]string*

  If name and version are not sufficient to provide a unique selection
  scheme, any arbitrary identity dimension can be added by using this field.
  If given, all those attributes contribute to the identity of the element
  and must be given to uniquely identify an element. The identity scheme can
  be chosen differently per element, by all effective identities of elements
  of a dedicated class (resources, sources, references) in a component must be
  unique.

Using multiple attributes of an artifact for its identity makes it easier to formally
describe the identity and to select a dedicated artifact from the set of
described artifacts. It avoids the need to
marshal a dedicated identity scheme for an intended usage scenario into a
single attribute value. Instead, different attributes can be used to represent
the dedicated selection dimensions. Selecting all artifacts for a partial set
of constraints is then just a partial match of the set of identity attributes.

For example:

You want to describe different image versions to be used
for different Kubernetes versions and for multiple purposes. With the identity
attributes this can easily be modeled by using
- the `name` attribute for the purpose (e.g. DNS controller)
- the `version` attribute for the image version
- and an extra identity attribute for the intended Kubernetes Version.

Then you don't need to derive artificially unique artifact names, instead
the identity of the artifact can naturally be composed by using appropriate
attributes. Selecting all artifacts for a dedicated purpose is possible
by selecting all artifacts with the appropriate `name` attribute, without the
need of parsing an artificial structure imprinted on the name attribute.

<div align="center">
<img src="ocmidentity.png" alt="Identities" width="800"/>
</div>

Every identity carrying element described by the Open Component Model can
therefore be identified by the triple *(Component Identity, Version Name,
Local Element Identity)*.

*Example:*

The component with the identity `github.com/gardener/external-dns-management`
contains software versions of a tool maintaining DNS entries in DNS providers
based on Kubernetes resource manifests.

Hereby, the prefix `github.com/gardener` describes a *GitHub* organization owned
by the Gardener team developing the component `external-dns-management`.

## Access Specification

The technical access to the physical content of an
artifact described as
part of a Component Version is expressed by an
*Access Specification*.
It describes the type of the *access method* and the type-specific access path to the content. In a concrete execution environment the *Access Method Type* is mapped to a concrete access method implementation to execute the procedure to finally access the content of an artifact.

The content of a described artifact is accessible by applying its
global identity triple to the following procedure:

- lookup of a component version in a component descriptor by using its component identity and version name in the desired repository context.
- identify the artifact by its local identity]
- apply the described access method

<div align="center">
<img src="ocmresourceaccess.png" alt="Structure of OCM Specification" width="800"/>
</div>

## Labels

There are several elements in the component descriptor, which
can be annotated by labels:

- The component version itself
- resource specifications
- source specifications
- component version references

*Labels* can be used to add additional formal information to a component model element, which do not have static formal fields in the component descriptor. Its usage is left to users of the component model. The usage of labels is left to the creator of a component version, therefore the set of labels must be extensible.

To be able to evaluate labels for any component version, the same label name must have the same meaning, regardless by which component provider they are generated. To assure that this information has a globally unique interpretation or meaning, labels must comply with some naming scheme and use a common structure.

There are two flavors of labels:

- labels with a predefined meaning for the component model itself.

  Those labels are used by the standard OCM library and tool set to   control some behaviour like signing.

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

## Repository Contexts

A *Repository Context* describes the access to an OCM Repository. This access is described by a [formal and typed specification](../formats/formats.md#repository-specifications). A component descriptor MAY contain information about the transport history by keeping a list of repository contexts. It SHOULD at least describe the last repository context for an OCM repository it was transported into.


## Signatures

A component version may be signed by some authority. It is possible to have multiple signatures in the component descriptor.

When signing a component version, all included component versions are digested by digesting their resources and normalizing their component descriptors (see Digest Info).

Every signature entry has the following formal fields:

- **`name`** (required) *string*

  The name if the signature. It must be unique in the context of a component
  version.

- **`digest`** (required) *Digest Info*

  The digest of the component version used to generate the signature.
  Different signatures may use different digest algorithms.

  The digest of a component version does not include volatile fields, like
  the access specification, which can change along a transportation chain.

- **`signature`** (required) *Signature Info*

  The signature for the specified digest.


## Digest Info

A digest is specified by the following fields:

- **`hashAlgorithm`** (required) *string*

  The used digest algorithm.

- **`normalisationAlgorithm`** (required) *string*

  The used normalization algorithm for the signed element.

- **`value`** (required) *string*

  The digest itself.

## Signature Info

A signature is specified by the following fields:

- **`algorithm`** (required) *string*

  The used [signing algorithm](../../appendix/C/README.md#signing-algorithms).

- **`mediaType`** (required) *string*

  The media type of the technical representation of the signature value.

- **`value`** (required) *string*

  The signature itself.

- **`issuer`** *string*

  The description of the issuer.
