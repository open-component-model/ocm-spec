# OCI Registries

The specification defines how OCM repositories, component descriptors, and artifacts are stored and resolved inside OCI registries. 
It standardizes the repository format, how component names map to OCI paths, and how versions are represented using either OCI manifests or OCI indexes. 
It prescribes strict rules for descriptor selection, LocalBlob handling, digest validation, and version-to-tag mapping. 
The specification also introduces a Component Index artifact used for referrer-based version discovery and defines fallback mechanisms for registries lacking referrer support.

## Table of Contents

<!-- TOC -->
* [OCI Registries](#oci-registries)
  * [Table of Contents](#table-of-contents)
  * [1. Scope](#1-scope)
  * [2. Conformance Terminology](#2-conformance-terminology)
  * [3. OCI Registry Requirements](#3-oci-registry-requirements)
  * [4. Repository Specification Format](#4-repository-specification-format)
    * [4.1 Synopsis](#41-synopsis)
    * [4.2 Specification Version](#42-specification-version)
    * [4.3 Version `v1` Fields](#43-version-v1-fields)
      * [`baseUrl` (string, REQUIRED)](#baseurl-string-required)
      * [`subPath` (string, OPTIONAL)](#subpath-string-optional)
      * [`componentNameMapping` (string, OPTIONAL)](#componentnamemapping-string-optional)
  * [5. OCI Repository Reference Grammar](#5-oci-repository-reference-grammar)
    * [5.1 Grammar](#51-grammar)
  * [6. Component Repository Mapping](#6-component-repository-mapping)
  * [**6.1 Example](#61-example)
    * [6.1.1 Input](#611-input)
    * [6.1.2 Resolved OCI Reference](#612-resolved-oci-reference)
  * [7. Component Version Representations](#7-component-version-representations)
  * [8. Manifest-Based Representation](#8-manifest-based-representation)
    * [8.1 Media Type](#81-media-type)
    * [8.2 Configuration Requirement](#82-configuration-requirement)
    * [8.3 LocalBlob Mapping (Manifest-Based)](#83-localblob-mapping-manifest-based)
    * [8.4 Example](#84-example)
  * [9. Alternative Representation Formats](#9-alternative-representation-formats)
  * [10. Index-Based Representation](#10-index-based-representation)
    * [10.1 Descriptor Storage](#101-descriptor-storage)
    * [10.2 Allowed Additional Manifests](#102-allowed-additional-manifests)
    * [10.3 Example](#103-example)
  * [11. Artifact-Level OCM OCI Annotations (Extended)](#11-artifact-level-ocm-oci-annotations-extended)
  * [12. Descriptor Selection Logic](#12-descriptor-selection-logic)
  * [**13. Component Index and Referrer Semantics**](#13-component-index-and-referrer-semantics)
    * [13.1 Purpose](#131-purpose)
    * [13.2 Media Type and Manifest Requirements](#132-media-type-and-manifest-requirements)
    * [13.3 Descriptor Requirements](#133-descriptor-requirements)
    * [13.4 Storage Rules](#134-storage-rules)
    * [13.5 Subject Reference Requirement](#135-subject-reference-requirement)
    * [13.6 Discovery Behavior](#136-discovery-behavior)
      * [13.6.1 Registries Supporting the Referrers API](#1361-registries-supporting-the-referrers-api)
      * [13.6.2 Registries Not Supporting the Referrers API](#1362-registries-not-supporting-the-referrers-api)
      * [13.6.3 Hybrid Behavior](#1363-hybrid-behavior)
    * [13.7 Component Version Lifecycle](#137-component-version-lifecycle)
      * [13.7.1 On Push](#1371-on-push)
      * [13.7.2 On Delete](#1372-on-delete)
      * [13.7.3 On Enumerating Versions](#1373-on-enumerating-versions)
  * [13.8 Referrer Tracking Policy](#138-referrer-tracking-policy)
    * [13.8.1 `ReferrerTrackingPolicyNone`](#1381-referrertrackingpolicynone)
    * [13.8.2 `ReferrerTrackingPolicyByIndexAndSubject`](#1382-referrertrackingpolicybyindexandsubject)
  * [13.9 Index Creation Rules (`CreateIfNotExists`)](#139-index-creation-rules-createifnotexists)
  * [14. Descriptor Encoding Formats](#14-descriptor-encoding-formats)
  * [15. LocalBlob Resolution and OCI Layout Handling](#15-localblob-resolution-and-oci-layout-handling)
    * [15.1 General Rules](#151-general-rules)
    * [15.2 Ingestion of LocalBlob Content](#152-ingestion-of-localblob-content)
    * [15.3 Descriptor Mapping](#153-descriptor-mapping)
    * [15.4 Resolution of LocalBlob Descriptors](#154-resolution-of-localblob-descriptors)
    * [15.5 Retrieval of LocalBlob Content](#155-retrieval-of-localblob-content)
      * [15.5.1 Layer-Based LocalBlob](#1551-layer-based-localblob)
      * [15.5.2 Manifest- or Index-Based LocalBlob (OCI Layout Reconstruction)](#1552-manifest--or-index-based-localblob-oci-layout-reconstruction)
    * [15.6 Interaction with Global Access](#156-interaction-with-global-access)
    * [15.7 Validation Requirements](#157-validation-requirements)
  * [16. OCIImage Digest Processing](#16-ociimage-digest-processing)
  * [17. Version Mapping Rules](#17-version-mapping-rules)
    * [17.1 BNF Grammar Definitions](#171-bnf-grammar-definitions)
    * [17.2 OCM Version → OCI Tag Transformation](#172-ocm-version--oci-tag-transformation)
    * [17.3 OCI Tag → OCM Version Transformation](#173-oci-tag--ocm-version-transformation)
    * [17.4 Manifest Annotation `software.ocm.componentversion`](#174-manifest-annotation-softwareocmcomponentversion)
  * [18. Blob Repository Mapping](#18-blob-repository-mapping)
  * [19. Compatibility Requirements](#19-compatibility-requirements)
<!-- TOC -->

## 1. Scope

This document defines the normative mapping of OCM component repositories, component descriptors, and associated artifacts onto OCI registries conforming to the [OCI Distribution Specification](https://github.com/opencontainers/distribution-spec/blob/main/spec.md).
It specifies:

* The repository specification format
* Repository location resolution
* Component descriptor representation
* Manifest-based and index-based storage models
* LocalBlob and OCIImage resource resolution
* Descriptor selection and lookup
* Version and digest mapping rules
* Artifact staging behavior
* Compatibility constraints

This document is authoritative for all interactions between OCM and OCI registry systems.

## 2. Conformance Terminology

The key words **MUST**, **MUST NOT**, **REQUIRED**, **SHALL**, **SHALL NOT**, **SHOULD**, **SHOULD NOT**, **MAY**, and **OPTIONAL** are to be interpreted as described in RFC 2119 and RFC 8174.

## 3. OCI Registry Requirements

An OCI registry used with OCM:

1. **MUST** conform to the OCI Distribution Specification.
2. **MUST** support hierarchical (deep) repository paths.
3. **MAY** support HTTP if explicitly enabled via a scheme in the base URL.
4. **MAY** host multiple OCM repositories concurrently.

Registries that do not support nested repository paths **MUST NOT** be used with this specification.

## 4. Repository Specification Format

The following repository specification format **MUST** be used to describe an OCM repository backed by an OCI registry.

### 4.1 Synopsis

```
type: <TYPE>[/VERSION]
[ATTRIBUTES]
```

Where:

```
<type-name> ::= <canonical-type> | <short-type>

<canonical-type> ::= "OCIRegistry" | "OCIRepository" | "ociRegistry"
<short-type>     ::= "OCI" | "oci"
```

### 4.2 Specification Version

Only version **`v1`** is currently defined.
Clients **MUST** reject unknown versions.

### 4.3 Version `v1` Fields

#### `baseUrl` (string, REQUIRED)

Defines the registry host.
The following constraints apply:

* If a scheme is present (`http://`, `https://`, `oci://`), clients **MUST** honor it.
* If no scheme is present, clients **MUST** assume HTTPS.
* The host **MUST** be interpreted as the OCI registry root.
* A fully qualified URL **MAY** be used to force HTTP usage.
* The path component of a URL **SHOULD** be interpreted as the subPath.

Examples:

```
eu.gcr.io
https://index.docker.io
http://eu.ghcr.io
oci://eu.gcr.io/my-project # my-project SHOULD be interpreted as subPath
```

#### `subPath` (string, OPTIONAL)

Specifies a repository prefix within the registry.
All component repositories **MUST** resolve under:

```
<baseUrl>/<subPath>
```

If omitted, `<subPath>` is empty.

#### `componentNameMapping` (string, OPTIONAL)

Defines the mapping of component identifiers to OCI repository names.

Supported values:

* `urlPath` (default, REQUIRED for forward compatibility)
* `sha256-digest` (deprecated)

Clients **SHOULD NOT** use deprecated mappings when writing.
Clients **MAY** ignore unknown values.

## 5. OCI Repository Reference Grammar

An OCM repository corresponds to a single OCI repository reference.

```
[scheme://]<host>[:<port>][/<repository-path>]
```

### 5.1 Grammar

```
<oci-repository-ref> ::= <scheme-opt> <host> <port-opt> <repo-path-opt>

<scheme-opt> ::= ε | "https://" | "http://" | "oci://"
<host> ::= <dns-label> { "." <dns-label> }
<dns-label> ::= <alphanum> { <alphanum | "-" > }
<port-opt> ::= ε | ":" <port>
<port> ::= <digit>+
<repo-path-opt> ::= ε | "/" <repo-path>
<repo-path> ::= <path-segment> { "/" <path-segment> }
<path-segment> ::= <alphanum> { <alphanum | "-" | "_" | "." }
```

Registries **MUST** accept repository paths formed according to this grammar.


## 6. Component Repository Mapping

A component identifier:

```
<component-id> ::= <id-segment> { "/" <id-segment> }
<id-segment> ::= <alphanum> { <alphanum | "-" | "_" | "." > }
```

**MUST** be mapped to the following repository structure:

```
<base-repository>/component-descriptors/<component-id>
```

The `component-descriptors` sub-path **MUST** be used to store identifiable component descriptors.
This sub-path **MAY** change in future versions of this API based on configuration.

The `componentNameMapping` field determines the transformation of `<component-id>`.

All component versions for the component appear under this repository.

## **6.1 Example

This section illustrates the application of the normative repository-mapping rules defined in Sections 5 and 6.

### 6.1.1 Input

| Field             | Value                            |
|-------------------|----------------------------------|
| Component Name    | `github.com/acme.org/helloworld` |
| Component Version | `1.0.0`                          |
| Registry Base URL | `ghcr.io/open-component-model/test`   |

The effective OCI repository MUST be derived as:

```
<registry>/<subpath>/component-descriptors/<component-name>
```

Applied to this example:

```
ghcr.io/open-component-model/test/component-descriptors/github.com/acme.org/helloworld
```

### 6.1.2 Resolved OCI Reference

The component version `1.0.0` MUST be mapped to an OCI tag of equal value.
The resulting fully qualified OCI reference becomes:

```
oci://ghcr.io/open-component-model/test/component-descriptors/github.com/acme.org/helloworld:1.0.0
```

## 7. Component Version Representations

A component version **MUST** be represented using one of:

1. **Manifest-Based Representation** (OCI Image Manifest)
2. **Index-Based Representation** (OCI Image Index)

Both representations **MUST** be supported by all readers.
Writers **MAY** choose either.


## 8. Manifest-Based Representation

### 8.1 Media Type

A component version stored as a manifest **MUST** use:

```
application/vnd.oci.image.manifest.v1+json
```

### 8.2 Configuration Requirement

The manifest **MUST** include a config whose media type is:

```
application/vnd.ocm.software.component.config.v1+json
```

The config JSON object **MUST** contain:

```
componentDescriptorLayer: <OCI descriptor>
```

This descriptor **MUST** reference the descriptor layer containing the component descriptor.
This descriptor **MAY** be used to lookup the component descriptor layer if the descriptor layer is not locatable at index 0 of the top level manifest
Any manifest lacking this requirement **MUST** be treated as invalid.

### 8.3 LocalBlob Mapping (Manifest-Based)

Each `localBlob` resource in the descriptor:

* **MUST** correspond to one OCI manifest layer.
* The layer digest **MUST** equal the resource’s `localReference`.
* The layer media type **MUST** equal the resource’s declared `mediaType`.
* If the resource specifies a digest, the layer **MUST** match that digest.
* A `globalAccess` entry **MAY** appear and **MAY** refer to any canonical OCI layer reference.

This mapping is deterministic and normative.

### 8.4 Example

The following manifest shows a valid OCI Artifact Manifest containing the OCM Component Descriptor for `github.com/acme.org/helloworld` in version `1.0.0`.

```json
{
  "schemaVersion": 2,
  "mediaType": "application/vnd.oci.image.manifest.v1+json",
  "artifactType": "application/vnd.ocm.software.component-descriptor.v2",
  "config": {
    "mediaType": "application/vnd.ocm.software.component.config.v1+json",
    "digest": "sha256:54f3c7c68e00ecd13141dcdc560c42ce1ad2ab59b8d098b9c60b4e0a7b774d9c",
    "size": 197
  },
  "layers": [
    {
      "mediaType": "application/vnd.ocm.software.component-descriptor.v2+json",
      "digest": "sha256:a259e8e0f4e82e3564277911b4437cf1f123be37e329415c68ba69b6cc184c4b",
      "size": 1310
    },
    {
      "mediaType": "text/plain",
      "digest": "sha256:c3ab8ff13720e8ad9047dd39466b3c8974e592c2fa383d4a3960714caef0c4f2",
      "size": 6,
      "annotations": {
        "software.ocm.artifact": "[{\"identity\":{\"name\":\"blob\",\"version\":\"1.0.0\"},\"kind\":\"resource\"}]"
      }
    }
  ],
  "annotations": {
    "org.opencontainers.image.authors": "Builtin OCI Repository Plugin",
    "org.opencontainers.image.description": "This is an OCM OCI Artifact Manifest that contains the component descriptor for the component github.com/acme.org/helloworld.\nIt is used to store the component descriptor in an OCI registry and can be referrenced by the official OCM Binding Library.",
    "org.opencontainers.image.documentation": "https://ocm.software",
    "org.opencontainers.image.source": "https://github.com/open-component-model/open-component-model",
    "org.opencontainers.image.title": "OCM Component Descriptor OCI Artifact Manifest for github.com/acme.org/helloworld in version 1.0.0",
    "org.opencontainers.image.url": "https://ocm.software",
    "org.opencontainers.image.version": "1.0.0",
    "software.ocm.componentversion": "component-descriptors/github.com/acme.org/helloworld:1.0.0",
    "software.ocm.creator": "Builtin OCI Repository Plugin"
  }
}
```

## 9. Alternative Representation Formats

A component version **MAY** be stored using alternative OCI artifact encodings, provided that all representations conform to the digest-based identity rules and remain fully resolvable through the descriptor selection logic in [Section 12](#12-descriptor-selection-logic).
Alternative formats exist to support registry compatibility, artifact packaging flexibility, and efficient transport. 
All formats in this section **MUST** be treated as semantically equivalent ways of storing a component version. 
Implementations **MUST** support reading all formats. 
Implementations **MAY** restrict writing to a subset.

## 10. Index-Based Representation

A component version **MAY** be represented as an [OCI Image Index](https://github.com/opencontainers/image-spec/blob/main/image-index.md):

```
application/vnd.oci.image.index.v1+json
```

### 10.1 Descriptor Storage

If represented through an OCI Image Index, this index **MUST** contain:

1. A config referencing the component descriptor layer
2. **Exactly one** manifest annotated as the descriptor manifest
3. Any number of additional referenced manifests

### 10.2 Allowed Additional Manifests

Additional referenced manifests representing artifacts **MUST** use:

* `application/vnd.oci.image.manifest.v1+json`
* `application/vnd.oci.image.index.v1+json`

These represent OCI-native artifacts for local artifact entries.

Additional referenced manifests are allowed but **MAY** be ignored.

### 10.3 Example

The following OCI Image Index illustrates a valid index-based representation of the component version
`github.com/acme.org/helloworld:1.0.0`.

This index:

* Uses media type `application/vnd.oci.image.index.v1+json`.
* Contains two referenced manifests:
  * The **descriptor manifest**, containing the component descriptor (`software.ocm.descriptor=true`).
  * An **additional artifact manifest**, representing an OCIImage resource.
* Includes annotations required for OCM component version metadata.

```json
{
  "schemaVersion": 2,
  "mediaType": "application/vnd.oci.image.index.v1+json",
  "manifests": [
    {
      "mediaType": "application/vnd.oci.image.manifest.v1+json",
      "digest": "sha256:653410c2b330f9f958c2283e8727e547b46e40f3cb8a717b3476a6791d9764a9",
      "size": 1660,
      "annotations": {
        "software.ocm.descriptor": "true",
        "org.opencontainers.image.title": "OCM Component Descriptor OCI Artifact Manifest for github.com/acme.org/helloworld in version 1.0.0",
        "org.opencontainers.image.version": "1.0.0",
        "software.ocm.componentversion": "component-descriptors/github.com/acme.org/helloworld:1.0.0",
        "software.ocm.creator": "Builtin OCI Repository Plugin"
      },
      "artifactType": "application/vnd.ocm.software.component-descriptor.v2"
    },
    {
      "mediaType": "application/vnd.oci.image.manifest.v1+json",
      "digest": "sha256:c2a2aadf9b8acac6e5ff3cd7af42d8d32f4e940f8f69a487d8c8c19d4e109219",
      "size": 480,
      "annotations": {
        "io.containerd.image.name": "docker.io/library/hello-world:v1",
        "software.ocm.artifact": "[{\"identity\":{\"name\":\"image\",\"version\":\"1.0.0\"},\"kind\":\"resource\"}]"
      },
      "platform": {
        "architecture": "amd64",
        "os": "linux"
      }
    }
  ],
  "annotations": {
    "org.opencontainers.image.title": "OCM Component Descriptor OCI Artifact Manifest Index for github.com/acme.org/helloworld in version 1.0.0",
    "org.opencontainers.image.version": "1.0.0",
    "software.ocm.componentversion": "component-descriptors/github.com/acme.org/helloworld:1.0.0",
    "software.ocm.creator": "Builtin OCI Repository Plugin"
  }
}
```

This example demonstrates all required structural conventions for an index-based representation:

* Exactly one descriptor manifest annotated with `software.ocm.descriptor="true"`.
* Optional additional manifests for resources or sources.
* Correct OCM component version annotations at the index level.

## 11. Artifact-Level OCM OCI Annotations (Extended)

OCI artifacts **MAY** include an annotation pointing back to its origin artifact representation in
the component descriptor:

```
software.ocm.artifact: [{ identity: {...}, kind: "resource|source" }]
```

These annotations:

* Distinguish resources from sources
* Identify resources located within the component descriptor and serve as back-reference.

OCI resolution **MUST NOT** depend on these annotations.

Resolution **MUST** be driven by `localReference`.

## 12. Descriptor Selection Logic

When resolving a version reference (OCI tag):

1. The tag **MUST** be resolved to an OCI artifact.
2. If the artifact is a manifest:
    * It **MUST** be treated as the component descriptor.
3. If the artifact is an index:
    * All manifests with annotation `software.ocm.descriptor="true"` **MUST** be enumerated.
    * If **exactly one** exists: it **MUST** be selected.
    * If **more than one** exists: resolution **MUST** fail.
    * If **none** exist:
        * The **first** manifest in the index (index 0) **MUST** be selected.
        * This ensures backward compatibility.

## **13. Component Index and Referrer Semantics**

A **Component Index** is an optional canonical, immutable OCI artifact that functions as the stable “subject root” for all component versions published in a repository. 
It provides a registry-native discovery mechanism using the OCI Referrers API and ensures consistent version enumeration across registries with differing levels of referrer support.
It allows efficient versioning queries without having to use the OCI tag API.

### 13.1 Purpose

The Component Index serves three normative purposes:

1. **Stable Subject Reference**
   All component versions **MUST** reference the Component Index as their OCI `subject`.
   This enables registry-native enumeration of all component versions via a single referrers query.

2. **Immutable Discovery Anchor**
   The Component Index **MUST** have a stable byte representation, digest, size, and descriptor.
   It **MUST NOT** change across component versions or OCM releases.

3. **Compatibility Layer**
   When the registry supports the OCI Referrers API, the index becomes the authoritative discovery mechanism.
   When unsupported, fallback mechanisms **MAY** be used without altering component versions.

### 13.2 Media Type and Manifest Requirements

The Component Index **MUST** use the media type:

```
application/vnd.ocm.software.component-index.v1+json
```

The artifact **MUST** be encoded as an OCI Image Manifest (`SchemaVersion: 2`) with:

* `ArtifactType` set to the Component Index media type
* A single empty config (`DescriptorEmptyJSON`)
* At least one zero-byte layer referenced by descriptor
* Annotations describing its purpose
* A canonical JSON encoding that produces a deterministic digest and size

Clients **MUST** treat the manifest as opaque and immutable.

### 13.3 Descriptor Requirements

The descriptor for the Component Index:

* **MUST** include the exact stable digest and size of the canonical JSON representation
* **MUST NOT** be regenerated or altered after publication

Implementations **MUST** validate descriptor correctness when creating or loading a Component Index.

### 13.4 Storage Rules

When preparing a repository:

1. The Component Index manifest layer **MUST** be present; if not, it **MUST** be uploaded.
2. The Component Index manifest **MUST** be present; if not, it **MUST** be uploaded using its canonical descriptor.
3. Clients **MUST NOT** rewrite or mutate an existing Component Index, but only reference it via its `subject`

These requirements apply uniformly across registries, irrespective of tag semantics.

### 13.5 Subject Reference Requirement

Every top-level Component Version artifact (manifest-based or index-based):

* **SHOULD** set the Component Index descriptor as its OCI `subject`.

If a registry rejects subject references due to limited API support:

* The component version **MUST** still be stored,
* The implementation **MAY** warn about unsupported referrers,
* The Component Index **MUST NOT** be modified.

### 13.6 Discovery Behavior

#### 13.6.1 Registries Supporting the Referrers API

* A referrers query on the Component Index descriptor **MUST** return all component version manifests in that repository.
* Returned entries **MUST** include all artifacts whose `subject.digest` matches the Component Index.

This is the authoritative method for version discovery.

#### 13.6.2 Registries Not Supporting the Referrers API

When referrers are unsupported (see [Section on Unavailable Referrers in OCI Distribution Spec](https://github.com/opencontainers/distribution-spec/blob/main/spec.md#unavailable-referrers-api)):

* Implementations **MAY** create and manage a fallback “surrogate index” manifest referencing all versions.
* This fallback index **MUST** have a deterministic tag (e.g., `<index-digest>.ocm.index`).
* Component versions **SHOULD** retain their `subject` fields even if the registry ignores them.

#### 13.6.3 Hybrid Behavior

If the registry partially supports referrers:

* Implementations **SHOULD** attempt the Referrers API first.
* If the query fails or yields incomplete results, implementations **MAY** use fallback mechanisms.

### 13.7 Component Version Lifecycle

#### 13.7.1 On Push

When adding a component version:

1. Ensure the Component Index exists (creating it if necessary)
2. Set the Component Index descriptor as the version’s `subject` in its top level manifest.
3. Push all component version artifacts.

If the registry supports referrers, an entry **MUST** added to the referrers list.
If it does not, fallback tagging logic **MAY** be used.

#### 13.7.2 On Delete

Deleting a component version:

* **MUST** remove only the version’s own artifacts.
* **MUST NOT** delete or modify the Component Index.

Registries **MAY** automatically prune stale referrers.
Garbage Collection of Referrers **MAY** only be supported by OCI registries with support for blob deletion.

#### 13.7.3 On Enumerating Versions

Implementations **MUST** enumerate versions using:

1. **Preferred:** Referrers API on the Component Index descriptor
2. **Fallback:**
    * Repository tag listing
    * Surrogate index (if present)
    * Registry-native metadata

Any valid component version discovered via these methods **MUST** be accepted.

## 13.8 Referrer Tracking Policy

The `ReferrerTrackingPolicy` dictates how subject references and fallback indexes are used.
It **SHOULD** be configurable in the repository implementation. If not configurable, the default behavior **MUST** represent `ReferrerTrackingPolicyNone`.

### 13.8.1 `ReferrerTrackingPolicyNone`

* The implementation **MUST NOT** attempt to record referrers.
* Discovery relies on tag listing only.

### 13.8.2 `ReferrerTrackingPolicyByIndexAndSubject`

* Component versions **MUST** set the Component Index as their subject.
* If the registry supports referrers:
    * No fallback index is required.
* If unsupported:
    * A deterministic surrogate index **MAY** be created and tagged.

This is the recommended policy for full interoperability across registries.

## 13.9 Index Creation Rules (`CreateIfNotExists`)

Implementations performing index creation:

1. **MUST** check whether the empty index layer exists; if not, it **MUST** be pushed.
2. **MUST** check whether the Component Index manifest exists using its descriptor.
3. If absent:
    * Canonical JSON of the index manifest **MUST** be generated.
    * The manifest **MUST** be pushed using the exact descriptor.

Existing indexes **MUST NOT** be regenerated or altered.

## 14. Descriptor Encoding Formats

Descriptors **MAY** be stored using:

| Category | Media Type                                                      |
|----------|-----------------------------------------------------------------|
| YAML     | `application/vnd.ocm.software.component-descriptor.v2+yaml`     |
| JSON     | `application/vnd.ocm.software.component-descriptor.v2+json`     |
| TAR      | `application/vnd.ocm.software.component-descriptor.v2+yaml+tar` |

When using the TAR format:

* The TAR **MUST** contain a single file named `component-descriptor.yaml`.

Only format version `v2` is presently defined.


## 15. LocalBlob Resolution and OCI Layout Handling

This section defines the normative behavior for ingestion, storage, resolution, and retrieval of `localBlob` resources, including handling via OCI Image Layouts.

### 15.1 General Rules

1. Each `localBlob` access in the component descriptor:
    - **MUST** correspond to exactly one OCI descriptor in the component version’s artifact graph.
    - **MUST** be addressable by `localReference`, which **MUST** equal the descriptor’s digest.
    - **MAY** be represented as:
        - A single OCI layer.
        - An OCI image manifest.
        - An OCI image index.

2. Resolution of `localBlob` backed resources:
    - **MUST** be driven by `localReference` digest equality.
    - **MUST** be independent of any optional annotations on OCI artifacts.
    - **MUST** NOT depend on tag names.

3. A `localBlob` resource with `globalAccess`:
    - **MUST** treat `globalAccess` as an alternative access path.
    - **MUST** NOT change the semantics of `localReference`-based resolution.

### 15.2 Ingestion of LocalBlob Content

1. When a [`localBlob`](../02-access-types/localblob.md) resource is added through the repository interface, its content:
    - **MAY** be a single raw blob.
    - **MAY** be an OCI Image Layout (including a tar representation).
    - **MAY** be an [OCM Artifact Set Archive](../common/formatspec.md) with a `main` artifact

2. If the content is an OCI Image Layout, the implementation:
    - **MAY** reject the content if the implementation does not know how to introspect OCI Image Layouts.
    - **MAY** interpret the OCI Image Layout as a single layer tar archive (**legacy behavior**).
    - **MAY** interpret the OCI Image Layout as a manifest or index with its content graph co-located (recommended behavior). 
      If support for OCI Image Layouts is available in the implementation, 
      - the repository **MUST** interpret it according to the [OCI Image Layout Specification](https://github.com/opencontainers/image-spec/blob/main/image-layout.md).
      - **MAY** identify exactly one main artifact (manifest or index) as the root of the layout.
      - If multiple roots are accepted, it **MAY** create a virtual root descriptor referencing all roots present in the layout.

3. For each ingested `localBlob` based artifact interpreted as an OCI artifact in form of an OCI Image Layout:
    - The implementation **MUST** upload the complete corresponding OCI artifact graph (manifest or index and all referenced blobs) to the target OCI repository concurrently.
    - The implementation **MUST** record the resulting root descriptor for later association with the component version.

4. blob ingestion:
    - **MUST** defer final association with the component version until `AddComponentVersion` (or equivalent commit operation) is invoked.
    - **MUST** allow repositories to maintain temporary in-memory or local caches for descriptors and blobs prior to commit.
    - **MUST** clear such temporary state for the affected component version after successful commit.

### 15.3 Descriptor Mapping

1. For each `localBlob` resource, after ingestion:
    - `localReference` **MUST** equal the digest of the selected OCI descriptor:
        - If the `localBlob` is represented as an OCI manifest or index, `localReference` **MUST** be the digest of that manifest or index.
        - If the `localBlob` is represented as a single layer, `localReference` **MUST** be the digest of that layer.

    - If the `localBlob` declares `mediaType`, it:
        - **MUST** match the descriptor’s media type if the descriptor is a layer.
        - **MUST** match the manifest media type if the descriptor is a manifest.
        - **MUST** be treated as authoritative when the descriptor type allows multiple interpretations.

2. When a `localBlob` also exposes `globalAccess`:
    - `globalAccess` **MUST** be a valid access object that can be resolved to an OCI artifact (for example, an `OCIImage` access).
    - The artifact referenced by `globalAccess` **MUST** be content-identical to the artifact identified by `localReference`.

### 15.4 Resolution of LocalBlob Descriptors

1. To resolve a `localBlob` for a component version, the implementation:

    - **MUST** load the top-level artifact (manifest or index) corresponding to the component version tag.
    - **MUST** construct a set of candidate descriptors by:
        - Including all `layers` from the top-level manifest.
        - Including all `manifests` from the top-level index, if present.

2. The implementation:
    - **MUST** select the descriptor whose digest equals `localReference`.
    - **MUST** treat the absence of a matching descriptor as an error.
    - **MUST** treat the presence of multiple descriptors with the same digest as an error.

3. Nested artifacts:
    - **MAY** be discovered through recursive traversal when the selected descriptor is a manifest or index.
    - **MUST** be included in retrieval when building OCI layouts, as specified in [Section 15.5](#155-retrieval-of-localblob-content).

### 15.5 Retrieval of LocalBlob Content

#### 15.5.1 Layer-Based LocalBlob

1. If the selected descriptor is a layer descriptor:

    - The implementation **MUST** fetch the blob from the OCI store using the descriptor.
    - The implementation **MUST** verify that the fetched content’s digest equals the descriptor’s digest.
    - The implementation **MUST** return the resulting artifact blob as an OCI Image Layout with a tar representation.
      The implementation **MAY** declare the resulting blobs media type as `application/vnd.ocm.software.oci.layout.v1` with optional `+tar` and `+gzip` suffixes to indicate encoding.
    - If a matching descriptor is found, but the support for OCI Image Layouts is not available,
      the implementation **MAY** attempt to **synthesize** an OCM Artifact Set with a `main` artifact referencing the selected descriptor.

#### 15.5.2 Manifest- or Index-Based LocalBlob (OCI Layout Reconstruction)

1. If the selected descriptor is a manifest or index descriptor, and OCI Layout support is available:

    - The implementation **MUST** resolve and fetch the complete artifact graph reachable from that descriptor:
        - The manifest or index itself.
        - All referenced manifests, indexes, configs, and layers.

    - The implementation **MUST** reconstruct a valid OCI Image Layout in memory or on storage, including:
        - A valid `oci-layout` file.
        - A valid `index.json` that designates the root artifact.
        - All blobs stored under `/blobs/<algorithm>/<hex>`.

    - The implementation **MUST** return the reconstructed layout as a single blob (for example, an OCI layout tar archive).

2. If completion of the artifact graph or reconstruction of the layout fails, the implementation **MUST** treat retrieval as an error.

### 15.6 Interaction with Global Access

1. If a `localBlob` has `globalAccess`:

    - Retrieval implementations **MAY** use `globalAccess` to obtain the artifact if resolution via `localReference` is not possible in the current repository.
    - When using `globalAccess`, the resolved artifact:
        - **MUST** be content-identical to the artifact referenced by `localReference`.
        - **MUST** be normalized to a canonical OCI reference of the form `<registry>/<repository>@<digest>` for internal processing.

2. A `localBlob` that lacks `globalAccess`:
    - **MUST** be retrievable solely by `localReference`.
    - **MUST** cause retrieval to fail if the corresponding descriptor cannot be resolved from the component version’s artifact graph.

### 15.7 Validation Requirements

Implementations:

1. **MUST** validate that each `localBlob`’s `localReference` refers to an existing OCI descriptor in the component version’s artifact graph before or during retrieval.
2. **MUST** validate that any declared `mediaType` is consistent with the descriptor type and the content where such validation is possible.
3. **MUST** validate that any `globalAccess` reference resolves to an artifact whose digest matches `localReference`.
4. **MUST** treat as errors:
    - Invalid OCI layouts used during ingestion.
    - Inconsistent digests between descriptors and fetched content.
    - Multiple candidate descriptors for a single `localReference`.
    - Inability to determine a unique main artifact in an ingested OCI layout.

## 16. OCIImage Digest Processing

For a resource with an OCI Image access:

```
access:
  type: OCIImage
  imageReference: <ref>
```

The following additional processing conditions apply:

1. If descriptor lacks a digest:
    * The resolved digest **MUST** be written back.
2. If descriptor contains a digest:
    * The digest **MUST** match the resolved manifest.
3. If the reference includes an explicit digest:
    * It **MUST** match the resolved manifest.
4. After resolution:
    * References **MUST** be canonicalized to `<fqdn>@<digest>`.


## 17. Version Mapping Rules

OCI registries impose restrictions on valid tag formats:
OCI tags **MUST NOT** contain the `+` character, while OCM semantic versions **MAY** include build metadata using `+`.

This section defines the **canonical, lossless, and reversible transformation** between:

* OCM component versions (semantic versions), and
* OCI tag strings (registry-compliant identifiers).

These rules **MUST** be applied consistently across all OCM implementations.

### 17.1 BNF Grammar Definitions

Any OCM Component Version can be represented as an OCI tag using the following grammar:

```
<oci-tag> ::= <base-tag> | <base-tag> ".build-" <build-segments>

<base-tag> ::= <core> <prerelease-opt>
```

Where `<core>`, `<prerelease-opt>`, and `<build-segments>` are as defined in the OCM version grammar, except:

* No `+` is allowed.
* Build metadata **must** use the `.build-` prefix.

### 17.2 OCM Version → OCI Tag Transformation

Given:

```
<ocm-version> = <base-version>[+<buildmeta>]
```

Apply:

1. **Preserve core version and prerelease components** unchanged.
2. **Rewrite build metadata**:

```
+<buildmeta> → .build-<buildmeta>
```

### 17.3 OCI Tag → OCM Version Transformation

Given:

```
<oci-tag> = <base-tag>[.build-<buildmeta>]
```

Apply:

```
.build-<buildmeta> → +<buildmeta>
```

**Examples**

| OCI Tag                   | OCM Version         |
|---------------------------|---------------------|
| `1.2.3`                   | `1.2.3`             |
| `1.2.3.build-meta`        | `1.2.3+meta`        |
| `1.2.3-alpha.build-ci.42` | `1.2.3-alpha+ci.42` |
| `0.9.0.build-sha.abcd`    | `0.9.0+sha.abcd`    |

Round-trip equivalence is **required** for all implementations.
That is, applying both transformations in succession **MUST** yield the original input.

### 17.4 Manifest Annotation `software.ocm.componentversion`

Every top-level descriptor manifest (manifest- or index-based) **SHOULD** contain:

```
software.ocm.componentversion: "<component-repo-path>:<ocm-version>"
```

Where `<ocm-version>` is produced using the version mapping transformation described in this section.

This annotation enforces a strong filterable guarantee that can be used to differentiate
component version manifests from other artifacts stored in the same OCI repository.

## 18. Blob Repository Mapping

Any `localBlob` with an OCI artifact media type **MUST** map to:

```
<base-repository>/<reference-hint>
```

If no tag is available:

* Digest references **MUST** be used.


## 19. Compatibility Requirements

1. Both manifest-based and index-based storage **SHOULD** be supported by all clients, but write support **MAY** be limited to one of these formats.
2. Legacy descriptor formats (YAML, JSON, TAR) **SHOULD** be supported by all clients. At least one format **MUST** be supported for writing.
3. Index-based representation **MUST NOT** deprecate manifest-based representation.
4. The Component Index referrers mechanism **MAY** be used when supported by the registry.