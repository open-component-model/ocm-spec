# npm — Node Package Manager archive

## Synopsis

```text
type: npm[/VERSION]
[ATTRIBUTES]
```

## Description

Access to an NodeJS package in an NPM registry.

## Supported Media Types

- `application/x-tar`

## Specification Version

The following versions are supported

### v1

Attributes:

- **`registry`** *string*

  Base URL of the NPM registry.

- **`package`** *string*

  Name of the NPM package.

- **`version`** *string*

  Version name of the NPM package.
