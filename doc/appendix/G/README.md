# G. Conventions

There are some conventions, which should be applied to provide a uniforms
usage accorss tools working with content provided by the component model.

These conventiones are not covered by the [model-tool contract](../../specification/contract/README.md). They are not part of the specifications
but should be obeyed to achieve some common understanding about the meaning of content.

## Intended Environments

There are several scenarios where artifacts will be provided as content of [component versions](../../specification/elements/README.md#component-versions), which might be bound to a dedicated (runtime) environment. If a component version should provide several flavors of the same artifact intended for different environments they should use the same element name (and version) and the environment should be reflected by one or more [extra identity properties](../../specification/elements/README.md#identities).

### Operating System and CPU Architecture

For executables and container images the specification for [OCI image indices](https://github.com/opencontainers/image-spec/blob/main/image-index.md#image-index-property-descriptions) should be used.

The following extra identity properties are defined:

- **`os`**: the operating system the element is intended for. It should use values listed in the Go Language document for [GOOS](https://go.dev/doc/install/source#environment).
- **`architecture`**: the CPU architecture the element is intended for. It should use values listed in the Go Language document for [GOARCH](https://go.dev/doc/install/source#environment). 

This convention is also used by the OCM command line command [ocm download resource -x ...](https://github.com/open-component-model/ocm/blob/main/docs/reference/ocm_download_resources.md) to download an executable for the actual runtime environment.

If platform specific images are described as separate resources instead of using a multiarch image, these extra identities should be used, also. 

## Selection of Usage Scenarios

Usage scenarios for sets of described artifacts are best described by a dedicated [description artifacts](../../specification/contract/README.md#how-does-it-look-like-in-the-open-component-model) with a dedicated tool-specific artifact type. Here, there is the complete freedom to describe the conditions and environments artifacts are to be used. The artifacts are described by [relative resource references](../../specification/elements/README.md#artifact-references) in relation to the component version containing the description artifact.

Another possibility is to use dedicated [labels](../../specification/elements/README.md#labels) to describe the usage scenario for dedicated artifacts. Here, the tool working on a component versions does not read a description artifact, but has to analyse the label settings of all the provided artifacts. In both cases there is a dedicated OCM specific interpretation of content provided by the component model. But while the first solution allows to describe a closed scenario in a dedicated resource, where resources from dependent component version can be described by relative resource references and multiple scenarios can be separated by multiple flavors of this resource, the label-based approach is restricted to a local component version and a single scenario. Instead of an artifact type for the description, labels with a defined [name structure](../../specification/formats/types.md#label-names) are required.
