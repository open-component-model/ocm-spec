# OCI Registries

Status: **Proposal**

_This specification is in proposal status as it is being unified with the rest of the OCM specifications._

The specification defines how OCM repositories, component descriptors, and artifacts are stored and resolved inside OCI registries. 
It standardizes the repository format, how component names map to OCI paths, and how versions are represented using either OCI manifests or OCI indexes. 
It prescribes strict rules for descriptor selection, LocalBlob handling, digest validation, and version-to-tag mapping. 
The specification also introduces a Component Index artifact used for referrer-based version discovery and defines fallback mechanisms for registries lacking referrer support.

<!-- TOC -->
* [OCI Registries](#oci-registries)
  * [1. Scope](#1-scope)
  * [2. Conformance Terminology](#2-conformance-terminology)
  * [3. Registry Requirements](#3-registry-requirements)
  * [4. Repository Specification Format](#4-repository-specification-format)
    * [4.1 `type`](#41-type)
    * [4.2 `baseUrl`](#42-baseurl)
    * [4.3 `subPath`](#43-subpath)
    * [4.4. `componentNameMapping`](#44-componentnamemapping)
    * [4.5. String Reference Grammar](#45-string-reference-grammar)
    * [4.6. Formal Grammar (Informative)](#46-formal-grammar-informative)
  * [5. Component Repository Mapping](#5-component-repository-mapping)
  * [6. Component Version Storage Models](#6-component-version-storage-models)
    * [6.1. Manifest Representation](#61-manifest-representation)
    * [6.2. Index Representation](#62-index-representation)
    * [6.3. Artifact-Level Annotations](#63-artifact-level-annotations)
  * [7. Descriptor Selection Logic](#7-descriptor-selection-logic)
  * [8. Component Index (Referrer Anchor)](#8-component-index-referrer-anchor)
    * [8.1 Requirements](#81-requirements)
    * [8.2 Version Behavior](#82-version-behavior)
    * [8.3 Discovery](#83-discovery)
    * [8.4 Referrer Tracking Policy](#84-referrer-tracking-policy)
    * [8.5 Component Index Lifecycle](#85-component-index-lifecycle)
      * [8.5.1 Creation](#851-creation)
      * [8.5.2 Publishing a Component Version](#852-publishing-a-component-version)
      * [8.5.3 Deleting a Component Version](#853-deleting-a-component-version)
      * [8.5.4 Version Enumeration](#854-version-enumeration)
      * [8.5.5 Fallback Behavior on Registries Without Referrer Support](#855-fallback-behavior-on-registries-without-referrer-support)
  * [9. Descriptor Encoding Formats](#9-descriptor-encoding-formats)
  * [10. `localBlob` Processing](#10-localblob-processing)
    * [10.1 Ingestion](#101-ingestion)
    * [10.2 Mapping](#102-mapping)
    * [10.3 Resolution](#103-resolution)
    * [10.4 Retrieval](#104-retrieval)
  * [11. `OCIArtifact/v1` Processing](#11-ociartifactv1-processing)
    * [11.1 Legacy Access Type Identifiers](#111-legacy-access-type-identifiers)
    * [11.2 Digest Resolution and Canonicalization Requirements](#112-digest-resolution-and-canonicalization-requirements)
    * [11.3 Translation of `localBlob` to `OCIArtifact/v1`](#113-translation-of-localblob-to-ociartifactv1)
  * [12. Tag and Version Mapping Rules](#12-tag-and-version-mapping-rules)
  * [13. Compatibility Requirements](#13-compatibility-requirements)
* [Examples (Informative)](#examples-informative)
  * [Simple Examples](#simple-examples)
    * [Repository Specification Examples](#repository-specification-examples)
      * [A. Minimal HTTPS Example](#a-minimal-https-example)
      * [B. OCI Scheme with Auto-Derived Subpath](#b-oci-scheme-with-auto-derived-subpath)
      * [C. Explicit Subpath (No Auto-Extraction)](#c-explicit-subpath-no-auto-extraction)
    * [Repository Grammar Validity](#repository-grammar-validity)
      * [Valid References](#valid-references)
      * [Invalid References](#invalid-references)
    * [Component → Repository Mapping](#component--repository-mapping)
  * [Intermediate Examples](#intermediate-examples)
    * [Manifest Representation](#manifest-representation)
    * [Index Representation](#index-representation)
    * [Descriptor Selection Logic](#descriptor-selection-logic)
    * [LocalBlob Resolution](#localblob-resolution)
    * [Version Mapping](#version-mapping)
  * [Advanced End-to-End Examples](#advanced-end-to-end-examples)
    * [Publishing a Component Version](#publishing-a-component-version)
      * [Scenario](#scenario)
      * [1. Repository Mapping](#1-repository-mapping)
      * [2. Version Tag Mapping](#2-version-tag-mapping)
      * [3. Manifest Assembly](#3-manifest-assembly)
      * [4. Component Index Subject](#4-component-index-subject)
      * [5. LocalBlob Mapping](#5-localblob-mapping)
    * [Subject Handling When Registry Rejects `subject`](#subject-handling-when-registry-rejects-subject)
    * [Full OCI Layout Reconstruction](#full-oci-layout-reconstruction)
    * [Index vs Manifest Fallback](#index-vs-manifest-fallback)
    * [LocalBlob → OCIArtifact/v1 Conversion](#localblob--ociartifactv1-conversion)
<!-- TOC -->

## 1. Scope

This specification defines the normative mapping of OCM repositories, component descriptors, and related artifacts onto OCI registries implementing the OCI Distribution Specification.
It specifies:

* Repository specification format and location resolution
* Mapping of component identifiers and versions to OCI repositories
* Manifest- and index-based component version storage
* Descriptor selection rules
* LocalBlob ingestion, storage, resolution, and retrieval
* Version mapping between OCM versions and OCI tags
* Component Index semantics for referrer-driven discovery
* Compatibility requirements for clients and registries

This document is authoritative for all interactions between OCM and OCI registries.
This document is normative unless explicitly marked as ‘Informative’.

## 2. Conformance Terminology

The key words **MUST**, **MUST NOT**, **SHOULD**, **SHOULD NOT**, **MAY**, and **OPTIONAL** follow RFC 2119 and RFC 8174.

## 3. Registry Requirements

An OCI registry used with OCM:

* **SHOULD** conform to the [OCI Distribution Specification v1.1.1](https://github.com/opencontainers/distribution-spec/releases/tag/v1.1.1).
* **MAY** allow HTTP when explicitly configured.
* **MAY** host multiple OCM repositories through different repository prefixes.

## 4. Repository Specification Format

An OCM repository backed by an OCI registry is described using the following structure:

```text
type: <TYPE>[/VERSION]
baseUrl: <registry-base-url>
subPath: <optional-prefix>
componentNameMapping: <mapping-mode>   # OPTIONAL
```

A repository specification determines the registry host, the optional subpath prefix, and how the OCM repository is rooted within the OCI namespace.


### 4.1 `type`

The repository type **SHOULD** be exactly:

```text
OCI/v1
```

This is the **only supported and non-deprecated** repository type.
All other identifiers are considered **deprecated**.

Clients **SHOULD** accept the following identifiers for backward compatibility and treat them the same as `OCI/v1`:

**Deprecated forms:**

```text
oci/v1
OCIRegistry/v1
ociRegistry/v1
OCIRepository/v1
OCI
oci
OCIRegistry
ociRegistry
OCIRepository
```

Compliant writers **SHOULD NOT** emit any deprecated identifier.

### 4.2 `baseUrl`

`baseUrl` **MUST** identify the registry host and optional port.
It MAY include an explicit scheme:

* `https://` (recommended)
* `http://` (only if allowed by policy)
* `oci://` (treated as HTTPS for transport)

If no scheme is present, clients **MUST** assume **HTTPS**.

**Allowed Examples**

```text
https://registry.example.com
https://registry.example.com:5000
oci://registry.example.com:5000
docker.io
ghcr.io
http://insecure-registry.local:8080
```

### 4.3 `subPath`

OCM repository specifications include a `subPath` field.
`subPath` defines the **repository prefix** under which all OCM-managed repositories are located.
Multiple OCM repositories MAY share the same registry via different `subPath` values.

If:

* `subPath` is empty **AND**
* `baseUrl` contains a path component,

then clients **MUST** automatically normalize the specification by splitting the value:

**Example:**

Input:

```text
baseUrl = "ghcr.io/open-component-model/ocm"
subPath = ""
```

Normalized form:

```text
baseUrl = "ghcr.io"
subPath = "open-component-model/ocm"
```

If a user supplies an explicit `subPath`, no auto-extraction occurs:

```text
baseUrl = "ghcr.io"
subPath = "open-component-model/ocm"
```

### 4.4. `componentNameMapping`

componentNameMapping controls how a component identifier:

```text
<id> ::= <segment>{"/"<segment>}
```

is mapped into the underlying OCI repository path.

Supported value: `urlPath`

Component identifiers are mapped directly as slash-separated OCI path segments without modification.

Deprecated mappings such as `sha256-digest` **MUST NOT** be used by writers but MAY be accepted by readers for backward compatibility.

### 4.5. String Reference Grammar

An OCI repository string reference has the form:

```text
[scheme://]<host>[:port][/<path>]
```

This reference form is a string-based representation of the OCI repository reference.
It can be used in places where a full repository specification is not practical, such as in a CLI.

In this case the repository reference **MUST** be parsed according to the following rules:

* If `scheme://` is missing, assume `https://`.
* `<host>` **MUST** be a valid DNS hostname.
* `:port` **MAY** be omitted; if present, it **MUST** be a valid TCP port number.
* `<path>` **MAY** be omitted; if present, it **MUST** consist of slash-separated segments of `[A-Za-z0-9._-]+`.
* The entire reference **MUST** conform to URI syntax rules.
* Invalid references **MUST** be rejected.
* The parsed reference **MUST** be converted into a repository specification with:
  * `baseUrl` = `scheme://host[:port]`
  * `subPath` = `<path>` (if present)

### 4.6. Formal Grammar (Informative)

The following grammar defines the canonical structure of repository references.
This grammar complements the parsing rules in [4.5](#45-string-reference-grammar)
and serves as an informative reference for implementers.

```text
<repository-ref> ::= [ <scheme> "://" ] <host> [ ":" <port> ] [ "/" <repo-path> ]
<scheme>         ::= "http" | "https" | "oci"
<host>           ::= <dns-label> { "." <dns-label> }
<dns-label>      ::= <alphanum> { <alphanum> | "-" }
<port>           ::= <digit> { <digit> }
<repo-path>      ::= <segment> { "/" <segment> }
<segment>        ::= <alphanum> { <alphanum> | "-" | "_" | "." }
<alphanum>       ::= "A".."Z" | "a".."z" | "0".."9" 
<digit>          ::= "0".."9"
```

## 5. Component Repository Mapping

A component identifier:

```text
<id> ::= <segment>{"/"<segment>}
<segment> ::= [A-Za-z0-9._-]+
```

**MUST** map to:

```text
<base-repository>/component-descriptors/<component-id>
```

All versions of a component reside in this repository.

## 6. Component Version Storage Models

A component version **MUST** be stored as either:

1. A **manifest** (`application/vnd.oci.image.manifest.v1+json`), or
2. An **index** (`application/vnd.oci.image.index.v1+json`).

Readers **MUST** accept all supported forms. Writers **MAY** restrict to one of these formats.

Supported representations are defined in [6.1. Manifest Representation](#61-manifest-representation) and [6.2. Index Representation](#62-index-representation).
Supported descriptor formats are defined in [9. Descriptor Encoding Formats](#9-descriptor-encoding-formats).

### 6.1. Manifest Representation

A manifest representing a component version:

* **MUST** contain exactly one layer annotated `software.ocm.descriptor="true"`.
* **MUST** include a config with media type
  `application/vnd.ocm.software.component.config.v1+json`.
* The config **MUST** contain a `componentDescriptorLayer` OCI descriptor.
* Each `localBlob` **MUST** map to exactly one layer whose digest equals its `localReference`.
* Optional `globalAccess` **MAY** be present but **MUST NOT** override digest resolution.

### 6.2. Index Representation

An index representing a component version:

* **MUST** contain exactly one manifest annotated `software.ocm.descriptor="true"`.
* **MUST** include a config with media type
  `application/vnd.ocm.software.component.config.v1+json`.
* The config **MUST** contain a `componentDescriptorLayer` OCI descriptor.
* Additional manifests **MAY** be included.
* The index config **MUST** reference the descriptor layer as a manifest based on [6.1. Manifest Representation](#61-manifest-representation).
* Each `localBlob` **MUST** map to either
  * exactly one layer whose digest equals its `localReference` located within the manifest annotated `software.ocm.descriptor="true"`, or
  * exactly one manifest or index whose digest equals its `localReference` located within the index.
    see [10. Local Blob Processing](#10-localblob-processing) for details.

### 6.3. Artifact-Level Annotations

Artifact Entries in the manifest or index (see [6.1. Manifest Representation](#61-manifest-representation) and [6.2. Index Representation](#62-index-representation)) **MAY** include:

```text
software.ocm.artifact: [{"identity": {...}, "kind": "resource|source"}]
```

This annotation:

* **MUST NOT** affect resolution
* **MUST NOT** override digest-based `localReference` logic

Digest equality **MUST** govern all mapping and resolution.

This annotation serves purely informational/discovery purposes and actual resolution **MUST** follow the rules in [10. Local Blob Processing](#10-localblob-processing).

## 7. Descriptor Selection Logic

When resolving a component version reference:

1. Resolve the tag to a descriptor, which **MUST** point to either a manifest or index. 
   The reference resolution must respect versioning rules defined in [12. Tag and Version Mapping Rules](#12-tag-and-version-mapping-rules).
2. If manifest → it **MUST** be interpreted as the component descriptor root according to [6.1. Manifest Representation](#61-manifest-representation).
3. If index → enumerate and find the manifest annotated `software.ocm.descriptor="true"`:
    * If exactly one exists → select it and interpret it according to [6.1. Manifest Representation](#61-manifest-representation).
    * If multiple exist → resolution **MUST** fail.
    * If none exist → select manifest[0] (compatibility rule).
    * Interpret other manifests as regular artifacts roots according to [6.2. Index Representation](#62-index-representation).

## 8. Component Index (Referrer Anchor)

The Component Index is a stable, immutable OCI manifest that functions as the referrer
anchor for all Component Versions within an OCM repository. Its manifest structure
and descriptor values are fixed exactly to those defined in the implementation and
**MUST** never vary. The rules in this section extend the definition of the Component Index
from [8.1 Requirements](#81-requirements), its role during version publication from
[8.2 Version Behavior](#82-version-behavior), and its role in discovery as described in
[8.3 Discovery](#83-discovery).

### 8.1 Requirements

The Component Index **MUST** match the exact manifest defined by the OCM implementation:

```json
{
  "schemaVersion" : 2,
  "mediaType" : "application/vnd.oci.image.manifest.v1+json",
  "artifactType" : "application/vnd.ocm.software.component-index.v1+json",
  "config" : {
    "mediaType" : "application/vnd.oci.empty.v1+json",
    "digest" : "sha256:44136fa355b3678a1146ad16f7e8649e94fb4fc21fe77e8310c060f61caaff8a",
    "size" : 2,
    "data" : "e30="
  },
  "layers" : [ {
    "mediaType" : "application/vnd.oci.empty.v1+json",
    "digest" : "sha256:44136fa355b3678a1146ad16f7e8649e94fb4fc21fe77e8310c060f61caaff8a",
    "size" : 2,
    "data" : "e30="
  } ],
  "annotations" : {
    "org.opencontainers.image.description" : "This is an OCM component index. It is an empty jsonthat can be used as referrer for OCM component descriptors. It is used as a subjectfor all OCM Component Version Top-Level Manifests and can be used to reference back allOCM Component Versions",
    "org.opencontainers.image.title" : "OCM Component Index V1"
  }
}
```

The canonical JSON for this manifest **MUST** produce the descriptor:

```text
Digest: sha256:9717cda41c478af11cba7ed29f4aa3e4882bab769d006788169cbccafc0fcd05
Size: 837
MediaType: application/vnd.oci.image.manifest.v1+json
ArtifactType: application/vnd.ocm.software.component-index.v1+json
```

This descriptor is normative and **MUST NOT** change.

### 8.2 Version Behavior

Each component version:

* **SHOULD** set the Component Index as its OCI `subject`.
* **MUST NOT** require registry support for referrers to publish successfully.

### 8.3 Discovery

Registries supporting the Referrers API:

* **MUST** return all component versions referencing the Component Index.

Registries lacking referrers:

* Clients **MAY** use deterministic surrogate indexes.
* Subjects **MUST** remain set even if ignored.

### 8.4 Referrer Tracking Policy

Registries differ in their support for referrers as defined by the OCI Distribution Specification.
Implementations interacting with Component Indexes **MUST** conform to the following policy:

1. When a registry supports the Referrers API:
    * Component Version manifests **MUST** appear in the referrers list for the Component Index.
    * Clients **MUST** enumerate versions exclusively through referrers (see [8.3](#83-discovery)).

2. When a registry does not support referrers:
    * Clients **MAY** fall back to repository listing.
    * Clients **MUST NOT** attempt to modify or recreate the Component Index to emulate referrer behavior.
    * The absence of referrers **MUST NOT** affect Component Index immutability (see [8.5](#85-component-index-lifecycle)).

3. Registries with partial subject/referrer support:
    * Clients **MUST** tolerate silent dropping of the `subject` field.
    * Clients **MUST** use a hybrid enumeration strategy combining available APIs and fallback mechanisms.

This policy ensures consistent behavior regardless of registry capability.

### 8.5 Component Index Lifecycle

#### 8.5.1 Creation

Creation follows the normative behavior equivalent and depends
on the repository structure defined in
[4. Repository Specification Format](#4-repository-specification-format).

Implementations **MUST** check whether the fixed empty layer exists in the repository,
and if it does not exist, they **MUST** push it using the exact descriptor and content
defined by this specification.

Implementations **MUST** check whether the Component Index manifest descriptor exists.
If it does not, they **MUST** marshal the fixed manifest byte-for-byte and push it using
the canonical descriptor defined above.

The canonical JSON representation of the manifest **MUST** be identical to the JSON used
to compute the descriptor’s digest and size.

The Component Index **MUST** be immutable. Implementations **MUST NOT** rewrite, replace,
or mutate an existing Component Index manifest under any circumstances.

Repeated initialization **MUST** be idempotent.

#### 8.5.2 Publishing a Component Version

Component Version publication interacts with the Component Index according to the
representation rules in  
[6. Component Version Storage Models](#6-component-version-storage-models).

Before publishing a Component Version, implementations **MUST** ensure the Component Index exists.

The top-level manifest of a Component Version SHOULD set its `subject` field to the
Component Index descriptor. If the registry rejects the subject field, the Component
Version **MUST** still be published without modifying the Component Index.

Publishing a Component Version **MUST NOT** regenerate, rewrite, or replace the Component Index.

If the registry supports the OCI Referrers API, publishing **MUST** cause the Component
Version to appear as a referrer of the Component Index descriptor.

The Component Index **MUST** remain an empty manifest without references to any component versions.

#### 8.5.3 Deleting a Component Version

Deletion behavior **MUST** preserve Component Index immutability.

Deletion **MUST** remove only the artifacts associated with the specific Component Version.

The Component Index **MUST NOT** be deleted, rewritten, regenerated, or replaced.

Implementations **MUST** tolerate registry-level garbage collection or referrer pruning
without attempting to recreate or update the Component Index.

The absence of Component Versions **MUST NOT** affect the digest or existence of the Component Index.

#### 8.5.4 Version Enumeration

Version enumeration depends on the discovery behavior defined in  
[8.3 Discovery](#83-discovery).

If the registry supports the OCI Referrers API, implementations **MUST** enumerate
Component Versions via the referrers list of the Component Index descriptor.

If the registry does not support referrers, implementations MAY use fallback methods,
including tag listing or repository metadata, but they **MUST** continue to treat the Component
Index descriptor as the authoritative anchor.

Any artifact whose `subject.digest` equals the Component Index digest **MUST** be
recognized as a Component Version.

The Component Index itself **MUST NOT** be considered a Component Version.

Implementations **MUST** remain correct even if Component Versions are externally added or removed.

#### 8.5.5 Fallback Behavior on Registries Without Referrer Support

Registries may ignore subject references. Behavior in such environments **MUST** ensure
consistent semantics.

Component Versions **MUST** still set their `subject` field to the Component Index descriptor,
regardless of registry support.

Implementations **MUST NOT** modify the Component Index or create surrogate indexes to emulate referrer behavior.

Implementations MAY maintain internal metadata for enumeration, but such metadata **MUST NOT**
modify content stored in the OCI registry and **MUST NOT** change the Component Index manifest or descriptor.

The Component Index **MUST** remain unchanged regardless of registry capability.

## 9. Descriptor Encoding Formats

Descriptors **MAY** use:

* `application/vnd.ocm.software.component-descriptor.v2+yaml`
* `application/vnd.ocm.software.component-descriptor.v2+json`
* `application/vnd.ocm.software.component-descriptor.v2+yaml+tar`
  When in TAR form **MUST** contain exactly one `component-descriptor.yaml`.

## 10. `localBlob` Processing

This deals with `localBlob` access methods referencing content stored within the same OCI artifact graph as the component version.
See [localBlob as an Access Type](../02-access-types/localblob.md)

### 10.1 Ingestion

Content presented as a `localBlob` **MAY** be a raw blob, an [OCI layout](https://github.com/opencontainers/image-spec/blob/v1.1.1/image-layout.md), or an OCM artifact set (deprecated).
Layout interpretation **MAY** be rejected if unsupported; if accepted, the entire artifact graph **MUST** be ingested.
If unsupported and not rejected, ingestion **SHOULD** proceed as a manifest layer.

### 10.2 Mapping

Each `localBlob`:

* **MUST** correspond to exactly one OCI descriptor (layer, manifest, or index).
* The descriptor digest **MUST** equal `localReference`.
* Declared media types **MUST** match descriptor media types.
* If `globalAccess` is provided, it **MUST** resolve to a digest-equal artifact.

### 10.3 Resolution

A client:

* **MUST** examine all descriptors reachable from the component version artifact.
* **MUST** identify exactly one descriptor matching `localReference`.
* **MUST** fail if zero or multiple matches exist.

### 10.4 Retrieval

* Layer descriptor → fetch blob directly.
* Manifest/index descriptor → reconstruct a valid OCI Image Layout containing all referenced blobs and descriptors.

Reconstruction failure **MUST** fail retrieval.

If reconstruction is attempted, the following rules apply:

* The root descriptor **MUST** become the sole entry in `index.json`.
* All referenced blobs **MUST** be written under `blobs/<alg>/<digest>`.
* Media types **MUST** be preserved exactly.
* Missing blobs, mismatched digests, or incomplete graphs **MUST** cause reconstruction failure.
* The resulting layout **MUST** be a valid OCI Image Layout as defined in
  <https://github.com/opencontainers/image-spec/blob/v1.1.1/image-layout.md>.

This provides a portable format for redistributing version content.

## 11. `OCIArtifact/v1` Processing

This deals with access methods of type `OCIArtifact/v1`, representing OCI artifacts stored in OCI registries.
See [ociArtifact as an Access Type](../02-access-types/ociartifact.md).

### 11.1 Legacy Access Type Identifiers

Clients **MUST** treat the following legacy identifiers exactly as `OCIArtifact/v1`:

```text
OCIArtifact
ociArtifact/v1
ociArtifact
ociRegistry/v1
ociRegistry
ociImage/v1
ociImage
OCIImage/v1
OCIImage
```

Compliant writers **SHOULD NOT** emit any of the deprecated identifiers above.

### 11.2 Digest Resolution and Canonicalization Requirements

An `OCIArtifact/v1` access method represents an OCI artifact that may resolve to either a manifest or an index as defined in
[6.1. Manifest Representation](#61-manifest-representation) and
[6.2. Index Representation](#62-index-representation).
When supplied through a `localBlob`, ingestion and mapping follow
[10. Local Blob Processing](#10-localblob-processing).

Digest processing for `OCIArtifact/v1` **MUST** satisfy all of the following:

1. **Missing digests**
   If the provided reference does not include a digest, clients **MUST** resolve the artifact,
   and **MAY** write back the canonical digest reference corresponding to the resolved manifest or index (see [10.3 Resolution](#103-resolution)).

2. **Digest validation**
   If the reference includes a digest in its access specification and its resource digest specification, the resolved artifact **MUST** match that digest exactly (see [10.2 Mapping](#102-mapping)).
   A mismatch **MUST** cause resolution failure.

3. **Deterministic tag resolution**
   Tag-based references **MUST** resolve deterministically to exactly one artifact.

4. **Canonical reference formatting**
   The final resolved reference **MUST** be canonicalized in digest form:

   ```text
   <registry>/<repository>@<digest>
   ```
   
This form may be restored by clients after resolution, ingestion, or mapping.

### 11.3 Translation of `localBlob` to `OCIArtifact/v1`

When an artifact originates from a `localBlob` and is translated into `OCIArtifact/v1`, ingestion **MUST** produce a stable digest (see
[10.1 Ingestion](#101-ingestion) and
[10.4 Retrieval](#104-retrieval)).
After upload, the resulting digest reference **MUST** replace any tag-based or non-digest reference,
but **SHOULD** retain its value if not modified.

The resulting `OCIArtifact/v1` access method **MUST** include:
* A digest-based `imageReference` pointing to the uploaded artifact.
* The original media type of the artifact (manifest or index).

## 12. Tag and Version Mapping Rules

Because OCI tags do not allow `+`, OCM versions with build metadata **MUST** encode it as:

```text
.build-<build>
```

Round-trip conversion between OCM versions and OCI tags **MUST** be exact.

Examples:

| OCI Tag             | OCM Version   |
|---------------------|---------------|
| `1.2.3`             | `1.2.3`       |
| `1.2.3.build-ci.42` | `1.2.3+ci.42` |

Tags **SHOULD** reference a manifest or index (see [6](#6-component-version-storage-models)) whose descriptor **MUST** include the annotation:

```text
software.ocm.componentversion: "<component>:<version>"
```

## 13. Compatibility Requirements

* Clients **SHOULD** support reading manifest- and index-based storage; write support **MAY** be limited.
* Descriptor formats (YAML, JSON, TAR) **SHOULD** be read; at least one **MUST** be written.
* Index-based representation **MUST NOT** deprecate manifest-based.
* Component Index semantics **MAY** rely on registry referrer support but MUST NOT require it.

# Examples (Informative)

This section contains **non-normative** examples illustrating how the rules in this specification operate in practice.
The structure, headings, and link anchors remain unchanged, but the example content has been rewritten for clarity and readability.

Examples are grouped into:

* [Simple Examples](#simple-examples)
* [Intermediate Examples](#intermediate-examples)
* [Advanced End-to-End Examples](#advanced-end-to-end-examples)

## Simple Examples

### Repository Specification Examples

*(References: [4. Repository Specification Format](#4-repository-specification-format))*

#### A. Minimal HTTPS Example

```text
type: OCI/v1
baseUrl: registry.example.com
```

Interpretation:

* No scheme → clients **MUST** assume HTTPS ([4.2](#42-baseurl)).
* The repository root is:
  `registry.example.com`
* Component descriptors map under:
  `registry.example.com/component-descriptors/<component>`

#### B. OCI Scheme with Auto-Derived Subpath

```text
type: OCI/v1
baseUrl: oci://ghcr.io/acme
```

* The scheme `oci://` is treated as HTTPS ([4.2](#42-baseurl)).
* The `/acme` suffix becomes the `subPath` ([4.3](#43-subpath)).

Normalized form:

```text
baseUrl: ghcr.io
subPath: acme
```

#### C. Explicit Subpath (No Auto-Extraction)

```text
type: OCI/v1
baseUrl: ghcr.io
subPath: open-component-model/ocm
```

Because `subPath` is explicitly provided, **no normalization** occurs ([4.3](#43-subpath)).

### Repository Grammar Validity

*(References: [4.5. Repository Reference Grammar](#45-string-reference-grammar))*

#### Valid References

| Reference                                        | Why valid                              |
|--------------------------------------------------|----------------------------------------|
| `ghcr.io/org/component`                          | Allowed hostname + valid path segments |
| `https://registry.example.com:5000/repo/subrepo` | Valid scheme, host, port, and segments |

#### Invalid References

| Reference       | Reason                               |
|-----------------|--------------------------------------|
| `ghcr..io/repo` | Hostname contains invalid double dot |
| `http:///repo`  | Scheme without hostname              |

Invalid references **MUST** be rejected ([4.5](#45-string-reference-grammar)).

### Component → Repository Mapping

*(References: [5. Component Repository Mapping](#5-component-repository-mapping))*

Given:

```text
Component ID: github.com/acme/helloworld
baseUrl: ghcr.io
subPath: ocm/test
```

The mapped OCI repository becomes:

```text
ghcr.io/ocm/test/component-descriptors/github.com/acme/helloworld
```

All versions reside under this repository.

## Intermediate Examples

### Manifest Representation

*(References: [6.1. Manifest Representation](#61-manifest-representation))*

A manifest storing a component version may look like:

```json
{
  "mediaType": "application/vnd.oci.image.manifest.v1+json",
  "config": {
    "mediaType": "application/vnd.ocm.software.component.config.v1+json",
    "digest": "sha256:abcd1234",
    "size": 123
  },
  "layers": [
    {
      "annotations": { "software.ocm.descriptor": "true" },
      "mediaType": "application/vnd.ocm.software.component-descriptor.v2+json",
      "digest": "sha256:componentdesc"
    },
    {
      "mediaType": "text/plain",
      "digest": "sha256:deadbeef"
    }
  ]
}
```

Key points:

* The descriptor is the layer annotated by media type.
* **MUST** contain exactly one layer annotated software.ocm.descriptor="true"
* Any `localBlob` with digest `sha256:deadbeef` must resolve to the second layer (([10.2](#102-mapping))).

### Index Representation

*(References: [6.2. Index Representation](#62-index-representation))*

```json
{
  "mediaType": "application/vnd.oci.image.index.v1+json",
  "manifests": [
    {
      "digest": "sha256:desc1",
      "annotations": { "software.ocm.descriptor": "true" }
    },
    {
      "digest": "sha256:artifact1"
    }
  ]
}
```

The descriptor root is:

```text
sha256:desc1
```

Additional manifests are regular artifacts.

### Descriptor Selection Logic

*(References: [7. Descriptor Selection Logic](#7-descriptor-selection-logic))*

Given an index:

| Digest     | Annotation        |
| ---------- | ----------------- |
| sha256:aaa | descriptor="true" |
| sha256:bbb | —                 |
| sha256:ccc | —                 |

Selected descriptor:

```text
sha256:aaa
```

If two descriptor annotations exist → **resolution MUST fail** ([7](#7-descriptor-selection-logic)).
If none exist → select the **first manifest** for compatibility ([7](#7-descriptor-selection-logic)).

### LocalBlob Resolution

*(References: [10.3 Resolution](#103-resolution))*

```text
localReference: sha256:beef1234
```

Resolution steps:

1. Examine **all** layers, manifests, and index entries reachable from the component version.
2. Find exactly **one** descriptor whose digest matches `sha256:beef1234`.
3. If 0 or >1 matches → **fail** ([10.3](#103-resolution)).

### Version Mapping

*(References: [12. Tag and Version Mapping Rules](#12-tag-and-version-mapping-rules))*

OCM → OCI:

```text
1.2.3+ci.42 → 1.2.3.build-ci.42
```

OCI → OCM:

```text
1.2.3.build-ci.42 → 1.2.3+ci.42
```

Round-trip **MUST** be exact.

## Advanced End-to-End Examples

### Publishing a Component Version

*(References: [5](#5-component-repository-mapping), [6.1](#61-manifest-representation), [7](#7-descriptor-selection-logic), [8](#8-component-index-referrer-anchor), [10](#10-localblob-processing), [12](#12-tag-and-version-mapping-rules))*

#### Scenario

* Component: `github.com/acme/helloworld`
* Version: `1.0.0+ci.5`
* Registry: `ghcr.io/ocm/test`
* LocalBlob digest: `sha256:beef1234`

#### 1. Repository Mapping

```text
ghcr.io/ocm/test/component-descriptors/github.com/acme/helloworld
```

#### 2. Version Tag Mapping

```text
1.0.0+ci.5 → 1.0.0.build-ci.5
```

#### 3. Manifest Assembly

Manifest includes:

* Descriptor layer
* LocalBlob layer (`sha256:beef1234`)
* Config referencing the descriptor layer

#### 4. Component Index Subject

Manifest sets its `subject` to the Component Index descriptor.

#### 5. LocalBlob Mapping

Digest equality ensures the LocalBlob resolves exactly to one descriptor.

### Subject Handling When Registry Rejects `subject`

*(References: [8.2 Version Behavior](#82-version-behavior), [8.5.2 Publishing a Component Version](#852-publishing-a-component-version))*

If the registry removes:

```json
"subject": { ... }
```

Then:

* Publication **MUST** still succeed.
* The Component Index **MUST NOT** be regenerated.
* Discovery may use fallback ([8.5.5](#855-fallback-behavior-on-registries-without-referrer-support)).

### Full OCI Layout Reconstruction

*(References: [10.4 Retrieval](#104-retrieval))*

Given a manifest referencing:

* several layers
* a nested manifest

Reconstruction produces a valid OCI Image Layout:

```text
index.json                          # includes only the root descriptor
blobs/sha256/<digest-of-root>
blobs/sha256/<each-layer>
blobs/sha256/<nested-manifest>
```

Failure conditions:

* Missing blob
* Digest mismatch
* Incomplete graph

Any of these **MUST** abort retrieval ([10.4](#104-retrieval)).

### Index vs Manifest Fallback

*(References: [7 Descriptor Selection Logic](#7-descriptor-selection-logic))*

If:

```text
sha256:index1
```

contains **no** descriptor annotation:

* **MUST** select `manifests[0]` as descriptor root.
* All others remain artifacts.

### LocalBlob → OCIArtifact/v1 Conversion

*(References: [11.3 Translation of `localBlob` to `OCIArtifact/v1`](#113-translation-of-localblob-to-ociartifactv1))*

Input:

```text
localBlob:
  mediaType: application/zip
  localReference: sha256:beef
```

After ingestion + upload:

```text
imageReference: ghcr.io/acme/repo@sha256:beef...
```

The access method becomes canonical digest form [11.2 Digest Resolution and Canonicalization Requirements](#112-digest-resolution-and-canonicalization-requirements).