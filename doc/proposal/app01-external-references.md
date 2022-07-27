# Appendix 1: External Accessible Reference Definitions

A *Component Descriptor* contains references to sources and resources. This could be either references to local blobs or 
to some external accessible artifacts. The format of these references depends on the type of the source or 
resource and the repository where it is stored. This chapter defines different formats for particular external 
accessible sources and resources. This set of predefined formats will be extended over time.  

Predefined reference formats defined in this specification MUST be used if applicable. If there is no matching reference
format defined in the specification, adopters MAY define their own formats. 


## Artifacts stored in OCI Registries

For artifacts stored in an OCI registry the following logical types are defined so far (will be extended):

- ociImage: OCI container image ([see](https://github.com/opencontainers/image-spec/blob/main/spec.md))
- helm.io/chart: helm chart ([see](https://helm.sh/docs/topics/registries/))

The access section looks as follows:

|  | Value | Description |
| --- | --- | --- |
| type | ociRegistry | |
| imageReference | name followed by tag or digest | reference to the OCI artefact, whereby name, tag and digest are specified [here](https://github.com/opencontainers/distribution-spec/blob/main/spec.md#pull) | 

An example for a reference to an OCI container image stored in an OCI registry look as follows: 

```yaml
resources:
  - name: example-name
    type: ociImage
    access:
      type: ociRegistry
      imageReference: name[:tag|@digest]
```

### Git

For Git repositories the following logical type is defined:
- git

The access section looks as follows:

|  | Value | Description |
| --- | --- | --- |
| type | github | |
| commit | | The referenced commit hash |
| ref |  | Some reference e.g. refs/tags/v1.30.1 | 
| repoUrl |  | URL of the git repository e.g. github.com/pathToYourRepo | 

An example looks as follows:

```yaml
sources:
  - name: example-name
    type: git
    access:
      type: github
      commit: 403ae4bf90c7d75c86b3584fd5e0a289abce5603
      ref: refs/tags/v1.30.1
      repoUrl: github.com/examplePath/exampleRepo
```

### Helm Chart in Helm Chart Repository

For helm charts stored in a [helm chart repository](https://helm.sh/docs/topics/chart_repository/) the following logical 
type is defined:

- helm.io/chart

The access section looks as follows:

|  | Value | Description |
| --- | --- | --- |
| type | helmChartRepository | |
| helmChartRepoUrl |  | URL to the helm chart repository |
| helmChartName |  | name of the helm chart | 
| helmChartVersion |  | helm chart version | 

An example looks as follows:

```yaml
resources:
  - name: example-name
    type: helm.io/chart
    access:
      type: helmChartRepository
      helmChartRepoUrl: repoURL
      helmChartName: example-helm-char-name
      helmChartVersion: 1.0.0
```

### S3

For objects stored in an [S3](https://aws.amazon.com/s3/) bucket, there are no predefined logical types so far.

The access section looks as follows:

|  | Value | Description |
| --- | --- | --- |
| type | s3 | |
| mediaType |  | [media type](https://www.iana.org/assignments/media-types/media-types.xhtml) of the object (optional) |
| bucketName |  | bucket name | 
| objectKey |  | object key | 

An example looks as follows:

```yaml
resources:
  - name: example-name
    type: yourLogicalType
    access:
      type: s3
      mediaType: application/pdf
      bucketName: bucket1
      objectKey: someKey
```

