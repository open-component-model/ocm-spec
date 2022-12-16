# Structuring Software with OCM

In this specification software products are comprised of logical units called
[**components**](../../specification/elements/README.md#components), for example frontend, backend and monitoring stack. The software product itself is then comprised of the other three components.

During the software development process new [**component versions**](../../specification/elements/README.md#component-versions)
are created.

A component version consists of a set of technical [artifacts](../../specification/elements/README.md#artifacts),
e.g. Docker images, Helm charts, binaries, configuration data etc.
Such artifacts are called **resources** in this specification.

Resources are usually built from something, e.g. code in a git repo,
named **sources** in this specification.

OCM introduces a so-called **Component Descriptor** for every
component version, that describes resources, sources and other
component versions belonging to a particular component version and
how to access them.

For each version of a component there is an own *Component Descriptor*, e.g. in our example there might be 
three component versions (and three *Component Descriptors*) for the frontend, but six component versions for the backend.

Not all component version combinations of frontend, backend and the monitoring stack are
compatible and form a valid product version. In order to define reasonable
version combinations for our software product, we could use another feature of
the *Component Descriptor*, which allows the aggregation of component versions.

For our example we could introduce an own component that describes the overall software product.
A particular version of this product component is again described by a
*Component Descriptor*, which contains references to *Component Descriptors* 
for frontend, backend and monitoring stack.

This is just one example how one can use OCM to model a software product version as a component with one *Component Descriptor* that contains references to other *Component Descriptors*, which again could have references to others and so on. You are not restricted to this approach, i.e. you could still just maintain a list of component version combinations which build a valid product release. But OCM provides a simple approach to specify what belongs to a product version. Starting with the *Component Descriptor* for a product version and following the component references, you could collect all artifacts, belonging to this product version.
