# Local Blobs

The central task of a component repository is to provide information about versioned sets of resources.
Therefore, a component descriptor as technical representation of a component version describes such
a set of resources. This explicitly includes access information, a formal description to describe a technical
access path. For the component model those resources are just seen as simple typed blobs.
This enables to formally reference blobs in external environments, as long as the described method is
known to the consuming environment. The evaluation of an access specification always results in a simple blob
representing the content of the described resource. This way basically all required blobs can be stored in any
supported external blob store. 

When using the component repository to transport content from one repository the another one
(possibly behind a firewall without access to external blob repositories), the described content of a component
version must be transportable by value together with the component descriptor. Therefore the access information
stored along with the described resoures may change over time or from environment to environment. But all
variants must describe the same technical content.

Such a tranport can be done in several ways:
- directly from an OCM repository to another one: To support transport by value requires the availability of a
  blob state in the target environment.
- indirectly using an intermedite file based format: This format must be capable to store blobs that have to be
  transported side-by-side with the component descriptors. In this format the component descriptor must be capable
  to describe the access to those locally stored blobs.

To simplify and unify the handling of those two scenarios, and generally the handling of blobs in various
environments, a component repository must also include support for storing
blobs under the identity of the component descriptor. A repository implementation may forward this task
to a predefinied other blob store or handle this part of the API in its own way.

This enables:
- a simple usage of a component repository to store any content without the need of always requiring other 
  externals stores for (possibly specific types of) resources. (for example for storing sinmple configuration data 
  along with the component descriptor)
- providing a respository implementation for filesystem formats that can transparently be used by component tools.
- the usage of a minimal repository environment on the target side of a transport by just using a dedicated
  component repository.

Therefore, *Component Repositories* MUST provide the possibility to store technical artifacts together with the 
*Component Descriptors* in the *Component Repository* itself as so-called *local blobs*. Therefore a dedicated general
access type `localBlob` is used that MUST be implemented by all repository implementations. This also allows to pack all 
component versions with their technical artifacts in a *Component Repository* as a completely self-contained package, a 
typical requirement if you need to deliver your product into a fenced landscape. 

As a short example, assume some component needs additional configuration data stored in some YAML file. If 
in some landscape of your transport chain there is only an OCI registry available to store content, then you need to 
define a format how to store such a YAML file in the OCI registry. With *local blobs* you could just upload the file into
the *Component Repository*. 

## Functions for Local Blobs

### UploadLocalBlob

A *Component Repository* MUST implement a method for uploading *local blobs*
as specified in this chapter.

**Description**: Allows uploading binary data. The binary data belong to a particular *Component Descriptor*
and can be referenced by the component descriptor in its *resources* or *sources* section.
*Component Descriptors* are not allowed to reference local blobs of other *Component Descriptors* in their resources.

When uploading a local blob, it is not REQUIRED that the corresponding *Component Descriptor* already exists.
Usually local blobs are uploaded first because it is not allowed to upload a *Component Descriptor* if its local
blobs not already exist.

The optional parameter *mediaType* provides information about the internal structure of the provided blob.

With the optional parameter *annotations* you could provide additional information about the blob. This information
could be used by the *Component Repository* itself or later if the local blob is stored again in some external
location, e.g. an OCI registry.

*LocalAccessInfo* provides the information how to access the blob data with the method *GetLocalBlob* (see below).

With the return value *globalAccessInfo*, the *Component Repository* could optionally provide an external reference to
the resource, e.g. if the blob contains the data of an OCI image it could provide an external OCI image reference.

**Inputs**:

- String name: Name of the *Component Descriptor*
- String version: Version of the *Component Descriptor*
- BinaryStream data: Binary stream containing the local blob data.
- String mediaType: media-type of the uploaded data (optional)
- String referenceName (optional): resource typpe specific information that can be used by a target
  repository to determine an identity for te potential global access.
- String globalAccess (optional): A JSON string describing a global access specification for the resource

**Outputs**:

- String localAccessInfo: The information how to access the source or resource as a *local blob*.
- String globalAccessInfo (optional): The information how to access the source or resource via a global reference. This must be
  the JSON representatio of a global access specification.

