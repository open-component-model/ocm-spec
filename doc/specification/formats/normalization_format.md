# Base Format for Normalization
The OCM component model allows for signing component descriptors. Signing is done using a text based format. Usually component descriptors are stored as yaml files. The signing ensures that a component descriptor has not been tampered with since ist was signed. As yaml is a text based format the signing should be robust against various minor changes not effecting the integrity:

* formatting issue (e.g. different indent depth)
* comments
* HTML escaping
* ...

Furthermore the OCM supports transportation of artifacts between repositories. Scenarios should be supported where artifacts are fetched from a different repository compared to the one it was signed from. This implies changing URLs in the component descriptor.

These two requirements result in the definition of a normalization format and procedure.

As a first step the component descriptor is converted to JSON and all line breaks are removed. All dictionaries are converted to a list where each element is a single-entry dictionary containing the key value pair of the original entry. The list is ordered in lexikographic order of the keys. In this way a sorting order can be guaranteed.

## Labels
Labels are removed before signing but can be marked with a special boolean property `signing` not to be removed and thus be part of the signature.

Example:

```
labels:
- name: label1
  value: foo
- name: label2
  value: bar
  signing: true
```
label1 will be excluded from the signature, label2 will be included.

## Excluded elements

The following elements are removed

* meta
* component/repositoryContext
* resources/access
* resources/srcRef
* resources/labels (unless marked for signing)
* sources/access
* sources/labels (unless marked for signing)
* references/labels (unless marked for signing)
* signatures


## Example:

```
  component:
    componentReferences: []
    name: github.com/vasu1124/introspect
    provider: internal
    version: 1.0.0
    repositoryContexts: []
    sources: []
    resources: []
  meta:
    schemaVersion: v2```
```

will be converted for signing to:

```
 [{"component":[{"componentReferences":[]},{"name":"github.com/vasu1124/introspect"},{"provider":[{"name":"internal"}]},{"resources":[]},{"sources":[]},{"version":"1.0.0"}]}]
```

or for better readability formatted (but not the format which is signed):

```
[
    {
        "component": [
            {
                "componentReferences": []
            },
            {
                "name": "github.com/vasu1124/introspect"
            },
            {
                "provider": [
                    {
                        "name": "internal"
                    }
                ]
            },
            {
                "resources": []
            },
            {
                "sources": []
            },
            {
                "version": "1.0.0"
            }
        ]
    }
]
```

Here is a more complete example:

```
  component:
    componentReferences: []
    name: github.com/vasu1124/introspect
    provider: internal
    repositoryContexts:
    - baseUrl: ghcr.io/vasu1124/ocm
      componentNameMapping: urlPath
      type: ociRegistry
    resources:
    - access:
        localReference: sha256:7f0168496f273c1e2095703a050128114d339c580b0906cd124a93b66ae471e2
        mediaType: application/vnd.docker.distribution.manifest.v2+tar+gzip
        referenceName: vasu1124/introspect:1.0.0
        type: localBlob
      digest:
        hashAlgorithm: sha256
        normalisationAlgorithm: ociArtifactDigest/v1
        value: 6a1c7637a528ab5957ab60edf73b5298a0a03de02a96be0313ee89b22544840c
      name: introspect-image
      labels:
        - name: label1
          value: foo
        - name: label2
          value: bar
          signing: true
      relation: local
      srcRefs: []
      type: ociImage
      version: 1.0.0
    - access:
        localReference: sha256:d1187ac17793b2f5fa26175c21cabb6ce388871ae989e16ff9a38bd6b32507bf
        mediaType: ""
        type: localBlob
      digest:
        hashAlgorithm: sha256
        normalisationAlgorithm: genericBlobDigest/v1
        value: d1187ac17793b2f5fa26175c21cabb6ce388871ae989e16ff9a38bd6b32507bf
      name: introspect-blueprint
      relation: local
      type: landscaper.gardener.cloud/blueprint
      version: 1.0.0
    - access:
        localReference: sha256:4186663939459149a21c0bb1cd7b8ff86e0021b29ca45069446d046f808e6bfe
        mediaType: application/vnd.oci.image.manifest.v1+tar+gzip
        referenceName: vasu1124/helm/introspect-helm:0.1.0
        type: localBlob
      digest:
        hashAlgorithm: sha256
        normalisationAlgorithm: ociArtifactDigest/v1
        value: 6229be2be7e328f74ba595d93b814b590b1aa262a1b85e49cc1492795a9e564c
      name: introspect-helm
      relation: external
      type: helm
      version: 0.1.0
    sources:
    - access:
        repository: github.com/vasu1124/introspect
        type: git
      name: introspect
      type: git
      version: 1.0.0
    version: 1.0.0
  meta:
    schemaVersion: v2
