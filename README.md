# Open Component Model (OCM)

[![REUSE status](https://api.reuse.software/badge/github.com/open-component-model/ocm-spec)](https://api.reuse.software/info/github.com/open-component-model/ocm-spec)


## Specification
1. [Model](doc/01-model/README.md)
   1. [OCM Model](doc/01-model/01-model.md#ocm-model)
      1. [Components and Component Versions](doc/01-model/01-model.md#components-and-component-versions)
      2. [Component Repositories](doc/01-model/01-model.md#component-repositories)
      3. [Summary](doc/01-model/01-model.md#summary)
   2. [Model Elements](doc/01-model/02-elements.md#model-elements)
      1. [Components and Component Versions](doc/01-model/02-elements.md#components-and-component-versions)
      2. [Artifacts (Resources and Sources)](doc/01-model/02-elements.md#artifacts-resources-and-sources)
      3. [Sources](doc/01-model/02-elements.md#sources)
      4. [Resources](doc/01-model/02-elements.md#resources)
      5. [References](doc/01-model/02-elements.md#references)
      6. [Identifiers](doc/01-model/02-elements.md#identifiers)
      7. [Access Specification](doc/01-model/02-elements.md#access-specification)
      8. [Labels](doc/01-model/02-elements.md#labels)
      9. [Prefdefined  Labels](doc/01-model/02-elements.md#predefined-labels)
      10. [Repository Contexts](doc/01-model/02-elements.md#repository-contexts)
      11. [Signatures](doc/01-model/02-elements.md#signatures)
      12. [Digest Info](doc/01-model/02-elements.md#digest-info)
      13. [Signature Info](doc/01-model/02-elements.md#signature-info)
   3. [Example for a complete Component Version](doc/01-model/03-example.md#example-for-a-complete-component-version)

2. [Processing OCM](doc/02-processing/README.md)
   1. [Referencing](doc/02-processing/01-references.md#referencing)
      1. [Absolute Artifact References](doc/02-processing/01-references.md#absolute-artifact-references)
   2. [Transport](doc/02-processing/02-transport.md#transport)
   3. [Signing](doc/02-processing/03-signing.md#signing)
      1. [Signing Algorithms](doc/02-processing/03-signing.md#signing-algorithms)
         1. [RSA](doc/02-processing/03-signing.md#rsa)
      2. [Verification Procedure](doc/02-processing/03-signing.md#verification-procedure)
         1. [Verify with RSA](doc/02-processing/03-signing.md#verify-with-rsa)
         2. [Verify with X509](doc/02-processing/03-signing.md#verify-with-x509)
   4. [Normalization](doc/02-processing/04-digest.md#normalization)
      1. [Artifact Digest](doc/02-processing/04-digest.md#artifact-digest)
      2. [Component Descriptor Digest](doc/02-processing/04-digest.md#component-descriptor-digest)
         1. [Normalization of the component-descriptor](doc/02-processing/04-digest.md#normalization-of-the-component-descriptor)
      3. [Artifact Digests](doc/02-processing/04-digest.md#artifact-digests)
      4. [Digest Algorithms](doc/02-processing/04-digest.md#digest-algorithms)
      5. [Normalization Types](doc/02-processing/04-digest.md#normalization-types)
      6. [Serialization Format](doc/02-processing/04-digest.md#serialization-format)
      7. [Recursive Digest Calculation](doc/02-processing/04-digest.md#recursive-digest-calculation)
      8. [Example](doc/02-processing/04-digest.md#example)
         1. [Simple Component-Version](doc/02-processing/04-digest.md#simple-component-version)
         2. [Component-Version With Reference](doc/02-processing/04-digest.md#component-version-with-reference)
3. [Operations](doc/03-operations/README.md)
4. [Persistence](doc/04-persistence/README.md)
5. [Glossary](doc/glossary.md)

## Contributing

Code contributions, feature requests, bug reports, and help requests are very welcome. Please refer to the [Contributing Guide in the Community repository](https://github.com/open-component-model/community/blob/main/CONTRIBUTING.md) for more information on how to contribute to OCM.

OCM follows the [CNCF Code of Conduct](https://github.com/cncf/foundation/blob/main/code-of-conduct.md).

## Licensing

Copyright 2022 SAP SE or an SAP affiliate company and Open Component Model contributors.
Please see our [LICENSE](LICENSE) for copyright and license information.
Detailed information including third-party components and their licensing/copyright information is available [via the REUSE tool](https://api.reuse.software/info/github.com/open-component-model/ocm-spec).
