# Attributes of Elements of a Component Version

## Element Identity

Similar to component identity, the element identity is composed by the fields `name` and `version`.
In additon to that sources, resources and references can have an `extraIdentity` if required.

A valid element identity has the following formal fields:

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

*Example:*

You want to describe different image versions to be used
for different Kubernetes versions deployed on different OS platforms and CPU architectures.
With identity attributes this can be easily modeled by using
- the `name` attribute for the purpose (e.g. OCM CLI)
- the `version` attribute for the version
- and an `extraIdentity` attribute for the intended Kubernetes OS platform and architecture
  (here for Linux on arm64 and amd64)

```yaml
component:
  name: github.com/open-component-model/ocmcli
  version: 0.5.0
  provider:
    name: ocm.software
  resources:
  - name: ocmcli
    version: v0.5.0
    access:
      imageReference: ghcr.io/open-component-model/ocm/ocm.software/ocmcli/ocmcli-image_linux_amd64:0.5.0
      type: ociRegistry
    relation: external
    type: ociImage
    extraIdentity:
      architecture: amd64
      os: linux
 - name: ocmcli
    version: v0.5.0
    access:
      imageReference: ghcr.io/open-component-model/ocm/ocm.software/ocmcli/ocmcli-image_linux_arm64:0.5.0
      type: ociRegistry
    relation: external
    type: ociImage
    extraIdentity:
      architecture: arm64
      os: linux
```

Then you don't need to derive artificially unique artifact names. Instead
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

The technical access to the physical content of an artifact described as part of a Component Version is expressed by an *Access Specification*. It describes the type of the *access method* and the type-specific access path to the content. In an implementation the *Access Method Type* is mapped to code for finally accessing the content of an artifact. Access methods and their specification versions can arbitrarely extended. This is a major [extension point](./07-extensions.md#access-methods) of the model.

The content of a described artifact is accessible by applying its global identity triple to the following procedure:

- lookup of a component version in a component descriptor by using its component identity and version name in the desired repository context.
- identify the artifact by its local identity
- apply the described access method

<div align="center">
<img src="ocmresourceaccess.png" alt="Structure of OCM Specification" width="800"/>
</div>

The access specification of an artifact may change when component versions are transported among repositories. 

Examples for access specification types are:

- `ociArtifact/v1`
- `myprotocol.acme.org/v1alpha1`

If no version is specified, implicitly the version `v1` is assumed.

The access method type is part of the access specification type. The access specification type may
define additional attributes required by the access method to provide the described artifact blob.

For example, access method `ociBlob` requires the OCI repository reference and the blob digest to be able to access the blob.

```yaml
...
  resources:
  - ...
    access:
      type: ociArtefact
      imageReference: ghcr.io/jensh007/ctf/github.com/open-component-model/ocmechoserver/echoserver:0.1.0
```

## Labels

*Labels* can be used to add additional formal information to a component model element,
which do not have static formal fields in the component descriptor.
The usage of a model element is left to users of the component model.
The usage of labels is left to the creator of a component version,
therefore the set of labels must be extensible. They can appear ar various locations:

- the component version itself
- resource specifications
- source specifications
- component version references

Elements featuring labels have an additional attribute `labels`,
which is a list of label entries.

A label entry consists of a dedicated set of meta attributes with a predefined meaning.
While arbitrary values are allowed for the label `value`, additional (vendor/user specific)
attributes are not allowed at the label entry level.

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

  non-signature relevant labels (the default) can be modified without breaking a potential signature.
  They can be changed in any repository the component version has been transferred to.
  This is supported to attach evolving information to a component version.
  But it also implies, that a component version must be updatable (re-transferable) in a certain target repository.
  This may lead to conflicting changes which might need to be resolved in a non-trivial way. 

  The merge behaviour can be specified together with the label definition using the `merge` attribute.
  It has the following fields:

  - `algorithm` (optional) *string*

    The name of the algorithm used to merge the label during a transport step.
    This is an [extension point](./07-extensions.md#label-merge-algorithms)
    of the model.

  - `config` (optional) *any*

    A configuration specific for the chosen algorithm.

To be able to evaluate labels for any component version,
the same label name must have the same meaning,
regardless by which component provider they are generated.
To assure that this information has a globally unique interpretation or meaning,
labels must comply with some naming scheme and use a common structure.

Label types are covered by the OCM extension concept, so you can also find information [here](./07-extensions.md#label-types).

## Repository Contexts

A *Repository Context* describes the access to an OCM Repository.
This access is described by a formal and typed specification.
A component descriptor MAY contain information about the transport history
by keeping a list of repository contexts.
It SHOULD at least describe the last repository context
for an OCM repository it was transported into.

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

  The used signing algorithm

- **`mediaType`** (required) *string*

  The media type of the technical representation of the signature value.

- **`value`** (required) *string*

  The signature itself.

- **`issuer`** *string*

  The description of the issuer.
