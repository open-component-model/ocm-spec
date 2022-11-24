# Structuring of Software with OCM

Software products are divided into logical units, which are called
[**components**](../../specification/elements/README.md#components) in this
specification. For example, a frontend, a backend and some
monitoring stack. The software product itself could be seen as a
component comprising the other three components.

As a result of the development phase, [**component versions**](../../specification/elements/README.md#component-versions)
are created, e.g. when you make a new release of a component.

A component version consists of a set of technical [artifacts](../../specification/elements/README.md#artifacts),
e.g. docker images, helm charts, binaries, configuration data etc.
Such artifacts are called **resources** in this specification.

Resources are usually build from something, e.g. code in a git repo,
named **sources** in this specification.

The OCM introduces a so called **Component Descriptor** for every
component version, to describe the resources, sources and other
component versions belonging to a particular component version and
how these could be accessed.

For the three components in our example software product,
one *Component Descriptor* exists for every component version,
e.g. three *Component Descriptors* for the three versions of the frontend,
six for the six versions of the backend etc.

Not all component version combinations of frontend, backend and monitoring are
compatible and build a valid product version. In order to define reasonable
version combinations for our software product, we could use another feature of
he *Component Descriptor*, which allows the aggregation of component versions.

For our example we could introduce a component for the overall product.
A particular version of this product component is again described by a
*Component Descriptor*, which contains references to particular
*Component Descriptors* for the frontend, backend and monitoring.

This is only one example how to describe a particular product version with OCM as a component with one *Component Descriptor* having references to other *Component Descriptors*, which itself could have such references and so on. You are not restricted to this approach, i.e. you could still just maintain a list of component version combinations which build a valid product release. But OCM provides you a simple approach to specify what belongs to a product version. Starting with the *Component Descriptor* for a product version and following the component references, you could collect all artifacts, belonging to this product version.
