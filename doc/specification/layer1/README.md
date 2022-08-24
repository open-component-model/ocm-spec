# 2.1 Model Structure and Elements

The Open Component Model provides a formal description of
delivery artefacts for dedicated semantics that are accessible
in some kind of repository.

This leads to the following major elements that must be specified
as part of the Open Component Model specification

- [Repositories](#repositories)
- [Components](#components)
- [Component Versions](#component-versions)
    - [Identities](#identities)
    - [Labels](#labels)
    - [Artefacts](#artefacts)
        - [Sources](#sources)
        - [Resources](#resources)
        - [Artefact Access](#artefact-access)
    - [Aggregation](#aggregation)
- [Signatures](#signatures)
- [Repository Contexts](#repository-contexts)

Those elements partly use further sub-level elements that are
defined in the context of their usage.

## Repositories

A *Component Repository* is a dedicated entity that provides technical access
to the other elements of the Open Component Model.

So far, we don't define a repository API for a dedicated technical native
instance of an OCM repository, because we want to use existing storage
subsystems, without the need of running OCM specific servers (Nevertheless,
such an API is still compatible with this specification and could be defined in
the future). 

Therefore, a component repository is typically an interpretation layer
on-top of a given well-known storage
subsystem hosting a content structure adhering to an
[element mapping specification (layer 3 of this specification)](../layer3/README.md)
for this kind of storage backend (e.g. OCI).

So, any tool or language binding can map an existing storage technology into an
OCM repository view by implementing the
[abstract operations (layer 2 of this specification)](../layer2/README.md))
using this specification for the dedicated storage technology.

If required, an own specification for a native OCM repository (similar to the
[OCI distribution spec](https://github.com/opencontainers/distribution-spec/blob/main/spec.md))
can be added.

A concrete instance of a repository is described by a [*Repository Specification*](../formats/types.md#repository-types))
for which a general simplified [textual denotation](../denotations/README.md#repositories) can be used.

## Components

A *Component* is an abstract entity describing a dedicated usage context or
meaning for provided software. This semantic is defined by the owner of a
component and subsumed by the component identity. It is technically defined
by a globally unique identifier.

A component identifier uses the following naming scheme:

<div align="center">

*&lt;DNS domain>* `/` *&lt;name component> {* `/` *&lt;name component> }*

</div>

Hereby the DNS domain plus optionally any number of leading name components MUST
be owned by the provider of a component. For example, `github.com`, as DNS domain
is shared by lots of organizations. Therefore, all component identities provided
based on this DNS name, must include the owner prefix of the providing
organization, e.g. `github.com/gardener`.

The component acts as a namespace to host multiple [*Component Versions*](#component-versions),
which finally describe dedicated technical artefact sets, which describe the
software artefacts required to run this tool.

*Example:*

The component with the identity `github.com/gardener/external-dns-management`
contains software versions of a tool maintaining DNS entries in DNS providers
based on Kubernetes resource manifests.

Hereby, the prefix `github.com/gardener` describes a *GitHub* organization owned
by the Gardener team developing the component `external-dns-management`.

## Component Versions

A *Component Version* is a concrete instance of a [Component](#components).
As such it describes a concrete set of (software) [Artefacts](#Artefacts)
adhering to the semantic assigned to the containing [Component](#components)
This semantic is subsumed by the identity of the component and defined by its owner.

A component version has a unique identity composed of the [component identity](#components)
and a version name following the [semantic versioning](https://semver.org)
specification. Component versions can be described by a dedicated [textual denotation](../denotations/README.md#component-versions)
(e.g. `github.com/gardener/external-dns-management:0.15.1`).

So, all versions provided for a component should provide software artefacts
with the semantic defined by the component. For example, for a component
pretending to be a Kubernetes DNS Controller, all provided versions should
provide versions of a DNS Controller, and not an ingress controller.

A component version is formally described by a [Component Descriptor](#component-descriptor).

### Component Descriptor

A *Component Descriptor* is used to describe a dedicated component version.
It is a YAML file with the structure defined [here](../formats/compdesc/README.md)

The main purpose of a component version is to describe a set of delivery
[artefacts](#artefacts). Such an artefact set is composed with two
mechanisms:
1) Artefacts can be directly described by a component descriptor
2) Artefacts described by another component version can be included into
   the local artefact set by describing a [reference](#aggregation) to this
   component version.

Those artefact composing elements all feature a common [set of attributes](#composing-the-artefact-set),
which are used to uniquely [identify the elements](#identities) in the context
of their component
descriptor. Additionally, they provide a possibility to formally enrich the
information attached to an element by using an arbitrary number of
appropriately named labels without the need for explicit dedicated model
attributes (for example, attaching hints for the triage of identified
vulnerabilities for this artefact).

A component descriptor describes:
- a history of [Repository Contexts](#repository-contexts) describing
  former repository locations of the component version along a transportation
  chain
- a set of [Labels](#labels) to assign arbitrary kinds of information to the
  component version, which is not formally defined by the Open Component Model
- an optional set of [Sources](#sources), that were used to generate the
  [Resources](#resources) provided by the component version
- a set of [Resources](#resources) provided with this component version
- an optional set of [References](#aggregation) included component versions
- an optional set of [Signatures](#signatures) provided by some authority
  to confirm some state or origin of the component version

### Composing the Artefact Set

There are several elements in a [component descriptor](#component-descriptor),
which can be used to compose the artefact set finally described by a component
version.

- elements, which directly describe an [artefact](#artefacts) as part of the
  component descriptor.
- [references](#aggregation), which can be used to include artefact sets described
  by other components.

All those descriptive elements share a common basic attribute set.
First, such an element must be uniquely identifiable in the context
of a component version. Therefore, it requires an [*Identity*](#identities).
To be able to attach additional formal meta information to such an element, which
is not directly described by existing model elements, it is possible to
define arbitrary [*Labels*](#labels). This enables the use of application specific
attributes, without the need of extending the basic component model for every
new arising use case.

### Identities

[Resources](#resources), [Sources](#sources), and [References](#aggregation)
have a unique identity in the context of a [Component Version](#component-versions).

All those element types share the same notion of an identity, which is a set
of key/value string pairs.
Such a set includes at least the `name` attribute of those elements.
If the element name cannot be chosen uniquely an optional `version` attribute
can be provided to assure uniqueness in the context of the [component version](#component-versions)
(and the type of element).
In such a case this attribute will be added to the effective identity
attribute set.
If even this is not sufficient to meet the requirements to identify
elements in the context of the component version, explicit identity attributes
can be defined. If given, all those
attributes always contribute to the identity of the element.

The element identity is composed by the following formal fields of an element:

- **`name`** (required) *string*

  The name of the element. In most of the cases the name should be chosen
  to be unique in the context of the list of elements.
  It basically also expresses the meaning or purpose of the element in the
  context of the component version. But it might be the
  case that multiple elements should be used for the same purpose. For example,
  a component version is used to describe multiple versions of an artefact,
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
  and must be given to uniquely identify an element.

Using multiple attributes of an artefact for its identity makes it easier to formally
describe the identity and to select a dedicated artefact from the set of
described artefacts. It avoids the need to
marshal a dedicated identity scheme for an intended usage scenario into a
single attribute value. Instead, different attributes can be used to represent
the dedicated selection dimensions. Selecting all artefacts for a partial set
of constraints is then just a partial match of the set of identity attributes.

For example:

You want to describe different image versions to be used
for different Kubernetes versions and for multiple purposes. With the identity
attributes this can easily be modeled by using
- the `name` attribute for the purpose (e.g. DNS controller)
- the `version` attribute for the image version
- and an extra identity attribute for the intended Kubernetes Version.

Then you don't need to derive artificially unique artefact names, instead
the identity of the artefact can naturally be composed by using appropriate
attributes. Selecting all artefacts for a dedicated purpose is possible
by selecting all artefacts with the appropriate `name` attribute, without the
need of parsing an artificial structure imprinted on the name attribute.

<div align="center"> 
<img src="ocmidentity.png" alt="Identities" width="800"/>
</div>

Every identity carrying element described by the Open Component Model can
therefore be identified by the triple *(Component Identity, Version Name,
Local Element Identity)*.

### Labels

*Labels* can be used to add additional formal information to a component
model element, which do not have static formal fields in the
[component descriptor](#component-descriptor). Its usage is
left to users of the component model, or better to the used toolsets
looking at component versions (for example: a scanning environment,
used to scan artefacts for vulnerabilities, uses a dedicated label
to control its behavior).

To be able to evaluate labels used by dedicated tool environments for any
[component version](#component-versions), the same
label name must have the same meaning, regardless by which component provider
they are generated. To assure that this information
has a globally unique interpretation or meaning, labels must comply with some
naming scheme and use a common [structure](../formats/types.md#label-names).

Labels are described by the element field

- **`labels`** *[]label*

  A list of arbitrary labels described by a formal name with a globally
  unique meaning (see [label structure](../formats/types.md#label-names)

### Artefacts

An *Artefact* is a blob containing some data in some technical format.
Every artefact described by the component version has
- an [Identity](#identities) in the context of the component version
- a dedicated globally unique [type](../formats/types.md#artefact-types) representing
  the kind of content and how it can be used
- a set of [Labels](#labels) to assign arbitrary kinds of information to the
  component version, which is not formally defined by the Open Component Model.
- a formal description of the [Access Specification](#artefact-access) ,
  which can be used to technically access the content of the artefact in form of
  a blob with a format defined by the artefact type. If there are multiple variants
  possible for the blob format, the access specification must be able to
  describe an optional media type. Applying an access specification always
  yields a media type. It might be implicitly provided the [implementation of
  an access method](../layer2/README.md#access-method-operations) or explicitly provided by the
  access specification.
- a (optional) digest of the artefact that is immutable during transport steps.

Those attributes are described by formal fields of the element description
in the component descriptor:

- the [identity](#identities) fields are directly embedded

- **`type`** (required) *string*

  The [type of an artefact](../formats/types.md#artefact-types) uniquely specifies the
  technical interpretation of an artefact, its kind, independent of its
  concrete technical representation.

  If there are different possible technical representation the [access method](#artefact-access)
  returns the concrete format used for the returned blob.

  For example, a helm chart (type `helmChart`) can be represented as
  OCI artefact or helm chart archive. Nevertheless, the technical meaning is
  to be a helm chart, even if represented as OCI image. The type `ociImage`
  describes an object that can be used as container image. So, although the
  technical representation might in both cases be an OCI image manifest, its
  semantics and use case is completely different. This is expressed
  by the chosen type of the artefact, which focuses on the semantics.

- **`labels`** (optional) *[]label*

  A list of arbitrary labels described by a formal name with a globally
  unique meaning (see [label structure](../formats/types.md#label-names)

- **`access`** (required) *access specification*

  The [access specification](../formats/types.md#access-method-types) for the actual artefact.
  The specification is typed. The type determines an access method to use
  to access the artefact blob. This type determines the technical procedure
  to use to access the artefact blob as well as the specification of the
  attributes that are required by this procedure to be able to identify a
  dedicated target blob.

The Open Component Model distinguishes two kinds of artefacts:
- [*Sources*](#sources) are optional artefacts that contain the sources, which
  were used to generate the deployment-relevant *Resources*
- [*Resources*](#resources) are artefacts that finally make up the deployment
  relevant set of artefacts

#### Sources

A *Source* is an [Artefact](#artefacts), which describes the sources that were
used to generate one or more of the [Resources](#resources) described by the
[component descriptor](#component-descriptor). This information might be used
by scanner tools to extract more information about then final binaries.

Source elements do not have specific additional formal attributes.

#### Resources

A *Resource* is a delivery [Artefact](#artefacts),
intended for deployment into a runtime environment, or describing additional
content, relevant for a deployment mechanism. For example, installation procedures
or meta-model descriptions controlling orchestration and/or deployment mechanisms.
(A simple example how such elements could be used to construct a deployment
mechanism on top of the Open Component Model can be found [here](../../scenarios/toi/README.md).)

The Open Component Model makes absolutely no assumptions, about how content described
by the model is finally deployed or used. All this is left to external tools and tool
specific deployment information is formally represented as other artefacts with
an appropriate dedicated own type.

In addition to the common [artefact](#artefacts) information, a resource
may optionally describe a reference to the [source](#sources) by specifying
its artefact identity.

A resource uses the following additional formal fields:

- **`digest`** (optional) [*digest*](#digest-info)

  If the component descriptor is signed (directly or indirectly by one of its
  referencing component versions), a digest of a resource is stored along with
  the resource description. This is required because there might be different
  digest and resource normalization algorithms.

- **`srcRef`** (optional) *struct*

  This field is used to describe the sources used to generate the resource.
  The selection is done by the following two fields:

    - **`identitySelector`** *map[string]string*

      [Identity attributes](#identities) determining an appropriate [source](#sources)
      element.

    - **`labels`** (optional) *[]label

      A list of arbitrary labels described by a formal name with a globally
      unique meaning (see [label structure](../formats/types.md#label-names)) can be used
      to attach more information about the part or kind of usage of the sources.


#### Artefact Access

The technical access to the physical content of an
[artefact](#artefacts) described as
part of a [Component Version](#component-versions) is expressed by an
[*Access Specification*](../formats/formats.md#access-specifications).
It describes the [type](../formats/types.md#access-method-types) of
the *access method* and the type-specific access path to the content in the
[repository context](#repository-contexts) the component descriptor has been
retrieved from.

The content of a described artefact is accessible by applying its
global identity triple to the following procedure:

- [lookup](../layer2/README.md#mandatory-operations) of a [component version](#component-versions)) and its
  [component descriptor](#component-descriptor) by using its
  component identity and version name in
  the desired [repository context](#repository-contexts)
- identify the artefact by its local [identity](#identities) (distinguish between [source](#sources)
  and [resource](#resources))
- [apply](../layer2/README.md#access-method-operations) the described [access method](#artefact-access)

<div align="center"> 
<img src="ocmresourceaccess.png" alt="Structure of OCM Specification" width="800"/>
</div>

### Aggregation

A [component version](#component-versions) may refer to other component versions
by adding a *Reference* to the component version.

A component version reference describes only the component version and no location or OCM
repository. It is always evaluated in the actual repository context.
This means, that the artefact set described by the referenced component version
is added to the local artefact set described by the component version defining
the reference. To keep a unique addressing scheme, like [artefacts](#artefacts),
references have an [identity](#identities).

A reference element has the following additional formal fields:

- **`componentName`** (required) *string*

  The identity of the component whose version is referenced.
  The elements common version field is required in this usage context.

### Artefact References

Following the chain of [references](#aggregation), starting from an initial
[component version](#component-versions),
any local or non-local artefact can be addressed relative to a component
version by a possibly empty sequence (for a local artefact) of reference
[identities](#identities)) followed by the artefact identity in the context of the finally
reached component version.

Such a composite, consisting of an artefact identity and a sequence of reference
identities is called relative *Source Reference* or *Resource Reference*.
It can be used in artefacts described by a [component version](#component-versions)
to refer to other artefacts described by the same component version containing the
artefact hosting the relative reference.

*Example:*

CompVers: `A:1.0.0`
```
- Resources: 
  - name: DEPLOYER
  - type: mySpecialDeploymentDescription
- 
- References:
  - name: content
    component: B:1.0.0
```

CompVers: `B:1.0.0`
```
- Resources:
  - name IMAGE
    type: ociImage
```

The deployment description contained in CompVers `A:1.0.0` may have
the following content

```
...
deploymentImages:
  - resource:
      name: IMAGE
      referencePath:
      - name: content
```

This description contains a resource reference indicating to
use the resource `IMAGE` in component version `B:1.0.0` when evaluated
in the context of component version `A:1.0.0`.

This way any content-related tool can interact with the Open Component Model,
by identifying resources and finally access resources described by the component
model.

This kind of relative access description is location-agnostic, meaning, independent
of the [repository context](#repository-contexts) used to access
the initial component version and resource. The stored description only
includes identities provided by the model. They can then be evaluated in a
dedicated repository context to finally obtain the artefact content
(or location) in the actually used environment (for example, after
transportation into a fenced environment).

Depending on the transport history of the component version, the
correct artefact location valid for the actual environment is used.

#### Absolute Artefact References

A relative reference can be extended to an location-agnostic absolute reference by extending
the pair by a third value, a component version identity.


<div align="center">

( *&lt;Component Version>* , *&lt;Reference Path> {* , *&lt;Local Artefact Identity> }* )

</div>

In a dedicated interpretation environment such a location-agnostic reference can again be 
transferred into a location-specific reference by adding a [repository-context](#repository-contexts).

Such a reference can then be used to finally address the content of this artefact by the
following procedure:

- gain access to the OCM [repository](#repositories) described by the repository context.
- gain access to the [component version](#component-versions), respectively the [component descriptor](#component-descriptor),
  by a [lookup operations](../layer2/README.md#mandatory-operations)
- follow the [resolution procedure for the relative artefact reference](#artefact-access).

## Signatures

A [component version](#component-versions) may be signed by some authority.
It is possible to have multiple signatures in the [component descriptor](#component-descriptor).

When signing a component version, all included component versions are
digested by digesting their [resources](#resources) and normalizing
their component descriptors (see [Digest Info](#digest-info)).

Every signature entry has the following formal fields:

- **`name`** (required) *string*

  The name if the signature. It must be unique in the context of a component
  version.

- **`digest`** (required) [*digest*](#digest-info)

  The digest of the component version used to generate the signature.
  Different signatures may use different digest algorithms.

  The digest of a component version does not include volatile fields, like
  the access specification, which can change along a transportation chain.

- **`signature`** (required) [*signature*](#signature-info)

  The signature for the specified digest.


##### Digest Info

A digest is specified by the following fields:

- **`hashAlgorithm`** (required) *string*

  The used digest algorithm.

- **`normalisationAlgorithm`** (required) *string*

  The used normalization algorithm for the signed element.

  For example, the digest of a component version must not include volatile
  fields, like
  the access specification, which can change along a transportation chain.
  To achieve a stable byte stream for calculating the digest, the component
  descriptor is transformed into a normalized form. The method to do so
  is specified by the normalization algorithm.

  Even artefact blobs can be normalized, for example the technical representation
  of an OCI image may depend on the access method. But the digest should be independent
  of the technical representation. The default is to just use the blob digest,
  but for OCI images the digest of the image manifest is used, regardless of the
  technical representation.

  This is handled by *Digest Handlers*, which can be defined for dedicated
  artefact type and media type combinations. All implementations must provide
  appropriate handlers for the used resources types to be interoperable.

- **`value`** (required) *string*

  The digest itself.

##### Signature Info

A signature is specified by the following fields:

- **`algorithm`** (required) *string*

  The used signing algorithm.

- **`mediaType`** (required) *string*

  The media type of the technical representation of the signature value.

- **`value`** (required) *string*

  The signature itself.

- **`issuer`** *string*

  The description of the issuer.

## Repository Contexts

A *Repository Context* describes the access to an [OCM Repository](#repositories).

This access is described by a [formal and typed specification](../formats/formats.md#repository-specifications).
A [component descriptor](#component-descriptor) may contain information
about the transport history by keeping a list of repository contexts.
It SHOULD at least describe the last repository context for a remotely accessible
OCM repository it was transported into.
