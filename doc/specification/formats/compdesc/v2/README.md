# Component Descriptor Serialization Version V2

A *Component Descriptor* of version v2 is a [YAML](https://yaml.org/) or [JSON](https://www.json.org/json-en.html) document according to this [schema](json-schema.yaml). Additional fields are not allowed.

In serialised form, *Component Descriptors* MUST be UTF-8-encoded. Either YAML, or JSON MUST be used. If YAML is used as serialisation format, only the subset of features defined by JSON MUST be used, thus allowing conversion to a JSON representation.

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
| component | Definition of the artefacts which belong to the component version. |

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

The inner elements are described in detail in chapter [Types](../../../elements/README.md)
