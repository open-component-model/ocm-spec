# Processing Component Versions

This chapter explains how to create and use components.

1. [Referencing](01-references.md#referencing)
   1. [Relative Artifact References](01-references.md#relative-artifact-references)
   2. [Absolute Artifact References](01-references.md#absolute-artifact-references)

2. [Transport](02-transport.md#transport)

3. [Signing](03-signing.md#signing)
   1. [Signing Algorithms](03-signing.md#signing-algorithms)
      1. [RSA](03-signing.md#rsa)
   2. [Verification Procedure](03-signing.md#verification-procedure)
      1. [Verify with RSA](03-signing.md#verify-with-rsa)
      2. [Verify with X509](03-signing.md#verify-with-x509)

4. [Normalization](04-digest.md#normalization)
   1. [Artifact Digest](04-digest.md#artifact-digest)
      1. [Digest Algorithms](04-digest.md#digest-algorithms)
   2. [Normalization Types](04-digest.md#normalization-types)
   3. [Serialization Format](04-digest.md#serialization-format)
   4. [Recursive Digest Calculation](04-digest.md#recursive-digest-calculation)

5. [Example](04-digest.md#example)
   1. [Simple Component-Version](04-digest.md#simple-component-version)
   2. [Component-Version With Reference](04-digest.md#component-version-with-reference)

6. [Component Descriptor Normalization](04-digest.md#component-descriptor-normalization)
   1. [`jsonNormalisationV1` vs `jsonNormalisationV2`](04-digest.md#jsonnormalisationv1-vs-jsonnormalisationv2)
   2. [Relevant information in Component Descriptors](04-digest.md#relevant-information-in-component-descriptors)
      1. [Access Methods](04-digest.md#access-methods)
   3. [Labels](04-digest.md#labels)
   4. [Exclude Resources from Normalization/Signing](04-digest.md#exclude-resources-from-normalizationsigning)
   5. [Generic Normalization Format](04-digest.md#generic-normalization-format)
      1. [Simple Values](04-digest.md#simple-values)
      2. [Dictionary](04-digest.md#dictionary)
      3. [Lists](04-digest.md#lists)
      4. [Combined example](04-digest.md#combined-example)
      5. [Empty values:](04-digest.md#empty-values)
7. [Artifact Normalization](04-digest.md#artifact-normalization)
   1. [Blob Representation Format for Resource Types](04-digest.md#blob-representation-format-for-resource-types)
   2. [Interaction of Local Blobs, Access Methods, Uploaders and Media Types](04-digest.md#interaction-of-local-blobs-access-methods-uploaders-and-media-types)
      1. [Access Methods](04-digest.md#access-methods-1)
      2. [Blob Uploaders](04-digest.md#blob-uploaders)