# Referencing

A component version may refer to other component versions by adding a reference to the component version. This can be used to compose *aggregations* of component versions.

A component version reference describes only the component version and no location or OCM repository. It is always evaluated in the actual repository context. In this way references are stable across transports.  To keep a unique addressing scheme, like artifacts, references have an identity.

A component version reference refers to another component version by using its identifier. A source or resource of the target component is identified by its `name` attribute (which must be unique within a component version).

## Example

Let's take the following component:
```yaml
component:
  name: github.com/jensh007/mariadb
  version: 10.11.2
  provider: ocm.software
  repositoryContexts:
  - baseUrl: eu.gcr.io
    componentNameMapping: urlPath
    subPath: sap-cp-k8s-ocm-gcp-eu30-dev/dev/d058463/microblog
    type: OCIRegistry
  resources:
  ...
  sources:
  ...
meta:
  ...
```

Here we have a component version mariadb:10.11.2 living in repository context `eu.gcr.io` at some path. Let's take a second component, referring to the this one:

```yaml
component:
  name: github.com/jensh007/microblog-deployment
  version: 0.23.1
  provider: ocm.software
  repositoryContexts:
  - baseUrl: eu.gcr.io
    componentNameMapping: urlPath
    subPath: sap-cp-k8s-ocm-gcp-eu30-dev/dev/d058463/microblog
    type: OCIRegistry
  resources: []
  sources: []
  componentReferences:
  ...
  - componentName: github.com/jensh007/mariadb
    name: mariadb
    version: 10.11.2
  ...
meta:
  ...
```
The reference target is described by the component version identifier and not by the repository location.

