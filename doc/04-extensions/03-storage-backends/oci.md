# OCI Registries

OCM component versions can be stored in OCI registries which are conforming to the [OCI distribution specification](https://github.com/opencontainers/distribution-spec/blob/main/spec.md). Additionally, a registry must support a deep repository structure.

## Specification Format

To describe a repository context for an OCM repository conforming to this specification the following repository specification format MUST be used.

### Synopsis

```text
type: OCIRegistry[/VERSION]
[ATTRIBUTES]
```

```text
type: ociRegistry[/VERSION]
[ATTRIBUTES]
```

### Description

Component descriptors and their artifacts will be mapped to an OCI registry according to the [OCI distribution specification](https://github.com/opencontainers/distribution-spec/blob/main/spec.md).

### Specification Versions

Supported specification version is `v1`.

#### Version `v1`

The type specific specification fields are:

- **`baseUrl`** *string*

  OCI registry reference. This is just the hostname, e.g. eu.gcr.io. Any specific repository can be specified using parameter `subPath`.

- **`subPath`** (optional) *string*

  The base repository name used for the OCM repository. The OCM based artifacts will use this path as repository prefix. An OCI registry may host many OCM repositories with different repository prefixes.

- **`componentNameMapping`** (optional) *string*

  This attribute describes how component names are mapped to OCI artifact repositories.
  There are two flavors:
  - `urlPath` (default) the component name is directly used as part of the OCI repository name.
  - `sha256-digest` (not used anymore) the digest of the component name is used to limit the length of the OCI repository name.

## Element Mapping

An OCI registry can be used to host multiple OCM repositories. Such an OCM repository is identified by an OCI repository reference.

<div align="center">

 &lt;*host*&gt;\[`:`&lt;*port*>]{`/`&lt;*repository part*>}

</div>

An OCM *component identifier* is mapped to a sub *repository name* prefixed with `component-descriptors/`. The complete repository name is

<div align="center">

*&lt;OCI base repository>* `/component-descriptors/` *&lt;component id>*

</div>

An OCM *version name* of a component version is mapped to an OCI *tag*.

The *component version* is represented as OCI *image manifest*.

This manifest uses a config media type `application/vnd.ocm.software.component.config.v1+json`.
According to the [OCI image specification](https://github.com/opencontainers/image-spec/blob/main/spec.md) this must be a JSON blob. This json file has one defined formal field:

- **`componentDescriptorLayer`** (required) [*OCI Content Descriptor*](https://github.com/opencontainers/image-spec/blob/main/descriptor.md)

  It references the layer blob containing the component descriptor. The layer
  always must be layer 0 of the manifest. It uses the media type
  `application/vnd.ocm.software.component-descriptor.v2+yaml+tar`

The descriptor layer contains a tar archive with at least a single file
with the name `component-descriptor.yaml` containing the component descriptor of the
component version. This file should always be the first file in the tar archive.

OCM *Local Blobs* are stored in additional OCI *Image Layers*. The local blob
identifier stored in the `localBlob` access specification is the OCI *blob digest*
of the blob. The media type of the blob is the one specified in the
access specification.

## Version Mapping

The Open Component Model supports version names according to [semantic versioning](https://semver.org/).
The tags used to represent versions in the [OCI specification](https://github.com/opencontainers/distribution-spec/blob/main/spec.md#pulling-manifests) do not allow to directly use semantic version names as tags, becase the plus (`+`) character is not supported. Therefore, the open component model version names have to be mapped
to OCI-compliant tag names.

The followinmg mapping for version is used, here:

- the optional plus `+` character used to attach build information in semantic versions is mapped to the sequence (`.build-`)

Mapping tags back to versions uses the following mappings:

- the last character sequence (`.build-`) is mapped to a plus (`+`) character.

This way the formal parts of a pre-release of semantic version (separated by dots) are kept
unchanged. The build/metadata suffix of a semantic version is just added as optional last pre-release part, where the prefix `build-` is used to indicate its meaning as metadata suffix.

## Blob Mappings

Local blobs with an OCI artifact media type will implicitly be mapped to a regular
artifact. The *reference hint* provided by the specification of the local access
is used to compose a repository name of the form:

<div align="center">

*&lt;oci base repository>* `/` *&lt;reference hint>*

</div>

Without a given tag, the provided external access specification (of type `ociArtifact`)
uses a digest based reference.

Additional blob transformations can be added by registering appropriate blob handlers.

## Example

Given the following component descriptor with a component version consisting of a file and an inline text:

```yaml
apiVersion: ocm.software/v3alpha1
kind: ComponentVersion
metadata:
  name: github.com/open-component-model/spec-example
  provider:
    name: github.com/open-component-model
  version: 1.0.0
repositoryContexts:
- baseUrl: eu.gcr.io
  componentNameMapping: urlPath
  subPath: ghcr.io/open-component-model/spec-example
  type: OCIRegistry
spec:
  resources:
  - access:
      globalAccess:
        digest: sha256:7acd701465611ed8a45d7889b4f3f6ed5e1450ca446f90fd6406cc59ea2baea8
        mediaType: text/plain
        ref: ghcr.io/open-component-model/spec-example/component-descriptors/github.com/open-component-model/spec-example
        size: 26
        type: ociBlob
      localReference: sha256:7acd701465611ed8a45d7889b4f3f6ed5e1450ca446f90fd6406cc59ea2baea8
      mediaType: text/plain
      type: localBlob
    name: noticeplain
    relation: local
    type: blob
    version: 1.0.0
  - access:
      globalAccess:
        digest: sha256:f5ba8322a580272bbaf93678c48881aa799795bafb9998600655fa669f6ea7bd
        mediaType: application/octet-stream
        ref: ghcr.io/open-component-model/spec-example/component-descriptors/github.com/open-component-model/spec-example
        size: 5266
        type: ociBlob
      localReference: sha256:f5ba8322a580272bbaf93678c48881aa799795bafb9998600655fa669f6ea7bd
      mediaType: application/octet-stream
      type: localBlob
    name: logo
    relation: local
    type: blob
```

The OCI image manifest will then have three layers (one for the component-descriptor, one for the logo file and one for the inline text):

```yaml
{
  "schemaVersion": 2,
  "mediaType": "application/vnd.oci.image.manifest.v1+json",
  "config": {
    "mediaType": "application/vnd.ocm.software.component.config.v1+json",
    "digest": "sha256:e63f662a4b600705ed975af69e23fd61d6d68ae1b38d3d3feefbd4df14ce4448",
    "size": 201
  },
  "layers": [
    {
      "mediaType": "application/vnd.ocm.software.component-descriptor.v2+yaml+tar",
      "digest": "sha256:0e75813f479e5486985747d6f741ee63d824097c8ee7e48b558bac608bded669",
      "size": 3072
    },
    {
      "mediaType": "text/plain",
      "digest": "sha256:7acd701465611ed8a45d7889b4f3f6ed5e1450ca446f90fd6406cc59ea2baea8",
      "size": 26
    },
    {
      "mediaType": "application/octet-stream",
      "digest": "sha256:f5ba8322a580272bbaf93678c48881aa799795bafb9998600655fa669f6ea7bd",
      "size": 5266
    }
  ]
}
```

The image configuration is:

```yaml
{
  "componentDescriptorLayer": {
    "mediaType": "application/vnd.ocm.software.component-descriptor.v2+yaml+tar",
    "digest": "sha256:0e75813f479e5486985747d6f741ee63d824097c8ee7e48b558bac608bded669",
    "size": 3072
  }
}
```

If the repo-url is `ghcr.io/open-component-model/spec-example` individual blobs can be accessed using references like

```text
ghcr.io/open-component-model/spec-example/component-descriptors/github.com/open-component-model/spec-example@sha256:f5ba8322a580272bbaf93678c48881aa799795bafb9998600655fa669f6ea7bd
ghcr.io/open-component-model/spec-example/component-descriptors/github.com/open-component-model/mymaspec-exampleriadb@sha256:0e75813f479e5486985747d6f741ee63d824097c8ee7e48b558bac608bded669
ghcr.io/open-component-model/spec-example/component-descriptors/github.com/open-component-model/spec-example@sha256:7acd701465611ed8a45d7889b4f3f6ed5e1450ca446f90fd6406cc59ea2baea8
```

Note that these references are contained in the component-descriptor under the `globalAccess` tag in the resources.