```
will be converted for signing to:

```
[{"component":[{"componentReferences":[]},{"name":"github.com/vasu1124/introspect"},{"provider":[{"name":"internal"}]},{"resources":[[{"digest":[{"hashAlgorithm":"sha256"},{"normalisationAlgorithm":"ociArtifactDigest/v1"},{"value":"6a1c7637a528ab5957ab60edf73b5298a0a03de02a96be0313ee89b22544840c"}]},{"labels":[[{"name":"label2"},{"signing":true},{"value":"bar"}]]},{"name":"introspect-image"},{"relation":"local"},{"type":"ociImage"},{"version":"1.0.0"}],[{"digest":[{"hashAlgorithm":"sha256"},{"normalisationAlgorithm":"genericBlobDigest/v1"},{"value":"d1187ac17793b2f5fa26175c21cabb6ce388871ae989e16ff9a38bd6b32507bf"}]},{"name":"introspect-blueprint"},{"relation":"local"},{"type":"landscaper.gardener.cloud/blueprint"},{"version":"1.0.0"}],[{"digest":[{"hashAlgorithm":"sha256"},{"normalisationAlgorithm":"ociArtifactDigest/v1"},{"value":"6229be2be7e328f74ba595d93b814b590b1aa262a1b85e49cc1492795a9e564c"}]},{"name":"introspect-helm"},{"relation":"external"},{"type":"helm"},{"version":"0.1.0"}]]},{"sources":[[{"name":"introspect"},{"type":"git"},{"version":"1.0.0"}]]},{"version":"1.0.0"}]}]
```

or formatted for better readability (but not the format which is signed):

```
[
    {
        "component": [
            {
                "componentReferences": []
            },
            {
                "name": "github.com/vasu1124/introspect"
            },
            {
                "provider": [
                    {
                        "name": "internal"
                    }
                ]
            },
            {
                "resources": [
                    [
                        {
                            "digest": [
                                {
                                    "hashAlgorithm": "sha256"
                                },
                                {
                                    "normalisationAlgorithm": "ociArtifactDigest/v1"
                                },
                                {
                                    "value": "6a1c7637a528ab5957ab60edf73b5298a0a03de02a96be0313ee89b22544840c"
                                }
                            ]
                        },
                        {
                            "labels": [
                                [
                                    {
                                        "name": "label2"
                                    },
                                    {
                                        "signing": true
                                    },
                                    {
                                        "value": "bar"
                                    }
                                ]
                            ]
                        },
                        {
                            "name": "introspect-image"
                        },
                        {
                            "relation": "local"
                        },
                        {
                            "type": "ociImage"
                        },
                        {
                            "version": "1.0.0"
                        }
                    ],
                    [
                        {
                            "digest": [
                                {
                                    "hashAlgorithm": "sha256"
                                },
                                {
                                    "normalisationAlgorithm": "genericBlobDigest/v1"
                                },
                                {
                                    "value": "d1187ac17793b2f5fa26175c21cabb6ce388871ae989e16ff9a38bd6b32507bf"
                                }
                            ]
                        },
                        {
                            "name": "introspect-blueprint"
                        },
                        {
                            "relation": "local"
                        },
                        {
                            "type": "landscaper.gardener.cloud/blueprint"
                        },
                        {
                            "version": "1.0.0"
                        }
                    ],
                    [
                        {
                            "digest": [
                                {
                                    "hashAlgorithm": "sha256"
                                },
                                {
                                    "normalisationAlgorithm": "ociArtifactDigest/v1"
                                },
                                {
                                    "value": "6229be2be7e328f74ba595d93b814b590b1aa262a1b85e49cc1492795a9e564c"
                                }
                            ]
                        },
                        {
                            "name": "introspect-helm"
                        },
                        {
                            "relation": "external"
                        },
                        {
                            "type": "helm"
                        },
                        {
                            "version": "0.1.0"
                        }
                    ]
                ]
            },
            {
                "sources": [
                    [
                        {
                            "name": "introspect"
                        },
                        {
                            "type": "git"
                        },
                        {
                            "version": "1.0.0"
                        }
                    ]
                ]
            },
            {
                "version": "1.0.0"
            }
        ]
    }
```
