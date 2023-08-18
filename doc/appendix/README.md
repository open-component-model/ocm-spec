# Appendix

The appendix describes incarnations of the various extension points
provided by the Open Component Model.

[A. Storage backend Mappings](A/README.md) <br>
[B. Access Methods](B/README.md) <br>
[C. Digest Calculation](C/README.md) <br>
[D. Signature types](D/README.md) <br>
[E. Artifact Types](E/README.md) <br>
[F. Labels](F/README.md) <br>
[G. Conventions](G/README.md) <br>
[H. Value Merge Algorithms](H/README.md) <br>

The specification is based on 4 basic functional extension points:
- The storage backend technologies to use to store OCM elements (available
  mapping specifications can be found in [appendix A](A/README.md)).
- Access to artifact content using different storage technologies. This
  is described by types access specifications (types with available
  implementations can be found in [appendix B](B/README.md)).
- Digest calculation for dedicated content technologies requiring digests different
  from standard byte sequence digests of artifact blobs (defined digest types
  can be found in [appendix C](C/README.md)).
- Defined signing extensions can be found in [appendix D](D/README.md)).

Additionally, there are two extension points for describing semantics
of artifacts:
- Formal artifact types describe the technical meaning of an artifact, 
  independent of their technical representation in a blob format (centrally
  defined types are described in [appendix E](E/README.md)).
- Dynamic attribution of artifacts with additional formal information not
  directly described by elements of the Open Component Model is possible
  with labels. The meaning of dedicated label names is globally unique
  (centrally defined label names with their meaning are defined in
  [appendix F](F/README.md)).

The provided reference implementation provides more functional
extension points to enrich and extend the functionality of the
standard library:

- *Artifact Uploaders* are used to implicitly store artifacts of dedicated types
  uploaded as local blobs in dedicated repositories.
- *Artifact Downloaders* are used to map artifact blobs to dedicated formats 
  for storing an artifact according to its type in the filesystem
- *Transport Handlers* controlling the handling of artifacts during
  transportation steps.

These extensions are not covered by this specification, because they are
specific to dedicated language bindings.
