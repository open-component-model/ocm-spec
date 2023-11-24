# Extending the Open Component Model

The OCM specification is designed to be extended in several ways. The definition of such elements is restricted to a minimum set of attributes and may include functional behavior. It typically consists of a type attribute.

Those extension points are used to cover technology-specific aspects to be known either by dedicated implementations of the model or by applications using the model.

There are two different kinds of extensions: functional and semantic.

- Functional extensions

  Functional extensions offer the possibility to enrich an implementation of the Open Component Model with technology-specific parts to support more technology environments, like storage backends for the model or artifacts described by the model.

  The functional extension points are:

  - [Access Methods](#access-methods)
  - [Storage backends](#storage-backends)
  - [Signing Algorithms](#signing-algorithms)
  - [Artifact Digest Normalization](#artifact-digest-normalization)
  - [Label Merge Algorithms](#lable-merge-algorithms)

- Semantic extensions
  
  Semantic extensions offer the possibility to describe the semantics and structure of an element
  by arbitrary types not defined by the Open Component Model itself.

  The semantic extension points are:

  - [Artifact Types](#artifact-types)
  - [Label Types](#label-types)


### Access Methods

The task of an access method is to provide access to the physical content of an artifact described by a component version.
The content is always provided as blob with a dedicated media type, either depending on the access method itself
or the [artifact type](#artifact-types). To fulfill its task an access method gets an access specification.

The list of centrally defined access methods types can be found [here](../04-extensions/02-access-types/README.md)

#### Access Specification

The technical access to the physical content of an artifact described as part of a Component Version is expressed
by an *Access Specification*. It specifies which access method to use and additionaly the type-specific attributes,
which are required by the access method to access the content. In an implementation the *Access Method Type* is mapped
to code for finally accessing the content of an artifact.

#### Access Method Names

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

#### Access specification format

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



### Label Merge Algorithms

### Storage Backends

### Signing Algorithms

### Artifact Digest Normalization

### Artifact Types 

Artifact types describe the meaning of an artifact independent of their technical representation in a blob format.
The artifact types defined by the core model (this specification) are described
in section [Artifact Types](02-elements-toplevel.md#artifact-types)

### Label Types

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
