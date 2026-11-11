# Conventions

To ensure uniformity across tools that interact with content from the component model,
certain conventions should be adhered to.

These conventions are not covered by the [model-tool contract](../05-guidelines/02-contract.md#model-contract).
They are also not part of the specifications but should be obeyed
to achieve a common understanding about the meaning of content.

## Intended Environments

There are several scenarios where artifacts will be provided as content of [component versions](./02-elements-toplevel.md), which might be bound to a dedicated runtime environment. If a component version should provide several flavors of the same artifact intended for different environments they should use the same element name and version, and the environment should be reflected by one or more [extra identity properties](./03-elements-sub.md#element-identity).

### Operating System and CPU Architecture

For executables and container images the platform properties defined by the specification for [OCI image indices](https://github.com/opencontainers/image-spec/blob/main/image-index.md#image-index-property-descriptions) should be used.

The following extra identity properties are defined. They correspond to the fields of the OCI `platform` object and MUST carry the same meaning:

- **`os`**: the operating system the element is intended for. It SHOULD use values listed in the Go Language document for [GOOS](https://go.dev/doc/install/source#environment).
- **`architecture`**: the CPU architecture the element is intended for. It should use values listed in the Go Language document for [GOARCH](https://go.dev/doc/install/source#environment).
- **`variant`** (optional): the variant of the CPU architecture, for example `v7` for `arm` or `v8` for `arm64`. It SHOULD use the values listed in the OCI image index specification. It MUST NOT be used for anything else than the CPU variant. Differences in how an artifact was built are expressed by the [`flavor`](#build-flavor) property.
- **`os.version`** (optional): the version of the operating system the element is intended for, for example `10.0.14393.1066` on Windows.
- **`os.features`** (optional): a comma-separated list of operating system features required by the element, for example `win32k` on Windows.

This convention is also used by the OCM command line command [ocm download resource -x ...](https://github.com/open-component-model/ocm/blob/main/docs/reference/ocm_download_resources.md) to download an executable for the actual runtime environment.

If platform specific images are described as separate resources instead of using a multiarch image, these extra identities should also be used.
Storage backend mappings based on OCI MAY transfer these properties into the `platform` field of OCI descriptors and vice versa.

### Build Flavor

The same version of an artifact is often built in several flavors for the same platform.
They differ in how they were built, but not in their purpose, their version or the platform they run on.
A typical example is a build that only uses a FIPS 140 validated cryptographic module, provided next to the standard build.
Such flavors should be described by the same element name and version and the following extra identity property:

- **`flavor`**: the build flavor of the element. The property MUST be omitted for the default build of an artifact.

Values SHOULD be lowercase tokens consisting of the characters `a-z`, `0-9`, `.` and `-`.
If a build combines several flavors, the tokens SHOULD be sorted lexicographically and joined with `+` (for example `debug+fips`),
so that every combination results in exactly one identity.

The flavor is not a platform property. It MUST NOT be transferred into the `platform` field of OCI descriptors, especially not into the OCI `variant` field.

The flavor SHOULD NOT be encoded into the element `version` (for example `1.2.3-fips`): following [semantic versioning](https://semver.org/#spec-item-9),
such a suffix denotes a pre-release, which is ordered before `1.2.3` and is excluded by most version constraints.
It SHOULD also not be encoded into the element `name`, as this prevents selecting all flavors of an artifact by its name.

A tool selecting an element without requesting a dedicated flavor SHOULD select the element without a `flavor` property.
A tool requesting a dedicated flavor MUST NOT fall back to another flavor or to the default build,
as, for example, an environment requiring FIPS compliance must not receive a non-compliant build.

The following values are commonly used. They are examples and not a closed set:

| Value                          | Use Case                                                                                                                                 |
|--------------------------------|------------------------------------------------------------------------------------------------------------------------------------------|
| `fips`                         | Uses only a FIPS 140 validated cryptographic module (for example the Go FIPS 140-3 module or the OpenSSL FIPS provider).                 |
| `debug`                        | Includes debug symbols, a shell or diagnostic tooling, which is omitted from the default build.                                          |
| `musl`                         | Linked against the musl C library instead of the GNU C library.                                                                          |
| `static`                       | Statically linked executable without dependencies to shared libraries.                                                                   |
| `cuda`, `rocm`                 | Built for a dedicated GPU computing platform, similar to [Python wheel variants](https://peps.python.org/pep-0817/).                     |
| `alpine`, `distroless`, `ubi`  | Container image built on top of a different base image.                                                                                  |
| `hardened`                     | Configured according to a security hardening benchmark (for example CIS benchmarks or DISA STIGs).                                       |
| `enterprise`                   | Edition with a different feature set or license.                                                                                         |

*Example:*

```yaml
resources:
  - name: ocmcli-image
    version: 0.5.0
    type: ociImage
    extraIdentity:
      architecture: amd64
      os: linux
    access: ...
  - name: ocmcli-image
    version: 0.5.0
    type: ociImage
    extraIdentity:
      architecture: amd64
      os: linux
      flavor: fips
    access: ...
```

A flavor applies to the element as a whole. If a multiarch image only contains FIPS builds, it is described by a single resource with the extra identity `flavor: fips` and without platform properties.

## Selection of Usage Scenarios

Usage scenarios for sets of described artifacts are best described by a dedicated description artifact with a dedicated tool-specific artifact type. Here, there is the complete freedom to describe the conditions and environments artifacts are to be used. The artifacts are described by [relative resource references](../05-guidelines/03-references.md#relative-artifact-references) in relation to the component version containing the description artifact.

Another possibility is to use dedicated [labels](./03-elements-sub.md#labels) to describe the usage scenario for dedicated artifacts. Here, the tool working on a component versions does not read a description artifact, but has to analyse the label settings of all the provided artifacts. In both cases there is a dedicated OCM specific interpretation of content provided by the component model. But while the first solution allows to describe a closed scenario in a dedicated resource, where resources from dependent component version can be described by relative resource references and multiple scenarios can be separated by multiple flavors of this resource, the label-based approach is restricted to a local component version and a single scenario. Instead of an artifact type for the description, labels with a defined [name structure](./03-elements-sub.md#labels) are required.
