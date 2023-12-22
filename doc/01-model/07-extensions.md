# Extending the Open Component Model

The OCM specification is designed to be extended in several ways. The definition of such elements is restricted to a minimum set of attributes and may include functional behavior. It typically consists of a type attribute.

Those extension points are used to cover technology-specific aspects to be known either by dedicated implementations of the model or by applications using the model.

There are two different kinds of extensions: functional and semantic.

## Functional extensions

Functional extensions offer the possibility to enrich an implementation of the Open Component Model with technology-specific parts to support more technology environments, like storage backends for the model or artifacts described by the model.

The functional extension points are:

- [Access  specifications](../01-model/03-elements-sub.md#access-specification)
- [Signing extensions](../02-processing/03-signing.md)
- [Digest calculations](../02-processing/04-digest.md)
- [Storage backends](../03-persistence/02-mappings.md)

## Semantic extensions

Semantic extensions offer the possibility to describe the semantics and structure of an element by arbitrary types not defined by the Open Component Model itself.

Extension points are:

- Artifact types describe the meaning of an artifact independent of their technical representation in a blob format. The artifact types defined by the core model (this specification) are described in section [Artifact Types](./02-elements-toplevel.md#artifact-types)
- Dynamic attribution of artifacts with additional information is possible using labels. The meaning of label names is globally unique. Labels are defined in section [Labels](./03-elements-sub.md#labels).
