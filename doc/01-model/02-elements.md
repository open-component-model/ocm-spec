
# Model Elements

The following section describes how a component (version) is specified in more detail. Please note that this section intends to give an overview and explain the principal elements and their structure. It is not a complete specification. See the [schemas](https://github.com/open-component-model/ocm/tree/main/resources) for a full definition.

## Components and Component Versions

A component version describes several kinds of elements.

- Artifacts represent technical content. They appear in two different flavors:
  - *Sources* describe the sources a component version  has been composed/generated from.
  - *Resources* describe the delivery artifacts contained in the component version.
- References describe the aggregation of other component versions.

All those described elements share a common set of metadata.

## Artifacts (Resources and Sources)

The Open Component Model distinguishes two kinds of artifacts:
- *Sources* are optional artifacts that contain the sources, which
  were used to generate the deployment-relevant *Resources*.
- *Resources* are artifacts that finally make up the deployment-relevant set of artifacts.

An *Artifact* is a blob containing some data in a technical format.
Every artifact described by the component version has

- an *Identity* in the context of the component version
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


### Artifact Types

The formal type of an artifact uniquely specifies the logical interpretation of an artifact and its kind, independent of its concrete technical representation.

If there are different possible technical representations, the access specification determines the concrete format given by a media type used for the returned blob.

For example, a helm chart (type `helmChart`) can be represented as OCI artifact or helm chart archive. Nevertheless, the technical meaning is the same. In both cases the artifact (resource)`type` will be `helmChart`. The acess specification however will be different. In the first case it will refer to the helm-chart archive. In the second case it the access type will be `ociImage`.

```yaml
  - access:
      helmChart: mariadb:12.2.7
      helmRepository: https://charts.bitnami.com/bitnami
      type: helm
    name: mariadb-chart
    relation: external
    type: helmChart
    version: 12.2.7
```

```yaml
...
  resources:
  - name: mariadb-chart
    relation: local
    type: helmChart
    version: 12.2.7
    access:
      imageReference: ghcr.io/open-component-model/helmexample/charts/mariadb:12.2.7
      type: ociArtifact
```

The access type `ociArtifact` however is also used for container images:

```yaml
  resources:
  - name: mariadb-image
    version: 10.11.2
    relation: external
    type: ociImage
    access:
      imageReference: bitnami/mariadb:10.11.2
      type: ociArtifact
```

The resource type `ociImage` now describes an object that can be used as a container image. So, the technical representation in both cases will be an OCI image manifest. The semantics how these objects can be used are completely different. This is expressed by the `type` of the artifact.

An artifact's kind and logical interpretation is encoded into a simple string. The artifact type must be globally unique. OCM defines a naming scheme to guarantee this uniqueness.

There are two kinds of types:

- Centrally defined type names managed by the OCM organization

  These types use flat names following a camel case scheme with the first character in lower case (for example `ociArtifact`).

  Their format is described by the following regular expression:

  ```regex
  [a-z][a-zA-Z0-9]*
  ```

- Vendor specific types

  Any organization may define dedicated types on their own. Nevertheless, the meaning of those types must be defined. There may be multiple such types provided by different organizations with the same meaning. Organizations should share and reuse such types instead of introducing new type names.

  To support a unique namespace for those type names vendor specific types MUST follow a hierarchical naming scheme based on DNS domain names. Every type name has to be preceded by a DNS domain owned by the providing organization (for example `landscaper.gardener.cloud/blueprint`). The local type must follow the above rules for centrally defined type names
  and is appended, separated by a slash (`/`).

  So, the complete pattern looks as follows:

  ```
  <DNS domain name>/[a-z][a-zA-Z0-9]*
  ```

## Sources

A *Source* is an artifact which describes the sources that were used to generate one or more of the resources. Source elements do not have specific additional formal attributes.

Example:

```yaml
  ...
  sources:
  - name: ocm_source
    version: 0.1.0
    type: git
    access:
      commit: 9b2cf6ced322c7b938533caa22d5a5f48105b3ab
      ref: refs/heads/main
      repoUrl: github.com/open-component-model/ocm
      type: github
```

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

Example:

```yaml
...
  resources:
  - name: image
    relation: external
    type: ociImage
    version: 1.0.0
    access:
      imageReference: gcr.io/google_containers/echoserver:1.10
      type: ociArtefact
```

## References

A component version may refer to other component versions by adding a *reference* to the component version.

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

Example:
```yaml
...
  references:
  - name: installer
    version: 0.1.0
    componentName: github.com/open-component-model/ocmhelminstaller
```

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

```yaml
...
component:
  name: github.com/open-component-model/ocmcli
  version: 0.3.0
  extraIdentity:
    arch: amd64
    os: linux
  resources:
  ...
...
```

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

The technical access to the physical content of an artifact described as part of a Component Version is expressed by an *Access Specification*. It describes the type of the *access method* and the type-specific access path to the content. In an implementation the *Access Method Type* is mapped to code for finally accessing the content of an artifact.

The content of a described artifact is accessible by applying its global identity triple to the following procedure:

- lookup of a component version in a component descriptor by using its component identity and version name in the desired repository context.
- identify the artifact by its local identity
- apply the described access method

<div align="center">
<img src="ocmresourceaccess.png" alt="Structure of OCM Specification" width="800"/>
</div>

The access specification of an artifact may change when component versions are transported among repositories. The set of access methods is not fixed. Because of this extensibility the names of access methods must be globally unique.

There are two flavors of method names:

- Centrally provided access methods

  Those methods should be implemented by OCM compliant libraries and tools. Using only such
  access methods guarantees universal access.

  These types use flat names following a camel case scheme with the first character in lower case (for example `ociArtifact`).

  Their format is described by the following regexp:

  ```regex
  [a-z][a-zA-Z0-9]*
  ```

- Vendor specific types

  Any organization using the open component model may define additional access methods on their own. Their name MUST be globally unique. There may be multiple such types provided by different organizations with the same meaning. Organizations should share such types and reuse existing types instead of introducing new type names.

  Using component versions with vendor specific access methods always means a restriction on using tools implementing these access methods. FOr exchanging such component versions involved parties must agree on the used toolset.

  To support a unique namespace for those type names vendor specific types MUST follow a hierarchical naming scheme based on DNS domain names. Every type name has to be suffixed by a DNS domain owned by the providing organization. The local type must follow the above rules for centrally defined type names and suffixed by the namespace separated by a dot (`.`)

  So, the complete pattern looks as follows:

  ```
  [a-z][a-zA-Z0-9]*\.<DNS domain name>
  ```

Every access method type must define a specification of the attributes required to locate the content. This specification may be versioned. Therefore, the type name used in an access specification may include a specification version appended by a slash (`/`). The version must match the following regular expression:

```
v[0-9]+([a-z][a-z0-9]*)?
```

Examples:
- `ociArtifact/v1`
- `myprotocol.acme.org/v1alpha1`

If no version is specified, implicitly the version `v1` is assumed.

The access method type is part of the access specification. The access method type may define
additional specification attributes required specify the access path to the artifact blob.

For example, the access method `ociBlob` requires the OCI repository reference
and the blob digest to be able to access the blob.

```yaml
...
  resources:
  - ...
    access:
      imageReference: ghcr.io/jensh007/ctf/github.com/open-component-model/ocmechoserver/echoserver:0.1.0
      type: ociArtefact
```

### Access Types
Access methods are used to access the content of artifacts of a component version.
The type of the methods defines how to access the artifact and the access specification
provides the required attributes to identify the blob and its location.

The following access types are defined:

---
#### gitHub

access to a commit in Git repository

*Synopsis:*
```
type: gitHub/v1
```

*Media type for blobs*

`application/x-tgz`

The artifact content is provided as g-zipped tar archive

*Specification Versions*

Supported specification version is `v1`

*Attributes*


- **`repoUrl`**  *string*

  Repository URL with or without scheme.

- **`ref`** (optional) *string*

  Original ref used to get the commit from

- **`commit`** *string*

  The sha/id of the git commit

---
#### helm

*Synopsis:*
```
type: helm/v1
```
*Specification Versions*

Supported specification version is `v1`

*Attributes*

- **`helmRepository`** *string*

  Helm repository URL.

- **`helmChart`** *string*

  The name of the Helm chart and its version separated by a colon.

- **`caCert`** *string*

  An optional TLS root certificate.

- **`keyring`** *string*

  An optional keyring used to verify the chart.

---
#### localBlob

access to a resource blob stored along with the component descriptor

It's implementation of an OCM repository type how to read the component descriptor. Every repository implementation may decide how and where local blobs are stored, but it MUST provide an implementation for this access method.

*Synopsis:*

```
type: localBlob/v1
```

*Attributes*

- **`localReference`** *string*

  Repository type specific location information as string. The value
  may encode any deep structure, but typically an access path is sufficient.

- **`mediaType`** *string*

  The media type of the blob used to store the resource. It may add
  format information like `+tar` or `+gzip`.

- **`referenceName`** (optional) *string*

  This optional attribute may contain identity information used by other repositories to restore some global access with an identity related to the original source.

  For example, an OCI artifact originally referenced using the access method `ociArtifact` is stored during a transport as local artifact. The reference name can then be set to its original repository name. An import step into an OCI repository may then decide to makethis artifact available again as regular OCI artifact using this attribute.

- **`globalAccess`** (optional) *access method specification*

  If a resource blob is stored locally, the repository implementation may decide to provide an external access information (usable by non OCM-aware tools). For example, an OCI artifact stored as local blob can be additionally stored as regular OCI artifact in an OCI registry.

  This additional external access information can be added using a second external access method specification.

---
#### npm

access to an NodeJS package in an NPM registry.

*Synopsis:*
```
type: npm/v1
```
*Specification Versions*

Supported specification version is `v1`

*Attributes*

- **`registry`** *string*

  Base URL of the NPM registry.

- **`package`** *string*

  Name of the NPM package.

- **`version`** *string*

  Version name of the NPM package.

---
#### ociArtifact

Access of an OCI artifact stored in an OCI registry

*Synopsis:*

```
type: ociArtifact/v1
```

*Media type for blobs*

- `application/vnd.oci.image.manifest.v1+tar+gzip`: OCI image manifests
- `application/vnd.oci.image.index.v1+tar.gzip`: OCI index manifests

Depending on the repository appropriate docker legacy types might be used.

*Attributes*

- **`imageReference`** *string*

  OCI image/artifact reference following the possible docker schemes:
    - `<repo>/<artifact>:<digest>@<tag>`
    - `<host>[<port>]/repo path>/<artifact>:<version>@<tag>`


---

#### ociBlob

Access of an OCI blob stored in an OCI repository.

*Synopsis:*
```
type: ociBlob/v1
```
*Specification Versions*

Supported specification version is `v1`

*Attributes*

- **`imageReference`** *string*

  OCI repository reference (this artifact name used to store the blob).

- **`mediaType`** *string*

  The media type of the blob

- **`digest`** *string*

  The digest of the blob used to access the blob in the OCI repository.

- **`size`** *integer*

  The size of the blob

---
#### s3

access to a blob stored in an S3 API compatible bucket

*Synopsis:*
```
type: s3/v1
```
*Specification Versions*

Supported specification version is `v1`

*Attributes*

- **`region`** (optional) *string*

  region identifier of the used store

- **`bucket`** *string*

  The name of the S3 bucket containing the blob

- **`key`** *string*

  The key of the desired blob

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

  Those labels are used by the standard OCM library and tool set to control some behaviour like signing. Labels without a namespace are relevant for the component model itself.

  Such labels use flat names following a camel case scheme with the first character in lower case.

  Their format is described by the following regexp:

  ```regex
  [a-z][a-zA-Z0-9]*
  ```

- vendor specific labels

  any organization using the open component model may define labels
  on their own. Nevertheless, their names must be globally unique.
  Basically there may be multiple such labels provided by different organizations
  with the same meaning. Such label names feature a namespace.

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

### Predefined  Labels

So far, no centrally predefined labels are defined.
There is a standard structure of a label
that includes label meta-data and the concrete label-specific attributes.
Every label must define a specification of its attributes,
to describe its value space. This specification may be versioned.
The version must match the following regexp

```
v[0-9]+([a-z][a-z0-9]*)?
```
So far, no centrally predefined labels are defined.

## Repository Contexts

A *Repository Context* describes the access to an OCM Repository. This access is described by a formal and typed specification. A component descriptor MAY contain information about the transport history by keeping a list of repository contexts. It SHOULD at least describe the last repository context for an OCM repository it was transported into.

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
