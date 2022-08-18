# 2.5 Extension Points for the Open Component Model Specification

The specification described in the former sections open some
extension points. Extension points are specifications, which are
restricted to a minimum set of attributes typically including an arbitrary
specification type attribute intended to be refined by dedicated type
incarnations.

Those extension points are used to cover technology-specific aspects,
which are handled in generic and technology-agnostic manner by the core model,
but must be known either by dedicated implementations of the model, or
by applications using the model.

There are two different kinds of extension points:

- [functional](functional.md) extension points offer the possibility to
  enrich an implementation of the Open Component Model by technology specific
  parts to support more technology environments, like storage backends for
  the model information or artefacts described by the model.
- [semantic](semantic.md) extension points offer the possibility to
  describe the semantic and/or structure of an element by arbitrary types not
  statically defined as part of the Open Component Model itself.
