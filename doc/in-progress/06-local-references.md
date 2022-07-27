# Local Blob Reference Definitions

## General Format

In a *Component Repository*, local blobs can be stored together with a *Component Descriptor*. Local blobs could store
different data like OCI images, helm charts, configuration data etc. 

The general format for references to local blobs is the same as for external accessible references:

|  | Description |
| --- | --- |
| type | Logical type of the referenced object, e.g. *helm.io/chart* for for a helm chart|
| access | object | Access information to fetch the data |

The access object has the following format:

|  | Value | Description |
| --- | --- | --- |
| string | localBlob| |
| mediaType | | media type of the stored data |
| annotations | | additional information about the stored data |
| localAccess | | information how to access the local blob |
| globalAccess | | information how to access the local blob via a external accessible reference |


## OCI Images as Local Blobs

```
...
  resources:
  - name: example-image
    type: oci-image
    access:
      type: localBlob
      mediaType: application/vnd.oci.image.manifest.v1+json
      annotations:
        name: test/monitoring
      localAccess: "digest: sha256:b5733194756a0a4a99a4b71c4328f1ccf01f866b5c3efcb4a025f02201ccf623"
      globalAccess: 
        imageReference: somePrefix/test/monitoring@sha:...
        type: ociRegistry
... 
```

```yaml
resources:
  - name: example-name
    relation: local
    type: helm.io/chart
    version: v0.1.0
    access:
      digest: <identifier/digest of the local blob>
      type: localBlob
```


