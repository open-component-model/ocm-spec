
# Access Method `npm` - Access to npm packages


### Synopsis

```
type: npm/v1
```

### Description
This method implements the access of an NPM package in an NPM registry.

Supported specification version is `v1`

### Specification Versions

#### Version `v1`

The type specific specification fields are:

- **`«registry»`** *string*

  Base URL of the NPM registry.

- **`«package»`** *string*

  The name of the NPM package.

- **`«version»`** *string*

  The version name of the NPM package.
