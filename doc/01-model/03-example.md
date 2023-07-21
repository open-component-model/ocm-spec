
# Example for a complete Component Version

```yaml
# Example for a signed component descriptor containing three resources and one reference
meta:
  configuredSchemaVersion: v2
component:
  name: github.com/open-component-model/ocmechoserver  # name of this component
  version: 0.1.0-dev                                   # version of this component
  provider:                                            # provider of this component
    name: open-component-model
  repositoryContexts: # -> origin of this document
  - baseUrl: ghcr.io
    componentNameMapping: urlPath
    subPath: jensh007/ctf
    type: OCIRegistry
  componentReferences:  # -> components referenced by this component
  - componentName: github.com/mandelsoft/ocmhelminstaller # -> name of referenced component
    name: installer    # -> name of reference in this component descriptor
    version: 0.1.0-dev # -> version of referenced component
    digest:            # -> digest used for signing this referenced component
      hashAlgorithm: sha256
      normalisationAlgorithm: jsonNormalisation/v1
      value: d1871d98a6b9ec11b562895efccdcb8b8f87d8dcb81eabc40cad4d9b68f0ea36
  resources: # -> resources making this component
  - name: image         # -> name of this resource
    version: "1.0"      # -> version of this resource
    type: ociImage      # -> type of the resource (here indicating a container image)
    relation: external  # -> located in an external registry
    access:             # -> access information how to locate this resource
      imageReference: gcr.io/google_containers/echoserver:1.10
      type: ociArtifact
    digest:             # -> digest of this resource used for signing
      hashAlgorithm: sha256
      normalisationAlgorithm: ociArtifactDigest/v1
      value: cb5c1bddd1b5665e1867a7fa1b5fa843a47ee433bbb75d4293888b71def53229
  - name: chart         # -> name of this resource
    version: 0.1.0-dev  # -> version of this resource
    type: helmChart     # -> type of the resource (here indicating a helm chart)
    relation: local     # -> located in the local registry
    access:             # -> access information how to locate this resource
      imageReference: ghcr.io/jensh007/ctf/github.com/open-component-model/ocmechoserver/echoserver:0.1.0
      type: ociArtifact
    digest:             # -> digest of this resource used for signing
      hashAlgorithm: sha256
      normalisationAlgorithm: ociArtifactDigest/v1
      value: 385531bf40fc2b93e1693c0270250deb8da488a8f6f8dcaa79b0ab2bf1041c0b
  - name: package      # -> name of this resource
    version: 0.1.0-dev # -> version of this resource
    type: toiPackage   # -> type of the resource (here indicating a custom tyoe)
    relation: local    # -> located in the local registry
    access:            # -> access information how to locate this resource
      globalAccess:
        digest: sha256:57563cb451bb79eb1c4bf0e71c66fdad1daf44fe55e128f12eae5f7e5496a188
        mediaType: application/vnd.toi.ocm.software.package.v1+yaml
        ref: ghcr.io/jensh007/ctf/component-descriptors/github.com/open-component-model/ocmechoserver
        size: 615
        type: ociBlob
      localReference: sha256:57563cb451bb79eb1c4bf0e71c66fdad1daf44fe55e128f12eae5f7e5496a188
      mediaType: application/vnd.toi.ocm.software.package.v1+yaml
      type: localBlob
    labels:            # -> labels on this resource as key-value pairs
    - name: commit
      value: 9b2cf6ced322c7b938533caa22d5a5f48105b3ab
    digest:            # -> digest of this resource used for signing
      hashAlgorithm: sha256
      normalisationAlgorithm: genericBlobDigest/v1
      value: 57563cb451bb79eb1c4bf0e71c66fdad1daf44fe55e128f12eae5f7e5496a188
  sources:  # -> information about the origin (source code) of this component
  - name: echoserver_source # -> name of the source
    version: 0.1.0-dev      # -> version of this source
    type: git               # -> type of the source (here Git repository)
    access:                 # -> access information how to locate this resource
      commit: 9b2cf6ced322c7b938533caa22d5a5f48105b3ab
      ref: refs/heads/main
      repoUrl: github.com/open-component-model/ocm
      type: github
signatures: # -> signing information using cryptographic signatures
- name: mysig # -> name of this signature
  digest: # -> digest of this signature including used algorithm
    hashAlgorithm: sha256
    normalisationAlgorithm: jsonNormalisation/v1
    value: cf08abae08bb874597630bc0573d941b1becc92b4916cbe3bef9aa0e89aec3f6
  signature:  # -> signature including used algorithm
    algorithm: RSASSA-PKCS1-V1_5
    mediaType: application/vnd.ocm.signature.rsa
    value: 390157b7311538bc50e31d126b413b49e2ec85a6bc16a4fe6a27fbc9f9b6f89bc9ac48091beff3d091a9eb0a62a35e0eb2b6f5ab35c3cdde6cfad3437d660894ecc9a4e42cc4664ade28e74c478d69fe791d18b81fb31ee6c5633a9ea2543e868281dd6de6d29b68200ba135fd5718b3fc0ac1cd437910d06c9a88753e00b7e5b778bf52d668a5e20e0f857702c5c03abc42933af2af00b701722c50835bc5f9d85fd523654647e49dccdede1e17f20e4a6b30037d3d151e08c58c2aabe638028dbfddbd4a63e4efb07983631e1cb98902677e7e17b9e5192d4a6c178ec694eaa260f7a7845378019ce3368082c466a4ff54d823191f44db61b7aa75ab2705d6
```