**Errors**:

- invalidArgument: If one of the input parameters is empty or not valid
- repositoryError: If some error occurred in the *Component Repository*

**Example**:
Assume you want to upload an OCI image to your *Component Repository* with the *UploadLocalBlob* function with media type
*application/vnd.oci.image.manifest.v1+tar+gzip*. The reference information can be set to the originial image name *gardener/specialimage*
to give a target repository a hint for determining the identity of a potential global access:

```
"sha256:b5733194756a0a4a99a4b71c4328f1ccf01f866b5c3efcb4a025f02201ccf623"
```

The request to store the local blob the looks as follows:

```
  mediaType: application/vnd.oci.image.manifest.v1+tar+gzip
  referenceName: gardener/specialimage
  localReference: "sha256:b5733194756a0a4a99a4b71c4328f1ccf01f866b5c3efcb4a025f02201ccf623"
... 
```

The *Component Repository* (in case it supports direct OCI access) could also provide some derived *globalAccessInfo* additionally containing the location in an OCI registry:

```
imageReference: <repository prefix>/gardener/specialimage@sha:...
type: ociRegistry
```

An entry to this resource with this information in the *Component Descriptor* then looks as the following:

```
...
  resources:
  - name: example-image
    type: oci-image
    access:
      type: localBlob
      mediaType: application/vnd.oci.image.manifest.v1+json
      referenceName: gardener/specialimage
      localReference: "sha256:b5733194756a0a4a99a4b71c4328f1ccf01f866b5c3efcb4a025f02201ccf623"
      globalAccess: 
        imageReference: <repository prefix>/gardener/specialimage@sha:...
        type: ociRegistry
... 
```

Optionally the repository could even omit the storage as local blob, and just provide a global type specific access specification
(depending of the given media type), which would result in the following resource specification:

```
...
  resources:
  - name: example-image
    type: oci-image
    access:
      type: ociRegistry
      imageReference: <repository prefix>/gardener/specialimage@sha:...
... 
```

The repository implementation is free to decide on the storage of local blobs based on the input information, it just has to return the
approriate access information. This way it could also decide to generally store blobs in a preconfigured blob store and
always return a global access (accessible form the environment the component repoitory lives in) specification for all kinds of blobs.

### GetLocalBlob

A *Component Repository* MUST implement a method for fetching *local blobs* as specified in this chapter.

**Description**: Fetches the binary data of a local blob. *localAccessInfo* is the *Component Repository* specific
access information you got when you uploaded the local blob.

**Inputs**:

- String name: Name of the *Component Descriptor*
- String version: Version of the *Component Descriptor*
- String localAccessInfo: Access information of the local blob

**Outputs**:

- BinaryStream data: Binary stream containing the local blob data.

**Errors**:

- doesNotExist: If the local blob does not exist
- invalidArgument: If one of the input parameters is empty or invalid
- repositoryError: If some error occurred in the *Component Repository*

### ListLocalBlobs

A *Component Repository* MAY implement a method for listing *local blobs* as specified in this chapter.

**Description**: Provides an iterator over all triples *componentName/componentVersion/localAccessInfo* of all
uploaded blobs. 

**Inputs**:

**Outputs**:

- Iterator over string triple: Triples of *componentName/componentVersion/localAccessInfo*

**Errors**:

- repositoryError: If some error occurred in the *Component Repository*

### DeleteLocalBlob

A *Component Repository* SHOULD implement a method for deleting *local blobs* as specified in this chapter.

**Description**: Deletes a local blob. *localAccessInfo* is the *Component Repository* specific
information you got when you uploaded the local blob.

An error occurs if there is still an existing reference to the local blob.

**Inputs**:

- String name: Name of the *Component Descriptor*
- String version: Version of the *Component Descriptor*
- String localAccessInfo: Access information of the local blob

**Outputs**:

**Errors**:

- doesNotExist: If the local blob does not exist
- existingReference: If the local blob is still referenced
- invalidArgument: If one of the input parameters is empty
- repositoryError: If some error occurred in the *Component Repository*
