# Transport Format

We will define a transport format for components. 
As a subtask we first must define a transport format for different types of resources that can be referenced by 
components.

## Transport Format of OCI Artifacts

We describe a file system structure that represents one or more OCI artifacts.
A tar file of this file structure will be called the transport archive of the OCI artifacts.

> Clarify that the containing directory is not part of the tar file.

The file system structure is a directory containing:

- an `artifact-descriptor.json` file
- and a `blobs` directory.

The `blobs` directory contains the manifest, config and the layer files of all OCI artifacts under consideration
in one flat file list. In case of multi arch artifacts, the `blobs` directory can also contain index manifest files.
Every file has a filename according to its
[digest](https://github.com/opencontainers/image-spec/blob/main/descriptor.md#digests), 
where the algorithm separator character is replaced by a dot ("."). 

The `artifact-descriptor.json` contains a list of all manifests with their tags.

> Purpose of the `artifact-descriptor.json`: 1. list of entry points or 2. tag assignment?
> During import one wants to loop over all entry points. But one does not handle maifests twice if index manifest and 
> (normal) manifest both have tags.
> How to achieve the order of import (referenced components first)

#### Example of a transport archive containing two artifacts

```text
transport-archive
├── artifact-descriptor.json
└── blobs
    ├── sha256.111... (manifest.json of artifact 1)
    ├── sha256.222... (config.json   of artifact 1)
    ├── sha256.333... (layer         of artifact 1)
    ├── sha256.444... (layer         of artifact 1)
    ├── sha256.555... (manifest.json of artifact 2)
    ├── sha256.666... (config.json   of artifact 2)
    ├── sha256.777... (layer         of artifact 2)
    └── sha256.888... (layer         of artifact 2)
```

The manifest list in the `artifact-descriptor.json` contains the tags for the two manifests:

```json
{
  "manifests": [
    { "digest": "sha:111...", "tags": ["v1.25.0"] },
    { "digest": "sha:555...", "tags": ["v1.12.0"] }
  ]
}
```


## Transport Format for Other Resource Types

Whenever a new resource type is supported, a corresponding transport format must be defined.


## Transport Format of a Component

We describe a file system structure that represents one or more components.
A tar file of this file structure will be called the transport archive of the components.

In a first step, all references to external resources are converted to resources of type `localBlob`.
This means two things: firstly, the resource in the component descriptor must be adjusted, 
and secondly, a local blob must be added. We use the transport archive of the resource as local blob. 

We have already defined a representation of components as OCI artifacts. 
Therefore, we can use for one or more component the same transport format as for OCI artifacts.

Note that the transformation of external resources increases the number of layers. Hence, the manifest of the original 
component (in its OCI representation) and the manifest in the transport format are different.

```text
artifact-archive
├── artifact-descriptor.json
└── blobs
    ├── sha.123... (manifest.json)
    ├── sha.234... (config.json)
    ├── sha.345... (component descriptor)
    ├── sha.456... (local blob / transport archive of a previously external resource)
    └── sha.567... (local blob / transport archive of a previously external resource)
```

The component version appears in the archive-descriptor.json as a tag associated to the digest of the component 
descriptor:

```json
{
  "manifests": [
    { "digest": "sha:345...", "tags": ["COMPONENT_VERSION"] }
  ]
}
```
