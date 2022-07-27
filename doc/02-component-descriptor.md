# Component Descriptor Specification

Usually, complex software products are divided into logical units, which are called **components** in this specification.
For example, a software product might consist of three components, a frontend, a backend and some monitoring stack.
Of course, the software product itself could be seen as a component comprising the other three components.

As a result of the development phase, **component versions** are created, e.g. when you make a new release of a component.

A component version consists of a set of technical artifacts, e.g. docker images, helm charts, binaries,
configuration data etc. Such artifacts are called **resources** in this specification.

Resources are usually build from something, e.g. code in a git repo, named **sources** in this specification.

The OCM introduces a so called **Component Descriptor** for every component version, to describe the resources, sources
and other component versions belonging to a particular component version and how these could be accessed.

For the three components in our example software product, one *Component Descriptor* exists for every component version,
e.g. three *Component Descriptor* for the three versions of the frontend, six for the six versions of the backend etc.

Not all component version combinations of frontend, backend and monitoring are compatible and build a valid product version.
In order to define reasonable version combinations for our software product, we could use another feature of
the *Component Descriptor*, which allows the aggregation of component versions.

For our example we could introduce a component for the overall product. A particular version of this product component
is again described by a *Component Descriptor*, which contains references to particular *Component Descriptors* for the
frontend, backend and monitoring.

This is only an example how to describe a particular product version with OCM as a component with one
*Component Descriptor* with references to other *Component Descriptors*, which itself could have such references and so on.
You are not restricted to this approach, i.e. you could still just maintain a list of component version combinations which
build a valid product release. But OCM provides you a simple approach to specify what belongs to a product version.
Starting with the *Component Descriptor* for a product version and following the component references, you could
collect all artifacts, belonging to this product version.

**Todo: Perhaps some small example image to make this more clear?**

*Component Descriptors* are the central concept of OCM. A *Component Descriptor* describes what belongs to a particular
version of a software component and how to access it. This includes:

- resources, i.e. technical artifacts like binaries, docker images, ...
- sources like code in github
- references to other software component versions

## Component Descriptor Format Specification

