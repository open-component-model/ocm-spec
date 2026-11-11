# Executable

## Type Name

**`executable`**

## Description

A blob describing an executable program. The artifact SHOULD use [extraIdentity](../../01-model/03-elements-sub.md#element-identity)
properties to describe the OS architecture and platform the program is intended for
(see [Operating System and CPU Architecture](../../01-model/06-conventions.md#operating-system-and-cpu-architecture))

- `os`: Operating system according to Golang property GOOS
- `architecture`: Architecture according to Golang property GOARCH
- `variant` (optional): Variant of the CPU architecture according to the OCI image index specification

Different builds of the same executable for the same platform (for example FIPS compliant builds) SHOULD be distinguished by the
[`flavor`](../../01-model/06-conventions.md#build-flavor) extra identity property.

## Format Variants

Media Types:

- `application/octet-stream`
- `application/octet-stream+gzip`
