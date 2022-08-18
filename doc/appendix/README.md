# Appendix

The appendix describes incarnations of the various extension points
provided by the Open Component Model.

[A. Storage backend Mappings](A/README.md) <br>
[B. Access Methods](B/README.md) <br>
[C. Digest Calculation](C/README.md) <br>
[D. Signature types](E/README.md) <br>

[E. Artefact Types](F/README.md) <br>
[F. Labels](F/README.md) <br>

The specification is based on 2 basic functional extension points:
- The storage backend technologies to use to store OCM elements (available
  mapping specifications can be found in [appendix A](A/README.md)).
- Access to artefact content using different storage technologies. This
  is described by types access specifications (types with available
  implementations can be found in [appendix B](B/README.md)).
- Digest calculation for dedicated content technologies requiring digests different
  from standard byte sequence digests of artefact blobs (defined digest types
  can be found in [appendix C](C/README.md)).
- Defined signing extensions can be found in [appendix D](D/README.md)).

Additionally, there are two extension points for describing semantics
of artefacts:
- Formal artefact types describe the technical meaning of an artefact, 
  independent of their technical representation in a blob format (centrally
  defined types are described in [appendix E](E/README.md)).
- Dynamic attribution of artefacts with additional formal information not
  directly described by elements of the Open Component Model is possible
  with labels. The meaning of dedicated label names is globally unique
  (centrally defined label names with their meaning are defined in
  [appendix F](F/README.md)).

The provided reference implementation provides more functional
extension points to enrich and extend the functionality of the
standard library:

- *Artefact Uploaders* are used to implicitly store artefacts of dedicated types
  uploaded as local blobs in dedicated repositories.
- *Artefact Downloaders* are used to map artefact blobs to dedicated formats 
  for storing an artefact according to its type in the filesystem
- *Transport Handlers* controlling the handling of artefacts during
  transportation steps.

These extensions are not covered by this specification, because they are
specific to dedicated language bindings.