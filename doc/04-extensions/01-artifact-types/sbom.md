# SBOM

## Type Name
**`sbom`**

## Description
An SBOM is a nested inventory, a list of ingredients that make up software components (https://www.cisa.gov/sbom)

## Format Variants

- **CycloneDX** (https://cyclonedx.org/specification/overview)  

  Media Types:  
  - `application/vnd.cyclonedx+xml`  for CycloneDX files in XML format 
  - `application/vnd.cyclonedx+json`  for CycloneDX files in JSON format 

- **SPDX** (https://spdx.github.io/spdx-spec/v2.3)  

  Media Types:  
  - `text/spdx` for SPDX files in tag-value format   
  - `application/spdx+xml` for SPDX files in RDF format   
  - `application/spdx+json` for SPDX files in JSON format   
  - `application/spdx+yaml` for SPDX files in YAML format

- **SWID** ([NIST](https://csrc.nist.gov/projects/software-identification-swid/guidelines) and [ISO](https://www.iso.org/standard/65666.html))
  
  Media Types:
  - `application/swid+xml` for SWID files in XML format 
  
- **Syft** (https://github.com/anchore/syft)
  
  Media Types:
  - `application/vnd.syft+json` for Syft generated SBOMs in JSON format