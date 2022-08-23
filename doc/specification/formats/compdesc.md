# 2.4.2 Component Descriptor
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
components on GitHub like *github.com/path-of-your-repo*‚.

Component versions refer to specific snapshots of a component. A common scenario being the release of a component.
Component versions MUST adhere to a loosened variant of [Semver 2.0.0](https://semver.org/).

Different to strict semver 2.0.0, component versions MAY:

- have an optional v prefix
- omit the third level (patch-level); if omitted, path-level is implied to equal 0