A *Component Descriptor* is a [YAML](https://yaml.org/) or [JSON](https://www.json.org/json-en.html) document
according to this [schema](component-descriptor-v2-schema.yaml). Additional fields are not allowed.

In serialised form, *Component Descriptors* MUST be UTF-8-encoded. Either YAML, or JSON MUST be used. If YAML is used
as serialisation format, only the subset of features defined by JSON MUST be used, thus allowing conversion to a
JSON representation.

YAML is recommended as preferred serialisation format.

YAML permits the usage of comments, and allows different formatting options. None of those are by contract part of a
*Component Descriptor*, thus implementations may arbitrarily choose to retain or not retain comments or formatting
options.

The order of attributes is insignificant, and MUST NOT be relied upon.

The order of elements in sequences MAY be significant and MUST be retained in cases where it is significant.

## Schema Version

A *Component Descriptor* document consists of two top level elements: *meta*, *component*

|  | Description |
| --- | --- |
| meta | Contains the schema version of the *Component Descriptor* specification. This document defines schema version *v2*. |
| component | Definition of the artifacts which belong to the component version. |

Example:

```
meta:
  - schemaVersion: "v2"
component:
  ...
```

## Component

The *component* field of a *Component Descriptor* has the following fields:

|  | Description |
| --- | --- |
| name | Component name |
| version | Component version |
| repositoryContexts | Locations of the *Component Descriptor* in a transport chain |
| provider | Provider of the component, e.g. a company, organization,... |
| sources | Array of references to sources |
| resources | Array of references to resources |
| componentReferences | Array of references to other *component versions* described by *Component Descriptors* |
| labels | Optional field to add additional information/extensions |

### Component Name and Version

Every *Component Descriptor* has a name and version, also called component name and component version. Name and version 
are the identifier for a *Component Descriptor* and the component version described by it.

```
meta:
  - schemaVersion: "v2"
component:
  name: ...
  version: ...
```

Component names reside in a global namespace. To avoid name conflicts component names MUST start with a valid domain
name (as specified by [RFC-1034](https://www.rfc-editor.org/info/rfc1034), [RFC-1035](https://www.rfc-editor.org/info/rfc1035)) 
followed by an optional URL path suffix (as specified by [RFC-1738](https://www.rfc-editor.org/info/rfc1738)).

Examples are:

- *github.com*
- *github.com/pathToYourRepo*

If no URL path suffix is specified, the domain MUST be possessed by the component owner. If a URL path suffix is 
specified, the namespace started by the concatenation of domain and URL path suffix MUST be controlled by the 
component owner.

A component name SHOULD reference a location where the component’s resources (typically source 
code, and/or documentation) are hosted. An example and recommended practise is using GitHub repository names for 
components on GitHub like *github.com/path-of-your-repo*.

Component versions refer to specific snapshots of a component. A common scenario being the release of a component.
Component versions MUST adhere to a loosened variant of [Semver 2.0.0](https://semver.org/).

Different to strict semver 2.0.0, component versions MAY:

- have an optional v prefix
- omit the third level (patch-level); if omitted, path-level is implied to equal 0

### References

Components versions are typically built from sources, maintained in source code management systems,
and transformed into resources (for example by a build), which are used at installation or runtime of the product.

Each *Component Descriptor* contains a field for references to the used sources and a field for references
to the required resources.

A component version might have also references to other component versions. The semantic of component references
is, that the referencing component version comprises the referenced component versions, i.e. it is an aggregation or
composition semantic.

A *Component Descriptor* has a field to specify references to other *Component Descriptors* and thereby to the component
versions described by them.

### References to Sources

The fields for references to sources are:

|  | Description |
| --- | --- |
| name | Logical name of the reference withing the *Component Descriptor* |
| extraIdentity | Optional field that in combination with the name and version uniquely identifies a reference within a *Component Descriptor* |
| version | Version of the reference in the *Component Descriptor* |
| type | Logical type. Specifies the content of the referenced sources, e.g. if it is git repository. |
| access | Access information to the location where the sources are located. MUST contain another type field describing the access method. |
| labels | Optional field to add additional information/extensions |

Example for a source reference:

```
...
component:
  sources:
  - name: example-sources-1
    version: v1.19.4
    type: git
    access:
      commit: e01326928b6f9825dba9fa530b8d4917f93194b0
      ref: refs/tags/v1.19.4
      repoUrl: github.com/gardener/example-sources-1
      type: github
      ...
```

### References to Resources

The fields for references to sources are:

|  | Description |
| --- | --- |
| name | Logical name of the reference withing the *Component Descriptor* |
| extraIdentity | Optional field that in combination with the name and version uniquely identifies a reference within a *Component Descriptor* |
| version | Version of the reference in the *Component Descriptor* |
| relation | “local” if the resource is derived from a source declared by the same component. “external” otherwise. |
| type | Logical type. Specifies the content of the referenced resource, e.g. if it is a helm chart, a JSON file etc. |
| access | Access information to the location of the resource. MUST contain an additional type field describing the access method. |
| srcRefs | If the corresponding resource was build from "local" sources, these could be listed here by providing their identifier within the *Component Descriptor*, i.e. their names and extraIdentities. |
| labels | Optional field to add additional information/extensions |

Example for resource references:

```
...
component:
  resources:
    - name: external-monitoring
      version: v0.8.3
      relation: external
      type: ociImage
      access:
        imageReference: example.com/monitoring:v0.8.3
        type: ociRegistry
...
```

Sources and resources declare through their access attribute a means to access the underlying artifacts.
This is done by declaring an access type (for example an OCI Image Registry), which defines the protocol through which
access is done. Depending on the access type, additional attributes are required (e.g. an OCI Image Reference).

OCM specifies the format and semantics of particular access types for particular resources and sources later in this 
specification.

### References to Components

The fields for references to sources are:

|  | Description |
| --- | --- |
| name | Logical name of the reference withing the *Component Descriptor*. |
| extraIdentity | Optional field that in combination with the name and version uniquely identifies a reference within a *Component Descriptor* |
| componentName | Component name of the referenced *Component Descriptor* |
| version | Component version of the referenced *Component Descriptor* |
| labels | Optional field to add additional information/extensions |

Example for component references:

```
component:
  componentReferences:
  - name: name-1
    componentName: github.com/.../component-name-1
    version: v1.38.3
  - name: name-2
    componentName: .../component-name-2
    version: v0.11.4 
```

As elaborated later in the context of *Component Repositories*, references to components do not need to declare an 
access attribute. The lookup is always done by their name and version.

### Identifier for Sources, Resources and Component References

Every entry in the *sources*, *resources* and *componentReferences* fields has a *name* field. The following restrictions
for valid names are defined:

- lower-cased alphanumeric ([a-z0-9])
- special characters ([-_+])
- any other characters are NOT acceptable
- names SHOULD consist of at least two, and less than 64 characters
- names MUST start with a lowercase character ([a-z])

Every *source*, *resource* or *componentReference* needs a unique identifier in a *Component Descriptor*.
In particular situations the name and version are not sufficient, e.g. if docker images for different platform are included.
Therefore, every entry has an additional optional field *extraIdentity* to resolve this problem, i.e. every entry
MUST have a unique combination of *name*, *version*, *extraIdentity* and formal type (*source*, *resource* or 
*componentReference*) within a *Component Descriptor*.

An *extraIdentity* is a map, of key value pairs whereby:

- The keys MUST adhere to the same restrictions defined for name values (see above)
- The values MUST be UTF-8-encoded non-empty strings.

Two *extraIdentities* are equal if they have the same key value pairs whereby the order is not relevant.

Example for two resource entries with the same name and version but different extra identities and therefore different identifier:

```
component:
  resources:
  - name: name-1
    version: 1.0.0
    extraIdentity:
      platform: "arm64"
      country: "us"
    ...
  - name: name-1
    version: 1.0.0
    extraIdentity:
      platform: "x86_64"
      country: "de"
    ...
```

### Labels

According to the [schema](component-descriptor-v2-schema.yaml) for the *Component Descriptor*, additional fields are 
not allowed. This express application specific extensions, every entry in the *sources*, *resources* and 
*componentReferences* fields, and the component itself may declare optional labels. 

Labels is a map, of key value pairs whereby:

- The keys MUST adhere to the same restrictions defined for name values (see [above](#identifier-for-sources-resources-and-component-references))
- The values MUST be either JSON or JSON compatible YAML.

Example:

```
component:
  labels:
    maintainer: "maintainer@my-component.net"
    tags: "monitoring,logging,internal"
  ...
```

### Repository Contexts

Every *Component Descriptor* has a field *repositoryContexts* containing an array of access information of 
*Component Descriptor Repositories*, i.e. stores for *Component Descriptors* which are specified later. 

The array of access information describes the transport chain of a *Component Descriptor* through different
*Component Descriptor Repositories*, whereby the last entry describes the current *Component Descriptor Repository*,
in which the *Component Descriptor* is stored.

The *repositoryContexts* are usually not specified manually in the *Component Descriptor*, but are rather set 
automatically when a component version is uploaded to a *Component Repository*. 



