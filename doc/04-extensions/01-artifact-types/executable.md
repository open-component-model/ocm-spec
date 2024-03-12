# Executable

## Type Name

**`executable`**

## Description

A blob describing an executable program. The artifact SHOULD use [extraIdentity](../../01-model/03-elements-sub.md#identifiers)
properties to describe the OS architecture and platform the program is intended for

- `os`: Operating system according to Golang property GOOS
- `architecture`: Architecture according to Golang property GOARCH

## Format Variants

Media Types:

- `application/octet-stream`
- `application/octet-stream+gzip`
