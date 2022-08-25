# Functional Extension Points of the Open Component Model Specification

The specification is based on 4 basic functional extension points:
- The [storage backend technologies](../layer3/README.md) to use to store OCM
  elements (available
  mapping specifications can be found in [appendix A](../../appendix/A/README.md)).
- [Access to artefact content](../layer1/README.md#artefact-access) using
  different storage technologies. This is described by types access
  specifications (types with available implementations can be found in
  [appendix B](../../appendix/B/README.md)).
- [Digest](../layer1/README.md#digests) calculation for dedicated content
  technologies requiring digests different from standard byte sequence digests
  of artefact blobs (defined digest types can be found in
  [appendix C](../../appendix/C/README.md)).
- Defined [signing](../layer1/README.md#signing) extensions can be found in
  [appendix D](../../appendix/D/README.md)).