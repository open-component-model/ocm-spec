## Topics for Discussion

- Repository Context in CD
  - current schema only allows OCI-Ref, this needs to be extensible
  - Should OCI ref be part of this spec?
    
- Clarify that components are not allowed to have two version with the same number but different formats, e.g. v0.1.0 and 0.1.0

## Topics to be added to the Specification
  1. Particular types (which types are supported ?)
  2. Transport (incl. CTF)
  3. Signing (already in progress: https://github.com/gardener/ocm-spec/blob/main/doc/proposal/in-progress/07-signing.md)

## Additional chapters / sections for the Specification
- we need namespace structure for 
  - logical types in references
  - access methods/types in references
  - label names
  - short names allowed for our definitions e.g. ociImage
  Work on this topic started under https://github.com/gardener/ocm/blob/master/docs/names/README.md, linked from https://github.com/gardener/ocm. Should be moved to the ocm-spec repository and linked properly.
  
- Add a chapter with terminology (see https://github.com/openservicebrokerapi/servicebroker/blob/v2.16/spec.md#notations-and-terminology)  
  - Terminology section: beside others must describe landscape, component version, snapshot 
- add complete component descriptor example
- references in the text to the CD spec for particular entries
- List with all errors and their semantics
- Tables for presenting field descriptions (see https://github.com/openservicebrokerapi/servicebroker/blob/v2.16/spec.md)
- Tables for input export params of functions (see https://github.com/openservicebrokerapi/servicebroker/blob/v2.16/spec.md) 

- Use-Cases / Scenarios with diagrams for Component Repos
- example of local blobs with oci image not good
- better motivation of flow für upload blobs (usually first blobs then component descriptor)
- change technical artifacts to software artifacts 
